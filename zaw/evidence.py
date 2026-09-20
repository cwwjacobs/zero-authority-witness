"""
Zero Authority Witness — Evidence packet construction

Rules (per PROMOTION_RULES and FORBIDDEN_PROMOTIONS):
- Lines that matched warnings do not become normal evidence.
- Every evidence item has authority "evidence_only".
- The packet itself has authority "none".
- source_ref is preserved for every item.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def evidence_from_text(
    text: str,
    warnings: List[Dict[str, str]],
    source_ref: str = "untrusted_snapshot",
) -> List[Dict[str, str]]:
    warning_texts = {w["text"] for w in warnings}
    evidence: List[Dict[str, str]] = []
    for line in [line.strip() for line in text.splitlines() if line.strip()]:
        if line in warning_texts:
            continue
        if len(line) < 4:
            continue
        evidence.append({
            "text": line,
            "authority": "evidence_only",
            "source_ref": source_ref,
        })
    return evidence


def build_evidence_packet(
    *,
    run_id: str,
    source_path: str,
    source_type: str,
    captured_at: str,
    snapshot_hash: str,
    task: str,
    evidence: List[Dict[str, str]],
    warnings_ref: str,
    blind_spots: List[str],
    claim_boundary: List[str],
) -> Dict:
    return {
        "packet_version": "0.1",
        "run_id": run_id,
        "source": {"path": source_path, "source_type": source_type},
        "captured_at": captured_at,
        "snapshot_hash": snapshot_hash,
        "authority": "none",
        "task": task,
        "evidence": evidence,
        "warnings_ref": warnings_ref,
        "blind_spots": blind_spots,
        "claim_boundary": claim_boundary,
    }


def write_evidence_packet(run_dir: Path, packet: Dict) -> Path:
    p = run_dir / "evidence_packet.json"
    p.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p
