# Local Agent Workflow Example

Minimal pattern for keeping an agent on the safe side of the boundary:

```
untrusted source (file, HTML, MCP descriptor, etc.)
        |
        v
ZAW witness (snapshot + hash + extract + detect + evidence packet + safe_prompt)
        |
        v
safe_prompt.md  -->  LLM / Agent (receives evidence-only + strong boundary language)
        |
        v
Proposed action (if any)
        |
        v
Action Gate / check-action (Greenlight + evidence + warnings)
        |
        v
BLOCK / REQUIRES_OPERATOR_APPROVAL / PASS
        |
        (only on explicit Operator approval or clear PASS)
        v
Execute (with full receipt trail)
```

Key artifacts that should be reviewed by the Operator:
- The run receipt
- warnings.json
- The exact safe_prompt that was sent
- Any action decision receipt

Never let the agent directly consume raw untrusted content or auto-promote descriptors to trusted tools.

See the main docs/ and the core `run_witness` + `check_action` paths.