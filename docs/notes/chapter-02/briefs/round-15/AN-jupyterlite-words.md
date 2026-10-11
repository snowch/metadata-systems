# Brief AN: the JupyterLite version's own words

Chapter 1 is also built as a Jupyter notebook in JupyterLite, to compare with the marimo notebook.
The prose is the marimo notebook's, except four slots where Jupyter works differently: Jupyter runs
nothing until the reader runs it, and a cell does not run again when a cell it uses changes. Every
fact below was checked on the built page on 10 October 2026, in Chromium. Write each slot as plain
sentences, following `docs/style.md` and the writing standard in `AGENTS.md`. Write only the slots
below, each under its key. Do not add facts. Do not mention a lab, an engine, a simulator,
JupyterLite, marimo, Pyodide or WebAssembly. Menu names are written as the page shows them, with a
comma between a menu and its item: "Run, then Run All Cells". The reader is "you", a data engineer.
British English. No em dashes.

## Slots

- **WARNING**: a short note at the top of the page, for a reader on a phone. At most four
  sentences. Facts, in this order:
  1. The page runs Python in your browser.
  2. The first time you open it, your browser downloads about 13 MB.
  3. On a computer, running every cell took about 10 seconds, and the page used about 440 MB of
     memory.
  4. If a phone runs short of memory, the browser may reload the page, and a reload loses anything
     you have not saved.
- **HOW_TO**: one paragraph in the chapter's opening, after the situation, before the figures.
  Facts:
  1. Nothing on the page runs until you run it. Run every cell first: Run, then Run All Cells, in
     the menu at the top.
  2. To run one cell, select it and press Shift+Enter, or press the run button, a triangle, in the
     toolbar.
  3. A cell does not run again when a cell it uses changes. After you change a cell, run the cells
     below it too: select the next cell, then Run, then Run Selected Cell and All Below.
  4. To keep your changes, save the notebook: File, then Save Notebook, or Ctrl+S (Cmd+S on a Mac).
     After a reload the page shows your saved copy.
  5. Your saved copy stays in this browser and is shown instead of the chapter, even after the
     chapter is updated.
- **THURSDAY_ROW**: before a cell that reads the row for one day from `daily_sales`, the day set in
  the cell above. Facts: it reads the row for the same day from `daily_sales`; the day is the one set
  in the cell above; if you changed the day there, run this cell too, because it does not run again
  by itself.
- **CHANGES**: before a menu of changes to the shop, with four cells below it that show the platform
  after a week run with the change chosen. Facts: choose a change; then select the first cell below
  the menu and choose Run, then Run Selected Cell and All Below; the cells below show the platform
  on Monday morning, after the week ran with the option you choose; the cells above the menu keep
  showing the week as it ran.
