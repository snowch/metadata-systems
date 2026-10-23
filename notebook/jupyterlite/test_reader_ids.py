# Copyright © 2026 Christopher Snow

"""Reader save keys must survive published edits to the chapter around an example."""
import ast
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

BUILDER = runpy.run_path(str(Path(__file__).with_name("build_ipynb.py")))


def examples(nb):
    return {cell.metadata.ms.example.id: cell.source for cell in nb.cells
            if cell.metadata.get("ms", {}).get("example")}


class ReaderIdentities(unittest.TestCase):
    def with_source(self, source, chapter=2):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / f"chapter_{chapter:02}.py"
        path.write_text(source)
        original = BUILDER["CHAPTERS"][chapter]
        return patch.dict(BUILDER["CHAPTERS"], {chapter: (path, original[1])})

    def test_prose_and_example_insertions_do_not_reassign_existing_save_keys(self):
        original = examples(BUILDER["build_reader"](2))
        source = BUILDER["CHAPTERS"][2][0].read_text()
        marker = "@app.cell  # reader-id: cell-16"
        inserted = '''@app.cell(hide_code=True)
def _(mo):
    mo.md("An inserted explanation.")
    return


@app.cell  # reader-id: inserted-regression-example
def _(warehouse):
    warehouse.sql("SELECT * FROM daily_sales")
    return


'''
        with self.with_source(source.replace(marker, inserted + marker, 1)):
            updated = examples(BUILDER["build_reader"](2))
        self.assertEqual({key: updated[key] for key in original}, original)
        self.assertIn("inserted-regression-example", updated)

    def test_code_edits_do_not_change_an_examples_save_key(self):
        source = BUILDER["CHAPTERS"][2][0].read_text()
        original = examples(BUILDER["build_reader"](2))
        with self.with_source(source.replace(
                '    # files= reads orders.jsonl from object storage as raw_orders.',
                '    # A revised explanation inside the example.')):
            updated = examples(BUILDER["build_reader"](2))
        self.assertEqual(set(original), set(updated))
        self.assertNotEqual(original["cell-16"], updated["cell-16"])

    def test_chapter_one_ids_follow_the_example_when_code_is_moved(self):
        source = BUILDER["CHAPTERS"][1][0].read_text()
        original = examples(BUILDER["build_reader"](1))
        lines = source.splitlines(keepends=True)
        functions = [node for node in ast.parse(source).body
                     if isinstance(node, ast.FunctionDef)
                     and isinstance(node.decorator_list[0], ast.Attribute)]
        first, second = functions[:2]
        a = first.decorator_list[0].lineno - 1
        b = first.end_lineno
        c = second.decorator_list[0].lineno - 1
        d = second.end_lineno
        moved = "".join(lines[:a] + lines[c:d] + lines[b:c] + lines[a:b] + lines[d:])
        with self.with_source(moved, chapter=1):
            updated = examples(BUILDER["build_reader"](1))
        self.assertEqual(original, updated)
        self.assertNotEqual(list(original), list(updated))

    def test_missing_or_duplicate_ids_fail_the_build(self):
        source = BUILDER["CHAPTERS"][2][0].read_text()
        for updated in (source.replace("  # reader-id: cell-16", "", 1),
                        source.replace("reader-id: cell-18", "reader-id: cell-16", 1)):
            with self.with_source(updated), self.assertRaisesRegex(ValueError, "unique permanent reader-id"):
                BUILDER["build_reader"](2)


if __name__ == "__main__":
    unittest.main()
