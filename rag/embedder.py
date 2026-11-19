# rag/embedder.py
from sentence_transformers import SentenceTransformer

# loaded once, reused for every call — no API needed
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Converts text strings into vector embeddings.
    Runs locally using sentence-transformers — completely free,
    no API calls, no rate limits, no credits needed.
    """
    vectors = _model.encode(texts, show_progress_bar=False)
    return vectors.tolist()