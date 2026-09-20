"""
Zero Authority Witness — Tool Promotion Guard

Blocks any automatic promotion of a third-party descriptor to CANONICAL.
"""

from __future__ import annotations

from .canonicalization import CanonicalizationStatus, initial_status_for_third_party


def guard_promotion_attempt(current: CanonicalizationStatus, proposed: CanonicalizationStatus) -> bool:
    """
    Returns True if the promotion should be blocked.
    Third-party descriptors may never jump straight to CANONICAL.
    """
    if proposed == CanonicalizationStatus.CANONICAL:
        if current not in (CanonicalizationStatus.RECEIPTED, CanonicalizationStatus.TESTED):
            return True  # block
    return False
