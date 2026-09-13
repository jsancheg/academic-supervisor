from academic_supervisor.context.thesis import extract_thesis


def test_extract_thesis_prefers_abstract_section():
    sections = [
        {"title": "1. Introduction", "paragraphs": ["Intro text."]},
        {"title": "Abstract", "paragraphs": ["This paper argues X.", "More detail."]},
    ]

    assert extract_thesis(sections) == "This paper argues X."


def test_extract_thesis_matches_abstract_case_and_numbering_insensitively():
    sections = [{"title": "2. ABSTRACT", "paragraphs": ["Main claim here."]}]

    assert extract_thesis(sections) == "Main claim here."


def test_extract_thesis_falls_back_to_first_paragraph_without_abstract():
    sections = [
        {"title": None, "paragraphs": []},
        {"title": "1. Introduction", "paragraphs": ["First real paragraph."]},
    ]

    assert extract_thesis(sections) == "First real paragraph."


def test_extract_thesis_returns_none_when_no_paragraphs():
    assert extract_thesis([{"title": None, "paragraphs": []}]) is None
