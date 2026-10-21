#!/usr/bin/env python3
"""Portable skill inspection and explicit runtime evidence. No package mutation or scheduler."""
import argparse
import base64
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import shutil
import sys
import time
import urllib.request

IGNORE = {'.git', '_archive', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'node_modules'}


def sha(raw): return hashlib.sha256(raw).hexdigest()
def git_sha(raw): return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def within(root, relative):
    rel = PurePosixPath(relative)
    if rel.is_absolute() or '..' in rel.parts or '\\' in relative or ':' in relative:
        raise ValueError('Unsafe relative package path')
    p = (root/relative).resolve()
    if not p.is_relative_to(root.resolve()): raise ValueError('Path escaped package')
    return p


def file_ref(path):
    p = path.resolve(strict=True)
    if not p.is_file(): raise ValueError('Expected a real file')
    return {'path': str(p), 'sha256': sha(p.read_bytes())}


def package(root):
    root = root.resolve(strict=True)
    found, total = {}, 0
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE)
        for d in dirs:
            p = Path(parent)/d
            if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
                raise ValueError('Linked directory outside inspection coverage')
        for name in sorted(files):
            if name.endswith(('.pyc', '.pyo')): continue
            p = Path(parent)/name
            if p.is_symlink(): raise ValueError('Linked file outside inspection coverage')
            before = p.stat(); total += before.st_size
            if total > 100_000_000 or len(found)>=10000: raise ValueError('Package size bound exceeded')
            h = hashlib.sha256()
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
            after = p.stat()
            if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
                raise ValueError('File changed while inspecting')
            found[p.relative_to(root).as_posix()] = h.hexdigest()
    if 'SKILL.md' not in found: raise ValueError('SKILL.md missing')
    return found


class GitHub:
    def __init__(self, seconds=90): self.deadline=time.monotonic()+seconds; self.cache={}
    def get(self, endpoint):
        if endpoint in self.cache: return self.cache[endpoint]
        remaining=self.deadline-time.monotonic()
        if remaining<=0: raise ValueError('Upstream total time budget exhausted')
        timeout=min(15,remaining)
        if shutil.which('gh'):
            r=subprocess.run([shutil.which('gh'),'api',endpoint],capture_output=True,timeout=timeout)
            if r.returncode: raise ValueError('GitHub read failed; not unchanged')
            raw=r.stdout
        else:
            req=urllib.request.Request('https://api.github.com/'+endpoint,headers={'User-Agent':'portable-skill-maintenance','Accept':'application/vnd.github+json'})
            with urllib.request.urlopen(req,timeout=timeout) as r: raw=r.read(15_000_001)
            if len(raw)>15_000_000: raise ValueError('GitHub response size bound exceeded')
        data=json.loads(raw); self.cache[endpoint]=data; return data
    def tree(self,repo,ref,prefix):
        data=self.get(f'repos/{repo}/git/trees/{ref}?recursive=1')
        if data.get('truncated') is not False: raise ValueError('Incomplete upstream tree')
        prefix=prefix.rstrip('/')+'/'
        files={}
        for row in data['tree']:
            if row['type']=='blob' and row['path'].startswith(prefix):
                name=row['path'][len(prefix):]
                if row.get('mode') not in ('100644','100755') or '..' in PurePosixPath(name).parts:
                    raise ValueError('Unsupported upstream link/path')
                files[name]=row['sha']
        if 'SKILL.md' not in files: raise ValueError('Upstream skill path missing')
        return files
    def blob(self,repo,identity):
        row=self.get(f'repos/{repo}/git/blobs/{identity}')
        if row.get('encoding')!='base64' or row.get('size',0)>512000: raise ValueError('Diff blob coverage exceeded')
        raw=base64.b64decode(row['content'])
        if git_sha(raw)!=identity: raise ValueError('Blob identity mismatch')
        return raw


def compare(repo,pin,prefix,root=None,api=None):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo or '') or not re.fullmatch('[a-f0-9]{40}',pin or ''):
        raise ValueError('Explicit public repository and full pinned SHA required')
    if not prefix or '..' in PurePosixPath(prefix).parts or prefix.startswith('/') or '\\' in prefix:
        raise ValueError('Explicit safe upstream skill path required')
    api=api or GitHub(); head=api.get(f'repos/{repo}/commits/HEAD')['sha']
    old=api.tree(repo,pin,prefix); new=api.tree(repo,head,prefix)
    changed=sorted(k for k in old.keys()|new.keys() if old.get(k)!=new.get(k))
    drift=None
    if root is not None:
        drift=[]
        for name,h in old.items():
            p=within(root,name)
            if not p.is_file() or git_sha(p.read_bytes())!=h: drift.append(name)
    diffs=[]; errors=[]
    for name in changed[:20]:
        try:
            a=api.blob(repo,old[name]) if name in old else b''
            b=api.blob(repo,new[name]) if name in new else b''
            if b'\0' in a+b: diffs.append('Binary change: '+name); continue
            diffs.append(''.join(difflib.unified_diff(a.decode('utf-8').splitlines(True),b.decode('utf-8').splitlines(True),fromfile=pin+'/'+name,tofile=head+'/'+name)))
        except (ValueError,UnicodeError,OSError,subprocess.SubprocessError) as exc: errors.append({'file':name,'error':str(exc)})
    text='\n'.join(diffs)
    return {'status':'update_available' if changed else 'unchanged','repo':repo,'pin':pin,'head':head,'path':prefix,
            'changed_files':changed,'local_upstream_drift':drift,'local_writes':False,
            'diff':text[:100000],'diff_complete':not errors and len(changed)<=20 and len(text)<=100000,'diff_errors':errors}


def state_path():
    if os.environ.get('LOCALAPPDATA'): return Path(os.environ['LOCALAPPDATA'])/'skill-maintenance'
    return Path(os.environ.get('XDG_STATE_HOME',str(Path.home()/'.local/state')))/'skill-maintenance'


def events(state):
    if not state.is_dir(): return []
    rows=[]
    for p in sorted(state.glob('*.json')):
        row=json.loads(p.read_text(encoding='utf-8')); identity=row.pop('id')
        if row.get('schema')!='skill-runtime-event/1' or sha(json.dumps(row,sort_keys=True).encode())!=identity or p.stem!=identity:
            raise ValueError('Receipt content identity mismatch')
        rows.append(dict(row,id=identity))
    return rows


def record(state,row):
    row=dict(schema='skill-runtime-event/1',recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),**row)
    identity=sha(json.dumps(row,sort_keys=True).encode());state.mkdir(parents=True,exist_ok=True)
    with (state/(identity+'.json')).open('x',encoding='utf-8') as f:json.dump(dict(row,id=identity),f,indent=2)
    return identity


def usage(rows,runtime,run_id=None):
    rows=[r for r in rows if r['runtime']==runtime and (not run_id or r['run_id']==run_id)]
    stale=0
    for row in rows:
        if row.get('artifact'):
            try: valid=file_ref(Path(row['artifact']['path']))==row['artifact']
            except (OSError,ValueError):valid=False
            if not valid: stale+=1
    return {'coverage':'explicit receipts in this state directory; other profiles and uninstrumented work unknown',
            'status':'observed' if rows else 'unknown','runtime':runtime,'events':rows,
            'counts':{stage:sum(r['stage']==stage for r in rows) for stage in ['read','applied_attested','verified_property','verification_failed']},
            'changed_or_missing_artifact_events':stale,'semantic_usefulness':'unknown; evaluate with the owning consumer'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['inspect','compare','read','applied','verify-bytes','usage'])
    p.add_argument('--root',type=Path);p.add_argument('--canonical',type=Path)
    p.add_argument('--repo');p.add_argument('--pin');p.add_argument('--path')
    p.add_argument('--file',default='SKILL.md');p.add_argument('--run-id');p.add_argument('--runtime')
    p.add_argument('--state-dir',type=Path);p.add_argument('--artifact',type=Path)
    p.add_argument('--criterion');p.add_argument('--expected-sha256');p.add_argument('--force',action='store_true')
    p.add_argument('--output',type=Path)
    a=p.parse_args(argv);status=0
    try:
        if a.action=='inspect':
            if not a.root: raise ValueError('--root required')
            files=package(a.root);out={'status':'inspected','root':str(a.root.resolve()),'files':files,'package_sha256':sha(json.dumps(files,sort_keys=True).encode()),'discovery_and_use':'unverified'}
            if a.canonical:
                canonical=package(a.canonical);out.update(status='matches' if files==canonical else 'differs',changed_files=sorted(k for k in files.keys()|canonical.keys() if files.get(k)!=canonical.get(k)))
        elif a.action=='compare':
            out=compare(a.repo,a.pin,a.path,a.root)
            if not out['diff_complete']:status=2
        else:
            if not a.runtime: raise ValueError('Explicit --runtime profile label required')
            state=a.state_dir or state_path();rows=events(state)
            if a.action=='usage':out=usage(rows,a.runtime,a.run_id)
            else:
                if not a.root or not a.run_id: raise ValueError('--root and --run-id required')
                entry=file_ref(within(a.root,'SKILL.md'))
                same=[r for r in rows if r['runtime']==a.runtime and r['run_id']==a.run_id and r['entry']==entry]
                row={'entry':entry,'runtime':a.runtime,'run_id':a.run_id}
                if a.action=='read':
                    source=within(a.root,a.file);raw=source.read_bytes();body=raw.decode('utf-8-sig');delivered=file_ref(source)
                    duplicate=any(r['stage']=='read' and r.get('delivered')==delivered for r in same)
                    out={'status':'unchanged' if duplicate and not a.force else 'delivered','source':delivered}
                    if out['status']=='delivered':
                        out.update(receipt=record(state,dict(row,stage='read',delivered=delivered)),content=body)
                else:
                    if not any(r['stage']=='read' for r in same):raise ValueError('No observed read for this exact version/context')
                    if not a.artifact:raise ValueError('--artifact required')
                    artifact=file_ref(a.artifact)
                    if a.action=='applied':
                        out={'status':'applied_attested','receipt':record(state,dict(row,stage='applied_attested',artifact=artifact)),
                             'limit':'Operator assertion, not independent semantic evaluation'}
                    else:
                        if not any(r['stage']=='applied_attested' and r.get('artifact')==artifact for r in same):raise ValueError('No application receipt for these artifact bytes')
                        if not a.criterion or not re.fullmatch('[a-fA-F0-9]{64}',a.expected_sha256 or ''):raise ValueError('Criterion and valid expected SHA256 required')
                        passed=artifact['sha256']==a.expected_sha256.lower();stage='verified_property' if passed else 'verification_failed'
                        out={'status':stage,'passed':passed,'criterion':a.criterion,'check':'artifact_sha256_equals_expected',
                             'limit':'Only byte identity; semantic usefulness and learning remain unknown',
                             'receipt':record(state,dict(row,stage=stage,artifact=artifact,criterion=a.criterion,expected_sha256=a.expected_sha256.lower(),passed=passed))}
                        if not passed:status=1
    except (ValueError,OSError,KeyError,subprocess.SubprocessError) as exc:
        out={'status':'incomplete','error':str(exc),'conclusion':'Unknown, never unchanged or unused'};status=2
    text=json.dumps(out,indent=2,ensure_ascii=False)
    if a.output:
        if not a.output.parent.is_dir():raise SystemExit('Output parent must already exist')
        with a.output.open('x',encoding='utf-8') as f:f.write(text+'\n')
    print(text);return status


if __name__=='__main__':sys.exit(main())
