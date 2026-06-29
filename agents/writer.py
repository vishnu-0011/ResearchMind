from graph.state import ResearchState


def writer_node(state: ResearchState) -> dict:
    print(f"✍️  Writer drafting report — retry #{state.get('retries', 0)}")
    # TODO Week 2: add RAG retrieval + Groq LLM draft
    return {
        "draft":   f"# Report on {state['topic']}\n\nStub draft.",
        "retries": state.get("retries", 0) + 1
    }