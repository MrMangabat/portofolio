# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/data_models/cover_letter_model.py
from typing import Dict
from pydantic import BaseModel, Field

class CoverLetterResult(BaseModel):
    company_name: str = Field(description="Identified company name")
    job_title: str = Field(description="Identified job title")
    introduction: str = Field(description="Introduction section of the cover letter")
    motivation: str = Field(description="Motivation section of the cover letter")
    unique_selling_points: str = Field(description="Unique selling points section of the cover letter")
    thank_you: str = Field(description="Thank you section of the cover letter")
