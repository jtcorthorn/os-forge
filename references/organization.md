# Preserve sources while reorganizing

Use only within an owner's authorized move scope. Inventory source files with exact hashes and inspect referrers: Markdown, active catalogs/generators, HTML/CSS assets, Office external relationships, symlinks and owner-identified external consumers. Local checks do not prove no external consumers exist. Ask one targeted question only if unknown consumers could materially affect safe use.

Keep coherent subtrees and original names where useful. Do not merge corporate identity, client aliases or duplicate versions on appearance alone. Record file-by-file moves, domain rationale and referrer handling in recipient Intake:

```json
{
  "schema_version": 1,
  "files": [
    {
      "old": "Incoming/terms.docx",
      "new": "20_Ventures/Example/originals/terms.docx",
      "size_bytes": 12345,
      "sha256": "replace with the actual measured SHA-256"
    }
  ]
}
```

This illustrates the schema; substitute actual source data before running. One file per row, all paths root-relative. Preview then apply:

```text
python <skill>/scripts/relocate_sources.py --root <root> --plan <root>/00_System/Intake/moves_YYYY-MM-DD.json --run-dir <root>/_archive/relocation_YYYY-MM-DD
python <skill>/scripts/relocate_sources.py --root <root> --plan <root>/00_System/Intake/moves_YYYY-MM-DD.json --run-dir <root>/_archive/relocation_YYYY-MM-DD --apply
```

Preview writes nothing. A run directory belongs to one immutable plan. Apply verifies backups of **all** originals before any move, then rechecks each source and moves exact files without overwriting. Receipt and backups support retries with the same plan/run directory; changed plans or divergent files stop. One active writer; do not execute concurrent applies.

The helper operates on local same-filesystem files. It does not remove old empty trees, repair references or do cross-filesystem transfers. A native coherent folder move may be preferable on Windows: validate resolved source/destination containment, verify backups, use `Move-Item -LiteralPath`, then compare each destination's bytes. Never delete original bytes to tidy a root.

Verify `inventory_after.csv` produced in the run directory:

```text
python <skill>/scripts/verify_sources.py --root <root> --inventory <root>/_archive/relocation_YYYY-MM-DD/inventory_after.csv
```

Repair active maps, notes, inventories, generators and authorized external referrers in the same change. Preserve human-edited records and regenerate catalogs through their owning script. Historical inventories remain historical. Office originals stay byte-identical; document embedded dependencies rather than silently editing/recalculating them. Compare newly broken source links with preexisting missing assets. A passed hash check does not prove reference integrity.

Backups, private plans, receipts and inventories stay in the recipient OS; never publish them with this skill.
