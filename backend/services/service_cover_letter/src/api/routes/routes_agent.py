# backend/services/service_cover_letter/src/api/routes/routes_agent.py

"""
Agent Routes - Cover Letter Generation using LangGraph Agent

This service uses the integrated LangGraph agent for cover letter generation.
The agent uses a 4-tier hierarchical supervisor architecture:
  - Tier 1: Main Supervisor
  - Tier 2: Officers (Personality, Document, Research)
  - Tier 3: Workers
  - Tier 4: Research Sub-agents
"""

from fastapi import APIRouter, Depends

from src.api.dependencies import get_agent_service
from src.api.schemas.agent_schemas import (
    AgentHealthResponse,
    CoverLetterRequest,
    CoverLetterResponse,
)
from src.service_layer.agent_service import AgentService

router = APIRouter()


@router.post("/generate", response_model=CoverLetterResponse)
async def generate_cover_letter(
    request: CoverLetterRequest,
    agent_service: AgentService = Depends(get_agent_service),
):
    """
    Generate a cover letter using the integrated AI agent.

    This endpoint uses the LangGraph-based hierarchical agent to:
    - Analyze the candidate profile against job requirements
    - Generate a tailored cover letter with structured sections
    - Create PDFs for both cover letter and CV

    Architecture:
        Main Supervisor -> Officers -> Workers -> Sub-agents

    Args:
        request: Job description and optional user input

    Returns:
        Generated cover letter with all sections and metadata

    Raises:
        HTTPException 500: Agent execution error
    """
    result = await agent_service.generate_cover_letter(
        job_description=request.job_description,
        user_id=request.user_id,
    )

    return CoverLetterResponse(**result)


@router.get("/health", response_model=AgentHealthResponse)
async def check_agent_health(
    agent_service: AgentService = Depends(get_agent_service),
):
    """
    Check if the agent is healthy and accessible.

    Returns agent configuration and status.
    """
    health = await agent_service.get_agent_health()
    return AgentHealthResponse(**health)
