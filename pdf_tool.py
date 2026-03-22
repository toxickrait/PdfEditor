import argparse
import re
from pypdf import PdfReader, PdfWriter
import sys
import pdf_redactor
import fitz  # PyMuPDF
from PIL import Image
import io
import os

# ----- MERGE -----
def merge_pdfs(pdf_list, output_file):
    writer = PdfWriter()

    for pdf_path in pdf_list:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
            print(f"Added: {pdf_path}")
        except Exception as e:
            print(f"Error adding {pdf_path}: {e}")

    with open(output_file, "wb") as f_out:
        writer.write(f_out)
    print(f"\nMerged PDF saved as: {output_file}")

# ----- DELETE -----
def delete_pages(input_file, output_file, pages_to_delete):
    reader = PdfReader(input_file)
    writer = PdfWriter()

    total_pages = len(reader.pages)
    pages_to_delete = sorted(set(pages_to_delete))

    print(f"Total pages in input PDF: {total_pages}")
    print(f"Deleting pages: {[p+1 for p in pages_to_delete]} (1-based index)")

    for i in range(total_pages):
        if i not in pages_to_delete:
            writer.add_page(reader.pages[i])
        else:
            print(f"Deleted page {i + 1}")

    with open(output_file, "wb") as f_out:
        writer.write(f_out)
    print(f"\nModified PDF saved as: {output_file}")

# ----- REDACT -----
def redact_pdf(input_pdf, output_pdf, patterns):
    options = pdf_redactor.RedactorOptions()
    # Support plain text and regex patterns
    regex_patterns = []
    for pattern in patterns:
        if pattern.startswith("re:"):
            regex_patterns.append((re.compile(pattern[3:]), lambda m: ""))
        else:
            regex_patterns.append((re.compile(re.escape(pattern)), lambda m: ""))
    options.content_filters = regex_patterns
    options.input_stream = open(input_pdf, "rb")
    options.output_stream = open(output_pdf, "wb")
    pdf_redactor.redactor(options)
    print(f"\nRedacted PDF saved as: {output_pdf}")

# ----- REORDER -----
def reorder_pages(input_file, output_file, new_order):
    """
    Reorder the pages of a PDF file.

    :param input_file: Path to the input PDF.
    :param output_file: Path to save the reordered PDF.
    :param new_order: List of 1-based page numbers in the desired order.
    """
    reader = PdfReader(input_file)
    writer = PdfWriter()
    total_pages = len(reader.pages)

    print(f"Total pages in input PDF: {total_pages}")
    print(f"New order (1-based): {new_order}")

    for page_num in new_order:
        idx = page_num - 1  # Convert to 0-based index
        if 0 <= idx < total_pages:
            writer.add_page(reader.pages[idx])
            print(f"Added page {page_num}")
        else:
            print(f"Warning: Page {page_num} is out of range and will be skipped.")

    with open(output_file, "wb") as f_out:
        writer.write(f_out)
    print(f"\nReordered PDF saved as: {output_file}")

# --------- Compress PDFs ---------
def compress_pdf(input_path, output_path, image_quality=40, dpi=100):
    # Open the original PDF
    doc = fitz.open(input_path)
    new_doc = fitz.open()

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        pix = page.get_pixmap(dpi=dpi)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_io = io.BytesIO()
        img.save(img_io, format="JPEG", quality=image_quality)
        img_io.seek(0)

        # Create a new blank page with the same size as the original
        rect = page.rect
        new_page = new_doc.new_page(width=rect.width, height=rect.height)

        # Insert the compressed image onto the new page
        new_page.insert_image(rect, stream=img_io.getvalue())

    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    print(f"Compressed PDF saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge PDFs or Delete pages from a PDF")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDF files")
    merge_parser.add_argument("pdfs", nargs="+", help="List of PDF files to merge")
    merge_parser.add_argument("-o", "--output", default="merged_output.pdf", help="Output merged PDF file")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete pages from a PDF")
    delete_parser.add_argument("input", help="Input PDF file")
    delete_parser.add_argument("output", help="Output PDF file")
    delete_parser.add_argument("pages", nargs="+", type=int, help="Pages to delete (1-based index)")

    # redact
    redact_parser = subparsers.add_parser("redact", help="Redact sensitive text (exact or regex)")
    redact_parser.add_argument("input", help="Input PDF")
    redact_parser.add_argument("output", help="Output PDF")
    redact_parser.add_argument("patterns", nargs="+", help='Text or regex patterns (prefix regex with "re:")')

    # Reorder command
    reorder_parser = subparsers.add_parser("reorder", help="Reorder pages in a PDF")
    reorder_parser.add_argument("input", help="Input PDF file")
    reorder_parser.add_argument("output", help="Output PDF file")
    reorder_parser.add_argument("order", nargs="+", type=int, help="New order of pages (1-based indices)")

    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress a PDF")
    compress_parser.add_argument("input", help="Path to the input PDF file.")
    compress_parser.add_argument("output", help="Path to save the compressed PDF.")
    compress_parser.add_argument("-q", "--quality", type=int, default=40, help="JPEG image quality (1–100). Default is 40.")
    compress_parser.add_argument("-d", "--dpi", type=int, default=100, help="Image DPI resolution. Default is 100.")

    args = parser.parse_args()

    if args.command == "merge":
        merge_pdfs(args.pdfs, args.output)
    elif args.command == "delete":
        # Convert 1-based to 0-based page numbers
        zero_based_pages = [p - 1 for p in args.pages if p > 0]
        delete_pages(args.input, args.output, zero_based_pages)
    elif args.command == "redact":
        redact_pdf(args.input, args.output, args.patterns)
    elif args.command == "reorder":
        # Example: python .\pdf_tool.py reorder input.pdf output.pdf 3 1 2
        reorder_pages(args.input, args.output, args.order)
    elif args.command == "compress":
        # Example: python .\pdf_tool.py compress input.pdf output.pdf --quality 40 --dpi 100
        compress_pdf(args.input, args.output, args.quality, args.dpi)
    else:
        parser.print_help()
        sys.exit(1)
