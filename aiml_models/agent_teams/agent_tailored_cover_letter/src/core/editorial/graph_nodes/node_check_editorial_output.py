# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_check_editorial_output.py

from typing import Dict
from langgraph.graph import StateGraph
from src.core.editorial.components.editorial_validation_utils import validate_words, invalid_sentences


def check_editorial_generation(state: Dict) -> StateGraph:
    """
    LangGraph-compatible validation node that checks for forbidden words and sentences in the editorial output.

    Args:
        state (Dict): Current graph state, must include 'generation', 'words_to_avoid', 'sentences_to_avoid'.

    Returns:
        Dict: Updated state with 'error' flag and possible editorial_error_messages.
    """
    generation = state["generation"]
    no_go_words = state["words_to_avoid"]
    no_go_sentences = state["sentences_to_avoid"]
    iterations = state["iterations"]
    messages = state["messages"]

    print("-------- VALIDATION: EDITORIAL LANGUAGE RULES --------")

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

    if violations:
        print("--- RULE VIOLATIONS DETECTED ---")
        return {
            **state,
            "error": "yes",
            "editorial_error_messages": violations,
            "iterations": iterations + 1,
            "messages": messages,  # unchanged
        }
    else:
        print("--- NO VIOLATIONS ---")
        return {
            **state,
            "error": "no",
            "editorial_error_messages": [],
            "iterations": iterations + 1,
            "messages": messages,
        }
