from graph.state import ResearchState

MAX_RETRIES = 2

def should_retry(state: ResearchState) -> str:
    if state["score"] >= 7 or state["retries"] >= MAX_RETRIES:
        return "done"
    return "retry"