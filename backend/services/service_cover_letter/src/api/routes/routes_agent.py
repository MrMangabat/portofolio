# backend/services/service_cover_letter/src/api/routes/routes_agent.py

"""
Agent Routes - Connects to ML Platform Approved Agent

This service calls the APPROVED and DEPLOYED cover letter agent.
The agent only becomes available after going through:
  1. Development & experimentation (ML Platform)
  2. Evaluation against test suites
  3. Approval workflow
  4. Containerization & deployment
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os

router = APIRouter()

# Agent endpoint - points to APPROVED agent container
AGENT_URL = os.getenv("AGENT_URL", "http://cover_letter_agent_prod:8000")


class CoverLetterRequest(BaseModel):
    job_description: str
    unique_user_input: Optional[str] = ""


class CoverLetterResponse(BaseModel):
    company_name: str
    job_title: str
    introduction: str
    motivation: str
    unique_selling_points: str
    bulletpoint_1: str
    bulletpoint_2: str
    bulletpoint_3: str
    bulletpoint_4: str
    thank_you: str
    iterations: int
    violations: int


@router.post("/generate", response_model=CoverLetterResponse)
async def generate_cover_letter(request: CoverLetterRequest):
    """
    Generate a cover letter using the approved AI agent.

    This endpoint calls the containerized agent that has been:
    - Developed and tested in the ML Platform
    - Evaluated against quality benchmarks
    - Approved for production use
    - Deployed as a standalone service

    Architecture:
        service_cover_letter → cover_letter_agent (approved container)

    Args:
        request: Job description and optional user input

    Returns:
        Generated cover letter with all sections

    Raises:
        HTTPException 503: Agent service unavailable
        HTTPException 500: Agent execution error
        HTTPException 504: Agent timeout
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{AGENT_URL}/generate",
                json={
                    "job_description": request.job_description,
                    "unique_user_input": request.unique_user_input
                }
            )

            if response.status_code == 200:
                return CoverLetterResponse(**response.json())
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Agent returned error: {response.text}"
                )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Agent execution timed out (>120s)"
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Agent service unavailable at {AGENT_URL}. Ensure approved agent is deployed."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error calling agent: {str(e)}"
        )


@router.get("/agent/health")
async def check_agent_health():
    """
    Check if the approved agent is healthy and accessible.

    Returns agent version and status.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{AGENT_URL}/health")

            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "agent_info": response.json()
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": response.text
                }

    except Exception as e:
        return {
            "status": "unreachable",
            "error": str(e),
            "agent_url": AGENT_URL
        }
