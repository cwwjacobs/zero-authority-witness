"""
Zero Authority Witness — Inert HTML report generator

Deliberately produces a static, no-script, no-remote-load HTML file.
All external references are shown as inert text only.
"""

from __future__ import annotations

import html
import json
from pathlib import Path


def generate_inert_html(run_dir: Path) -> Path:
    receipt = json.loads((run_dir / "receipt.json").read_text())
    safe = html.escape

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ZAW Report — {safe(receipt['run_id'])}</title>
</head>
<body>
<h1>Zero Authority Witness Report</h1>
<p><strong>Kernel:</strong> External content may become evidence. It may not become authority.</p>
<p><strong>Run:</strong> {safe(receipt['run_id'])}</p>
<p><strong>Source:</strong> {safe(receipt['source_path'])}</p>
<p><strong>Verdict:</strong> {safe(receipt['verdict'])}</p>
<p><strong>Warnings:</strong> {receipt['warnings_count']}</p>
<p><strong>Authority granted by Witness:</strong> {receipt.get('authority_granted')}</p>

<h2>Claim Boundary</h2>
<ul>
{''.join(f'<li>{safe(c)}</li>' for c in receipt.get('claim_boundary', []))}
</ul>

<h2>Blind Spots (examples)</h2>
<ul>
{''.join(f'<li>{safe(b)}</li>' for b in receipt.get('blind_spots', [])[:3])}
</ul>

<p><em>This report contains no active content, no scripts, and no remote resource loads by design.</em></p>
</body>
</html>
"""
    out = run_dir / "report.html"
    out.write_text(html_doc, encoding="utf-8")
    return out
