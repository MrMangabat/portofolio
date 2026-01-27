# backend/services/service_cover_letter/src/api/routes/routes_research.py

"""
Research Routes - Parallel Company Research Endpoints

This service provides endpoints for executing research on companies
using specialized research officers (financial, business, company, macro).
"""

from fastapi import APIRouter, Depends, HTTPException, Path

from src.api.dependencies import get_research_service
from src.api.schemas.research_schemas import (
    CachedResearchResponse,
    ResearchOfficerType,
    ResearchRequest,
    ResearchResponse,
    SingleResearchRequest,
)
from src.service_layer.research_service import ResearchService
from src.service_layer.research_service import ResearchOfficerType as ServiceOfficerType

router = APIRouter()


def _convert_officer_type(api_type: ResearchOfficerType) -> ServiceOfficerType:
    """Convert API enum to service layer enum."""
    return ServiceOfficerType(api_type.value)


@router.post("/company/all", response_model=ResearchResponse)
async def research_company_all(
    request: ResearchRequest,
    research_service: ResearchService = Depends(get_research_service),
):
    """
    Execute all research officers in parallel for a company.

    This endpoint runs all 4 research officers concurrently:
    - Financial Analyst
    - Business Intelligence Analyst
    - Company Profile Analyst
    - Macro Officer

    Target latency: ~200ms for all parallel executions.

    Args:
        request: Company name and optional list of specific officers

    Returns:
        Combined research results from all officers
    """
    officers = None
    if request.officers:
        officers = [_convert_officer_type(o) for o in request.officers]

    result = await research_service.execute_all_research(
        company_name=request.company_name,
        officers=officers,
    )

    return ResearchResponse(**result)


@router.post("/company/{officer}", response_model=ResearchResponse)
async def research_company_single(
    officer: ResearchOfficerType = Path(
        ...,
        description="The research officer type to execute",
    ),
    request: SingleResearchRequest = ...,
    research_service: ResearchService = Depends(get_research_service),
):
    """
    Execute a single research officer for a company.

    Available officers:
    - financial: Financial due diligence
    - business: Business model and competitive analysis
    - company: People, culture, and organizational analysis
    - macro: Industry trends and macroeconomic analysis

    Args:
        officer: The type of research officer to run
        request: Company name to research

    Returns:
        Research results from the specified officer
    """
    service_officer = _convert_officer_type(officer)

    result = await research_service.execute_single_research(
        company_name=request.company_name,
        officer_type=service_officer,
    )

    return ResearchResponse(
        company=request.company_name,
        results={officer.value: result},
        errors=None,
        total_officers=1,
        successful=1 if result.get("status") != "error" else 0,
    )


@router.get("/company/{company_name}/cached", response_model=CachedResearchResponse)
async def get_cached_research(
    company_name: str = Path(
        ...,
        min_length=1,
        max_length=200,
        description="The company name to look up",
    ),
    research_service: ResearchService = Depends(get_research_service),
):
    """
    Get cached research results for a company.

    Returns previously cached research if available,
    or indicates that no cache exists.

    Args:
        company_name: The company to look up

    Returns:
        Cached research results or not found indicator
    """
    cached = await research_service.get_cached_research(company_name)

    if cached:
        return CachedResearchResponse(
            company=company_name,
            found=True,
            results=cached.get("results"),
            cached_at=cached.get("cached_at"),
        )

    return CachedResearchResponse(
        company=company_name,
        found=False,
        results=None,
        cached_at=None,
    )
