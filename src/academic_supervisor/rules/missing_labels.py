from typing import Literal, TypedDict

from academic_supervisor.context.figures_registry import RegistryEntry


class MissingLabelIssue(TypedDict):
    type: Literal["figure", "table"]
    number: int
    problem: Literal["missing_caption", "not_referenced"]


def detect_missing_labels(registry: list[RegistryEntry]) -> list[MissingLabelIssue]:
    issues: list[MissingLabelIssue] = []

    for entry in registry:
        if not entry["has_caption"]:
            issues.append(
                {"type": entry["type"], "number": entry["number"], "problem": "missing_caption"}
            )
        elif not entry["referenced_in_paragraphs"]:
            issues.append(
                {"type": entry["type"], "number": entry["number"], "problem": "not_referenced"}
            )

    return issues
