# graph/builder.py
from langgraph.graph import StateGraph, END
from graph.state import ResearchState
from graph.router import should_retry


def build_graph():
    """
    Assembles the full ResearchMind agent pipeline.
    Nodes are imported here — stubs for now, replaced week by week.
    """
    # import agent nodes
    from agents.researcher import researcher_node
    from agents.writer     import writer_node
    from agents.critic     import critic_node

    g = StateGraph(ResearchState)

    # Register nodes 
    g.add_node("researcher", researcher_node)
    g.add_node("writer",     writer_node)
    g.add_node("critic",     critic_node)

    # Define edges 
    g.set_entry_point("researcher")
    g.add_edge("researcher", "writer")
    g.add_edge("writer",     "critic")

    # Conditional edge (the feedback loop) 
    g.add_conditional_edges(
        "critic",
        should_retry,
        {
            "retry": "writer",
            "done":  END
        }
    )

    return g.compile()