"""
Zero Authority Witness — Tool / MCP Risk Classifier

Flags obvious high-risk capabilities mentioned in descriptors.
"""

from __future__ import annotations

import re
from typing import List, Dict

RISK_PATTERNS: Dict[str, str] = {
    "filesystem": r"read|write|file|path|~/.|secret|env|private",
    "network": r"http|url|fetch|request|upload|exfil",
    "shell": r"shell|exec|subprocess|command|os\.system",
    "auth": r"token|credential|password|api.?key|auth",
    "browser": r"browser|page|dom|cookie|localstorage",
    "memory": r"memory|context|history|previous",
    "repo": r"git|repo|clone|commit|push",
    "API": r"api|call|invoke|tool",
    "exfiltration": r"exfil|send|post|leak|steal",
    "policy_mutation": r"allowlist|greenlight|policy|trust|mark.*trusted|canonicalize",
}


def classify_descriptor(text: str) -> List[str]:
    text_l = text.lower()
    risks = []
    for risk, pat in RISK_PATTERNS.items():
        if re.search(pat, text_l):
            risks.append(risk)
    return sorted(set(risks))
