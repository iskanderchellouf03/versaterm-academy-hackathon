import csv
import io

from src.config import CHUNK_SIZE


def _chunk_text(text, source_page=None):
    chunks = []
    # Split on double newlines first, then fall back to single newlines for dense text
    paragraphs = text.split("\n\n")
    if len(paragraphs) <= 1:
        paragraphs = text.split("\n")
    current = ""
    idx = 0
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 > CHUNK_SIZE and current:
            chunks.append({"text": current.strip(), "page": source_page, "index": idx})
            idx += 1
            current = para
        else:
            current = current + "\n" + para if current else para
    # Handle remaining text — split long blocks into CHUNK_SIZE pieces
    if current.strip():
        remaining = current.strip()
        while len(remaining) > CHUNK_SIZE:
            # Find a natural break point (sentence end, comma, or space)
            cut = remaining[:CHUNK_SIZE].rfind(". ")
            if cut < CHUNK_SIZE // 2:
                cut = remaining[:CHUNK_SIZE].rfind(" ")
            if cut < 1:
                cut = CHUNK_SIZE
            else:
                cut += 1
            chunks.append({"text": remaining[:cut].strip(), "page": source_page, "index": idx})
            idx += 1
            remaining = remaining[cut:].strip()
        if remaining:
            chunks.append({"text": remaining, "page": source_page, "index": idx})
    return chunks


def extract_pdf(file_bytes):
    from PyPDF2 import PdfReader

    reader = PdfReader(io.BytesIO(file_bytes))
    chunks = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            chunks.extend(_chunk_text(text, source_page=i + 1))
    return chunks


def extract_docx(file_bytes):
    from docx import Document

    doc = Document(io.BytesIO(file_bytes))
    text = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return _chunk_text(text)


def extract_txt(file_bytes):
    text = file_bytes.decode("utf-8", errors="replace")
    return _chunk_text(text)


def extract_csv(file_bytes):
    text = file_bytes.decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text))
    rows = [", ".join(row) for row in reader if any(cell.strip() for cell in row)]
    joined = "\n".join(rows)
    return _chunk_text(joined)


def extract_text(file_bytes, file_type):
    extractors = {
        "pdf": extract_pdf,
        "docx": extract_docx,
        "txt": extract_txt,
        "csv": extract_csv,
    }
    extractor = extractors.get(file_type.lower())
    if not extractor:
        return []
    return extractor(file_bytes)
