"""
Zero Authority Witness — Snapshot module

Responsible for reading the source and writing the exact source_snapshot.txt.
"""

from __future__ import annotations

from pathlib import Path

# Cap a single witnessed artifact so a hostile or accidental oversized input
# cannot exhaust memory. Operators can raise this explicitly per call.
DEFAULT_MAX_INPUT_BYTES = 5_000_000


def read_source(path: Path, max_bytes: int = DEFAULT_MAX_INPUT_BYTES) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input not found: {path}")
    size = path.stat().st_size
    if size > max_bytes:
        raise ValueError(
            f"Input too large: {size} bytes exceeds max_bytes={max_bytes}. "
            "Pass a larger max_bytes explicitly if this input is trusted and intended."
        )
    # Untrusted intake may not be valid UTF-8; decode defensively so the
    # witness records what was seen instead of crashing on hostile bytes.
    return path.read_bytes().decode("utf-8", errors="replace")


def write_snapshot(run_dir: Path, source_text: str) -> Path:
    snapshot_path = run_dir / "source_snapshot.txt"
    snapshot_path.write_text(source_text, encoding="utf-8")
    return snapshot_path
