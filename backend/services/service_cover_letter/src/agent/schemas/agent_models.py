"""Pydantic schemas for structured LLM outputs."""

from pydantic import BaseModel, Field, field_validator


class CVProfile(BaseModel):
    """Structured output for CV profile section generation."""

    profile_text: str = Field(
        min_length=100,
        max_length=1500,
        description=(
            "A 3-5 sentence professional profile paragraph for a CV. "
            "Structure: (1) State education/degree and core expertise areas, "
            "(2) Highlight specific practical experience relevant to the position, "
            "(3) Mention key technical strengths and methodologies, "
            "(4) State what role you're seeking and what you aim to contribute. "
            "Write in third person implied (no 'I' statements). Be specific and concise."
        ),
    )


class ProfileAnalysis(BaseModel):
    """Structured output for profile analysis."""

    required_skills: list[str] = Field(
        min_length=1,
        description="Skills required by the job position",
    )
    relevant_skills: list[str] = Field(
        min_length=1,
        description="Skills relevant to the job position",
    )
    relevant_experience: list[str] = Field(
        min_length=1,
        description="Work experiences relevant to the job",
    )
    skills_match: dict[str, bool] = Field(
        description="Boolean dict indicating skill matches (skill name -> True if candidate has it)"
    )
    reasoning_for_experience_selection: str = Field(
        min_length=50,
        description="Reasoning behind experience selection",
    )
    summary: str = Field(
        min_length=50,
        max_length=500,
        description="Brief summary of candidate fit",
    )


class KeyHighlightCategory(BaseModel):
    """A category of key highlights with bullet points."""

    title: str = Field(
        min_length=3,
        max_length=50,
        description="Category title (e.g., 'AI/ML Development', 'Technical Proficiency')",
    )
    points: list[str] = Field(
        min_length=3,
        max_length=3,
        description="Exactly 3 bullet points highlighting achievements/skills in this category",
    )

    @field_validator("points")
    @classmethod
    def validate_points_not_empty(cls, v: list[str]) -> list[str]:
        """Ensure each bullet point has meaningful content."""
        for i, point in enumerate(v):
            if len(point.strip()) < 10:
                raise ValueError(f"Point {i + 1} is too short (minimum 10 characters)")
        return v


class KeyHighlights(BaseModel):
    """Key highlights section for cover letter."""

    header: str = Field(
        min_length=10,
        max_length=100,
        description="Section header text (e.g., 'Key highlights of my experience and skills:')",
    )
    categories: list[KeyHighlightCategory] = Field(
        min_length=3,
        max_length=3,
        description="Exactly 3 highlight categories with bullet points",
    )


class CoverLetterContent(BaseModel):
    """Structured output for cover letter content generation."""

    company_name: str = Field(
        min_length=1,
        max_length=100,
        description="Company name extracted from the job posting",
    )
    position: str = Field(
        min_length=2,
        max_length=100,
        description="Job position title as stated in the job posting",
    )
    intro_paragraph: str = Field(
        min_length=100,
        max_length=800,
        description="Opening paragraph introducing the candidate and their interest in the role (2-4 sentences)",
    )
    motivation_paragraph: str = Field(
        min_length=80,
        max_length=600,
        description="What motivates the candidate about this specific opportunity (2-3 sentences)",
    )
    who_am_i: str = Field(
        min_length=80,
        max_length=600,
        description="Brief paragraph about who you are - your background, education, and core identity as a professional (2-3 sentences)",
    )
    key_highlights: KeyHighlights = Field(
        description="Key highlights section with 3 categories, each with 3 bullet points"
    )
    approach_for_role_paragraph: str = Field(
        min_length=100,
        max_length=800,
        description="How the candidate would approach and contribute to the role (2-4 sentences)",
    )
    outro_paragraph: str = Field(
        min_length=50,
        max_length=400,
        description="Closing paragraph with call to action (1-2 sentences)",
    )
