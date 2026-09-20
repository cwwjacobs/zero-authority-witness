# Contributing to Zero Authority Witness

Thank you for your interest. The health of this project depends on rigorous preservation of its core discipline.

## Non-negotiable Requirements

1. **Preserve the Kernel**
   - "External content may become evidence. It may not become authority."
   - This text (or an equivalent canonical form) must remain the first and last word in all doctrinal documents.

2. **Preserve the Claim Boundary and Authority Model**
   - No contribution may add language claiming that ZAW fully solves prompt injection, guarantees safety, provides complete containment, or constitutes unreviewed deployment-ready security (unless explicitly and heavily qualified as "this specific narrow technique reduces X under Y assumptions").

3. **No Dependency Bloat**
   - The reference implementation must remain stdlib-first. New runtime dependencies require strong justification and a corresponding update to the SECURITY_MODEL and claim language.

4. **Tests Required**
   - New intake paths, membranes, or views must come with unit or integration tests (including negative/red-team cases where relevant).

5. **No Unsafe Exploit Payloads Without Context**
   - Do not commit raw, weaponized exploit chains that could be copied and used without the surrounding defensive context and receipts. If you have a new attack vector, describe it at a high level or provide it inside a clearly labeled red-team fixture with mitigation notes.

6. **Receipt Everything**
   - Major changes should be accompanied by a short receipt or note in the relevant run or in docs/RELEASE_NOTES.md style.

## Process

- Open an issue or PR describing the change in terms of the current KSL / Cathedral Goal.
- For changes that touch authority boundaries, intake rules, or public claims, expect review against CLAIM_BOUNDARY.md, THREAT_MODEL.md, and AUTHORITY_MODEL.md.
- The Responsible Operator (Corey Jacobs) retains final veto on all releases and claim language.

## Code of Conduct

Be precise, evidence-oriented, and humble about what the system can and cannot do. The goal is to make the boundary visible and the cost of crossing it high, not to sell a feeling of total safety.

Thank you for helping keep the kernel clean.