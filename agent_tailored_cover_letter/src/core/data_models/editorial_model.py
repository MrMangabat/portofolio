# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/data_models/editorial_model.py

from typing import List, Literal
from pydantic import BaseModel, Field


class RuleViolation(BaseModel):
    """
    Represents a single rule violation detected during editorial validation.

    Simplified to only track banned words and sentences.
    """
    rule_id: Literal["banned_word", "banned_sentence"] = Field(
        description="Type of violation: banned_word or banned_sentence"
    )
    section: Literal[
        "company_name", "job_title", "introduction", "motivation",
        "unique_selling_points",
        "thank_you"
    ] = Field(
        description="Section of the cover letter where the violation occurred"
    )
    offending_text: str = Field(
        description="Exact literal span from the draft that caused the violation."
    )
    explanation: str = Field(
        description="Concise natural-language reason (≤ 50 words)."
    )


class EditorialResult(BaseModel):
    """
    Editorial validation result returned by the audit node.

    Simplified to only contain violations for banned words and sentences.
    """
    violated_rules: List[RuleViolation] = Field(
        description="All banned word/sentence violations detected in this generation."
    )
