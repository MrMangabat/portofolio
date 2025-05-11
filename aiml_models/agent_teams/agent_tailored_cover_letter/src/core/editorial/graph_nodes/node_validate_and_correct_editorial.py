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

    # Construct next state (mutate safely)
    updated_state: CoverLetterGraphState = {
        **state,
        "generation": result,
    }

    # Append log snapshot
    log = updated_state.get("generation_violation_log", {})
    log[f"iteration_{iteration}"] = {
        "timestamp": timestamp,
        "violations": state.get("editorial_violations", []),
        "generation_snapshot": generation,
    }
    updated_state["generation_violation_log"] = log

    # Append agent trace
    updated_state["agent_trace"] = (updated_state.get("agent_trace") or []) + [f"editorial_agent @ {timestamp}"]

    # Append system messages
    updated_state["messages"] += [
        ("system", f"[editorial_agent] Iteration {iteration} completed at {timestamp}."),
        ("system", f"[editorial_agent] Violated rules: {state.get('editorial_violations', [])}")
    ]

    # Log last 3 iterations for inspection
    logger.info("Application generation completed, Iteration: %s", iteration)

    for i in range(iteration, max(iteration - 3, -1), -1):
        key = f"iteration_{i}"
        if key in log:
            logger.info("Snapshot %s: %s", key, log[key])

    return updated_state
