import os
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from graph.state import ResearchState
from config.prompts import CRITIC_PROMPT


def parse_critic_response(response_text: str) -> tuple[int, str]:
    """
    Parses the Critic LLM response to extract score and feedback.
    Expected format:
    SCORE: 7
    FEEDBACK: The report is well structured but...
    """
    score    = 0
    feedback = ""

    # extract score
    score_match = re.search(r'SCORE:\s*(\d+)', response_text)
    if score_match:
        score = int(score_match.group(1))
        # clamp between 1 and 10 just in case LLM goes out of range
        score = max(1, min(10, score))

    # extract feedback
    feedback_match = re.search(r'FEEDBACK:\s*(.*)', response_text, re.DOTALL)
    if feedback_match:
        feedback = feedback_match.group(1).strip()

    return score, feedback


def critic_node(state: ResearchState) -> dict:
    """
    Critic agent — reads the Writer's draft and scores it
    on accuracy, citations, structure, depth and clarity.
    Sends feedback back to Writer if score is below threshold.
    """
    topic = state["topic"]
    draft = state["draft"]

    print(f"\n=> Critic reviewing draft...")

    # build the prompt
    prompt = CRITIC_PROMPT.format(
        topic = topic,
        draft = draft
    )

    # call Groq LLM
    llm = ChatGroq(
        model       = "llama-3.3-70b-versatile",
        temperature = 0.1,    # very low temp — we want consistent scoring
        api_key     = os.environ["GROQ_API_KEY"]
    )
    response      = llm.invoke([HumanMessage(content=prompt)])
    response_text = response.content

    print(f"   Raw critic response:\n{response_text}\n")

    # parse score and feedback
    score, feedback = parse_critic_response(response_text)

    print(f"   Score: {score}/10")
    print(f"   Feedback: {feedback[:100]}...")

    # set final report if passing
    final_report = draft if score >= 7 else ""

    return {
        "score":        score,
        "feedback":     feedback,
        "final_report": final_report
    }