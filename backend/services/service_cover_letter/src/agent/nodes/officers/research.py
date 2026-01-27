"""Research & Analysis Officer node (Tier 2)."""

import logging

from langchain_core.messages import HumanMessage
from langsmith import traceable

from ...state import State

logger = logging.getLogger(__name__)


@traceable(run_type="chain", name="Research Analysis Officer")
def research_analysis_officer(state: State) -> State:
    """Research & Analysis Officer: Manages M&A due diligence sub-agents.

    TODO: Implement intelligent routing for 4 sub-agents
    - Financial Analyst (financial DD)
    - Business Intelligence Analyst (business model DD)
    - Company Profile Analyst (people/culture DD)
    - Macro Officer (industry/macro DD)
    - Coordinate parallel or sequential execution
    """
    logger.info("[TIER 2] Research & Analysis Officer delegating DD tasks...")

    # Simplified routing (TODO: make intelligent)
    # In real implementation, could run sub-agents in parallel
    if not state.get("company_data"):
        # Start with financial analysis
        next_worker = "financial_analyst"
    else:
        # All DD complete, report back
        next_worker = "report_to_supervisor"

    return {
        "next": next_worker,
        "current_officer": "research_analysis_officer",
        "messages": [
            HumanMessage(content=f"Research Officer routing to: {next_worker}")
        ],
    }
