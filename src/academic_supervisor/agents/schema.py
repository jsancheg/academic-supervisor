from typing import Literal, TypedDict

AgentSource = Literal["grammar", "clarity", "coherence"]


class ReviewIssue(TypedDict):
    problem: str
    location: str
    why: str
    suggested_fix: str
    source: AgentSource
    paragraph_index: int
