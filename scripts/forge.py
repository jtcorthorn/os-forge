"""OS Forge: stdlib-only, preview-first, conflict-aware snapshot deployment."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

FACTORY = Path(__file__).resolve().parents[1]
VERSION = '1.0.0'

def blueprint_root():
    return FACTORY / 'assets' / 'blueprint'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def contained(root, relative):
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes root: {relative}')
    return candidate

def read_json(path, fallback):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else fallback

def render(config):
    blueprint = blueprint_root()
    result = {}
    for path in sorted(blueprint.rglob('*')):
        if not path.is_file():
            continue
        # Workshop history and interpreter caches are not recipient templates.
        if any(part in {'_archive', '__pycache__', '.git'} for part in path.relative_to(blueprint).parts):
            continue
        if path.suffix.lower() in {'.pyc', '.pyo'}:
            continue
        relative = path.relative_to(blueprint).as_posix()
        data = path.read_bytes()
        if path.suffix.lower() in {'.md', '.txt', '.json', '.yaml', '.yml'}:
            text = data.decode('utf-8-sig').replace('{{OWNER}}', config['owner'])
            if '{{OWNER}}' in text:
                raise ValueError(f'Unresolved owner token: {relative}')
            data = text.encode('utf-8')
        result[relative] = data
    entry_language = config.get('entry_language', 'es')
    if entry_language not in {'es', 'en'}:
        raise ValueError('entry_language supports es/en; translate other owner-facing languages locally')
    if entry_language == 'en':
        entry = (FACTORY / 'assets' / 'entries' / 'en.md').read_text(encoding='utf-8-sig')
        result['EMPIEZA_AQUI.md'] = entry.replace('{{OWNER}}', config['owner']).encode('utf-8')
    for relative, extra in config.get('append', {}).items():
        contained(blueprint, relative)
        if relative not in result:
            raise ValueError(f'Append target absent from blueprint: {relative}')
        result[relative] += ('\n' + extra.strip() + '\n').encode('utf-8')
    # Intake is recipient-owned when supplied. A generic starter supports future recipients.
    if not config.get('external_intake', False):
        result['00_System/Intake/MAPA.md'] = b'# Intake\n\nNo sources have been supplied. Read CONTEXT.md, then use the owner profile to choose one useful first task.\n'
        result['00_System/Intake/CONTEXT.md'] = b'# Intake contract\n\nInputs: owner-supplied original files. Work: inventory relative paths, dates, formats and read failures; inspect task-relevant content. Outputs: generated source index and source-linked orientation. Human boundary: preserve originals and distinguish facts from inference. No cross-person data copies.\n'
    return result

def plan(config, target):
    expected = render(config)
    manifest = read_json(target / '_meta/forge-manifest.json', {'files': {}})
    old = manifest.get('files', {})
    rows = []
    # Detect case-fold collisions even when running on a case-sensitive host.
    folded = {}
    for rel in expected:
        key = rel.casefold()
        if key in folded:
            raise ValueError(f'Case collision: {folded[key]} and {rel}')
        folded[key] = rel
    for rel, data in expected.items():
        dest = contained(target, rel)
        incoming = sha(data)
        if not dest.exists():
            state = 'add'
            current = None
        elif not dest.is_file():
            state, current = 'conflict', None
        else:
            current = sha(dest.read_bytes())
            baseline = old.get(rel, {}).get('sha256')
            if baseline is None:
                state = 'conflict'
            elif current == incoming:
                state = 'unchanged'
            elif incoming == baseline:
                state = 'kept-local'
            elif current == baseline:
                state = 'update'
            else:
                state = 'conflict'
        rows.append({'path': rel, 'action': state, 'current_sha256': current,
                     'incoming_sha256': incoming})
    for rel in sorted(set(old) - set(expected)):
        rows.append({'path': rel, 'action': 'retained-upstream-removal'})
    return expected, manifest, rows

def unique_archive(target):
    base = target / '_archive' / 'forge' / datetime.now().strftime('%Y-%m-%d')
    dest, n = base, 2
    while dest.exists():
        dest = base.with_name(base.name + f'_v{n}')
        n += 1
    return dest

def deploy(config, target, apply=False):
    target = target.resolve()
    blueprint = blueprint_root().resolve()
    if target == FACTORY or target.is_relative_to(FACTORY) or FACTORY.is_relative_to(target):
        raise ValueError('Deployment must be outside the factory and its ancestor folders')
    expected, previous, rows = plan(config, target)
    counts = {action: sum(r['action'] == action for r in rows) for action in sorted({r['action'] for r in rows})}
    conflicts = [r['path'] for r in rows if r['action'] == 'conflict']
    summary = {'target': str(target), 'version': VERSION, 'applied': False,
               'counts': counts, 'conflicts': conflicts}
    if not apply:
        return summary
    if conflicts:
        summary['blocked'] = 'No files changed: resolve local/unmanaged conflicts before applying.'
        return summary
    changed = [r for r in rows if r['action'] in {'add', 'update'}]
    manifest_path = contained(target, '_meta/forge-manifest.json')
    removals = [r['path'] for r in rows if r['action'] == 'retained-upstream-removal']
    if not changed and not removals and manifest_path.exists():
        summary['applied'] = True
        summary['no_op'] = True
        return summary
    # Recheck actual bytes immediately before mutations. No overwrite of raced local edits.
    for r in rows:
        if 'current_sha256' not in r:
            continue
        dest = contained(target, r['path'])
        now = sha(dest.read_bytes()) if dest.is_file() else None
        if now != r['current_sha256'] or (r['action'] == 'add' and dest.exists()):
            raise RuntimeError(f'Concurrent modification: {r["path"]}')
    archive = unique_archive(target)
    if manifest_path.exists():
        archive.mkdir(parents=True, exist_ok=True)
        shutil.copy2(manifest_path, archive / 'forge-manifest.json')
    for r in changed:
        dest = contained(target, r['path'])
        if r['action'] == 'update':
            backup = contained(archive, r['path'])
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, backup)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(expected[r['path']])
        if sha(dest.read_bytes()) != r['incoming_sha256']:
            raise IOError(f'Write verification failed: {r["path"]}')
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {'version': VERSION, 'owner': config['owner'],
                'deployed_at': datetime.now().astimezone().isoformat(),
                'files': {rel: {'sha256': sha(data)} for rel, data in expected.items()},
                'retained_upstream_removals': sorted(set(previous.get('retained_upstream_removals', [])) | set(removals))}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    summary['applied'] = True
    summary['verified_files'] = len(changed)
    return summary

def verify(target):
    target = target.resolve()
    manifest = read_json(target / '_meta/forge-manifest.json', {'files': {}})
    missing, modified, broken, unresolved, long_maps, external = [], [], [], [], [], []
    # Only generated/current OS documentation, never text hidden in recipient original folders.
    roots = [target / p for p in ('00_System','10_Finances','20_Ventures','30_Projects',
             '40_Health','50_Learning','60_Travel','70_Records','80_Library','90_Archive','_templates','_inbox')]
    docs = [p for p in target.glob('*.md')]
    docs += [p for root in roots if root.exists() for p in root.rglob('*.md')]
    for rel, item in manifest['files'].items():
        p = contained(target, rel)
        if not p.is_file(): missing.append(rel)
        elif sha(p.read_bytes()) != item['sha256']: modified.append(rel)
    for p in docs:
        # Retained snapshots keep their historical links; only active routes
        # determine navigation readiness. Managed-byte checks above still apply.
        if '_archive' in p.relative_to(target).parts:
            continue
        text = p.read_text(encoding='utf-8-sig')
        if '{{OWNER}}' in text: unresolved.append(p.relative_to(target).as_posix())
        if p.name == 'MAPA.md' and len(text.splitlines()) > 60:
            long_maps.append(p.relative_to(target).as_posix())
        for link in re.findall(r'\]\((<[^>]+>|[^)]+)\)',text):
            link = link.strip().strip('<>')
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',link) or link.startswith('#'):
                continue
            link = unquote(link.split('#')[0])
            if not link: continue
            destination = (p.parent / link).resolve()
            if not destination.is_relative_to(target):
                external.append({'file':p.relative_to(target).as_posix(),'link':link})
            if not destination.exists():
                broken.append({'file':p.relative_to(target).as_posix(),'link':link})
    return {'target':str(target),'managed_files':len(manifest['files']), 'markdown_checked':len(docs),
            'missing_managed':missing,'locally_modified':modified,'broken_links':broken,
            'outside_root_links':external,'unresolved_tokens':unresolved,'maps_over_60_lines':long_maps,
            'runtime_adoption':'not verified','cloud_permissions':'not verified',
            'pass':bool(manifest['files']) and not (missing or broken or unresolved or external or long_maps)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    d = sub.add_parser('deploy')
    d.add_argument('--config',type=Path,required=True)
    d.add_argument('--target',type=Path,required=True)
    d.add_argument('--apply',action='store_true')
    v = sub.add_parser('verify')
    v.add_argument('--target',type=Path,required=True)
    args = parser.parse_args()
    result = deploy(read_json(args.config,{}),args.target,args.apply) if args.command=='deploy' else verify(args.target)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result.get('conflicts') or result.get('pass') is False:
        raise SystemExit(2)

if __name__=='__main__': main()
