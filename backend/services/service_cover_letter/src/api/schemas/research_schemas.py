"""API schemas for research endpoints."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ResearchOfficerType(str, Enum):
    """Types of research officers available."""

    FINANCIAL = "financial"
    BUSINESS = "business"
    COMPANY = "company"
    MACRO = "macro"


class ResearchRequest(BaseModel):
    """Request schema for parallel research execution."""

    company_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The company name to research",
    )
    officers: Optional[list[ResearchOfficerType]] = Field(
        None,
        description="Specific officers to run (default: all)",
    )


class SingleResearchRequest(BaseModel):
    """Request schema for single officer research."""

    company_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The company name to research",
    )


class OfficerResult(BaseModel):
    """Result from a single research officer."""

    officer: str
    company: str
    status: str
    data: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class ResearchResponse(BaseModel):
    """Response schema for research endpoints."""

    company: str = Field(
        ...,
        description="The company that was researched",
    )
    results: dict[str, OfficerResult] = Field(
        default_factory=dict,
        description="Results from each research officer",
    )
    errors: Optional[list[dict[str, Any]]] = Field(
        None,
        description="List of errors if any occurred",
    )
    total_officers: int = Field(
        ...,
        description="Total number of officers executed",
    )
    successful: int = Field(
        ...,
        description="Number of successful executions",
    )


class CachedResearchResponse(BaseModel):
    """Response schema for cached research lookup."""

    company: str
    found: bool
    results: Optional[dict[str, Any]] = None
    cached_at: Optional[str] = None
