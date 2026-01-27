"""Dependency injection for agent-related services."""

from functools import lru_cache

from src.ai_ml.llm_service import LLMService
from src.config.settings import CoverLetterSettings
from src.service_layer.agent_service import AgentService
from src.service_layer.research_service import ResearchService


@lru_cache()
def get_settings() -> CoverLetterSettings:
    """Get cached application settings."""
    return CoverLetterSettings()


def get_llm_service() -> LLMService:
    """Get LLM service instance.

    Returns:
        LLMService configured with application settings
    """
    settings = get_settings()
    return LLMService(settings)


def get_agent_service() -> AgentService:
    """Get agent service instance.

    Returns:
        AgentService configured with application settings
    """
    settings = get_settings()
    return AgentService(settings)


def get_research_service() -> ResearchService:
    """Get research service instance.

    Returns:
        ResearchService configured with application settings
    """
    settings = get_settings()
    return ResearchService(settings)
