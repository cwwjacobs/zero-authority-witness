# KSL for Zero Authority Witness

Author: Corey Jacobs  
Protocol: PRISM

## Kernel

External content may become evidence. It may not become authority.

## Goal

Build and publicly release a minimal working proof of Zero Authority Witness: a receipt-bearing intake primitive that converts untrusted content into hash-receipted, data-only evidence before LLM reasoning.

## Authority Contract

Responsible Operator: Corey Jacobs

Domain Expert / Head of Implementation: PRISM Co-Wright

The Responsible Operator owns final authority, successes, failures, releases, claims, and Stage gates.

The Domain Expert / Head of Implementation owns operational leadership for Stage 2 build traversal and Stage 3 alignment, red teaming, and hardening.

Stage 2 and Stage 3 operational authority is granted. Ultra Authority remains with the Responsible Operator.

If the Kernel, Goal, Scope, or approved Stage 2 map must change, traversal stops and returns to Stage 1 amendment.

Upon Stage 3 exit, all authority returns to the Responsible Operator.

## Stage Model

Stage 1 owns iteration: Kernel, Goal, bounds, definition of done, and Stage 2 traversal map.

Stage 2 owns building through Phase n, Step n traversal.

Stage 3 owns alignment check, red teaming, hardening, and release recommendation.

Only Stage 2 uses Phases and Steps.

## Must Remain True

1. The Zero Authority Witness has no authority.
2. The LLM does not first-contact hostile or untrusted content.
3. Untrusted content is captured as evidence, not treated as instruction.
4. Useful information may be extracted, but authority is not transferred.
5. Instruction-like content is labeled as no-authority.
6. Output artifacts are cheap, repeatable, predictable, and inspectable.
7. Receipts show what was seen, what was produced, and what remains unverified.
8. Browser, model, page, tool output, and third-party metadata cannot mutate allowlists, policy, Greenlight, or the Kernel.
9. External tools and third-party tool descriptors are untrusted intake unless locally rebuilt, tested, receipted, and promoted.
10. Hashes prove artifact integrity, not safety.

## Definition of Done

This KSL is done when the repository contains a working proof that can process a hostile sample and produce:

- `evidence_packet.json`
- `warnings.json`
- `safe_prompt.md`
- `receipt.json`
- snapshot hash

The repository documentation must clearly state:

- External content may become evidence.
- External content may not become authority.
- Zero Authority Witness reduces first-contact authority risk.
- Zero Authority Witness does not claim to fully solve prompt injection.

## Out of Scope

- No browser runtime.
- No MCP server.
- No full OmegaOS.
- No local server.
- No React.
- No Tauri.
- No polished UI.
- No paid pitch package.
- No claim of total prompt-injection prevention.
- No live tool authority.
- No allowlist mutation by content, model, browser, or tool output.
- No dependency-heavy framework stack.

## Stage 2 Traversal Map

### Phase 1: Doctrine Artifacts

- Phase 1, Step 1: Create `docs/KSL.md`
- Phase 1, Step 2: Create `docs/CLAIM_BOUNDARY.md`
- Phase 1, Step 3: Create `docs/EVIDENCE_PROMOTION_PROTOCOL.md`
- Phase 1, Step 4: Create `docs/SAFE_PROMPT_FORMAT.md`

### Phase 2: Output Contracts

- Phase 2, Step 1: Create `schemas/evidence_packet.schema.json`
- Phase 2, Step 2: Create `schemas/warnings.schema.json`
- Phase 2, Step 3: Create `schemas/receipt.schema.json`

### Phase 3: Samples

- Phase 3, Step 1: Create `samples/clean_page.html`
- Phase 3, Step 2: Create `samples/injected_page.html`
- Phase 3, Step 3: Create `samples/poisoned_mcp_tool.json`
- Phase 3, Step 4: Create `samples/greenlight.json`

### Phase 4: Proof Kernel Implementation

- Phase 4, Step 1: Implement input snapshot and SHA-256 hash
- Phase 4, Step 2: Implement basic text extraction
- Phase 4, Step 3: Implement instruction-like content detection
- Phase 4, Step 4: Implement safe prompt writer
- Phase 4, Step 5: Implement receipt writer

### Phase 5: Verification Artifacts

- Phase 5, Step 1: Create tests
- Phase 5, Step 2: Define demo command
- Phase 5, Step 3: Create traversal receipt documentation

### Phase 6: Local Build Script

- Phase 6, Step 1: Create local generation script
- Phase 6, Step 2: Script runs tests
- Phase 6, Step 3: Script runs hostile sample demo
