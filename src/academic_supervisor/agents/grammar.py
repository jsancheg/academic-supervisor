from typing import Protocol

from academic_supervisor.agents.base import run_agent
from academic_supervisor.agents.schema import ReviewIssue

_GRAMMAR_MODEL = "llama3.2:3b"

_ROLE_INSTRUCTIONS = (
    "Sentence-level grammar, punctuation, and agreement correctness only. "
    "Ignore style, clarity, and argument quality."
)


class GrammarLLM(Protocol):
    def invoke(self, prompt: str) -> str: ...


def build_grammar_llm(
    model: str = _GRAMMAR_MODEL, base_url: str = "http://localhost:11434"
) -> GrammarLLM:
    from langchain_ollama import OllamaLLM

    return OllamaLLM(model=model, base_url=base_url)


def run_grammar_agent(paragraphs: list[str], llm: GrammarLLM) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []

    for index, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            continue

        issues.extend(
            run_agent("grammar", _ROLE_INSTRUCTIONS, paragraph, index, llm.invoke)
        )

    return issues
