from graph.state import ResearchState

MAX_RETRIES = 2
PASS_SCORE  = 7


def should_retry(state: ResearchState) -> str:
    """
    Conditional edge function — called after Critic node.
    Returns 'retry' to send back to Writer, or 'done' to end.
    """
    score   = state.get("score", 0)
    retries = state.get("retries", 0)

    if score >= PASS_SCORE:
        print(f"✅ Critic passed the report with score {score}/10")
        return "done"

    if retries >= MAX_RETRIES:
        print(f"⚠️ Max retries reached ({retries}). Accepting report with score {score}/10")
        return "done"

    print(f"🔁 Critic score {score}/10 — sending back to Writer (retry {retries + 1}/{MAX_RETRIES})")
    return "retry"