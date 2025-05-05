# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_decide_editorial_correction.py

from typing import Dict
from src.core.graph_master.master_graph_flow import GraphState

MAX_EDITORIAL_ITERATIONS: int = 2  # Can be configured later


def decide_editorial_next_step(state: Dict) -> str:
    """
    Decides whether to loop back to editorial correction or move to the final step.

    Args:
        state (Dict): Current graph state.

    Returns:
        str: Name of the next node ("validate_and_correct_editorial" or "finalize_output").
    """
    error: str = state["error"]
    iterations: int = state["iterations"]

    if error == "no" or iterations >= MAX_EDITORIAL_ITERATIONS:
        print("--- DECISION: Editorial complete, proceed to finalize ---")
        return "finalize_output"
    else:
        print("--- DECISION: Editorial failed, retrying... ---")
        return "validate_and_correct_editorial"
