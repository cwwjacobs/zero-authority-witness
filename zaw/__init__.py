"""
Zero Authority Witness (ZAW) — Cathedral v0.1-rc1

A receipt-bearing intake membrane that converts untrusted content
into hash-receipted, data-only evidence before LLM reasoning or action.

Absolute Kernel:
    External content may become evidence.
    It may not become authority.

Author: Corey Jacobs
Protocol: PRISM
"""

__version__ = "0.1.0-rc1"

# Compatibility re-exports so that existing code and tests that do
# "import zaw; zaw.run(...)" continue to work during the transition.
# The real implementation lives in zaw.core.
from .core import run_witness as run  # type: ignore

__all__ = ["__version__", "run", "run_witness"]
