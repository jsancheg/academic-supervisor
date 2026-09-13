import json
from typing import Callable

from academic_supervisor.agents.prompts import build_prompt
from academic_supervisor.agents.schema import AgentSource, ReviewIssue

LLMCallable = Callable[[str], str]

_REQUIRED_FIELDS = ("problem", "location", "why", "suggested_fix")


def run_agent(
    source: AgentSource,
    role_instructions: str,
    paragraph: str,
    paragraph_index: int,
    invoke: LLMCallable,
    context: str = "",
) -> list[ReviewIssue]:
    prompt = build_prompt(role_instructions, paragraph, paragraph_index, context)
    raw_response = invoke(prompt)

    return _parse_issues(raw_response, source, paragraph_index)


def _parse_issues(
    raw_response: str, source: AgentSource, paragraph_index: int
) -> list[ReviewIssue]:
    try:
        parsed = json.loads(_extract_json_array(raw_response))
    except (json.JSONDecodeError, ValueError):
        return []

    if not isinstance(parsed, list):
        return []

    issues: list[ReviewIssue] = []
    for item in parsed:
        if not isinstance(item, dict) or not all(key in item for key in _REQUIRED_FIELDS):
            continue
        issues.append(
            {
                "problem": str(item["problem"]),
                "location": str(item["location"]),
                "why": str(item["why"]),
                "suggested_fix": str(item["suggested_fix"]),
                "source": source,
                "paragraph_index": paragraph_index,
            }
        )

    return issues


def _extract_json_array(text: str) -> str:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON array found in response")
    return text[start : end + 1]
