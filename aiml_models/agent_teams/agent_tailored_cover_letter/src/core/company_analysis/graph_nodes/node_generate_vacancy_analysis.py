# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/graph_nodes/node_generate_vacancy_analysis.py

from datetime import datetime
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from langgraph.graph import StateGraph
from src.core.company_analysis.agent_service_class_company_analysis import AgentServiceClassCompanyAnalysis
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.infrastructure.llm_client import LLMClient
import logging


logger = logging.getLogger(__name__)


def generate_vacancy_analysis(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node for generating structured job vacancy analysis.

    Args:
        state (CoverLetterGraphState): Graph state containing job_description (and possibly other context)

    Returns:
        CoverLetterGraphState: Updated state with 'analysis_output' key
    """
    logger.info("COMPANY ANALYSIS NODE: Starting job vacancy analysis")

    # Step 1: Build agent and run analysis
    agent = AgentServiceClassCompanyAnalysis(
        prompt_builder=AnalysisPromptBuilder(),
        response_parser=JobAnalysisResultParser(),
        llm_client=LLMClient()
    )
    result = agent.analyze_job_vacancy(state)

    # Step 2: Construct message log update
    updated_messages = state["messages"] + [
        ("system", f"[company_analysis] Completed analysis: {result.analysis_output}"),
        ("system", f"[company_analysis] Extracted job title: {result.job_title}"),
    ]

    # Step 3: Append to agent_trace
    trace = state.get("agent_trace", [])
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    trace.append(f"NODE: company_analysis @ {timestamp}")

    # Step 4: Print state tree
    logger.info("Iteration: %s", state['iterations'])
    logger.info("Job Title: %s", result.job_title)
    logger.info("Skills Match: %s", result.matching_skills)
    logger.info("Agent Trace: %s", trace)
    logger.info("Analysis Summary: %s", result.analysis_output)
    logger.info("Finished job vacancy analysis node")

    return {
        **state,
        "analysis_output": result,
        "matching_skills": result.matching_skills,
        "messages": updated_messages,
        "agent_trace": trace,
    }
