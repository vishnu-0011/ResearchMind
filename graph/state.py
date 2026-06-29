from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    topic: str                          # user input
    findings: list[dict]                # [{title, content, url}]
    sources: list[str]                  # URLs collected
    draft: str                          # Writer's output
    feedback: str                       # Critic's notes on failure
    score: int                          # Critic's 1-10 score
    retries: int                        # tracks feedback loop count
    final_report: str                   # approved output