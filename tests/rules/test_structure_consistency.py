from academic_supervisor.rules.structure_consistency import check_heading_order


def _section(title: str | None) -> dict:
    return {"title": title, "paragraphs": ["text"]}


def test_no_issues_when_headings_correctly_ordered():
    sections = [_section("1. Introduction"), _section("2. Methodology"), _section("3. Conclusion")]

    assert check_heading_order(sections) == []


def test_flags_skipped_section_number():
    sections = [_section("1. Introduction"), _section("3. Conclusion")]

    issues = check_heading_order(sections)

    assert issues == [{"title": "3. Conclusion", "expected": 2, "found": 3}]


def test_sub_headings_do_not_break_top_level_sequence():
    sections = [
        _section("1. Introduction"),
        _section("2. Methodology"),
        _section("2.1 Data Collection"),
        _section("2.2 Analysis"),
        _section("3. Results"),
    ]

    assert check_heading_order(sections) == []
