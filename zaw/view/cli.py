"""
Zero Authority Witness — View CLI (operator summary)
"""

from __future__ import annotations

import json
from pathlib import Path


def print_summary(receipt_path: Path) -> None:
    r = json.loads(receipt_path.read_text())
    print("Run:", r.get("run_id"))
    print("Source:", r.get("source_path"))
    print("Snapshot:", r.get("snapshot_hash"))
    print("Evidence artifacts present")
    print("Warnings:", r.get("warnings_count"))
    print("Verdict:", r.get("verdict"))
    print("Authority granted:", r.get("authority_granted"))
    for bs in r.get("blind_spots", [])[:2]:
        print("Blind spot:", bs)
