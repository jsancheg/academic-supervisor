from academic_supervisor.rules.missing_labels import detect_missing_labels


def _entry(kind: str, number: int, has_caption: bool, references: list[int]) -> dict:
    return {
        "type": kind,
        "number": number,
        "caption": "caption" if has_caption else None,
        "page": 1 if has_caption else None,
        "has_caption": has_caption,
        "referenced_in_paragraphs": references,
    }


def test_no_issue_when_captioned_and_referenced():
    registry = [_entry("figure", 1, True, [0])]

    assert detect_missing_labels(registry) == []


def test_flags_referenced_but_uncaptioned_entry():
    registry = [_entry("figure", 1, False, [0])]

    assert detect_missing_labels(registry) == [
        {"type": "figure", "number": 1, "problem": "missing_caption"}
    ]


def test_flags_captioned_but_unreferenced_entry():
    registry = [_entry("table", 2, True, [])]

    assert detect_missing_labels(registry) == [
        {"type": "table", "number": 2, "problem": "not_referenced"}
    ]
