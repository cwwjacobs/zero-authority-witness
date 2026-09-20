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
