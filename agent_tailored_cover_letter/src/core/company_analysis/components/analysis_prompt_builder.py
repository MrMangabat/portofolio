# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py
# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py

from langchain_core.messages.base import BaseMessage
from typing import List
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.analysis_result_model import JobAnalysisResult

class AnalysisPromptBuilder:
    """
    Purpose:
        Constructs a structured prompt for LLM analysis of job vacancies.

    Capabilities:
        - Extracts required skills from job description
        - Matches candidate skills against job requirements
        - Ensures structured JSON output compliance
    """

    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)
        self.format_instructions = self.parser.get_format_instructions()

    def build_prompt(self) -> ChatPromptTemplate:
        system_analysis_template_str = """
You are an AI assistant specializing in HR job requirement extraction and skills matching.

**CRITICAL - Extract These First:**
- company_name: The exact name of the hiring company
- job_title: The exact job title/position name
- language_detected: Primary language (e.g., "English", "Danish", "German")

**Instructions:**

1. **employees_skills_requirement (Dictionary):**
   
   Evaluate EACH skill from the <Candidate skills> section against the job requirements.
   
   For EVERY skill in the candidate's list:
   - Mark as `true` if the skill IS explicitly required by the job OR has a direct equivalent mentioned
   - Mark as `false` if the skill is NOT mentioned or required by the job
   
   IMPORTANT: This dictionary must contain ALL skills from <Candidate skills>, not new skills extracted from the job description.
   
   Equivalence examples:
   - Candidate has "Business analytics" + Job mentions "analytical skills" → Mark as TRUE
   - Candidate has "SCRUM" + Job mentions "Agile methodologies" → Mark as TRUE
   - Candidate has "Team player" + Job mentions "collaborative" → Mark as TRUE
   - Candidate has "Python" + Job does NOT mention "Python" → Mark as FALSE
   - Candidate has "Docker" + Job mentions "digital tools" (vague) → Mark as FALSE
   
   Be strict: Only mark TRUE if there is a clear, direct match or equivalent term.

2. **matching_skills (Dictionary):**
   
   This is a FILTERED subset of employees_skills_requirement.
   
   Include ONLY skills where employees_skills_requirement = TRUE.
   Do NOT include skills marked as FALSE.
   Do NOT include skills marked as FALSE even if they appear in this dictionary.
   
   Example:
    - If employees_skills_requirement contains: Python (false), Problem solving (true), SQL (false)
    - Then matching_skills should contain: Problem solving (true)

3. **analysis_output:**
   
   Provide a structured analysis containing:
   
   A. Match Statistics:
      - "X of Y candidate skills match (Z%)"
   
   B. Strongest Matches (3-5 skills):
      - List the candidate skills that match the job requirements
   
   C. Required Skills Missing from Candidate Profile:
      - If the job description mentions skills NOT in the candidate's list, note them here
      - Examples: "Microsoft Office", "Workshop facilitation", "PowerPoint"
   
   D. Candidate Skills Not Required by Job:
      - List 3-5 notable technical skills the candidate has that the job doesn't need
      - Example: "Candidate has Python, FastAPI, Docker - not required for this role"
   
   Format example:
   "14 of 57 skills match (24.5%). Strongest matches: Problem-solving, Strategy, Agile, Communication, Collaboration. Job requires but candidate lacks: Microsoft Office, Workshop facilitation. Candidate surplus: Python, FastAPI, Neo4J, Docker, PyTorch not needed for this consulting role."

**CRITICAL RULES:**

- Only mark a skill as required (TRUE) if the EXACT term or a direct equivalent appears in the job description
- "Data analysis" mentioned in job does NOT mean "Python" is required unless "Python" is explicitly written
- "Digital tools" mentioned in job does NOT mean "Docker", "Git", or "FastAPI" unless those specific tools are named
- When uncertain about a match, mark as FALSE
- Be conservative: It's better to miss a match (false negative) than to hallucinate a match (false positive)

<Position Description>
{job_position}
</Position Description>

<Candidate skills>
{my_skills}
</Candidate skills>

**Final Reminders:**
- employees_skills_requirement: Dictionary containing ALL candidate skills with TRUE/FALSE values
- matching_skills: Filtered dictionary containing ONLY skills marked as TRUE
- analysis_output: Your structured analysis following the A/B/C/D format above
- Be strict and conservative with matches
{format_instructions}
"""

        SYSTEM_PROMPT = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_analysis_template_str,
                input_variables=["job_position", "my_skills"],
                partial_variables={"format_instructions": self.format_instructions}
            )
        )

        return ChatPromptTemplate(
            messages=[SYSTEM_PROMPT],
            input_variables=["job_position", "my_skills"]
        )