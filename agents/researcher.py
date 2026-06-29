from graph.state import ResearchState


def researcher_node(state: ResearchState) -> dict:
    print(f"🔍 Researcher starting on topic: {state['topic']}")
    # TODO Week 1: add Tavily search + LlamaIndex chunking
    return {
        "findings": [{"title": "stub", "content": "stub content", "url": "http://example.com"}],
        "sources":  ["http://example.com"]
    }