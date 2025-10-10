# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/graph_master/initialize_graph.py

from typing import TypedDict, List, Annotated, Dict, Any, Optional
from langgraph.graph.message import add_messages, AnyMessage
from operator import add


def add_to_dict(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reducer function for merging dictionaries in LangGraph state.
    Merges new keys into existing dict without overwriting.
    """
    return {**existing, **new}


class CoverLetterGraphState(TypedDict):
    # Core flow inputs
    messages: Annotated[List[AnyMessage], add_messages]  # Auto-accumulates messages
    job_description: str
    unique_user_input: str  # User-specific notes/instructions for cover letter generation
    skills: list[str]  # Raw user skills
    cv: str  # User's CV content

    # Company analysis outputs
    analysis_output: Optional[Dict[str, Any]]  # From company_analysis node
    matching_skills: Optional[Dict[str, bool]]  # Skills matched between job and candidate
    language_detected: str  # Detected language of job description

    # Cover letter generation
    cover_letter_output: Optional[Dict[str, Any]]  # Final output from cover letter agent
    generation: str  # Current generation text

    # Semantic search & constraints
    best_match_template_cover_letter: Optional[str]  # Result from semantic similarity node
    words_to_avoid: List[str]  # Banned words from corrections API
    sentences_to_avoid: List[str]  # Banned sentences from corrections API

    # Tracing & history (auto-accumulating)
    agent_trace: Annotated[List[str], add]  # Tracks which nodes/agents touched the state
    cover_letter_revision_history: Annotated[List[Dict[str, Any]], add]  # Tracks all cover letter revisions

    # Editorial validation (auto-accumulating)
    editorial_violations: Annotated[List[str], add]  # Tracks active rule violations per iteration
    generation_violation_log: Annotated[Dict[str, Any], add_to_dict]  # Time-series log of prior generations (keyed by iteration)

    # Iteration control
    iterations: int  # Current iteration count
    max_iterations: int  # Maximum allowed iterations
