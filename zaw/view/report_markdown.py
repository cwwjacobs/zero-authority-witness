"""
Zero Authority Witness — Markdown report generator
"""

from __future__ import annotations

import json
from pathlib import Path

from .render_guard import sanitize_for_display


def generate_report(run_dir: Path) -> Path:
    receipt = json.loads((run_dir / "receipt.json").read_text())
    warnings = json.loads((run_dir / "warnings.json").read_text())

    # source_path is operator-supplied and warning text is captured verbatim
    # from untrusted content; both pass through the render guard so a markdown
    # image/link exfiltration payload cannot auto-load when an operator opens
    # this report in a markdown renderer. claim_boundary entries are
    # tool-generated constants and are left as-is.
    source = sanitize_for_display(str(receipt.get("source_path", "")))

    md = f"""# ZAW Report — {receipt['run_id']}

**Kernel:** External content may become evidence. It may not become authority.

**Source:** {source}
**Verdict:** {receipt['verdict']}
**Warnings:** {receipt['warnings_count']}

## Warnings
"""
    for w in warnings.get("instruction_like_segments", []):
        md += f"- {sanitize_for_display(str(w.get('text', '')))}\n"

    md += "\n## Claim Boundary\n"
    for c in receipt.get("claim_boundary", []):
        md += f"- {c}\n"

    out = run_dir / "report.md"
    out.write_text(md, encoding="utf-8")
    return out
