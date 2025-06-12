from typing import Optional, List
from pydantic import BaseModel, Field

class ReflectedSection(BaseModel):
    """
    Represents a single reflected section with both the revised text and the rationale behind it.

    Purpose:
        Makes the reflection process transparent and auditable by including reasoning for each change.

    Capabilities:
        - Holds the updated content for a specific section.
        - Explains how and why it was changed during reflection.
    """
    content: str = Field(description="The updated section content after applying the reflection.")
    reflection_explanation: Optional[str] = Field(default=None, description="Explanation of what was changed and why.")

class ReflectResult(BaseModel):
    """
    Holds all reflected sections of a cover letter, including both content and reasoning.

    Purpose:
        Enables partial updates and makes the model’s corrections traceable and interpretable.

    Capabilities:
        - Each field is optional and only present if the section was flagged and regenerated.
        - Fully compatible with CoverLetterResult merging logic (via `.content` field).
    """
    introduction: Optional[ReflectedSection] = None
    motivation: Optional[ReflectedSection] = None
    unique_selling_points: Optional[ReflectedSection] = None
    bulletpoint_1: Optional[ReflectedSection] = None
    bulletpoint_2: Optional[ReflectedSection] = None
    bulletpoint_3: Optional[ReflectedSection] = None
    bulletpoint_4: Optional[ReflectedSection] = None
    thank_you: Optional[ReflectedSection] = None
