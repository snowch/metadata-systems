# Copyright © 2026 Christopher Snow

"""The JupyterLite version's own words: each replaces a paragraph the marimo notebook still has,
states what was measured on the JupyterLite page, and keeps the writing standard's rules.

notebook/jupyterlite/build_ipynb.py builds the Jupyter notebook from the marimo notebook and needs
nbformat; this checks, with the standard library only, what would make that build stop or the page
say something untrue.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARIMO = (ROOT / "notebook" / "chapter_01.py").read_text(encoding="utf-8")
sys.path.insert(0, str(ROOT / "notebook" / "jupyterlite"))
import words  # noqa: E402

SLOTS = {name: getattr(words, name) for name in ("WARNING", "HOW_TO", "THURSDAY_ROW", "CHANGES")}


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", s)


class TheJupyterLiteWords(unittest.TestCase):
    def test_each_replaces_a_paragraph_the_marimo_notebook_has_once(self):
        for key, text in words.MARIMO.items():
            self.assertEqual(MARIMO.count(text), 1, key)

    def test_the_warning_states_the_measurements(self):
        note = flat((ROOT / "docs" / "notes" / "notebook-prototype.md").read_text(encoding="utf-8"))
        for said, measured in [
            ("downloads about 13 MB", "| Size if the host compresses text and WebAssembly (gzip, level 6) | 17.5 MB | 12.5 MB |"),
            ("running every cell took about 10 seconds", "| Run All Cells, from the press to the last output | (cells run on load) | 9.4 to 9.9 s |"),
            ("the page used about 440 MB of memory", "| Peak memory of the page's renderer process | 0.97 to 1.16 GB | 0.42 to 0.45 GB |"),
        ]:
            self.assertIn(said, words.WARNING)
            self.assertIn(measured, note)
        self.assertIn("a reload loses anything you have not saved", words.WARNING)

    def test_the_menu_names_stay_apart(self):
        # "menu bar" is the page's menus; "menu" alone is the list of changes.
        self.assertIn("in the menu bar at the top", words.HOW_TO)
        self.assertIn("In the menu bar at the top, choose Run", words.CHANGES)
        self.assertIn("Choose a change from the menu below", words.CHANGES)

    def test_the_writing_rules(self):
        source = (ROOT / "scripts" / "prose.mjs").read_text(encoding="utf-8")
        phrases = re.findall(r'phrase: "([^"]+)"', source) + ["the lab ", "the lab's", "Metadata Lab"]
        self.assertGreater(len(phrases), 10)
        for name, text in SLOTS.items():
            self.assertNotIn("[[", text, name)
            self.assertNotIn("—", text, name)
            self.assertEqual([p for p in phrases if p.lower() in text.lower()], [], name)
            for word in ("JupyterLite", "marimo", "Pyodide", "WebAssembly"):
                self.assertNotIn(word, text, name)


if __name__ == "__main__":
    unittest.main()
