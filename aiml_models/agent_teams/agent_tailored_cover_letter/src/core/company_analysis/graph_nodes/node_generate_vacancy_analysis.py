# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/graph_nodes/node_generate_vacancy_analysis.py

from src.core.graph_master.master_graph_flow import CoverLetterGraphState
from langgraph.graph import StateGraph
from src.core.company_analysis.agent_service_class_company_analysis import AgentServiceClassCompanyAnalysis
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.infrastructure.llm_client import LLMClient


def generate_vacancy_analysis(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node for generating structured job vacancy analysis.

    Args:
        state (Dict): Graph state containing job_description (and possibly other context)

    Returns:
        Dict: Updated state with 'analysis_output' key
    """
    print("------ Analyzing job vacancy ------")

    agent = AgentServiceClassCompanyAnalysis(
        prompt_builder=AnalysisPromptBuilder(),
        response_parser=JobAnalysisResultParser(),
        llm_client=LLMClient()
    )

    return agent.analyze_job_vacancy(state)
