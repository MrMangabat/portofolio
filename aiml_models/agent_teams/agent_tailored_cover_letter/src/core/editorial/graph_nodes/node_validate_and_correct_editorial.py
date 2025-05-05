# src/core/editorial/graph_nodes/node_validate_and_correct_editorial.py

from typing import Dict
from src.core.graph_master.master_graph_flow import CoverLetterGraphState
from langgraph.graph import StateGraph
from src.core.editorial.agent_serive_class_editorial import AgentServiceClassEditorial
from src.core.editorial.components.editorial_prompt_builder import EditorialPromptBuilder
from src.core.editorial.components.editorial_response_parser import EditorialResultParser
from src.infrastructure.llm_client import LLMClient


def validate_and_correct_editorial(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node for applying editorial validation with possible self-correction.

    Args:
        state (Dict): LangGraph graph state.

    Returns:
        Dict: Updated state with corrected generation.
    """
    print("----- EDITORIAL AGENT: Running validation pass -----")

    agent = AgentServiceClassEditorial(
        prompt_builder=EditorialPromptBuilder(),
        response_parser=EditorialResultParser(),
        llm_client=LLMClient()
    )
    # Run the agent and get updated state
    updated_state: Dict = agent.validate_and_correct(state)

    # Append logging info (before the update was applied)
    current_log = updated_state.get("editorial_violation_log", [])
    current_log.append({
        "iteration": updated_state["iterations"],
        "violations": updated_state.get("editorial_error_messages"),
        "generation_snapshot": state["generation"]
    })

    # Return the updated state with the extended log
    return {
        **updated_state,
        "editorial_violation_log": current_log
    }