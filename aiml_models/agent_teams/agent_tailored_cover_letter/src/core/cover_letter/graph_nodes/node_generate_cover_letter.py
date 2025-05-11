# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_generate_cover_letter.py

from datetime import datetime
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from langgraph.graph import StateGraph

from src.core.cover_letter.agent_service_class_cover_letter import AgentServiceClassCoverLetter
from src.infrastructure.correction_client import CorrectionsClient
from src.core.cover_letter.components.cover_letter_prompt_builder import CoverLetterPromptBuilder
from src.core.cover_letter.components.cover_letter_parser import CoverLetterResultParser
from src.infrastructure.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)


def generate_cover_letter(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node for generating a personalized cover letter.

    Args:
        state (CoverLetterGraphState): Current LangGraph state, including job analysis, skills, CV, and user rules.

    Returns:
        CoverLetterGraphState: Updated state with generated cover letter content under key 'cover_letter_output'.
    """
    logger.info("COVER LETTER NODE: Generating Cover Letter")

    # Step 1: Instantiate the agent
    agent = AgentServiceClassCoverLetter(
        corrections_client=CorrectionsClient(),
        prompt_builder=CoverLetterPromptBuilder(),
        response_parser=CoverLetterResultParser(),
        llm_client=LLMClient()
    )

    result = agent.generate_cover_letter(state)

    # Step 2: Log messages
    logger.info("Generated result: introduction=%s, skills=%s, thank_you=%s", result.introduction, result.skills, result.thank_you)
    messages = state["messages"] + [
        ("system", f"[cover_letter_gen] Generated introduction: {result.introduction}"),
        ("system", f"[cover_letter_gen] Skills emphasis: {result.skills}"),
        ("system", f"[cover_letter_gen] Thank-you section: {result.thank_you}")
    ]

    # Step 3: Append to agent_trace
    trace = state.get("agent_trace", [])
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    trace.append(f"NODE: cover_letter_gen @ {timestamp}")

    # Step 4: Debug print
    logger.info("Iteration: %s", state['iterations'])
    logger.info("Introduction: %s", result.introduction)
    logger.info("Motivation: %s", result.motivation)
    logger.info("Thank you: %s", result.thank_you)
    logger.info("Agent Trace: %s", trace)
    logger.info("Finished generate_cover_letter node")

    return {
        **state,
        "generation": result,
        "cover_letter_output": result.dict(),
        "messages": messages,
        "agent_trace": trace,
    }
