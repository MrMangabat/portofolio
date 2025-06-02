# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/graph_master/initialize_graph.py

from typing import TypedDict, List, Annotated, Dict, Any, Optional
from langgraph.graph.message import add_messages, AnyMessage


class CoverLetterGraphState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    job_description: str
    skills: list[str]  # Raw user skills
    analysis_output: Optional[Dict[str, Any]]  # From company_analysis
    matching_skills: Optional[Dict[str, bool]]  # From company_analysis
    cover_letter_output: Optional[Dict[str, Any]]  # Final output from cover letter agent
    generation: str

    words_to_avoid: List[str]
    sentences_to_avoid: List[str]

    best_match_template_cover_letter: Optional[str]  # Result from semantic similarity node
    cv: str  # Will be overwritten with real value later, initialized manually

    agent_trace: Optional[List[str]] = None  # Tracks which nodes/agents touched the state
    editorial_violations: Optional[List[str]] = None  # Tracks active rule violations
    generation_violation_log: Optional[List[Dict[str, Any]]] = None  # Time-series log of prior generations

    iterations: int
