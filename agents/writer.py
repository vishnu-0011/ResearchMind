# agents/writer.py
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from graph.state import ResearchState
from config.prompts import WRITER_PROMPT
from tools.retriever import retrieve


def writer_node(state: ResearchState) -> dict:
    """
    Writer agent — retrieves relevant chunks from ChromaDB
    and writes a full markdown research report using Groq LLM.
    """
    topic    = state["topic"]
    sources  = state["sources"]
    retries  = state.get("retries", 0)
    feedback = state.get("feedback", "")

    print(f"\n✍️  Writer drafting report (attempt {retries + 1})...")

    # Step 1 — RAG retrieval instead of raw findings
    print(f"   Retrieving relevant chunks from vector store...")
    retrieved = retrieve(query=topic, n_results=6)

    if not retrieved:
        # fallback to raw findings if retrieval fails
        print("   ⚠️ RAG retrieval empty — falling back to raw findings")
        retrieved = [
            {"text": f["content"], "source": f["url"]}
            for f in state["findings"]
        ]

    # Step 2 — format retrieved chunks for the prompt
    context_text = ""
    for i, chunk in enumerate(retrieved):
        context_text += f"""
[{i+1}] Source: {chunk['source']}
Content: {chunk['text']}
"""

    # Step 3 — add retry feedback if this is a revision
    retry_note = ""
    if retries > 0 and feedback:
        retry_note = f"""
IMPORTANT — This is revision #{retries}.
Critic feedback from last draft:
{feedback}
Address every point above in this new version.
"""

    # Step 4 — build prompt and call Groq
    prompt = WRITER_PROMPT.format(
        topic    = topic,
        findings = context_text
    ) + retry_note

    llm = ChatGroq(
        model       = "llama-3.3-70b-versatile",
        temperature = 0.3,
        api_key     = os.environ["GROQ_API_KEY"]
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    draft    = response.content

    print(f"✅ Writer done — {len(draft)} characters written")

    return {
        "draft":   draft,
        "retries": retries + 1
    }