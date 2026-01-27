"""Agent module for CV/Cover Letter generation workflow.

This module contains the hierarchical supervisor agent for generating
tailored CVs and cover letters using a 4-tier architecture:
- Tier 1: Main Supervisor
- Tier 2: Officers (Research, Personality, Document)
- Tier 3: Workers
- Tier 4: Research Sub-agents
"""

from .graph_builder import build_graph
from .state import State, load_initial_state

__all__ = [
    "build_graph",
    "State",
    "load_initial_state",
]
