# backend/aiml_models/llm_agents/job_analysis.py

### External imports ###
import sys
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
### Internal imports ###
from prompt_templates.analyse_vacant_position_prompt import create_analysis_prompt
from utils import set_project_root



def initial_analysis_chain(some_input: str, some_skills: list[str], llm_model: ChatOpenAI, parser: PydanticOutputParser) -> dict:
    
    # pydantic_analysis_formatter = analysis_parser.get_format_instructions()  
    analysis_chain = create_analysis_prompt(skillsets=some_skills, job_to_apply=some_input) | llm_model | parser

    analysis_output = analysis_chain.invoke(
        {
            "job_position":some_input, 
            "my_skills":some_skills, 
            # "format_messages":pydantic_analysis_formatter
        }
    )

    return analysis_output

