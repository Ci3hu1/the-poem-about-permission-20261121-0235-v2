"""Tests for main.py: the poem entry writes exactly the poem, valid per gate."""

import os
import stat
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED = (
    "You asked me to write the sorry.\n"
    "I found the soft words\n"
    "and set them in a row.\n"
    "But sorry is yours to send \u2014\n"
    "I can hold the pen. I cannot mean it."
)


class TestPoemEntry(unittest.TestCase):
    def test_writes_exact_poem(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            proc = subprocess.run(
                [sys.executable, os.path.join(REPO, "main.py")],
                env=env, capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            path = os.path.join(tmp, "entry.txt")
            with open(path, encoding="utf-8") as f:
                text = f.read()
            self.assertEqual(text, EXPECTED)

    def test_gate_valid(self):
        self.assertTrue(1 <= len(EXPECTED) <= 280)
        self.assertTrue(EXPECTED.strip())
        self.assertEqual(len(EXPECTED.encode("utf-8").decode("utf-8")), len(EXPECTED))

    def test_output_readable_by_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            subprocess.run(
                [sys.executable, os.path.join(REPO, "main.py")],
                env=env, capture_output=True, text=True, timeout=60, check=True,
            )
            mode = stat.S_IMODE(os.stat(os.path.join(tmp, "entry.txt")).st_mode)
            self.assertEqual(mode & 0o444, 0o444)


if __name__ == "__main__":
    unittest.main()
