from typing import Literal, TypedDict

from academic_supervisor.ingestion.figures import FigureTableEntry


class NumberingIssue(TypedDict):
    type: Literal["figure", "table"]
    expected: int
    found: int
    page: int


def check_numbering_order(captions: list[FigureTableEntry]) -> list[NumberingIssue]:
    issues: list[NumberingIssue] = []

    for kind in ("figure", "table"):
        entries = [caption for caption in captions if caption["type"] == kind]
        for expected, entry in enumerate(entries, start=1):
            if entry["number"] != expected:
                issues.append(
                    {
                        "type": kind,
                        "expected": expected,
                        "found": entry["number"],
                        "page": entry["page"],
                    }
                )

    return issues
