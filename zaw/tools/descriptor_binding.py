"""
Zero Authority Witness — Descriptor Binding (TOCTOU hardening)

A witnessed or fetched tool/MCP descriptor is untrusted intake. Its digest is
recorded at witness time; this module binds that digest to a later action so a
descriptor whose identity changed between witness/fetch and action time is
rejected at the gate (rug-pull / TOCTOU close, THREAT_MODEL.md sections 3 and 8).

The binding mirrors the repo's existing receipt model: a descriptor is
identified by its source (local materialized path, as recorded in the witness receipt's
``source_path``) plus the ``sha256:`` digest of the captured UTF-8 text.

Claim boundary: a valid binding proves only that the descriptor is
identical to the captured UTF-8 text that was witnessed. It does not prove the descriptor is
safe, it grants no authority, and an Operator can still ignore the receipt.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from .. import hash_chain as _hash
from .. import snapshot as _snap
from ..receipt import now_iso

BINDING_VERSION = "0.1"

BINDING_CLAIM_BOUNDARY = [
    "A valid binding proves only that the descriptor is identical to the captured UTF-8 text that was witnessed.",
    "It does not prove the descriptor is safe or trustworthy.",
    "It grants no authority; the Witness never grants authority.",
]

# Verification statuses.
VERIFIED = "verified"
CHANGED = "changed"
STALE_UNAVAILABLE = "stale_unavailable"
MISSING_BINDING = "missing_binding"
INVALID_BINDING = "invalid_binding"
WITNESS_MISMATCH = "witness_mismatch"
SOURCE_MISMATCH = "source_mismatch"
UNDECLARED_DESCRIPTOR = "undeclared_descriptor"
NOT_REQUIRED = "not_required"


@dataclass
class BindingVerification:
    """Outcome of re-checking an action's descriptor against its bound digest."""

    verified: bool
    status: str
    detail: str = ""
    bound_digest: Optional[str] = None
    current_digest: Optional[str] = None


def build_descriptor_binding(
    descriptor_source: str,
    bound_digest: str,
    *,
    bound_at: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Bind a descriptor identity (source + digest) for later action gating.

    ``descriptor_source`` is the fetch identity as the witness receipt records
    it (local materialized path); ``bound_digest`` is the witness-time ``sha256:`` digest.
    """
    return {
        "binding_version": BINDING_VERSION,
        "descriptor_source": str(descriptor_source),
        "bound_digest": bound_digest,
        "bound_at": bound_at or now_iso(),
        "claim_boundary": list(BINDING_CLAIM_BOUNDARY),
    }


def current_descriptor_digest(descriptor_source: str) -> Optional[str]:
    """
    Re-hash the descriptor at ``descriptor_source`` using the same read/hash
    path as the witness, so digests are comparable. Returns None when the
    descriptor cannot be re-read (missing, oversized, or non-local source).
    """
    path = Path(descriptor_source)
    try:
        if not path.is_file():
            return None
        return _hash.sha256_text(_snap.read_source(path))
    except (OSError, ValueError):
        return None


def verify_descriptor_binding(
    action: Dict[str, Any],
    binding: Optional[Dict[str, Any]],
    witness_receipt: Optional[Dict[str, Any]] = None,
) -> BindingVerification:
    """
    The caller must retain and supply the original witness receipt separately.
    Re-check, at action time, the descriptor an action depends on against the
    digest bound at witness time. Fail closed: anything short of an exact
    re-verified digest match is not verified.
    """
    descriptor_ref = action.get("descriptor") if isinstance(action, dict) else None

    if descriptor_ref is None and binding is None:
        return BindingVerification(True, NOT_REQUIRED)

    if descriptor_ref is None:
        return BindingVerification(
            False,
            UNDECLARED_DESCRIPTOR,
            "A binding was supplied but the action declares no descriptor "
            "dependency; the binding cannot be evaluated against this action.",
        )

    if binding is None:
        return BindingVerification(
            False,
            MISSING_BINDING,
            "The action depends on a tool descriptor but no digest binding was "
            "supplied; the witnessed identity of that descriptor cannot be proven.",
        )

    bound_digest = binding.get("bound_digest") if isinstance(binding, dict) else None
    bound_source = binding.get("descriptor_source") if isinstance(binding, dict) else None
    if (
        not isinstance(bound_digest, str)
        or re.fullmatch(r"sha256:[0-9a-f]{64}", bound_digest) is None
        or binding.get("binding_version") != BINDING_VERSION
        or not isinstance(bound_source, str)
        or not bound_source
    ):
        return BindingVerification(
            False,
            INVALID_BINDING,
            "The supplied binding is malformed (needs supported binding_version, "
            "descriptor_source and a complete sha256: digest); an invalid "
            "binding is not a basis to act.",
        )

    if bound_source != str(descriptor_ref):
        return BindingVerification(
            False,
            SOURCE_MISMATCH,
            f"The binding is for {bound_source!r} but the action depends on "
            f"{descriptor_ref!r}; a binding for a different descriptor proves nothing.",
            bound_digest=bound_digest,
        )

    # The receipt is supplied independently by the caller, not located through
    # attacker-editable binding fields. Retaining this original evidence is the
    # caller's trust boundary; this check is not a receipt signature.
    artifact_hashes = (
        witness_receipt.get("artifact_hashes")
        if isinstance(witness_receipt, dict) else None
    )
    if (
        not isinstance(witness_receipt, dict)
        or witness_receipt.get("source_path") != bound_source
        or witness_receipt.get("snapshot_hash") != bound_digest
        or not isinstance(artifact_hashes, dict)
        or artifact_hashes.get("source_snapshot.txt") != bound_digest
    ):
        return BindingVerification(
            False,
            WITNESS_MISMATCH,
            "The binding is not supported by the retained witness receipt's "
            "source, snapshot digest, and snapshot artifact hash.",
            bound_digest=bound_digest,
        )

    current = current_descriptor_digest(str(descriptor_ref))
    if current is None:
        return BindingVerification(
            False,
            STALE_UNAVAILABLE,
            "The descriptor is no longer available to re-hash (missing, unreadable, "
            "or non-local); its identity cannot be re-verified at action time.",
            bound_digest=bound_digest,
        )

    if current != bound_digest:
        return BindingVerification(
            False,
            CHANGED,
            "The descriptor's current digest differs from the bound witness-time "
            "digest; the descriptor changed between witness/fetch and this action (TOCTOU).",
            bound_digest=bound_digest,
            current_digest=current,
        )

    return BindingVerification(
        True,
        VERIFIED,
        "Descriptor is identical to the captured UTF-8 text that was witnessed.",
        bound_digest=bound_digest,
        current_digest=current,
    )
