"""
Zero Authority Witness — Render guard for reports

Strips or neuters potential exfiltration channels (markdown images/links,
HTML active content) when generating operator views.
"""

from __future__ import annotations

import re


def sanitize_for_display(text: str) -> str:
    # Turn markdown images and links into inert text
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '[image removed for safety]', text)
    text = re.sub(r'\[[^\]]+\]\((https?://[^)]+)\)', r'[\1] (link shown inert)', text)
    # Remove script tags if any HTML leaked through
    text = re.sub(r'<\s*script[^>]*>.*?</\s*script\s*>', '[script removed]', text, flags=re.I | re.S)
    return text
