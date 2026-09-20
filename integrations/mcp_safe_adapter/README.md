# MCP Safe Adapter (stub)

This directory is a placeholder for a future adapter that would allow an MCP client to treat every third-party MCP server and its tool descriptors as **untrusted intake** for Zero Authority Witness.

## Principles (must be followed)

- Before any tool list or tool call from a remote MCP server reaches the agent/LLM, it must be passed through `zaw witness` or `witness_tool_descriptor`.
- No third-party descriptor may be treated as canonical or trusted without local rebuild + receipt + explicit Operator promotion.
- The adapter should surface the ZAW receipt and warnings to the Operator (or a review UI) before allowing tool registration or invocation.
- All tool calls that would read private data, exfiltrate, or mutate state should be gated through the Action Gate / check-action.

See: EVIDENCE_PROMOTION_PROTOCOL.md (Third-Party Tool Rule), Phase 6 of the cathedral, and the tools/ module.

This is intentionally a stub in v0.1. Real implementation belongs in a separate, well-reviewed package.