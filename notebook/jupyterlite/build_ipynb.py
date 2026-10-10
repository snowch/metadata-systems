# Copyright © 2026 Christopher Snow

"""Builds Chapter 1 as Jupyter notebooks, for JupyterLite, from the marimo notebooks.

The chapter is in two parts, one notebook each. The prose and the visible code are the marimo
notebooks' (`notebook/chapter_01_part_1.py` and `_part_2.py`), cell by cell, so the two versions
say the same thing. What differs is what the two tools do differently:

- marimo runs cells in the order their names need, so its setup cells sit at its foot; Jupyter runs
  from the top, so they move there, with the install of the two packages the page bundles.
- marimo's controls (the menu of changes, the handover note) become ipywidgets; a figure shown with
  `mo.Html` is IPython's `HTML`; a column of outputs is `display`; the callout is a quoted
  paragraph.
- the sentences about running cells say what Jupyter does (`words.py`), and a link from one part
  to the other names the other notebook.

Anything in the marimo notebook this does not know how to carry over stops the build.

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
sys.path.insert(0, str(HERE))
import words  # noqa: E402

HIDDEN = {"jupyter": {"source_hidden": True}}

# The two parts: each marimo notebook, and the name of the Jupyter notebook built from it.
PARTS = {
    1: (HERE.parent / "chapter_01_part_1.py", "chapter_01_part_1.ipynb"),
    2: (HERE.parent / "chapter_01_part_2.py", "chapter_01_part_2.ipynb"),
}

# The marimo pages link to each other by their place in the site (export.sh): part 1 is the site's
# index, part 2 is part-2.html. In JupyterLite each links to the other notebook by its name.
LINKS = {"](./)": f"]({PARTS[1][1]})", "](part-2.html)": f"]({PARTS[2][1]})"}

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
    """The statements' source, dedented, as they stand in the marimo notebook."""
    lines = source.splitlines()
    return textwrap.dedent("\n".join(lines[stmts[0].lineno - 1 : stmts[-1].end_lineno]))


def is_call(node: ast.AST, attr: str) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == attr


def keyword(call: ast.Call, name: str) -> ast.expr:
    return next(k.value for k in call.keywords if k.arg == name)


def find(stmts: list[ast.stmt], attr: str) -> ast.Call:
    return next(n for s in stmts for n in ast.walk(s) if is_call(n, attr))


def code_font(text: str) -> str:
    """A label's `names` in the code font, as marimo draws them, in HTML."""
    parts = text.split("`")
    return "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(parts))


def menu(stmts: list[ast.stmt], source: str) -> str:
    if words.MARIMO["CHANGES"] not in source:
        raise SystemExit("the marimo notebook's lead for the menu of changes has changed: update words.py")
    call = find(stmts, "dropdown")
    options = ast.literal_eval(keyword(call, "options"))
    label = ast.literal_eval(keyword(call, "label"))
    default = ast.literal_eval(keyword(call, "value"))
    return f"""change = widgets.Dropdown(
    options={list(options.items())!r},
    value={options[default]!r},
    layout=widgets.Layout(width="100%"),
)
display(HTML({"<p>" + words.CHANGES + "</p><p>" + label + "</p>"!r}), change)"""


def note(stmts: list[ast.stmt]) -> str:
    call = find(stmts, "text_area")
    label = ast.literal_eval(keyword(call, "label"))
    placeholder = ast.literal_eval(keyword(call, "placeholder"))
    return f"""note = widgets.Textarea(placeholder={placeholder!r}, layout=widgets.Layout(width="100%", height="12em"))
widgets.VBox([widgets.HTML({"<p>" + code_font(label) + "</p>"!r}), note])"""


def build(part: int, replaced: dict[str, int]) -> nbformat.NotebookNode:
    """One part's Jupyter notebook; `replaced` counts where each slot of `words.py` went."""
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
            text = textwrap.dedent(first.value.args[0].value).strip()
            for key, marimo in words.MARIMO.items():
                if marimo in text and key != "CHANGES":
                    text = text.replace(marimo, getattr(words, key))
                    replaced[key] += 1
            for key, marimo in words.AFTER.items():
                if marimo in text:
                    text = text.replace(marimo, marimo + "\n\n" + getattr(words, key))
                    replaced[key] += 1
            for marimo, jupyter in LINKS.items():
                text = text.replace(marimo, jupyter)
            out.append(nbformat.v4.new_markdown_cell(text))
            continue
        code = lines_of(source, stmts)
        if not hidden:
            out.append(nbformat.v4.new_code_cell(code))
        elif "mo.callout(" in code:
            # The warning, then the setup, hidden, before the chapter's first section.
            out.append(nbformat.v4.new_markdown_cell("> " + words.WARNING[part]))
            out.extend(nbformat.v4.new_code_cell(setup, metadata=HIDDEN) for setup in SETUP)
        elif "import marimo as mo" in code or "week = shop.run_week()" in code:
            continue  # the setup, which Jupyter runs first (SETUP)
        elif "mo.ui.dropdown(" in code:
            out.append(nbformat.v4.new_code_cell(menu(stmts, source), metadata=HIDDEN))
            replaced["CHANGES"] += 1
        elif "mo.ui.text_area(" in code:
            out.append(nbformat.v4.new_code_cell(note(stmts), metadata=HIDDEN))
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "Html"):
            out.append(nbformat.v4.new_code_cell("HTML(" + ast.unparse(first.value.args[0]) + ")", metadata=HIDDEN))
        elif len(stmts) == 1 and isinstance(first, ast.Expr) and is_call(first.value, "vstack"):
            parts = ",\n    ".join(ast.unparse(e) for e in first.value.args[0].elts)
            out.append(nbformat.v4.new_code_cell(f"display(\n    {parts},\n)", metadata=HIDDEN))
        else:
            raise SystemExit(f"no Jupyter form for this hidden cell of the marimo notebook:\n{code}")
    if not any("piplite" in "".join(c.source) for c in out):
        raise SystemExit(f"part {part}'s warning has moved: the setup has nowhere to go")
    for i, cell in enumerate(out):
        cell["id"] = f"cell-{i + 1:02d}"
    nb = nbformat.v4.new_notebook(cells=out)
    nb.metadata = {
        "kernelspec": {"name": "python", "display_name": "Python (Pyodide)", "language": "python"},
        "language_info": {"name": "python"},
    }
    return nb


def build_all() -> dict[str, nbformat.NotebookNode]:
    """Both parts, by notebook name; each sentence `words.py` replaces is found exactly once."""
    replaced = {key: 0 for key in [*words.MARIMO, *words.AFTER]}
    notebooks = {name: build(part, replaced) for part, (_, name) in PARTS.items()}
    for key, count in replaced.items():
        if count != 1:
            raise SystemExit(f"the sentences words.py places {key} by matched {count} cells, not 1: update words.py")
    return notebooks


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
