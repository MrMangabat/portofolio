# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_respose_parser.py

from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.analysis_result_model import JobAnalysisResult

class JobAnalysisResultParser:
    """
        Purpose:
            Defines how to parse the response from the LLM after analyzing a job vacancy.
            
        Capabilities:
            - Defines the expected output schema (JobAnalysisResult).
            - Provides a parser to transform the raw LLM response into this schema.
            
        Reasoning:
            Separating parsing logic ensures:
            ✅ Clear contract between LLM response and internal system.
            ✅ Easy updates if fields change.
            ✅ Standalone testability.
    """
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)

    def parse(self, llm_response: str) -> JobAnalysisResult:
        print(f"\n\nLLM response: {llm_response}")
        return JobAnalysisResult.model_validate_json(llm_response)
