# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_respose_parser.py
import re
import json

from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.analysis_result_model import JobAnalysisResult


class JobAnalysisResultParser:
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)

