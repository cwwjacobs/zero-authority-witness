"""
Zero Authority Witness — Action Gate (Authority Membrane)

Decides a proposed action with a deterministic, default-deny policy built from
two independent axes plus the mutation guard:

  * capability  — what the action's concrete operands would actually DO
                  (zaw/authority/capability.py), never its self-description.
  * provenance  — whether those operands trace to witnessed untrusted evidence
                  (zaw/action/causality.py), by structural token match, not by a
                  self-reported source label.
  * mutation    — direct attempts to mutate protected authority/state
                  (zaw/authority/mutation_guard.py).
  * binding     — when an action depends on a witnessed/fetched tool
                  descriptor, the descriptor's digest is re-checked at action
                  time against the witness-time binding and any change is
                  rejected (zaw/tools/descriptor_binding.py, TOCTOU).

Verdicts: PASS / WARN / BLOCK / REQUIRES_OPERATOR_APPROVAL.

Authority is granted only by the Operator's Greenlight; nothing here promotes
evidence to authority. A high-consequence action is never silently PASSed — at
most WARN when it is explicitly within Greenlight and untainted. See
AUTHORITY_MODEL.md and FORBIDDEN_PROMOTIONS.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal

from ..authority import capability as _cap
from ..authority import mutation_guard as _mut
from ..tools import descriptor_binding as _binding
from . import causality as _causality

Verdict = Literal["PASS", "WARN", "BLOCK", "REQUIRES_OPERATOR_APPROVAL"]

_HIGH = "high"
_MEDIUM = "medium"


@dataclass
class ActionDecision:
    verdict: Verdict
    reasons: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    tainted: bool = False
    taint_matches: List[str] = field(default_factory=list)
    severity: str = "none"
    descriptor_binding: Dict[str, Any] | None = None


def evaluate_action(
    action: Dict[str, Any],
    greenlight: Dict[str, Any] | None = None,
    warnings: Dict[str, Any] | None = None,
    evidence_packet: Dict[str, Any] | None = None,
    descriptor_binding: Dict[str, Any] | None = None,
) -> ActionDecision:
    greenlight = greenlight or {}
    caps = _cap.classify_action(action)
    sev = _cap.severity(caps)
    taint = _causality.trace_taint(action, evidence_packet, warnings)
    mutation_hits = _mut.detect_mutation_attempt(action)

    allowed_caps = _cap.classify_phrases(greenlight.get("allowed", []))
    # Only the high-severity capability of a not_allowed phrase is treated as a
    # prohibition, so "read secrets" forbids secret_access without also
    # forbidding every benign read.
    forbidden_caps = {
        c for c in _cap.classify_phrases(greenlight.get("not_allowed", []))
        if _cap.SEVERITY.get(c, "low") == _HIGH
    }

    d = ActionDecision(
        verdict="REQUIRES_OPERATOR_APPROVAL",
        capabilities=sorted(caps),
        tainted=taint.tainted,
        taint_matches=taint.matches,
        severity=sev,
    )

    # --- BLOCK rules (forbidden promotions / kernel violations), first match wins ---

    # 0. TOCTOU binding: an action that depends on a witnessed/fetched tool
    #    descriptor is gated on that descriptor's bound identity. A changed,
    #    stale, mismatched, or unbound descriptor is rejected — the action would
    #    otherwise be authorized by a descriptor that no longer exists as witnessed.
    if action.get("descriptor") is not None or descriptor_binding is not None:
        binding_result = _binding.verify_descriptor_binding(action, descriptor_binding)
        d.descriptor_binding = {
            "descriptor_source": action.get("descriptor"),
            "bound_digest": binding_result.bound_digest,
            "current_digest": binding_result.current_digest,
            "verification": binding_result.status,
        }
        if not binding_result.verified:
            d.verdict = "BLOCK"
            d.reasons.append(
                f"Descriptor binding failed ({binding_result.status}): {binding_result.detail}"
            )
            return d

    # 1. Direct attempt to mutate protected authority/state.
    if "state_mutation" in caps or mutation_hits:
        d.verdict = "BLOCK"
        d.reasons.append(
            "Proposes to mutate protected authority/state "
            "(allowlist / Greenlight / policy / trust / kernel). Forbidden promotion."
        )
        if mutation_hits:
            d.reasons.append(f"Mutation-guard matched: {', '.join(sorted(set(mutation_hits)))}.")
        return d

    # 2. Treating untrusted content as instruction is the kernel violation itself.
    if "instruction_execution" in caps:
        d.verdict = "BLOCK"
        d.reasons.append("Proposes to treat untrusted content as instruction / authority.")
        return d

    # 3. Operator explicitly prohibited this capability in the Greenlight.
    blocked_by_gl = caps & forbidden_caps
    if blocked_by_gl:
        d.verdict = "BLOCK"
        d.reasons.append(f"Capability {sorted(blocked_by_gl)} is in Greenlight not_allowed.")
        return d

    # 4. Untrusted provenance driving a consequential action = external content
    #    becoming authority over a side effect.
    if taint.tainted and sev == _HIGH:
        d.verdict = "BLOCK"
        d.reasons.append(
            "A high-capability operand traces to witnessed untrusted evidence "
            f"({', '.join(taint.matches[:3])}). Evidence may not drive consequential actions."
        )
        return d

    # 5. Read-secret + move-data-off-boundary is the canonical exfiltration shape.
    if "secret_access" in caps and "data_egress" in caps:
        d.verdict = "BLOCK"
        d.reasons.append("Reads secret material and moves data off-boundary in one action.")
        return d

    # --- non-BLOCK tail: choose a verdict, then apply the persistence floor ---

    if sev == _HIGH:
        if caps <= allowed_caps and not taint.tainted:
            d.verdict = "WARN"
            d.reasons.append("High-capability action is within Greenlight; review the receipt before proceeding.")
        else:
            d.verdict = "REQUIRES_OPERATOR_APPROVAL"
            d.reasons.append("High-capability action is not pre-authorized by Greenlight; Operator must approve.")
    elif taint.tainted:
        d.verdict = "REQUIRES_OPERATOR_APPROVAL"
        d.reasons.append(
            "An operand traces to witnessed untrusted evidence "
            f"({', '.join(taint.matches[:3])}); Operator review required."
        )
    elif sev == _MEDIUM:
        if caps <= allowed_caps:
            d.verdict = "PASS"
            d.reasons.append(
                "Within Greenlight at capability granularity; "
                "ZAW does not verify path-level scope — review the target."
            )
        else:
            d.verdict = "REQUIRES_OPERATOR_APPROVAL"
            d.reasons.append("Filesystem action is not in Greenlight allowed; Operator must approve.")
    else:
        if caps <= allowed_caps:
            d.verdict = "PASS"
            d.reasons.append("No consequential capability detected and within Greenlight.")
        else:
            d.verdict = "WARN"
            d.reasons.append("No explicit Greenlight authorization for this action; proceed only after review.")

    if action.get("persistence") is True and d.verdict in ("PASS", "WARN"):
        d.verdict = "REQUIRES_OPERATOR_APPROVAL"
        d.reasons.append("Action declares persistence; persistent effects require Operator approval.")

    return d


def decide_action(
    action: Dict[str, Any],
    greenlight: Dict[str, Any],
    warnings: Dict[str, Any],
    evidence_packet: Dict[str, Any] | None = None,
    descriptor_binding: Dict[str, Any] | None = None,
) -> Verdict:
    """Back-compatible facade returning just the verdict string."""
    return evaluate_action(action, greenlight, warnings, evidence_packet, descriptor_binding).verdict
