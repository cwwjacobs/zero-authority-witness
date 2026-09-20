"""
Zero Authority Witness — Allow / Deny checker (Authority Membrane)

Returns one of: PASS, WARN, BLOCK, REQUIRES_OPERATOR_APPROVAL
"""

from __future__ import annotations

from typing import Dict, Any, Literal

Verdict = Literal["PASS", "WARN", "BLOCK", "REQUIRES_OPERATOR_APPROVAL"]


def check_allowed(action: Dict[str, Any], allow_manifest: Dict[str, Any]) -> Verdict:
    """
    Very simple first implementation.
    In a real deployment this would be far more sophisticated.
    """
    action_str = str(action).lower()

    denied = [d.lower() for d in allow_manifest.get("denied_actions", [])]
    for d in denied:
        if d in action_str:
            return "BLOCK"

    allowed = [a.lower() for a in allow_manifest.get("allowed_actions", [])]
    for a in allowed:
        if a in action_str:
            return "PASS"

    # If it touches anything that looks like mutation or private data, be cautious
    if any(k in action_str for k in ["secret", "private", "upload", "mutate", "allowlist", "greenlight", "policy"]):
        return "REQUIRES_OPERATOR_APPROVAL"

    return "WARN"
