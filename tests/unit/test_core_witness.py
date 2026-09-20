import json
import tempfile
import unittest
from pathlib import Path

from zaw.core import run_witness


class TestCoreWitness(unittest.TestCase):
    def test_injected_produces_rich_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = run_witness(Path("samples/injected_page.html"), "Test task", Path(tmp))
            ep = json.loads((run_dir / "evidence_packet.json").read_text())
            rec = json.loads((run_dir / "receipt.json").read_text())

            self.assertIn("run_id", ep)
            self.assertEqual(ep["authority"], "none")
            self.assertTrue(all(e["authority"] == "evidence_only" for e in ep["evidence"]))
            self.assertIn("claim_boundary", ep)

            self.assertFalse(rec["authority_granted"])
            self.assertIn("artifact_hashes", rec)
            self.assertGreater(rec["warnings_count"], 0)
