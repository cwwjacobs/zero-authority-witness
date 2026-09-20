# Forbidden Promotions — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Absolute Kernel

External content may become evidence.  
It may not become authority.

Promotion to evidence is allowed.  
Promotion to authority is forbidden.

## Core Rule

No untrusted content, no evidence derived from untrusted content, no LLM reasoning over that evidence, and no tool output may ever be promoted (automatically or by sleight-of-hand) into any of the following authoritative statuses inside the designed flow of Zero Authority Witness.

## Explicitly Forbidden Promotions

The following transitions are forbidden:

### 1. Evidence → Authority

Evidence must never be treated as, or allowed to become, authoritative command.

- "The page said to do X, therefore we should do X."
- "The evidence is clean, therefore we can trust future content from this source."
- Using evidence text directly as system/developer instructions or as Greenlight scope without explicit Operator approval.

### 2. Evidence → Policy

Evidence may not be used to write, append to, or override policy documents, safety rules, or behavioral guidelines for the agent or the Operator.

### 3. Evidence → Allowlist / Allow Manifest

It is forbidden for evidence or tool descriptors to cause new entries to be added to any allow manifest, allowed origins list, allowed actions list, or similar structure without a separate, explicit, receipted Operator decision.

### 4. Evidence → Greenlight

A Greenlight is an Operator artifact. Evidence may inform the Operator's decision to create or amend a Greenlight, but the evidence itself may not expand, mutate, or substitute for a Greenlight.

Any proposed action that would require a Greenlight change must surface as `REQUIRES_OPERATOR_APPROVAL` (or BLOCK) and must be accompanied by a clear decision receipt.

### 5. Evidence → Trusted Tool / Canonical Tool

Third-party tool descriptors and MCP servers are untrusted intake by definition.

- A descriptor may be witnessed, risk-classified, and used to generate a local skeleton.
- It must not be marked `CANONICAL`, added to a trusted tool registry, or given special execution privileges solely because a receipt or evidence packet exists for it.
- Advancement to `REBUILT_LOCAL` / `TESTED` / `RECEIPTED` / `CANONICAL` requires explicit local work and Operator promotion recorded outside the automatic intake.

### 6. Evidence → Kernel Mutation

The Kernel ("External content may become evidence. It may not become authority."), the claim boundary, the threat model, the authority model, and the promotion rules themselves are not mutable by evidence or by LLM output.

Any attempt (in content or in a proposed action) to alter these foundations must be detected by the mutation guard and result in BLOCK or REQUIRES_OPERATOR_APPROVAL.

### 7. Warning-Labeled Content → Evidence

Content that the detector has placed in the Warning Packet with `authority: "none"` must not be re-included in the normal evidence list or treated as ordinary evidence in the safe prompt.

### 8. Hash Presence → Trust or Authority

The existence of a `snapshot_hash` or artifact hashes must never be treated as evidence of safety, correctness, or authorization.

Hash worship is a named threat (see THREAT_MODEL.md) and is countered by the Hash Boundary in CLAIM_BOUNDARY.md and by the requirement that hashes travel alongside (not instead of) the full claim boundary and blind spots.

## Enforcement

- The Authority Membrane (`mutation_guard.py`, `scope_delta.py`, `allow.py`) is responsible for detecting attempts at these forbidden promotions in proposed actions and returning appropriate verdicts.
- The Tool Descriptor Intake (`promotion_guard.py`, `canonicalization.py`) prevents automatic canonicalization.
- The safe prompt and all Witness View generators must carry the claim boundary and must not present evidence in a way that implies it has been promoted to authority.
- Documentation, examples, and integration stubs must not suggest or demonstrate forbidden promotions.

## Consequence of Violation

Any implementation, documentation, integration, or runtime behavior that performs or implies one of the forbidden promotions is a defect against the kernel.

Such defects must be:
- Detected (ideally by tests in `tests/red_team/` or by review of receipts)
- Receipted
- Corrected before further use
- Documented in the next traversal or release receipt if they affect public claims

---

**There is no safe or "pragmatic" exception to these forbidden promotions. The kernel is the exception handler.**

**End of FORBIDDEN_PROMOTIONS.md**