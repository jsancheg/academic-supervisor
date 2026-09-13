from academic_supervisor.agents.coherence import run_coherence_agent


class _FakeLLM:
    def __init__(self, responses):
        self._responses = list(responses)
        self.prompts = []

    def invoke(self, prompt):
        self.prompts.append(prompt)
        return self._responses.pop(0)


def test_flags_coherence_issue_with_all_required_fields():
    llm = _FakeLLM(
        [
            """[
                {
                    "problem": "Contradicts the thesis",
                    "location": "correlation does not imply causation",
                    "why": "This directly contradicts the paper's causal claim",
                    "suggested_fix": "reframe as a causal, supported claim"
                }
            ]"""
        ]
    )

    issues = run_coherence_agent(
        ["Here, correlation does not imply causation."],
        {"thesis": "X causes Y."},
        llm,
    )

    assert len(issues) == 1
    issue = issues[0]
    assert issue["source"] == "coherence"
    assert issue["paragraph_index"] == 0
    assert issue["problem"] == "Contradicts the thesis"


def test_thesis_is_embedded_in_prompt():
    llm = _FakeLLM(["[]"])

    run_coherence_agent(["Some paragraph."], {"thesis": "X causes Y."}, llm)

    assert "X causes Y." in llm.prompts[0]
    assert "Document context:" in llm.prompts[0]


def test_missing_thesis_omits_context_section():
    llm = _FakeLLM(["[]"])

    run_coherence_agent(["Some paragraph."], {}, llm)

    assert "Document context:" not in llm.prompts[0]


def test_no_issues_returns_empty_list():
    llm = _FakeLLM(["[]"])

    issues = run_coherence_agent(["Consistent paragraph."], {"thesis": "X causes Y."}, llm)

    assert issues == []


def test_skips_blank_paragraphs_without_calling_llm():
    llm = _FakeLLM([])

    issues = run_coherence_agent(["", "   "], {"thesis": "X causes Y."}, llm)

    assert issues == []
    assert llm.prompts == []


def test_tolerates_malformed_llm_output():
    llm = _FakeLLM(["not valid json at all"])

    issues = run_coherence_agent(["Some paragraph."], {"thesis": "X causes Y."}, llm)

    assert issues == []
