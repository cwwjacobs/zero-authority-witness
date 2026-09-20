# FAQ — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Why not just use prompt filters or "put the untrusted content in a user message"?

Prompt filters are fragile and easy to bypass with novel phrasing or encoding. Putting content in a user message still gives the model the opportunity to treat it as instruction unless you also change the surrounding system/developer contract — which is exactly what many injection attacks try to do.

ZAW does something more fundamental: it never lets the untrusted content reach the model as raw authority-bearing text in the first place. The only thing the model normally sees is a carefully constructed `safe_prompt.md` that repeats the kernel.

## Why not let the LLM browse the web or call tools directly on untrusted content?

Because then the first contact with hostile material happens inside the model (or the tool-using agent). At that point the boundary is already lost. The model can be instructed to exfiltrate, to mutate its own instructions, or to launder the content into policy.

ZAW keeps the model from ever having first contact. The human Operator (via the Witness artifacts) has first contact.

## Why hashes if they don't prove safety?

Hashes prove that the artifact you are looking at right now is the same one that was captured at intake time. This is essential for provenance, for TOCTOU detection on live sources, and for later audits.

They are deliberately not sold as a safety guarantee. The claim boundary and the blind spots travel with the hashes precisely to prevent hash worship.

## Why "evidence-only"? Isn't that just another label the model can ignore?

The label is part of a larger contract:
- The safe prompt repeats the boundary language in human-readable form.
- The receipt and the evidence packet carry the claim boundary and the warnings.
- The Authority Membrane and Action Gate (when used) can still BLOCK or require explicit approval even if the model later says "this looks fine".

The label is a signal to both the model and to the surrounding control plane. It is not magic, but it is a strong, consistent, receipted signal.

## What does ZAW actually solve?

It reduces first-contact authority risk for the specific surfaces it witnesses (files, HTML, JSON descriptors, etc.).

It makes the following things expensive or visible:
- Hidden instructions in staged content
- Obvious tool descriptor poisoning
- Attempts to launder untrusted data into policy or allowlists
- Silent expansion of scope without Operator receipts

It does not solve the general prompt injection problem for arbitrary untrusted input that reaches the model through other channels.

## How does MCP / tool poisoning fit?

Third-party MCP servers and tool descriptors are explicitly called out in the EVIDENCE_PROMOTION_PROTOCOL as untrusted intake.

ZAW can snapshot them, hash them, run the detector across all their text fields (description, schema, etc.), classify obvious risks (filesystem, exfil, policy mutation), and refuse to treat them as canonical.

A clean receipt for a descriptor is not an authorization to use it with elevated privileges. It is evidence that you saw what was there at one point in time.

## Why is the implementation so small and stdlib-only?

Because the goal is a cheap, repeatable, inspectable, auditable membrane that can be understood and reviewed by a human Operator without pulling in a large trusted computing base.

Every additional dependency is another potential attack surface and another thing that must be receipted and understood.

## Can I depend on this as a deployed security product?

Not yet. This is a public-safe v0.1 reference implementation of a defensive primitive.

It is suitable for operators and developers who are willing to read receipts, inspect warnings, and maintain Greenlights. It is not a set-and-forget security product.

See CLAIM_BOUNDARY.md, THREAT_MODEL.md, and SECURITY_MODEL.md.

---

The honest answer to almost every "does it completely solve X?" question is: it reduces risk on the witnessed path and makes the boundary visible. The Operator remains responsible.