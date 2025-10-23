from typing import Dict
from datetime import datetime
from langgraph.graph import StateGraph
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.core.editorial.agent_service_class_editorial import AgentServiceClassEditorial
from src.core.editorial.components.editorial_prompt_builder import EditorialPromptBuilder
from src.core.editorial.components.editorial_response_parser import EditorialResultParser
from src.infrastructure.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)


def validate_and_correct_editorial(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node for applying editorial validation with possible self-correction.

    Args:
        state (CoverLetterGraphState): LangGraph graph state.

    Returns:
        CoverLetterGraphState: Updated state with corrected generation.
    """
    logger.info("EDITORIAL AGENT: Running validation pass")

    # Timestamp for logging
    timestamp: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Unpack inputs from state
    job_description: str = state["job_description"]
    skills: list[str] = state["skills"]
    generation: str = state["generation"]
    violations: list[str] = state.get("editorial_error_messages", [])
    iteration: int = state["iterations"]

    # Run editorial agent — no state mutation
    agent = AgentServiceClassEditorial(
        prompt_builder=EditorialPromptBuilder(),
        response_parser=EditorialResultParser(),
        llm_client=LLMClient()
    )
    result = agent.validate_and_correct(
        job_description=job_description,
        skills=skills,
        generation=generation,
        editorial_violations=violations
    )

    # Prepare new trace entry (auto-accumulated via Annotated[List[str], add])
    new_trace = f"editorial_agent @ {timestamp}"

    # Prepare new violation log entry (auto-merged via Annotated[Dict, add_to_dict])
    new_log_entry = {
        f"iteration_{iteration}": {
            "timestamp": timestamp,
            "violations": state.get("editorial_violations", []),
            "generation_snapshot": generation,
        }
    }

    # Prepare system messages
    new_messages = [
        ("system", f"[editorial_agent] Iteration {iteration} completed at {timestamp}."),
        ("system", f"[editorial_agent] Violated rules: {state.get('editorial_violations', [])}")
    ]

    # Log last 3 iterations for inspection
    logger.info("Application generation completed, Iteration: %s", iteration)

    # Get current log for inspection (read-only)
    current_log = state.get("generation_violation_log", {})
    for i in range(iteration, max(iteration - 3, -1), -1):
        key = f"iteration_{i}"
        if key in current_log:
            logger.info("Snapshot %s: %s", key, current_log[key])

    # Return only new values (LangGraph auto-merges)
    return {
        "generation": result,
        "generation_violation_log": new_log_entry,
        "agent_trace": [new_trace],
        "messages": new_messages,
        "iterations": iteration + 1,  # Increment iteration counter after editorial pass
    }
