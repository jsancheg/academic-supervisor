from academic_supervisor.rules.citation_format import validate_citation_format


def _citation(raw: str, style: str, paragraph_index: int = 0) -> dict:
    return {"raw": raw, "style": style, "paragraph_index": paragraph_index}


def test_flags_parenthetical_citation_using_and():
    citations = [_citation("(Smith and Jones, 2020)", "parenthetical")]

    issues = validate_citation_format(citations)

    assert len(issues) == 1
    assert issues[0]["raw"] == "(Smith and Jones, 2020)"
    assert "and" in issues[0]["problem"]


def test_accepts_parenthetical_citation_using_ampersand():
    citations = [_citation("(Smith & Jones, 2020)", "parenthetical")]

    assert validate_citation_format(citations) == []


def test_flags_narrative_citation_using_ampersand():
    citations = [_citation("Smith & Jones (2020)", "narrative")]

    issues = validate_citation_format(citations)

    assert len(issues) == 1
    assert issues[0]["raw"] == "Smith & Jones (2020)"
    assert "&" in issues[0]["problem"]


def test_accepts_narrative_citation_using_and():
    citations = [_citation("Smith and Jones (2020)", "narrative")]

    assert validate_citation_format(citations) == []


def test_single_author_citations_are_never_flagged():
    citations = [
        _citation("(Smith, 2020)", "parenthetical"),
        _citation("Smith (2020)", "narrative"),
    ]

    assert validate_citation_format(citations) == []
