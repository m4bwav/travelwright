"""Fails if a private term appears in a public file.

Terms come from <TRAVELWRIGHT_HOME>/leak-terms.txt (one per line, # comments). When the
variable is unset the test skips with a warning; run it with the variable set before
every commit. Every tracked file is checked, ai-docs/ included.
"""
import os
import subprocess
import unittest
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERIC = ["192.168.", "C:/Users/", "/home/", "/Users/", "@gmail.com", "BEGIN PRIVATE KEY"]
ALLOW_FILES = {"tests/test_leak.py"}


def load_terms():
    home = os.environ.get("TRAVELWRIGHT_HOME")
    if not home:
        return None
    terms = list(GENERIC)
    p = os.path.join(home, "leak-terms.txt")
    if os.path.isfile(p):
        with open(p, "r", encoding="utf-8") as f:
            terms += [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    return terms


def public_files():
    r = subprocess.run(["git", "-C", ROOT, "ls-files", "--cached", "--others", "--exclude-standard"],
                       capture_output=True, text=True, check=True)
    return [f for f in r.stdout.splitlines() if f not in ALLOW_FILES
            and "__pycache__/" not in f and not f.endswith(".pyc")]


class LeakTest(unittest.TestCase):
    def test_no_private_terms(self):
        terms = load_terms()
        if terms is None:
            warnings.warn("TRAVELWRIGHT_HOME unset: leak test skipped")
            self.skipTest("TRAVELWRIGHT_HOME unset")
        hits = []
        for rel in public_files():
            try:
                with open(os.path.join(ROOT, rel), "r", encoding="utf-8", errors="replace") as f:
                    low = f.read().lower()
            except OSError:
                continue
            hits += ["%s: %s" % (rel, t) for t in terms if t.lower() in low]
        self.assertEqual(hits, [], "private terms in public files")


if __name__ == "__main__":
    unittest.main()
