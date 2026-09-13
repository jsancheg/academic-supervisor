from academic_supervisor.context.schema import init_session_state


def test_init_session_state_sets_all_default_keys():
    state: dict = {}

    init_session_state(state)

    assert state["document"] == ""
    assert state["parsed_paragraphs"] == []
    assert state["issues"] == []
    assert state["citation_index"] == []
    assert state["figure_table_registry"] == []
    assert state["global_context"] == {
        "thesis": None,
        "section_structure_map": [],
        "terminology_map": {},
        "citation_index": [],
        "figure_table_registry": [],
    }


def test_init_session_state_does_not_clobber_existing_keys():
    state = {"document": "already loaded"}

    init_session_state(state)

    assert state["document"] == "already loaded"
    assert state["parsed_paragraphs"] == []


def test_init_session_state_defaults_are_independent_instances():
    state_a: dict = {}
    state_b: dict = {}

    init_session_state(state_a)
    init_session_state(state_b)
    state_a["parsed_paragraphs"].append("mutated")

    assert state_b["parsed_paragraphs"] == []
