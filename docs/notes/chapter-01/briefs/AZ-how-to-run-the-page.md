# Brief AZ: how to run the page, as steps in a box

Chapter 1's opening paragraph about running the page moves out of the story into a box of its own,
just under the box that warns about the download, so the story is not broken by instructions about
the page. The author asked for it as steps. The box looks different from the warning.

Write each slot following `docs/style.md` and `AGENTS.md`. British English. No em dashes. Do not
mention a lab, an engine, Jupyter, JupyterLite, Pyodide or WebAssembly. The reader is "you", a data
engineer. Markdown: `**bold**` for a button's name.

## Facts

1. Nothing on the page runs until you run it.
2. Run every cell first. The button for that is **Run all**, at the top of the page.
3. A cell does not run again when a cell it uses changes.
4. After you change a cell, select it and press **Run below**: it runs that cell and every cell
   below it.
5. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac).
6. After a reload, the page shows your saved copy.
7. Your saved copy stays in this browser, and it is shown instead of the chapter, even after the
   chapter is updated.

## Wording the tests hold

- Each button is named after the word "press", in bold: `press **Run all**`, `press **Run below**`,
  `press **Save**`.
- Fact 2 contains the exact words `press **Run all**, at the top of the page`.
- Do not use the words "menu", "menu bar", "toolbar" or "triangle".

## Slots

- **label**: a short label at the top of the box, two to four words, naming what the box is about
  (running and saving the page). Not a sentence. Not "How to" or "Getting started".
- **steps**: a numbered Markdown list of three steps, each one or two short sentences: running
  every cell first (facts 1 and 2), running again after a change (facts 3 and 4), and keeping your
  changes (facts 5, 6 and 7). Every fact appears once.
