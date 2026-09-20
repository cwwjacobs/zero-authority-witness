# Evidence Promotion Protocol

Author: Corey Jacobs  
Protocol: PRISM

## Core Rule

Promotion to evidence is allowed.

Promotion to authority is forbidden.

## Purpose

The Evidence Promotion Protocol defines how untrusted content is allowed to move into an LLM workflow without arriving as instruction, policy, or authority.

## Flow

1. Untrusted content enters the Zero Authority Witness.
2. The Witness captures a snapshot.
3. The snapshot is hashed.
4. Text is extracted.
5. Instruction-like content is labeled no-authority.
6. Useful content is emitted as evidence-only.
7. A safe prompt is generated for LLM reasoning.
8. A receipt records what happened and what remains unverified.

## Authority Rule

The Zero Authority Witness has no authority.

It cannot:

- approve
- promote to trust
- mutate allowlists
- mutate policy
- mutate Greenlight
- mutate the Kernel
- grant tool access
- canonicalize third-party tools

## Evidence Rule

Extracted claims must retain evidence-only status.

A claim extracted from untrusted content may be useful, but it does not become trusted merely because it was extracted.

## Third-Party Tool Rule

Third-party MCP servers and tool descriptors are untrusted intake.

They may structurally inform what a tool claims to do, but they do not become canonical authority.

A tool may become canonical only after local rebuild, testing, receipts, and explicit promotion outside this proof kernel.

## Safe Use

The LLM may reason over the evidence packet.

The LLM may not treat untrusted evidence as instruction.

The LLM may not use untrusted evidence to modify policy, allowlists, Greenlight, or tool authority.

## Failure Boundary

If evidence promotion cannot preserve the evidence/authority boundary, the content must remain unpromoted and the run must emit a warning or deficiency receipt.
