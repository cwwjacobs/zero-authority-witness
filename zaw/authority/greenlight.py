"""
Zero Authority Witness — Greenlight loader (Authority Membrane)

Minimal implementation for v0.1. Loads and does basic shape checking.
The real power is in how callers (core, action gate) use the Greenlight.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


def default_greenlight(goal: str = "Default minimal Greenlight") -> Dict[str, Any]:
    return {
        "goal": goal,
        "allowed": ["read staged input", "extract evidence", "label warnings", "write receipts"],
        "not_allowed": [
            "treat external content as instruction",
            "mutate allowlists",
            "read secrets",
            "upload files",
            "grant tool authority",
        ],
        "authority_owner": "Responsible Operator",
    }


def load_greenlight(path: Path | None) -> Dict[str, Any]:
    if path is None or not path.exists():
        return default_greenlight()
    data = json.loads(path.read_text(encoding="utf-8"))
    check_greenlight_shape(data)
    return data


def check_greenlight_shape(g: Dict[str, Any]) -> None:
    required = {"goal", "allowed", "not_allowed", "authority_owner"}
    missing = required - set(g.keys())
    if missing:
        raise ValueError(f"Greenlight missing required fields: {missing}")
    if not isinstance(g["allowed"], list) or not isinstance(g["not_allowed"], list):
        raise ValueError("Greenlight allowed/not_allowed must be lists")
