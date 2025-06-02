# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/components/cover_letter_parser.py

from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.cover_letter_model import CoverLetterResult


class CoverLetterResultParser:
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=CoverLetterResult)

