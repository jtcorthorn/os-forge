"""Preview or apply a root-scoped, backed-up file relocation plan; never overwrite."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def inside(root, path):
    resolved = path.resolve()
    if resolved == root or not resolved.is_relative_to(root):
        raise ValueError(f'Path must be strictly inside recipient root: {path}')
    cursor = path.absolute()
    while cursor != root and cursor != cursor.parent:
        if cursor.is_symlink() or getattr(cursor, 'is_junction', lambda: False)():
            raise ValueError(f'Symlink/junction is not an ordinary file path: {cursor}')
        cursor = cursor.parent
    return resolved


def relative(root, value):
    if not isinstance(value, str):
        raise ValueError('Plan paths must be strings')
    value = value.replace('\\', '/')
    if not value or value.startswith('/') or ':' in value or any(
        p in {'', '.', '..'} for p in value.split('/')
    ):
        raise ValueError(f'Invalid relative path: {value}')
    path = inside(root, root / value)
    # Fail rather than guess on filesystem case aliases, including on Linux.
    cursor = root
    for part in Path(value).parts:
        if cursor.is_dir():
            aliases = [p.name for p in cursor.iterdir() if p.name.casefold() == part.casefold()]
            if aliases and aliases != [part]:
                raise ValueError(f'Case-ambiguous path: {value}')
        cursor = cursor / part
    return path


def matches(path, row):
    return path.is_file() and path.stat().st_size == row['size_bytes'] and digest(path) == row['sha256']


def save_json(path, data):
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('w', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def relocate(root, plan_path, run_dir, apply=False):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError('Recipient root must already exist')
    plan_path, run_dir = inside(root, plan_path), inside(root, run_dir)
    data = json.loads(plan_path.read_text(encoding='utf-8-sig'))
    if data.get('schema_version') != 1 or not isinstance(data.get('files'), list) or not data['files']:
        raise ValueError('Expected schema_version=1 and a nonempty files list')
    rows = []
    old_keys, new_keys, prefixes = set(), set(), {}
    for item in data['files']:
        old, new = relative(root, item['old']), relative(root, item['new'])
        row = {'old': old.relative_to(root).as_posix(), 'new': new.relative_to(root).as_posix(),
               'size_bytes': item['size_bytes'], 'sha256': item['sha256']}
        if not isinstance(row['size_bytes'], int) or isinstance(row['size_bytes'], bool) or row['size_bytes'] < 0:
            raise ValueError('size_bytes must be a measured nonnegative integer')
        if not isinstance(row['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', row['sha256']):
            raise ValueError('sha256 must be the measured lowercase 64-digit digest')
        a, b = row['old'].casefold(), row['new'].casefold()
        if a in old_keys or b in new_keys or a == b:
            raise ValueError('Duplicate/case-colliding source or destination')
        old_keys.add(a)
        new_keys.add(b)
        for p in (old, new):
            if p == plan_path or p == run_dir or p.is_relative_to(run_dir) or run_dir.is_relative_to(p):
                raise ValueError('Plan and run directory cannot overlap moved files')
        parent = new.parent
        while parent != root:
            if parent.exists() and not parent.is_dir():
                raise ValueError('Destination parent is an existing file')
            parent = parent.parent
        parts = Path(row['new']).parts
        for i in range(1, len(parts) + 1):
            spelling = '/'.join(parts[:i])
            prior = prefixes.setdefault(spelling.casefold(), spelling)
            if prior != spelling:
                raise ValueError('Case-colliding destination directory names')
        rows.append(row)
    if old_keys & new_keys:
        raise ValueError('Source/destination overlap or cyclic relocation is not supported')
    # A destination cannot be an ancestor of another planned destination file.
    for key in new_keys:
        if any('/'.join(key.split('/')[:i]) in new_keys for i in range(1, len(key.split('/')))):
            raise ValueError('A planned destination file is another destination parent')

    fingerprint = digest(plan_path)
    receipt_path = run_dir / 'receipt.json'
    receipt = None
    if run_dir.exists():
        inside(root, receipt_path)
        if not receipt_path.is_file():
            raise ValueError('Existing run directory has no receipt; choose a new run directory')
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        if receipt.get('plan_sha256') != fingerprint or receipt.get('files') != rows:
            raise ValueError('Run directory belongs to a different plan')
    states = []
    for row in rows:
        old, new = relative(root, row['old']), relative(root, row['new'])
        if old.exists():
            if new.exists() or not matches(old, row):
                raise ValueError(f'Source changed or destination occupied: {row["old"]}')
            states.append('pending')
        elif receipt and matches(new, row) and matches(inside(root, run_dir / 'originals' / row['sha256']), row):
            states.append('moved')
        else:
            raise ValueError(f'Original missing or incomplete recovery evidence: {row["old"]}')
    result = {'files': len(rows), 'bytes': sum(r['size_bytes'] for r in rows),
              'already_moved': states.count('moved'), 'pending': states.count('pending'),
              'applied': False, 'coverage': 'File bytes only; active referrers require separate repair/checks.'}
    if not apply:
        return result

    run_dir.parent.mkdir(parents=True, exist_ok=True)
    if receipt is None:
        run_dir.mkdir()  # exclusive reservation; never adopt an unrelated directory
        receipt = {'schema_version': 1, 'plan_sha256': fingerprint, 'files': rows, 'states': states}
        save_json(receipt_path, receipt)
    lock = run_dir / 'apply.lock'
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.close(descriptor)
    try:
        originals = inside(root, run_dir / 'originals')
        originals.mkdir(exist_ok=True)
        # Verify all backups before the first source mutation.
        for row, state in zip(rows, states):
            backup = inside(root, originals / row['sha256'])
            if backup.exists():
                if not matches(backup, row):
                    raise ValueError(f'Backup differs: {row["old"]}')
            elif state == 'pending':
                source = relative(root, row['old'])
                if not matches(source, row):
                    raise ValueError(f'Concurrent source change: {row["old"]}')
                with source.open('rb') as src, backup.open('xb') as dst:
                    shutil.copyfileobj(src, dst)
                if not matches(backup, row):
                    raise IOError(f'Backup verification failed: {row["old"]}')
            else:
                raise ValueError('A moved file has no verified backup')
        for i, (row, state) in enumerate(zip(rows, states)):
            if state == 'moved':
                continue
            old, new = relative(root, row['old']), relative(root, row['new'])
            if new.exists() or not matches(old, row):
                raise ValueError(f'Concurrent modification: {row["old"]}')
            new.parent.mkdir(parents=True, exist_ok=True)
            if old.stat().st_dev != new.parent.stat().st_dev:
                raise ValueError('Cross-filesystem move is unsupported; originals and backups are preserved')
            os.rename(old, new)
            if not matches(new, row):
                raise IOError(f'Destination verification failed: {row["new"]}')
            states[i] = 'moved'
            receipt['states'] = states
            save_json(receipt_path, receipt)
        receipt['states'] = states
        receipt['complete'] = True
        save_json(receipt_path, receipt)
        after = run_dir / 'inventory_after.csv'
        if not after.exists():
            with after.open('x', encoding='utf-8-sig', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=['relative_path', 'size_bytes', 'sha256'])
                writer.writeheader()
                writer.writerows({'relative_path': r['new'], 'size_bytes': r['size_bytes'],
                                  'sha256': r['sha256']} for r in rows)
        result.update(applied=True, verified_files=len(rows), receipt=str(receipt_path), inventory_after=str(after))
        return result
    finally:
        lock.unlink()  # only our own transient lock; no user/original file is removed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(relocate(args.root, args.plan, args.run_dir, args.apply), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f'Relocation stopped: {error}\n')
