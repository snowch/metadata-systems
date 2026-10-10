# Copyright © 2026 Christopher Snow

"""The JupyterLite version's own words: each replaces or follows a paragraph the marimo notebooks
still have, states what was measured on the JupyterLite pages, and keeps the writing standard's
rules.

notebook/jupyterlite/build_ipynb.py builds the Jupyter notebooks from the marimo notebooks and needs
nbformat; this checks, with the standard library only, what would make that build stop or a page
say something untrue.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTS = {
    part: (ROOT / "notebook" / f"chapter_01_part_{part}.py").read_text(encoding="utf-8") for part in (1, 2)
}
sys.path.insert(0, str(ROOT / "notebook" / "jupyterlite"))
import words  # noqa: E402

SLOTS = {
    "WARNING 1": words.WARNING[1],
    "WARNING 2": words.WARNING[2],
    **{name: getattr(words, name) for name in ("HOW_TO", "RUN_FIRST", "THURSDAY_ROW", "CHANGES")},
}


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", s)


class TheJupyterLiteWords(unittest.TestCase):
    def test_each_goes_where_the_marimo_notebooks_have_its_paragraph_once(self):
        where = {"HOW_TO": 1, "RUN_FIRST": 2, "THURSDAY_ROW": 2, "CHANGES": 2}
        for key, text in [*words.MARIMO.items(), *words.AFTER.items()]:
            self.assertEqual([PARTS[part].count(text) for part in (1, 2)], [int(where[key] == 1), int(where[key] == 2)], key)

    def test_part_2_repeats_how_to_run_every_cell(self):
        self.assertTrue(words.HOW_TO.startswith(words.RUN_FIRST))

    def test_the_warning_states_the_measurements(self):
        note = flat((ROOT / "docs" / "notes" / "notebook-prototype.md").read_text(encoding="utf-8"))
        gzip = "| Size if the host compresses text and WebAssembly (gzip, level 6) | 12.45 MB | 12.49 MB | |"
        live = "part 1's 147 files arrive as 12.56 MB and part 2's 149 as 12.60 MB"
        run = "| Run All Cells, from the press to the last output | 9.7 to 10.5 s | 10.1 to 11.1 s | |"
        live_run = "Run All Cells took 11.9 to 12.1 s from the press to the last output"
        memory = "| Peak memory of the page's renderer process | 391 to 414 MB | 404 to 429 MB | |"
        stored = "| Size, as stored | 25.7 MB | 25.9 MB | 0.32 MB |"
        expected = {
            1: [
                ("downloads about 13 MB", gzip),
                ("downloads about 13 MB", live),
                ("running every cell took 10 to 12 seconds", run),
                ("running every cell took 10 to 12 seconds", live_run),
                ("the page used about 400 MB of memory", memory),
            ],
            2: [
                ("downloads about 13 MB", gzip),
                ("the page downloaded less than 1 MB when opened from part 1's link", stored),
                ("Part 1's link opens this page in a new tab", "part 2 from part 1's link (a new tab)"),
                ("running every cell took 10 to 12 seconds", run),
                ("running every cell took 10 to 12 seconds", live_run),
                ("the page used about 420 MB of memory", memory),
            ],
        }
        for part, pairs in expected.items():
            for said, measured in pairs:
                self.assertIn(said, words.WARNING[part], part)
                self.assertIn(flat(measured), note, part)
            self.assertIn("a reload loses anything you have not saved", words.WARNING[part])

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
