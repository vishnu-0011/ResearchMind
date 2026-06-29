"""from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    topic: str                          # user input
    findings: list[dict]                # [{title, content, url}]
    sources: list[str]                  # URLs collected
    draft: str                          # Writer's output
    feedback: str                       # Critic's notes on failure
    score: int                          # Critic's 1-10 score
    retries: int                        # tracks feedback loop count
    final_report: str                   # approved output"""

from typing import TypedDict, List, Optional


class ResearchState(TypedDict):
    """
    Shared state object passed between all agents in the graph.
    Every agent reads from this and writes back to it.
    """
    topic: str                          # the research topic the user entered
    findings: List[dict]                # list of {title, content, url}
    sources: List[str]                  # list of source URLs collected
    draft: str                          # the full draft report in markdown
    score: int                          # quality score 1-10
    feedback: str                       # critic's notes if score < 7
    retries: int                        # how many times writer has been retried
    final_report: str                   # approved report shown to user