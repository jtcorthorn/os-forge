"""Inventory explicitly named recipient source paths, keeping evidence in that recipient OS."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

def inventory(root, sources, output):
    root = root.resolve()
    output = output.resolve()
    if not output.is_relative_to(root):
        raise ValueError('Source inventories must stay inside the recipient OS')
    if output.exists():
        raise FileExistsError('Choose a new dated filename; existing inventory is preserved')
    files = set()
    coverage = []
    for relative in sources:
        source = (root / relative).resolve()
        if source == root or not source.is_relative_to(root):
            raise ValueError('Name explicit source files/folders inside the recipient OS')
        if not source.exists():
            raise FileNotFoundError(source)
        selected = [source] if source.is_file() else [p for p in source.rglob('*') if p.is_file()]
        coverage.append({'source':relative,'files_found':len(selected)})
        for path in selected:
            if not path.resolve().is_relative_to(root):
                raise ValueError('Source link escapes recipient OS')
        files.update(selected)
    rows = []
    for path in sorted(files,key=lambda p:str(p).casefold()):
        row = {'relative_path':path.relative_to(root).as_posix(), 'size_bytes':'',
               'extension':path.suffix.lower(), 'modified_utc':'', 'sha256':'','hash_status':'ok'}
        try:
            stat = path.stat()
            row['size_bytes'] = stat.st_size
            from datetime import timezone
            row['modified_utc'] = datetime.fromtimestamp(stat.st_mtime,timezone.utc).isoformat()
            digest = hashlib.sha256()
            with path.open('rb') as handle:
                for block in iter(lambda:handle.read(1024*1024),b''):
                    digest.update(block)
            row['sha256'] = digest.hexdigest()
        except OSError as error:
            row['hash_status'] = type(error).__name__
        rows.append(row)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=['relative_path','size_bytes','extension','modified_utc','sha256','hash_status'])
        writer.writeheader()
        writer.writerows(rows)
    return {'coverage':coverage,'files':len(rows),'read_errors':sum(r['hash_status']!='ok' for r in rows),
            'output':str(output),'content_review':'not performed','captured':datetime.now().astimezone().isoformat()}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--source',action='append',required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result=inventory(a.root,a.source,a.output)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(2 if result['read_errors'] else 0)
