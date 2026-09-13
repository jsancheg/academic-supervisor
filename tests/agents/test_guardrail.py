from academic_supervisor.agents.guardrail import enforce_snippet_only, is_full_rewrite

_PARAGRAPH = (
    "This paragraph discusses several distinct points across multiple sentences, "
    "covering background context, a supporting argument, and a brief concluding "
    "remark, so it should be treated as a genuine multi-sentence paragraph."
)


def _issue(suggested_fix: str) -> dict:
    return {
        "problem": "p",
        "location": "l",
        "why": "w",
        "suggested_fix": suggested_fix,
        "source": "grammar",
        "paragraph_index": 0,
    }


def test_short_snippet_is_not_a_full_rewrite():
    assert not is_full_rewrite(_PARAGRAPH, "few words")


def test_near_full_paragraph_rewrite_is_flagged():
    rewrite = (
        "This section explains several distinct points across multiple sentences "
        "covering background details, a supporting claim, and a brief closing remark."
    )
    assert is_full_rewrite(_PARAGRAPH, rewrite)


def test_short_paragraph_is_never_flagged():
    short_paragraph = "Short paragraph here."
    assert not is_full_rewrite(short_paragraph, "An entirely different short paragraph.")


def test_enforce_snippet_only_drops_full_rewrites_and_keeps_snippets():
    rewrite = (
        "This section explains several distinct points across multiple sentences "
        "covering background details, a supporting claim, and a brief closing remark."
    )
    issues = [_issue("few words"), _issue(rewrite)]

    kept = enforce_snippet_only(issues, _PARAGRAPH)

    assert kept == [_issue("few words")]
