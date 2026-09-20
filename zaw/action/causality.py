"""
Zero Authority Witness — Provenance / taint tracing for proposed actions.

The question this answers is structural, not self-reported:

    do the consequential operands of this action (its target, parameters, url,
    body — NOT its free-text reason) quote or embed content the Witness captured
    from an untrusted source?

If they do, the action is being driven by untrusted evidence — exactly the
"external content becoming authority" event the kernel forbids. We decide this by
matching *significant* tokens (URLs, file paths, emails, identifier-like
literals) of the action's operands against the witnessed evidence + warning
corpus. We never read a field the action fills in about its own origin.

Blind spots (see CLAIM_BOUNDARY.md): this catches literal quoting / embedding.
An attacker who transforms evidence (encoding, paraphrase, concatenation) before
placing it in an operand can evade taint matching. The capability tier in the
gate is the backstop for that case — consequential capabilities require Operator
authorization regardless of whether taint was detected.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

_META_KEYS = {"reason", "requested_by", "source_ref", "persistence", "data_leaving_boundary"}

_URL = re.compile(r"https?://[^\s\"'<>)]+", re.IGNORECASE)
_PATH = re.compile(r"[~./][\w./~+-]{3,}")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_LOCATOR = re.compile(r"[/:@._\d-]")
_STRIP = ".,;:!?\"'()[]{}"


@dataclass
class TaintResult:
    tainted: bool = False
    matches: List[str] = field(default_factory=list)


def _is_significant(tok: str) -> bool:
    """A token worth matching: a locator/identifier, not a dictionary word.
    Avoids tainting on common words an answer would legitimately quote
    (e.g. 'refund', 'policy')."""
    tok = tok.strip().strip(_STRIP)
    if len(tok) < 6:
        return False
    if _LOCATOR.search(tok):
        return True
    return len(tok) >= 16


def _significant_tokens(text: str) -> Set[str]:
    toks: Set[str] = set()
    toks |= set(_URL.findall(text))
    toks |= set(_EMAIL.findall(text))
    toks |= set(_PATH.findall(text))
    for w in re.split(r"\s+", text):
        w = w.strip().strip(_STRIP)
        if _is_significant(w):
            toks.add(w)
    return {t.strip().lower() for t in toks if len(t.strip()) >= 6}


def _operand_text(action: Dict[str, Any]) -> str:
    parts: List[str] = []
    for k, v in action.items():
        if k in _META_KEYS:
            continue
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, (list, tuple)):
            parts.extend(str(x) for x in v)
        elif isinstance(v, dict):
            parts.extend(str(x) for x in v.values())
    return " ".join(parts)


def _evidence_corpus(evidence_packet: Dict[str, Any], warnings: Dict[str, Any]) -> str:
    lines: List[str] = []
    for item in (evidence_packet or {}).get("evidence", []) or []:
        t = item.get("text") if isinstance(item, dict) else None
        if isinstance(t, str):
            lines.append(t)
    for seg in (warnings or {}).get("instruction_like_segments", []) or []:
        t = seg.get("text") if isinstance(seg, dict) else None
        if isinstance(t, str):
            lines.append(t)
    return "\n".join(lines).lower()


def trace_taint(
    action: Dict[str, Any],
    evidence_packet: Dict[str, Any] | None,
    warnings: Dict[str, Any] | None,
) -> TaintResult:
    corpus = _evidence_corpus(evidence_packet or {}, warnings or {})
    if not corpus:
        return TaintResult(False, [])
    operand_tokens = _significant_tokens(_operand_text(action))
    matches = sorted(tok for tok in operand_tokens if tok in corpus)
    return TaintResult(bool(matches), matches)


def estimate_causality(action, evidence_packet, warnings) -> str:
    """Back-compatible label, now derived structurally (no self-report)."""
    return "untrusted_evidence" if trace_taint(action, evidence_packet, warnings).tainted else "unknown"
