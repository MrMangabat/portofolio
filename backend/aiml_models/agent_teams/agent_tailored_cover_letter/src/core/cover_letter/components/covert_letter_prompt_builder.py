# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py


from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.analysis_result_model import JobAnalysisResult  # Structured Output Model

class AnalysisPromptBuilder:
    """
    Purpose:
        Constructs a structured prompt for LLM analysis of job vacancies.

    Capabilities:
        - Defines a system message that sets expectations for analysis and required JSON schema.
        - Injects dynamic user inputs (job description + skills) via a separate human message.
        - Ensures that the output **strictly follows** a structured JSON format.

    Reasoning:
        - ✅ Separates **inputs** (user data) from **outputs** (expected JSON schema).
        - ✅ Reinforces JSON output compliance to avoid parsing errors.
        - ✅ Executes `.format_messages()` to correctly inject variables.
    """

    def __init__(self) -> None:
        # Enforce structured JSON output
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)
        self.format_instructions = self.parser.get_format_instructions()

    def cover_letter_build_prompt(self, skillsets: list[str], job_to_apply: str) -> ChatPromptTemplate:
        # System message enforcing JSON output
        system_analysis_template_str = """
        You are an AI assistant specializing in HR job analysis.
        Your task is to analyze a given job vacancy and match it with a candidate's skills.
        - Identified relevant skills from the job description.
        - Match the required skills with the candidate’s skills.
        - Assess the candidate's suitability for the role.
        - Identify:
            - The company name.
            - The job title.
            - Required skills and technical experience (stored as a dictionary).
            - Matching skills (stored as a dictionary).
        - Write a detailed analysis of the job vacancy and the candidate's skills on a one pager
        The candidate's skills are:
        {my_skills}

        {format_instructions}
        """

        SYSTEM_PROMPT = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_analysis_template_str,
                input_variables=["my_skills"],  # No user input needed
                partial_variables={"format_instructions": self.parser.get_format_instructions()}  # Enforce JSON format
            )
        )

        # Human input message
        human_analysis_template_str = """
        Here is a job description that needs analysis:
        Job Vacancy: 
        {job_position}
        
        {format_instructions}
        """

        HUMAN_PROMPT = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_analysis_template_str,
                input_variables=["job_position"],
                partial_variables={"format_instructions": self.parser.get_format_instructions()}  # Enforce JSON format
            )
        )
        # Ensure that messages are formatted BEFORE returning the ChatPromptTemplate
        messages = [SYSTEM_PROMPT, HUMAN_PROMPT]
        print(messages)
        chat_prompt = ChatPromptTemplate(
            messages=messages
        )


        chat_prompt.format_messages(
            job_position=skillsets,
            my_skills=job_to_apply,
            format_messages=self.parser.get_format_instructions()
        )

        return chat_prompt
