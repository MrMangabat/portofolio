"""API schemas for agent endpoints."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class CoverLetterRequest(BaseModel):
    """Request schema for cover letter generation."""

    job_description: str = Field(
        ...,
        min_length=50,
        max_length=10000,
        description="The job posting/description text",
    )
    user_id: Optional[str] = Field(
        None,
        description="Optional user ID for tracking",
    )


class KeyHighlightCategoryResponse(BaseModel):
    """Response schema for key highlight category."""

    title: str
    points: list[str]


class KeyHighlightsResponse(BaseModel):
    """Response schema for key highlights."""

    header: str
    categories: list[KeyHighlightCategoryResponse]


class CoverLetterContentResponse(BaseModel):
    """Response schema for cover letter content."""

    company_name: str
    position: str
    intro_paragraph: str
    motivation_paragraph: str
    who_am_i: str
    key_highlights: Optional[KeyHighlightsResponse] = None
    approach_for_role_paragraph: str
    outro_paragraph: str


class CoverLetterResponse(BaseModel):
    """Response schema for cover letter generation."""

    success: bool = Field(
        ...,
        description="Whether the generation was successful",
    )
    cover_letter: Optional[dict[str, Any]] = Field(
        None,
        description="The generated cover letter data",
    )
    feedback: dict[str, Any] = Field(
        default_factory=dict,
        description="Feedback from the generation process",
    )
    messages_count: Optional[int] = Field(
        None,
        description="Number of messages in the workflow",
    )
    error: Optional[str] = Field(
        None,
        description="Error message if generation failed",
    )


class AgentHealthResponse(BaseModel):
    """Response schema for agent health check."""

    status: str = Field(
        ...,
        description="Health status (healthy/unhealthy)",
    )
    graph_nodes: Optional[Any] = Field(
        None,
        description="Number of nodes in the agent graph",
    )
    llm_model: Optional[str] = Field(
        None,
        description="The LLM model being used",
    )
    error: Optional[str] = Field(
        None,
        description="Error message if unhealthy",
    )
