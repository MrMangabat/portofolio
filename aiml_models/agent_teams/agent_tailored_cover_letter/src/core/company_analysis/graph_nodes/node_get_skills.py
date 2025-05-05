# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/graph_nodes/node_get_skills.py

from typing import Dict, List
from src.infrastructure.correction_client import CorrectionsClient
from src.core.graph_master.master_graph_flow import CoverLetterGraphState
from langgraph.graph import StateGraph


def get_skills(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node to fetch user-defined skills from the CorrectionsClient.

    Args:
        state (Dict): Current LangGraph state.

    Returns:
        Dict: Updated state with 'skills' key.
    """
    print("------ Fetching skills from CorrectionsClient ------")

    corrections_client = CorrectionsClient()
    skills_response: List[str] = [item["text"] for item in corrections_client.fetch_corrections("skill")]

    return {**state, "skills": skills_response}