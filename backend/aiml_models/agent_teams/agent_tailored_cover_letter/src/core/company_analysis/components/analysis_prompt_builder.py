# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from typing import List



from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import List
from src.core.data_models.analysis_result_model import JobAnalysisResult  # Your data model

class AnalysisPromptBuilder:
    """
Purpose:
    Constructs the structured prompt for the LLM to analyze a job vacancy.

Capabilities:
    - Defines a static system message that sets expectations for analysis and the required output schema.
    - Injects dynamic user inputs (job description + skills) via a separate human message.

Reasoning:
    This class only handles **prompt assembly** — it has zero logic for output parsing, validation, or generation.
    ✅ Clear separation between inputs (user data) and outputs (expected schema).
    ✅ No parser coupling.
    ✅ Full testability in isolation.
"""
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)

    def build_prompt(self, skillsets: List[str], job_to_apply: str) -> ChatPromptTemplate:
        system_analysis_template_str = """
        You are a senior HR analyst working for a career advisory platform.
        You do not sugarcoat the truth and provide honest and constructive feedback to job seekers.
        
        Your task is to analyze the provided job vacancy:
        - Extract the all identified skills for the role
        - Match the skills required for the role with the candidate's skills.
        - Provide an assestment on the candidate's suitability for the role.  additional provide details on where you found these skills and traits
        Job Vacancy Description:
        {job_position}

        Candidate's Skills:
        {my_skills}

        {format_instructions} 
        """

        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_analysis_template_str,
                input_variables=[],
                partial_variables={"format_instructions": self.parser.get_format_instructions()}
            )
        )

        human_analysis_template_str = """


        Candidate's Skills:
        {my_skills}
        """

        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_analysis_template_str,
                input_variables=["job_position", "my_skills"]
            )
        )

        return ChatPromptTemplate(messages=[system_prompt, human_prompt])
