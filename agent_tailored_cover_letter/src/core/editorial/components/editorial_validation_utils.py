# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/components/editorial_validation_utils.py

from typing import List

def normalize_text(text: str) -> str:
    return text.lower().strip()

def validate_words(do_not_use_words: List[str], component_value: str) -> List[str]:
    component_value_normalized = normalize_text(component_value)
    return [word for word in do_not_use_words if normalize_text(word) in component_value_normalized]

def invalid_sentences(sentences: List[str], context: str) -> List[str]:
    context_normalized = normalize_text(context)
    return [sentence for sentence in sentences if normalize_text(sentence) in context_normalized]
