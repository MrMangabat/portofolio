"""Personality Analysis Officer node (Tier 2)."""

import logging

from langchain_core.messages import HumanMessage
from langsmith import traceable

from ...state import State

logger = logging.getLogger(__name__)


@traceable(run_type="chain", name="Personality Analysis Officer")
def personality_analysis_officer(state: State) -> dict[str, object]:
    """Personality Analysis Officer: Manages candidate profile analysis.

    Routes to analyze_profile, then reports back to main_supervisor.
    """
    logger.info("[OFFICER] Personality Analysis Officer receiving task...")

    profile_data: dict[str, object] = state.get("profile_data", {})

    # Check if analysis has been done (analyze_profile adds "analysis" key)
    if "analysis" not in profile_data:
        next_worker = "analyze_profile"
    else:
        next_worker = "report_to_supervisor"

    return {
        "next": next_worker,
        "current_officer": "personality_analysis_officer",
        "messages": [
            HumanMessage(content=f"Personality Officer routing to: {next_worker}")
        ],
    }
