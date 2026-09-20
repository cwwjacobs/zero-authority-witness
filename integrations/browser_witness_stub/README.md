# Browser / View Witness Stub

The browser or any rendering/viewing component has **no authority** over allowlists, Greenlight, policy, or the Kernel.

## Rules

- Any content fetched or rendered by a browser/view must still be staged and passed through the Zero Authority Witness before the extracted text or "what the user saw" summary is treated as evidence.
- The view cannot grant trust. It can only contribute raw (or rendered) material that is then witnessed.
- Reports or summaries generated for the Operator must go through the Witness View render guard (no active links/images that can exfiltrate).

See: docs/WITNESS_VIEW.md and the web/ + view/ modules.

This stub exists to make the boundary explicit for future browser integration work.