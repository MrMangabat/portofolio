# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/data_models/cover_letter_model.py
from typing import Dict
from pydantic import BaseModel, Field

class CoverLetterResult(BaseModel):
    company_name: str = Field(description="Identified company name")
    job_title: str = Field(description="Identified job title")
    analysis_output: str = Field(description="Analysis of the vacancy")
    employees_skills_requirement: Dict[str, bool] = Field(description="Required skills and technical experience")
    matching_skills: Dict[str, bool] = Field(description="Matching skills between the job and the candidate")
    generated_cover_letter: str = Field(description="Generated cover letter")
    bulletpoint_1: str = Field(description="First bullet point")
    bulletpoint_2: str = Field(description="Second bullet point")
    bulletpoint_3: str = Field(description="Third bullet point")
    bulletpoint_4: str = Field(description="Fourth bullet point")
