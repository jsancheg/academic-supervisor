import copy
from typing import Any, MutableMapping, TypedDict


class GlobalContext(TypedDict, total=False):
    thesis: str | None
    section_structure_map: list[dict[str, Any]]
    terminology_map: dict[str, dict[str, list[int]]]
    citation_index: list[dict[str, Any]]
    figure_table_registry: list[dict[str, Any]]


class SessionState(TypedDict, total=False):
    document: str
    parsed_paragraphs: list[str]
    global_context: GlobalContext
    issues: list[dict[str, Any]]
    citation_index: list[dict[str, Any]]
    figure_table_registry: list[dict[str, Any]]


def _default_global_context() -> GlobalContext:
    return {
        "thesis": None,
        "section_structure_map": [],
        "terminology_map": {},
        "citation_index": [],
        "figure_table_registry": [],
    }


def _default_session_state() -> SessionState:
    return {
        "document": "",
        "parsed_paragraphs": [],
        "global_context": _default_global_context(),
        "issues": [],
        "citation_index": [],
        "figure_table_registry": [],
    }


def init_session_state(state: MutableMapping[str, Any]) -> None:
    for key, value in _default_session_state().items():
        if key not in state:
            state[key] = copy.deepcopy(value)
