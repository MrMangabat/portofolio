# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/graph_nodes/node_generate_vacancy_analysis.py

import json
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
    analysis_output = result['analysis_output']

    # Step 2: Prepare new trace entry (auto-accumulated via Annotated[List[str], add])
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    new_trace = f"NODE: company_analysis @ {timestamp}"

    # Step 3: Print state tree
    logger.info("Iteration: %s", state['iterations'])
    logger.info("Job Title: %s", analysis_output.job_title)
    logger.info("Skills Match: %s", analysis_output.matching_skills)
    logger.info("Adding trace: %s", new_trace)
    logger.info("Analysis Summary: %s", analysis_output.analysis_output)
    logger.info("Finished job vacancy analysis node")

    logger.info("Analysis output (formatted):\n%s", json.dumps(analysis_output.model_dump(), indent=2))

    # Return only new values (LangGraph auto-merges)
    return {
        "analysis_output": analysis_output,
        "matching_skills": analysis_output.matching_skills,
        "agent_trace": [new_trace],
    }
