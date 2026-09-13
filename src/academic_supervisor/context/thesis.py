from academic_supervisor.ingestion.sections import Section


def extract_thesis(sections: list[Section]) -> str | None:
    for section in sections:
        title = section["title"] or ""
        if title.strip().lower().lstrip("0123456789. ") == "abstract":
            if section["paragraphs"]:
                return section["paragraphs"][0]

    for section in sections:
        if section["paragraphs"]:
            return section["paragraphs"][0]

    return None
