"""
Zero Authority Witness — Web-specific Blind Spots (Phase 7)
"""

from __future__ import annotations

from typing import List


WEB_BLIND_SPOTS: List[str] = [
    "Dynamic JavaScript not rendered or executed.",
    "Server-side rendered or auth-gated content not inspected.",
    "Remote server state at fetch time is unknown and may have changed (TOCTOU).",
    "Fingerprinting, tracking, or conditional content based on client characteristics is invisible.",
    "Redirects, cookies, or session-dependent responses are not followed or stored.",
    "Large responses may be truncated.",
    "Only static text/HTML extraction is performed; binary resources, images, etc. are not analyzed.",
]


def get_web_blind_spots() -> List[str]:
    return WEB_BLIND_SPOTS[:]
