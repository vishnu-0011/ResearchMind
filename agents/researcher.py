# agents/researcher.py
from graph.state import ResearchState
from tools.search import search_web
from tools.fetcher import clean_content


def researcher_node(state: ResearchState) -> dict:
    """
    Researcher agent — searches the web for the topic
    and returns structured findings with sources.
    """
    topic = state["topic"]
    print(f"\n=>Researcher searching for: {topic}")

    # Step 1 — search the web
    raw_results = search_web(query=topic, max_results=5)
    print(f"   Found {len(raw_results)} results")

    # Step 2 — clean and structure findings
    findings = []
    sources  = []

    for i, item in enumerate(raw_results):
        cleaned = clean_content(item["content"])

        if not cleaned:
            continue  # skip empty results

        findings.append({
            "title":   item["title"],
            "content": cleaned,
            "url":     item["url"]
        })
        sources.append(item["url"])

        print(f"   [{i+1}] {item['title'][:60]}...")

    print(f"=> Researcher done — {len(findings)} findings collected")

    return {
        "findings": findings,
        "sources":  sources
    }