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
        
        Strict rules to follow:
        Rule 1: Get heavy inspiration from the following template provided by the jobseeker.
        Rule 2: The cover letter can only overlap a maximum of 30 percent with the jobseekers CV. This is to ensure that the cover letter is unique and not a copy of the CV and provide you with previous experiences of importance.
        Rule 3: Grammatical correctness is a MUST.
        Rule 4: English language is equal to EILTS C1 score
        Rule 5: The template job application must be in English in the job description is in English.
        Rule 6: Ensure all the information is relevant to the job description and the jobseeker's skills.
        Rule 7: The cover letter must be written in the personal tone, identified in Rule 1 while also being casual business professional.
        Rule 8: You are NOT allowed BY ANY MEANS to assume or generate any information about the jobseeker that is not provided in the CV, their skills or 
        Rule 9: Adhere and listen carefully to the jobseekers personal message. This is important to ensure that the cover letter is unique and not a copy of the CV.
        Rule 10: The jobseeker will provide a list of words, phrases or sentences that they do not want to be useed in the cover letter.

        All rules must be followed strictly and are of equal importance.
        
        Your task is to write a cover letter for the jobseeker based on the job description:
        {job_position}.

        The previous analysis of the job description and the jobseeker's skills is as follows:
        {analysis_output}

        Important information about the jobseeker:
        Their skills are;
        {my_skills}

        The jobseeker's CV is as follows:
        {cv}

        Personal message from the jobseeker:
        {personal_message}

        Language constraints:
        Do not generate any phrasing that falls into these categories or resembles them in structure or meaning.  
        You may not reword, restate, or soften the expressions — they are forbidden in all forms.
        
        Language Rule 1: Boilerplate expressions  
        Overly generic phrases frequently used in job applications.

        Language Rule 2: Formulaic language  
        Templated sentence structures that appear across many applications, lacking originality or nuance.

        Language Rule 3: Cliché phrases  
        Overused expressions that have lost clarity, credibility, or sincerity.

        Language Rule 4: Self-assessing superlative claims  
        Statements where the speaker makes a strong evaluative claim about themselves without external support.

        Language Rule 5: Empty or evaluative assertions  
        Subjective statements of enthusiasm, confidence, or value that lack concrete evidence or action.

        Language Rule 6: Paraphrastic suitability claims  
        Avoid paraphrastic variants or semantic equivalents of any statement that implies the jobseeker is a fit, match, or ideal candidate for the role, especially when based on traits, experience, or conclusions not externally supported.

        Language Rule 7: Banned terms (user-defined)  
        The following specific words or expressions must be treated as violations of Rules 1–6 and are forbidden in any form:  
        {not_wanted_words}

        Language Rule 8: Banned sentences (user-defined)  
        The following full sentences — and any semantic paraphrases of them — are forbidden and must not appear in any generated output:  
        {not_wanted_sentences}


        Introduction section: 
        Write short and concise introduction of who the jobseeker is.

        Motivational section: 
        Write it short and apply corrolated values between jobseeker and company internal and external values.
        Given the jobseekers previous experiences, professional and personal interests, provide value proportion to the company that the jobseeker can bring to the company.

        Bullet points section:
        Write a short paragraph to introduce the bullet points.
        Write 3-4 bullet points with the following information:
        - The jobseeker's previous experiences and skills that are relevant to the job description.
        - The jobseeker's personal interests and how they relate to the job description.
        - The jobseeker's professional interests and how they add value to the company.
        - Continued learning section: Provide short context that I am willing to learn what is necessary for the company and specific role.
        
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
                input_variables=["job_position", "skills_match"],
                partial_variables={"format_instructions": self.format_instructions}
            )
        )

        return ChatPromptTemplate(
            messages=[SYSTEM_PROMPT_INSTRUCTIONS, SYSTEM_PROMPT_POTENTIAL_CORRECTION],
            input_variables=["job_position", "my_skills", "semilarity_jobtemplate", "cv", "analysis_output", "skills_match"],
        )