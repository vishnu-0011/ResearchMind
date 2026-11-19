# tools/retriever.py
from rag.embedder    import get_embeddings
from rag.vectorstore import query_chunks


def retrieve(query: str, n_results: int = 5) -> list[dict]:
    """
    Embeds the query and returns the most semantically
    similar chunks from ChromaDB as {text, source} dicts.
    """
    query_embedding = get_embeddings([query])[0]
    return query_chunks(query_embedding, n_results=n_results)


def retrieve_multi(queries: list[str], n_per_query: int = 4) -> list[dict]:
    """Retrieve for several angles, deduplicate, and merge."""
    seen, merged = set(), []
    for q in queries:
        for chunk in retrieve(q, n_results=n_per_query):
            if chunk["text"] not in seen:
                seen.add(chunk["text"])
                merged.append(chunk)
    return merged