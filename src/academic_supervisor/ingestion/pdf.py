from pathlib import Path
from typing import IO

import fitz


def _open(source: str | Path | bytes | IO[bytes]) -> fitz.Document:
    if isinstance(source, (bytes, bytearray)):
        return fitz.open(stream=bytes(source), filetype="pdf")
    if hasattr(source, "read"):
        return fitz.open(stream=source.read(), filetype="pdf")
    return fitz.open(source)


def extract_pages_text(source: str | Path | bytes | IO[bytes]) -> list[str]:
    with _open(source) as doc:
        return [page.get_text("text") for page in doc]


def read_pdf(source: str | Path | bytes | IO[bytes]) -> str:
    pages = extract_pages_text(source)
    return "\n\n".join(page.strip() for page in pages if page.strip())
