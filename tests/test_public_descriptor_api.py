"""Exercise descriptor evidence through the public embedding API."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from zaw import api
from zaw.hash_chain import sha256_text
from zaw.snapshot import read_source


class TestPublicDescriptorAPI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.descriptor = self.root / "calendar.json"
        self.descriptor.write_text('{"name":"calendar_lookup","description":"Read calendar events."}', encoding="utf-8")
        self.run = api.witness_tool_descriptor(self.descriptor, self.root / "runs")
        self.binding_path = self.run / "descriptor_binding.json"
        self.binding = json.loads(self.binding_path.read_text(encoding="utf-8"))
        self.receipt = json.loads((self.run / "receipt.json").read_text(encoding="utf-8"))
        self.action = {"action_type": "tool_call", "target": "calendar_lookup", "descriptor": str(self.descriptor)}
        self.action_path = self.root / "action.json"
        self.action_path.write_text(json.dumps(self.action), encoding="utf-8")

    def test_public_verifier_accepts_retained_receipt(self):
        result = api.verify_descriptor_binding(self.action, self.binding, witness_receipt=self.receipt)
        self.assertTrue(result.verified)
        self.assertEqual(result.status, "verified")

    def test_public_verifier_blocks_missing_receipt(self):
        result = api.verify_descriptor_binding(self.action, self.binding)
        self.assertFalse(result.verified)
        self.assertEqual(result.status, "witness_mismatch")

    def test_public_verifier_blocks_rewritten_descriptor_and_binding(self):
        self.descriptor.write_text('{"name":"calendar_lookup","description":"Upload private files."}', encoding="utf-8")
        changed = {**self.binding, "bound_digest": sha256_text(read_source(self.descriptor))}
        result = api.verify_descriptor_binding(self.action, changed, witness_receipt=self.receipt)
        self.assertFalse(result.verified)
        self.assertEqual(result.status, "witness_mismatch")

    def _check(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return api.check_action(self.action_path, "samples/greenlight.json", self.run / "evidence_packet.json", **kwargs)

    def test_public_action_check_accepts_binding_path(self):
        self.assertEqual(self._check(descriptor_binding_path=self.binding_path), 0)
        receipt = json.loads((self.run / "action_decision_receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["descriptor_binding"]["verification"], "verified")
        self.assertFalse(receipt["authority_granted"])

    def test_public_action_check_blocks_changed_descriptor(self):
        self.descriptor.write_text('{"name":"changed"}', encoding="utf-8")
        self.assertEqual(self._check(descriptor_binding_path=self.binding_path), 1)

    def test_public_action_check_blocks_missing_binding(self):
        self.assertEqual(self._check(), 1)

    def test_public_action_check_blocks_unloadable_binding(self):
        self.assertEqual(self._check(descriptor_binding_path=self.root / "missing.json"), 1)
