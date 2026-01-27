"""State definition for CV generation workflow."""

import json
import operator
import os
from typing import Annotated, TypedDict


class State(TypedDict):
    """State for CV generation workflow."""

    messages: Annotated[list, operator.add]  # Conversation history
    next: str  # Next node to route to
    current_officer: str  # Current officer handling the task
    job_position: str  # Raw job position text
    profile_data: dict  # Candidate profile information
    company_data: dict  # Company research results
    documents: dict  # Generated CV and Cover Letter
    feedback: dict  # User feedback and reflection


def get_master_data_path() -> str:
    """Get the path to master_data.json.

    Returns:
        str: Absolute path to master_data.json
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    return os.path.join(data_dir, "master_data.json")


def load_master_data() -> dict:
    """Load master_data.json.

    Returns:
        dict: The master data dictionary
    """
    master_data_path = get_master_data_path()
    with open(master_data_path, encoding="utf-8") as f:
        return json.load(f)


def load_initial_state(job_position: str) -> State:
    """Load initial state with job position and profile data.

    Args:
        job_position: The job position text (raw text, not a file path)

    Returns:
        State: Initial state dictionary with job position and profile data
    """
    # Load master_data.json
    master_data = load_master_data()

    return {
        "messages": [],
        "next": "",
        "current_officer": "",
        "job_position": job_position,
        "profile_data": master_data.get("document_generation_officer", {}),
        "company_data": {},
        "documents": {},
        "feedback": {},
    }
