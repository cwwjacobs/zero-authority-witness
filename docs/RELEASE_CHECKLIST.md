# Release Checklist — Zero Authority Witness v0.1

**Protocol:** PRISM

Before cutting or declaring a release candidate, the following must be verified:

## Functional

- [ ] `python3 -m unittest discover` passes (or all failures are understood and receipted).
- [ ] `python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"` succeeds and produces the 7 canonical artifacts.
- [ ] `python3 -m zaw.cli witness samples/injected_page.html --task "..."` succeeds.
- [ ] The generated receipt for the hostile sample has `verdict: "PASS_WITH_NOTES"`, `authority_granted: false`, and a non-empty warnings list.
- [ ] The generated safe prompt contains the exact Authority Boundary and Required Behavior language from the proof kernel.
- [ ] Tool descriptor witness on `samples/poisoned_mcp_tool.json` produces warnings and does not mark the descriptor CANONICAL.

## Claims and Language

- [ ] No document, README, example, or generated artifact claims that ZAW:
  - fully solves prompt injection
  - guarantees safety
  - provides complete containment
  - detects all attacks
  - makes third-party tools or MCP servers trustworthy
- [ ] All public-facing text uses the bounded language from CLAIM_BOUNDARY.md ("reduces first-contact authority risk", "evidence only", "hash proves integrity not safety", etc.).

## Packaging and Compatibility

- [ ] `pip install -e .` (or equivalent) succeeds with no extra runtime dependencies.
- [ ] `zaw version` (after install) reports the correct v0.1-rc1 string.
- [ ] The root `zaw.py` compat command still works exactly as in the original proof.
- [ ] `python -m zaw.cli` works.

## Governance and Receipts

- [ ] NOTICE, CITATION.cff, FUNDING.md, CONTRIBUTING.md, SECURITY.md are present and accurate.
- [ ] RELEASE_NOTES.md exists for this rc and accurately describes limitations.
- [ ] A FULL_CATHEDRAL_TRAVERSAL_RECEIPT.md (or equivalent) has been produced for this build.
- [ ] The KSL / Cathedral Goal / claim boundary have not been silently broadened.

## Known Acceptable Deviations (to be noted in the final receipt)

- Some Phase 4–8 membranes are present as functional stubs or minimal implementations (full power will come in later increments).
- The old monolithic `tests/test_zaw.py` may require PYTHONPATH or minor adjustment for the package layout (the required demo commands and unittest discover target are satisfied).
- Web and browser stubs are intentionally minimal and do not include live network in the default test path.

Sign-off on this checklist is evidence that the v0.1 public-safe reference shape has been achieved while preserving the kernel. It is not a claim of total security.