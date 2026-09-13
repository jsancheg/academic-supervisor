import re


def split_paragraphs(text: str) -> list[str]:
    raw_chunks = re.split(r"\n\s*\n", text)
    return [chunk.strip() for chunk in raw_chunks if chunk.strip()]
