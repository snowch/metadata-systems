# Brief AX: one notebook link per chapter, explained once

The front page lists the chapters by part. Each written chapter's line is its number and title,
which opens the chapter's page. The author asked to drop the long link under each line ("This
chapter as a notebook: run its Python in your browser. About 13 MB first time."). Instead, each
chapter that is also a notebook gets a short link at the right end of its line, and one sentence
under the heading "Contents" explains the notebooks once.

Write each slot following `docs/style.md` and `AGENTS.md`. British English. No em dashes. Do not
mention a lab, an engine, Jupyter, JupyterLite, Pyodide or WebAssembly. Do not use the word "part":
on this page it names the course's eight parts. The reader is "you", a data engineer.

## Facts

- A notebook is a page where you run the chapter's Python code in your browser.
- The first time you open a notebook, the browser downloads about 13 MB.
- The chapters that have one show the short link at the right of their line; Chapters 1 and 2 do.
- A chapter's title opens the chapter's page, which needs no download beyond the course.

## Slots

- **notebook_link**: the short link at the right of a chapter's line, which opens the chapter's
  notebook. One or two words.
- **notebooks_note**: one sentence under "Contents". Facts: a chapter with that link (give the
  link's words from notebook_link, in quotation marks) can also be opened as a notebook, where you
  run its Python code in your browser; the first time, the browser downloads about 13 MB.
