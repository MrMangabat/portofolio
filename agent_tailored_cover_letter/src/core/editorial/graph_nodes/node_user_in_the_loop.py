# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_human_in_the_loop.py

from datetime import datetime
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from langgraph.graph import StateGraph
import logging

logger = logging.getLogger(__name__)

def user_in_the_loop(state: CoverLetterGraphState) -> StateGraph:
    """
    Placeholder node to simulate a human review step in the pipeline.

    Args:
        state (CoverLetterGraphState): The full graph state.

    Returns:
        CoverLetterGraphState: Partial state with new trace and message.
    """
    timestamp: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Prepare new trace entry (auto-accumulated via Annotated[List[str], add])
    new_trace = f"human_in_the_loop @ {timestamp}"

    # Prepare new message
    new_message = ("system", f"[human_in_the_loop] Review passed at {timestamp}.")

    logger.info("HUMAN REVIEW PLACEHOLDER PASSED, Adding trace: %s", new_trace)

    # Return only new values (LangGraph auto-merges)
    return {
        "agent_trace": [new_trace],
        "messages": [new_message],
    }
