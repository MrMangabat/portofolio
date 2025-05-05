# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/graph_nodes/node_generate_vacancy_analysis.py

from src.core.graph_master.master_graph_flow import CoverLetterGraphState
from src.core.company_analysis.agent_service_class_company_analysis import AgentServiceClassCompanyAnalysis
from src.infrastructure.correction_client import CorrectionsClient
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.infrastructure.llm_client import LLMClient


def grammatical_rules_classifier(state: CoverLetterGraphState) -> GraphState:
    pass
    
    return grammatical_rules_classifier(state)
