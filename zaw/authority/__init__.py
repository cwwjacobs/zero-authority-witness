"""
Authority Membrane package.

Exports the key functions for scope and allow decisions.
"""
from .greenlight import load_greenlight, default_greenlight, check_greenlight_shape
from .allow import check_allowed
from .mutation_guard import detect_mutation_attempt, guard_action
from .scope_delta import compute_scope_delta

__all__ = [
    "load_greenlight",
    "default_greenlight",
    "check_greenlight_shape",
    "check_allowed",
    "detect_mutation_attempt",
    "guard_action",
    "compute_scope_delta",
]
