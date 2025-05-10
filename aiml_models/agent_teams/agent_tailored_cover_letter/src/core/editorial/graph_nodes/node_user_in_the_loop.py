# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_human_in_the_loop.py

from datetime import datetime
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from langgraph.graph import StateGraph

def user_in_the_loop(state: CoverLetterGraphState) -> StateGraph:
    """
    Placeholder node to simulate a human review step in the pipeline.

    Args:
        state (CoverLetterGraphState): The full graph state.

    Returns:
        CoverLetterGraphState: State passed through without modification.
    """
    timestamp: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    state["agent_trace"] = (state.get("agent_trace") or []) + [f"human_in_the_loop @ {timestamp}"]
    state["messages"] += [("system", f"[human_in_the_loop] Review passed at {timestamp}.")]

    print("------ HUMAN REVIEW PLACEHOLDER PASSED ------")
    return state
