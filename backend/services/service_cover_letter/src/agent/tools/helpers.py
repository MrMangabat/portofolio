"""Helper utility functions for CV Resume Builder."""


def is_danish(text: str) -> bool:
    """Detect if text is primarily in Danish using common word heuristics.

    Args:
        text: Text to analyze

    Returns:
        bool: True if text appears to be Danish
    """
    danish_words = [
        "og",
        "til",
        "med",
        "vi",
        "har",
        "din",
        "dine",
        "skal",
        "kan",
        "vil",
        "er",
        "at",
        "en",
        "det",
        "de",
        "som",
        "på",
        "for",
        "ikke",
        "af",
    ]
    text_lower = text.lower()
    matches = sum(1 for word in danish_words if f" {word} " in f" {text_lower} ")
    return matches >= 3


def sanitize(text: str, max_len: int = 30) -> str:
    """Sanitize text for use in filenames.

    Args:
        text: Text to sanitize
        max_len: Maximum length of output string

    Returns:
        str: Sanitized string safe for filenames
    """
    clean = "".join(c if c.isalnum() else "_" for c in text)
    return clean.lower().strip("_")[:max_len]
