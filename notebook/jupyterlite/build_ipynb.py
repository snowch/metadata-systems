# Copyright © 2026 Christopher Snow

"""Builds Chapter 1 as Jupyter notebooks, for JupyterLite, from the chapter's two source files.

The chapter is in two parts, one notebook each. Each part is written as a Python file of cells
(`notebook/chapter_01_part_1.py` and `_part_2.py`), in marimo's file format, which keeps the chapter
diffable and lets the tests read every sentence; marimo itself no longer reaches a reader (the
author ruled it out as too big for a phone). This turns each file into a Jupyter notebook, cell by
cell, with the same prose and the same visible code:

- the setup cells, at the foot of a source file, move to the top, since Jupyter runs from the top,
  with the install of the packages the page bundles;
- the controls (the menu of changes, the handover note) become ipywidgets; a figure shown with
  `mo.Html` is IPython's `HTML`; a column of outputs is `display`; the warning is a quoted
  paragraph.

Anything in a source file this does not know how to carry over stops the build.

Usage: python3 build_ipynb.py OUT_DIR [--check]
  writes OUT_DIR/chapter_01_part_1.ipynb and OUT_DIR/chapter_01_part_2.ipynb.
  --check  runs each notebook here, in CPython, first, and stops if a cell raises.
"""

import ast
import sys
import textwrap
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent

HIDDEN = {"jupyter": {"source_hidden": True}}

# The two parts: each source file, and the name of the Jupyter notebook built from it. The parts link
# to each other by these names.
PARTS = {
    1: (HERE.parent / "chapter_01_part_1.py", "chapter_01_part_1.ipynb"),
    2: (HERE.parent / "chapter_01_part_2.py", "chapter_01_part_2.ipynb"),
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

import shop
from shop import figures""",
    """week = shop.run_week()
storage, warehouse, reporting = week.storage, week.warehouse, week.reporting""",
]


def lines_of(source: str, stmts: list[ast.stmt]) -> str:
    """The statements' source, dedented, as they stand in the source file."""
    lines = source.splitlines()
    return textwrap.dedent("\n".join(lines[stmts[0].lineno - 1 : stmts[-1].end_lineno]))


def is_call(node: ast.AST, attr: str) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == attr


def keyword(call: ast.Call, name: str) -> ast.expr:
    return next(k.value for k in call.keywords if k.arg == name)


def find(stmts: list[ast.stmt], attr: str) -> ast.Call:
    return next(n for s in stmts for n in ast.walk(s) if is_call(n, attr))


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


def note(stmts: list[ast.stmt]) -> str:
    call = find(stmts, "text_area")
    label = ast.literal_eval(keyword(call, "label"))
    placeholder = ast.literal_eval(keyword(call, "placeholder"))
    return f"""note = widgets.Textarea(placeholder={placeholder!r}, layout=widgets.Layout(width="100%", height="12em"))
widgets.VBox([widgets.HTML({"<p>" + code_font(label) + "</p>"!r}), note])"""


def build(part: int) -> nbformat.NotebookNode:
    """One part's Jupyter notebook."""
    source = PARTS[part][0].read_text(encoding="utf-8")
    out = []
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
            # The warning, then the setup, hidden, before the chapter's first section.
            warning = ast.literal_eval(find(stmts, "md").args[0])
            out.append(nbformat.v4.new_markdown_cell("> " + warning))
            out.extend(nbformat.v4.new_code_cell(setup, metadata=HIDDEN) for setup in SETUP)
        elif "import marimo as mo" in code or "week = shop.run_week()" in code:
            continue  # the setup, which Jupyter runs first (SETUP)
        elif "mo.ui.dropdown(" in code:
            out.append(nbformat.v4.new_code_cell(menu(stmts), metadata=HIDDEN))
        elif "mo.ui.text_area(" in code:
            out.append(nbformat.v4.new_code_cell(note(stmts), metadata=HIDDEN))
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "Html"):
            out.append(nbformat.v4.new_code_cell("HTML(" + ast.unparse(first.value.args[0]) + ")", metadata=HIDDEN))
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "vstack"):
            parts = ",\n    ".join(ast.unparse(e) for e in first.value.args[0].elts)
            out.append(nbformat.v4.new_code_cell(f"display(\n    {parts},\n)", metadata=HIDDEN))
        else:
            raise SystemExit(f"no Jupyter form for this hidden cell of the source file:\n{code}")
    if not any("piplite" in "".join(c.source) for c in out):
        raise SystemExit(f"part {part} has no warning: the setup has nowhere to go")
    for i, cell in enumerate(out):
        cell["id"] = f"cell-{i + 1:02d}"
    nb = nbformat.v4.new_notebook(cells=out)
    nb.metadata = {
        "kernelspec": {"name": "python", "display_name": "Python (Pyodide)", "language": "python"},
        "language_info": {"name": "python"},
    }
    return nb


def build_all() -> dict[str, nbformat.NotebookNode]:
    """Both parts, by notebook name."""
    return {name: build(part) for part, (_, name) in PARTS.items()}


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
