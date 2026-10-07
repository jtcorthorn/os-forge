#!/usr/bin/env python3
"""Extract stored XLSX/XLSM cells without walking a styled worksheet grid."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import time
import zipfile
from xml.etree import ElementTree as ET

VERSION = "1.0"
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inside(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def tag(local):
    return "{" + MAIN_NS + "}" + local


def shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    out = []
    with z.open("xl/sharedStrings.xml") as f:
        for event, el in ET.iterparse(f, events=("end",)):
            if el.tag == tag("si"):
                out.append("".join((t.text or "") for t in el.iter(tag("t"))))
                el.clear()
    return out


def sheet_targets(z):
    with z.open("xl/workbook.xml") as f:
        workbook = ET.parse(f).getroot()
    with z.open("xl/_rels/workbook.xml.rels") as f:
        rels = ET.parse(f).getroot()
    targets = {}
    for rel in rels.findall("{" + PKG_REL_NS + "}Relationship"):
        target = rel.attrib.get("Target", "")
        if target.startswith("/"):
            target = target.lstrip("/")
        else:
            target = posixpath.normpath(posixpath.join("xl", target))
        targets[rel.attrib["Id"]] = target
    result = []
    for sh in workbook.findall(".//" + tag("sheet")):
        rid = sh.attrib.get("{" + REL_NS + "}id")
        target = targets.get(rid)
        if target and target in z.namelist() and target.startswith("xl/worksheets/"):
            result.append((sh.attrib.get("name", ""), target))
    return result


def extract_one(source, content_path, max_chars, max_cells, timeout):
    started = time.monotonic()
    metrics = {"sheets": [], "stored_nonempty_cells_observed": 0, "emitted_cells": 0, "text_characters": 0}
    warnings = ["Raw cached values and date serials retained; formulas were not recalculated"]
    status = "complete"
    with zipfile.ZipFile(source) as z, content_path.open("w", encoding="utf-8", newline="\n") as out:
        strings = shared_strings(z)
        sheets = sheet_targets(z)
        for sheet_name, xml_path in sheets:
            sm = {"name": sheet_name, "xml_part": xml_path, "declared_dimension": None,
                  "stored_nonempty_cells_observed": 0, "emitted_cells": 0}
            metrics["sheets"].append(sm)
            with z.open(xml_path) as stream:
                for event, el in ET.iterparse(stream, events=("end",)):
                    if el.tag == tag("dimension"):
                        sm["declared_dimension"] = el.attrib.get("ref")
                    if el.tag == tag("row"):
                        el.clear()
                        continue
                    if el.tag != tag("c"):
                        continue
                    if time.monotonic() - started > timeout:
                        status = "timeout"; warnings.append(f"File exceeded {timeout} seconds; coverage incomplete")
                        break
                    coord = el.attrib.get("r", "")
                    cell_type = el.attrib.get("t", "n")
                    formula_el = el.find(tag("f"))
                    value_el = el.find(tag("v"))
                    inline_el = el.find(tag("is"))
                    formula = formula_el.text if formula_el is not None else None
                    raw = value_el.text if value_el is not None else None
                    inline = "".join(t.text or "" for t in inline_el.iter(tag("t"))) if inline_el is not None else None
                    # A styled but empty <c> has no actual value, inline string, or formula.
                    if formula is None and raw is None and inline is None:
                        el.clear(); continue
                    metrics["stored_nonempty_cells_observed"] += 1
                    sm["stored_nonempty_cells_observed"] += 1
                    if metrics["emitted_cells"] >= max_cells:
                        status = "truncated"; warnings.append("Cell budget reached; coverage incomplete")
                        el.clear(); break
                    display = inline if inline is not None else raw
                    if cell_type == "s" and raw is not None:
                        try:
                            display = strings[int(raw)]
                        except (ValueError, IndexError):
                            display = "[invalid shared string index " + raw + "]"
                            warnings.append("Invalid shared string reference")
                    if display is None:
                        display = "[cached value missing]"
                    remain = max_chars - metrics["text_characters"]
                    if remain <= 0:
                        status = "truncated"; warnings.append("Character budget reached; coverage incomplete")
                        el.clear(); break
                    if len(display) > remain:
                        display = display[:remain]
                        status = "truncated"; warnings.append("Character budget reached; coverage incomplete")
                    rec = {"locator": f"sheet:{sheet_name}/cell:{coord}", "locator_kind": "sheet_cell",
                           "sheet": sheet_name, "cell": coord, "text": display,
                           "cell_type": cell_type, "cached_value_raw": raw,
                           "value_interpretation": "raw stored value; numeric dates may be Excel serials"}
                    if inline is not None:
                        rec["inline_string"] = True
                    if formula is not None:
                        rec["formula"] = formula
                        if raw is None:
                            rec["cached_value_missing"] = True
                    if cell_type == "e":
                        rec["formula_error"] = True
                    out.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
                    metrics["emitted_cells"] += 1
                    sm["emitted_cells"] += 1
                    metrics["text_characters"] += len(display)
                    el.clear()
                    if status == "truncated":
                        break
            if status != "complete":
                break
    if status == "complete" and metrics["emitted_cells"] == 0:
        status = "no_text"
    if source.suffix.lower() == ".xlsm":
        warnings.append("Macros not executed")
    return status, metrics, sorted(set(warnings))


def run(args):
    root = Path(args.root).resolve()
    inventory = Path(args.inventory).resolve()
    output = Path(args.output).resolve()
    if not root.is_dir() or not inventory.is_file() or not inside(inventory, root):
        raise SystemExit("Root/inventory missing or inventory outside recipient root")
    if not inside(output, root) or output == root:
        raise SystemExit("Output must be a child of recipient root")
    output.mkdir(parents=True, exist_ok=True)
    content_dir = output / "content"; content_dir.mkdir(exist_ok=True)
    with inventory.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or not {"relative_path", "sha256"}.issubset(rows[0]):
        raise SystemExit("Inventory must contain relative_path,sha256,size_bytes (or bytes)")
    if "size_bytes" not in rows[0] and "bytes" not in rows[0]:
        raise SystemExit("Inventory must contain size_bytes or bytes")
    selected = set(args.select or [])
    chosen = [r for r in rows if Path(r["relative_path"]).suffix.lower() in (".xlsx", ".xlsm")
              and (not selected or r["relative_path"] in selected or r["sha256"].lower() in selected)]
    if selected and not chosen:
        raise SystemExit("No selected XLSX/XLSM entries in inventory")
    config = {"max_chars": args.max_chars, "max_cells": args.max_cells, "timeout": args.timeout}
    signature = hashlib.sha256(json.dumps({"version": VERSION, "script_sha256": sha(Path(__file__)), "config": config}, sort_keys=True).encode()).hexdigest()
    prior_path = output / "manifest.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8")) if prior_path.exists() else {}
    prior_entries = {r["relative_path"]: r for r in prior.get("sources", [])} if prior.get("engine_signature") == signature else {}
    entries = []
    aliases = {}
    for row in chosen:
        rel = row["relative_path"].replace("\\", "/")
        p = Path(rel)
        entry = {"relative_path": rel, "sha256": row["sha256"].lower(),
                 "size_bytes": int(row.get("size_bytes") or row.get("bytes") or 0),
                 "format": p.suffix.lower().lstrip(".")}
        if p.is_absolute() or ".." in p.parts or not rel:
            entry["status"] = "invalid_path"; entries.append(entry); continue
        source = (root / p).resolve()
        if not inside(source, root) or inside(source, output):
            entry["status"] = "invalid_path"; entries.append(entry); continue
        if not source.is_file():
            entry["status"] = "missing"; entries.append(entry); continue
        actual = sha(source)
        if actual != entry["sha256"]:
            entry.update(status="hash_mismatch", actual_sha256=actual); entries.append(entry); continue
        if source.stat().st_size != entry["size_bytes"]:
            entry.update(status="size_mismatch", actual_size_bytes=source.stat().st_size); entries.append(entry); continue
        key = entry["sha256"] + "." + entry["format"]
        artifact = content_dir / (key + ".jsonl")
        if key in aliases:
            base = aliases[key]
            entry.update({k: base[k] for k in ("status", "metrics", "warnings", "content") if k in base})
            entry["alias_of"] = base["relative_path"]
        elif (old := prior_entries.get(rel)) and old.get("sha256") == entry["sha256"] and old.get("status") in ("complete", "no_text", "truncated") and artifact.exists():
            entry.update({k: old[k] for k in ("status", "metrics", "warnings", "content") if k in old})
            entry["resumed"] = True
        else:
            temp = content_dir / (key + ".tmp")
            try:
                status, metrics, warnings = extract_one(source, temp, args.max_chars, args.max_cells, args.timeout)
                entry.update(status=status, metrics=metrics, warnings=warnings)
                os.replace(temp, artifact)
                entry["content"] = "content/" + artifact.name
            except Exception as e:
                entry.update(status="error", warnings=[type(e).__name__ + ": " + str(e)[:300]])
                if temp.exists(): temp.unlink()
        aliases[key] = entry
        entries.append(entry)
    manifest = {"schema_version": 1, "engine_signature": signature, "config": config,
                "root": str(root), "inventory": str(inventory), "sources": entries}
    temp = output / "manifest.tmp"
    temp.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, prior_path)
    counts = {}
    for e in entries: counts[e["status"]] = counts.get(e["status"], 0) + 1
    print(json.dumps({"manifest": str(prior_path), "source_count": len(entries), "statuses": counts}, sort_keys=True))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", required=True); p.add_argument("--inventory", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--select", action="append", help="Exact inventory relative_path or SHA-256; repeat as needed")
    p.add_argument("--max-chars", type=int, default=20_000_000)
    p.add_argument("--max-cells", type=int, default=2_000_000)
    p.add_argument("--timeout", type=int, default=300)
    args = p.parse_args()
    if min(args.max_chars, args.max_cells, args.timeout) <= 0:
        p.error("Budgets and timeout must be positive")
    run(args)


if __name__ == "__main__":
    main()
