# Copyright © 2026 Christopher Snow

"""The Jupyter pages' controls and warnings: the toolbar buttons the texts tell the reader to press
exist on the page, and each part's warning states what was measured on the pages.

notebook/jupyterlite/overrides.json adds two labelled buttons to the notebook's toolbar, because on
a phone the menus at the top of the page open when tapped but their items do nothing, while the
toolbar's buttons respond (docs/notes/notebook-prototype.md). This checks, with the standard library
only, that the texts and the buttons agree.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = {
    part: (ROOT / "notebook" / f"chapter_01_part_{part}.py").read_text(encoding="utf-8") for part in (1, 2)
}
OVERRIDES = json.loads((ROOT / "notebook" / "jupyterlite" / "overrides.json").read_text(encoding="utf-8"))


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def toolbar() -> dict[str, str]:
    """The labelled buttons the page adds to the notebook's toolbar, by label: their commands."""
    items = OVERRIDES["@jupyterlab/notebook-extension:panel"]["toolbar"]
    return {item["label"]: item["command"] for item in items if "label" in item}


class TheToolbar(unittest.TestCase):
    def test_the_two_buttons_run_every_cell_and_the_cells_below(self):
        self.assertEqual(
            toolbar(),
            {"Run all": "notebook:run-all-cells", "Run below": "notebook:run-all-below"},
        )

    def test_the_texts_press_only_buttons_the_page_has(self):
        named = {label for source in SOURCE.values() for label in re.findall(r"press \*\*([^*]+)\*\*", source)}
        self.assertEqual(named, set(toolbar()))

    def test_the_texts_send_nobody_to_the_menus_at_the_top(self):
        # On a phone those menus' items do nothing; the texts use the toolbar instead.
        for part, source in SOURCE.items():
            for words in ("menu bar", "Run All Cells", "Save Notebook", "Run Selected Cell"):
                self.assertNotIn(words, source, part)
        self.assertIn("in the toolbar at the top of the page", SOURCE[1])
        self.assertIn("in the toolbar at the top of the page", SOURCE[2])

    def test_the_menu_of_changes_is_the_only_menu_the_texts_name(self):
        self.assertIn("Choose a change to the shop from the menu below.", SOURCE[2])
        self.assertNotIn("menu", SOURCE[1].replace("dropdown", ""))


class TheWarnings(unittest.TestCase):
    def test_each_warning_states_the_measurements(self):
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
            [warning] = re.findall(r'mo\.callout\(mo\.md\("([^"]+)"\)', SOURCE[part])
            for said, measured in pairs:
                self.assertIn(said, warning, part)
                self.assertIn(flat(measured), note, part)
            self.assertIn("a reload loses anything you have not saved", warning)


if __name__ == "__main__":
    unittest.main()
