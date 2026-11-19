# tools/ingestor.py
from rag.chunker    import chunk_text
from rag.embedder   import get_embeddings
from rag.vectorstore import add_chunks, clear_collection


def ingest_findings(findings: list[dict], collection_name: str = "researchmind"):
    """
    Takes raw findings from the Researcher agent and:
    1. Chunks each finding into smaller pieces
    2. Embeds each chunk using HF Inference API
    3. Stores chunks + embeddings in ChromaDB
    """
    print(f"\n📥 Ingesting {len(findings)} findings into vector store...")

    # clear previous session data
    clear_collection(collection_name)

    all_chunks   = []
    all_sources  = []

    for finding in findings:
        text   = finding.get("content", "")
        source = finding.get("url", "")

        if not text:
            continue

        # chunk the content
        chunks = chunk_text(text)
        all_chunks.extend(chunks)
        all_sources.extend([source] * len(chunks))

        print(f"   → {len(chunks)} chunks from: {finding['title'][:50]}...")

    if not all_chunks:
        print("   ⚠️ No chunks created — findings may be empty")
        return

    # embed all chunks
    print(f"   Embedding {len(all_chunks)} chunks via HF Inference API...")
    embeddings = get_embeddings(all_chunks)

    # store in ChromaDB
    add_chunks(all_chunks, embeddings, all_sources, collection_name)
    print(f"✅ Ingestion complete — {len(all_chunks)} chunks ready for retrieval")