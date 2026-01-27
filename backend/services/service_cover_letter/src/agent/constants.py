"""Constants for CV Resume Builder.

Centralizes magic numbers, domain values, and configuration settings.
"""

# =============================================================================
# DATA LIMITS
# =============================================================================

# Prompt truncation limits
MAX_JOB_POSITION_LENGTH = 1500  # Max chars of job position to include in prompts

# Item limits for LLM context
MAX_EDUCATION_ITEMS = 3
MAX_PROJECTS_ITEMS = 3
MAX_SKILLS_PREVIEW = 20
# Note: Work experience has no limit - all experiences are sent to LLM


# =============================================================================
# SKILL DOMAINS
# =============================================================================


class SkillDomains:
    """Skill domain constants and normalization."""

    TECHNICAL = "technical"
    SOFT_SKILLS = "soft_skills"
    BUSINESS_TOOLS = "business_tools"

    ALL = {TECHNICAL, SOFT_SKILLS, BUSINESS_TOOLS}

    # Normalize inconsistent domain values
    NORMALIZER = {
        "soft_skill": SOFT_SKILLS,
        "soft_skills": SOFT_SKILLS,
        "technical": TECHNICAL,
        "business_tools": BUSINESS_TOOLS,
    }

    @classmethod
    def normalize(cls, domain: str) -> str:
        """Normalize a domain string to standard form."""
        return cls.NORMALIZER.get(domain, domain)


# =============================================================================
# LETTER CLOSINGS (Internationalization)
# =============================================================================

LETTER_CLOSINGS = {
    "da": "Med venlig hilsen,",
    "en": "Best regards,",
}


# =============================================================================
# LLM SETTINGS
# =============================================================================

LLM_TIMEOUT_SECONDS = 60  # Timeout for LLM API calls


# =============================================================================
# PDF LAYOUT CONSTANTS
# =============================================================================

# Marker shapes for timeline
VALID_MARKER_SHAPES = {"circle", "square", "diamond"}

# Diamond marker size (points)
DIAMOND_MARKER_SIZE = 4
