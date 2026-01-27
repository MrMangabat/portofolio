"""Main Supervisor node (Tier 1) for CV Resume Builder workflow."""

import logging

from langchain_core.messages import HumanMessage
from langsmith import traceable

from ..state import State

logger = logging.getLogger(__name__)

# Main supervisor system prompt
MAIN_SUPERVISOR_PROMPT = (
    "You are the Main Supervisor (Captain/Commander) managing a CV/Resume generation workflow. "
    "Your officers are: research_analysis_officer, personality_analysis_officer, document_generation_officer. "
    "Delegate tasks to the appropriate officer based on the current state. "
    "When all work is complete, respond with FINISH."
)


@traceable(run_type="chain", name="Main Supervisor")
def main_supervisor(state: State) -> State:
    """Main Supervisor (Captain/Commander): Delegates to officers.

    Workflow: personality_analysis_officer -> document_generation_officer -> FINISH
    """
    logger.info("[MAIN SUPERVISOR] Captain making delegation decision...")

    profile_data = state.get("profile_data", {})
    feedback = state.get("feedback", {})

    # High-level routing logic
    # NOTE: Skipping research_analysis_officer for now (focus on doc generation)
    if not profile_data or "analysis" not in profile_data:
        # Step 1: Analyze the candidate profile
        next_node = "personality_analysis_officer"
    elif feedback.get("status") == "completed":
        # Step 3: PDF generated, workflow complete
        pdf_path = feedback.get("pdf_path", "unknown")
        logger.info("Workflow complete! PDF: %s", pdf_path)
        next_node = "FINISH"
    else:
        # Step 2 and beyond: Generate/finalize documents
        next_node = "document_generation_officer"

    logger.info("Delegating to: %s", next_node)

    return {
        "next": next_node,
        "messages": [
            HumanMessage(content=f"Main Supervisor delegating to: {next_node}")
        ],
    }
