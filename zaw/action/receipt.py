"""
Zero Authority Witness — Action decision receipt

Records the verdict AND the deterministic basis for it (capabilities detected,
untrusted-provenance matches, reasons), so an Operator can audit *why* an action
was blocked or escalated — not just that it was. authority_granted is always
False: the Witness never grants authority.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_action_receipt(
    *,
    run_id: str,
    action: Dict[str, Any],
    verdict: str,
    reason: str,
    greenlight_ref: str | None = None,
    evidence_ref: str | None = None,
    capabilities: Optional[List[str]] = None,
    tainted: bool = False,
    taint_matches: Optional[List[str]] = None,
    descriptor_binding: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    receipt = {
        "action_receipt_version": "0.2",
        "run_id": run_id,
        "created_at": now_iso(),
        "action": action,
        "verdict": verdict,
        "reason": reason,
        "capabilities": sorted(capabilities or []),
        "tainted": bool(tainted),
        "taint_matches": list(taint_matches or []),
        "greenlight_ref": greenlight_ref,
        "evidence_ref": evidence_ref,
        "authority_granted": False,
    }
    # Additive: present only when the action was gated on a descriptor binding.
    # Records the bound and action-time digests so the TOCTOU basis is auditable.
    if descriptor_binding is not None:
        receipt["descriptor_binding"] = descriptor_binding
    return receipt


def write_action_receipt(run_dir: Path, receipt: Dict[str, Any]) -> Path:
    p = run_dir / "action_decision_receipt.json"
    p.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p
