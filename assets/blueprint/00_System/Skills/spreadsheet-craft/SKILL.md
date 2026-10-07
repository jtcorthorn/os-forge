---
name: spreadsheet-craft
description: Build or edit a spreadsheet with explicit inputs, formulas, units, and checks that make the model auditable. Use for calculations, trackers, and analyses.
---

# Spreadsheet craft

Identify the decision and the authoritative source rows. Keep raw inputs, assumptions, calculation, and presentation distinguishable. Put units, currency, dates, and source notes beside the data they qualify. Preserve workbook structure and formulas when editing an existing file.

Prefer formulas for repeated calculations and deterministic scripts for bulk transformations. Avoid hardcoded numbers hidden inside formulas. Check totals, row counts, key uniqueness, date parsing, formula errors, and at least one independently calculated example. For financial models, test a boundary case and reconcile to source totals.

Open or render the workbook in a spreadsheet engine if available. Check visible formatting, filters, frozen panes, chart labels, and print range. A successful library write does not prove recalc or visual usability. State whether recalc was verified. Retain prior versions before replacement.

Read [references/runtime.md](references/runtime.md) for optional tools and format limits.
