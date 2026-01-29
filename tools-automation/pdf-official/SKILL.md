---
name: pdf
description: Use when you need to extract text/tables from PDFs, merge/split documents, fill forms, or generate new PDFs. Keywords: pdf, pypdf, pdfplumber, extract text, ocr, merge pdf.
---

# PDF Processing Expert

## Overview

This skill provides efficient methods for PDF manipulation. It prioritizes performance and correct tool selection.

> [!TIP]
> **Performance First**: For simple text extraction or page operations, CLI tools (`pdftotext`, `qpdf`) are 10-50x faster than Python libraries. See [Performance Guide](references/performance.md).

## Quick Start

### 1. Read Text (Best for reliability)

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
   print(pdf.pages[0].extract_text())
```

### 2. Merge Documents (Best for speed)

```python
from pypdf import PdfWriter

writer = PdfWriter()
writer.append("doc1.pdf")
writer.append("doc2.pdf")
writer.write("merged.pdf")
```

## Common Tasks & Tool Selection

| Goal                    | Recommended Tool                           | Reference                                                                           |
| ----------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Extract Text/Tables** | `pdfplumber` (Python) or `pdftotext` (CLI) | [Library Guide](references/library-guide.md#pdfplumber---text-and-table-extraction) |
| **Merge/Split/Rotate**  | `pypdf` (Python) or `qpdf` (CLI)           | [Library Guide](references/library-guide.md#merge-pdfs)                             |
| **Generate PDFs**       | `reportlab`                                | [Library Guide](references/library-guide.md#reportlab---create-pdfs)                |
| **Fill Forms**          | `pypdf` or `pdf-lib`                       | See `forms.md`                                                                      |
| **OCR Scanned Docs**    | `pytesseract` + `pdf2image`                | [Library Guide](references/library-guide.md#extract-text-from-scanned-pdfs)         |

## Documentation & References

- [**Library Guide**](references/library-guide.md): Detailed code snippets for pypdf, pdfplumber, reportlab.
- [**Performance Guide**](references/performance.md): Optimization tips for large files and low-memory environments.
- [**Forms Guide**](forms.md): Special instructions for handling PDF forms.
