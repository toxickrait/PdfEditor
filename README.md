# PdfEditor

A lightweight command-line tool for common PDF manipulation tasks — merge, delete pages, redact text, reorder pages, and compress.

---

## Features

| Command    | Description                                      |
|------------|--------------------------------------------------|
| `merge`    | Combine multiple PDF files into one              |
| `delete`   | Remove specific pages from a PDF                 |
| `redact`   | Erase sensitive text (plain string or regex)     |
| `reorder`  | Rearrange pages in a custom order                |
| `compress` | Reduce file size by re-rendering pages as images |

---

## Setup

### Using uv (recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager. If you don't have it yet:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then set up the project:

```bash
# Create a virtual environment and install all dependencies
uv sync
```

Run the tool via:

```bash
uv run python pdf_tool.py <command> [options]
```

---

### Using pip

```bash
pip install pypdf pymupdf pillow pdf-redactor
```

---

## Usage

```bash
python pdf_tool.py <command> [options]
```

### Merge

Merge two or more PDFs into a single file.

```bash
python pdf_tool.py merge file1.pdf file2.pdf file3.pdf -o merged.pdf
```

| Argument       | Description                              |
|----------------|------------------------------------------|
| `pdfs`         | One or more input PDF files              |
| `-o, --output` | Output filename (default: `merged_output.pdf`) |

---

### Delete Pages

Delete specific pages from a PDF (pages use **1-based** indexing).

```bash
python pdf_tool.py delete input.pdf output.pdf 2 5 7
```

| Argument | Description                            |
|----------|----------------------------------------|
| `input`  | Input PDF file                         |
| `output` | Output PDF file                        |
| `pages`  | Page numbers to delete (1-based index) |

---

### Redact

Remove sensitive text from a PDF. Supports plain strings and regular expressions.

```bash
# Plain text
python pdf_tool.py redact input.pdf output.pdf "John Doe" "555-1234"

# Regex (prefix with "re:")
python pdf_tool.py redact input.pdf output.pdf "re:\d{3}-\d{4}"
```

| Argument   | Description                                             |
|------------|---------------------------------------------------------|
| `input`    | Input PDF file                                          |
| `output`   | Output PDF file                                         |
| `patterns` | Text or regex patterns to redact (prefix regex with `re:`) |

---

### Reorder Pages

Rearrange pages into a new order using **1-based** page numbers.

```bash
# Move page 3 to the front: 3 1 2
python pdf_tool.py reorder input.pdf output.pdf 3 1 2
```

| Argument | Description                                    |
|----------|------------------------------------------------|
| `input`  | Input PDF file                                 |
| `output` | Output PDF file                                |
| `order`  | New page order using 1-based page numbers      |

---

### Compress

Reduce PDF file size by converting pages to compressed JPEG images.

```bash
python pdf_tool.py compress input.pdf output.pdf --quality 40 --dpi 100
```

| Argument        | Description                                    |
|-----------------|------------------------------------------------|
| `input`         | Input PDF file                                 |
| `output`        | Output PDF file                                |
| `-q, --quality` | JPEG quality 1–100 (default: `40`)             |
| `-d, --dpi`     | Render resolution in DPI (default: `100`)      |

> **Note:** Compression works by rasterizing each page as an image. This reduces file size but removes selectable text and may lower visual quality at very low DPI/quality settings.

---

## License

MIT
