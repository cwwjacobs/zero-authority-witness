"""
Zero Authority Witness — Capability classifier (Authority Membrane)

Deterministically maps a proposed action — or a Greenlight phrase — to a set of
capability tags, based on its concrete operands (action_type, target, parameter
values), NOT on any self-description of intent in a free-text reason.

The same lexicon classifies what an action *does* and what a Greenlight
*allows / forbids*, so scope checks compare like with like.

This is pattern matching, not semantic understanding (see CLAIM_BOUNDARY.md). It
is intentionally conservative: when in doubt it tags more, which pushes the gate
toward REQUIRES_OPERATOR_APPROVAL / BLOCK, never toward a silent PASS. It cannot
distinguish a benign path from a dangerous one of the same capability kind
(path-level scope is a known blind spot).
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Set

# capability tag -> regex matched against lowercased operand text
CAPABILITY_PATTERNS: Dict[str, str] = {
    "instruction_execution": (
        r"treat\s+.*\bas\b\s+(system|developer|instruction|authority)"
        r"|follow\s+(the\s+)?instructions?"
        r"|do\s+what\s+(this|it|the\s+page|the\s+content)\s+says"
        r"|as\s+system\s+authority|\bobey\b"
    ),
    "state_mutation": (
        r"allowlist|allow[_\s-]?manifest|greenlight|canonical|\bpolicy\b|\bkernel\b"
        r"|mark\s+.*\btrust|grant\s+.*\bauthorit|add\s+.*\b(allow|trust)|\bmutate\b"
        r"|escalate\s+privile"
    ),
    "secret_access": (
        r"\.ssh\b|id_rsa|id_ed25519|\.pem\b|\.env\b|\.aws\b|\bcredential|\bsecret"
        r"|\bpassword|api[_-]?key|\btoken\b|\.netrc|git-credentials|keychain"
        r"|private[_-]?key|/etc/(shadow|passwd)|/etc/|/proc/|/sys/"
        r"|\.bash_history|\.zsh_history"
    ),
    "data_egress": (
        r"https?://|\bupload\b|\bexfil|\bpost\b|\bsend\b|webhook|\bfetch\b|outbound"
        r"|\bemail\b|\bcurl\b|\bwget\b|\bpush\b"
    ),
    "code_execution": (
        r"\bexec\b|\beval\b|\bshell\b|subprocess|os\.system|\bspawn\b|/bin/(sh|bash)"
        r"|powershell|\bsystem\("
    ),
    "filesystem_write": r"\bwrite\b|\bappend\b|\bdelete\b|\brm\b|\bmv\b|chmod|chown|truncate|overwrite|\bunlink\b",
    "filesystem_read": r"\bread\b|\bcat\b|\bopen\b|\bload\b|\bdownload\b|file://",
}

SEVERITY: Dict[str, str] = {
    "instruction_execution": "high",
    "state_mutation": "high",
    "secret_access": "high",
    "data_egress": "high",
    "code_execution": "high",
    "filesystem_write": "medium",
    "filesystem_read": "medium",
}

_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}
_RANK_NAME = {v: k for k, v in _RANK.items()}

# Free-text narration the action writes about itself is excluded from capability
# classification; it is not a trustworthy operand. (mutation_guard still scans the
# whole action separately for direct mutation phrasing.)
_META_KEYS = {"reason", "requested_by", "source_ref"}


def _operand_text(action: Dict[str, Any]) -> str:
    parts: List[str] = []
    at = action.get("action_type")
    if isinstance(at, str):
        parts.append(at)
    tgt = action.get("target")
    if isinstance(tgt, str):
        parts.append(tgt)
    for k, v in action.items():
        if k in _META_KEYS or k in ("action_type", "target"):
            continue
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, (list, tuple)):
            parts.extend(str(x) for x in v)
        elif isinstance(v, dict):
            parts.extend(str(x) for x in v.values())
    return " ".join(parts)


def classify_text(text: str) -> Set[str]:
    t = text.lower()
    # also search an underscore-normalized copy so "http_post" -> "http post"
    t = t + " " + t.replace("_", " ")
    return {cap for cap, pat in CAPABILITY_PATTERNS.items() if re.search(pat, t)}


def classify_action(action: Dict[str, Any]) -> Set[str]:
    caps = classify_text(_operand_text(action))
    if action.get("data_leaving_boundary") is True:
        caps.add("data_egress")
    return caps


def classify_phrases(phrases: Iterable[str]) -> Set[str]:
    caps: Set[str] = set()
    for p in phrases or []:
        if isinstance(p, str):
            caps |= classify_text(p)
    return caps


def severity(caps: Iterable[str]) -> str:
    rank = max((_RANK[SEVERITY.get(c, "low")] for c in caps), default=0)
    return _RANK_NAME[rank]
