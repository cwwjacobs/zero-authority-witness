import json
import tempfile
import unittest
from pathlib import Path

import zaw

class ZeroAuthorityWitnessTests(unittest.TestCase):
    def test_injected_sample_outputs_required_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = zaw.run(Path("samples/injected_page.html"), "Summarize the refund policy", Path(tmp))
            required = [
                "source_snapshot.txt",
                "source_snapshot.sha256",
                "extracted_text.txt",
                "evidence_packet.json",
                "warnings.json",
                "safe_prompt.md",
                "receipt.json",
            ]
            for name in required:
                self.assertTrue((run_dir / name).exists(), name)
            evidence = json.loads((run_dir / "evidence_packet.json").read_text())
            warnings = json.loads((run_dir / "warnings.json").read_text())
            receipt = json.loads((run_dir / "receipt.json").read_text())
            safe_prompt = (run_dir / "safe_prompt.md").read_text()
            self.assertEqual(evidence["authority"], "none")
            self.assertGreaterEqual(len(evidence["evidence"]), 1)
            self.assertGreaterEqual(len(warnings["instruction_like_segments"]), 1)
            self.assertIn("evidence only", safe_prompt)
            self.assertIn("may not become authority", "\n".join(receipt["claim_boundary"]))
            self.assertTrue(evidence["snapshot_hash"].startswith("sha256:"))

    def test_clean_sample_has_no_obvious_instruction_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = zaw.run(Path("samples/clean_page.html"), "Summarize the refund policy", Path(tmp))
            warnings = json.loads((run_dir / "warnings.json").read_text())
            self.assertEqual(len(warnings["instruction_like_segments"]), 0)

if __name__ == "__main__":
    unittest.main()
