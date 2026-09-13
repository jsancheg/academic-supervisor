from academic_supervisor.agents import grammar as grammar_agent
from academic_supervisor.graph.state import SupervisorState


def _mark(state: SupervisorState, name: str) -> SupervisorState:
    # `trace` uses an operator.add reducer (see state.py), so just return the
    # increment — LangGraph concatenates it onto the existing list.
    return {"trace": [name]}


def ingest_document(state: SupervisorState) -> SupervisorState:
    """Placeholder for issues #6/#7: read text/PDF into state["document"]."""
    return _mark(state, "ingest_document")


def parse_document(state: SupervisorState) -> SupervisorState:
    """Placeholder for issues #8/#9/#10: paragraphs, sections, figures/tables."""
    return _mark(state, "parse_document")


def build_global_context(state: SupervisorState) -> SupervisorState:
    """Placeholder for issues #11-#16: thesis, structure map, terminology, indexes."""
    return _mark(state, "build_global_context")


def run_rule_engine(state: SupervisorState) -> SupervisorState:
    """Placeholder for issues #17-#20: citations, numbering, labels, structure."""
    return _mark(state, "run_rule_engine")


def run_grammar_agent(state: SupervisorState) -> SupervisorState:
    """Issue #21: LLM-based grammar review, sentence-level, snippets only."""
    paragraphs = state.get("parsed_paragraphs", [])
    result = _mark(state, "run_grammar_agent")
    if paragraphs:
        llm = grammar_agent.build_grammar_llm()
        result["issues"] = grammar_agent.run_grammar_agent(paragraphs, llm)
    return result


def run_clarity_agent(state: SupervisorState) -> SupervisorState:
    """Placeholder for issue #22: clarity/flow review."""
    return _mark(state, "run_clarity_agent")


def run_coherence_agent(state: SupervisorState) -> SupervisorState:
    """Placeholder for issue #23: global argument consistency review."""
    return _mark(state, "run_coherence_agent")


def supervisor_merge(state: SupervisorState) -> SupervisorState:
    """Placeholder for issues #26-#29: merge, de-duplicate, resolve conflicts."""
    return _mark(state, "supervisor_merge")


def render_output(state: SupervisorState) -> SupervisorState:
    """Placeholder for issues #30-#33: structured report rendering."""
    return _mark(state, "render_output")
