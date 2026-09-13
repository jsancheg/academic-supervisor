import re
from pathlib import Path
from typing import IO, Literal, TypedDict

from academic_supervisor.ingestion.pdf import extract_pages_text

_CAPTION_PATTERN = re.compile(r"^(Figure|Fig\.?|Table)\s+(\d+)\s*[:.\-]?\s*(.*)$", re.IGNORECASE)


class FigureTableEntry(TypedDict):
    type: Literal["figure", "table"]
    number: int
    caption: str
    page: int


def detect_figures_tables(source: str | Path | bytes | IO[bytes]) -> list[FigureTableEntry]:
    entries: list[FigureTableEntry] = []

    for page_number, page_text in enumerate(extract_pages_text(source), start=1):
        for line in page_text.split("\n"):
            match = _CAPTION_PATTERN.match(line.strip())
            if not match:
                continue

            label, number, caption = match.groups()
            entry_type: Literal["figure", "table"] = (
                "table" if label.lower().startswith("table") else "figure"
            )
            entries.append(
                {
                    "type": entry_type,
                    "number": int(number),
                    "caption": caption.strip(),
                    "page": page_number,
                }
            )

    return entries
