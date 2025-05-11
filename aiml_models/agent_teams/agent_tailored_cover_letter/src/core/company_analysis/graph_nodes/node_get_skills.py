# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/graph_nodes/node_get_skills.py

from typing import List, Dict
from datetime import datetime
from src.infrastructure.correction_client import CorrectionsClient
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from langgraph.graph import StateGraph
import logging

logger = logging.getLogger(__name__)


def get_skills(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node to fetch user-defined skills from the CorrectionsClient.

    Args:
        state (CoverLetterGraphState): Current LangGraph state.

    Returns:
        CoverLetterGraphState: Updated state with 'skills' key.
    """
    logger.info("Fetching skills from CorrectionsClient")

    corrections_client = CorrectionsClient()
    skills_response: List[str] = [item["text"] for item in corrections_client.fetch_corrections("skill")]

    # Build timestamp for traceability
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Prepare updated trace
    agent_trace = state.get("agent_trace", [])
    agent_trace.append(f"NODE: get_skills @ {timestamp}")

    # Print state trace

    logger.info("Iteration: %s", state["iterations"])
    logger.info("Skills fetched: %s", skills_response)
    logger.info("Agent trace: %s", agent_trace)
    logger.info("Finished get_skills node")

    # Return updated state
    return {
        **state,
        "skills": skills_response,
        "agent_trace": agent_trace
    }
