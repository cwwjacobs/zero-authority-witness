"""
Zero Authority Witness — Public API (Phase 14)

Stable entry points for embedding ZAW in other tools or harnesses.
All functions return or produce receipted artifacts and respect the kernel.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional

from .core import run_witness
from .cli import main as cli_main  # for programmatic CLI if desired
from .tools.descriptor_binding import (
    build_descriptor_binding as _build_descriptor_binding,
    verify_descriptor_binding as _verify_descriptor_binding,
)
from .tools.descriptor_witness import witness_tool_descriptor as _witness_tool_descriptor


def witness_file(
    input_path: Path | str,
    task: str,
    runs_dir: Path | str = "runs",
    greenlight_path: Path | str | None = None,
) -> Path:
    """Convenience wrapper around the core witness."""
    return run_witness(
        Path(input_path),
        task,
        Path(runs_dir),
        Path(greenlight_path) if greenlight_path else None,
    )


def witness_text(
    text: str,
    task: str,
    runs_dir: Path | str = "runs",
    source_name: str = "inline-text",
) -> Path:
    """
    Witness raw text by writing it to a temp file first, then running the witness.
    The temp file is left in the run dir as source_snapshot.
    """
    import tempfile
    from pathlib import Path as _P

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = _P(tmp) / f"{source_name}.txt"
        tmp_path.write_text(text, encoding="utf-8")
        return run_witness(tmp_path, task, Path(runs_dir))


def witness_tool_descriptor(
    descriptor_path: Path | str,
    runs_dir: Path | str = "runs",
) -> Path:
    """Witness a third-party tool/MCP descriptor as untrusted intake."""
    return _witness_tool_descriptor(Path(descriptor_path), Path(runs_dir))


def build_descriptor_binding(descriptor_source: str, bound_digest: str) -> Dict[str, Any]:
    """Bind a witnessed descriptor identity (source + sha256: digest) for action gating."""
    return _build_descriptor_binding(descriptor_source, bound_digest)


def verify_descriptor_binding(action: Dict[str, Any], binding: Optional[Dict[str, Any]]):
    """Re-check an action's descriptor against its bound digest at action time."""
    return _verify_descriptor_binding(action, binding)


def build_safe_prompt_from_run(run_dir: Path) -> str:
    """Return the safe_prompt.md content for an existing run."""
    return (run_dir / "safe_prompt.md").read_text(encoding="utf-8")


def check_action(
    action_path: Path | str,
    greenlight_path: Path | str,
    evidence_path: Path | str,
) -> int:
    """
    Programmatic access to the check-action logic.
    Returns the exit-code style verdict (0=ok-ish, 1=BLOCK, 2=REQUIRES...).
    """
    from .cli import _cmd_check_action
    import argparse

    args = argparse.Namespace(
        action=str(action_path),
        greenlight=str(greenlight_path),
        evidence=str(evidence_path),
    )
    return _cmd_check_action(args)
