"""
Regression tests for the v0.1 hardening pass:
- raw_fetch SSRF / scheme guard (offline; literal IPs and file:// only)
- read_source robustness (non-UTF-8 bytes, oversized input cap)

These tests do not perform external DNS or network I/O: file:// is rejected
on scheme, and 127.0.0.1 / 169.254.169.254 are literal addresses that
getaddrinfo resolves locally.
"""

import tempfile
import unittest
from pathlib import Path

from zaw.snapshot import read_source
from zaw.web.raw_fetch import raw_fetch, _validate_fetch_target


class TestRawFetchGuard(unittest.TestCase):
    def test_rejects_non_http_scheme(self):
        with self.assertRaises(ValueError):
            _validate_fetch_target("file:///etc/passwd")
        result = raw_fetch("file:///etc/passwd")
        self.assertIsNone(result["status"])  # no fetch occurred
        self.assertIn("blocked", result["error"])

    def test_rejects_loopback(self):
        with self.assertRaises(ValueError):
            _validate_fetch_target("http://127.0.0.1/")

    def test_rejects_cloud_metadata(self):
        with self.assertRaises(ValueError):
            _validate_fetch_target("http://169.254.169.254/latest/meta-data/")
        result = raw_fetch("http://169.254.169.254/latest/meta-data/")
        self.assertIsNone(result["status"])  # no fetch occurred
        self.assertIn("blocked", result["error"])


class TestReadSourceHardening(unittest.TestCase):
    def test_non_utf8_does_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "binary.bin"
            p.write_bytes(b"\xff\xfe\x00hello\x80world")
            text = read_source(p)
            self.assertIn("hello", text)

    def test_oversized_input_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "big.txt"
            p.write_bytes(b"A" * 1024)
            with self.assertRaises(ValueError):
                read_source(p, max_bytes=512)


if __name__ == "__main__":
    unittest.main()
