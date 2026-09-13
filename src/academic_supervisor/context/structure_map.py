from typing import TypedDict

from academic_supervisor.ingestion.sections import Section


class SectionStructureEntry(TypedDict):
    title: str | None
    paragraph_count: int


def build_section_structure_map(sections: list[Section]) -> list[SectionStructureEntry]:
    return [
        {"title": section["title"], "paragraph_count": len(section["paragraphs"])}
        for section in sections
    ]
