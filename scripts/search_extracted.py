#!/usr/bin/env python3
"""Literal search over recipient-local extraction manifests and JSONL artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


SEARCHABLE = {"complete", "truncated", "timeout"}


def inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_state(root: Path, entry: dict) -> str:
    rel = entry.get("resolved_relative_path") or entry.get("relative_path")
    if not rel:
        return "unknown"
    path = (root / rel).resolve()
    if not inside(path, root):
        return "invalid_path"
    if not path.is_file():
        return "missing"
    expected = entry.get("sha256")
    if not expected:
        return "unknown"
    return "current" if sha256(path) == expected.lower() else "stale"


def run(args):
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit("Recipient root does not exist")
    groups = {}
    coverage = {"manifests": 0, "listed_sources": 0, "searchable_sources": 0,
                "skipped_status_sources": 0, "missing_artifacts": 0,
                "artifacts_scanned": 0, "records_scanned": 0, "malformed_records": 0,
                "scan_complete": True}
    for raw_manifest in args.manifest:
        manifest_path = Path(raw_manifest).resolve()
        if not inside(manifest_path, root) or not manifest_path.is_file():
            raise SystemExit("Manifest missing or outside recipient root: " + raw_manifest)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        coverage["manifests"] += 1
        for entry in manifest.get("sources", []):
            coverage["listed_sources"] += 1
            if entry.get("status") not in SEARCHABLE or not entry.get("content"):
                coverage["skipped_status_sources"] += 1
                continue
            artifact = (manifest_path.parent / entry["content"]).resolve()
            if not inside(artifact, root) or not inside(artifact, manifest_path.parent):
                raise SystemExit("Artifact path leaves manifest directory: " + entry["content"])
            if not artifact.is_file():
                coverage["missing_artifacts"] += 1
                continue
            coverage["searchable_sources"] += 1
            groups.setdefault(artifact, []).append(entry)
    needle = re.compile(re.escape(args.query), flags=re.IGNORECASE)
    hits = []
    for artifact, sources in sorted(groups.items(), key=lambda x: str(x[0]).casefold()):
        coverage["artifacts_scanned"] += 1
        with artifact.open(encoding="utf-8", errors="replace") as f:
            for line_no, line in enumerate(f, 1):
                coverage["records_scanned"] += 1
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    coverage["malformed_records"] += 1
                    continue
                value = rec.get("text", "")
                if not isinstance(value, str):
                    continue
                match = needle.search(value)
                if match is None:
                    continue
                source = sources[0]
                start = max(0, match.start() - args.context)
                end = min(len(value), match.end() + args.context)
                excerpt = value[start:end]
                hits.append({"source_path": source.get("resolved_relative_path") or source.get("relative_path"),
                             "source_hash_state": source_state(root, source),
                             "alias_count": len(sources) - 1,
                             "source_status": source.get("status"),
                             "locator": rec.get("locator"),
                             "locator_kind": rec.get("locator_kind"),
                             "excerpt": excerpt,
                             "excerpt_clipped_before": start > 0,
                             "excerpt_clipped_after": end < len(value),
                             "artifact": artifact.relative_to(root).as_posix(),
                             "record_line": line_no})
                if len(hits) >= args.limit:
                    coverage["scan_complete"] = False
                    break
        if len(hits) >= args.limit:
            break
    coverage["unique_artifacts_available"] = len(groups)
    coverage["unscanned_artifacts"] = len(groups) - coverage["artifacts_scanned"]
    print(json.dumps({"query": args.query, "hits": hits, "coverage": coverage,
                      "interpretation": "No match is not proof of absence; extraction may omit image text, unsupported formats, or truncated content."},
                     ensure_ascii=False, sort_keys=True))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", required=True)
    p.add_argument("--manifest", action="append", required=True, help="Recipient-local manifest; repeat for supplemental extraction")
    p.add_argument("--query", required=True, help="Literal case-insensitive text")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--context", type=int, default=250)
    args = p.parse_args()
    if not args.query or args.limit <= 0 or args.context < 0 or args.context > 5000:
        p.error("Query must be nonempty, limit positive, context between 0 and 5000")
    run(args)


if __name__ == "__main__":
    main()
