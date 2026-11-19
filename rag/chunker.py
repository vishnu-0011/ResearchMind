# rag/chunker.py
from llama_index.core.node_parser import SentenceSplitter


def chunk_text(text: str, chunk_size: int = 256, chunk_overlap: int = 30) -> list[str]:
    """chunk_size and chunk_overlap are measured in TOKENS (~4 characters each)."""
    """
    Splits a long text into smaller overlapping chunks.
    chunk_size: max characters per chunk
    chunk_overlap: how many characters overlap between chunks
    — overlap ensures context isn't lost at chunk boundaries
    """
    splitter = SentenceSplitter(
        chunk_size    = chunk_size,
        chunk_overlap = chunk_overlap
    )

    chunks = splitter.split_text(text)
    return [c.strip() for c in chunks if c.strip()]