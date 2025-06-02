# src/core/editorial/agent_service_class_editorial.py
from typing import Dict, List
from src.core.editorial.components.editorial_prompt_builder import EditorialPromptBuilder
from src.core.editorial.components.editorial_response_parser import EditorialResultParser
from src.infrastructure.llm_client import LLMClient
from src.core.data_models.editorial_model import EditorialResult


class AgentServiceClassEditorial:
    """
    Purpose:
        Handles correction and validation of AI-generated cover letters using editorial rules.

    Capabilities:
        - Uses strict rule-based prompts to revise only problematic sections.
        - Invokes LLM with structured editorial prompt.
        - Returns corrected generation as EditorialResult — no state mutation.

    Reasoning:
        Pure service object — isolated logic, testable, no side effects on LangGraph state.
    """

    def __init__(
        self,
        prompt_builder: EditorialPromptBuilder,
        response_parser: EditorialResultParser,
        llm_client: LLMClient
    ) -> None:
        self.prompt_builder: EditorialPromptBuilder = prompt_builder
        self.response_parser: EditorialResultParser = response_parser
        self.llm_client: LLMClient = llm_client

    def validate_and_correct(self, job_description: str, skills: List[str], generation: str, editorial_violations: List[str]) -> EditorialResult:
        """
        Applies editorial validation logic to revise a generated cover letter through the prompt.

        Args:
            job_description (str): The original job description.
            skills (List[str]): User-provided skill list.
            generation (str): The previous cover letter.
            editorial_violations (List[str]): List of violations to fix.

        Returns:
            EditorialResult: Parsed, corrected output.
        """
        prompt_chain = (
            self.prompt_builder.build_prompt()
            | self.llm_client.get_model("gpt")
            | self.response_parser.parser
        )

        return prompt_chain.invoke({
            "job_description": job_description,
            "my_skills": ", ".join(skills),
            "generation": generation,
            "editorial_error_messages": editorial_violations
        })
        