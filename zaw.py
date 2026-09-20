#!/usr/bin/env python3
"""
Zero Authority Witness — root compatibility entrypoint

This file preserves the original proof-kernel invocation:

    python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"

It also keeps the module-level `run` function so that code doing
`import zaw; zaw.run(...)` (as in the original tests/test_zaw.py)
continues to work while the cathedral package is being adopted.

All real implementation now lives in the `zaw` package.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Re-export the package so "import zaw" gives the cathedral package
# (this makes the existing test import work once PYTHONPATH or install is correct).
import zaw as _zaw_pkg  # noqa: F401
from zaw.core import run_witness as run  # re-export for the old test contract


def main() -> int:
    parser = argparse.ArgumentParser(description="Zero Authority Witness proof kernel (compat)")
    parser.add_argument("input", help="Path to untrusted input file")
    parser.add_argument("--task", required=True, help="Operator task / Greenlight goal")
    parser.add_argument("--runs-dir", default="runs", help="Directory for run artifacts")
    args = parser.parse_args()

    run_dir = run(Path(args.input), args.task, Path(args.runs_dir))
    print(f"Zero Authority Witness run complete: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
