"""
Zero Authority Witness — Snapshot Delta (Phase 7)

Simple comparison of two captured snapshots by hash and basic text diff.
"""

from __future__ import annotations

import difflib
from pathlib import Path
from typing import Dict, Any, List


def compare_snapshots(
    snapshot_a: str | Path,
    snapshot_b: str | Path,
    snapshot_hash_a: str | None = None,
    snapshot_hash_b: str | None = None,
) -> Dict[str, Any]:
    """
    Returns a delta report.
    If hashes are provided and differ, delta is immediate.
    Otherwise performs a simple unified diff (limited).
    """
    if isinstance(snapshot_a, Path):
        text_a = snapshot_a.read_text(encoding="utf-8")
    else:
        text_a = snapshot_a

    if isinstance(snapshot_b, Path):
        text_b = snapshot_b.read_text(encoding="utf-8")
    else:
        text_b = snapshot_b

    result: Dict[str, Any] = {
        "hash_a": snapshot_hash_a,
        "hash_b": snapshot_hash_b,
        "hash_match": (snapshot_hash_a == snapshot_hash_b) if snapshot_hash_a and snapshot_hash_b else None,
        "identical": text_a == text_b,
        "diff_lines": [],
        "blind_spots": ["Only simple text diff; semantic or structural changes may not be highlighted."],
    }

    if result["hash_match"] is True:
        result["identical"] = True
        return result

    # Limited diff
    diff = list(difflib.unified_diff(
        text_a.splitlines(keepends=True),
        text_b.splitlines(keepends=True),
        fromfile="snapshot_a",
        tofile="snapshot_b",
        n=2,
    ))
    result["diff_lines"] = diff[:50]  # cap output
    if len(diff) > 50:
        result["blind_spots"].append("Diff was truncated for size.")

    return result
