import re
from typing import TypedDict

_NUMBERED_HEADING = re.compile(r"^\d+(\.\d+)*\.?\s+\S.*$")
_CHAPTER_HEADING = re.compile(r"^chapter\s+\d+\b", re.IGNORECASE)
_MAX_HEADING_LENGTH = 80


class Section(TypedDict):
    title: str | None
    paragraphs: list[str]


def is_heading(paragraph: str) -> bool:
    line = paragraph.strip()
    if not line or len(line) > _MAX_HEADING_LENGTH:
        return False
    if _NUMBERED_HEADING.match(line) or _CHAPTER_HEADING.match(line):
        return True
    if line.endswith((".", ",", ";", ":")):
        return False
    return line.isupper() and any(char.isalpha() for char in line)


def detect_sections(paragraphs: list[str]) -> list[Section]:
    sections: list[Section] = []
    current: Section = {"title": None, "paragraphs": []}

    for paragraph in paragraphs:
        if is_heading(paragraph):
            if current["title"] is not None or current["paragraphs"]:
                sections.append(current)
            current = {"title": paragraph, "paragraphs": []}
        else:
            current["paragraphs"].append(paragraph)

    if current["title"] is not None or current["paragraphs"]:
        sections.append(current)

    return sections
