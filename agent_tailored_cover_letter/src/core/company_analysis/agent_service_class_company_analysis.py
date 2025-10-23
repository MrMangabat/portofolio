# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/agent_service_class_company_analysis.py
from typing import Dict
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.infrastructure.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)

class AgentServiceClassCompanyAnalysis:
    def __init__(
        self,
        prompt_builder: AnalysisPromptBuilder,
        response_parser: JobAnalysisResultParser,
        llm_client: LLMClient
    ) -> None:
        self.prompt_builder = prompt_builder
        self.response_parser = response_parser
        self.llm_client = llm_client

    def analyze_job_vacancy(self, state: Dict) -> Dict:
        job_description: str = state["job_description"]
        skills_response: list[str] = state["skills"]
        candidate_inputs: str = state.get("unique_user_input", "")

        logger.info("=" * 80)
        logger.info("Starting job vacancy analysis")

        # Create LCEL chain: prompt | llm | parser
        chain = self.prompt_builder.build_prompt() | self.llm_client.get_model("ollama") | self.response_parser.parser


        # Invoke the chain
        result = chain.invoke({
            "job_position": job_description,
            "my_skills": ", ".join(skills_response),
            "candidate_inputs": candidate_inputs
        })

        logger.info("PARSED RESULT:")
        logger.info(f"Company: {result.company_name}")
        logger.info(f"Job Title: {result.job_title}")
        logger.info(f"Language: {result.language_detected}")
        logger.info("=" * 80)

        return {**state, "analysis_output": result}
