# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/data_models/editorial_model.py

from typing import List
from pydantic import BaseModel, Field

class EditorialResult(BaseModel):
    """
    Purpose:
        Defines the structure for the editorial agent's validated output of a cover letter.
    Capabilities:
        - Stores clean, corrected sections of the cover letter.
        - Used for validation, further loop corrections, and final output if all rules are met.
    Reasoning:
        Ensures modular structured content that can be validated independently or replaced selectively.
    """

    company_name: str = Field(escription="Company name extracted from job analysis.")
    job_title: str = Field(description="Job title extracted from job analysis.")
    introduction: str = Field(description="Corrected introduction paragraph.")
    motivation: str = Field(description="Corrected motivational paragraph linking user and company.")
    skills: str = Field(description="Corrected paragraph highlighting matching skills.")
    continued_learning: str = Field(description="Corrected paragraph showing willingness to learn.")
    bullet_points: List[str] = Field(description="List of corrected bullet points.")
    thank_you: str = Field(description="Corrected thank-you note section.")
