from academic_supervisor.agents.schema import ReviewIssue

_MAX_SNIPPET_RATIO = 0.6
# A single short sentence's grammatical fix is naturally close in length to the
# original, so only apply the ratio check to genuine multi-sentence paragraphs.
_MIN_PARAGRAPH_WORDS_FOR_CHECK = 20


def is_full_rewrite(paragraph: str, suggested_fix: str) -> bool:
    paragraph_words = paragraph.split()
    if len(paragraph_words) < _MIN_PARAGRAPH_WORDS_FOR_CHECK:
        return False

    fix_words = suggested_fix.split()
    return len(fix_words) >= _MAX_SNIPPET_RATIO * len(paragraph_words)


def enforce_snippet_only(issues: list[ReviewIssue], paragraph: str) -> list[ReviewIssue]:
    return [issue for issue in issues if not is_full_rewrite(paragraph, issue["suggested_fix"])]
