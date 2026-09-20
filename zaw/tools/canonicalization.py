"""
Zero Authority Witness — Tool Descriptor Canonicalization Status

Third-party descriptors must NEVER become CANONICAL automatically.
"""

from __future__ import annotations

from enum import Enum


class CanonicalizationStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    INTAKED = "INTAKED"
    MAPPED = "MAPPED"
    REBUILT_LOCAL = "REBUILT_LOCAL"
    TESTED = "TESTED"
    RECEIPTED = "RECEIPTED"
    CANONICAL = "CANONICAL"


def initial_status_for_third_party() -> CanonicalizationStatus:
    """Default for anything that arrived from outside the Operator's control."""
    return CanonicalizationStatus.INTAKED


def can_be_canonical(status: CanonicalizationStatus) -> bool:
    return status == CanonicalizationStatus.CANONICAL
