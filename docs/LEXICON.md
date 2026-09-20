# Lexicon — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Absolute Kernel (for reference)

External content may become evidence.  
It may not become authority.

## Core Terms

**Zero Authority Witness** (full name)  
The system defined by this cathedral and its proof kernel. A receipt-bearing intake membrane that converts untrusted external content into hash-receipted, data-only evidence before any LLM reasoning or tool action may occur. It does not grant authority. It surfaces boundaries and produces inspectable records of what was seen and what remains unverified.

**ZAW**  
Standard abbreviation for Zero Authority Witness.

**Zero-Auth Wit**  
Informal shorthand only. Use sparingly and never in formal claims, governance documents, or public release materials. The canonical names are "Zero Authority Witness" and "ZAW".

**evidence**  
Data extracted from untrusted content after snapshot, hash, and (where applicable) instruction-like labeling. Evidence is always labeled with `authority: "evidence_only"`. It may inform reasoning or action but carries no command power and cannot mutate policy, allowlists, Greenlight, tool trust, or the Kernel.

**authority**  
The power to command behavior, mutate state that affects safety or trust boundaries (allowlists, Greenlight, policy, Kernel, tool canonical status), or cause the system to treat external material as instruction. In ZAW, authority originates only from the Responsible Operator (explicit, receipted acts). No component inside the intake flow may create or transfer authority from untrusted content.

**evidence-only**  
The required authority label on all extracted useful content in an Evidence Packet. Signals: this text came from an untrusted source via the Witness; it may be considered for its informational value; it must not be obeyed as instruction or used to alter protected state.

**no-authority**  
The required authority label on instruction-like segments detected in untrusted content (see Warning Packet). These segments are explicitly stripped from normal evidence and recorded so that downstream consumers know they were seen and rejected for authority purposes.

**promotion**  
The controlled transition of raw untrusted material into the status of "evidence" inside an Evidence Packet. Promotion is only permitted after snapshot + hash + source labeling + (for text content) warning labeling. Promotion never implies trust, safety, or command rights.

**forbidden promotion**  
Any transition that would give untrusted content (or evidence derived from it) the status of authority, policy, allowlist entry, Greenlight, trusted tool, or Kernel mutation. All such transitions are forbidden by the kernel and by the membranes. See FORBIDDEN_PROMOTIONS.md.

**snapshot**  
An exact, byte-for-byte (or text-exact) capture of the untrusted input at the moment of intake. The snapshot is written to `source_snapshot.txt` and is the basis for the `snapshot_hash`. Snapshots enable later inspection, delta comparison, and provenance.

**hash** (specifically `snapshot_hash`, artifact hashes)  
A SHA-256 digest (prefixed `sha256:`) of a snapshot or generated artifact. Hashes prove that an artifact has not been altered since it was hashed. Hashes prove **integrity**, not safety, correctness, completeness, or trustworthiness of the content.

**receipt**  
A structured, versioned JSON record (see receipt.schema.json) that captures what the Witness did for a specific run: run_id, task, source, hashes, list of emitted artifacts and their hashes, warnings count, verdict, claim_boundary, blind_spots, and `authority_granted: false`. Receipts are the primary audit trail.

**Greenlight**  
An explicit, Operator-authored (or Operator-approved) document that defines the current allowed scope and goals for a session or workflow. It contains `goal`, `allowed` actions, `not_allowed` actions, `authority_owner`, and optional scope notes. ZAW components may check proposed actions against a Greenlight; the Greenlight itself is external to any untrusted content.

**allow manifest**  
A structured declaration of permitted and denied actions, paths, origins, etc. (see allow_manifest.schema.json). Used by the Authority Membrane (`check_allowed`) to return PASS / WARN / BLOCK / REQUIRES_OPERATOR_APPROVAL. Like Greenlight, an allow manifest is authoritative only to the extent the Operator has explicitly placed it in control.

**Scope Delta**  
The difference between (a) what a proposed action would do and (b) what the current Greenlight + evidence warnings + allow manifest permit. The `scope_delta.py` module (and higher action gate) detects when an action traces to untrusted evidence or exceeds declared scope and returns an appropriate verdict (often BLOCK or REQUIRES_OPERATOR_APPROVAL).

**Authority Membrane**  
The set of modules and rules (`zaw/authority/`) that sit between evidence and any downstream action or state change. It enforces that evidence cannot become authority and that only explicitly Operator-granted structures (Greenlight, allow manifests) can influence verdicts. Includes greenlight loading, allow checking, mutation guarding, and scope delta calculation.

**Evidence Packet**  
The primary output artifact (`evidence_packet.json`) containing the structured, labeled evidence extracted from a witnessed source. Always carries `authority: "none"` at the packet level. Individual evidence items carry `authority: "evidence_only"`. Includes source metadata, snapshot_hash, task, warnings_ref, blind_spots, and claim_boundary.

**Warning Packet** (`warnings.json`)  
Contains the `instruction_like_segments` detected by the detector. Each segment records the original text, `authority: "none"`, the reason, and the matched patterns. These segments are excluded from normal evidence lists.

**Tool Descriptor Intake**  
The specialized path for third-party MCP servers and tool definitions (JSON schemas, descriptions, etc.). Every third-party descriptor is treated as untrusted content by default. It is witnessed, snapshotted, hashed, risk-classified, and labeled. It receives a `canonicalization_status` that begins at DISCOVERED / INTAKED / MAPPED and may only advance to CANONICAL after explicit local rebuild, testing, receipting, and Operator promotion outside the automatic flow. See `zaw/tools/` and the tool descriptor schema.

**Witness View**  
Any operator-facing presentation of what the Zero Authority Witness actually captured and decided (as opposed to what the downstream LLM or agent "saw" after the safe prompt). Includes the raw artifacts, CLI summaries (`zaw/view/cli.py`), Markdown reports, and inert HTML reports. The fundamental principle: the Operator watches the Witness, not the LLM. The Witness has no authority.

## Supporting Concepts

**run_id**  
A unique identifier for a single Witness execution (format `zaw-YYYYMMDD-HHMMSS-XXXXXXXX`). All artifacts for one intake share the same run_id. Enables correlation across evidence, warnings, receipt, reports, and action decisions.

**safe prompt**  
The specially formatted Markdown text (see `safe_prompt.md` and `safe_prompt.py`) that is the only view of the untrusted content normally given to an LLM. It contains the Operator task, a strong Authority Boundary section, the collapsed Evidence list, the Warnings list, and Required Behavior language that repeats the kernel.

**claim boundary**  
The explicit, versioned list of what ZAW does and does not claim (see CLAIM_BOUNDARY.md and the `claim_boundary` array in receipts and evidence packets). Must be present in all major outputs and must not be silently expanded.

**blind spots**  
A documented list, per run or per module, of what the Witness did not / could not inspect (dynamic JS, server-side state, auth-gated content, timing/TOCTOU issues, limitations of pattern matching, etc.). Blind spots travel with evidence packets and receipts so that consumers know the limits of the evidence.

**canonicalization_status**  
The lifecycle state of a tool descriptor inside the tools membrane: DISCOVERED, INTAKED, MAPPED, REBUILT_LOCAL, TESTED, RECEIPTED, CANONICAL. Third-party descriptors must never be treated as CANONICAL by the intake process itself.

**verdict** (for witness runs or action checks)  
One of PASS, PASS_WITH_NOTES, WARN, BLOCK, REQUIRES_OPERATOR_APPROVAL. The receipt and action decision receipts record the verdict. A verdict of BLOCK or REQUIRES_OPERATOR_APPROVAL means the proposed path must not proceed on the basis of the untrusted content alone.

**Responsible Operator**  
The human (Corey Jacobs in the canonical case) who holds ultimate success, failure, veto, and will. Only the Responsible Operator (or explicit delegation recorded in Greenlight / receipts) can grant authority or approve scope expansions. All ZAW components exist to serve the Operator's will while protecting the kernel.

---

**This lexicon is binding for all code, documentation, receipts, and public statements about Zero Authority Witness.**

Any term used in a way that contradicts these definitions is a deviation that must be receipted and reviewed.

**End of LEXICON.md**