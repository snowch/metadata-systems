# Copyright © 2026 Christopher Snow

"""Builds the written chapters as Jupyter notebooks, for JupyterLite, from their source files.

Each written chapter is a notebook. Each is written as a Python file of cells
(`notebook/chapter_01.py` and `chapter_02.py`), in marimo's file format, which keeps the chapter
diffable and lets the tests read every sentence; marimo itself no longer reaches a reader (the
author ruled it out as too big for a phone). This turns each file into a Jupyter notebook, cell by
cell, with the same prose and the same visible code:

- the setup cells, at the foot of a source file, move to the top, since Jupyter runs from the top,
  with the install of the packages the page bundles;
- a figure shown with `mo.Html` is drawn here, from the shop's week, into a Markdown cell (notebook/shop/figures.py);
  a column of outputs is `display`; a callout (the warning, and
  the steps for running and saving the page) is a box, a div the course's stylesheet draws.

Anything in a source file this does not know how to carry over stops the build.

Usage: python3 build_ipynb.py OUT_DIR [--check]
  writes OUT_DIR/chapter_01.ipynb and OUT_DIR/chapter_02.ipynb.
  --check  runs each notebook here, in CPython, first, and stops if a cell raises.
"""

import ast
import hashlib
import json
import re
import sys
import textwrap
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent

# The shop's week, which the build draws each figure from (notebook/shop/figures.py).
sys.path.insert(0, str(HERE.parent))
import shop  # noqa: E402
from shop import figures  # noqa: E402

WEEK = shop.run_week()

HIDDEN = {"jupyter": {"source_hidden": True}}

# The chapters: each source file, and the name of the Jupyter notebook built from it. The chapters
# link to each other by these names.
CHAPTERS = {
    1: (HERE.parent / "chapter_01.py", "chapter_01.ipynb"),
    2: (HERE.parent / "chapter_02.py", "chapter_02.ipynb"),
    3: (HERE.parent / "chapter_03.py", "chapter_03.ipynb"),
    4: (HERE.parent / "chapter_04.py", "chapter_04.ipynb"),
    5: (HERE.parent / "chapter_05.py", "chapter_05.ipynb"),
    6: (HERE.parent / "chapter_06.py", "chapter_06.ipynb"),
    7: (HERE.parent / "chapter_07.py", "chapter_07.ipynb"),
    8: (HERE.parent / "chapter_08.py", "chapter_08.ipynb"),
    9: (HERE.parent / "chapter_09.py", "chapter_09.ipynb"),
    10: (HERE.parent / "chapter_10.py", "chapter_10.ipynb"),
    11: (HERE.parent / "chapter_11.py", "chapter_11.ipynb"),
    12: (HERE.parent / "chapter_12.py", "chapter_12.ipynb"),
    13: (HERE.parent / "chapter_13.py", "chapter_13.ipynb"),
    14: (HERE.parent / "chapter_14.py", "chapter_14.ipynb"),
    15: (HERE.parent / "chapter_15.py", "chapter_15.ipynb"),
    16: (HERE.parent / "chapter_16.py", "chapter_16.ipynb"),
    17: (HERE.parent / "chapter_17.py", "chapter_17.ipynb"),
    18: (HERE.parent / "chapter_18.py", "chapter_18.ipynb"),
    19: (HERE.parent / "chapter_19.py", "chapter_19.ipynb"),
    20: (HERE.parent / "chapter_20.py", "chapter_20.ipynb"),
    21: (HERE.parent / "chapter_21.py", "chapter_21.ipynb"),
    22: (HERE.parent / "chapter_22.py", "chapter_22.ipynb"),
    23: (HERE.parent / "chapter_23.py", "chapter_23.ipynb"),
    24: (HERE.parent / "chapter_24.py", "chapter_24.ipynb"),
    25: (HERE.parent / "chapter_25.py", "chapter_25.ipynb"),
    26: (HERE.parent / "chapter_26.py", "chapter_26.ipynb"),
    27: (HERE.parent / "chapter_27.py", "chapter_27.ipynb"),
    28: (HERE.parent / "chapter_28.py", "chapter_28.ipynb"),
    29: (HERE.parent / "chapter_29.py", "chapter_29.ipynb"),
    30: (HERE.parent / "chapter_30.py", "chapter_30.ipynb"),
    31: (HERE.parent / "chapter_31.py", "chapter_31.ipynb"),
    32: (HERE.parent / "chapter_32.py", "chapter_32.ipynb"),
    33: (HERE.parent / "chapter_33.py", "chapter_33.ipynb"),
}

# Jupyter runs from the top: these come first. In the browser the shop's package is installed from
# the site itself; run here, at build time, it is already importable.
SETUP = [
    """import sys

if sys.platform == "emscripten":
    import piplite

    await piplite.install(["shop"], deps=False)""",
    """from IPython.display import HTML, display

import shop""",
    """week = shop.run_week()
storage, warehouse, reporting = week.storage, week.warehouse, week.reporting""",
]


def lines_of(source: str, stmts: list[ast.stmt]) -> str:
    """The statements' source as they stand in the source file, with any comment above the first,
    less the four spaces marimo indents a cell's body by. A line with less indent is inside a string
    (a note a reader writes starts at the margin) and is kept as it is."""
    lines = source.splitlines()
    start = stmts[0].lineno - 1
    # A comment above a cell's first statement belongs to the cell.
    while start > 0 and lines[start - 1].strip().startswith("#"):
        start -= 1
    lines = lines[start : stmts[-1].end_lineno]
    return "\n".join(line[4:] if line.startswith("    ") else line for line in lines)


def is_call(node: ast.AST, attr: str) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == attr


def keyword(call: ast.Call, name: str) -> ast.expr:
    return next(k.value for k in call.keywords if k.arg == name)


def find(stmts: list[ast.stmt], attr: str) -> ast.Call:
    return next(n for s in stmts for n in ast.walk(s) if is_call(n, attr))


# A callout's kind, and the class the course's stylesheet (notebook/buttons/style/index.css) gives
# its box: the warning, the steps for running the page, and the requirement a chapter questions. A
# kind not listed here stops the build.
BOXES = {"warn": "ms-box-warning", "info": "ms-box-steps", "neutral": "ms-box-requirement", "success": "ms-box-finding"}


def box(name: str, text: str) -> str:
    """A box in a Markdown cell: a div the stylesheet draws, with Markdown inside it."""
    return f'<div class="ms-box {name}">\n\n{text}\n\n</div>'


# A figure inside a Markdown cell's text, where it must sit with the words around it: in a closed
# block, say, which cannot span two cells. The text holds the figure's call in a comment,
# `<!-- figure: figures.figure(...) -->`, and the build draws it there, as it draws a figure cell.
FIGURE = re.compile(r"<!-- figure: (.+?) -->", re.S)


def draw(call: str) -> str:
    """A figure, drawn from the shop's week (notebook/shop/figures.py)."""
    return eval(compile(call, "figure", "eval"), {"figures": figures, "week": WEEK, "shop": shop})


def build(chapter: int) -> nbformat.NotebookNode:
    """One chapter's Jupyter notebook."""
    source = CHAPTERS[chapter][0].read_text(encoding="utf-8")
    out = []
    setup_at = None  # where the setup goes: after the boxes the chapter opens with
    for node in ast.parse(source).body:
        if not isinstance(node, ast.FunctionDef):
            continue
        deco = node.decorator_list[0]
        hidden = isinstance(deco, ast.Call) and any(k.arg == "hide_code" and k.value.value for k in deco.keywords)
        stmts = [s for s in node.body if not isinstance(s, ast.Return)]
        first = stmts[0]
        if len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "md") and isinstance(first.value.args[0], ast.Constant):
            text = textwrap.dedent(first.value.args[0].value).strip()
            answer = re.search(r"<!-- answer: (guesses|daily_sales|clean_orders|report) -->", text)
            metadata = {"ms": {"answer": answer.group(1)}} if answer else {}
            if answer:
                text = text.replace(answer.group(0), "").strip()
            out.append(nbformat.v4.new_markdown_cell(FIGURE.sub(lambda m: draw(m.group(1)), text), metadata=metadata))
            continue
        code = lines_of(source, stmts)
        marker = re.search(r"# reader-id: ([a-zA-Z0-9_-]+)", source.splitlines()[deco.lineno - 1])
        identity = {"ms": {"readerId": marker.group(1)}} if marker else {}
        if not hidden:
            out.append(nbformat.v4.new_code_cell(code, metadata=identity))
        elif "mo.callout(" in code:
            # A box: the warning, the steps for running and saving the page, or a requirement. The
            # setup, hidden, follows the warning and any box straight after it, so the boxes stay
            # together.
            kind = keyword(find(stmts, "callout"), "kind").value
            text = textwrap.dedent(ast.literal_eval(find(stmts, "md").args[0])).strip()
            out.append(nbformat.v4.new_markdown_cell(box(BOXES[kind], text)))
            if kind == "warn" or setup_at == len(out) - 1:
                setup_at = len(out)
        elif "import marimo as mo" in code or "week = shop.run_week()" in code:
            continue  # the setup, which Jupyter runs first (SETUP)
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "Html"):
            # A figure: drawn here from the shop's week and written into a Markdown cell, so it
            # shows before anything runs.
            drawn = draw(ast.unparse(first.value.args[0]))
            out.append(nbformat.v4.new_markdown_cell(drawn))
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "vstack"):
            parts = ",\n    ".join(ast.unparse(e) for e in first.value.args[0].elts)
            out.append(nbformat.v4.new_code_cell(f"display(\n    {parts},\n)", metadata={**HIDDEN, **identity}))
        else:
            raise SystemExit(f"no Jupyter form for this hidden cell of the source file:\n{code}")
    if setup_at is None:
        raise SystemExit(f"chapter {chapter} has no warning: the setup has nowhere to go")
    # Marked as the setup, which the row of buttons' extension runs, silently, as the page opens
    # (notebook/buttons/index.js, warmUp), so Python is ready by the time the reader runs a cell.
    out[setup_at:setup_at] = [nbformat.v4.new_code_cell(setup, metadata={**HIDDEN, "ms": {"setup": True}}) for setup in SETUP]
    for i, cell in enumerate(out):
        cell["id"] = f"cell-{i + 1:02d}"
    nb = nbformat.v4.new_notebook(cells=out)
    nb.metadata = {
        "kernelspec": {"name": "python", "display_name": "Python (Pyodide)", "language": "python"},
        "language_info": {"name": "python"},
    }
    nb.metadata["ms"] = stamp(nb)
    return nb


def digest(text: str) -> str:
    """The first 16 hexadecimal digits of the text's SHA-256."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def cells_text(cells: list) -> str:
    """The notebook's cells as one text, each its type, a line break, its source and a NUL: the
    text the row of buttons' extension hashes too (notebook/buttons/index.js, sourcesOf)."""
    return "".join(f"{cell['cell_type']}\n{''.join(cell['source'])}\0" for cell in cells)


def stamp(nb: nbformat.NotebookNode) -> dict[str, str]:
    """The chapter's version, which changes whenever anything in the published notebook does, and
    the hash of its cells as published. A reader's saved copy keeps both, so the extension can tell
    that the chapter has been updated since, and whether the reader changed any cell
    (notebook/buttons/index.js, update)."""
    return {"version": digest(nbformat.writes(nb)), "sources": digest(cells_text(nb.cells))}


def build_all() -> dict[str, nbformat.NotebookNode]:
    """Every canonical chapter in the reading view."""
    return {name: build_reader(chapter) for chapter, (_, name) in CHAPTERS.items()}


def build_reader(chapter: int = 1) -> nbformat.NotebookNode:
    """Keep the chapter's cells and computations, with reader controls and concise descriptions."""
    nb = build(chapter)
    words = json.loads((HERE / "reader.json").read_text(encoding="utf-8"))
    descriptions = words["descriptions"] if chapter == 1 else {}
    replaced = set()
    first_ids = ["products", "customers", "orders", "clean_customers", "clean_orders", "daily_sales"]
    heading = f"Chapter {chapter}"
    counts = {}
    index = 0
    identities = set()
    for cell in nb.cells:
        cell.metadata["deletable"] = False
        if cell.cell_type == "markdown":
            cell.metadata["editable"] = False
            if "ms-box-warning" in cell.source:
                cell.source = box("ms-box-warning", words["warning"])
            elif "ms-box-steps" in cell.source and "**Running and saving" in cell.source:
                cell.source = box("ms-box-steps", words["instructions" if chapter == 1 else "instructionsDependent"])
            title = cell.source.split("\n", 1)[0]
            if title in descriptions:
                cell.source = descriptions[title]
                replaced.add(title)
            if cell.metadata.get("ms", {}).get("answer") == "guesses":
                cell.source = words["answerInstructions"]
            for before, after in words.get("proseReplacements", {}).items():
                cell.source = cell.source.replace(before, after)
            for match in re.finditer(r"^#{1,6} (.+)$", cell.source, re.M):
                heading = match.group(1).replace("`", "")
        elif cell.metadata.get("ms", {}).get("setup"):
            cell.metadata["editable"] = False
        else:
            counts[heading] = counts.get(heading, 0) + 1
            title = heading if counts[heading] == 1 else f"{heading} ({counts[heading]})"
            identifier = cell.metadata.get("ms", {}).get("readerId")
            if not identifier or identifier in identities:
                raise ValueError(f"Chapter {chapter}: every example needs a unique permanent reader-id")
            identities.add(identifier)
            if chapter == 1:
                title = dict(zip(first_ids, ["The product catalogue", "The customers", "The orders", "clean_customers", "clean_orders", "daily_sales"]))[identifier]
            cell.metadata["ms"] = {"example": {"id": identifier, "title": title, "source": cell.source,
                "editable": not cell.metadata.get("jupyter", {}).get("source_hidden", False)}}
            index += 1
    if chapter == 1 and index != len(first_ids):
        raise ValueError("Chapter 1 reader examples no longer match the chapter")
    if replaced != descriptions.keys():
        raise ValueError("Reader descriptions no longer match the chapter headings")
    nb.metadata["ms"] = {**stamp(nb), "reader": True, "dependent": chapter != 1}
    return nb


def check(nb: nbformat.NotebookNode) -> None:
    """Runs a copy of the notebook in CPython, from the notebook's folder so `shop` imports; a cell
    that raises stops the build.

    The page itself ships without outputs. JupyterLite opens a notebook as untrusted, and an
    untrusted notebook's saved HTML is shown with its styles stripped, so
    every figure would look broken until the reader ran the notebook; signing it does not help,
    since the signature lives in the signing machine's database, not in the file."""
    import copy

    from nbclient import NotebookClient

    NotebookClient(
        copy.deepcopy(nb),
        kernel_name="python3",
        timeout=300,
        resources={"metadata": {"path": str(HERE.parent)}},
    ).execute()


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "chapter_01b.ipynb").unlink(missing_ok=True)
    for name, nb in build_all().items():
        if "--check" in sys.argv:
            check(nb)
        nbformat.validate(nb)
        nbformat.write(nb, str(out / name))
        print(f"{out / name}: {len(nb.cells)} cells")
