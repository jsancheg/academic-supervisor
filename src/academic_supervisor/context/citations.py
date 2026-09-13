import re
from typing import Literal, TypedDict

_PARENTHETICAL_CITATION = re.compile(r"\(([A-Z][^()]*?,\s*\d{4}[a-z]?)\)")
_NARRATIVE_CITATION = re.compile(
    r"\b([A-Z][A-Za-z\-]+(?:\s(?:and|&|et al\.?)\s[A-Za-z\-]+)*)\s\((\d{4}[a-z]?)\)"
)


class CitationEntry(TypedDict):
    raw: str
    style: Literal["parenthetical", "narrative"]
    paragraph_index: int


def build_citation_index(paragraphs: list[str]) -> list[CitationEntry]:
    index: list[CitationEntry] = []

    for paragraph_index, paragraph in enumerate(paragraphs):
        for match in _PARENTHETICAL_CITATION.finditer(paragraph):
            index.append(
                {
                    "raw": match.group(0),
                    "style": "parenthetical",
                    "paragraph_index": paragraph_index,
                }
            )
        for match in _NARRATIVE_CITATION.finditer(paragraph):
            index.append(
                {
                    "raw": match.group(0),
                    "style": "narrative",
                    "paragraph_index": paragraph_index,
                }
            )

    return index
