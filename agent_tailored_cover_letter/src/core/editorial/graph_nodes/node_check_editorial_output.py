# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_check_editorial_output.py

from datetime import datetime
from typing import Dict
from langgraph.graph import StateGraph
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.core.editorial.components.editorial_validation_utils import validate_words, invalid_sentences
import logging

logger = logging.getLogger(__name__)


def check_editorial_generation(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph-compatible validation node that checks for forbidden words and sentences
    in the editorial output using user-defined rules.

    Args:
        state (CoverLetterGraphState): Current graph state.

    Returns:
        StateGraph: Updated state with validation error flag and messages.
    """
    logger.info("VALIDATION: EDITORIAL LANGUAGE RULES started")

    generation = state["generation"]
    no_go_words = state["words_to_avoid"]
    no_go_sentences = state["sentences_to_avoid"]
    iterations = state["iterations"]
    messages = state["messages"]

    # Structure generation content
    generation_components = {
        "company_name": generation.company_name,
        "introduction": generation.introduction,
        "job_title": generation.job_title,
        "motivation": generation.motivation,
        "skills": generation.skills,
        "continued_learning": generation.continued_learning,
        "thank_you": generation.thank_you,
        "bullet_points": " ".join(generation.bullet_points),
    }

    violations: list[str] = []

    for section, content in generation_components.items():
        try:
            validate_words(no_go_words, content)
        except ValueError as ve:
            violations.append(f"[{section}] Invalid words: {ve}")

        try:
            invalid_sentences(no_go_sentences, content)
        except ValueError as ve:
            violations.append(f"[{section}] Invalid sentences: {ve}")

    # Timestamp for trace
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    trace = state.get("agent_trace", [])
    trace.append(f"NODE: check_editorial_output @ {timestamp}")

    # Append system message
    new_msg = ("system", f"[editorial_validator] Iteration {iterations} checked {len(generation_components)} sections. Violations: {len(violations)}")

    updated_messages = messages + [new_msg]

    # Log validation results
    logger.info("Iteration: %s", iterations)
    logger.info("Violations found: %s", violations)
    for v in violations:
        logger.info("Violation detail: %s", v)
    logger.info("Trace: %s", trace)
    logger.info("Finished VALIDATION node")

    return {
        **state,
        "error": "yes" if violations else "no",
        "editorial_error_messages": violations,
        "iterations": iterations + 1,
        "messages": updated_messages,
        "agent_trace": trace,
    }
