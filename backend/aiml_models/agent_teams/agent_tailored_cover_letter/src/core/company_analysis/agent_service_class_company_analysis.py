# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/agent_service_class_company_analysis.py

from typing import Dict, List
from src.infrastructure.correction_client import CorrectionsClient
from src.core.company_analysis.components.analysis_post_processing import PostProcessingNormalizer
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.core.cover_letter.components.analysis_rules_validator import AnalysisRulesValidator
from src.core.data_models.analysis_result_model import JobAnalysisResult
from src.infrastructure.llm_client import LLMClient

class AgentServiceClassCompanyAnalysis:
    """
    Purpose:
        Orchestrates the full flow of analyzing a job vacancy using the company analysis agent.

    Capabilities:
        - Fetch forbidden words, sentences, and skills from service_cover_letter.
        - Builds and sends a structured prompt to the LLM via LLMClient.
        - Parses the LLM response into structured data.
        - Builds a report on the job

    Reasoning:
        This centralizes all flow logic into a single point, maintaining separation between:
        - Infrastructure (API calls, LLM calls)
        - Core logic (prompt, parsing, validation)
    """

    def __init__(
        self,
        corrections_client: CorrectionsClient,
        prompt_builder: AnalysisPromptBuilder,
        response_parser: JobAnalysisResultParser,
        rules_validator: AnalysisRulesValidator,
        llm_client: LLMClient
    ) -> None:
        self.corrections_client = corrections_client
        self.prompt_builder = prompt_builder
        self.response_parser = response_parser
        self.rules_validator = rules_validator
        # self.post_processing_normalizer = 
        self.llmm_client = llm_client.get_model('gpt')
        self.correction_history: List[Dict] = []  # Tracks all corrections across iterations

    def analyze_job_vacancy(self, job_description: str, candidate_skills) -> JobAnalysisResult:
        """
        Handles the full pipeline of analyzing a job vacancy.

        Args:
            job_description (str): The text description of the job to analyze.

        Returns:
            JobAnalysisResult: The structured response from the AI.
        """
        # Fetch forbidden words, sentences, and skills
  
        skills_response = [item["text"] for item in self.corrections_client.fetch_corrections("skill")]

        messages = self.prompt_builder.build_prompt(skills_response, job_description, self.response_parser)


        # ✅ Invoke the LLM (pass the structured prompt directly)
        initial_analysis_chain = messages | self.llm_client | self.response_parser

        raw_response = initial_analysis_chain.invoke(
                {
                    "job_position": job_description,
                    "my_skills": candidate_skills,
                }
        )


        return raw_response

    def _log_feedback(self, feedback: Dict) -> None:    
        """
        Logs the validation feedback for debugging and self-correction tracking.

        Args:
            feedback (Dict): The validation feedback containing reflection and status.
        """
        print(f"\n❌ Iteration {feedback['iteration']} failed — Reflection for self-correction:\n{feedback['reflection']}\n")

