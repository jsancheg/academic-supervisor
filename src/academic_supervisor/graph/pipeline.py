from langgraph.graph import END, START, StateGraph

from academic_supervisor.graph import nodes
from academic_supervisor.graph.state import SupervisorState


def build_graph() -> StateGraph:
    graph = StateGraph(SupervisorState)

    graph.add_node("ingest_document", nodes.ingest_document)
    graph.add_node("parse_document", nodes.parse_document)
    graph.add_node("build_global_context", nodes.build_global_context)
    graph.add_node("run_rule_engine", nodes.run_rule_engine)
    graph.add_node("run_grammar_agent", nodes.run_grammar_agent)
    graph.add_node("run_clarity_agent", nodes.run_clarity_agent)
    graph.add_node("run_coherence_agent", nodes.run_coherence_agent)
    graph.add_node("supervisor_merge", nodes.supervisor_merge)
    graph.add_node("render_output", nodes.render_output)

    graph.add_edge(START, "ingest_document")
    graph.add_edge("ingest_document", "parse_document")
    graph.add_edge("parse_document", "build_global_context")
    graph.add_edge("build_global_context", "run_rule_engine")

    # Rule engine fans out to the three LLM agents, which converge on the
    # supervisor merge node. See _docs/plan.md sections 6.3-6.5.
    graph.add_edge("run_rule_engine", "run_grammar_agent")
    graph.add_edge("run_rule_engine", "run_clarity_agent")
    graph.add_edge("run_rule_engine", "run_coherence_agent")
    graph.add_edge("run_grammar_agent", "supervisor_merge")
    graph.add_edge("run_clarity_agent", "supervisor_merge")
    graph.add_edge("run_coherence_agent", "supervisor_merge")

    graph.add_edge("supervisor_merge", "render_output")
    graph.add_edge("render_output", END)

    return graph


def compile_graph():
    return build_graph().compile()
