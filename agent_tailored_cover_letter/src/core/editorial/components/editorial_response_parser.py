# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/components/editorial_response_parser.py

from langchain_core.output_parsers import PydanticOutputParser
from src.core.data_models.editorial_model import EditorialResult


class EditorialResultParser:
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=EditorialResult)

