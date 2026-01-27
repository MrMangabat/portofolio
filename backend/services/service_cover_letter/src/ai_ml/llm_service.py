"""LLM Service for GPT-4o orchestration.

This module wraps ChatOpenAI with settings injection for the cover letter agent.
Embeddings stay in qdrant_repository (unchanged).
"""

from typing import Type, TypeVar

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.config.settings import CoverLetterSettings

T = TypeVar("T", bound=BaseModel)


class LLMService:
    """LLM Service wrapping ChatOpenAI with settings injection."""

    def __init__(self, settings: CoverLetterSettings):
        """Initialize LLM service with settings.

        Args:
            settings: Application settings containing OpenAI API key and LLM config
        """
        self._settings = settings
        self._llm = ChatOpenAI(
            model=getattr(settings, "LLM_MODEL", "gpt-4o"),
            temperature=getattr(settings, "LLM_TEMPERATURE", 0.1),
            api_key=settings.OPENAI_API_KEY,
        )

    @property
    def llm(self) -> ChatOpenAI:
        """Get the underlying ChatOpenAI instance."""
        return self._llm

    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt and return the response.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            The LLM response as a string
        """
        response = self._llm.invoke(prompt)
        return response.content

    def invoke_structured(self, prompt: str, schema: Type[T]) -> T:
        """Invoke the LLM with a prompt and return structured output.

        Args:
            prompt: The prompt to send to the LLM
            schema: Pydantic model class for structured output

        Returns:
            Instance of the schema populated with LLM response
        """
        structured_llm = self._llm.with_structured_output(schema)
        return structured_llm.invoke(prompt)

    def with_structured_output(self, schema: Type[T]):
        """Get an LLM instance configured for structured output.

        Args:
            schema: Pydantic model class for structured output

        Returns:
            ChatOpenAI instance configured for structured output
        """
        return self._llm.with_structured_output(schema)
