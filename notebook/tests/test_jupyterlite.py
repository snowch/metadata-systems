# Copyright © 2026 Christopher Snow

"""The Jupyter pages' controls and warnings: the buttons the texts tell the reader to press exist on
the page, and each chapter's warning states what was measured on the pages.

notebook/buttons/ is a JupyterLab extension that adds a row of large buttons above every notebook's
cells, because on a phone the menus at the top of the page open when tapped but their items do
nothing, and the toolbar's buttons are 21 pixels tall (docs/notes/notebook-prototype.md). This
checks, with the standard library only, that the texts and the buttons agree, and that the build
adds the row to the site; notebook/jupyterlite/smoke.mjs presses the buttons in a browser.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = {
    chapter: (ROOT / "notebook" / f"chapter_0{chapter}.py").read_text(encoding="utf-8") for chapter in (1, 2)
}
BUTTONS = ROOT / "notebook" / "buttons"
LABELS = json.loads((BUTTONS / "buttons.json").read_text(encoding="utf-8"))


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", s)


class TheButtons(unittest.TestCase):
    def test_the_row_runs_every_cell_runs_from_the_selected_cell_and_saves(self):
        self.assertEqual(LABELS, {"runAll": "Run all", "runBelow": "Run below", "save": "Save"})

    def test_every_button_has_an_action(self):
        index = (BUTTONS / "index.js").read_text(encoding="utf-8")
        [actions] = re.findall(r"^const actions = \{\n(.*?)^\};", index, re.M | re.S)
        self.assertEqual(set(re.findall(r"^  (\w+)\(", actions, re.M)), set(LABELS))

    def test_the_texts_press_every_button_and_only_those(self):
        named = {label for source in SOURCE.values() for label in re.findall(r"press \*\*([^*]+)\*\*", source)}
        self.assertEqual(named, set(LABELS.values()))

    def test_the_texts_send_nobody_to_the_menus_or_the_toolbar(self):
        # On a phone the menus' items do nothing and the toolbar's buttons are small; the texts use
        # the row.
        for part, source in SOURCE.items():
            for words in ("menu bar", "toolbar", "triangle", "Run All Cells", "Save Notebook"):
                self.assertNotIn(words, source, part)
            self.assertIn("press **Run all**, at the top of the page", source, part)

    def test_the_menu_of_changes_is_the_only_menu_the_texts_name(self):
        self.assertIn("Choose a change to the shop from the menu below.", SOURCE[2])
        self.assertNotIn("menu", SOURCE[1].replace("dropdown", ""))

    def test_the_build_adds_the_row_to_the_site(self):
        build = (ROOT / "notebook" / "jupyterlite" / "build.sh").read_text(encoding="utf-8")
        package = json.loads((BUTTONS / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(package["jupyterlab"]["outputDir"], "labextension")
        self.assertIn('--LiteBuildConfig.federated_extensions="$buttons/labextension"', build)


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
                ("the page downloaded less than 1 MB when opened from Chapter 1's link", stored),
                ("Chapter 1's link opens this page in a new tab", "part 2 from part 1's link (a new tab)"),
                ("running every cell took 10 to 12 seconds", run),
                ("running every cell took 10 to 12 seconds", live_run),
                ("the page used about 420 MB of memory", memory),
            ],
        }
        for part, pairs in expected.items():
            [warning] = re.findall(r'mo\.callout\(mo\.md\(r"""(.*?)"""\), kind="warn"\)', SOURCE[part], re.S)
            warning = flat(warning)
            # One line stays visible; the measurements fold into a section the reader opens.
            self.assertIn("<details><summary>", warning, part)
            self.assertLess(warning.index("downloads about 13 MB"), warning.index("<details>"), part)
            for said, measured in pairs:
                # A phrase may open its sentence, so its first letter's case is not compared.
                self.assertIn(said.lower(), warning.lower(), part)
                self.assertIn(flat(measured), note, part)
            self.assertIn("a reload loses anything you have not saved", warning)



class TheBoxes(unittest.TestCase):
    """The warning and the steps for running the page are boxes, set apart from the chapter's text."""

    def test_every_kind_of_box_the_build_writes_has_a_style(self):
        build = (ROOT / "notebook" / "jupyterlite" / "build_ipynb.py").read_text(encoding="utf-8")
        css = (BUTTONS / "style" / "index.css").read_text(encoding="utf-8")
        [boxes] = re.findall(r"^BOXES = (\{.*\})$", build, re.M)
        for name in ("ms-box", *eval(boxes).values()):
            self.assertIn(f".jp-RenderedMarkdown .{name} {{", css)

    def test_each_chapter_opens_with_a_warning_and_the_steps(self):
        for chapter, source in SOURCE.items():
            self.assertEqual(re.findall(r'\bkind="(\w+)"\)', source), ["warn", "info"], chapter)
            [steps] = re.findall(r'mo\.callout\(mo\.md\(r"""(.*?)"""\), kind="info"\)', source, re.S)
            self.assertIn("press **Run all**, at the top of the page", steps, chapter)

    def test_chapter_1s_steps_name_every_button(self):
        [steps] = re.findall(r'mo\.callout\(mo\.md\(r"""(.*?)"""\), kind="info"\)', SOURCE[1], re.S)
        self.assertEqual(set(re.findall(r"press \*\*([^*]+)\*\*", steps)), set(LABELS.values()))

    def test_printed_text_keeps_its_lines(self):
        css = (BUTTONS / "style" / "index.css").read_text(encoding="utf-8")
        rule = css.split('.jp-OutputArea-output[data-mime-type="application/vnd.jupyter.stdout"] pre {')[1]
        self.assertIn("white-space: pre;", rule.split("}")[0])


class TheTheme(unittest.TestCase):
    def test_the_notebooks_follow_the_readers_light_or_dark_setting(self):
        overrides = json.loads((ROOT / "notebook" / "jupyterlite" / "overrides.json").read_text(encoding="utf-8"))
        self.assertIs(overrides["@jupyterlab/apputils-extension:themes"]["adaptive-theme"], True)


class TheFigures(unittest.TestCase):
    """The figures go into Markdown cells, which drop <style> and inline <svg>."""

    @classmethod
    def setUpClass(cls):
        import base64
        import sys

        sys.path.insert(0, str(ROOT / "notebook"))
        import shop
        from shop import figures

        cls.week = shop.run_week()
        cls.figures = figures
        cls.decode = staticmethod(lambda b64: base64.b64decode(b64).decode("utf-8"))

    def test_the_html_figures_carry_no_style_and_no_svg(self):
        for drawn in (self.figures.pipeline(self.week), self.figures.dashboard_chart(self.week)):
            html = self.figures.figure(drawn, "a caption")
            self.assertNotIn("<style", html)
            self.assertNotIn("<svg", html)

    def test_the_week_is_an_svg_image_with_its_own_dark_colours_and_a_description(self):
        img = self.figures.week_strip(self.week)
        [alt, b64] = re.findall(r'^<img class="ms-svg" alt="([^"]+)" src="data:image/svg\+xml;base64,([^"]+)">$', img)[0]
        svg = self.decode(b64)
        self.assertIn("prefers-color-scheme:dark", svg)
        self.assertNotIn("currentColor", svg)
        self.assertIn("you start work at 09:00 on Mon 14", alt)
        # 14-unit text in a 340-unit drawing: at least 11 pixels in a column 268 pixels wide.
        self.assertIn('viewBox="0 0 340 ', svg)
        self.assertIn("font-size:14px", svg)

    def test_every_figure_the_chapters_show_is_drawn_into_markdown(self):
        build = (ROOT / "notebook" / "jupyterlite" / "build_ipynb.py").read_text(encoding="utf-8")
        self.assertIn("nbformat.v4.new_markdown_cell(drawn)", build)
        for source in SOURCE.values():
            self.assertNotIn("figures.raw_text", source)

if __name__ == "__main__":
    unittest.main()
