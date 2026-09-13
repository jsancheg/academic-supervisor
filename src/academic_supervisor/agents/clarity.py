from typing import Protocol

from academic_supervisor.agents.base import run_agent
from academic_supervisor.agents.schema import ReviewIssue

_CLARITY_MODEL = "phi3:latest"

_ROLE_INSTRUCTIONS = (
    "Clarity, flow, and readability at the paragraph level only. Point out "
    "wordy, ambiguous, or hard-to-follow phrasing. Ignore grammar mechanics "
    "and global argument consistency. Suggested fixes must be short rewrite "
    "snippets for the specific unclear phrase, never a full paragraph rewrite."
)


class ClarityLLM(Protocol):
    def invoke(self, prompt: str) -> str: ...


def build_clarity_llm(
    model: str = _CLARITY_MODEL, base_url: str = "http://localhost:11434"
) -> ClarityLLM:
    from langchain_ollama import OllamaLLM

    return OllamaLLM(model=model, base_url=base_url)


def run_clarity_agent(paragraphs: list[str], llm: ClarityLLM) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []

    for index, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            continue

        issues.extend(run_agent("clarity", _ROLE_INSTRUCTIONS, paragraph, index, llm.invoke))

    return issues
