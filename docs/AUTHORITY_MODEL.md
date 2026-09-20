# Authority Model — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Absolute Kernel (Locked)

External content may become evidence.  
It may not become authority.

## Fundamental Rule

**Authority is granted only by the Responsible Operator (or by structures the Operator has explicitly and receiptedly placed in control).**

No component of the Zero Authority Witness, no LLM, no tool output, no webpage, no MCP descriptor, and no piece of evidence may create, transfer, or exercise authority on its own.

## Who / What Can Grant Authority

| Source                        | Can Grant Authority? | Notes |
|-------------------------------|----------------------|-------|
| Responsible Operator (human)  | Yes (primary)        | Explicit will, recorded in Greenlight, allow manifests, or direct approval receipts. |
| Browser / renderer / viewer   | No                   | The view has no authority over allowlists, Greenlight, or Kernel. |
| LLM output / reasoning        | No                   | The model receives evidence only and may not mutate protected state. |
| Tool output / MCP responses   | No                   | Third-party tool results are further untrusted intake. |
| Third-party metadata / descriptors | No              | MCP servers and tool schemas are witnessed as untrusted content. |
| Evidence Packet content       | No                   | Evidence informs; it does not command or promote itself. |
| Hashes                        | No                   | Hashes prove integrity of artifacts, never safety or authority. |
| Previous runs / "we did this before" | No             | Each intake and each action decision stands on its own receipts. |

## What Evidence and Untrusted Content May Never Do

Evidence and untrusted content are forbidden from:

- Becoming or being treated as policy
- Being added to any allowlist or allow manifest
- Mutating or expanding Greenlight
- Granting trust or canonical status to a tool or origin
- Altering the Kernel or the claim boundary
- Causing the system to treat the content as instruction ("do what this says")
- Silently changing the scope of a session without an explicit Operator receipt

## The Authority Membrane (Enforcement Layer)

The `zaw/authority/` modules exist to make the above rules mechanically enforceable:

- `greenlight.py` — loads and validates Operator-authored Greenlight documents.
- `capability.py` — deterministically classifies what a proposed action's **operands** (action_type, target, parameter values) would actually do, into capability tags (secret_access, data_egress, code_execution, state_mutation, instruction_execution, filesystem_read/write). The same lexicon classifies Greenlight `allowed`/`not_allowed` phrases, so scope is compared like-with-like.
- `causality.py` — traces **provenance**: whether the action's operands quote or embed content the Witness captured from an untrusted source, by matching significant tokens (URLs, paths, identifiers) against the evidence + warning corpus. This is structural; it does **not** read any self-reported origin field on the action.
- `mutation_guard.py` — detects attempts (in content or proposed actions) to mutate protected structures and forces a BLOCK.
- `gate.py` — combines the above into the decision (`evaluate_action` / `decide_action`).
- `allow.py` — secondary allow/deny-manifest checker for explicit `allowed_actions`/`denied_actions` manifests.
- `scope_delta.py` — thin facade over the gate for callers that import `compute_scope_delta`.

No amount of "the evidence says this is fine", "the tool descriptor claims it is safe", or a benign-sounding `reason` field is allowed to bypass these checks. The action's narration of itself is not an operand.

### How the Action Gate decides (deterministic, default-deny)

The verdict is computed from **capability × provenance**, first matching rule wins:

1. Action would mutate protected authority/state (or the mutation guard fires) → **BLOCK** (forbidden promotion).
2. Action would treat untrusted content as instruction → **BLOCK**.
3. A capability the Greenlight lists in `not_allowed` is present → **BLOCK**.
4. A **high**-severity operand traces to witnessed untrusted evidence (taint) → **BLOCK** (external content driving a consequential action).
5. Reads secret material **and** moves data off-boundary in one action → **BLOCK**.
6. Otherwise a high-severity capability is **never silently PASSed**: `WARN` only if it is explicitly within Greenlight and untainted, else `REQUIRES_OPERATOR_APPROVAL`.
7. Tainted (non-high) → `REQUIRES_OPERATOR_APPROVAL`. Medium (filesystem) within Greenlight → `PASS`, else `REQUIRES_OPERATOR_APPROVAL`. Low/none within Greenlight → `PASS`. A declared `persistence` raises any `PASS`/`WARN` to `REQUIRES_OPERATOR_APPROVAL`.

Every `check-action` writes an `action_decision_receipt.json` recording the verdict, the capabilities detected, the taint matches, and the reasons.

**Honest blind spots of this gate (it does what it says, and no more):**

- Capability classification is **pattern matching, not semantics** — it authorizes a *kind* of capability, not a specific path. It cannot distinguish "read the staged input" from "read `/some/other/file`" of the same kind; the Operator must keep Greenlights tight and review `PASS`/`WARN` on medium capabilities.
- Taint tracing catches **literal** quoting/embedding of evidence. An attacker who encodes, paraphrases, or reassembles evidence before placing it in an operand can evade taint detection — which is why high-consequence capabilities require Operator authorization regardless of detected taint.
- The gate decides whether an action *may proceed on this basis*; it does not execute, sandbox, or roll back anything.

## Greenlight and Allow Manifests Are Operator Artifacts

- A Greenlight is not derived from content. It is authored or explicitly approved by the Responsible Operator for a specific goal and scope.
- An allow manifest is likewise an Operator-controlled declaration.
- Both travel with receipts when they are used to make decisions.
- If a proposed action would require changing the Greenlight or allow manifest, that change itself must be an explicit Operator act, not an automatic consequence of evidence.

## Action Decisions and Authority

When `check-action` (or equivalent higher gate) is used:

- The decision receipt records the verdict and the `authority_granted` status (almost always false for content-derived proposals).
- A verdict of `REQUIRES_OPERATOR_APPROVAL` means a human must consciously review the full receipt, warnings, and scope delta and then explicitly approve (or modify the Greenlight).
- A verdict of `BLOCK` means the action must not proceed on the basis of the witnessed material.

## LLM and Agent Integration

The only sanctioned path from untrusted content to an LLM is through a **safe prompt** generated by the Witness. The safe prompt contains the explicit Authority Boundary language and the Required Behavior section that repeats the kernel.

Even when the LLM is given a safe prompt, the output of the LLM is still not authority. Any action the LLM proposes must still pass through the Action Gate / Authority Membrane if it would affect protected state.

## Third-Party Tools and MCP Servers

See also the Tool Descriptor Intake rules (PHASE 6).

- A third-party tool descriptor may be parsed and risk-classified.
- It may contribute to a local rewrite template (with prominent TODOs and warnings).
- It must never be treated as CANONICAL or trusted simply because it was successfully witnessed or because a receipt exists for it.
- Canonical status requires local rebuild, testing, receipting, and explicit Operator promotion recorded outside the automatic intake flow.

## Summary Table — Authority Flow

- Raw untrusted content → always `raw` / `witnessed`
- After snapshot + hash → `snapshotted` / `hashed`
- After extraction + labeling → `evidence-only` or `no-authority` (never higher)
- Operator Greenlight / allow manifest → the only structures that can legitimately influence verdicts toward PASS
- Proposed action that traces to evidence or exceeds scope → BLOCK or REQUIRES_OPERATOR_APPROVAL
- Final human approval (when required) → recorded in a decision receipt with `authority_granted` context

## Violations

Any code path, documentation statement, integration, or runtime behavior that allows untrusted content or evidence to mutate protected state, or that treats a third-party descriptor as canonical without the required local steps, is a violation of the Authority Model.

Such violations must be treated as defects, receipted, and corrected. They must not be rationalized by "the model wanted it" or "the evidence looked clean."

---

**The Responsible Operator is the sole source of authority. Everything else is evidence, warning, or guardrail.**

**End of AUTHORITY_MODEL.md**