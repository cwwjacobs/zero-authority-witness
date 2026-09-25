# Operator Guide — Using Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## The Basic Loop (for a human Operator)

1. You have untrusted content (a webpage, a document, an MCP tool descriptor, a JSON payload, pasted text, etc.).
2. You stage it (or point ZAW at the file/URL descriptor).
3. You run the Witness with a clear task / Greenlight goal:
   ```
   python3 -m zaw.cli witness path/to/untrusted.html --task "Summarize the refund policy"
   ```
   or the compat form:
   ```
   python3 zaw.py path/to/untrusted.html --task "..."
   ```
4. You inspect the run directory (latest under `runs/`):
   - Look at `warnings.json` first.
   - Read the `receipt.json` (especially `verdict`, `claim_boundary`, `blind_spots`).
   - Review `safe_prompt.md` to see exactly what the LLM will be shown.
5. If you need to act on the evidence, propose the action and (where implemented) run it through the action gate:
   ```
   python3 -m zaw.cli check-action proposed.json --greenlight samples/greenlight.json --evidence runs/.../evidence_packet.json
   ```
   If the action depends on a witnessed tool/MCP descriptor, declare it in the action's `descriptor` field and pass the run's binding so the descriptor is re-verified at action time:
   ```
   python3 -m zaw.cli check-action proposed.json --greenlight samples/greenlight.json --evidence runs/.../evidence_packet.json --descriptor-binding runs/.../descriptor_binding.json
   ```
   A descriptor that changed since witnessing is BLOCKed. The binding proves captured text identity against the retained witness receipt only — review the receipt either way.
6. Only proceed with actions that receive PASS (or that you have explicitly approved after a REQUIRES_OPERATOR_APPROVAL receipt).

## Greenlight and Scope

Keep a living `greenlight.json` (or equivalent) that states the current goal and the explicitly allowed / not-allowed actions for this session.

ZAW will never expand your Greenlight for you. Evidence can only inform your decision to change it.

## Reviewing Tool Descriptors

When you encounter a new MCP server or tool:

- Run it through the tool descriptor witness path (or simply `zaw witness` on the JSON).
- Examine the risk flags and any warnings found in description or schema fields.
- Assume the descriptor is hostile until you have locally rebuilt, tested, and receipted a safe wrapper.
- Never let a "looks clean in the summary" receipt become an automatic trust decision.

## What Good Operator Behavior Looks Like

- You treat every new run as independent.
- You read the warnings and the full receipt before acting.
- You keep Greenlight and allow manifests as small and explicit as possible.
- You record your approvals (when required) as decision receipts.
- You update the claim boundary language if you ever extend the system.

## What Bad Operator Behavior Looks Like

- "The model got the safe prompt, the receipt says PASS_WITH_NOTES, we're good."
- Ignoring the warnings section because the evidence list looked useful.
- Letting a proposed action that touches private files or mutates policy go through because "the evidence suggested it".
- Accumulating "temporary" trust in a source across many runs without a recorded review.

The system is designed to make the bad path visible and expensive. It cannot make the bad path impossible if the Operator chooses to ignore the receipts.

---

Use the Witness. Read the receipts. The Operator holds authority.
Descriptor checks require the original operator-retained witness receipt; replacing
the descriptor and binding alone cannot replace that witnessed identity. Entire
evidence-store replacement is outside this unsigned integrity model. Remote
descriptors must be materialized locally; no live remote re-fetch is implemented.
