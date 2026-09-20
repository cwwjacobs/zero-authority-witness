"""
Zero Authority Witness — Hashing and artifact integrity

All hashes are SHA-256 and are recorded with the "sha256:" prefix.
Hashes prove integrity of the artifact at the time it was written.
They do not prove safety or authority.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    data = path.read_bytes()
    return "sha256:" + hashlib.sha256(data).hexdigest()


def build_artifact_hashes(run_dir: Path, artifacts: list[str]) -> Dict[str, str]:
    """
    Return a map of artifact name -> its sha256 for every artifact that exists
    on disk in the run_dir.
    """
    result: Dict[str, str] = {}
    for name in artifacts:
        p = run_dir / name
        if p.exists():
            if p.suffix in {".json", ".txt", ".md", ".html"} or name.endswith(".sha256"):
                # text or we already have the hash file
                if name.endswith(".sha256"):
                    result[name] = p.read_text(encoding="utf-8").strip()
                else:
                    result[name] = sha256_file(p)
            else:
                result[name] = sha256_file(p)
    return result
