"""Document Generation Officer node (Tier 2)."""

import logging

from langchain_core.messages import HumanMessage
from langsmith import traceable

from ...state import State

logger = logging.getLogger(__name__)


@traceable(run_type="chain", name="Document Generation Officer")
def document_generation_officer(state: State) -> State:
    """Document Generation Officer: Manages document creation and refinement.

    Workflow: generate_docs -> user_review (PDF generation) -> report_to_supervisor
    """
    logger.info("[OFFICER] Document Generation Officer receiving task...")

    documents = state.get("documents", {})
    feedback = state.get("feedback", {})

    # Route through document generation workflow
    if not documents:
        # Step 1: Generate the cover letter content
        next_worker = "generate_docs"
    elif feedback.get("status") == "completed":
        # Step 3: PDF generated successfully, report back to supervisor
        next_worker = "report_to_supervisor"
    elif documents.get("cover_letter"):
        # Step 2: Cover letter generated, finalize and create PDF
        next_worker = "user_review"
    else:
        # Fallback
        next_worker = "generate_docs"

    logger.info("Routing to: %s", next_worker)

    return {
        "next": next_worker,
        "current_officer": "document_generation_officer",
        "messages": [
            HumanMessage(content=f"Document Officer routing to: {next_worker}")
        ],
    }
