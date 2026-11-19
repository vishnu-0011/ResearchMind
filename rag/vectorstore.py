# rag/vectorstore.py
import chromadb
from chromadb.config import Settings


# single in-memory client shared across the app
_client = chromadb.Client(Settings(anonymized_telemetry=False))


def get_or_create_collection(name: str = "researchmind"):
    """Returns existing collection or creates a new one."""
    return _client.get_or_create_collection(name=name)


def add_chunks(chunks: list[str], embeddings: list[list[float]], 
               sources: list[str], collection_name: str = "researchmind"):
    """
    Stores text chunks and their embeddings in ChromaDB.
    Each chunk is linked to its source URL for citation tracking.
    """
    collection = get_or_create_collection(collection_name)

    # ChromaDB needs unique string IDs for each chunk
    ids = [f"chunk_{i}_{hash(chunk) % 100000}" for i, chunk in enumerate(chunks)]

    collection.add(
        ids        = ids,
        embeddings = embeddings,
        documents  = chunks,
        metadatas  = [{"source": src} for src in sources]
    )

    print(f"   Stored {len(chunks)} chunks in ChromaDB")


def query_chunks(query_embedding: list[float], n_results: int = 5,
                 collection_name: str = "researchmind") -> list[dict]:
    """
    Finds the most relevant chunks for a given query embedding.
    Returns list of {text, source} dicts.
    """
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_embeddings = [query_embedding],
        n_results        = min(n_results, collection.count())
    )

    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "text":   doc,
            "source": results["metadatas"][0][i].get("source", "")
        })

    return chunks


def clear_collection(collection_name: str = "researchmind"):
    """Clears the collection between research sessions."""
    try:
        _client.delete_collection(collection_name)
    except Exception:
        pass