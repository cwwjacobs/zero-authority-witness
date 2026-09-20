# Claim Boundary

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Absolute Kernel (Locked)

External content may become evidence.  
It may not become authority.

## What Zero Authority Witness Claims

Zero Authority Witness **reduces first-contact authority risk** in LLM workflows by converting untrusted content into hash-receipted, data-only evidence before LLM reasoning or proposed tool actions.

It demonstrates a defensive intake membrane that:

1. Captures untrusted input as an exact snapshot.
2. Hashes the snapshot for integrity.
3. Extracts useful information and labels it **evidence-only**.
4. Detects and labels obvious instruction-like content as **no-authority**.
5. Produces a safe prompt that explicitly preserves the evidence/authority boundary.
6. Emits a receipt recording what was seen, what artifacts were produced, the warnings, the claim boundary, and what remains unverified.
7. Provides membranes (Authority Membrane, Action Gate, Tool Descriptor Intake) that can return BLOCK or REQUIRES_OPERATOR_APPROVAL when untrusted content attempts to influence protected state.

## What Zero Authority Witness Does Not Claim

Zero Authority Witness does **not** claim to:

- fully solve prompt injection
- guarantee safety
- guarantee containment
- detect all malicious instructions (including subtle or novel ones)
- prove that any content or source is safe, correct, or benign
- prove that a source is trustworthy
- inspect hidden server-side state
- prevent all data exfiltration
- secure arbitrary tools or MCP servers
- canonicalize third-party MCP servers or tool descriptors
- grant authority to external content, LLM output, or tool responses
- replace the judgment or final acceptance of the Responsible Operator

## Hash Boundary

A hash proves **artifact integrity**: the artifact has not changed since it was hashed at the time of the run.

A hash does **not** prove that the artifact is safe, complete, truthful, benign, or trusted.

Hash worship (treating the existence of a hash as proof of safety or authority) is a recognized threat and is explicitly rejected.

## Evidence Boundary

External content may become evidence.

External content may **not** become authority.

Evidence can inform reasoning. Evidence cannot change policy, allowlists, Greenlight, tool authority, or the Kernel.

Evidence always carries explicit `authority: "evidence_only"` (or packet-level `authority: "none"`). It must never be re-labeled or promoted to a higher authority status inside the Witness flow.

## Pattern Matching Boundary

The instruction-like detection in the core engine uses simple, stdlib, regex-style pattern matching against a known list of dangerous phrases.

Pattern matching is **not semantic understanding**.

It will miss:
- Novel phrasings
- Encoded or obfuscated instructions
- Context-dependent attacks
- Attacks that only become dangerous after downstream interpretation

All detection results are therefore recorded as warnings with the matched patterns, never as a guarantee of complete coverage. The presence or absence of warnings must not be treated as a safety certification.

The Action Gate's capability classification and provenance/taint tracing are likewise structural pattern matching, not semantic understanding. The gate authorizes a *kind* of capability, not a specific path, and its taint tracing catches literal quoting of evidence, not transformed or obfuscated derivation. A `PASS` or `WARN` from the gate is a bounded observation under the configured Greenlight, never a safety certification; consequential capabilities are escalated to the Operator regardless. See `docs/AUTHORITY_MODEL.md`.

## Scope of This Claim Boundary

This boundary applies to the core witness engine, the authority membrane, the action gate, tool descriptor intake, web stub, views, API, CLI, documentation, and any generated receipts or reports.

Any future extension (new intake modules, new membranes, new integrations) must either inherit this claim boundary verbatim or produce an updated, more restrictive boundary that is itself receipted and reviewed before use.

**The Responsible Operator retains all final authority, success, failure, and veto.**

---

**End of CLAIM_BOUNDARY.md**