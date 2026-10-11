# Brief AU: the two chapters on the front page

The author made the first notebook a chapter of its own. Chapter 1 is now "The shop and its
platform", a notebook only; Chapter 2 is "The invisible data system", the chapter's page as before,
and also a notebook. The front page lists every chapter by part, one line each: the chapter's
number and title, and under it a short note in small grey text. A written chapter's note says how
many of its challenges are complete, or "No challenges". Every fact below was checked on 11 October
2026.

Write each slot as plain words, following `docs/style.md` and the writing standard in `AGENTS.md`.
Write only the slots below, each under its key. Do not add facts. Do not mention a lab, an engine,
a simulator, Jupyter, JupyterLite, marimo, Pyodide or WebAssembly. Do not use the word "part": on
this page it names the course's eight parts. The reader is "you", a data engineer. British English.
No em dashes.

## Facts

- A notebook is a page where you run the chapter's Python code in your browser.
- The first time you open a notebook, the browser downloads about 13 MB.
- Chapter 1's line opens its notebook. Chapter 2's line opens the chapter's page; a second link,
  under Chapter 2's line, opens the same chapter as a notebook.

## Slots

- **notebook_note**: the small note under Chapter 1's line. Facts: the chapter is a notebook; you
  run its Python code in your browser; the first time, the browser downloads about 13 MB. One
  short sentence.
- **notebook_also**: the text of the second link under Chapter 2's line. Facts: it opens the same
  chapter as a notebook, where you run its Python code; the first time, about 13 MB. At most twelve
  words.
