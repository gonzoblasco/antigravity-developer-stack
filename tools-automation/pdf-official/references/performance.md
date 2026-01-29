# PDF Processing Performance Guide

Processing PDFs can be resource-intensive. Follow these guidelines to optimize for speed and memory usage.

## Tool Selection Strategy

| Task                  | Fast & Low Memory (Stream based) | Heavy but Powerful (DOM based) |
| --------------------- | -------------------------------- | ------------------------------ |
| **Text Extraction**   | `pdftotext` (CLI), `pypdf`       | `pdfplumber`, `pymupdf` (fitz) |
| **Merging/Splitting** | `qpdf` (CLI), `pypdf`            | `pdf-lib` (Node)               |
| **Rendering/Images**  | `pdf2image`                      | `pdf.js`                       |

## Python Optimization Tips

### 1. Lazy Loading with `pypdf`

`pypdf` loads pages lazily by default. Avoid iterating over all pages unless necessary.

```python
# ✅ GOOD: Reads metadata without parsing whole file
reader = PdfReader("huge_doc.pdf")
print(reader.metadata)

# ❌ BAD: Iterating unnecessarily
for page in reader.pages:
    pass
```

### 2. Stream-based Writing

When writing huge PDFs, use append mode if supported, or ensure you are not holding all page objects in memory.

### 3. `pdfplumber` Memory Management

`pdfplumber` keeps a detailed object model of the PDF. For large files, open and close per page or use context managers strictly to free memory.

```python
# ✅ GOOD: Process page by page
with pdfplumber.open("huge.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        # process text immediately

# ❌ BAD: Collecting all pages objects into a list
with pdfplumber.open("huge.pdf") as pdf:
    all_pages = [p for p in pdf.pages] # Explodes memory
```

## CLI Shortcuts (Highest Performance)

If you just need raw text or simple page ops, shell out to CLI tools. They are written in C/C++ and are orders of magnitude faster.

```python
import subprocess

def fast_text_extract(path):
    # ~50x faster than pypdf for pure text
    result = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    return result.stdout
```

## Parallel Processing

PDF pages are usually independent. You can parallelize extraction:

```python
from concurrent.futures import ProcessPoolExecutor

def process_page(page_num):
    # Logic to extract from specific page
    pass

with ProcessPoolExecutor() as executor:
    executor.map(process_page, range(100))
```
