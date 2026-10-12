# Copyright © 2026 Christopher Snow

"""Builds the written chapters as Jupyter notebooks, for JupyterLite, from their source files.

Each written chapter is a notebook. Each is written as a Python file of cells
(`notebook/chapter_01.py` and `chapter_02.py`), in marimo's file format, which keeps the chapter
diffable and lets the tests read every sentence; marimo itself no longer reaches a reader (the
author ruled it out as too big for a phone). This turns each file into a Jupyter notebook, cell by
cell, with the same prose and the same visible code:

- the setup cells, at the foot of a source file, move to the top, since Jupyter runs from the top,
  with the install of the packages the page bundles;
- the control (the menu of changes) becomes an ipywidget; a figure shown with
  `mo.Html` is drawn here, from the shop's week, into a Markdown cell (notebook/shop/figures.py);
  a column of outputs is `display`; a callout (the warning, and
  the steps for running and saving the page) is a box, a div the course's stylesheet draws.

Anything in a source file this does not know how to carry over stops the build.

Usage: python3 build_ipynb.py OUT_DIR [--check]
  writes OUT_DIR/chapter_01.ipynb and OUT_DIR/chapter_02.ipynb.
  --check  runs each notebook here, in CPython, first, and stops if a cell raises.
"""

import ast
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
}

# Jupyter runs from the top: these come first. In the browser the three packages the page bundles
# are installed from the site itself, without the dependencies the kernel already has (IPython,
# traitlets) or does not need (ipywidgets' front-end package); run here, at build time, they are
# already importable.
SETUP = [
    """import sys

if sys.platform == "emscripten":
    import piplite

    await piplite.install(["comm", "ipywidgets", "shop"], deps=False)""",
    """import ipywidgets as widgets
from IPython.display import HTML, display

import shop""",
    """week = shop.run_week()
storage, warehouse, reporting = week.storage, week.warehouse, week.reporting""",
]


def lines_of(source: str, stmts: list[ast.stmt]) -> str:
    """The statements' source as they stand in the source file, less the four spaces marimo
    indents a cell's body by. A line with less indent is inside a string (the handover note's
    lines start at the margin) and is kept as it is."""
    lines = source.splitlines()[stmts[0].lineno - 1 : stmts[-1].end_lineno]
    return "\n".join(line[4:] if line.startswith("    ") else line for line in lines)


def is_call(node: ast.AST, attr: str) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == attr


def keyword(call: ast.Call, name: str) -> ast.expr:
    return next(k.value for k in call.keywords if k.arg == name)


def find(stmts: list[ast.stmt], attr: str) -> ast.Call:
    return next(n for s in stmts for n in ast.walk(s) if is_call(n, attr))


# A callout's kind, and the class the course's stylesheet (notebook/buttons/style/index.css) gives
# its box. A kind not listed here stops the build.
BOXES = {"warn": "ms-box-warning", "info": "ms-box-steps"}


def box(name: str, text: str) -> str:
    """A box in a Markdown cell: a div the stylesheet draws, with Markdown inside it."""
    return f'<div class="ms-box {name}">\n\n{text}\n\n</div>'


def code_font(text: str) -> str:
    """A label's `names` in the code font, as Markdown would set them, in HTML."""
    parts = text.split("`")
    return "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(parts))


def inline(text: str) -> str:
    """A sentence's Markdown `names` and **button labels** as HTML, for a lead a widget shows."""
    parts = code_font(text).split("**")
    return "".join(f"<strong>{p}</strong>" if i % 2 else p for i, p in enumerate(parts))


def menu(stmts: list[ast.stmt]) -> str:
    """The menu of changes: its lead, its label, and a dropdown of the same options."""
    call = find(stmts, "dropdown")
    options = ast.literal_eval(keyword(call, "options"))
    label = ast.literal_eval(keyword(call, "label"))
    default = ast.literal_eval(keyword(call, "value"))
    lead = ast.literal_eval(find(stmts, "md").args[0])
    return f"""change = widgets.Dropdown(
    options={list(options.items())!r},
    value={options[default]!r},
    layout=widgets.Layout(width="100%"),
)
display(HTML({"<p>" + inline(lead) + "</p><p>" + inline(label) + "</p>"!r}), change)"""


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
            out.append(nbformat.v4.new_markdown_cell(textwrap.dedent(first.value.args[0].value).strip()))
            continue
        code = lines_of(source, stmts)
        if not hidden:
            out.append(nbformat.v4.new_code_cell(code))
        elif "mo.callout(" in code:
            # A box: the warning, or the steps for running and saving the page. The setup, hidden,
            # follows the warning and any box straight after it, so the boxes stay together.
            kind = keyword(find(stmts, "callout"), "kind").value
            text = textwrap.dedent(ast.literal_eval(find(stmts, "md").args[0])).strip()
            out.append(nbformat.v4.new_markdown_cell(box(BOXES[kind], text)))
            if kind == "warn" or setup_at == len(out) - 1:
                setup_at = len(out)
        elif "import marimo as mo" in code or "week = shop.run_week()" in code:
            continue  # the setup, which Jupyter runs first (SETUP)
        elif "mo.ui.dropdown(" in code:
            out.append(nbformat.v4.new_code_cell(menu(stmts), metadata=HIDDEN))
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "Html"):
            # A figure: drawn here from the shop's week and written into a Markdown cell, so it
            # shows before anything runs.
            drawn = eval(compile(ast.Expression(first.value.args[0]), "figure", "eval"), {"figures": figures, "week": WEEK})
            out.append(nbformat.v4.new_markdown_cell(drawn))
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "vstack"):
            parts = ",\n    ".join(ast.unparse(e) for e in first.value.args[0].elts)
            out.append(nbformat.v4.new_code_cell(f"display(\n    {parts},\n)", metadata=HIDDEN))
        else:
            raise SystemExit(f"no Jupyter form for this hidden cell of the source file:\n{code}")
    if setup_at is None:
        raise SystemExit(f"chapter {chapter} has no warning: the setup has nowhere to go")
    out[setup_at:setup_at] = [nbformat.v4.new_code_cell(setup, metadata=HIDDEN) for setup in SETUP]
    for i, cell in enumerate(out):
        cell["id"] = f"cell-{i + 1:02d}"
    nb = nbformat.v4.new_notebook(cells=out)
    nb.metadata = {
        "kernelspec": {"name": "python", "display_name": "Python (Pyodide)", "language": "python"},
        "language_info": {"name": "python"},
    }
    return nb


def build_all() -> dict[str, nbformat.NotebookNode]:
    """Every chapter, by notebook name."""
    return {name: build(chapter) for chapter, (_, name) in CHAPTERS.items()}


def check(nb: nbformat.NotebookNode) -> None:
    """Runs a copy of the notebook in CPython, from the notebook's folder so `shop` imports; a cell
    that raises stops the build.

    The page itself ships without outputs. JupyterLite opens a notebook as untrusted, and an
    untrusted notebook's saved HTML is shown with its styles stripped and its widgets as text, so
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
    for name, nb in build_all().items():
        if "--check" in sys.argv:
            check(nb)
        nbformat.validate(nb)
        nbformat.write(nb, str(out / name))
        print(f"{out / name}: {len(nb.cells)} cells")
