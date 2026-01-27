"""Profile analysis worker node (Tier 3)."""

import json
import logging

from langchain_core.messages import HumanMessage
from langsmith import traceable

from ...schemas import ProfileAnalysis
from ...state import State, load_master_data
from ..._llm_context import get_llm_service

logger = logging.getLogger(__name__)


@traceable(run_type="chain", name="Analyze Profile")
def analyze_profile(state: State) -> dict[str, object]:
    """Worker: Analyze candidate profile against job position.

    Reads profile data from master_data.json, uses LLM with structured output.
    """
    logger.info("[TIER 3] Analyzing candidate profile...")

    job_position: str = state.get("job_position", "")

    # Load from master_data.json (the database)
    master_data = load_master_data()
    profile_data: dict[str, object] = master_data.get("document_generation_officer", {})
    logger.debug("Loaded profile data with %d keys", len(profile_data))
    logger.debug("Job position length: %d chars", len(job_position))

    # Get LLM service
    llm_service = get_llm_service()
    structured_llm = llm_service.with_structured_output(ProfileAnalysis)

    prompt: str = f"""Analyze this job position and candidate profile.

!!! TASKS !!!
Provide a comprehensive analysis of the candidate's profile in relation to the job position.
- Identify and list relevant skills that match the job requirements.
- Identify and list relevant work experiences that align with the job duties.


JOB POSITION:
{job_position[:2000]}

CANDIDATE PROFILE:
{json.dumps(profile_data, indent=2)}"""

    try:
        analysis: ProfileAnalysis = structured_llm.invoke(prompt)
        if analysis is None:
            logger.warning("LLM returned None - check API key and model availability")
            # Create a default analysis
            analysis = ProfileAnalysis(
                required_skills=["Python", "AI/ML", "RAG"],
                relevant_skills=["Python", "RAG Systems", "NLP"],
                relevant_experience=["Data Science projects", "Software development"],
                skills_match={},
                reasoning_for_experience_selection="Default analysis due to LLM failure",
                summary="Profile matches key requirements",
            )
        logger.info(
            "LLM analysis: %d skills, %d experiences",
            len(analysis.relevant_skills),
            len(analysis.relevant_experience),
        )
        logger.debug("Reasoning: %s", analysis.reasoning_for_experience_selection)
        logger.debug("Summary: %s", analysis.summary)
    except Exception as e:
        logger.error("LLM analysis failed: %s", e)
        # Create a default analysis
        analysis = ProfileAnalysis(
            required_skills=["Python", "AI/ML", "RAG"],
            relevant_skills=["Python", "RAG Systems", "NLP"],
            relevant_experience=["Data Science projects", "Software development"],
            skills_match={},
            reasoning_for_experience_selection=f"Default analysis due to error: {e}",
            summary="Profile analysis unavailable - using defaults",
        )

    return {
        "messages": [HumanMessage(content=f"Profile analysis: {analysis.summary}")],
        "profile_data": {"raw": profile_data, "analysis": analysis.model_dump()},
    }
