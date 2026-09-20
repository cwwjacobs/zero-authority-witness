"""
Zero Authority Witness — Receipt writer

The receipt is the primary audit artifact. It must always record that
authority was not granted by the Witness itself (authority_granted: false).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_receipt(
    *,
    run_id: str,
    task: str,
    source_path: str,
    snapshot_hash: str,
    artifact_hashes: Dict[str, str],
    artifacts: List[str],
    warnings_count: int,
    verdict: str,
    claim_boundary: List[str],
    blind_spots: List[str],
) -> Dict:
    return {
        "receipt_version": "0.1",
        "run_id": run_id,
        "created_at": now_iso(),
        "task": task,
        "source_path": source_path,
        "snapshot_hash": snapshot_hash,
        "artifact_hashes": artifact_hashes,
        "artifacts": artifacts,
        "warnings_count": warnings_count,
        "verdict": verdict,
        "claim_boundary": claim_boundary,
        "blind_spots": blind_spots,
        "authority_granted": False,
    }


def write_receipt(run_dir: Path, receipt: Dict) -> Path:
    p = run_dir / "receipt.json"
    p.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p
