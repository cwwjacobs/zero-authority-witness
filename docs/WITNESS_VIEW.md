# Witness View — The Operator Watches the Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Core Principle

The human Operator watches **the Zero Authority Witness**, not the LLM or the agent that receives the safe prompt.

The Witness has no authority.

## What This Means in Practice

- When you run `zaw witness ...` or `python3 zaw.py ...`, you look at the artifacts in the generated run directory (source_snapshot, warnings.json, evidence_packet, receipt, safe_prompt.md).
- The safe_prompt.md is the *only* view of the untrusted content that is normally given to the LLM. It contains strong boundary language.
- Any decision to act on the evidence (especially actions that would read private data, mutate state, or cross a boundary) must still pass the Authority Membrane and Action Gate (or an explicit Operator override recorded in a decision receipt).
- Pretty summaries, HTML reports, or "the model said it was fine" are never a substitute for reviewing the raw warnings and the receipt.

## The Witness View Artifacts

- `source_snapshot.txt` + hash — exactly what was captured.
- `warnings.json` — instruction-like segments that were labeled no-authority.
- `evidence_packet.json` — the collapsed, labeled evidence (all items `evidence_only`).
- `receipt.json` — the full record of the run, including claim boundary, blind spots, and `authority_granted: false`.
- `safe_prompt.md` — the boundary-preserving text actually sent to the model.
- (Later) action decision receipts and report.md / inert HTML reports.

All of these are cheap, local, inspectable text/JSON files. They are the ground truth for the Operator.

## Why This Matters for MCP and Tool Descriptors

When a third-party MCP server or tool descriptor arrives, the Witness View shows you the raw descriptor (snapshotted), any instruction-like text the detector found in any field, the risk classification, and the explicit statement that the descriptor is not canonical.

You decide (via Greenlight, allow manifest, or direct review) whether to invest the work to locally rebuild and test a safe wrapper. The Witness never makes that decision for you.

## Failure Modes to Watch For

- Operator fatigue: "There are 50 clean receipts, this one must be fine too."
- Over-trust in the safe prompt: "The model got a safe prompt, therefore its output is safe to execute."
- Treating the existence of a receipt as proof that the Operator has reviewed and approved the content.
- Letting a downstream agent or UI hide the warnings section or the raw receipt.

The cathedral provides `zaw view` helpers (CLI summary, Markdown report, inert HTML) precisely to make the Witness View easy to consume without hiding the hard parts.

---

**We do not watch the model. We watch the Witness that stood between the untrusted world and the model.**

**End of WITNESS_VIEW.md**