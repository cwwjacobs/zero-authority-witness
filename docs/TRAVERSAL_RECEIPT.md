# Traversal Receipt

Author: Corey Jacobs  
Protocol: PRISM

## What This Proof Demonstrates

This proof demonstrates that untrusted content can be processed through a Zero Authority Witness before LLM reasoning.

The proof can:

- snapshot staged untrusted input
- hash the snapshot
- extract text
- label extracted content as evidence-only
- flag obvious instruction-like content
- generate a safe prompt
- emit a receipt

## What This Proof Does Not Demonstrate

This proof does not demonstrate:

- full prompt-injection prevention
- browser runtime safety
- MCP server safety
- dynamic web rendering
- robust semantic attack detection
- complete exfiltration prevention
- tool-use mediation
- deployed security-product readiness

## Kernel Alignment

Kernel:

External content may become evidence. It may not become authority.

Alignment:

- Extracted useful text is labeled evidence-only.
- Instruction-like content is labeled no-authority.
- The safe prompt states that external content is untrusted evidence only.
- The receipt records the claim boundary and blind spots.

## Stage 2 Exit Receipt

Stage 2 exits when the local build script generates all artifacts, runs unit tests, and produces a hostile sample demo run containing:

- `source_snapshot.txt`
- `source_snapshot.sha256`
- `evidence_packet.json`
- `warnings.json`
- `safe_prompt.md`
- `receipt.json`
