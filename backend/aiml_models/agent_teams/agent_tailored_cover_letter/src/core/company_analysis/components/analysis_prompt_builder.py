# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py


from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from typing import List

from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.analysis_result_model import JobAnalysisResult

class AnalysisPromptBuilder:
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)  # pydantic_schema instead of pydantic_object


    def build_prompt(self, skillsets: List[str], job_to_apply: str) -> ChatPromptTemplate:
        system_analysis_template_str = """
        You are a senior HR analyst working on a career advisory platform.
        Your job is to analyze the following job vacancy and extract structured insights.

        Respond with a JSON object under the key 'job_analysis_result'.
        """

        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_analysis_template_str,
                input_variables=[],
            )
        )

        human_analysis_template_str = """
        Job Vacancy Description:
        {job_position}
        Candidate's Skills:
        {my_skills}
        """

        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_analysis_template_str,
                input_variables=["job_position", "my_skills"],
            )
        )

        return ChatPromptTemplate(messages=[system_prompt, human_prompt])
