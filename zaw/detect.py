"""
Zero Authority Witness — Instruction-like content detection

This module contains the simple, explicit, stdlib pattern list used by the
proof kernel and the cathedral. It is deliberately not a semantic classifier.

All matches result in warnings with authority "none".
"""

from __future__ import annotations

import re
from typing import Dict, List

INSTRUCTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s+prompt",
    r"developer\s+message",
    r"treat\s+.*\s+as\s+system\s+authority",
    r"reveal\s+secrets?",
    r"upload\s+private\s+files?",
    r"upload\s+files?",
    r"change\s+the\s+allowlist",
    r"mark\s+.*\s+trusted",
    r"read\s+private\s+files?",
    r"grant\s+.*\s+authority",
    r"send\s+.*\s+to\s+attacker",
    r"exfiltrate",
    r"mutate\s+policy",
    r"mutate\s+Greenlight",
    r"canonicalize\s+this\s+tool",
]


def find_instruction_like_segments(text: str) -> List[Dict[str, str]]:
    segments: List[Dict[str, str]] = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        matched = []
        for pattern in INSTRUCTION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                matched.append(pattern)
        if matched:
            segments.append({
                "text": line,
                "authority": "none",
                "reason": "instruction_like_content_detected",
                "matched_patterns": ", ".join(matched),
            })
    return segments


def write_warnings(run_dir: Path, segments: List[Dict[str, str]]) -> Path:
    import json
    warnings = {
        "warnings_version": "0.1",
        "instruction_like_segments": segments,
    }
    p = run_dir / "warnings.json"
    p.write_text(json.dumps(warnings, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p
