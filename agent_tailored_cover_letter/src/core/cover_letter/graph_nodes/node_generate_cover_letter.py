# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_generate_cover_letter.py

from datetime import datetime
from typing import Dict, Any
from langchain_core.messages import AIMessage

from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.core.cover_letter.agent_service_class_cover_letter import AgentServiceClassCoverLetter
from src.core.cover_letter.components.cover_letter_prompt_builder import CoverLetterPromptBuilder
from src.core.cover_letter.components.cover_letter_parser import CoverLetterResultParser
from src.infrastructure.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)


def generate_cover_letter(state: CoverLetterGraphState) -> Dict[str, Any]:
    """
    LangGraph node to generate a personalized cover letter (initial generation only).

    Purpose:
        Converts job insights, user CV, skills, and preferences into a formal cover letter.
        This node handles ONLY initial generation. Revisions are handled by node_reflection_cover_letter.

    Capabilities:
        - Uses OOP service pattern (AgentServiceClassCoverLetter)
        - Enforces banned words/sentences
        - Logs detailed trace and appends AIMessage to conversation state
        - Returns structured CoverLetterResult

    Reasoning:
        Follows OOP microservice architecture pattern consistent with Node 2 (analyse_vacancy).
        Separation of concerns: generation vs. surgical revision.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    iteration = state.get("iterations", 0)

    logger.info("=" * 80)
    logger.info("NODE: node_generate_cover_letter - Starting initial cover letter generation")
    logger.info("Iteration: %s", iteration)
    logger.info("=" * 80)

    # 1️⃣ Build agent with OOP components
    logger.info("🆕 INITIAL GENERATION MODE: Creating cover letter from scratch")
    agent = AgentServiceClassCoverLetter(
        corrections_client=None,  # Not used in current flow
        prompt_builder=CoverLetterPromptBuilder(),
        response_parser=CoverLetterResultParser(),
        llm_client=LLMClient()
    )

    # 2️⃣ Run generation via service class
    logger.info("Invoking cover letter generation service...")
    updated_state = agent.agent_generate_cover_letter(state)
    result = updated_state["cover_letter_output"]

    # 3️⃣ Build AIMessage for trace
    out = (
        f"Company: {result.company_name}\n"
        f"Job Title: {result.job_title}\n"
        f"Intro: {result.introduction}\n"
        f"Motivation: {result.motivation}\n"
        f"USP: {result.unique_selling_points}\n"
        f"Thank you: {result.thank_you}"
    )
    updated_message = AIMessage(content=f"[CoverLetterGeneration]:\n{out}")
    updated_msgs = state.get("messages", []) + [updated_message]

    # 4️⃣ Add to revision history (mark as initial generation)
    new_revision_entry = {
        "iteration": iteration,
        "timestamp": timestamp,
        "cover_letter": result.dict() if hasattr(result, 'dict') else result,
        "revision_type": "initial",
    }

    # 5️⃣ Trace update
    new_trace = f"NODE: generate_cover_letter @ {timestamp} - Initial generation"
    logger.info("Adding trace: %s", new_trace)
    logger.info("=" * 20)
    logger.info("NODE: generate_cover_letter - Complete (Initial Generation)")
    logger.info("=" * 20)

    return {
        "cover_letter_output": result.dict() if hasattr(result, 'dict') else result,
        "generation": result,
        "messages": updated_msgs,
        "agent_trace": [new_trace],
        "cover_letter_revision_history": [new_revision_entry],
    }
