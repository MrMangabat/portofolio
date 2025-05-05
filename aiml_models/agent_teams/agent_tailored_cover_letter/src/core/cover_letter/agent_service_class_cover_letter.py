# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/agent_service_class_cover_letter.py

from typing import Dict
from src.infrastructure.correction_client import CorrectionsClient
from src.core.cover_letter.components.cover_letter_prompt_builder import CoverLetterPromptBuilder
from src.core.cover_letter.components.cover_letter_parser import CoverLetterResultParser
from src.infrastructure.llm_client import LLMClient

from typing import Dict, Any
from src.infrastructure.correction_client import CorrectionsClient
from src.core.cover_letter.components.cover_letter_prompt_builder import CoverLetterPromptBuilder
from src.core.cover_letter.components.cover_letter_parser import CoverLetterResultParser
from src.infrastructure.llm_client import LLMClient

class AgentServiceClassCoverLetter:
    def __init__(
        self,
        corrections_client: CorrectionsClient,
        prompt_builder: CoverLetterPromptBuilder,
        response_parser: CoverLetterResultParser,
        llm_client: LLMClient
    ) -> None:
        self.corrections_client = corrections_client
        self.prompt_builder = prompt_builder
        self.response_parser = response_parser
        self.llm_client = llm_client

    def generate_cover_letter(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Purpose:
            Executes cover letter generation based on prior analysis, template match, and user CV.
        Capabilities:
            - Assembles all required context from the graph state.
            - Builds and runs the LLM prompt chain.
            - Returns updated state with cover letter output.
        Reasoning:
            Keeps prompt orchestration centralized and aligned with expected GraphState.
        """

        # Extract required fields from state
        job_description: str = state["job_description"]
        my_skills: list[str] = state["skills"]
        semilarity_jobtemplate: str = state["best_match_template_cover_letter"]
        analysis_output: Dict[str, Any] = state["analysis_output"]
        skills_match: Dict[str, bool] = state["matching_skills"]
        cv: str = state["cv"]
        personal_message: str = state.get("personal_message", "")
        not_wanted_words: list[str] = state["words_to_avoid"]
        not_wanted_sentences: list[str] = state["sentences_to_avoid"]

        # Build the prompt chain
        prompt_chain = (
            self.prompt_builder.build_prompt()
            | self.llm_client.get_model("gpt")
            | self.response_parser.parser.parser
        )

        # Invoke the chain with full context
        result = prompt_chain.invoke({
            "job_position": job_description,
            "my_skills": ", ".join(my_skills),
            "semilarity_jobtemplate": semilarity_jobtemplate,
            "analysis_output": analysis_output,
            "skills_match": skills_match,
            "cv": cv,
            "personal_message": personal_message,
            "not_wanted_words": ", ".join(not_wanted_words),
            "not_wanted_sentences": " ".join(not_wanted_sentences)
        })

        # Return updated state with generated output
        return {**state, "cover_letter_output": result}

