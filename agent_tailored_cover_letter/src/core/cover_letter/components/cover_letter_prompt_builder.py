# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/components/cover_letter_prompt_builder.py

from langchain_core.messages.base import BaseMessage
from typing import List
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.analysis_result_model import JobAnalysisResult  # Structured Output Model

class CoverLetterPromptBuilder:


    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)
        self.format_instructions = self.parser.get_format_instructions()

    def build_prompt(self) -> ChatPromptTemplate:
        # System message template
        system_analysis_template_str = """
        You are a professional writer, whos aim is to assist in writing cover letter for job seekers.
        For you to have a better understanding of the job, you will first get the job description, previous experiences and a analysis of the job description.
        
        ***TASK***
        Strict rules to follow:
        - Get inspiration from the following template provided in the <Template for inspiration>.
        -- The template is only for inspiration, writing style of the candidate
        -- Do NOT copy the company name, job title or any other specific context in relation to that unique application.
        
        
        Grammatical correctness is a MUST.
        English language is equal to EILTS C1 score

        **CRITICAL:**   <language_detected>     
        You are NOT allowed BY ANY MEANS to assume or generate any information about the jobseeker that is not provided in the CV, their skills or 
        The cover letter must be written in the personal tone, identified in <template to follow closely>,
        The jobseeker will provide a list of words, phrases or sentences that they do not want to be useed in the cover letter.




        The template job application must be in language detected.
        <language_detected>
        {language_detected}
        </language_detected>

        Your task is to write a cover letter for the jobseeker based on the job description:
        <position description>
        {job_position}
        </position description>

        <analysis_output>
        {analysis_output}
        </analysis_output>

        <Candidate skills>
        {my_skills}
        </Candidate skills>

        <Skills Match>
        {skills_match}
        </Skills Match>

        <candidate CV>
        {cv}
        </candidate CV>

        <Template for inspiration>
        {semilarity_jobtemplate}
        </Template for inspiration>

        <Personal message from candidate>
        {personal_message}
        </Personal message from candidate>

        <BANED WORDS> 
        {not_wanted_words}
        </BANED WORDS>

        <BANNED SENTENCES>
        {not_wanted_sentences}
        </BANNED SENTENCES>


        Introduction section: 
        Write short and concise introduction of who the jobseeker is.

        Motivational section: 
        Write it short and apply corrolated values between jobseeker and company internal and external values.
        Given the jobseekers previous experiences, professional and personal interests, provide value proportion to the company that the jobseeker can bring to the company.

        
        Thank you section:
        Write a short and concise thank you note to set up a coffee.
        {format_instructions}
        """

        SYSTEM_PROMPT_INSTRUCTIONS = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_analysis_template_str,
                input_variables=["job_position", "my_skills", "semilarity_jobtemplate", "cv", "analysis_output", "skills_match", "not_wanted_words", "not_wanted_sentences", "personal_message"],
                partial_variables={"format_instructions": self.format_instructions}
            )
        )

        # Human message template
        system_potential_correction_template_str = """
        Message from the editor agent. Issues with the cover letter:
        {messages_placeholder}
        {format_instructions}
        """

        SYSTEM_PROMPT_POTENTIAL_CORRECTION = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_potential_correction_template_str,
                input_variables=["job_position", "skills_match", "messages_placeholder"],
                partial_variables={"format_instructions": self.format_instructions}
            )
        )

        return ChatPromptTemplate(
            messages=[SYSTEM_PROMPT_INSTRUCTIONS, SYSTEM_PROMPT_POTENTIAL_CORRECTION],
            input_variables=["job_position", "my_skills", "semilarity_jobtemplate", "cv", "analysis_output", "skills_match"],
        )