"""
Text processing and normalization utilities.
"""

import re
from typing import Dict, Any

def clean_text(text: str) -> str:
    """Normalize whitespace and strip unprintable characters."""
    if not text:
        return ""
    # Replace multiple spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)
    # Replace more than 3 consecutive newlines with 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def get_text_stats(text: str) -> Dict[str, Any]:
    """Calculate statistics such as word count, reading time, estimated tokens."""
    if not text:
        return {
            "char_count": 0,
            "word_count": 0,
            "est_tokens": 0,
            "read_time_mins": 0
        }
    
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    # Roughly 1 token ~ 4 characters in English
    est_tokens = max(1, char_count // 4)
    # Average reading speed: 200 words per minute
    read_time_mins = max(1, round(word_count / 200))

    return {
        "char_count": char_count,
        "word_count": word_count,
        "est_tokens": est_tokens,
        "read_time_mins": read_time_mins
    }

def truncate_text_for_ai(text: str, max_chars: int = 14000) -> (str, bool):
    """
    Truncate text if it exceeds max_chars to prevent context overflow.
    Returns (processed_text, was_truncated).
    """
    if len(text) <= max_chars:
        return text, False
    
    truncated = text[:max_chars]
    # Try to cut at the last paragraph or sentence
    last_break = truncated.rfind("\n\n")
    if last_break > max_chars * 0.8:
        truncated = truncated[:last_break]
    else:
        last_period = truncated.rfind(". ")
        if last_period > max_chars * 0.8:
            truncated = truncated[:last_period + 1]

    return truncated, True
