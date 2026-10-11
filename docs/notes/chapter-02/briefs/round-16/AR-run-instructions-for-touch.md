# Brief AR: running cells with the toolbar, on a phone and on a computer

The author ruled out the first notebook version as too big for a phone; the chapter's notebook is
now the Jupyter version only. Its texts tell the reader to use the menus at the top of the page (Run,
then Run All Cells; File, then Save Notebook). On a phone those menus open when tapped, but their
items do nothing. The toolbar's buttons do respond to a tap, so the page gets two labelled buttons
and the texts below are rewritten to use the toolbar. Every fact was checked on the built page on
10 October 2026, in Chromium, by touch at phone width and by mouse at desktop width.

Write each slot as plain sentences, following `docs/style.md` and the writing standard in
`AGENTS.md`. Write only the slots below, each under its key. Do not add facts. Do not mention a
lab, an engine, a simulator, Jupyter, JupyterLite, marimo, Pyodide or WebAssembly, and do not
mention the menus at the top of the page or that anything does not work on a phone. The reader is
"you", a data engineer, on a phone or a computer: say "press" for a button, which covers a tap and a
click. British English. No em dashes. A button's label is written as it appears on the page.

## The toolbar, as the page shows it

A row of buttons at the top of the page, under the page's title. From left to right, among others:
a save button (an icon of a disk); then the two new buttons, which show their labels as text; then a
run button (a triangle).

- New button 1: runs every cell of the notebook, from the top.
- New button 2: runs the selected cell and every cell below it.
- The run button (a triangle): runs the selected cell, then selects the next cell. On a keyboard,
  Shift+Enter does the same.
- The save button (a disk): saves the notebook. On a keyboard, Ctrl+S (Cmd+S on a Mac) does the
  same.
- To select a cell, press it.

## Slots

- **label_run_all** and **label_run_below**: the two new buttons' labels. At most two words each,
  each starting with "Run".
- **how_to**: one paragraph in part 1's opening, after the situation and the paragraph on the three
  systems, before the figures. Facts, in this order:
  1. Nothing on the page runs until you run it. Run every cell first: press the first new button,
     in the toolbar at the top.
  2. To run one cell, select it and press the run button, a triangle, in the toolbar (or press
     Shift+Enter on a keyboard).
  3. A cell does not run again when a cell it uses changes. After you change a cell, select it and
     press the second new button, which runs it and every cell below it.
  4. To keep your changes, press the save button, a disk, in the toolbar (or Ctrl+S, Cmd+S on a
     Mac). After a reload, the page shows your saved copy.
  5. Your saved copy stays in this browser and is shown instead of the chapter, even after the
     chapter is updated.
- **run_first**: part 2's first instruction, at the end of its opening section. Facts: nothing on
  the page runs until you run it; run every cell first: press the first new button, in the toolbar
  at the top. One or two sentences.
- **thursday_row**: before a cell that reads the row for one day from `daily_sales`; the day is set
  in the code cell above it. Facts: the cell reads the row for the same day from `daily_sales`; the
  day is the one set in the code cell above; if you change the day there, run this cell too, because
  it does not run again by itself: select the code cell above and press the second new button.
- **changes**: before a menu of changes to the shop (a list you choose from), with four cells below
  it that show the platform after a week run with the change chosen. Facts: choose a change from the
  menu below; then select the first cell below the menu and press the second new button; the cells
  below show the platform on Monday morning, after the week ran with the change you chose; the
  cells above the menu keep showing the week as it ran.
