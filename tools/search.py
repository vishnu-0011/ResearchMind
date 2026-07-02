import os
from tavily import TavilyClient


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches the web using Tavily and returns a list of results.
    Each result is a dict with title, content, and url.
    """
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    response = client.search(
        query=query,
        search_depth="advanced",#deeper search, better results
        max_results=max_results,
        include_raw_content=True#gets full page content not just snippet
    )
    results = []
    for item in response.get("results", []):
        results.append({
            "title":   item.get("title", ""),
            "content": item.get("content", "") or item.get("raw_content", ""),
            "url":     item.get("url", "")
        })

    return results