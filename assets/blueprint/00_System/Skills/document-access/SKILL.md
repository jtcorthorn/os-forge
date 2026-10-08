---
name: document-access
description: Select a reliable reading, extraction or editing route for unfamiliar document and media formats. Use when a file cannot be read directly, when processing mixed-format intake, or when a conversion loses tables, images or source locators. Preserve originals and distinguish parser coverage from the source's actual content.
---

# Document access

Read the owning map and contract. Identify the actual file type from original bytes and metadata, obtain an authorized original-byte copy and record its source path/ID, date and SHA256. A cloud pointer or extracted Markdown is not the original. Prefer an existing native connector or format-specific skill before adding a converter. Do not execute macros, embedded scripts or attachments.

| Input/task | Preferred route | Acceptance |
|---|---|---|
| Markdown, TXT, CSV, JSON, XML, YAML, logs | Native UTF-8 read or deterministic parser | Encoding, row/record counts, truncation and original hash |
| PDF | Available PDF skill/native reader; inspect pages for layout or scans | Page locators, page coverage, embedded text versus OCR |
| DOCX/DOTX or native Word | Available document/Word skill and authorized native editor | Paragraph/table preservation; render when layout matters |
| XLSX/XLS/XLSM/ODS/CSV | Spreadsheet skill/native workbook; sparse stored-cell recovery when needed | Sheet/cell locators, formulas versus cached values, omitted rows |
| PPTX/POTX/ODP or native slides | Presentation skill/native editor | Slide locators, notes and visual elements |
| Text PDF, DOCX/PPTX/XLSX, HTML, CSV, JSON, XML or Markdown | Microsoft MarkItDown local SDK, with plugins and hosted services disabled unless authorized | Extracted content against source, warnings, escaped text and coverage |
| ODT/ODS/ODP, email or complex PDF | Reviewed upstream Docling skill, with format-specific local extras and a working host engine | Conversion status, source locators, warnings and supported engine |
| PNG/JPEG/TIFF/WebP or scanned pages | Original image view and available local OCR | Pixel readability, OCR uncertainty and page/image locator |
| Audio/video | Available transcription skill/local ASR | Language, time ranges, speaker uncertainty and source hash |
| EPUB, archives, legacy DOC/PUB or proprietary files | Inspect available format tool or owner-supplied export | Preserve container and members; list unsupported/encrypted objects |

Use Docling's maintained skill from `docling-project/docling`, path `docling/.agents/skills/docling`; inspect its current requirements before installation. Use OpenAI's `transcribe` skill for authorized API transcription when the required account/key and cost boundary exist. Installing a skill does not install its parser, OCR models or credentials. Prefer small format extras over a blanket ML install; local extraction does not authorize sending private sources to a hosted converter. Route document authoring to the dedicated editing skill rather than flattening a workbook/deck to Markdown.

For mixed corpora use the OS Forge inventory/extraction helpers if available, preserving page/paragraph/slide/cell provenance and failed/unsupported items. A near-empty or lossy extraction is incomplete coverage; check the actual source or another supported route. One retry with a changed method is useful; repeating an unchanged failure is not. Use Markdown for reading by default and structured JSON when a downstream parser needs it, unless the owner specifies a format.

Save originals and derived outputs in their owning domain. Keep intake gates and effective access. Verify one consequential extracted claim against the original before relying on it. Report supported and verified formats separately from untested optional routes; never claim that every possible format is supported.
