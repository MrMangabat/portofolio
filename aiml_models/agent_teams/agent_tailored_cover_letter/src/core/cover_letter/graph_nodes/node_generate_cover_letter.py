# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_generate_cover_letter.py

from src.core.graph_master.master_graph_flow import CoverLetterGraphState
from langgraph.graph import StateGraph
from src.core.cover_letter.agent_service_class_cover_letter import AgentServiceClassCoverLetter
from src.infrastructure.correction_client import CorrectionsClient
from src.core.cover_letter.components.cover_letter_prompt_builder import CoverLetterPromptBuilder
from src.core.cover_letter.components.cover_letter_parser import CoverLetterResultParser
from src.infrastructure.llm_client import LLMClient


def generate_cover_letter(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node for generating a personalized cover letter.

    Args:
        state (Dict): Current LangGraph state, including job analysis, skills, CV, and user rules.

    Returns:
        Dict: Updated state with generated cover letter content under key 'cover_letter_output'.
    """
    print("------ Generating Cover Letter ------")

    agent = AgentServiceClassCoverLetter(
        corrections_client=CorrectionsClient(),
        prompt_builder=CoverLetterPromptBuilder(),
        response_parser=CoverLetterResultParser(),
        llm_client=LLMClient()
    )

    return agent.generate_cover_letter(state)
