# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/components/editorial_prompt_builder.py

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.core.editorial.components.editorial_response_parser import EditorialResultParser


class EditorialPromptBuilder:
    """
    Purpose:
        Builds the LangChain prompt for the editorial agent responsible for correcting and validating a generated cover letter.

    Capabilities:
        - Provides LLM with the previous generation.
        - Injects validation errors (from rule violations) for the LLM to address.
        - Forces re-generation in the exact output structure expected.
    
    Reasoning:
        Keeps the editorial logic encapsulated and rule-driven.
    """

    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=EditorialResultParser().parser)
        self.format_instructions = self.parser.get_format_instructions()

    def build_prompt(self) -> ChatPromptTemplate:
        system_template = """
You are an editorial validator for AI-generated cover letters. Your role is to enforce language rules and correct the text *only* where violations occur.

You are provided with:
- The original job description
- A structured cover letter previously generated
- A list of editorial violations (word, sentence, phrasing issues)
- A set of user-defined banned terms and patterns
- A list of user-provided skills

Strict rules:
- DO NOT assume or hallucinate content not present in the CV or user input.
- DO NOT modify sections that are not flagged.
- DO NOT change the structure of the original generation.
- DO NOT exceed a 30% overlap between the CV and the cover letter.
- DO NOT fix tone unless it violates rules.
- DO NOT change the order of sections or output fields.

Language constraints:
- Rule 1: Remove boilerplate expressions
- Rule 2: Remove formulaic language
- Rule 3: Remove cliché phrases
- Rule 4: Remove overly self-assessing superlative claims
- Rule 5: Remove empty or evaluative assertions
- Rule 6: Remove paraphrastic suitability claims
- Rule 7: DO NOT use banned terms: {not_wanted_words}
- Rule 8: DO NOT use banned sentences or paraphrases: {not_wanted_sentences}

Your task:
1. Only update parts that violate the constraints.
2. Ensure corrected output is *functionally the same* (semantics preserved) but adheres to the language rules.
3. Maintain personal tone and grammatical fluency (IELTS C1+ level).
4. Return the output in **strictly the same structured format**.

{format_instructions}
        """

        SYSTEM_PROMPT = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_template,
                input_variables=[],
                partial_variables={"format_instructions": self.format_instructions}
            )
        )

        human_template = """
Job description: {job_description}
User skills: {my_skills}
Original generation (structured): {generation}

Please revise the generation strictly according to the rule violations.
Do not repeat previous mistakes or introduce hallucinated content.

Violation that occurred:
{editorial_error_messages}
        """

        HUMAN_PROMPT = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_template,
                input_variables=["job_description", "my_skills", "generation", "editorial_error_messages"]
            )
        )

        return ChatPromptTemplate(
            messages=[SYSTEM_PROMPT, HUMAN_PROMPT],
            input_variables=["job_description", "my_skills", "generation", "editorial_error_messages"]
        )