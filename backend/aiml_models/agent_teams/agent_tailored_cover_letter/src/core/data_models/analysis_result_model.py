# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/data_models/analysis_result_model.py

from typing import Dict
from pydantic import BaseModel, Field

class JobAnalysisResult(BaseModel):
    company_name: str = Field(description="Identified company name")
    job_title: str = Field(description="Identified job title")
    analysis_output: str = Field(description="Analysis of the vacancy")
    employees_skills_requirement: Dict[str, bool]
    matching_skills: Dict[str, bool]
