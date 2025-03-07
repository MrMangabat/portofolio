# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_prompt_builder.py

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from typing import List

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
        pass  # No dependencies needed — pure prompt logic.

    def build_prompt(self, skillsets: List[str], job_to_apply: str) -> ChatPromptTemplate:
        """
        Assembles and returns the structured prompt for the LLM.

        Args:
            skillsets (List[str]): Candidate's skills (from service_cover_letter corrections).
            job_to_apply (str): Full job description text.

        Returns:
            ChatPromptTemplate: Fully assembled system+human message ready for LLM.
        """

        # ⚙️ Static system message — this does NOT rely on dynamic input.
        system_message = """
You are a senior HR analyst working for a career advisory platform.
Your task is to analyze the provided job vacancy and return **only** a JSON object that matches this schema:

Important:
- Do not add explanations, greetings, or comments.
- Only return the JSON object — no other text.
        """.strip()

        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(template=system_message)
        )

        # ⚙️ Dynamic human message — this injects **real user data** (description + skills).
        human_message = """
Job Vacancy Description:
{job_position}

Candidate's Skills:
{my_skills}
        """.strip()

        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message,
                input_variables=["job_position", "my_skills"]  # These are real inputs injected at runtime.
            )
        )

        # ✅ Combine into a final ChatPromptTemplate (what Ollama sees).
        return ChatPromptTemplate(messages=[system_prompt, human_prompt])
