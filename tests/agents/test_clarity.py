from academic_supervisor.agents.clarity import run_clarity_agent


class _FakeLLM:
    def __init__(self, responses):
        self._responses = list(responses)
        self.prompts = []

    def invoke(self, prompt):
        self.prompts.append(prompt)
        return self._responses.pop(0)


def test_flags_clarity_issue_with_all_required_fields():
    llm = _FakeLLM(
        [
            """[
                {
                    "problem": "Overly dense sentence",
                    "location": "the aforementioned multifaceted considerations",
                    "why": "The phrasing obscures the actual point being made",
                    "suggested_fix": "these factors"
                }
            ]"""
        ]
    )

    issues = run_clarity_agent(
        ["We must account for the aforementioned multifaceted considerations."], llm
    )

    assert len(issues) == 1
    issue = issues[0]
    assert issue["source"] == "clarity"
    assert issue["paragraph_index"] == 0
    assert issue["problem"] == "Overly dense sentence"
    assert issue["suggested_fix"] == "these factors"


def test_no_issues_returns_empty_list():
    llm = _FakeLLM(["[]"])

    issues = run_clarity_agent(["This paragraph is already clear."], llm)

    assert issues == []


def test_skips_blank_paragraphs_without_calling_llm():
    llm = _FakeLLM([])

    issues = run_clarity_agent(["", "   "], llm)

    assert issues == []
    assert llm.prompts == []


def test_tolerates_malformed_llm_output():
    llm = _FakeLLM(["not valid json at all"])

    issues = run_clarity_agent(["Some paragraph."], llm)

    assert issues == []


def test_prompt_scopes_role_to_clarity_not_grammar_or_coherence():
    llm = _FakeLLM(["[]"])

    run_clarity_agent(["A paragraph to review."], llm)

    prompt = llm.prompts[0]
    assert "Clarity, flow, and readability" in prompt
    assert "Never rewrite the whole paragraph" in prompt
