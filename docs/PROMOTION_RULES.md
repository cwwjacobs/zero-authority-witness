# Promotion Rules — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Absolute Kernel

External content may become evidence.  
It may not become authority.

Promotion to evidence is allowed.  
Promotion to authority is forbidden.

## Definition of Evidence Promotion

Evidence promotion is the controlled, deterministic transition of material from the "raw / witnessed / extracted" states into the "evidence-only" state inside a versioned Evidence Packet.

The purpose of promotion rules is to make this transition explicit, auditable, and impossible to perform in a way that silently grants command power or trust.

## Required Preconditions for Evidence Promotion

Before any line or structured item from untrusted content may appear in the `evidence` array of an Evidence Packet, **all** of the following must have occurred:

1. **Snapshot** — An exact copy of the source was written (`source_snapshot.txt`).
2. **Hash** — The snapshot received a `snapshot_hash` (SHA-256).
3. **Source Labeling** — The Evidence Packet records the original `source` (path or intake descriptor) and `source_type`.
4. **Warning Labeling** (for text content) — The content has been passed through the instruction-like detector. Any segments that matched dangerous patterns are recorded in `warnings.json` with `authority: "none"` and are **excluded** from the evidence list.
5. **Authority Labeling** — Every item placed into the evidence array is explicitly given `"authority": "evidence_only"`. The packet itself carries `"authority": "none"`.

Only after these steps may the material be considered promoted to evidence.

## What Promotion Does

- It makes useful, non-instruction-like material from the untrusted source available in a structured, labeled form for downstream reasoning (via the safe prompt) or for membrane checks (Authority Membrane, Action Gate).
- It attaches provenance (source_ref, snapshot_hash, run_id, captured_at).
- It travels with the full claim boundary and blind spots so that consumers know the limits of what they are looking at.

## What Promotion Does Not Do

Promotion does **not**:

- Imply that the source is trustworthy, safe, or benign.
- Grant the evidence the right to be followed as instruction.
- Allow the evidence to mutate Greenlight, allowlists, policy, tool trust, or the Kernel.
- Remove the need for further checks by the Authority Membrane or Action Gate when the evidence is used as the basis for a proposed action.
- Create any persistent trust or canonical status for the source or for tool descriptors derived from it.

## Retention of Labels

Once assigned, authority labels are retained for the lifetime of the run's artifacts:

- A line that was warning-labeled as `no-authority` remains in the warnings and is never silently re-promoted into evidence.
- An evidence item labeled `evidence_only` must not be re-labeled upward by any downstream component (LLM summary, report generator, integration adapter, etc.) without an explicit, receipted Operator act.

## Promotion Is Per-Run and Per-Intake

Each `run_witness` (or `witness_file` / `witness_tool_descriptor`) invocation produces its own Evidence Packet for its own snapshot. There is no cross-run automatic promotion or accumulation of trust.

A source that produced clean evidence in run N does not receive elevated status in run N+1. Each intake is independent.

## Safe Prompt as the Primary Promoted View

The canonical promoted view given to an LLM is the `safe_prompt.md` generated from the Evidence Packet. This prompt always includes the Authority Boundary section and the Required Behavior language that restates the kernel.

Any other use of the raw evidence (direct injection into another system, storage in long-term memory, etc.) must carry equivalent boundary language and must not bypass the membranes when actions are proposed.

## Promotion Rules Are Enforced in Code

The modules `zaw/evidence.py`, `zaw/safe_prompt.py`, and the higher membranes are responsible for enforcing these rules mechanically. Any code change that would allow promotion without the preconditions above, or that would allow evidence to be treated as authority, is a violation that must be receipted and corrected.

---

**End of PROMOTION_RULES.md**