import re


def clean_content(text: str, max_chars: int = 2000) -> str:
    """
    Cleans raw web content — removes extra whitespace,
    HTML artifacts, and trims to a readable length.
    """
    if not text:
        return ""

    # remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()

    # trim to max length to avoid token overflow
    if len(text) > max_chars:
        text = text[:max_chars] + "..."

    return text