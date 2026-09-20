"""
Zero Authority Witness — URL Intake (Phase 7)

Creates an intake request for a URL without performing any network I/O unless
explicitly requested via raw_fetch.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class URLIntakeRequest:
    url: str
    task: str
    timeout: float = 10.0
    # Future: headers, etc. kept minimal per stdlib + bounded constraint


def create_url_intake(url: str, task: str, timeout: float = 10.0) -> URLIntakeRequest:
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")
    return URLIntakeRequest(url=url, task=task, timeout=timeout)
