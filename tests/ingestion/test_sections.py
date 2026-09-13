from academic_supervisor.ingestion.sections import detect_sections, is_heading


def test_is_heading_detects_numbered_heading():
    assert is_heading("1. Introduction")
    assert is_heading("2.3 Related Work")


def test_is_heading_detects_all_caps_heading():
    assert is_heading("ABSTRACT")


def test_is_heading_rejects_normal_sentence():
    assert not is_heading("This is a normal sentence in a paragraph.")


def test_detect_sections_groups_paragraphs_under_headings():
    paragraphs = [
        "1. Introduction",
        "This is the introduction text.",
        "2. Methodology",
        "This describes the method.",
        "More methodology detail.",
    ]

    sections = detect_sections(paragraphs)

    assert [s["title"] for s in sections] == ["1. Introduction", "2. Methodology"]
    assert sections[0]["paragraphs"] == ["This is the introduction text."]
    assert sections[1]["paragraphs"] == [
        "This describes the method.",
        "More methodology detail.",
    ]


def test_detect_sections_with_no_headings_returns_single_untitled_section():
    paragraphs = ["Just one paragraph.", "And another one."]

    sections = detect_sections(paragraphs)

    assert len(sections) == 1
    assert sections[0]["title"] is None
    assert sections[0]["paragraphs"] == paragraphs
