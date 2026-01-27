"""Routing functions and configuration for CV Resume Builder workflow."""

from .state import State

# Three officers (sub-supervisors) reporting to main supervisor
OFFICERS = {
    "research_analysis_officer": {
        "sub_agents": [
            "financial_analyst",
            "business_intelligence_analyst",
            "company_profile_analyst",
            "macro_officer",
        ],
        "description": "Manages M&A-level due diligence: financial, business, people, and macro analysis",
    },
    "personality_analysis_officer": {
        "workers": ["analyze_profile"],
        "description": "Manages candidate profile and personality analysis",
    },
    "document_generation_officer": {
        "workers": ["generate_docs", "reflect", "user_review"],
        "description": "Manages document creation, refinement, and review",
    },
}


def route_main_supervisor(state: State) -> str:
    """Route from main supervisor to officers or END."""
    return state["next"]


def route_officer(state: State) -> str:
    """Route from officer to worker or back to main supervisor."""
    return state["next"]
