from pathlib import Path
from typing import IO

import pymupdf


def _open(source: str | Path | bytes | IO[bytes]) -> pymupdf.Document:
    if isinstance(source, (bytes, bytearray)):
        return pymupdf.open(stream=bytes(source), filetype="pdf")
    if hasattr(source, "read"):
        return pymupdf.open(stream=source.read(), filetype="pdf")
    return pymupdf.open(source)


def extract_pages_text(source: str | Path | bytes | IO[bytes]) -> list[str]:
    with _open(source) as doc:
        return [page.get_text("text") for page in doc]


def read_pdf(source: str | Path | bytes | IO[bytes]) -> str:
    pages = extract_pages_text(source)
    return "\n\n".join(page.strip() for page in pages if page.strip())
