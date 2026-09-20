"""
Zero Authority Witness — Action verdicts
"""

from __future__ import annotations

from typing import Literal

Verdict = Literal["PASS", "WARN", "BLOCK", "REQUIRES_OPERATOR_APPROVAL"]
