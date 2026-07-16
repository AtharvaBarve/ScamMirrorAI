"""Input validation and sanitization utilities."""

import html
import re
from typing import Optional


def sanitize_text_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize text input to prevent XSS and normalize content.

    Args:
        text: The input text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text string
    """
    if not isinstance(text, str):
        return ""

    text = text.strip().replace('\x00', '')

    # Limit length
    if len(text) > max_length:
        text = text[:max_length]

    # Basic HTML escaping to prevent XSS (though we're not rendering HTML directly,
    # this is good practice for any potential future web display)
    text = html.escape(text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def validate_text_input(text: str) -> tuple[bool, Optional[str]]:
    """
    Validate text input for basic quality checks.

    Args:
        text: The input text to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Text input cannot be empty"

    if len(text.strip()) < 3:
        return False, "Text input is too short (minimum 3 characters)"

    # Check for excessive repetition (potential spam/garbage)
    if len(text) > 10:
        # Check if more than 70% is the same character repeated
        if len(set(text)) < max(3, len(text) * 0.3):
            # Allow some repetition for things like "AAAAA" or "!!!"
            # but flag excessive repetition
            char_counts = {}
            for char in text:
                char_counts[char] = char_counts.get(char, 0) + 1

            max_count = max(char_counts.values()) if char_counts else 0
            if max_count > len(text) * 0.8:  # More than 80% same character
                return False, "Input contains excessive repetitive characters"

    return True, None


def validate_and_sanitize_text(text: str, max_length: int = 10000) -> tuple[str, Optional[str]]:
    """
    Validate and sanitize text input in one step.

    Args:
        text: The input text to process
        max_length: Maximum allowed length

    Returns:
        Tuple of (processed_text, error_message)
        If error_message is not None, processing failed and processed_text should be ignored
    """
    # Validate first
    is_valid, error_msg = validate_text_input(text)
    if not is_valid:
        return "", error_msg

    # Then sanitize
    sanitized = sanitize_text_input(text, max_length)
    return sanitized, None
