"""LLM context management for agent nodes.

This module provides a way to inject the LLMService into agent nodes
without having to pass it through the state.
"""

from typing import Optional

from src.ai_ml.llm_service import LLMService

# Module-level LLM service instance
_llm_service: Optional[LLMService] = None


def set_llm_service(llm_service: LLMService) -> None:
    """Set the LLM service for agent nodes to use.

    Args:
        llm_service: The LLMService instance to use
    """
    global _llm_service
    _llm_service = llm_service


def get_llm_service() -> LLMService:
    """Get the configured LLM service.

    Returns:
        The LLMService instance

    Raises:
        RuntimeError: If LLM service hasn't been configured
    """
    if _llm_service is None:
        raise RuntimeError(
            "LLM service not configured. Call set_llm_service() before using agent nodes."
        )
    return _llm_service


def clear_llm_service() -> None:
    """Clear the LLM service (useful for testing)."""
    global _llm_service
    _llm_service = None
