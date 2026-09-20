# Cathedral Goal — Zero Authority Witness v0.1

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Absolute Kernel (Locked)

> External content may become evidence.  
> It may not become authority.

This kernel is non-negotiable. Every component, every artifact, every decision in the cathedral must preserve this boundary.

## Primary Goal

Build a public-safe v0.1 reference version of Zero Authority Witness: a receipt-bearing intake membrane for LLM workflows where external content, webpages, documents, MCP/tool descriptors, and proposed actions are witnessed, snapshotted, hashed, collapsed into data-only evidence, checked against authority boundaries, and receipted before any model/tool action can treat them as authority.

The system reduces first-contact authority risk, preserves provenance, surfaces instruction-like content, and prevents untrusted content from directly mutating allowlists, Greenlight, policy, tools, or Kernel authority inside the designed flow.

## What "Cathedral" Means

"Cathedral" denotes a complete, coherent, vaulted structure built according to a rigorous plan (this Stage 2 Traversal Map), not a collection of ad-hoc scripts or a minimal proof alone.

It means:

- A factored, importable, testable Python package (`zaw`) with clear module boundaries.
- Stable, versioned JSON schemas for all major artifacts.
- Layered membranes (evidence promotion, authority, action gate, tool descriptor intake).
- Multiple output views (CLI summary, Markdown reports, inert HTML reports).
- A rich, committed test corpus covering benign, obvious injection, hidden injection, tool poisoning, and authority laundering cases.
- Governance and public-good release artifacts.
- Receipts at every significant stage, including this full traversal receipt.
- Strict adherence to stdlib-first, no-dependency, inspectable, repeatable, cheap artifacts.
- Explicit, documented claim boundaries and threat model.

The cathedral is the full realization of the 16-Phase Stage 2 Traversal Map. It is production-*shaped* (structured, reviewable, extensible, governed) while remaining deliberately minimal in runtime dependencies and claims.

## What the Cathedral Includes

- **Core Witness Engine** (factored from the proof kernel): snapshot, hash, extract (HTML/text/JSON/MD), detect instruction-like patterns, evidence packet, safe prompt, receipt.
- **Authority Membrane** (`zaw/authority/`): Greenlight loading and shape checking, allow/deny manifest checking, mutation guard, scope delta detection.
- **Proposed Action Gate** (`zaw/action/`): causality estimation, verdict (PASS/WARN/BLOCK/REQUIRES_OPERATOR_APPROVAL), action decision receipts.
- **MCP / Tool Descriptor Intake** (`zaw/tools/`): descriptor witness, risk classifier (filesystem, network, shell, exfil, policy mutation, etc.), canonicalization status (third-party descriptors start as INTAKED/MAPPED, never auto-CANONICAL), safe local rewrite template generator, promotion guard.
- **Bounded Static Web Witness Stub** (`zaw/web/`): URL intake, optional stdlib urllib fetch (explicit, no cookies, timeout, recorded blind spots), snapshot delta, web-specific blind spots. No browser engine.
- **Witness Views** (`zaw/view/`): operator-facing CLI summary, Markdown report generator, inert local-only HTML report (no scripts, no remote loads), render guard against exfiltration channels.
- **Test Corpus & Harness**: fixtures for benign, obvious injection, hidden injection, tool poisoning, authority laundering; unit, integration, red-team, and golden tests.
- **Public API & CLI**: `zaw/api.py`, `zaw/cli.py` (witness, check-action, version), console script entrypoint.
- **Packaging**: `pyproject.toml` (stdlib-only, setuptools, zero runtime deps), `__version__`, editable install support.
- **Documentation Suite**: CATHEDRAL_GOAL, LEXICON, strengthened CLAIM_BOUNDARY, THREAT_MODEL, AUTHORITY_MODEL, INTAKE_STATES, PROMOTION_RULES, FORBIDDEN_PROMOTIONS, WITNESS_VIEW, OPERATOR_GUIDE, DEVELOPER_GUIDE, SECURITY_MODEL, FAQ, RELEASE_CHECKLIST, FULL_CATHEDRAL_TRAVERSAL_RECEIPT.
- **Governance / Public-Good Release**: NOTICE, CITATION.cff, FUNDING.md, CONTRIBUTING.md, SECURITY.md, RELEASE_NOTES.md.
- **Receipts & Verification**: `receipts/` directory, `scripts/run_verification.sh`, full traversal receipt.
- **Compatibility Layer**: root `zaw.py` remains a working entrypoint for the original proof demo command and existing test expectations during transition.
- **Examples & Integration Stubs**: local agent workflow example, MCP safe adapter stub, browser witness stub.

All outputs remain cheap, repeatable, predictable, inspectable JSON/Markdown/text artifacts.

## What the Cathedral Explicitly Excludes (Per Constraints)

- No React, no frontend framework.
- No Tauri, no desktop packaging in core.
- No local web server or HTTP service.
- No heavyweight frameworks or third-party runtime dependencies.
- No hidden or automatic remote calls (network only in the explicit, opt-in, bounded `zaw/web/raw_fetch.py` module when deliberately invoked).
- No telemetry, no phoning home.
- No browser automation (Playwright, Selenium, Chromium, etc.) required for core tests or functionality. The web stub is stdlib urllib only and optional.
- No claim that the system fully solves prompt injection, guarantees safety, provides complete containment, or constitutes unreviewed deployment-ready security.
- No automatic canonicalization or trust of third-party MCP/tool descriptors.
- No mutation of Greenlight, allowlists, policy, Kernel, or tool authority by evidence or LLM output.

## Relationship to the Existing Proof Kernel

The files present at the start of this traversal (zaw.py, docs/KSL.md + CLAIM_BOUNDARY.md + EVIDENCE_PROMOTION_PROTOCOL.md + SAFE_PROMPT_FORMAT.md + TRAVERSAL_RECEIPT.md, the three schemas, four samples, tests/test_zaw.py, the prior run artifact, LICENSE, README, build script) constitute the **minimal viable proof kernel**.

That proof kernel successfully demonstrates the doctrine:
- It snapshots and hashes untrusted input.
- It extracts text (with HTML script/style stripping).
- It labels instruction-like segments as no-authority.
- It emits evidence-only packets.
- It generates the required safe prompt language.
- It produces a full receipt with claim boundary and blind spots.
- The demo on `samples/injected_page.html` yields PASS_WITH_NOTES and the expected artifacts.

The cathedral does **not** replace or invalidate this proof. It is the structured, membrane-complete, schema-driven, testable, governanced evolution of the same kernel.

Key preservation rules applied throughout this build:
- The Absolute Kernel text remains the first and last word.
- The exact safe prompt boundary language and "evidence only / may not become authority" phrasing is retained.
- The original `python3 zaw.py samples/injected_page.html --task "..."` command continues to work.
- Existing test expectations for artifact names and basic authority/evidence labels continue to be satisfied (via compatibility shims in `__init__.py` or the root wrapper until tests are expanded in Phase 10).
- PRISM attribution and "Author: Corey Jacobs / Protocol: PRISM" headers are present on all new and updated doctrinal documents.
- No broadening of claims beyond what the implemented code and tests actually support.
- All deviations from the traversal map (if any) are documented in the final FULL_CATHEDRAL_TRAVERSAL_RECEIPT.md.

The proof kernel is the seed and the compatibility anchor. The cathedral is the full building raised on that foundation according to the Phase/Step plan.

## Exit for This Document

This document (docs/CATHEDRAL_GOAL.md) exists and defines the target, scope, relationship to the proof, and exclusions for the v0.1 cathedral build.

**We are building the cathedral. The kernel is held. The Operator holds authority.**

---

**End of CATHEDRAL_GOAL.md**