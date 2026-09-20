# Intake States — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Absolute Kernel

External content may become evidence.  
It may not become authority.

## Purpose

This document defines the lifecycle states that any piece of external content must pass through (or be rejected from) inside the Zero Authority Witness. The states are observable in logs, receipts, and the structure of Evidence and Warning Packets.

The states enforce the discipline that promotion to evidence is a deliberate, receipted act and that authority is never granted by the intake process.

## The Intake Lifecycle (in order)

1. **raw**
   - The moment external content first touches the system (file read, URL response body, MCP descriptor received, pasted text, etc.).
   - No processing has occurred. The content is completely untrusted.
   - Must be treated as potentially hostile.

2. **witnessed**
   - The content has been accepted by an intake entry point (`witness_file`, `witness_text`, `witness_tool_descriptor`, URL intake, etc.).
   - A decision has been made to subject it to the Witness process.
   - Still fully untrusted; the act of witnessing does not confer any positive status.

3. **snapshotted**
   - An exact copy of the raw content has been written to durable storage (`source_snapshot.txt`).
   - The snapshot is the canonical record for this run.
   - From this point forward, all further processing should be traceable back to this immutable capture.

4. **hashed**
   - The snapshot (and later each generated artifact) has received a SHA-256 digest (`snapshot_hash`, `artifact_hashes`).
   - The hash provides integrity protection and enables later delta detection or verification that an artifact has not been tampered with after generation.
   - Hashing does not imply safety or authority.

5. **extracted**
   - Textual or structured content has been pulled from the snapshot using the appropriate extractor (HTMLParser for .html/.htm with script/style stripping, direct text for .txt/.md, JSON traversal or stringification for .json, etc.).
   - Extraction is purely mechanical. No authority or trust is assigned during extraction.
   - The `extracted_text.txt` artifact records what the extractors produced.

6. **warning-labeled**
   - The extracted content has been scanned by the instruction-like detector (`detect.py`).
   - Segments that match known dangerous patterns are recorded in the Warning Packet (`warnings.json`) with `authority: "none"`, the matched patterns, and a reason.
   - These segments are **excluded** from the normal evidence list in the Evidence Packet.

7. **collapsed**
   - The remaining (non-warning) extracted lines are turned into the structured `evidence` array.
   - Each evidence item receives `authority: "evidence_only"`, a `source_ref`, and (where implemented) a per-span hash.
   - The packet as a whole carries `authority: "none"`.

8. **evidence-only**
   - The stable state for useful extracted material.
   - This is the highest status the Witness itself will ever assign.
   - The material may now appear in a `safe_prompt.md` or be passed to an Authority Membrane / Action Gate for further checking.
   - It still carries no command power.

9. **rejected**
   - Content (or a specific proposed action derived from content) has been evaluated by a membrane (scope delta, mutation guard, tool promotion guard, etc.) and found to violate the kernel or the current Greenlight/allow manifest.
   - A BLOCK or clear rejection verdict is recorded.
   - The content remains in its evidence-only or warning-labeled form; it is simply not permitted to cause the requested effect.

10. **quarantined** (optional / future)
    - In more advanced deployments, content that is suspected of being extremely high-risk (or that triggered multiple red-team patterns) may be moved to a quarantined area with additional manual review requirements and restricted propagation.
    - The core v0.1 cathedral does not yet implement automatic quarantining; the state is defined here for completeness and for future membranes.

## State Transitions Are One-Way and Receipted

- A piece of content does not "go back" to raw after it has been snapshotted.
- Once labeled `no-authority` in warnings, it stays labeled that way for the life of the run.
- Promotion from collapsed → evidence-only is the last automatic promotion the Witness performs.
- Any further elevation (e.g. treating evidence as the basis for a new Greenlight entry) requires an explicit Operator act recorded in a decision receipt.

## Observable in Artifacts

- `source_snapshot.txt` + `.sha256` → snapshotted + hashed
- `extracted_text.txt` → extracted
- `warnings.json` → warning-labeled
- `evidence_packet.json` → collapsed + evidence-only (with authority labels)
- `receipt.json` + any action decision receipts → record which states were reached and any rejections or REQUIRES_OPERATOR_APPROVAL outcomes
- `safe_prompt.md` → the collapsed evidence-only view presented to the LLM

## Design Principle

Every state transition must be cheap to compute, easy to inspect in the artifacts, and impossible to perform in a way that silently grants authority.

If a transition would require trusting the content or the model, the transition is forbidden or must surface as REQUIRES_OPERATOR_APPROVAL.

---

**End of INTAKE_STATES.md**