import re
from typing import TypedDict

from academic_supervisor.context.citations import CitationEntry

_HAS_AND_WORD = re.compile(r"\band\b", re.IGNORECASE)


class CitationFormatIssue(TypedDict):
    raw: str
    paragraph_index: int
    problem: str


def validate_citation_format(citations: list[CitationEntry]) -> list[CitationFormatIssue]:
    issues: list[CitationFormatIssue] = []

    for citation in citations:
        raw = citation["raw"]

        if citation["style"] == "parenthetical" and _HAS_AND_WORD.search(raw):
            issues.append(
                {
                    "raw": raw,
                    "paragraph_index": citation["paragraph_index"],
                    "problem": "Parenthetical citation uses 'and' instead of '&'",
                }
            )
        elif citation["style"] == "narrative" and "&" in raw:
            issues.append(
                {
                    "raw": raw,
                    "paragraph_index": citation["paragraph_index"],
                    "problem": "Narrative citation uses '&' instead of 'and'",
                }
            )

    return issues
