# Brief AS: a row of large buttons at the top of the page

The author asked for custom buttons: the toolbar's buttons are 21 pixels tall, too small to press
easily on a phone. The page now has a row of three large buttons, each 44 pixels tall, and the
two labelled toolbar buttons are gone. The texts that send the reader to the toolbar are rewritten
to use the row. Every fact below was checked on the built page on 10 October 2026, in Chromium, by
touch at phone width and by mouse at desktop width.

Write each slot as plain sentences, following `docs/style.md` and the writing standard in
`AGENTS.md`. Write only the slots below, each under its key. Do not add facts. Do not mention a
lab, an engine, a simulator, Jupyter, JupyterLite, marimo, Pyodide or WebAssembly, and do not
mention the menus at the top of the page, the toolbar, or that anything does not work on a phone.
Do not explain why the buttons are large. The reader is "you", a data engineer, on a phone or a
computer: say "press" for a button, which covers a tap and a click. British English. No em dashes.
A button's label is written in bold, as it appears on the page: **Run all**.

## The row, as the page shows it

A row of three buttons at the top of the page, above the first cell. Each shows its label as text.
From left to right:

1. **Run all**: runs every cell of the notebook, from the top.
2. **Run below**: runs the selected cell and every cell below it.
3. The third button saves the notebook. On a keyboard, Ctrl+S (Cmd+S on a Mac) does the same.

## Slots

- **label_save**: the third button's label. One word.
- **how_to**: one paragraph in part 1's opening, after the situation and the paragraph on the three
  systems, before the figures. It replaces a paragraph that also told the reader how to run one
  cell; leave that out. Facts, in this order:
  1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the
     top of the page.
  2. A cell does not run again when a cell it uses changes. After you change a cell, select it and
     press **Run below**, which runs it and every cell below it.
  3. To keep your changes, press the third button, by its label from label_save (or Ctrl+S, Cmd+S
     on a Mac). After a reload, the page shows your saved copy.
  4. Your saved copy stays in this browser and is shown instead of the chapter, even after the
     chapter is updated.
- **run_first**: part 2's first instruction, at the end of its opening section. Facts: nothing on
  the page runs until you run it; run every cell first: press **Run all**, at the top of the page.
  One or two sentences.

## What the page says elsewhere, kept word for word

Do not repeat these.

- Before a cell that reads one day's row: "The code cell below reads the row from `daily_sales`
  for the day that the code cell above sets. If you change the day in the code cell above, run the
  code cell below too. It does not run again by itself. Select the code cell above and press **Run
  below**, which runs that cell and every cell below it."
- Before the menu of changes: "Choose a change to the shop from the menu below. Then select the
  first cell below the menu and press **Run below**. The cells below show the platform on Monday
  morning, after the week ran with the change you chose. The cells above the menu keep showing the
  week as it ran."
