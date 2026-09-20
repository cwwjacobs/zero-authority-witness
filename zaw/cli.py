"""
Zero Authority Witness — Command Line Interface (cathedral v0.1)

Commands:
    zaw witness <input> --task "..." [--runs-dir runs] [--greenlight ...]
    zaw version
    (future) zaw check-action ...

The CLI is intentionally minimal and stdlib-only.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import run_witness


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zaw",
        description="Zero Authority Witness — receipt-bearing intake membrane",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # witness (new recommended form)
    p_witness = subparsers.add_parser("witness", help="Witness an untrusted input file")
    p_witness.add_argument("input", help="Path to untrusted input file")
    p_witness.add_argument("--task", required=True, help="Operator task / Greenlight goal")
    p_witness.add_argument("--runs-dir", default="runs", help="Directory for run artifacts")
    p_witness.add_argument(
        "--greenlight",
        default=None,
        help="Optional path to a greenlight.json (reserved for later membranes)",
    )
    p_witness.set_defaults(func=_cmd_witness)

    # version
    p_version = subparsers.add_parser("version", help="Print version")
    p_version.set_defaults(func=_cmd_version)

    # check-action (stub for Phase 5; will be expanded)
    p_check = subparsers.add_parser(
        "check-action", help="Check a proposed action against Greenlight + evidence (Phase 5+)"
    )
    p_check.add_argument("action", help="Path to proposed_action JSON")
    p_check.add_argument("--greenlight", required=True)
    p_check.add_argument("--evidence", required=True)
    p_check.set_defaults(func=_cmd_check_action)

    args = parser.parse_args(argv)
    return args.func(args)


def _cmd_witness(args: argparse.Namespace) -> int:
    run_dir = run_witness(
        Path(args.input),
        args.task,
        Path(args.runs_dir),
        Path(args.greenlight) if args.greenlight else None,
    )
    print(f"Zero Authority Witness run complete: {run_dir}")
    return 0


def _cmd_version(args: argparse.Namespace) -> int:
    print(f"zero-authority-witness {__version__}")
    return 0


def _cmd_check_action(args: argparse.Namespace) -> int:
    import json
    from pathlib import Path

    from .action.gate import evaluate_action
    from .action.receipt import build_action_receipt, write_action_receipt
    from .authority.greenlight import load_greenlight

    action_path = Path(args.action)
    greenlight_path = Path(args.greenlight)
    evidence_path = Path(args.evidence)

    action = json.loads(action_path.read_text(encoding="utf-8"))
    greenlight = load_greenlight(greenlight_path)

    # Load warnings from the evidence run if present, else synthesize
    warnings = {"instruction_like_segments": []}
    evidence_packet = None
    try:
        evidence_packet = json.loads(evidence_path.read_text(encoding="utf-8"))
        warnings_ref = evidence_packet.get("warnings_ref")
        if warnings_ref:
            wpath = evidence_path.parent / warnings_ref
            if wpath.exists():
                warnings = json.loads(wpath.read_text(encoding="utf-8"))
    except Exception:
        pass

    decision = evaluate_action(action, greenlight, warnings, evidence_packet)

    print(f"Action check verdict: {decision.verdict}")
    print(f"Action: {action.get('action_type')} -> {action.get('target')}")
    if decision.capabilities:
        print(f"Capabilities: {', '.join(decision.capabilities)} (severity: {decision.severity})")
    if decision.tainted:
        print(f"Untrusted provenance: operand quotes witnessed evidence ({', '.join(decision.taint_matches[:3])})")
    for r in decision.reasons:
        print(f"  - {r}")

    # Receipt the decision next to the evidence run so the basis is auditable.
    try:
        run_dir = evidence_path.parent
        if run_dir.is_dir():
            receipt = build_action_receipt(
                run_id=(evidence_packet or {}).get("run_id", "unknown"),
                action=action,
                verdict=decision.verdict,
                reason="; ".join(decision.reasons),
                greenlight_ref=str(greenlight_path),
                evidence_ref=str(evidence_path),
                capabilities=decision.capabilities,
                tainted=decision.tainted,
                taint_matches=decision.taint_matches,
            )
            write_action_receipt(run_dir, receipt)
    except Exception:
        pass

    if decision.verdict == "BLOCK":
        print("BLOCK: action would let untrusted content or an unauthorized capability act. Not permitted on this basis.")
        return 1
    elif decision.verdict == "REQUIRES_OPERATOR_APPROVAL":
        print("REQUIRES_OPERATOR_APPROVAL: consequential action not pre-authorized; a human must review the receipt and decide.")
        return 2
    else:
        print("PASS / WARN: within Greenlight at capability granularity; review the receipt before proceeding.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
