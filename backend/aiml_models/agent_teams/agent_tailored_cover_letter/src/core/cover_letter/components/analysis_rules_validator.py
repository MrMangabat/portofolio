# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/components/analysis_rules_validator.py


from typing import List, Dict, Any
from src.core.data_models.analysis_result_model import JobAnalysisResult

class AnalysisRulesValidator:
    """
    Purpose:
        Validates the analysis result against forbidden words and sentences across multiple iterations.
        Supports progressive error tracking for self-correction.

    Capabilities:
        - Scans the analysis output for forbidden content.
        - Tracks all found issues per iteration.
        - Generates reflection instructions for self-correction.
        - Returns structured result instead of raising exceptions.

    Reasoning:
        This separates detection from logic flow.
        ✅ Easy to pass feedback into reflection loops.
        ✅ Supports time-series error analysis (how errors evolve over iterations).
    """

    def validate(self, analysis_result: JobAnalysisResult, forbidden_words: List[str], forbidden_sentences: List[str], iteration: int) -> Dict[str, Any]:
        """
        Validates the analysis output, tracks issues, and prepares correction feedback.

        Args:
            analysis_result: Structured result to validate.
            forbidden_words: List of forbidden words.
            forbidden_sentences: List of forbidden sentences.
            iteration: Current iteration number (for logging).

        Returns:
            Dict containing status, found issues, and reflection feedback.
        """
        issues = self._check_forbidden_content(analysis_result.analysis_output, forbidden_words, forbidden_sentences)

        if not issues["words"] and not issues["sentences"]:
            return {
                "status": "passed",
                "iteration": iteration,
                "found_issues": issues,
                "reflection": None
            }

        reflection = self._generate_reflection(issues)

        return {
            "status": "failed",
            "iteration": iteration,
            "found_issues": issues,
            "reflection": reflection
        }

    def _check_forbidden_content(self, text: str, forbidden_words: List[str], forbidden_sentences: List[str]) -> Dict[str, List[str]]:
        """
        Internal content scan, checks against words & sentences.
        """
        text_lower = text.lower()

        found_words = [word for word in forbidden_words if word.lower() in text_lower]
        found_sentences = [sentence for sentence in forbidden_sentences if sentence.lower() in text_lower]

        return {
            "words": found_words,
            "sentences": found_sentences
        }

    def _generate_reflection(self, issues: Dict[str, List[str]]) -> str:
        """
        Generates self-correction reflection instruction.
        """
        reflection = []
        if issues["words"]:
            reflection.append(f"Remove or replace these words: {', '.join(issues['words'])}.")
        if issues["sentences"]:
            reflection.append(f"Rephrase or remove these sentences: {', '.join(issues['sentences'])}.")
        
        reflection.append("Keep the meaning intact but ensure no forbidden language is present.")
        return " ".join(reflection)
