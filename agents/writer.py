import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from graph.state import ResearchState
from config.prompts import WRITER_PROMPT


def writer_node(state: ResearchState) -> dict:
    """
    Writer agent — takes findings from Researcher
    and writes a full markdown research report using Groq LLM.
    """
    topic    = state["topic"]
    findings = state["findings"]
    retries  = state.get("retries", 0)
    feedback = state.get("feedback", "")

    print(f"\n=>  Writer drafting report (attempt {retries + 1})...")

    # format findings into readable text for the prompt
    findings_text = ""
    for i, f in enumerate(findings):
        findings_text += f"""
        [{i+1}] Title: {f['title']}
            URL: {f['url']}
            Content: {f['content']}
        """

    # if this is a retry, add critic feedback to the prompt
    retry_note = ""
    if retries > 0 and feedback:
        retry_note = f"""
IMPORTANT: This is revision #{retries}. The critic gave this feedback on your last draft:
{feedback}
Please address all the points mentioned above in this new version.
"""

    # build the full prompt
    prompt = WRITER_PROMPT.format(
        topic    = topic,
        findings = findings_text
    ) + retry_note

    # call Groq LLM
    llm      = ChatGroq(
        model = "llama-3.3-70b-versatile",
        temperature = 0.3,         #low temp = more factual, less creative
        api_key     = os.environ["GROQ_API_KEY"]
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    draft    = response.content

    print(f"✅ Writer done — {len(draft)} characters written")

    return {
        "draft":   draft,
        "retries": retries + 1
    }