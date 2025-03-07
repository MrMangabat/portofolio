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


class JobAnalysisResultParser:
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)

    def parse(self, llm_response: str) -> JobAnalysisResult:
        print("\n🛠️ Raw LLM Response (Before Parsing):")
        print(f"RAW TEXT: {llm_response}")
        # The parser will strip markdown wrappers, trailing junk, and more
        return self.parser.parse(llm_response)
