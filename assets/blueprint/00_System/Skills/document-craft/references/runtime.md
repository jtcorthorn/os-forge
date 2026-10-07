# Document runtime choices

Use an existing native editor when available. For `.docx` programmatic edits, `python-docx` can handle ordinary paragraphs, styles, and tables, while LibreOffice or Word can render for visual inspection. Specialized features such as tracked changes, fields, comments, content controls, and complex headers need tool support and a preservation check. For Markdown or HTML, render in the intended viewer. Record the actual tool used and whether final layout was inspected. Do not assume this package installs Word, LibreOffice, fonts, or any plugin.
