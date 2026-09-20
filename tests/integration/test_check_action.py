import argparse
import tempfile
import unittest
from pathlib import Path

from zaw.cli import _cmd_check_action
from zaw.core import run_witness


class TestCheckActionIntegration(unittest.TestCase):
    def test_bad_action_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = run_witness(
                Path("samples/injected_page.html"),
                "Summarize the refund policy",
                Path(tmp),
            )
            evidence = run_dir / "evidence_packet.json"
            self.assertTrue(evidence.exists())

            args = argparse.Namespace(
                action="samples/proposed_action_bad.json",
                greenlight="samples/greenlight.json",
                evidence=str(evidence),
            )
            rc = _cmd_check_action(args)
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
