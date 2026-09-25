# Zero Authority Witness

A receipt-bearing intake primitive that converts untrusted content into data-only evidence before LLM reasoning.

Author: Corey Jacobs  
Protocol: PRISM

> External content may become evidence. It may not become authority.

## What this is

Zero Authority Witness (ZAW) is a public-safe v0.1 reference implementation of a defensive intake membrane for LLM workflows. It snapshots untrusted input, hashes the captured artifact, extracts useful content as evidence-only data, flags obvious instruction-like content, emits a safe prompt, and writes receipts.

The goal is not to prove that content is safe. The goal is to prevent external content from silently becoming authority inside the designed flow.

## Quick start

```bash
python3 -m unittest discover -s tests -v
python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"
python3 -m zaw.cli witness samples/injected_page.html --task "Summarize the refund policy"
bash scripts/run_verification.sh
```

A witness run creates a directory under `runs/` containing:

- `source_snapshot.txt`
- `source_snapshot.sha256`
- `extracted_text.txt`
- `evidence_packet.json`
- `warnings.json`
- `safe_prompt.md`
- `receipt.json`

`runs/` is intentionally ignored by git because it is generated local output.

## Install for local development

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -e .
zaw version
```

If your platform blocks direct system installs, use a virtual environment. Do not use system-package override flags unless you understand the risk.

## Main commands

```bash
python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"
python3 -m zaw.cli witness samples/injected_page.html --task "Summarize the refund policy"
python3 -m zaw.cli check-action samples/proposed_action_bad.json --greenlight samples/greenlight.json --evidence <run-dir>/evidence_packet.json
```

A hostile `check-action` should return `BLOCK` with a non-zero exit code. That is intentional blocking behavior, not a script failure.

## Descriptor binding (TOCTOU hardening)

Witnessing a tool/MCP descriptor (`zaw witness`-family, `witness_tool_descriptor`) also writes `descriptor_binding.json` next to the run receipt: the descriptor's source identity and its witness-time `sha256:` digest. An action that depends on a descriptor can declare it via the action's `descriptor` field and be gated against that binding:

```bash
python3 -m zaw.cli check-action proposed.json --greenlight samples/greenlight.json --evidence <run-dir>/evidence_packet.json --descriptor-binding <run-dir>/descriptor_binding.json
```

At action time the descriptor's current digest is re-checked against the bound one. A changed, missing, or unverifiable descriptor — or a missing, malformed, or mismatched binding — returns `BLOCK`. A valid binding proves only that the descriptor is identical to the captured UTF-8 text that was witnessed; it does not prove the descriptor is safe, and it grants no authority.

Descriptor binding checks apply to **local materialized descriptors**; remote
URL/MCP identities cannot be re-fetched by this verifier and fail closed. The CLI
uses `receipt.json` beside the explicitly selected `--evidence` packet as the
retained witness record. API callers must pass that original record separately
as `witness_receipt` to `evaluate_action` / `verify_descriptor_binding`. A binding
alone is insufficient. Its source and digest must match the receipt's source,
snapshot digest, and snapshot artifact hash before checking the current source.
Retain the original receipt in operator-controlled storage: these receipts are
not signed, and replacing the entire evidence store is outside this guarantee.
The comparison covers captured UTF-8 text (invalid bytes decode with replacement),
not arbitrary binary byte identity, and it does not make execution atomic with
the check or grant authority.

## Claim boundary

ZAW reduces first-contact authority risk on witnessed paths. It does not fully solve prompt injection, guarantee safety, prove that sources are trustworthy, prevent all exfiltration, or secure arbitrary tools.

Hashes prove artifact integrity, not safety.

See:

- `docs/CLAIM_BOUNDARY.md`
- `docs/EVIDENCE_PROMOTION_PROTOCOL.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/THREAT_MODEL.md`
- `docs/FULL_CATHEDRAL_TRAVERSAL_RECEIPT.md`

## Public-safe release state

This repository is suitable as a public proof / v0.1.0-rc1 reference implementation. It is not a deployed security product. Use it as evidence, reference code, and a foundation for further hardening.

## License and support

Zero Authority Witness is source-available under the **PolyForm Noncommercial License 1.0.0**. Noncommercial use is permitted under the included license; commercial use requires a separate written license from Corey Jacobs.

See `LICENSE`, `COMMERCIAL_LICENSE.md`, and `FUNDING.md`.
