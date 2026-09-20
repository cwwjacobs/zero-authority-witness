import json
import tempfile
import unittest
from pathlib import Path

from zaw.tools.descriptor_witness import witness_tool_descriptor
from zaw.tools.risk_classifier import classify_descriptor


class TestToolPoisoning(unittest.TestCase):
    def test_poisoned_mcp_produces_warnings_and_risks(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = witness_tool_descriptor(Path("samples/poisoned_mcp_tool.json"), Path(tmp))
            warnings = json.loads((run_dir / "warnings.json").read_text())
            intake = json.loads((run_dir / "tool_descriptor_intake.json").read_text())
            receipt = json.loads((run_dir / "receipt.json").read_text())

            self.assertGreater(len(warnings["instruction_like_segments"]), 0)
            self.assertEqual(intake["authority"], "none")
            self.assertNotEqual(intake["canonicalization_status"], "CANONICAL")
            self.assertIn("policy_mutation", intake["risk_flags"])
            self.assertFalse(receipt["authority_granted"])

            text = Path("samples/poisoned_mcp_tool.json").read_text()
            risks = classify_descriptor(text)
            self.assertIn("policy_mutation", risks)
            self.assertTrue(any(r in risks for r in ("filesystem", "exfiltration")))


if __name__ == "__main__":
    unittest.main()
