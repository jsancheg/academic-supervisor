import re
from pathlib import Path
from typing import IO


def read_text(source: str | Path | IO[bytes]) -> str:
    if hasattr(source, "read"):
        raw = source.read()
    else:
        raw = Path(source).read_bytes()

    if isinstance(raw, bytes):
        try:
            decoded = raw.decode("utf-8")
        except UnicodeDecodeError:
            decoded = raw.decode("latin-1")
    else:
        decoded = raw

    return normalize_whitespace(decoded)


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip("\n")
