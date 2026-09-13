from academic_supervisor.agents.grammar import run_grammar_agent


class _FakeLLM:
    def __init__(self, responses):
        self._responses = list(responses)
        self.prompts = []

    def invoke(self, prompt):
        self.prompts.append(prompt)
        return self._responses.pop(0)


def test_flags_grammar_error_with_all_required_fields():
    llm = _FakeLLM(
        [
            """[
                {
                    "problem": "Subject-verb disagreement",
                    "location": "The results shows a clear trend",
                    "why": "The plural subject 'results' requires the verb 'show'",
                    "suggested_fix": "The results show a clear trend"
                }
            ]"""
        ]
    )

    issues = run_grammar_agent(["The results shows a clear trend."], llm)

    assert len(issues) == 1
    issue = issues[0]
    assert issue["source"] == "grammar"
    assert issue["paragraph_index"] == 0
    assert issue["problem"] == "Subject-verb disagreement"
    assert issue["location"] == "The results shows a clear trend"
    assert issue["why"]
    assert issue["suggested_fix"] == "The results show a clear trend"


def test_no_issues_returns_empty_list():
    llm = _FakeLLM(["[]"])

    issues = run_grammar_agent(["This sentence is grammatically correct."], llm)

    assert issues == []


def test_skips_blank_paragraphs_without_calling_llm():
    llm = _FakeLLM([])

    issues = run_grammar_agent(["", "   "], llm)

    assert issues == []
    assert llm.prompts == []


def test_tolerates_malformed_llm_output():
    llm = _FakeLLM(["not valid json at all"])

    issues = run_grammar_agent(["Some paragraph."], llm)

    assert issues == []


def test_ignores_entries_missing_required_fields():
    llm = _FakeLLM(
        [
            """[
                {"problem": "Missing fix", "location": "some text"}
            ]"""
        ]
    )

    issues = run_grammar_agent(["Incomplete entry."], llm)

    assert issues == []


def test_tracks_paragraph_index_across_multiple_paragraphs():
    llm = _FakeLLM(
        [
            "[]",
            """[
                {
                    "problem": "Incorrect verb form",
                    "location": "He go to the library",
                    "why": "Third-person singular subjects require 'goes'",
                    "suggested_fix": "He goes to the library"
                }
            ]""",
        ]
    )

    issues = run_grammar_agent(
        ["First paragraph is fine.", "He go to the library."], llm
    )

    assert len(issues) == 1
    assert issues[0]["paragraph_index"] == 1


def test_prompt_forbids_full_paragraph_rewrites():
    llm = _FakeLLM(["[]"])

    run_grammar_agent(["A paragraph to review."], llm)

    assert "Never rewrite the whole paragraph" in llm.prompts[0]
