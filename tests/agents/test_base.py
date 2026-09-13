from academic_supervisor.agents.base import run_agent


def _invoke_returning(response):
    def invoke(prompt):
        invoke.last_prompt = prompt
        return response

    return invoke


def test_run_agent_parses_valid_issue():
    invoke = _invoke_returning(
        """[
            {
                "problem": "P",
                "location": "L",
                "why": "W",
                "suggested_fix": "F"
            }
        ]"""
    )

    issues = run_agent("grammar", "role", "paragraph text", 2, invoke)

    assert issues == [
        {
            "problem": "P",
            "location": "L",
            "why": "W",
            "suggested_fix": "F",
            "source": "grammar",
            "paragraph_index": 2,
        }
    ]


def test_run_agent_returns_empty_for_empty_array():
    invoke = _invoke_returning("[]")

    assert run_agent("clarity", "role", "text", 0, invoke) == []


def test_run_agent_drops_entries_missing_fields():
    invoke = _invoke_returning('[{"problem": "P", "location": "L"}]')

    assert run_agent("coherence", "role", "text", 0, invoke) == []


def test_run_agent_tolerates_non_json_response():
    invoke = _invoke_returning("I cannot find any issues.")

    assert run_agent("grammar", "role", "text", 0, invoke) == []


def test_run_agent_extracts_array_from_surrounding_text():
    invoke = _invoke_returning(
        'Sure, here you go:\n[{"problem": "P", "location": "L", "why": "W", '
        '"suggested_fix": "F"}]\nHope that helps.'
    )

    issues = run_agent("grammar", "role", "text", 0, invoke)

    assert len(issues) == 1
