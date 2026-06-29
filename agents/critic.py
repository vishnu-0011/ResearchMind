from graph.state import ResearchState


def critic_node(state: ResearchState) -> dict:
    print(f"🧐 Critic reviewing draft...")
    # TODO Week 3: add Groq LLM scoring
    return {
        "score":         8,          # hardcoded pass for now
        "feedback":      "",
        "final_report":  state["draft"]
    }