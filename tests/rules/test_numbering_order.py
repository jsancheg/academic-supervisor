from academic_supervisor.rules.numbering_order import check_numbering_order


def _entry(kind: str, number: int, page: int) -> dict:
    return {"type": kind, "number": number, "caption": "caption", "page": page}


def test_no_issues_when_sequential():
    captions = [_entry("figure", 1, 1), _entry("figure", 2, 2), _entry("table", 1, 3)]

    assert check_numbering_order(captions) == []


def test_flags_skipped_figure_number():
    captions = [_entry("figure", 1, 1), _entry("figure", 3, 2)]

    issues = check_numbering_order(captions)

    assert issues == [{"type": "figure", "expected": 2, "found": 3, "page": 2}]


def test_figure_and_table_sequences_are_independent():
    captions = [_entry("figure", 1, 1), _entry("table", 1, 1), _entry("figure", 2, 2)]

    assert check_numbering_order(captions) == []
