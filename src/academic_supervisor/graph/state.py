import operator
from typing import Annotated, Any, TypedDict


class SupervisorState(TypedDict, total=False):
    document: str
    parsed_paragraphs: list[str]
    global_context: dict[str, Any]
    issues: list[dict[str, Any]]
    citation_index: list[dict[str, Any]]
    figure_table_registry: list[dict[str, Any]]
    report: str
    # Annotated with operator.add so parallel agent nodes (grammar/clarity/coherence)
    # can each append to the trace without clobbering each other's writes.
    trace: Annotated[list[str], operator.add]
