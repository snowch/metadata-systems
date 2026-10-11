# Brief AL: the notebook's warning for phones, how to run a cell, and one menu label

Chapter 1 is prototyped as a notebook: the essay, with cells of Python the reader runs, changes
and runs again, in the browser. Three slots need words. Every fact below was measured on the
exported page on 10 October 2026, in Chromium, served from this machine: the measurements and
their sources are in `docs/notes/notebook-prototype.md`. Write each slot as plain sentences,
following `docs/style.md` and the writing standard in `AGENTS.md`. Write only the slots below, each
under its key. Do not add facts. Do not mention a lab, an engine, a simulator, marimo, Pyodide or
WebAssembly. The reader is "you", a data engineer. British English. No em dashes.

## Slots

- **phone_warning**: a short note at the top of the page, before the chapter starts, for a reader
  on a phone. At most four sentences. Facts, in this order:
  1. The page runs Python in your browser.
  2. The first time you open it, your browser downloads up to about 32 MB.
  3. On a computer, Python took 10 to 15 seconds to start, and the page used about 1 GB of memory.
  4. If a phone runs short of memory, the browser may reload the page, and a reload loses what you
     changed or wrote on the page.
- **how_to**: one short paragraph in the chapter's opening, after the situation, before the
  figures. Facts:
  1. The boxes of code with numbered lines are cells you can run.
  2. To run a cell, press its run button, a triangle at the top right of the cell, or press
     Ctrl+Enter (Cmd+Enter on a Mac) while typing in the cell.
  3. On a computer the run button appears when the pointer is over the cell; on a phone it is
     always there.
  4. When you run a cell, the cells that use its results run again.
  5. Nothing you change is saved: reloading the page shows the chapter as it was published.
- **change_option_refunds**: one label in a menu of changes to the shop, plain text with no
  backticks, at most eight words. It replaces "From Saturday, daily_sales program keeps every
  unrefunded order", which lacks an article. Facts: from Saturday's row on, the program that
  writes `daily_sales` keeps every order that has not been refunded. The other labels in the menu
  are "The shop stays as it is", "An analyst copies clean_orders every night" and "The daily_sales
  program fails on the last night".
