# Brief AT: links between the course and the chapter's notebooks

The author asked for the course and Chapter 1's two notebooks to link to each other. The course's
front page lists every chapter by part; Chapter 1's line links to the chapter's page, where the
whole chapter is on one page. Under that line, the page gains links to the two notebooks. Each
notebook gains a line at its top and its foot with links to the course's front page and to the
other notebook. Every fact below was checked on the built pages on 11 October 2026.

Write each slot as plain words, following `docs/style.md` and the writing standard in `AGENTS.md`.
Write only the slots below, each under its key. Do not add facts. Do not mention a lab, an engine,
a simulator, Jupyter, JupyterLite, marimo, Pyodide or WebAssembly. The reader is "you", a data
engineer. British English. No em dashes.

## Facts

- On the front page, the word "Part" already names the course's eight parts ("Part 1: Why metadata
  exists"). Do not use "part" in the front page's slot.
- The two notebooks hold the same chapter as the chapter's page, split in two. The first is titled
  "The shop and its platform"; the second "Thursday's revenue and what the platform cannot say".
  In a notebook you run the chapter's Python code in your browser. The first time, the browser
  downloads about 13 MB. Each link shows the notebook's title, and nothing else.
- Inside a notebook, the notebooks call themselves "part 1" and "part 2" ("Chapter 1, part 1: The
  shop and its platform"), and the course's parts are never mentioned.
- The course's front page is headed "Contents" where it lists the chapters.

## Slots

- **notebooks_lead**: on the front page, a short lead before the two notebook links, under
  Chapter 1's line. Facts: the same chapter, as two notebooks; you run its code in your browser;
  the first time, the browser downloads about 13 MB. One sentence, or a phrase ending in a colon.
- **nav_contents**: inside a notebook, the label of a link to the course's front page. At most
  three words.
