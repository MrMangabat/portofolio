"""Document generation worker nodes (Tier 3)."""

import json
import logging
from datetime import datetime

from langchain_core.messages import HumanMessage
from langsmith import traceable

from ...constants import (
    LETTER_CLOSINGS,
    MAX_EDUCATION_ITEMS,
    MAX_JOB_POSITION_LENGTH,
    MAX_PROJECTS_ITEMS,
    MAX_SKILLS_PREVIEW,
    SkillDomains,
)
from ...schemas import CoverLetterContent, CVProfile
from ...state import State
from ...tools.helpers import is_danish, sanitize
from ...tools.pdf_generators import generate_cv_pdf_helper, generate_pdf
from ..._llm_context import get_llm_service

logger = logging.getLogger(__name__)


def _validate_state_for_documents(state: State) -> None:
    """Validate that state contains required keys for document generation.

    Args:
        state: The workflow state dict

    Raises:
        ValueError: If required keys are missing
    """
    required_keys = {"job_position", "profile_data"}
    missing = required_keys - set(state.keys())
    if missing:
        raise ValueError(f"State missing required keys: {missing}")


def _generate_cv_profile(
    job_position: str,
    analysis: dict[str, object],
    raw_profile: dict[str, object],
    use_danish: bool = False,
) -> str:
    """Generate a tailored CV profile paragraph using LLM.

    Args:
        job_position: The job posting text
        analysis: Profile analysis with relevant skills/experience
        raw_profile: Raw candidate profile data
        use_danish: Whether to write in Danish

    Returns:
        A tailored profile paragraph for the CV
    """
    language = "Danish" if use_danish else "English"
    llm_service = get_llm_service()
    structured_llm = llm_service.with_structured_output(CVProfile)

    education_items = raw_profile.get("education", [])[:MAX_EDUCATION_ITEMS]
    project_items = raw_profile.get("projects", [])[:MAX_PROJECTS_ITEMS]

    prompt = f"""Generate a professional CV profile paragraph tailored to this job position.

WRITE IN: {language}

JOB POSITION:
{job_position[:MAX_JOB_POSITION_LENGTH]}

CANDIDATE BACKGROUND:
- Education: {json.dumps(education_items, indent=2)}
- Relevant Skills: {analysis.get("relevant_skills", [])}
- Relevant Experience: {analysis.get("relevant_experience", [])}
- Key Projects: {json.dumps(project_items, indent=2)}

INSTRUCTIONS:
Write a 3-5 sentence professional profile paragraph for a CV. The profile should:
1. Open with the candidate's highest education (MSc Data Science) and core expertise areas
2. Highlight 1-2 specific practical experiences most relevant to THIS job position
3. Mention key technical strengths (e.g., specific technologies, methodologies)
4. Close with what type of role they're seeking and what they aim to contribute

Style guidelines:
- Write in third person implied (avoid "I" - use phrases like "Data Science graduate with...")
- Be specific and quantifiable where possible
- Match the tone to the job posting
- Keep it concise but impactful
"""

    try:
        result: CVProfile = structured_llm.invoke(prompt)
        return result.profile_text
    except (ValueError, RuntimeError, TypeError) as e:
        logger.warning("CV profile generation failed: %s", e)
        # Fallback to analysis summary
        return analysis.get("summary", "")


@traceable(run_type="chain", name="Generate Documents")
def generate_documents(state: State) -> dict[str, object]:
    """Worker: Generate Cover Letter using LLM with structured output.

    Uses the profile analysis and job position to generate tailored cover letter content.

    Args:
        state: Workflow state containing job_position and profile_data

    Returns:
        Updated state with generated cover letter in documents

    Raises:
        ValueError: If state is missing required keys
    """
    logger.info("Generating cover letter...")

    _validate_state_for_documents(state)

    job_position: str = state.get("job_position", "")
    profile_data: dict[str, object] = state.get("profile_data", {})
    analysis: dict[str, object] = profile_data.get("analysis", {})
    raw_profile: dict[str, object] = profile_data.get("raw", {})

    # If raw_profile is empty, use profile_data directly (for backwards compatibility)
    if not raw_profile:
        logger.warning("raw_profile not found, using profile_data instead")
        raw_profile = profile_data

    logger.debug(
        "Using analysis with %d relevant skills",
        len(analysis.get("relevant_skills", [])),
    )
    logger.debug("Job position length: %d chars", len(job_position))

    # Detect language
    use_danish = is_danish(job_position)
    language_instruction = "Write in Danish." if use_danish else "Write in English."
    language_code = "da" if use_danish else "en"
    logger.info("Language detected: %s", "Danish" if use_danish else "English")

    # Get LLM service and use structured output
    llm_service = get_llm_service()
    structured_llm = llm_service.with_structured_output(CoverLetterContent)

    skills_preview = raw_profile.get("skills", [])[:MAX_SKILLS_PREVIEW]
    work_experience = raw_profile.get("work_experience", [])  # No limit - show all

    prompt = f"""Generate a professional cover letter for this job application.

{language_instruction}

JOB POSITION:
{job_position}

CANDIDATE PROFILE ANALYSIS:
- Relevant Skills: {analysis.get("relevant_skills", [])}
- Relevant Experience: {analysis.get("relevant_experience", [])}
- Summary: {analysis.get("summary", "")}
- Reasoning: {analysis.get("reasoning_for_experience_selection", "")}

RAW PROFILE DATA:
- Personal Info: {json.dumps(raw_profile.get("personal_info", {}), indent=2)}
- Skills (top {MAX_SKILLS_PREVIEW}): {json.dumps(skills_preview, indent=2)}
- Work Experience: {json.dumps(work_experience, indent=2)}
- Education: {json.dumps(raw_profile.get("education", []), indent=2)}
- Projects: {json.dumps(raw_profile.get("projects", []), indent=2)}
- Certifications: {json.dumps(raw_profile.get("certifications", []), indent=2)}

INSTRUCTIONS:
1. Extract the company name from the job posting (e.g., "Nykredit", "Systematic", etc.)
2. {language_instruction}
3. intro_paragraph: Opening statement about interest in the role and why you're a good fit
4. motivation_paragraph: What motivates you about this specific opportunity
5. who_am_i: Brief paragraph about who you are - your background, education (MSc Data Science), and professional identity
6. key_highlights: Create exactly 3 categories with exactly 3 bullet points each
7. approach_for_role_paragraph: How you would approach and contribute to the role
8. outro_paragraph: Closing with call to action
9. Be specific and reference actual skills/experience from the profile
10. Keep paragraphs concise (2-4 sentences each)
11. Match the tone to the company culture implied by the job posting
"""

    logger.info("Invoking LLM for cover letter generation...")
    cover_letter: CoverLetterContent = structured_llm.invoke(prompt)
    logger.info("Generated cover letter for position: %s", cover_letter.position)

    # Get candidate name with validation
    personal_info = raw_profile.get("personal_info", {})
    candidate_name = personal_info.get("name") if personal_info else None
    if not candidate_name:
        logger.warning("No candidate name found in profile, using placeholder")
        candidate_name = "Candidate Name"

    # Build complete JSON for PDF generation
    application_data = {
        "personal_info": raw_profile.get("personal_info", {}),
        "social_profiles": raw_profile.get("social_profiles", []),
        **cover_letter.model_dump(),
        "signature": {
            "closing": LETTER_CLOSINGS.get(language_code, LETTER_CLOSINGS["en"]),
            "name": candidate_name,
        },
        "footer_note": "",
    }

    return {
        "messages": [
            HumanMessage(content=f"Generated cover letter for: {cover_letter.position}")
        ],
        "documents": {"cover_letter": application_data},
        "feedback": {"status": "generated"},
    }


@traceable(run_type="chain", name="Reflect on Output")
def reflect_on_output(state: State) -> State:
    """Worker: LLM self-critique.

    TODO: Implement reflection
    - Review generated documents
    - Check for consistency, grammar, formatting
    - Suggest improvements
    - Quality assurance
    """
    logger.info("Reflecting on output (placeholder)...")

    return {
        "messages": [HumanMessage(content="Reflected on generated documents")],
        "feedback": {},  # TODO: Populate with reflection feedback
    }


def _prepare_cv_data(
    raw_profile: dict[str, object],
    analysis: dict[str, object],
    position: str,
    profile_text: str = "",
    max_technical_skills: int = 20,
    max_soft_skills: int = 15,
) -> dict[str, object]:
    """Prepare CV data with title, profile, and filtered skills.

    Args:
        raw_profile: Raw profile data from master_data.json
        analysis: Profile analysis from LLM (contains relevant_skills)
        position: Job position title
        profile_text: Generated CV profile paragraph (if empty, uses analysis summary)
        max_technical_skills: Maximum number of technical skills to include
        max_soft_skills: Maximum number of soft skills to include

    Returns:
        Transformed CV data ready for PDF generation
    """
    cv_data = dict(raw_profile)  # Copy to avoid mutating original

    # 1. Set title from job position
    personal_info = dict(cv_data.get("personal_info", {}))
    personal_info["title"] = position
    cv_data["personal_info"] = personal_info

    # 2. Add profile - use generated profile or fall back to analysis summary
    cv_data["profile"] = profile_text if profile_text else analysis.get("summary", "")

    # 3. Filter skills by domain with separate limits
    all_skills = cv_data.get("skills", [])
    relevant_skill_names = set(analysis.get("relevant_skills", []))

    # Separate skills by domain
    technical_skills = []
    soft_skills = []

    for skill in all_skills:
        if not isinstance(skill, dict):
            continue
        skill_name = skill.get("name", "")
        domain = skill.get("domain", "technical")

        # Normalize domain value
        domain = SkillDomains.normalize(domain)

        # Check if skill is relevant (from analysis)
        is_relevant = skill_name in relevant_skill_names

        if domain in (SkillDomains.TECHNICAL, SkillDomains.BUSINESS_TOOLS):
            technical_skills.append((skill, is_relevant))
        elif domain == SkillDomains.SOFT_SKILLS:
            soft_skills.append((skill, is_relevant))

    # Sort each group: relevant skills first, then by proficiency
    def sort_key(item: tuple) -> tuple:
        skill, is_relevant = item
        return (not is_relevant, -skill.get("proficiency", 0))

    technical_skills.sort(key=sort_key)
    soft_skills.sort(key=sort_key)

    # Take top N from each domain
    filtered_skills = []
    filtered_skills.extend([s for s, _ in technical_skills[:max_technical_skills]])
    filtered_skills.extend([s for s, _ in soft_skills[:max_soft_skills]])

    cv_data["skills"] = filtered_skills

    return cv_data


@traceable(run_type="chain", name="User Review & PDF Generation")
def user_review(state: State) -> State:
    """Worker: Finalize documents and generate PDFs.

    Generates both cover letter and CV PDFs directly from data (no JSON files).
    Saves to: src/data/pdf/not_applied_yet/{company}/
        - {company}_{position}_{name}_{date}.pdf (cover letter)
        - {company}_cv_{name}_{date}.pdf (CV)

    Args:
        state: Workflow state containing documents and profile_data

    Returns:
        Updated state with PDF paths in feedback
    """
    logger.info("Finalizing documents and generating PDFs...")

    documents = state.get("documents", {})
    cover_letter_data = documents.get("cover_letter", {})
    profile_data = state.get("profile_data", {})
    raw_profile = profile_data.get("raw", {})
    analysis = profile_data.get("analysis", {})

    if not cover_letter_data:
        logger.warning("No cover letter data found in state")
        return {
            "messages": [HumanMessage(content="No documents to finalize")],
            "feedback": {"status": "error", "message": "No cover letter data"},
        }

    # Extract data for filename
    company = cover_letter_data.get("company_name", "unknown")
    position = cover_letter_data.get("position", "application")
    name = cover_letter_data.get("personal_info", {}).get("name", "unknown")
    date_str = datetime.now().strftime("%Y%m%d")

    cover_letter_pdf_path = None
    cv_pdf_path = None

    try:
        # Generate cover letter PDF
        cover_letter_output = (
            f"{sanitize(company)}_{sanitize(position)}_{sanitize(name)}_{date_str}"
        )
        logger.info("Cover letter filename: %s.pdf", cover_letter_output)
        cover_letter_pdf_path = generate_pdf(
            cover_letter_data, company, cover_letter_output
        )
        logger.info("Cover letter PDF generated: %s", cover_letter_pdf_path)

        # Generate CV PDF using prepared data with title, profile, and filtered skills
        if raw_profile:
            # Generate tailored CV profile using LLM
            job_position = state.get("job_position", "")
            use_danish = is_danish(job_position) if job_position else False
            logger.info("Generating tailored CV profile...")
            cv_profile = _generate_cv_profile(
                job_position, analysis, raw_profile, use_danish
            )
            logger.info("CV profile generated: %d chars", len(cv_profile))

            cv_data = _prepare_cv_data(
                raw_profile, analysis, position, profile_text=cv_profile
            )
            cv_output = f"{sanitize(company)}_cv_{sanitize(name)}_{date_str}"
            logger.info("CV filename: %s.pdf", cv_output)
            logger.debug(
                "CV title: %s", cv_data.get("personal_info", {}).get("title", "N/A")
            )
            logger.debug("CV skills: %d filtered skills", len(cv_data.get("skills", [])))
            cv_pdf_path = generate_cv_pdf_helper(cv_data, company, cv_output)
            logger.info("CV PDF generated: %s", cv_pdf_path)
        else:
            logger.warning("No raw profile data found, skipping CV generation")

        return {
            "messages": [
                HumanMessage(
                    content=f"Generated PDFs: {cover_letter_pdf_path}, {cv_pdf_path}"
                )
            ],
            "feedback": {
                "status": "completed",
                "cover_letter_pdf": cover_letter_pdf_path,
                "cv_pdf": cv_pdf_path,
            },
        }
    except (OSError, IOError, ValueError) as e:
        logger.error("PDF generation failed: %s", e, exc_info=True)
        return {
            "messages": [HumanMessage(content=f"PDF generation failed: {e}")],
            "feedback": {"status": "error", "message": str(e)},
        }
