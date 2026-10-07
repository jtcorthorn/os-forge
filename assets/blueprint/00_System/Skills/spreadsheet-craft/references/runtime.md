# Spreadsheet runtime choices

Use Excel or another native spreadsheet engine when available for recalc and final inspection. `openpyxl` edits `.xlsx` without evaluating formulas. `pandas` is suitable for tabular analysis but may drop formulas and formatting when rewriting a workbook. `LibreOffice` can recalculate and export, subject to feature compatibility. For cloud sheets, use the authorized connector and inspect exact ranges. Record the engine used, whether formulas recalculated, and any unsupported macros, external links, pivots, or charts. No runtime is bundled here.
