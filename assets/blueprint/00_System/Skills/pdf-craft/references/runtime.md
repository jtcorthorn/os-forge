# PDF runtime choices

For text extraction, use a PDF reader or libraries such as `pypdf` or `pdfplumber`; inspect page images where tables or columns matter. OCR requires an available engine and manual checking of consequential values. For creation, a document editor, HTML-to-PDF renderer, or `reportlab` may work. Poppler or another renderer can make page images for visual inspection. Check the actual output file, page count, page order, and representative pages. This package includes no binary tools or fonts.
