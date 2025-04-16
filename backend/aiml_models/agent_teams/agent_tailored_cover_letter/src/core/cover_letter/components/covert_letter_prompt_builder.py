# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py

# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py

from langchain_core.messages.base import BaseMessage
from typing import List
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.analysis_result_model import JobAnalysisResult  # Structured Output Model

class AnalysisPromptBuilder:
    """
    Purpose:
        Constructs a structured prompt for LLM generation of cover letters.
        Works only with openai models.

    Capabilities:
        - Defines a system message that sets expectations how to craft a cover letter.
        - Injects dynamic user inputs (job description + skills) via a separate human message.
        - Ensures that the output **strictly follows** a structured JSON format.
        - Takes user templates/previous cover letters into account through cosine-similarity and uses that.

    Reasoning:
        - 
    """

    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)
        self.format_instructions = self.parser.get_format_instructions()

    def build_prompt(self) -> ChatPromptTemplate:
        # System message template
        system_analysis_template_str = """
        You are to assist in writing cover letter for a job.
        This template is the jobtemplate: {semilarity_jobtemplate}. Keep the personal tonality found.
        The jobtemplate is a professional document and the generated cover letter must adhere to it.
        Grammatical correctness is essential.
        Use casual language.
        Ensure the English language is equal to EILTS C1 score.
        The template job application must be in English.
        The unique skills can be in this list: {my_skills}.
        {messages_placeholder}
        {format_instructions}
        """

        SYSTEM_PROMPT = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_analysis_template_str,
                input_variables=["my_skills"],
                partial_variables={"format_instructions": self.format_instructions}
            )
        )

        # Human message template
        human_analysis_template_str = """
        Introduction section: Write three lines to generate an introduction with interest in IT and AI with inspiration from the {analysis_output}.
        Motivation section: Write it short and use few examples found matching pairs {skill_match} and how these can be utilized for the company's benefit.
        Continued learning section: Provide short context that I am willing to learn what is necessary for the company and specific role.
        Thank you section: Write a short and concise thank you note to set up a coffee.
        I DO NOT have prior experience in a professional environment in programming, ONLY academia.
        I DO have prior experience in project management.
        {messages_placeholder}
        {format_instructions}
        """

        HUMAN_PROMPT = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_analysis_template_str,
                input_variables=["job_position"],
                partial_variables={"format_instructions": self.format_instructions}
            )
        )

        return ChatPromptTemplate(
            messages=[SYSTEM_PROMPT, HUMAN_PROMPT],
            input_variables=["job_position", "my_skills"]
        )