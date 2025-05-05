
from typing import TypedDict, List, Annotated, Dict, Any, Optional
from langgraph.graph.message import add_messages, AnyMessage



class CoverLetterGraphState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    iterations: int
    editorial_violations: Optional[List[str]]  # Explicit list of rule-based violations (strings)
    job_description: str
    skills: list[str]  # Raw user skills
    best_match_template_cover_letter: Optional[str]  # Result from semantic similarity node
    analysis_output: Optional[Dict[str, Any]]  # From company_analysis
    matching_skills: Optional[Dict[str, bool]]  # From company_analysis
    cover_letter_output: Optional[Dict[str, Any]]  # Final output from cover letter agent
    generation: str
    words_to_avoid: List[str]
    sentences_to_avoid: List[str]
    editorial_error_messages: Optional[List[str]]  # Only validation errors (not chat context)
    cv: str = "empty placeholder" # Mocked or extracted CV content
    agent_trace: Optional[List[str]]  # Optional trace of agent hops like ["company_analysis", "cover_letter_gen"]
