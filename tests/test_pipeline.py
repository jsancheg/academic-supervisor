from academic_supervisor.graph.pipeline import compile_graph


def test_graph_runs_end_to_end():
    app = compile_graph()
    result = app.invoke({"document": "sample text"})

    assert result["trace"][0] == "ingest_document"
    assert result["trace"][-1] == "render_output"
    assert set(result["trace"]) == {
        "ingest_document",
        "parse_document",
        "build_global_context",
        "run_rule_engine",
        "run_grammar_agent",
        "run_clarity_agent",
        "run_coherence_agent",
        "supervisor_merge",
        "render_output",
    }
