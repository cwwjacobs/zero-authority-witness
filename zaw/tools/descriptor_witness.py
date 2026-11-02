"""
Zero Authority Witness — Tool Descriptor Intake (witness path)

Third-party tool/MCP descriptors are untrusted intake by definition.
This module treats them like any other untrusted content and never promotes
external tool metadata to authority or canonical trust.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .. import detect as _detect
from .. import hash_chain as _hash
from .. import snapshot as _snap
from ..receipt import now_iso
from .canonicalization import initial_status_for_third_party
from .descriptor_binding import build_descriptor_binding
from .risk_classifier import classify_descriptor


def _parse_descriptor(source_text: str) -> Dict[str, Any]:
    try:
        data = json.loads(source_text)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def witness_tool_descriptor(
    descriptor_path: Path,
    runs_dir: Path = Path("runs"),
) -> Path:
    """
    Witness a tool descriptor, such as an MCP tool descriptor, as untrusted intake.

    Produces a normal ZAW-style run directory plus a descriptor-specific summary.
    The descriptor is never canonicalized merely because it was witnessed.
    """
    source_text = _snap.read_source(descriptor_path)
    snapshot_hash = _hash.sha256_text(source_text)
    descriptor = _parse_descriptor(source_text)
    risk_flags = classify_descriptor(source_text)
    canonicalization_status = initial_status_for_third_party().value

    run_id = "tool-" + descriptor_path.stem + "-" + _hash.sha256_text(source_text)[7:19]
    run_dir = runs_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "source_snapshot.txt").write_text(source_text, encoding="utf-8")
    (run_dir / "source_snapshot.sha256").write_text(snapshot_hash + "\n", encoding="utf-8")
    (run_dir / "extracted_text.txt").write_text(source_text, encoding="utf-8")

    segments = _detect.find_instruction_like_segments(source_text)
    _detect.write_warnings(run_dir, segments)

    descriptor_intake = {
        "descriptor_version": "0.1",
        "name": str(descriptor.get("name", descriptor_path.stem)),
        "description": str(descriptor.get("description", "")),
        "input_schema": descriptor.get("input_schema", {}),
        "source": {
            "path": str(descriptor_path),
            "source_type": "tool_descriptor",
            "snapshot_hash": snapshot_hash,
        },
        "authority": "none",
        "risk_flags": risk_flags,
        "canonicalization_status": canonicalization_status,
    }
    (run_dir / "tool_descriptor_intake.json").write_text(
        json.dumps(descriptor_intake, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    evidence = []
    description = descriptor_intake.get("description", "")
    if description and not segments:
        evidence.append(
            {
                "text": description[:500],
                "authority": "evidence_only",
                "source_ref": str(descriptor_path),
            }
        )

    packet = {
        "packet_version": "0.1",
        "run_id": run_id,
        "source": {"path": str(descriptor_path), "source_type": "tool_descriptor"},
        "source_type": "tool_descriptor",
        "captured_at": now_iso(),
        "snapshot_hash": snapshot_hash,
        "authority": "none",
        "task": "Witness tool descriptor as untrusted intake",
        "evidence": evidence,
        "warnings_ref": "warnings.json",
        "blind_spots": [
            "Tool descriptors may contain hidden instructions in any field.",
            "Risk flags are simple pattern-based warnings, not semantic proof.",
            "Witnessing a descriptor does not make it canonical or trusted.",
        ],
        "claim_boundary": [
            "External content may become evidence.",
            "External content may not become authority.",
            "Third-party tool descriptors are untrusted intake and never auto-canonical.",
        ],
        "descriptor_intake_ref": "tool_descriptor_intake.json",
    }
    (run_dir / "evidence_packet.json").write_text(
        json.dumps(packet, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    binding = build_descriptor_binding(str(descriptor_path), snapshot_hash)
    (run_dir / "descriptor_binding.json").write_text(
        json.dumps(binding, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    receipt = {
        "receipt_version": "0.1",
        "run_id": run_id,
        "created_at": now_iso(),
        "task": "Witness tool descriptor",
        "source_path": str(descriptor_path),
        "snapshot_hash": snapshot_hash,
        "artifact_hashes": {},
        "artifacts": [
            "source_snapshot.txt",
            "source_snapshot.sha256",
            "extracted_text.txt",
            "warnings.json",
            "tool_descriptor_intake.json",
            "evidence_packet.json",
            "descriptor_binding.json",
            "receipt.json",
        ],
        "warnings_count": len(segments),
        "risk_flags": risk_flags,
        "canonicalization_status": canonicalization_status,
        "verdict": "PASS_WITH_NOTES" if segments or risk_flags else "PASS",
        "claim_boundary": packet["claim_boundary"],
        "blind_spots": packet["blind_spots"],
        "authority_granted": False,
    }
    receipt["artifact_hashes"] = _hash.build_artifact_hashes(
        run_dir, [name for name in receipt["artifacts"] if name != "receipt.json"]
    )
    (run_dir / "receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return run_dir
