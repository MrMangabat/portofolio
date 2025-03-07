# File: src/core/company_analysis/components/post_processing_normalizer.py

from typing import Dict, Any
from src.core.data_models.analysis_result_model import JobAnalysisResult
import logging

class PostProcessingNormalizer:
    """
    Purpose:
        Ensures the final parsed JobAnalysisResult strictly matches expected schema.
        Fixes minor model drift issues (like casing, missing optional fields, etc.).
        Logs warning if normalization was required — signals potential LLM drift.

    Capabilities:
        - Fills missing fields with defaults (if ever needed).
        - Normalizes field names (optional, currently not applied).
        - Logs warnings if normalization applied (for audit trace).

    Reasoning:
        - Protects downstream systems from LLM drift.
        - Centralizes schema enforcement outside parsing (separation of concerns).
        - Makes agent more robust against future LLM changes.

    """
    def __init__(self) -> None:
        self.logger = logging.getLogger("PostProcessingNormalizer")

    def normalize(self, parsed_result: JobAnalysisResult) -> JobAnalysisResult:
        """
        Applies normalization rules (if any) and logs if applied.

        Args:
            parsed_result: Raw parsed JobAnalysisResult.

        Returns:
            JobAnalysisResult: Normalized and schema-compliant object.
        """
        normalized = parsed_result.model_copy(deep=True)  # Deep copy to avoid mutation

        # Example normalization — futureproofing for future schema evolution
        # (Right now, no change — but future fields/casing rules can go here)

        # Log if any normalization was applied (future-proof, always log check)
        if normalized != parsed_result:
            self.logger.warning("Normalization applied to parsed JobAnalysisResult. LLM outputstructure drift detected.")
        
        return normalized
