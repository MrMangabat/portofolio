# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/agent_service_class_company_analysis.py
from typing import Dict
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.infrastructure.llm_client import LLMClient

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

        prompt_chain = (
            self.prompt_builder.build_prompt()
            | self.llm_client.get_model("gpt")
            | self.response_parser.parser
        )

        result = prompt_chain.invoke({
            "job_position": job_description,
            "my_skills": ", ".join(skills_response)
        })

        return {**state, "analysis_output": result}
