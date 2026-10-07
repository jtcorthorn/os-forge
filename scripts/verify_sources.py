"""Compare a preserved source inventory to actual bytes without changing either."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

def verify(root, inventory, prefix=''):
    root = root.resolve()
    errors = []
    count = total = 0
    with inventory.open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            path = (root / prefix / row['relative_path']).resolve()
            if not path.is_relative_to(root):
                errors.append({'path':row['relative_path'],'error':'outside-root'})
                continue
            count += 1
            try:
                digest = hashlib.sha256()
                with path.open('rb') as handle:
                    for block in iter(lambda:handle.read(1024*1024),b''):
                        digest.update(block)
                size = path.stat().st_size
                expected_size = int(row.get('size_bytes',row.get('bytes','-1')))
                if digest.hexdigest() != row['sha256'] or size != expected_size:
                    errors.append({'path':row['relative_path'],'error':'content-or-size-changed'})
                total += size
            except OSError as exc:
                errors.append({'path':row['relative_path'],'error':type(exc).__name__})
    return {'files_compared':count,'bytes_compared':total,'errors':errors,'pass':count>0 and not errors,
            'coverage':'Only files listed in the supplied baseline inventory; no claim about unlisted files or cloud state.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--inventory',type=Path,required=True)
    p.add_argument('--prefix',default='')
    args=p.parse_args()
    result=verify(args.root,args.inventory,args.prefix)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['pass'] else 2)
