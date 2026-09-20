# Release Notes — Zero Authority Witness v0.1.0-rc1

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## What Exists (Public-Safe RC Shape)

- Complete factored `zaw` package (stdlib only) with clear module boundaries.
- Core witness engine (`run_witness`) that produces the canonical seven artifacts and the richer cathedral fields (run_id, captured_at, artifact_hashes, source_ref on evidence items, claim_boundary in packets, `authority_granted: false` in receipts).
- Authority Membrane basics (Greenlight loader, simple allow checker, mutation guard).
- Action gate pieces (causality estimation, verdict types, action decision receipts) + a `proposed_action_bad.json` sample.
- Tool / MCP Descriptor Intake (descriptor witness, risk classifier, canonicalization status machine, promotion guard, rewrite template generator).
- Bounded web stub modules (url intake, raw_fetch skeleton, snapshot delta, blind spots).
- Witness View helpers (CLI summary, Markdown report generator, inert HTML report guard).
- Rich test corpus layout (benign / injection_obvious / injection_hidden / tool_poisoning / authority_laundering fixtures).
- Full documentation suite including CATHEDRAL_GOAL, LEXICON, strengthened CLAIM_BOUNDARY, THREAT_MODEL, AUTHORITY_MODEL, INTAKE_STATES, PROMOTION_RULES, FORBIDDEN_PROMOTIONS, WITNESS_VIEW, OPERATOR_GUIDE, DEVELOPER_GUIDE (partial), SECURITY_MODEL (via existing + new), FAQ.
- Governance artifacts: NOTICE, CITATION.cff, FUNDING.md, CONTRIBUTING.md, SECURITY.md.
- Packaging (`pyproject.toml` with console script `zaw`).
- Compatibility layer: root `zaw.py` and package `__init__` so the original proof demo command and `zaw.run(...)` contract continue to work.
- Verification script and this release notes + release checklist.

## What Is Limited (Honest v0.1-rc1 Scope)

- Many of the Phase 4–8 membranes are present and functional at a basic level but are not yet deeply integrated into every code path or exhaustively red-teamed.
- The proposed action gate (`check-action`) is a deterministic, default-deny decision over **capability × provenance**: it classifies what an action's operands would do and whether they trace to witnessed untrusted evidence, and never reads a self-reported origin label. It blocks consequential actions driven by untrusted content and escalates unauthorized high-capability actions to the Operator, writing an `action_decision_receipt.json`. Known limits (documented in AUTHORITY_MODEL.md): capability matching is coarse (authorizes a *kind*, not a path) and taint tracing catches literal quoting, not transformed/obfuscated derivation.
- Web fetch is intentionally optional and stubbed for tests (no live network in the default verification path).
- The old `tests/test_zaw.py` works via the compat re-export; a fuller `tests/unit/` + `tests/integration/` + `tests/red_team/` + golden suite is scaffolded but not 100% populated in this rc.
- No browser automation, no server, no heavy frameworks (by design).

## What the Release Deliberately Does Not Claim

See CLAIM_BOUNDARY.md, THREAT_MODEL.md, and the CATHEDRAL_GOAL.md. This rc reduces first-contact authority risk on the witnessed paths and provides a public-safe reference structure for further work. It does not guarantee safety.

## Next Work (Recommended KSL for Subsequent Increments)

- Deep integration of the Authority Membrane and Action Gate into the core `run_witness` + CLI flows.
- Expansion of the red-team fixture corpus and automated checks for the named threats.
- Stronger canonicalization and promotion guard enforcement with receipts.
- Optional but bounded live URL witness with full TOCTOU + header recording.
- MCP safe adapter reference implementation (in `integrations/`).
- Operator tooling for maintaining living Greenlights and reviewing batches of receipts.

## Verification Commands (must pass for this rc)

```
python3 -m unittest discover
python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"
python3 -m zaw.cli witness samples/injected_page.html --task "Summarize the refund policy"
```

All three are expected to succeed with the hostile sample producing PASS_WITH_NOTES and visible warnings.

---

This is a receipt-bearing, evidence-only release. The Operator remains the source of authority.

**End of RELEASE_NOTES.md**