"""Build a neutral-only UTF-8 publication snapshot, never traverse private roots."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

TOP_FILES = {'README.md', 'SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', '.gitignore',
             'CHANGELOG.md', 'requirements-extraction.txt'}
PREFIXES = ('assets/blueprint/', 'assets/entries/', 'references/', 'scripts/', 'agents/', '.github/workflows/')
EXCLUDED = {'.git', '_archive', '__pycache__', '.venv', 'node_modules', '_extracted'}
PRIVATE_PATH = re.compile(r'(?:^|/)(?:instances|_inbox|_extracted|_archive)(?:/|$)')
LEAK = re.compile(r'(?:[A-Z]:[\\/](?:Users|OneDrive)[\\/](?!OWNER|example)[A-Za-z0-9_. -]+|[\w.+-]+@(?:gmail|hotmail|outlook)\.com|RFQ[-]20\d{2}[-]\d+|comet_message_id[=]\d+|agent_[a-z0-9]{8,}|gh[oprsu]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,})', re.I)

def allowed(path):
    if path == 'assets/instance.example.json':
        return True
    return path in TOP_FILES or path.startswith(PREFIXES)

def collect(source):
    source = Path(source).resolve()
    records = []
    for p in sorted(source.rglob('*')):
        rel = p.relative_to(source).as_posix()
        if any(part in EXCLUDED for part in p.relative_to(source).parts):
            continue
        if not p.is_file():
            continue
        if p.is_symlink() or not p.resolve().is_relative_to(source):
            raise ValueError('Publication source is a symlink/outside root: ' + rel)
        if not allowed(rel):
            raise ValueError('Unallowlisted publication path: ' + rel)
        # Neutral blueprint inbox contracts are intentional templates, not inputs.
        if PRIVATE_PATH.search(rel) and not rel.startswith('assets/blueprint/'):
            raise ValueError('Private/source intake path refused: ' + rel)
        raw = p.read_bytes()
        text = raw.decode('utf-8-sig')
        if LEAK.search(text):
            raise ValueError('Private source or credential marker refused: ' + rel)
        records.append({'path': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
    if not any(r['path'] == 'CHANGELOG.md' for r in records):
        raise ValueError('A verified improvement snapshot requires CHANGELOG.md')
    return records

def build(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.is_relative_to(source):
        raise ValueError('Snapshot output must be outside the public source tree')
    records = collect(source)
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {'schema_version': 1, 'scope': 'neutral-public-package', 'files': records,
                'content_hash': hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()}
    temporary = destination / 'SYNC_BUNDLE.tmp'
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for record in records:
            archive.write(source / record['path'], record['path'])
        archive.writestr('SYNC_MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
    temporary.replace(destination / 'SYNC_BUNDLE.zip')
    manifest['bundle_sha256'] = hashlib.sha256((destination / 'SYNC_BUNDLE.zip').read_bytes()).hexdigest()
    (destination / 'SYNC_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = build(args.source, args.output)
    print(json.dumps({'files': len(result['files']), 'content_hash': result['content_hash'], 'bundle_sha256': result['bundle_sha256']}))

if __name__ == '__main__':
    main()
