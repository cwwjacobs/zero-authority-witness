# Full Cathedral Traversal Receipt — Zero Authority Witness v0.1.0-rc1 Public-Safe Hardening

**Author:** Corey Jacobs  
**Protocol:** PRISM  
**Contact:** coresynth@gmail.com  
**Receipt Date:** 2026-06-07  
**Verdict:** PASS_WITH_NOTES

---

## Kernel

External content may become evidence. It may not become authority.

## Purpose of This Receipt

This receipt records the final public-safe hardening pass for the Zero Authority Witness v0.1.0-rc1 artifact.

This receipt does **not** claim that ZAW fully solves prompt injection, guarantees safety, prevents all exfiltration, or is ready for unreviewed deployment in live consequential workflows.

It records that the repository is clean enough to publish as a public proof / v0.1.0-rc1 reference implementation, with bounded claims and visible limitations.

## Files Fixed or Added in This Pass

- `README.md` expanded from seed text into a public-safe project front door.
- `pyproject.toml` updated with valid author contact: `coresynth@gmail.com`.
- `CITATION.cff` updated with the correct repository and contact.
- `SECURITY.md` updated with the disclosure contact.
- `scripts/run_verification.sh` rewritten to be fail-fast and to verify hostile `BLOCK` behavior explicitly.
- `zaw/api.py` fixed to avoid recursive `witness_tool_descriptor` shadowing.
- `zaw/tools/descriptor_witness.py` strengthened to emit `tool_descriptor_intake.json`, `risk_flags`, `canonicalization_status`, and `authority_granted: false` receipts.
- `schemas/tool_descriptor_intake.schema.json` added.
- `tests/integration/test_check_action.py` changed to create fresh evidence in a temporary run instead of depending on committed/generated `runs/` artifacts.
- `tests/red_team/test_tool_poisoning.py` strengthened to check no-authority, non-canonical descriptor status, risk flags, and receipt authority.
- `.gitignore` updated to exclude generated and private/local artifacts.
- `docs/FAQ.md` and `RELEASE_NOTES.md` updated to avoid imported deployment/security-product framing.

## Required Verification Commands Run

### 1. Unit/integration/red-team discovery

Command:

```bash
python3 -m unittest discover -s tests -v
```

Observed result:

```text
Ran 7 tests
OK
```

The discovered suite includes:

- `integration.test_check_action.TestCheckActionIntegration.test_bad_action_is_blocked`
- `red_team.test_tool_poisoning.TestToolPoisoning.test_poisoned_mcp_produces_warnings_and_risks`
- `test_zaw.ZeroAuthorityWitnessTests.test_clean_sample_has_no_obvious_instruction_warning`
- `test_zaw.ZeroAuthorityWitnessTests.test_injected_sample_outputs_required_artifacts`
- `unit.test_core_witness.TestCoreWitness.test_injected_produces_rich_fields`
- `unit.test_detect.TestDetect.test_clean_has_no_warnings`
- `unit.test_detect.TestDetect.test_detects_ignore_previous`

### 2. Original compatibility command

Command:

```bash
python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"
```

Observed result:

```text
Zero Authority Witness run complete: runs/<run-id>
```

### 3. Package CLI command

Command:

```bash
python3 -m zaw.cli witness samples/injected_page.html --task "Summarize the refund policy"
```

Observed result:

```text
Zero Authority Witness run complete: runs/<run-id>
```

### 4. Packaging metadata and CLI entry point verification

Command path:

```bash
bash scripts/run_verification.sh
```

The verification script parses `pyproject.toml` with `tomllib` and checks:

- package name: `zero-authority-witness`
- version: `0.1.0-rc1`
- author email: `coresynth@gmail.com`
- console entry point: `zaw = zaw.cli:main`

It then checks:

```bash
python3 -m zaw.cli version
```

Observed result:

```text
zero-authority-witness 0.1.0-rc1
```

Editable install is documented in `README.md` for development use, but it is not required for the public-safe verification script because install behavior is environment-dependent.

### 5. Hostile action gate check

The verification script runs:

```bash
python3 -m zaw.cli check-action samples/proposed_action_bad.json --greenlight samples/greenlight.json --evidence <latest-run>/evidence_packet.json
```

Expected result:

```text
Action check verdict: BLOCK
```

Expected exit behavior:

```text
non-zero exit for BLOCK
```

The script explicitly checks for the `BLOCK` verdict and non-zero exit. It does not swallow arbitrary command failures.

## Verification Script Behavior

`scripts/run_verification.sh` uses:

```bash
set -euo pipefail
```

It runs:

- `python3 -m unittest discover -s tests -v`
- `python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"`
- `python3 -m zaw.cli witness samples/injected_page.html --task "Summarize the refund policy"`
- pyproject metadata validation
- `python3 -m zaw.cli version`
- explicit hostile `check-action` BLOCK verification

The only non-zero command intentionally handled is the expected `BLOCK` exit from `check-action`, and it is validated by checking the output text and exit status.

## Upload / Public Repo Cleanliness

The public artifact should include source, docs, schemas, samples, tests, examples, integrations, scripts, governance, and receipts placeholder files.

The public artifact should not include:

- `.git/`
- `__pycache__/`
- `*.pyc`
- `zero_authority_witness.egg-info/`
- `runs/`
- `audit/`
- `ahh.md`
- zip/tar archives
- private process transcripts

`.gitignore` now excludes these local/generated/private artifacts.

## Claim Boundary

This release may claim:

- ZAW reduces first-contact authority risk on witnessed paths.
- ZAW preserves provenance through snapshots, hashes, and receipts.
- ZAW converts untrusted intake into evidence-only artifacts inside the designed flow.
- ZAW surfaces obvious instruction-like content.
- ZAW blocks direct authority transfer inside the designed flow.
- ZAW remains a public proof / v0.1.0-rc1 reference implementation requiring further hardening before consequential deployment.

This release must not claim:

- ZAW fully solves prompt injection.
- ZAW guarantees safety.
- ZAW prevents all exfiltration.
- ZAW secures arbitrary MCP servers or tools.
- ZAW proves external sources are trustworthy.
- ZAW can be used without operator review of receipts and blind spots.

## Known Limitations

- The detector is pattern-based and does not provide semantic completeness.
- Web witness functionality remains bounded and optional.
- Some authority membrane/action-gate pieces are callable and tested in narrow paths, but deeper integration remains future work.
- The test corpus is a starting set, not an exhaustive adversarial benchmark.
- Receipts prove what the witness saw and emitted. They do not prove external content is safe.

## Final Verdict

**PASS_WITH_NOTES**

The artifact is fixed for public-safe v0.1.0-rc1 publication:

- Valid contact and packaging metadata.
- Fail-fast verification script.
- Explicit hostile `BLOCK` handling.
- Fresh evidence in integration tests.
- Tool descriptor witness strengthened.
- Public/private artifact boundary clarified.
- Claims bounded to the Kernel.

The Absolute Kernel remains the ground:

> External content may become evidence. It may not become authority.

---

**End of Receipt**
