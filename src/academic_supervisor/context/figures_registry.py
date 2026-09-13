import re
from typing import Literal, TypedDict

from academic_supervisor.ingestion.figures import FigureTableEntry

_REFERENCE_PATTERN = re.compile(r"\b(Figure|Fig\.?|Table)\s+(\d+)\b", re.IGNORECASE)


class RegistryEntry(TypedDict):
    type: Literal["figure", "table"]
    number: int
    caption: str | None
    page: int | None
    has_caption: bool
    referenced_in_paragraphs: list[int]


def build_figure_table_registry(
    paragraphs: list[str], captions: list[FigureTableEntry]
) -> list[RegistryEntry]:
    registry: dict[tuple[str, int], RegistryEntry] = {}

    for caption in captions:
        key = (caption["type"], caption["number"])
        registry[key] = {
            "type": caption["type"],
            "number": caption["number"],
            "caption": caption["caption"],
            "page": caption["page"],
            "has_caption": True,
            "referenced_in_paragraphs": [],
        }

    for paragraph_index, paragraph in enumerate(paragraphs):
        for match in _REFERENCE_PATTERN.finditer(paragraph):
            label, number = match.groups()
            entry_type: Literal["figure", "table"] = (
                "table" if label.lower().startswith("table") else "figure"
            )
            key = (entry_type, int(number))
            if key not in registry:
                registry[key] = {
                    "type": entry_type,
                    "number": int(number),
                    "caption": None,
                    "page": None,
                    "has_caption": False,
                    "referenced_in_paragraphs": [],
                }
            registry[key]["referenced_in_paragraphs"].append(paragraph_index)

    return sorted(registry.values(), key=lambda entry: (entry["type"], entry["number"]))
