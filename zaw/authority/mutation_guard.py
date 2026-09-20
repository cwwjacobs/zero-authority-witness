"""
Zero Authority Witness — Mutation Guard

Detects attempts (in content or proposed actions) to mutate protected structures.
"""

from __future__ import annotations

from typing import Dict, Any, List


MUTATION_KEYWORDS = [
    "change the allowlist",
    "mark .* trusted",
    "grant .* authority",
    "mutate policy",
    "mutate greenlight",
    "add to greenlight",
    "update kernel",
    "treat as system authority",
]


def detect_mutation_attempt(text_or_action: str | Dict[str, Any]) -> List[str]:
    s = str(text_or_action).lower()
    hits = []
    for kw in MUTATION_KEYWORDS:
        import re
        if re.search(kw, s, re.IGNORECASE):
            hits.append(kw)
    return hits


def guard_action(action: Dict[str, Any]) -> bool:
    """Return True if the action looks like a forbidden mutation attempt."""
    return bool(detect_mutation_attempt(action))
