# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_decide_editorial_correction.py

import logging
from typing import Literal
from src.core.graph_master.initialize_graph import CoverLetterGraphState

logger = logging.getLogger(__name__)


def decide_editorial_next_step(state: CoverLetterGraphState) -> Literal["reflection_cover_letter", "user_in_the_loop"]:
    """
    Decides whether to loop back for surgical revision or proceed to human review.

    Logic:
        - If violations exist AND under max_iterations → surgical revision via reflection node
        - If no violations OR hit max_iterations → proceed to human review

    Args:
        state (CoverLetterGraphState): Current graph state.

    Returns:
        str: "reflection_cover_letter" (surgical revision) or "user_in_the_loop" (exit loop)
    """
    violations = state.get("editorial_violations", [])
    iterations: int = state.get("iterations", 0)
    max_iterations: int = state.get("max_iterations", 3)

    has_violations = len(violations) > 0
    under_limit = iterations < max_iterations

    logger.info("=" * 80)
    logger.info("DECISION: Editorial routing")
    logger.info("  • Current iteration: %d / %d", iterations, max_iterations)
    logger.info("  • Violations: %d", len(violations))
    logger.info("  • Has violations: %s", has_violations)
    logger.info("  • Under limit: %s", under_limit)

    if has_violations and under_limit:
        logger.info("  → DECISION: Surgical revision via reflection_cover_letter")
        logger.info("=" * 80)
        return "reflection_cover_letter"
    else:
        if not has_violations:
            logger.info("  → DECISION: No violations - proceed to human review")
        else:
            logger.warning("  → DECISION: Max iterations reached - proceed despite %d violations", len(violations))
        logger.info("=" * 80)
        return "user_in_the_loop"
