"""Validate a neutral snapshot and prepare additive Git tree changes without network writes."""
from __future__ import annotations
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath
from build_sync_bundle import allowed, LEAK


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def verify(bundle, manifest):
    bundle = Path(bundle)
    if hashlib.sha256(bundle.read_bytes()).hexdigest() != manifest['bundle_sha256']:
        raise ValueError('Bundle hash mismatch')
    files = manifest['files']
    if hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest() != manifest['content_hash']:
        raise ValueError('Content identity mismatch')
    expected = {r['path']: r for r in files}
    if len(expected) != len(files) or len(files) > 1000:
        raise ValueError('Duplicate or excessive source paths')
    results = {}
    with zipfile.ZipFile(bundle) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected) | {'SYNC_MANIFEST.json'}:
            raise ValueError('Archive members do not match manifest')
        if sum(i.file_size for i in archive.infolist()) > 50_000_000:
            raise ValueError('Archive exceeds bounded content size')
        inner = json.loads(archive.read('SYNC_MANIFEST.json'))
        if inner['files'] != files or inner['content_hash'] != manifest['content_hash']:
            raise ValueError('Inner manifest mismatch')
        for name, record in expected.items():
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name or not allowed(name):
                raise ValueError('Unsafe/unallowlisted archive path: ' + name)
            raw = archive.read(name)
            if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
                raise ValueError('Source bytes mismatch: ' + name)
            text = raw.decode('utf-8')
            if LEAK.search(text):
                raise ValueError('Source/credential marker: ' + name)
            results[name] = {'path': name, 'mode': '100644', 'type': 'blob', 'content': text,
                             'git_blob_sha1': git_blob(raw)}
    return results


def prepare(bundle, manifest, remote, baseline, protected=()):
    files = verify(bundle, manifest)
    if remote.get('truncated') is not False:
        raise ValueError('Remote tree coverage incomplete')
    current = {r['path']: r['sha'] for r in remote['tree'] if r['type'] == 'blob'}
    prior = {r['path']: r['git_blob_sha1'] for r in baseline['files']}
    changes = []
    for name, row in files.items():
        if current.get(name) == row['git_blob_sha1']:
            continue
        if any(name == p or name.startswith(p.rstrip('/') + '/') for p in protected):
            raise ValueError('Protected publication control changed: ' + name)
        if name in current and current[name] != prior.get(name):
            raise ValueError('Remote file changed outside the verified baseline: ' + name)
        if name not in current and name in prior:
            raise ValueError('Remote source removal needs reconciliation: ' + name)
        changes.append(row)
    if changes and not any(r['path'] == 'CHANGELOG.md' for r in changes):
        raise ValueError('Changed snapshot requires a new verified changelog entry')
    # Base-tree construction deliberately retains remote-only and source-removed files.
    return {'changes': changes, 'retained_remote_paths': sorted(set(current) - set(files)),
            'content_hash': manifest['content_hash'], 'no_op': not changes}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--bundle', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--remote', required=True)
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--protected', action='append', default=[])
    args = parser.parse_args()
    read = lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
    plan = prepare(args.bundle, read(args.manifest), read(args.remote), read(args.baseline), args.protected)
    Path(args.output).write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'changes': len(plan['changes']), 'retained_remote_paths': len(plan['retained_remote_paths']), 'no_op': plan['no_op']}))
