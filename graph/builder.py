from langgraph.graph import StateGraph, END
from graph.state import ResearchState
from agents.researcher import researcher_node
from agents.writer import writer_node
from agents.critic import critic_node
from graph.router import should_retry

def build_graph():
    g = StateGraph(ResearchState)

    g.add_node("researcher", researcher_node)
    g.add_node("writer",     writer_node)
    g.add_node("critic",     critic_node)

    g.set_entry_point("researcher")
    g.add_edge("researcher", "writer")
    g.add_edge("writer",     "critic")

    # Conditional: retry to writer or finish
    g.add_conditional_edges(
        "critic",
        should_retry,
        {"retry": "writer", "done": END}
    )
    return g.compile()