"""Discover owning-scope improvement sources without assuming absent work is done."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

SKIP = {'.git', '_archive', 'archive', 'node_modules', '__pycache__', '_extracted', '_site', 'runtime', '.venv'}
NAME = re.compile(r'improvement|proposal|pending[-_]edits|backlog|handoff|mejora', re.I)

def discover(root, scopes, canary=None):
    root = Path(root).resolve()
    sources, errors = [], []
    for scope in scopes:
        relative = Path(scope)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Scopes must remain inside the authorized root')
        start = (root / relative).resolve()
        if not start.is_relative_to(root) or not start.is_dir():
            errors.append({'scope': scope, 'error': 'missing or outside authorized root'})
            continue
        def failed(err):
            errors.append({'scope': scope, 'error': str(err)})
        for parent, dirs, files in os.walk(start, onerror=failed, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d.lower() not in SKIP and not (Path(parent) / d).is_symlink())
            for name in sorted(files):
                p = Path(parent) / name
                rel = p.relative_to(root).as_posix()
                if p.suffix.lower() != '.md' or not (NAME.search(name) or 'proposals' in p.parts or 'handoffs' in p.parts):
                    continue
                try:
                    if p.is_symlink():
                        raise ValueError('symlink source not followed')
                    raw = p.read_bytes()
                    raw.decode('utf-8-sig')
                    sources.append({'path': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
                except (OSError, UnicodeError, ValueError) as err:
                    errors.append({'path': rel, 'error': str(err)})
    sources = sorted({s['path']: s for s in sources}.values(), key=lambda s: s['path'])
    if canary and not any(s['path'] == canary for s in sources):
        errors.append({'path': canary, 'error': 'known proposal canary missing from inspected coverage'})
    return {'status': 'incomplete' if errors else 'complete_for_declared_scopes', 'scopes': scopes,
            'sources': sources, 'errors': errors, 'exclusions': sorted(SKIP)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--scope', action='append', required=True)
    parser.add_argument('--canary')
    args = parser.parse_args()
    result = discover(args.root, args.scope, args.canary)
    print(json.dumps(result, indent=2))
    return int(result['status'] == 'incomplete')

if __name__ == '__main__':
    raise SystemExit(main())
