"""Agent Service for cover letter generation workflow orchestration."""

import logging
from typing import Optional

from langsmith import traceable

from src.agent import build_graph, load_initial_state
from src.agent._llm_context import clear_llm_service, set_llm_service
from src.ai_ml.llm_service import LLMService
from src.config.settings import CoverLetterSettings

logger = logging.getLogger(__name__)


class AgentService:
    """Service for orchestrating the cover letter generation agent workflow."""

    def __init__(self, settings: CoverLetterSettings):
        """Initialize the agent service.

        Args:
            settings: Application settings
        """
        self._settings = settings
        self._llm_service = LLMService(settings)
        self._recursion_limit = getattr(settings, "AGENT_RECURSION_LIMIT", 50)

    @traceable(run_type="chain", name="Generate Cover Letter")
    async def generate_cover_letter(
        self,
        job_description: str,
        user_id: Optional[str] = None,
    ) -> dict:
        """Generate a cover letter for a job description.

        Args:
            job_description: The job posting/description text
            user_id: Optional user ID for tracking

        Returns:
            dict containing the generated cover letter data and metadata
        """
        logger.info(
            "Starting cover letter generation for user: %s",
            user_id or "anonymous",
        )
        logger.debug("Job description length: %d chars", len(job_description))

        try:
            # Set the LLM service for agent nodes to use
            set_llm_service(self._llm_service)

            # Load initial state with job position
            initial_state = load_initial_state(job_description)

            # Build and invoke the graph
            graph = build_graph()
            result = graph.invoke(
                initial_state,
                {"recursion_limit": self._recursion_limit},
            )

            logger.info("Cover letter generation completed successfully")

            # Extract relevant data from result
            documents = result.get("documents", {})
            cover_letter = documents.get("cover_letter", {})
            feedback = result.get("feedback", {})

            return {
                "success": True,
                "cover_letter": cover_letter,
                "feedback": feedback,
                "messages_count": len(result.get("messages", [])),
            }

        except Exception as e:
            logger.error("Cover letter generation failed: %s", e, exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "cover_letter": None,
                "feedback": {"status": "error", "message": str(e)},
            }

        finally:
            # Clean up the LLM service context
            clear_llm_service()

    async def get_agent_health(self) -> dict:
        """Check the health of the agent service.

        Returns:
            dict with health status information
        """
        try:
            # Try to build the graph to verify everything is configured correctly
            graph = build_graph()
            return {
                "status": "healthy",
                "graph_nodes": len(graph.nodes) if hasattr(graph, "nodes") else "unknown",
                "llm_model": getattr(self._settings, "LLM_MODEL", "gpt-4o"),
            }
        except Exception as e:
            logger.error("Agent health check failed: %s", e)
            return {
                "status": "unhealthy",
                "error": str(e),
            }
