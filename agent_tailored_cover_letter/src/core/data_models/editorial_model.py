# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/data_models/editorial_model.py

from typing import List, Literal
from pydantic import BaseModel, Field


class RuleViolation(BaseModel):
    """
    Represents a single rule violation detected during editorial validation.
    """
    rule_id: Literal[
        "Rule 1", "Rule 2", "Rule 3", "Rule 4", "Rule 5",
        "Rule 6", "Rule 7", "Rule 8", "Rule 9", "Rule 10",
        "Language Rule 1", "Language Rule 2", "Language Rule 3",
        "Language Rule 4", "Language Rule 5", "Language Rule 6",
        "Language Rule 7", "Language Rule 8"
    ]
    section: Literal[
        "company_name", "job_title", "introduction", "motivation", 
        "skills", "continued_learning", "thank_you", "bullet_points"
    ]
    error_type: str  # e.g., "invalid_phrase", "hallucination"
    explanation: str  # Explanation of the issue in natural language


class EditorialResult(BaseModel):
    """
    Final corrected generation returned by the editorial agent.
    """
    company_name: str = Field(description="Company name extracted from job analysis.")
    job_title: str = Field(description="Job title extracted from job analysis.")
    introduction: str = Field(description="Corrected introduction paragraph.")
    motivation: str = Field(description="Corrected motivational paragraph linking user and company.")
    skills: str = Field(description="Corrected paragraph highlighting matching skills.")
    continued_learning: str = Field(description="Corrected paragraph showing willingness to learn.")
    bullet_points: List[str] = Field(description="List of corrected bullet points.")
    thank_you: str = Field(description="Corrected thank-you note section.")
    violated_rules: List[RuleViolation] = Field(description="All rule violations this generation fixed.")
