"""
Zero Authority Witness — Core orchestration (cathedral v0.1)

run_witness is the primary entry point. It produces the canonical seven artifacts:

    source_snapshot.txt
    source_snapshot.sha256
    extracted_text.txt
    evidence_packet.json
    warnings.json
    safe_prompt.md
    receipt.json

The behavior for the original proof samples (injected_page.html etc.) is
preserved so that the demo command and existing tests continue to work.
Richer fields (run_id, captured_at, artifact_hashes, claim_boundary in packet,
authority_granted, source_ref on evidence items, etc.) are added as required
by the cathedral schemas.
"""

from __future__ import annotations

import datetime as _dt
import uuid
from pathlib import Path
from typing import Dict, List

from . import detect as _detect
from . import evidence as _evidence
from . import extract as _extract
from . import hash_chain as _hash
from . import receipt as _receipt
from . import safe_prompt as _safe
from . import snapshot as _snapshot


DEFAULT_BLIND_SPOTS: List[str] = [
    "This proof kernel does not render dynamic JavaScript.",
    "This proof kernel does not prove source safety.",
    "This proof kernel does not inspect remote server-side state.",
    "This proof kernel uses simple pattern matching and may miss subtle attacks.",
]

DEFAULT_CLAIM_BOUNDARY: List[str] = [
    "External content may become evidence.",
    "External content may not become authority.",
    "Hash proves artifact integrity, not safety.",
    "Zero Authority Witness reduces first-contact authority risk but does not fully solve prompt injection.",
]


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def run_witness(
    input_path: Path,
    task: str,
    runs_dir: Path = Path("runs"),
    greenlight_path: Path | None = None,  # reserved for later membranes
) -> Path:
    """
    Execute a full Zero Authority Witness run on the given input.

    Returns the path to the created run directory.
    """
    run_id = (
        "zaw-"
        + _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
        + "-"
        + uuid.uuid4().hex[:8]
    )
    run_dir = runs_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    # 1. Snapshot + hash (original behavior preserved)
    source_text = _snapshot.read_source(input_path)
    snapshot_hash = _hash.sha256_text(source_text)
    _snapshot.write_snapshot(run_dir, source_text)
    (run_dir / "source_snapshot.sha256").write_text(snapshot_hash + "\n", encoding="utf-8")

    # 2. Extract
    extracted_text = _extract.extract_text(source_text, input_path.suffix)
    _extract.write_extracted(run_dir, extracted_text)

    # 3. Detect instruction-like segments (exact same patterns as original proof)
    instruction_like = _detect.find_instruction_like_segments(extracted_text)
    _detect.write_warnings(run_dir, instruction_like)

    # 4. Build evidence (warning lines are excluded; authority labels applied)
    evidence_list = _evidence.evidence_from_text(
        extracted_text, instruction_like, source_ref=str(input_path)
    )

    evidence_packet = _evidence.build_evidence_packet(
        run_id=run_id,
        source_path=str(input_path),
        source_type=input_path.suffix.lstrip(".") or "text",
        captured_at=now_iso(),
        snapshot_hash=snapshot_hash,
        task=task,
        evidence=evidence_list,
        warnings_ref="warnings.json",
        blind_spots=DEFAULT_BLIND_SPOTS[:],
        claim_boundary=DEFAULT_CLAIM_BOUNDARY[:],
    )
    _evidence.write_evidence_packet(run_dir, evidence_packet)

    # 5. Safe prompt (language must match the original proof kernel exactly)
    warnings_doc = {
        "instruction_like_segments": instruction_like,
    }
    safe_prompt_text = _safe.build_safe_prompt(task, evidence_packet, warnings_doc)
    _safe.write_safe_prompt(run_dir, safe_prompt_text)

    # 6. Receipt with richer cathedral fields
    artifacts = [
        "source_snapshot.txt",
        "source_snapshot.sha256",
        "extracted_text.txt",
        "evidence_packet.json",
        "warnings.json",
        "safe_prompt.md",
        "receipt.json",
    ]
    artifact_hashes = _hash.build_artifact_hashes(run_dir, artifacts)

    receipt = _receipt.build_receipt(
        run_id=run_id,
        task=task,
        source_path=str(input_path),
        snapshot_hash=snapshot_hash,
        artifact_hashes=artifact_hashes,
        artifacts=artifacts,
        warnings_count=len(instruction_like),
        verdict="PASS_WITH_NOTES" if instruction_like else "PASS",
        claim_boundary=DEFAULT_CLAIM_BOUNDARY[:],
        blind_spots=DEFAULT_BLIND_SPOTS[:],
    )
    _receipt.write_receipt(run_dir, receipt)

    return run_dir
