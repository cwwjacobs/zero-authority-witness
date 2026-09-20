# Developer Guide — Zero Authority Witness

**Author:** Corey Jacobs  
**Protocol:** PRISM

---

## Public API (stable for v0.1)

See `zaw/api.py` (to be expanded) and the modules under `zaw/`:

- `zaw.core.run_witness(input_path, task, runs_dir="runs")` — the main engine.
- `zaw.cli` — the command line (witness, version, check-action stub).
- Individual modules (`snapshot`, `detect`, `evidence`, `safe_prompt`, etc.) can be used directly for custom intake pipelines.

## Extending the Witness

- New extractors go in `extract.py` (keep the contract that extraction grants no authority).
- New detectors go in `detect.py` (they must only ever produce `authority: "none"` warnings).
- New membranes belong under `authority/` or `action/`.
- New tool/MCP handling belongs under `tools/`.

Every new path must emit (or update) the standard artifacts and carry the claim boundary + blind spots.

## Running Tests

```
python3 -m unittest discover
```

Golden tests (when added) should normalize timestamps and run_ids.

## Adding a New Fixture

Place hostile or boundary-case samples under `tests/fixtures/<category>/`.

Update or add red-team tests that assert the expected warnings or BLOCK verdicts.

## Packaging

`pyproject.toml` declares a zero-dependency package with console script `zaw`.

Use `pip install -e .` for development.

## Philosophy for Contributors

If your change makes it easier for evidence to become authority, or makes the Operator less likely to see the raw warnings and receipts, it is probably the wrong change.

The cathedral exists to make the boundary visible and the cost of ignoring it high.

See also CATHEDRAL_GOAL.md and CONTRIBUTING.md.