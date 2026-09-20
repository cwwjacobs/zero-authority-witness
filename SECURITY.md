# Security Policy

## Responsible Disclosure

If you discover a vulnerability or a way the Zero Authority Witness can be made to violate its own kernel, please report it privately.

Preferred contact: coresynth@gmail.com

Please do **not** submit live secrets, production credentials, or complete weaponized exploit chains in public issues.

## Scope

This policy covers the reference implementation: the `zaw` package, proof kernel, schemas, documented membranes, verification script, and governance artifacts.

It does **not** cover:

- Downstream integrations built on top of ZAW.
- The security of any LLM, MCP server, or external content fed into ZAW.
- Browser or operating-system level issues outside the stdlib components.

## What We Consider Security-Relevant

- Any code path that performs a forbidden promotion, such as evidence to authority, evidence to Greenlight mutation, or third-party descriptor to canonical trust without explicit external approval.
- Failures of mutation guard, scope-delta, or action-gate logic that are not clearly labeled in receipts.
- Witness View artifacts, especially HTML reports, that can become active exfiltration channels despite the render guard.
- Silent broadening of claims in documentation or generated output.

Thank you for helping keep the boundary honest.

**The kernel is the security boundary. Everything else is evidence.**
