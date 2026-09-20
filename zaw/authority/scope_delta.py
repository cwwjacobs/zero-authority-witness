"""
Zero Authority Witness — Scope Delta (Authority Membrane)

Compares a proposed action against the current Greenlight + witnessed evidence.
The full deterministic decision (capability x provenance, default-deny) lives in
``zaw/action/gate.py``; this module is the thin, stable facade so callers that
import ``compute_scope_delta`` keep working.
"""

from __future__ import annotations

from typing import Any, Dict, Literal

Verdict = Literal["PASS", "WARN", "BLOCK", "REQUIRES_OPERATOR_APPROVAL"]


def compute_scope_delta(
    action: Dict[str, Any],
    greenlight: Dict[str, Any],
    warnings: Dict[str, Any],
    evidence_packet: Dict[str, Any] | None = None,
) -> Verdict:
    # Local import avoids an import cycle (gate imports the membrane modules).
    from ..action.gate import evaluate_action

    return evaluate_action(action, greenlight, warnings, evidence_packet).verdict
