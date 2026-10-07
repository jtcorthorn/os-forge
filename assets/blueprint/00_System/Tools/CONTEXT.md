# Local source extraction tools

Inputs: a current CSV inventory of original files inside this OS, with `relative_path,sha256,size_bytes` (or `bytes`).
Work: read original bytes without changing them; emit searchable text and provenance in the owning company or personal domain.
Output: `manifest.json` plus hash-keyed JSONL with page, slide, paragraph, sheet/cell or line locators.
Boundary: keep personal health separate from company extraction. Generated text is evidence for retrieval, not permission or operating truth.

## Run on this station
Use Python 3.10+ with PyMuPDF or pypdf for PDF, and openpyxl for Excel; other supported text/Office formats use the standard library.
From the OS root, use this command with the actual current inventory and owning-domain output folder:

```text
python 00_System/Tools/extract_sources.py --root . --inventory <current-inventory.csv> --output <owning-domain>/_extracted/<run-date>
```

The station agent resolves those paths from Intake and the selected domain contract before execution.
No account credentials, macros or HTML scripts are executed. Do not install missing dependencies or use an external service outside the owner's authorization.
Default limits: 2,000,000 characters per source, 5,000 pages/slides, 10,000 rows per sheet and 120 seconds per file.
The manifest separates complete embedded-text extraction from truncation, OCR needs, password requirements, unsupported formats and failures.
Even a complete PDF extraction may omit image-only pages; inspect its warnings and page metrics.
Excel cached values and formulas are not recalculated. Layout, scanned images and embedded diagrams need separate inspection when consequential.
The script resumes matching source hash, code/config signature and existing artifacts. Source aliases share extraction but originals remain separate.
Store prior runs as evidence; do not treat the presence of text files as proof every source was successfully read.

## Sparse Excel recovery
When Excel declares huge formatted ranges, [extract_sparse_xlsx.py](extract_sparse_xlsx.py) scans actual stored nonempty cells instead of walking a rectangular grid. It needs only Python's standard library.
Use the same `--root`, `--inventory` and a separate `--output`, with repeated `--select` relative paths or hashes for affected workbooks only.
It preserves sheet/cell locators, formulas, raw cached values and declared dimensions. Raw numeric dates require interpretation of original formatting; no recalculation occurs.
Keep the original extraction manifest and this supplement. Effective coverage must explain which source uses which result.

## Retrieve without loading the corpus into a model
Use [search_extracted.py](search_extracted.py), a standard-library-only literal search tool:

```text
python 00_System/Tools/search_extracted.py --root . --manifest <owning-domain>/_extracted/<run-date>/manifest.json --query "search phrase" --limit 10 --context 250
```

Repeat `--manifest` for supplemental runs when relevant. The owning knowledge map identifies current manifests.
`--root` must be the same logical source root used for that extraction, which may be the company folder rather than the whole personal OS. Search manifests with different source roots separately; use the owning knowledge map's scoped command.
Results carry source path, locator, bounded excerpt, alias count and current source-hash state.
The tool reports search coverage and stops at the requested hit limit. It does not establish which source is approved or current.
A changed or missing original must be resolved before relying on its old extracted text. No-match is not proof of absence.
