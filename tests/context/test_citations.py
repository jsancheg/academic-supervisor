from academic_supervisor.context.citations import build_citation_index


def test_build_citation_index_detects_parenthetical_citation():
    paragraphs = ["As shown in (Smith, 2020), the results are clear."]

    index = build_citation_index(paragraphs)

    assert index == [
        {"raw": "(Smith, 2020)", "style": "parenthetical", "paragraph_index": 0}
    ]


def test_build_citation_index_detects_narrative_citation():
    paragraphs = ["Smith (2020) argues that the results are clear."]

    index = build_citation_index(paragraphs)

    assert index == [
        {"raw": "Smith (2020)", "style": "narrative", "paragraph_index": 0}
    ]


def test_build_citation_index_detects_multiple_citations_in_one_paragraph():
    paragraphs = ["Both (Smith, 2020) and (Jones, 2019) agree on this point."]

    index = build_citation_index(paragraphs)

    assert len(index) == 2
    assert {entry["raw"] for entry in index} == {"(Smith, 2020)", "(Jones, 2019)"}
    assert all(entry["paragraph_index"] == 0 for entry in index)


def test_build_citation_index_returns_empty_when_no_citations():
    assert build_citation_index(["No citations in this paragraph at all."]) == []
