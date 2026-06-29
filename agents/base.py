from graph.state import ResearchState


def make_empty_state(topic: str) -> ResearchState:
    """Returns a clean starting state for a given topic."""
    return ResearchState(
        topic        = topic,
        findings     = [],
        sources      = [],
        draft        = "",
        score        = 0,
        feedback     = "",
        retries      = 0,
        final_report = ""
    )