# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/agent_service_class_company_analysis.py


from typing import Dict, List
from src.infrastructure.correction_client import CorrectionsClient
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.core.company_analysis.components.analysis_rules_validator import AnalysisRulesValidator
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
        - Validates the result against forbidden content rules.
        - Supports iterative self-correction if validation fails.

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
        llm_client: LLMClient  # This MUST be present
        ) -> None:
        self.corrections_client = corrections_client
        self.prompt_builder = prompt_builder
        self.response_parser = response_parser
        self.rules_validator = rules_validator
        self.llm_client = llm_client
        self.correction_history: List[Dict] = []  # Tracks all corrections across iterations

    def analyze_job_vacancy(self, job_description: str) -> JobAnalysisResult:
        # Fetch forbidden words, sentences, and skills
        forbidden_words = [item["text"] for item in self.corrections_client.fetch_corrections("word")]
        forbidden_sentences = [item["text"] for item in self.corrections_client.fetch_corrections("sentence")]
        skillsets = [item["text"] for item in self.corrections_client.fetch_corrections("skill")]

        # Main generation loop with up to 12 self-correction attempts
        for iteration in range(1, 13):
            prompt = self.prompt_builder.build_prompt(skillsets, job_description)
            formatted_prompt = prompt.format_messages(job_position=job_description, my_skills=skillsets)

            # 🔥 Invoke the real LLM via Ollama
            raw_response = self.llm_client.invoke(formatted_prompt)

            # Parse response
            parsed_response = self.response_parser.parse(raw_response)

            # Validate response
            feedback = self.rules_validator.validate(parsed_response, forbidden_words, forbidden_sentences, iteration)

            if feedback["status"] == "passed":
                print(f"✅ Analysis passed after {iteration} iterations.")
                return parsed_response

            # Store feedback for future self-correction
            self.correction_history.append(feedback)

            # Prepare for next round with feedback (could modify prompt, but for now we log and retry as-is)
            self._log_feedback(feedback)

        raise ValueError("🚨 Analysis failed after 12 correction attempts.")

    def _log_feedback(self, feedback: Dict) -> None:
        print(f"\n❌ Iteration {feedback['iteration']} failed — Reflection for self-correction:\n{feedback['reflection']}\n")


