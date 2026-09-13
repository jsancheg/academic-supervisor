from typing import Any, Protocol

from academic_supervisor.agents.base import run_agent
from academic_supervisor.agents.schema import ReviewIssue

_COHERENCE_MODEL = "qwen2.5:7b-instruct-q4_K_M"

_ROLE_INSTRUCTIONS = (
    "Global argument consistency only. Judge whether this paragraph logically "
    "supports and stays consistent with the document's stated thesis. Flag "
    "contradictions, unsupported tangents, or drift from the main argument. "
    "Ignore grammar mechanics and sentence-level clarity."
)


class CoherenceLLM(Protocol):
    def invoke(self, prompt: str) -> str: ...


def build_coherence_llm(
    model: str = _COHERENCE_MODEL, base_url: str = "http://localhost:11434"
) -> CoherenceLLM:
    from langchain_ollama import OllamaLLM

    return OllamaLLM(model=model, base_url=base_url)


def run_coherence_agent(
    paragraphs: list[str], global_context: dict[str, Any], llm: CoherenceLLM
) -> list[ReviewIssue]:
    thesis = global_context.get("thesis") or ""
    context = f"Document's main thesis: {thesis}" if thesis else ""

    issues: list[ReviewIssue] = []
    for index, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            continue

        issues.extend(
            run_agent("coherence", _ROLE_INSTRUCTIONS, paragraph, index, llm.invoke, context)
        )

    return issues
