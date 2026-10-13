# Chapter 1 as a notebook: the prototype

The author asked whether the course could be delivered as notebooks that run in the browser, for
readers who are data engineers and think in notebooks, and then for a prototype of Chapter 1. This
note records what was built, why each choice was made, what was measured, and what is still open.
The prototype was published beside the course, under `/jupyterlite/`. On 11 October 2026 the
author made the notebooks the only version of each chapter (`docs/plan.md`, "11 October 2026: only
the notebooks"): the site's address is unchanged, and the course's front page links each chapter's
notebook. This note keeps the prototype's record as it was made.

The notebook was first built in marimo, then in JupyterLite to compare, and the author ruled marimo
out as too big for a phone ("marimo ruled out", at the end). The sections before that one record
the comparison as it was made; the two source files keep marimo's file format, and nothing of
marimo reaches a reader.

## What was built

- `notebook/chapter_01_part_1.py` and `chapter_01_part_2.py`: Chapter 1 as two marimo notebooks,
  one per part (one notebook, `chapter_01.py`, until the split under "The chapter in two parts",
  below). The
  prose is the chapter's approved essay, with part 1's tour of the shop added; the figures are drawn
  by the notebooks' own Python; the cells of code are visible, and the reader can change and run
  every one. The words new to the notebook were drafted by Haiku from briefs AK and AL
  (`docs/notes/chapter-02/briefs/round-15/`), and those of the two parts from AO and AP
  (`round-16/`).
- `notebook/shop/`: the shop's platform in Python, standard library only. Object storage holds
  real JSON Lines and CSV files in a temporary directory and records each file's key, size and
  last-modified time; the warehouse is SQLite, with a catalogue queryable as
  `information_schema.tables` and `.columns`; the reporting tool records the dashboard. Amounts are
  integer pence. It reproduces every number the course's engine (`packages/lab`) computes for the
  chapter.
- `notebook/tests/`: the engine's facts (`test_engine.py`) and every sentence and number the
  notebook states (`test_words.py`), with the course's prohibited phrases. `scripts/check.sh` runs
  them.
- `notebook/export.sh`: the export, which both workflows run. `marimo export html-wasm --mode edit
  --offline --execute` writes a static site: Python (Pyodide), every package and the notebook's own
  `shop` package are bundled into it, so the page fetches nothing from another site; the outputs are
  computed at export time and saved into the page. Both parts go into one site, part 1 as
  `index.html` and part 2 as `part-2.html`. Then `run_on_load.py` makes the cells run when the
  pages load, and `licences.py` checks the bundled packages' licences.
- `notebook/notebook.css`: three rules for marimo's editor, which the export inlines. A cell whose
  code is hidden shows only its output, without the faded first line of code marimo puts above it;
  on a screen narrower than 640 px, marimo's floating controls (which sat over the prose) and its
  side rail are hidden.
- `.github/workflows/notebook.yml` builds the export on every branch, prints the resolved packages
  and every file with its size into the log, and keeps the site as an artifact; `deploy.yml`
  builds it into the published site under `/notebook/` on main.

## Decisions

- **marimo, not Jupyter.** A marimo notebook is a Python file, so it diffs, lints and tests like
  code; its cells are reactive, so changing the day re-runs the cell that reads that day's row;
  and its export produces a static site with Python and the packages bundled. JupyterLite would
  serve the same purpose, with notebooks stored as JSON.
- **SQLite, not DuckDB; JSON Lines and CSV, not Parquet; integer pence.** SQLite is in Pyodide's
  standard library; DuckDB's package alone is about 9.8 MB compressed. JSON Lines and CSV are read
  with the standard library, and a reader can see the files as they are stored. Pence keep every
  sum exact. The course's TypeScript engine uses Parquet and decimal pounds; the notebook's model of
  the files differs from the course's, and its prose says what JSON Lines and CSV record.
- **Edit mode, not run mode.** marimo can export a notebook as an app (`--mode run`): outputs and
  controls, no code, about 0.39 GB of memory against about 1 GB (below). In run mode the reader
  cannot see or change the code, so the chapter's leads ("you can change it and run the cell
  again") would be false. The prototype is the notebook; run mode is the lighter option if the
  author wants pages a phone can hold more easily, with its own wording.
- **Cells run on load.** marimo's export embeds marimo's default configuration, in which a
  notebook does not run its cells when it opens: every cell shows the saved output, marked as
  needing a run, and the menu of changes and the handover note do nothing until the reader presses
  "run all". `run_on_load.py` sets `auto_instantiate` in the page, and fails if marimo moves it.

## Measurements

These are the chapter's as one notebook, before it was split; "The chapter in two parts", below,
has each part's. All on 10 October 2026, in Playwright's Chromium 141.0.7390.37 (build 1194),
headless, on this Linux container, from a local HTTP server: no network delay and no CPU
throttling. "Phone" is Chromium's phone emulation (390 by 844 pixels, touch); no real phone was
measured.

| | marimo, editable (`/notebook/`) | JupyterLite (`/jupyterlite/`) | marimo, read-only (not published) |
| --- | --- | --- | --- |
| Files one visit downloads | 255 | 149 | 232 |
| Size, as stored | 31.9 MB | 25.9 MB | 27.3 MB |
| Size if the host compresses text and WebAssembly (gzip, level 6) | 17.5 MB | 12.5 MB | 16.1 MB |
| First content drawn | 3.4 to 4.4 s | 2.5 to 2.7 s | 2.0 s |
| Python ready | 9.5 to 15 s | (starts with the page; not timed) | 8 to 9 s |
| Every code cell run once | 12 to 17 s, by itself | 12.9 to 13.2 s, when Run All Cells is pressed as the page draws | about 10 s, by itself |
| Run All Cells, from the press to the last output | (cells run on load) | 9.4 to 9.9 s | (cells run on load) |
| A change from the menu shown | 3.0 to 7.5 s | 0.1 s after Run Selected Cell and All Below; nothing before | 2.2 s |
| The edited day cell re-run | 0.3 to 0.5 s, and the cell that reads that day's row with it | its own output only: the next cell keeps the old day until it is run | (no code to edit) |
| Peak memory of the page's renderer process | 0.97 to 1.16 GB | 0.42 to 0.45 GB | 0.39 GB |
| Requests to another site | none | none | none |
| Console errors | 8 to 12, all "Language server initialization failed" | none | none |
| What a reload keeps | nothing | what was saved (File, Save Notebook), with its outputs; the note box returns when its cell runs, empty | nothing |

- The published page, measured after the deploy of `d3b11c6` from
  `https://snowch.github.io/metadata-systems/notebook/`, in the same Chromium, through this
  environment's network, at both widths: one visit makes 267 requests and transfers 17.1 MB, since
  GitHub Pages compresses what it sends, the WebAssembly and the wheels included (gzip); Python is
  ready after 15 to 16.5 s, the download included; every code cell has run by 19 to 20 s; a change
  from the menu shows in 3.8 to 5.2 s; no request goes to another site, and the page logs no error.
  marimo does not re-run the 29 markdown-only cells, whose saved output is their text: only the 25
  code cells run on load.
- The published JupyterLite page, measured after the deploy of `5157bb6` from
  `https://snowch.github.io/metadata-systems/jupyterlite/`, the same way: the 156 files a visit,
  a save and a reload fetched transfer 12.7 MB, GitHub Pages compressing the WebAssembly and the
  wheels as for marimo; the chapter's first text shows at 7.1 s; with Run All Cells pressed as the
  page draws, every cell has run at 19.4 s (11.4 s after the press); memory peaks at 437 MB; all
  480 requests go to snowch.github.io, and the page logs no error.
- The whole site is 47.3 MB in 527 files (CI's log, the export of commit 3682a04); most of
  marimo's scripts load only when a feature that needs them is used.
- Memory: the kernel's Python heap is 75 MB. Edit mode starts a second copy of Python to save the
  notebook (30 MB of WebAssembly memory), and its code editors and controls take the rest. For
  scale, a blank page measured 81 MB and Pyodide with SQLite running the shop's week 211 MB, in
  the same harness.
- On reload, everything the reader changed is lost: an edited cell, the handover note and the
  menu's choice. Ctrl+S saves nothing (the export turns autosave off), and the page reads the
  notebook embedded in it before anything a browser stored.
- The language server's errors come from marimo's editor timing out after 30 s; nothing on the page
  shows them. The page also logs that interrupts are not available: a running cell cannot be
  stopped, since GitHub Pages cannot send the headers that would allow it.

How it was measured: CI cannot hand the artifact over here (the artifact store and the log archive
are blocked by this environment's network policy, as is `wasm.marimo.app`, where marimo fetches its
package lockfile). So the export was rebuilt locally with marimo's own code and one change: a
lockfile assembled from Pyodide's published lockfile and the PyPI wheels CI's export resolved,
each checked by sha256. The rebuilt site matched CI's file for file and byte for byte, except the
lockfile, which differs only in two default fields. The scripts are session scratch, not part of
the repository.

## The JupyterLite version

Asked "why marimo, not JupyterLite?", the author asked for the same chapter in JupyterLite to compare.
It is `notebook/jupyterlite/`, published at `/jupyterlite/` beside the marimo notebook.

- `build_ipynb.py` builds the Jupyter notebooks from the marimo notebooks, cell by cell: the same
  prose and the same visible code. What Jupyter does differently is all it changes. The setup
  cells move to the top, since Jupyter runs from the top. marimo's controls become ipywidgets (the
  tabs, the menu of changes, the handover note), `mo.Html` becomes IPython's `HTML`, and the callout
  becomes a quoted paragraph. Four texts say what Jupyter does (`words.py`, Haiku's drafts of brief
  AN). Anything in the marimo notebook it cannot carry over stops the build.
- The first, hidden cell installs `shop`, ipywidgets and its `comm` from the site with piplite,
  without dependencies: ipywidgets declares its front-end package, which the kernel does not need,
  and the page turns off piplite's fall-back to PyPI.
- `fetch_pyodide.py` puts Pyodide 314.0.6's runtime and the 15 packages the kernel loads when it
  starts (micropip, IPython and jedi, with what they depend on) into the site, each wheel checked
  against Pyodide's lockfile. The list was found by building against the CDN and watching what the
  page fetched. The kernel then loads nothing from another site.
- The page is JupyterLite's Notebook interface (Jupyter Notebook 7.6.3 on JupyterLab 4.6.4): a menu
  bar, a toolbar, numbered cells; a hidden cell shows its first line and "•••". The site's root
  opens the file list, which holds the chapter.
- The page ships without saved outputs. JupyterLite opens a notebook as untrusted, and an untrusted
  notebook's saved HTML is shown with its styles stripped and its widgets as text: every figure
  read as a run of words until the notebook ran. Signing it with `jupyter trust` does not help,
  since the signature is kept in the signing machine's database, not in the file. The build still
  runs the notebook once in CPython, and stops if a cell raises.
- Nothing runs until the reader runs it, and a cell does not run again when a cell it uses
  changes: after editing the day, the next cell keeps showing the old day's row until it is run;
  after choosing a change, the cells below show the old week until they are run. The page's texts
  say so.
- A saved notebook survives a reload, in the browser's storage, and, as JupyterLite's
  documentation says, a reader's saved copy is shown instead of the published one even after the
  chapter is updated.

## The chapter in two parts

Having read the notebooks, the author asked for the chapter in two parts: the first to get the
reader used to the shop and its processes, the second to start on the issues. Both notebook
versions are split. The course's essay page is not: the course numbers its chapters, so the same
split there needs a decision (the last open question, below).

- `chapter_01_part_1.py`, "Chapter 1, part 1: The shop and its platform": the situation and the
  head of the shop's message, "Thursday's revenue looks wrong", as the chapter has always opened,
  and why the reader looks round first: to tell whether Thursday's figure is wrong, they need to know
  what the platform holds and what happens on it each night. Then the three systems, the seven
  assets and the week, as before, and a section for each thing the shop keeps, each with a cell that
  reads it: `products.csv` and `customers.jsonl` printed as they are stored, one day's orders from
  `orders.jsonl` (Monday, and the reader can change the day), the warehouse's three tables, and the
  dashboard. It ends with a link to part 2, which starts on Thursday. 12 code cells and 14 of prose.
- At first the message closed part 1, and part 1 was a tour with no question in front of it, which
  `CLAUDE.md` warns against: data shown without a question to answer from it. The author agreed that
  separating the shop from the issues is right and asked for the story to be introduced differently:
  the message opens part 1 again, so the tour serves the question, and part 2 still holds the
  investigation (brief AQ).
- `chapter_01_part_2.py`, "Chapter 1, part 2: Thursday's revenue and what the platform cannot say":
  the essay from its questions to the handover. It opens with the message, the systems' figure and
  the dashboard; the paragraph on what JSON Lines and CSV record moved to part 1, where the reader
  first opens the files; nothing else changed. 23 code cells and 26 of prose.
- Part 1 is written so as not to answer part 2. It says what each file and table holds, never which
  is made from which. It reads the files and tables, not what the systems record about them (sizes,
  times, owners), which part 2's "What the platform holds" is about. It counts nothing that shows
  Thursday's gap or the order the export writes twice. It describes the records by their fields,
  since one customer has no email address and three of Thursday's orders have no customer.
- "The shop's processes" are those the reader can see: orders as the checkout records them, with
  their statuses; the catalogue; the customers; and the night's work as the week's figure shows it
  (the files written again, then the tables, then the dashboard). The programs stay unseen, as the
  chapter requires.
- The new words are Haiku's drafts of briefs AO and AP (`docs/notes/chapter-02/briefs/round-16/`),
  checked for facts only. AO's first draft copied two wrong facts from the brief itself (that every
  customer has an email address, and every order a customer) and gave titles without each part's
  subject; AP's first draft stated a measurement made on a computer as a rule for every browser.
  Each went back with a note. Part 1's section heading "The shop and its platform" was cut, as a
  repeat of its title.
- The marimo export writes both pages into one site: part 1 is `index.html`, so `/notebook/` still
  opens the chapter, and part 2 is `part-2.html`. marimo's offline bundle files each package under
  its hash and names the lockfile after its contents, so the two pages share one copy of Python, of
  every package and of `shop`'s wheel: the site is 47.4 MB in 528 files, one file more than before.
- The JupyterLite site holds `chapter_01_part_1.ipynb` and `chapter_01_part_2.ipynb`, and its root's
  file list shows both. Each part links to the other by the other's name. Jupyter Notebook opens a
  link to a notebook in a new tab, so a reader who follows part 1's link has two tabs, each with its
  own Python; part 2's warning says that part 1 stays open. Part 2 starts with the first two
  sentences of part 1's text on running cells, since nothing on it shows until it runs.

Measured on 10 October 2026 as above, but in a browser profile kept on disk, as a reader's browser
has: Playwright's default profile keeps its cache in memory, did not keep Python's 9.6 MB
WebAssembly file, and fetched it again for each of the page's two Pythons and again for part 2, 19.2
MB a profile on disk serves from its cache. Each range is over runs at both widths.

| | marimo, part 1 (`/notebook/`) | marimo, part 2 opened alone | marimo, part 2 from part 1's link |
| --- | --- | --- | --- |
| Files the visit downloads | 255 | 255 | 1, `part-2.html` |
| Size, as stored | 31.8 MB | 31.9 MB | 0.15 MB |
| Size if the host compresses text and WebAssembly (gzip, level 6) | 17.0 MB | 17.0 MB | |
| First content drawn | 1.9 to 2.3 s | 2.3 to 2.5 s | 1.4 to 1.7 s |
| Python ready | 8.9 to 10.3 s | 8.9 to 9.3 s | 7.7 to 8.7 s |
| Every code cell run once, by itself | 12.2 to 13.7 s | 13.7 to 14.7 s | 12.5 to 14.8 s |
| Peak memory of the page's renderer process | 0.79 to 0.82 GB | 1.01 to 1.09 GB | 1.03 to 1.05 GB, part 1 having run in the same process |
| Requests to another site | none | none | none |
| Console errors in the first 50 s | 53, all "Language server initialization failed", from 30 s on | 74, the same | |

| | JupyterLite, part 1 | JupyterLite, part 2 opened alone | JupyterLite, part 2 from part 1's link (a new tab) |
| --- | --- | --- | --- |
| Files the visit downloads | 147 | 149 | 11 |
| Size, as stored | 25.7 MB | 25.9 MB | 0.32 MB |
| Size if the host compresses text and WebAssembly (gzip, level 6) | 12.45 MB | 12.49 MB | |
| First content drawn | 2.6 to 2.9 s | 2.8 to 2.9 s | |
| Run All Cells, from the press to the last output | 9.7 to 10.5 s | 10.1 to 11.1 s | |
| Peak memory of the page's renderer process | 391 to 414 MB | 404 to 429 MB | |
| Requests to another site | none | none | none |
| Console errors in the first 50 s | none | none | |

- The published pages, measured after the deploy of `0e2cef9` from `snowch.github.io`, the same
  way, through this environment's network. marimo: part 1 sends 17.04 MB in 267 requests, as
  Playwright counts what each response sent; Python is ready at 14.0 to 15.0 s and every code cell
  has run at 18.2 to 19.4 s; memory peaks at 0.80 GB. Part 2 from part 1's link sends 0.03 MB, is
  ready at 7.9 to 10.1 s and has run every cell at 13.0 to 13.8 s; opened alone it sends 17.0 MB,
  is ready at 14.9 s and peaks at 0.93 GB. JupyterLite: Playwright cannot see the size of what the
  page's service worker fetches, so each file a visit requested was fetched again as a browser asks
  for it, compressed: part 1's 147 files arrive as 12.56 MB and part 2's 149 as 12.60 MB. The first
  text shows at 5.9 to 7.2 s, Run All Cells took 11.9 to 12.1 s from the press to the last output,
  memory peaks at 396 to 438 MB, and part 1's link opens part 2 in a new tab. No page requested
  anything from another site or logged an error while measured.
- Each page's warning (brief AP) states these: about 17 MB the first time; Python ready in 9 to 17 s
  on part 1 and 8 to 17 s on part 2, where the top of each range is the published single notebook's
  15 to 16.5 s; about 0.8 GB and about 1 GB; about 13 MB; 10 to 12 s to run every cell, the local
  and the published pages' range (the drafts said "about 10" and "10 to 11" seconds, measured
  locally, and the numbers were corrected once the published pages took 12 s); about 400 MB and
  about 420 MB; and for part 2, less than 1 MB from part 1's link.
- Part 1 needs less memory than the single notebook did (0.79 to 0.82 GB against 0.97 to 1.16 GB
  in marimo, 391 to 414 MB against 0.42 to 0.45 GB in JupyterLite); part 2 about as much.

## Chapters 3 and 4

Measured 12 October 2026 on the built site served locally (`python3 -m http.server`-like, logging
each response's bytes), in Chromium with a profile kept on disk, by pressing **Run all** in the row
of buttons and waiting until no cell waits to run. "From the link" opens the chapter before, runs
it, then follows its "Next" link.

| | Chapter 3 | Chapter 4 |
| --- | --- | --- |
| Opened alone: files, as stored | 151 files, 25.79 MB | 151 files, 25.78 MB |
| Opened from the chapter before's link, after it ran | 11 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 8.9 to 9.6 s | 8.9 to 10.5 s |
| Peak memory of a renderer process, opened alone | 400 to 418 MB | 400 to 406 MB |
| Peak memory, with the chapter before open in its own tab | 630 to 639 MB | 624 to 626 MB |
| Cells with an error output; console errors | none | none |

The files a chapter downloads opened alone are the same as Chapter 2's, so the compressed size is
the 12.5 MB measured for it above. Each chapter's warning (brief CD) states: about 13 MB the first
time on its own; less than 1 MB from the chapter before's link; 9 to 12 seconds to run every cell;
about 420 MB (Chapter 3) and about 410 MB (Chapter 4). The published pages, measured the same way
after the deploy of `2690b76` from `snowch.github.io`, opened alone on a computer: Run all took
11.8 s (Chapter 3) and 11.4 s (Chapter 4), with memory peaking at 421 MB and 408 MB. The warnings
said "9 to 11 seconds" until then, from the local build alone; they now say "9 to 12 seconds".

## Chapters 5 and 6

Measured 12 October 2026 as Chapters 3 and 4 were, on the built site served locally.

| | Chapter 5 | Chapter 6 |
| --- | --- | --- |
| Opened from the chapter before's link, after it ran | 11 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 8.3 to 8.7 s | 8.0 to 9.3 s |
| Peak memory of a renderer process, opened alone | 397 to 403 MB | 398 to 418 MB |
| Peak memory, with the chapter before open in its own tab | 615 MB | 625 MB |
| Cells with an error output; console errors | none | none |

Opened alone, each downloads the files Chapter 2 does (about 12.5 MB compressed). Each warning
(brief GA) states: about 13 MB on its own; less than 1 MB from the chapter before's link; 9 to 12
seconds to run every cell, the published Chapters 3 and 4 having taken up to 11.8 s; about 400 MB
(Chapter 5) and about 420 MB (Chapter 6).

## Chapters 7, 8 and 9

Measured 12 October 2026 as Chapters 5 and 6 were, on the built site served locally. Each segment of
the server's log from a chapter's link was cut where the next measurement began.

| | Chapter 7 | Chapter 8 | Chapter 9 |
| --- | --- | --- | --- |
| Opened from the chapter before's link, after it ran | 19 files, 0.29 MB, in a new tab | 17 files, 0.29 MB, in a new tab | 11 files, 0.29 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 8.0 to 9.3 s | 8.9 to 9.3 s | 8.3 to 9.0 s |
| Peak memory of a renderer process, opened alone | 397 to 421 MB | 396 to 405 MB | 403 to 411 MB |
| Peak memory, with the chapter before open in its own tab | 630 MB | 622 MB | 618 MB |
| Cells with an error output; console errors | none | none | none |

Each warning states: about 13 MB on its own; less than 1 MB from the chapter before's link; 9 to 12
seconds to run every cell, as the published Chapters 3 to 6 took up to 12 s; about 420 MB (Chapter
7), about 400 MB (Chapter 8) and about 410 MB (Chapter 9).

## Chapters 10 to 13

Measured 12 October 2026 as Chapters 7 to 9 were, on the built site served locally, before the
outside review. Each segment of the server's log from a chapter's link was cut where the next
measurement began.

| | Chapter 10 | Chapter 11 | Chapter 12 | Chapter 13 |
| --- | --- | --- | --- | --- |
| Opened from the chapter before's link, after it ran | 14 files, 0.32 MB, in a new tab | 15 files, 0.32 MB, in a new tab | 14 files, 0.32 MB, in a new tab | 15 files, 0.32 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 8.3 to 8.5 s | 7.8 to 8.9 s | 7.6 to 7.7 s | 8.1 to 9.3 s |
| Peak memory of a renderer process, opened alone | 395 to 403 MB | 395 to 402 MB | 395 to 402 MB | 397 to 403 MB |
| Peak memory, with the chapter before open in its own tab | 622 MB | 621 MB | 611 MB | 616 MB |
| Cells with an error output; console errors | none | none | none | none |

Each warning states: about 13 MB on its own; less than 1 MB from the chapter before's link; 9 to 12
seconds to run every cell, as the published Chapters 7 to 9 took up to 11 s; about 400 MB.

## Chapters 14 to 17

Measured 12 October 2026 as Chapters 10 to 13 were, on the built site served locally, before the
outside review. The row of buttons now carries the arrows, so the link followed is the chapter text's
own "Next" link, as before. The one console error in each link measurement is the measuring script's
own request that marks the server's log, which the server answers with 404.

| | Chapter 14 | Chapter 15 | Chapter 16 | Chapter 17 |
| --- | --- | --- | --- | --- |
| Opened from the chapter before's link, after it ran | 11 files, 0.32 MB, in a new tab | 12 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 8.3 to 8.9 s | 8.4 to 9.0 s | 8.2 to 9.5 s | 7.9 to 8.9 s |
| Peak memory of a renderer process, opened alone | 395 to 402 MB | 394 to 400 MB | 394 to 402 MB | 392 to 397 MB |
| Peak memory, with the chapter before open in its own tab | 619 MB | 614 MB | 612 MB | 605 MB |
| Cells with an error output; console errors from the page | none | none | none | none |

Each warning states what Chapters 10 to 13 state: about 13 MB on its own; less than 1 MB from the
chapter before's link; 9 to 12 seconds to run every cell, as the published Chapters 10 to 13 took
9.8 to 11.6 s; about 400 MB.

Published at `32be44b` and measured live the same day, each opened alone at desktop and phone
widths: ready to run in 5.4 to 7.1 s; Run all 10.0 to 11.2 s (Chapter 14), 10.6 to 11.2 s (15),
10.2 to 10.6 s (16), 10.2 to 11.0 s (17); peak memory 397 to 404 MB; no error output and no console
error. One desktop run of Chapter 15 stopped its clock at 0.6 s with 346 MB, before Run all had
started its cells; two more runs took 11.0 and 11.2 s, and the 0.6 s is left out. The warning's 9
to 12 seconds and about 400 MB hold.

## Chapters 18 to 23

Measured 12 October 2026 as Chapters 14 to 17 were, on the built site served locally, before the
outside review's changes, which add a few small cells to Chapters 18 to 21 and 23. The link
followed is the chapter text's own "Next" link.

| | Chapter 18 | Chapter 19 | Chapter 20 | Chapter 21 | Chapter 22 | Chapter 23 |
| --- | --- | --- | --- | --- | --- | --- |
| Opened from the chapter before's link, after it ran | 11 files, 0.32 MB, in a new tab | 11 files, 0.31 MB, in a new tab | 11 files, 0.31 MB, in a new tab | 11 files, 0.31 MB, in a new tab | 11 files, 0.31 MB, in a new tab | 11 files, 0.31 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 7.8 to 8.5 s | 7.6 to 8.5 s | 8.2 to 8.5 s | 7.8 to 8.0 s | 7.8 to 8.7 s | 8.1 to 8.3 s |
| Peak memory of a renderer process, opened alone | 395 to 402 MB | 393 to 402 MB | 392 to 395 MB | 390 to 397 MB | 388 to 394 MB | 395 to 398 MB |
| Peak memory, with the chapter before open in its own tab | 611 MB | 608 MB | 608 MB | 608 MB | 608 MB | 608 MB |
| Cells with an error output; console errors from the page | none | none | none | none | none | none |

Each warning states what Chapters 14 to 17 state: about 13 MB on its own; less than 1 MB from the
chapter before's link; 9 to 12 seconds to run every cell, as the published Chapters 14 to 17 took
10.0 to 11.2 s while the same pages took 7.9 to 9.5 s here; about 400 MB. The live measurement after
publishing is the check on the 9 to 12 seconds.

Published at `b15b63a`, after the review's changes, and measured live the same day, each opened alone
at desktop and phone widths: ready to run in 5.2 to 6.1 s; Run all 10.2 to 10.4 s (Chapter 18), 10.4
to 11.2 s (19), 9.8 to 10.0 s (20), 9.4 to 9.6 s (21), 9.2 to 9.4 s (22), 9.8 s (23); peak memory 389
to 411 MB; no error output and no console error. The warning's 9 to 12 seconds and about 400 MB hold.

## Chapters 24 to 28

Measured 13 October 2026 as Chapters 18 to 23 were, on the built site served locally, after the
outside review's changes. The link followed is the chapter text's own "Next" link.

| | Chapter 24 | Chapter 25 | Chapter 26 | Chapter 27 | Chapter 28 |
| --- | --- | --- | --- | --- | --- |
| Opened from the chapter before's link, after it ran | 11 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab | 11 files, 0.31 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 8.2 to 9.1 s | 8.0 to 8.8 s | 8.1 to 8.5 s | 8.3 to 8.6 s | 8.6 to 9.0 s |
| Peak memory of a renderer process, opened alone | 396 to 403 MB | 389 to 402 MB | 394 to 400 MB | 391 to 404 MB | 393 to 397 MB |
| Peak memory, with the chapter before open in its own tab | 615 MB | 612 MB | 611 MB | 615 MB | 615 MB |
| Cells with an error output; console errors from the page | none | none | none | none | none |

Each warning states what Chapters 18 to 23 state: about 13 MB on its own; less than 1 MB from the
chapter before's link; 9 to 12 seconds to run every cell, as the published Chapters 18 to 23 took 9.2
to 11.2 s while the same pages took 7.6 to 8.7 s here; about 400 MB. The live measurement after
publishing is the check on the 9 to 12 seconds.

Published at `f0fa7d7` and measured live the same day, each opened alone at desktop and phone widths:
ready to run in 5.3 to 6.5 s; Run all 10.0 to 11.4 s (Chapter 24), 10.2 to 10.8 s (25), 10.2 to 11.0 s
(26), 10.2 s (27), 10.8 to 11.8 s (28); peak memory 394 to 412 MB; no error output and no console
error. A first try at Chapter 24 on the phone stopped at 180 s waiting for the page to load, and one
at Chapter 28 on desktop recorded a Run all of 0.6 s; both, tried twice more, gave the figures above.
The warning's 9 to 12 seconds and about 400 MB hold.

## Chapters 29 to 32

Measured 13 October 2026 as Chapters 24 to 28 were, on the built site served locally, after the
outside review's changes. The link followed is the chapter text's own "Next" link.

| | Chapter 29 | Chapter 30 | Chapter 31 | Chapter 32 |
| --- | --- | --- | --- | --- |
| Opened from the chapter before's link, after it ran | 11 files, 0.32 MB, in a new tab | 11 files, 0.32 MB, in a new tab | 11 files, 0.31 MB, in a new tab | 11 files, 0.31 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 8.9 to 9.5 s | 8.4 to 9.5 s | 8.4 to 8.5 s | 8.5 to 9.1 s |
| Peak memory of a renderer process, opened alone | 391 to 399 MB | 394 to 399 MB | 398 MB | 392 to 398 MB |
| Peak memory, with the chapter before open in its own tab | 609 MB | 614 MB | 608 MB | 617 MB |
| Cells with an error output; console errors from the page | none | none | none | none |

Each warning states what Chapters 24 to 28 state. Live, 13 October 2026, published at `c12c414`,
opened alone at desktop and phone widths: Run all 10.0 to 11.4 s, peak memory 396 to 406 MB, no
error output, no console error; one desktop run of Chapter 31 timed 0.6 s, as Chapter 28's once did,
and measured again took 11.2 s. The warnings' 9 to 12 seconds and about 400 MB hold.

## Chapter 33

Measured 13 October 2026 as Chapters 29 to 32 were, on the built site served locally, after the
outside review's changes. The link followed is Chapter 32's "Next" link.

| | Chapter 33 |
| --- | --- |
| Opened from the chapter before's link, after it ran | 11 files, 0.33 MB, in a new tab |
| Run all, from the press until no cell waits (desktop, phone, from the link) | 9.9 to 10.3 s |
| Peak memory of a renderer process, opened alone | 407 to 414 MB |
| Peak memory, with the chapter before open in its own tab | 627 MB |
| Cells with an error output; console errors from the page | none |

The ferry runs in the page beside the shop's package, and the chapter holds more cells than any
other. Live, 13 October 2026, published at `cd06d1f`, opened alone at desktop and phone widths: Run
all 11.5 to 11.8 s, peak memory 417 to 424 MB, no error output, no console error. Its warning says
about 420 MB, from the live peak, where Chapters 18 to 32 say about 400; the 9 to 12 seconds hold.

## Phones

Nothing here measured a real phone, so the page says only what was measured and what one report
shows: in Safari, a page that uses a lot of memory can be reloaded by the browser, with the
message "This webpage was reloaded because it was using significant memory" (a developer's report
on Apple's developer forums, `docs/sources.md`). A reload loses what the reader changed, as
measured above. The warning at the top of the notebook says so (brief AL).

## marimo ruled out

On 10 October 2026 the author ruled marimo out: it is too big for a phone. Measured on a computer,
marimo's pages peaked at 0.79 to 1.09 GB of memory and JupyterLite's at 391 to 429 MB, for the same
two parts ("The chapter in two parts").

- Removed: the marimo export (`export.sh`, `run_on_load.py`, `notebook.css`, and `pyproject.toml`,
  which held only marimo's settings), its job in `notebook.yml` and its step in `deploy.yml`. marimo
  is no longer installed or run anywhere; the tests run in `notebook.yml`'s JupyterLite job.
- `/notebook/` and `/notebook/part-2.html`, the marimo pages' addresses, are now two small pages
  (`notebook/redirect/`) that send a browser to the same parts in JupyterLite, so earlier links
  still arrive.
- The chapter's two source files stay as they are: Python files of cells in marimo's file format,
  which `build_ipynb.py` turns into the Jupyter notebooks and the tests read sentence by sentence.
  marimo's controls in them (`mo.ui.dropdown`, `mo.ui.text_area`, `mo.callout`) are only the
  notation the build converts. The Jupyter versions of the sentences that said how to run a cell,
  which `words.py` used to put in place of marimo's, are now in the source files themselves, and
  `words.py` is gone. A link from one part to the other names the other notebook.

### The menus on a phone

Asked about menus that do not work on a phone, the menus were tapped in Chromium's phone emulation,
with touch events, at 390 by 844 pixels, on the published JupyterLite page. Every menu at the top of
the page opens when tapped, but tapping an item does nothing: Run, then Run All Cells, ran no cell
in 15 s. A mouse click on the same item works. The Run menu is also wider than the screen (429
pixels on a 390-pixel screen). The toolbar's buttons respond to a tap: "Restart the kernel and run
all cells" asked to restart, and on Restart ran every cell. No real phone was tested.

- `notebook/jupyterlite/overrides.json`, which the build reads from the lite folder (JupyterLite's
  documentation, `docs/sources.md`), adds two labelled buttons to the notebook's toolbar: "Run all"
  (`notebook:run-all-cells`) and "Run below" (`notebook:run-all-below`). JupyterLab's toolbar
  settings take a button's command, label, icon, caption and rank, not its size.
- The texts that told the reader to use the menus now use the toolbar: Run all, the run button (a
  triangle), Run below and the save button (a disk), with the keyboard's Shift+Enter and Ctrl+S
  beside them (Haiku's drafts of brief AR; the Thursday row's lead went back once, because "this
  cell" pointed at the paragraph instead of the cell below it).
- Checked on the built site, by touch at 390 pixels and by mouse at 1280: Run all ran part 1 in 7.6
  s and part 2 in 7.8 to 8.0 s; part 1's link opened part 2 in a new tab; after the day was changed
  to Friday and Run below pressed with that cell selected, the next cell showed Friday's row; after
  a change was chosen and Run below pressed on the first cell under the menu, the cells below showed
  the failed night; the save button kept an edit through a reload; no page logged an error.
- The two buttons are 45 by 21 and 68 by 21 pixels, and the toolbar's own 21 by 21: smaller than
  the 40 pixels the course asks of a control on a phone. Published on 10 October 2026 (414a013),
  and checked live by touch and by mouse the same way; the next change replaced the two buttons.

### A row of large buttons

Asked whether the page could have custom buttons, the site gained a JupyterLab extension of its own,
`notebook/buttons/`: a row of three buttons above every notebook's cells, Run all, Run below and
Save, each 44 pixels tall, in JupyterLab's colours, so the row follows its light and dark themes.
The two labelled toolbar buttons and `overrides.json` are gone, and the texts name the row (Haiku's
draft of brief AS; the brief left out the run button, a triangle, since Run below does what the
texts need).
The author did not choose to have the notebook run itself on opening, so it does not.

- JupyterLab 4.6 builds extensions with `@jupyter/builder`, not the older `@jupyterlab/builder`
  (the `jupyterlab` 4.6.4 package's `staging/package.json`). `build.sh` installs it from
  `notebook/buttons/package-lock.json` and builds the extension into `notebook/buttons/labextension/`,
  which the JupyterLite build copies into the site (`LiteBuildConfig.federated_extensions`). The
  extension takes JupyterLab's own modules from the page; what it adds to the site is 18 KB.
- JupyterLab's Run All and Run All Below select the last cell and scroll to it: after Run all at
  the top of part 1, by touch at 390 pixels, the notebook stood at 5,807 of its 6,685 pixels. The
  row's buttons run the same cells with JupyterLab's `NotebookActions.runCells`, which keeps the
  selected cell, and Run all first selects a cell that starts in view, since JupyterLab scrolls to
  the selected cell after a run only when less than 28 pixels of it shows (`docs/sources.md`).
- Checked on the built site, by touch at 390 pixels and by mouse at 1280, both parts as the texts
  say: Run all from 600 pixels down left the notebook at 600, and ran part 1 in 8.5 to 8.8 s and
  part 2 in 9.3 to 9.4 s; after the day was changed to Friday and Run below pressed with that cell
  selected, the notebook did not move and the next cell, in view, showed Friday's row; after a
  change was chosen and Run below pressed on the first cell under the menu, the notebook did not
  move and the cells below showed the failed night; Save kept an edit through a reload; no page
  logged an error. The row was also screenshot in the dark theme, at both widths.
- `notebook/jupyterlite/smoke.mjs` does the same by touch in the notebook workflow, on every
  branch: the row's labels and heights, Run all in both parts with every visible code cell run and
  no error output, Run below in part 2, and the notebook left where it was scrolled. It failed, as
  it should, on a copy of the site without the extension; a cell that raises shows as the error
  output it counts.

### Arrows to the chapters either side

Asked whether the row should carry links to the other chapters, the author agreed to two arrows at
its right end, to the chapter before and the chapter after. The row stays in view while the cells
scroll; the links the chapter's text gives are at its top and its end, and a Part III chapter is
long.

- The extension finds the chapters among the site's files, the notebooks named `chapter_NN.ipynb`,
  so a chapter added to the site gains its arrows, and the chapter before it its Next arrow, with
  no list to keep. Chapter 1 has no Previous arrow, and the last chapter no Next.
- Each arrow is a link, `index.html?path=chapter_NN.ipynb`, that opens in a new tab, as the text's
  links do, so each chapter's warning, which says the link from the chapter before opens it in a new
  tab, and the memory measured with that chapter open, still hold. Each arrow's accessible name and
  tooltip are the text's links' own words, "Previous: Chapter 12" and "Next: Chapter 14".
- Width. With the three buttons as they were, at 360 pixels the row was 24 pixels too wide for two
  arrows with their chapters' numbers. Below 430 pixels the arrows show without their numbers, 40
  pixels wide and 44 tall, the buttons' side padding is 10 pixels and the gaps 4. A first try, with
  12 and 6 and arrows 44 wide, fitted in Inter, this machine's interface typeface, with 8 pixels to
  spare, and failed in CI, whose runner draws the interface in a wider one: in DejaVu Sans the row
  took 361 pixels. Now it takes 333 in DejaVu Sans and 323 in Inter. Above 430 pixels each arrow
  shows its chapter's number.
- Checked on the built site, by touch at 360 and 390 pixels, in the light and dark themes, and by
  mouse at 1280: Chapters 1, 7, 12 and 13 show the arrows they should; the row did not scroll;
  every arrow was 44 pixels tall; Chapter 13's Previous arrow opened Chapter 12 in a new tab, and
  Chapter 13 stayed open. `smoke.mjs` checks each chapter's arrows, their height and their new tab,
  that the row fits 360 pixels, and that Chapter 1's Next arrow opens Chapter 2.

### A link to the contents between the arrows

The author asked for a button to the contents between the arrows, and agreed to one on wider
screens only, opening in a new tab.

- It is a link like the arrows, 44 pixels tall, to the course's front page, which opens in a new
  tab so that the reader's notebook stays open. Its text is "Contents"; its accessible name and
  tooltip are the text's own link's words, "Back to contents". The front page is two folders above
  the notebook's page (`jupyterlite/notebooks/index.html` beside the course, the deploy workflow),
  so the link is relative and leads to the front page wherever the site is served. Chapter 1 has it
  before its Next arrow, the last chapter after its Previous arrow.
- Width. It shows from 600 pixels. At 430 pixels, the first width tried, the three buttons, both
  arrows with their numbers and the link took about 490 pixels in Inter, and the Next arrow was cut
  off. On a phone the text's own link to the contents, at its top and its end, is the way back.
- The rule that pushed the arrows to the row's right end was "a link straight after a button"; with
  the contents link hidden, Chapter 1's Next arrow would have sat beside Save. The last button now
  takes the free space after it instead, whichever links follow.
- Checked on the built site at 360, 430, 599, 600 and 1280 pixels, light and dark: the link shows
  from 600, between the arrows, and the row does not scroll. `smoke.mjs` checks every chapter at
  600 pixels (the link's name, text, address, new tab, height and place, and that the row fits) and
  at 360 (that it does not show).
- Later the same day the author, on a phone about 410 pixels wide, saw room for it between the
  arrows. It now shows from 390 pixels as an icon, a list's three lines drawn in the text's colour,
  40 pixels wide, with the same name and tooltip, and its word from 600. Below 500 pixels the row
  takes its phone form (arrows without numbers, closer together): 324 pixels, 368 with the icon
  (333 and 377 in DejaVu Sans). From 500 the arrows show their numbers again, 440 with the icon; from
  600, 478 with the word. So the arrows lost their numbers between 430 and 499 pixels, where they
  had them, so that the icon fits. 360-pixel phones still have no room for it; 375-pixel ones would
  in Inter but not in DejaVu Sans, so the line is at 390. Checked at 360, 390, 412 (dark), 499, 500
  and 600 pixels; `smoke.mjs` checks every chapter at 390, 500 and 600 (icon or word, place, address,
  new tab, height, and that the row fits) and at 360.

### The menu bar and the toolbar hidden

After the row was published, the author reported that the buttons did not seem to work, and asked
for the menu bar and the toolbar to be hidden. The failure did not reproduce in Chromium's phone
emulation, where every press ran; no real phone was available to test. Two changes followed:

- The extension hides the menu bar (`app.shell.menu`, as Jupyter Notebook's zen mode does) and the
  notebook's toolbar, so the row is the only control at the top of the page; on a phone it is the
  first thing on the page.
- With the toolbar went the only sign that Python was busy, and the first press on a phone waits
  for Python to start. While a press's work is under way, the row's buttons are disabled and the
  pressed one shows a spinner after its label (still with reduced motion). A press by touch is now
  left to the browser; only a mouse press keeps the focus in the notebook, as before.
- Checked on the built site, by touch at 390 pixels and by mouse at 1280: the menu bar and the
  toolbar are hidden; Run all showed its spinner for 7.3 to 8.3 s on part 1; every run of both
  parts left the notebook where it was, with the results as before; Save kept an edit through a
  reload; no page logged an error. `smoke.mjs` now checks the hidden bars and the busy row too.

### Links between the course and the notebooks

Asked what the course's navigation should be, the author agreed to make the front page the hub.
Under Chapter 1's line, the front page lists the two notebooks by title (not as "part 1" and "part
2": on that page "Part" names the course's eight parts), after a lead that says they are the same
chapter with code you run, and the first download (brief AT; `content/lessons/notebooks.ts`). Each
notebook opens and ends with "Back to contents · Part 1 · Part 2", the current part unlinked.

- A relative link in a notebook opens as a file of the JupyterLite site (`../../index.html` became
  `files/index.html`, and `/index.html` the file browser), so the link back to the course is its
  whole address, https://snowch.github.io/metadata-systems/, and opens in a new tab, as the
  links between the parts do. A build served anywhere else still links to the published course.
- Checked: on the built course, at 390 and 1280 pixels, the two links lead to the notebooks under
  the base path and are 44 to 54 pixels tall, with no sideways scroll; in the built notebooks, by
  touch at 390 pixels, "Back to contents" opened the course, and both parts ran as before. The
  course's Playwright suite checks the links, and a content test each title against its
  notebook's heading.
- The front page's start button still opens the chapter's page, which keeps the whole chapter.

### Two chapters

On 11 October 2026 the two parts became Chapters 1 and 2 (`docs/plan.md`, "two chapters where
there was one"). The source files are now `notebook/chapter_01.py` and `chapter_02.py`, built as
`chapter_01.ipynb` and `chapter_02.ipynb`; their headings are "Chapter 1: The shop and its
platform" and "Chapter 2: The invisible data system", the plan's titles; each opens and ends with
"Back to contents" and a link to the other chapter, "Next: Chapter 2" or "Previous: Chapter 1". In
the texts, "part 1" and "part 2" became "Chapter 1" and "Chapter 2", the same sentences otherwise.
The earlier notebook addresses (`?path=chapter_01_part_1.ipynb`) no longer open a notebook, and a
copy a reader saved under the old name stays in their browser under it; `/notebook/` and
`/notebook/part-2.html` send a browser to the new ones. The measurements above were taken when the
notebooks were parts, and their names in this note are the names they had then.

## Open questions for the author

- Whether the notebook should replace the essay pages, sit beside them, or be dropped: answered
  on 11 October 2026, when the notebooks replaced the pages.
- Whether the notebook should run every cell as soon as it opens, as the marimo version did. The
  row's extension could do it; the page would then do the 10 to 12 seconds of work on opening, and
  the texts would change.
- In a notebook the reader meets code. The visible cells use the shop's three systems (`storage`,
  `warehouse`, `reporting`) and three helpers of the chapter (`shop.run_week`,
  `shop.queries_that_rebuild`, `shop.cleaning_rules_that_fit`); the code that draws the figures
  is in hidden cells. "No lab on the page" (`CLAUDE.md`) holds for the words; whether it should hold
  for the code is the author's call.

## Chapter 2 on an emulated slow phone, 13 October 2026

The author asked for the chapter to be tried on a modest device: a fresh opening, Run all, the next
chapter's arrow, and a reload. No real phone is to hand, so a computer was set to run like one: the
browser in a CPU cgroup held to a third of one core (`cpu.cfs_quota_us` 33000 of 100000), as a
390-pixel touch screen, against the built site served with gzip through a server that holds every
request to one shared bandwidth and adds a fixed latency. DevTools' own throttling was tried first
and set aside: it slows the page's main thread and its requests, but not the Web Worker in which
Python starts and fetches its packages, so it understated the times.

| Emulated phone, Chapter 2, third of one core | Fast 4G (9 Mbps, 170 ms) | Slow 4G (1.6 Mbps, 563 ms) |
| --- | --- | --- |
| Opened alone, until the text shows | 11.3 s | 25.2 s |
| First Run all, from the press until no cell waits | 51.1 s | 98.4 s |
| The Next arrow, until Chapter 3 shows in a new tab | 9.2 s | 9.8 s |
| A reload, until the text shows again (outputs cleared) | 7.4 s | 8.7 s |
| Run all again after the reload (all 15 outputs back) | 40.1 s | 36.3 s |
| Peak memory of a renderer process | 361 MB | 356 MB |
| Error outputs, errors in the console | none | none |

Chapter 2's warning says so: its visible line says a slow phone can take a minute or more, and its
details give these times.

### Python started as the page opens

Most of that first Run all was Python installing the shop's package and running the setup cells,
not the chapter's code (under half a second in CPython). The row of buttons' extension now sends the
setup cells' code to Python as soon as the kernel is up, silently (`warmUp` in
`notebook/buttons/index.js`; the build marks the cells `"ms": {"setup": true}`): no cell runs, no
output appears and no count changes. Measured again, the same way, with Run all pressed as soon as
the page showed and after 45 seconds of reading:

| Emulated phone, Chapter 2, with the warm-up | Fast 4G (9 Mbps, 170 ms) | Slow 4G (1.6 Mbps, 563 ms) |
| --- | --- | --- |
| Run all pressed as soon as the page showed | 52.0 s | 100.6 s |
| Run all pressed after 45 s of reading | 4.5 s | 54.8 s |
| Run all again at once after a reload | 38.8 s | 40.0 s |

A press during the warm-up waits for it; no run gave an error. Every chapter has the warm-up: the
setup cells are the same in each.
