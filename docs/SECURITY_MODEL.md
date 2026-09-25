# Security Model — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Assumptions

- The Operator is a competent human who will actually read receipts and warnings for high-stakes work.
- The machine running ZAW is under the Operator's control (or a trusted build environment).
- Untrusted content is staged locally before the Witness sees it (or fetched only through the explicit, bounded web stub when the Operator deliberately invokes it).
- The stdlib and the Python interpreter itself are part of the trusted base (as with any pure-Python tool).

## What ZAW Protects Against (on the Witnessed Path)

- First-contact prompt injection and obvious hidden instructions in the staged content.
- Classic tool descriptor poisoning (instructions in description or schema fields).
- Attempts to launder evidence into policy, allowlists, or Greenlight without Operator involvement (via the Authority Membrane and action gate).
- Rug-pulls on locally materialized tool/MCP descriptors that are gated through the action gate: the descriptor's digest is re-checked against `descriptor_binding.json` at action time and a changed identity is BLOCKed (detection at use time, not prevention of change).
- Silent mutation of protected state by untrusted content.
- Exfiltration via generated reports (render guard + inert HTML).

## What ZAW Does Not Protect Against

- Attacks that reach the LLM through other channels (direct user messages, previous context, RAG, fine-tuning, etc.).
- Novel or heavily obfuscated instructions that the simple pattern detector misses.
- Supply-chain attacks against the Python stdlib or the host OS.
- Operator error (ignoring warnings, approving dangerous actions after a REQUIRES receipt, accumulating "temporary" trust).
- TOCTOU on live remote sources unless the Operator uses snapshot delta, re-witnesses, or (for locally materialized tool/MCP descriptors) gates the action on `descriptor_binding.json`.
- Anything after the safe prompt leaves the Witness (the model can still be socially engineered by the *evidence* it is shown).

## Failure Modes

- The Operator treats a clean receipt as a safety certification.
- A downstream agent or UI hides the warnings or the full receipt.
- Evidence is stored long-term and later treated as trusted context without re-witnessing.
- The Greenlight or allow manifest is allowed to drift without receipts.

## Defense in Depth Recommendations

- Keep Greenlights small and explicit.
- Review warnings before every high-stakes action.
- Re-witness live sources when time has passed or the remote is untrusted.
- Use the action gate / check-action for anything that would read private data or mutate state.
- Treat all generated reports and safe prompts as potentially sensitive (they contain extracted content).

This is a membrane, not a fortress. Its job is to make the boundary legible and to force explicit Operator acts where authority would otherwise leak.

See also THREAT_MODEL.md and CLAIM_BOUNDARY.md.
Descriptor checks require the original operator-retained witness receipt; replacing
the descriptor and binding alone cannot replace that witnessed identity. Entire
evidence-store replacement is outside this unsigned integrity model. Remote
descriptors must be materialized locally; no live remote re-fetch is implemented.
