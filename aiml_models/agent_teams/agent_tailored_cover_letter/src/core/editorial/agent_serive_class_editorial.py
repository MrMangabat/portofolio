# src/core/editorial/agent_service_class_editorial.py

from typing import Dict, List
from src.core.editorial.components.editorial_prompt_builder import EditorialPromptBuilder
from src.core.editorial.components.editorial_response_parser import EditorialResultParser
from src.infrastructure.llm_client import LLMClient

class AgentServiceClassEditorial:
    """
    Purpose:
        Handles correction and validation of AI-generated cover letters using editorial rules.
    
    Capabilities:
        - Uses strict rule-based prompts to revise only problematic sections.
        - Invokes LLM with structured editorial prompt.
        - Returns a corrected generation.
    
    Reasoning:
        Keeps editorial validation encapsulated with minimal prompt injection, allowing future changes to rules or parser without affecting other agents.
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

    def validate_and_correct(self, state: Dict) -> Dict:
        """
        Applies editorial validation logic to revise a generated cover letter through the prompt.

        Args:
            state (Dict): LangGraph graph state.

        Returns:
            Dict: Updated state with validated generation.
        """
        job_description: str = state["job_description"]
        skills: List[str] = state["skills"]
        generation: str = state["generation"]
        editorial_violations: List[str] = state["editorial_error_messages"]

        prompt_chain = (
            self.prompt_builder.build_prompt()
            | self.llm_client.get_model("gpt")
            | self.response_parser.parser
        )

        result = prompt_chain.invoke({
            "job_description": job_description,
            "my_skills": ", ".join(skills),
            "generation": generation,
            "messages": editorial_violations
        })

        return {**state, "generation": result}
