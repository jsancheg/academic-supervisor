import re
from typing import TypedDict

from academic_supervisor.ingestion.sections import Section

_TOP_LEVEL_NUMBERED_HEADING = re.compile(r"^(\d+)(\.\d+)*\.?\s")


class StructuralIssue(TypedDict):
    title: str
    expected: int
    found: int


def check_heading_order(sections: list[Section]) -> list[StructuralIssue]:
    issues: list[StructuralIssue] = []
    expected = 1

    for section in sections:
        title = section["title"]
        if not title:
            continue

        match = _TOP_LEVEL_NUMBERED_HEADING.match(title.strip())
        if not match or match.group(2) is not None:
            # Not a numbered heading, or a sub-heading (e.g. "2.1 ...") - skip.
            continue

        found = int(match.group(1))
        if found != expected:
            issues.append({"title": title, "expected": expected, "found": found})
        expected = found + 1

    return issues
