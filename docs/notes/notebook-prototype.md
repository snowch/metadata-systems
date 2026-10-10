# Chapter 1 as a notebook: the prototype

The author asked whether the course could be delivered as notebooks that run in the browser, for
readers who are data engineers and think in notebooks, and then for a prototype of Chapter 1. This
note records what was built, why each choice was made, what was measured, and what is still open.
The course itself is unchanged: the prototype is published beside it, under `/notebook/`.

## What was built

- `notebook/chapter_01_part_1.py` and `chapter_01_part_2.py`: Chapter 1 as two marimo notebooks,
  one per part (one notebook, `chapter_01.py`, until the split under "The chapter in two parts",
  below). The
  prose is the chapter's approved essay, with part 1's tour of the shop added; the figures are drawn
  by the notebooks' own Python; the cells of code are visible, and the reader can change and run
  every one. The words new to the notebook were drafted by Haiku from briefs AK and AL
  (`docs/notes/chapter-01/briefs/round-15/`), and those of the two parts from AO and AP
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
- The new words are Haiku's drafts of briefs AO and AP (`docs/notes/chapter-01/briefs/round-16/`),
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

## Phones

Nothing here measured a real phone, so the page says only what was measured and what one report
shows: in Safari, a page that uses a lot of memory can be reloaded by the browser, with the
message "This webpage was reloaded because it was using significant memory" (a developer's report
on Apple's developer forums, `docs/sources.md`). A reload loses what the reader changed, as
measured above. The warning at the top of the notebook says so (brief AL).

## Open questions for the author

- Which notebook, if either: marimo's (cells re-run by themselves, about 1 GB, edits lost on
  reload) or JupyterLite's (familiar, about 0.44 GB, nothing runs until asked, saved edits kept
  and shown in place of later updates).
- Whether the notebook should replace the essay pages, sit beside them, or be dropped.
- Edit mode or run mode: a notebook the reader edits, at about 1 GB in a desktop browser, or a
  page of outputs and controls at about 0.39 GB.
- marimo's editor brings its own chrome: a status bar, a menu, a settings button, an assistant panel
  on a computer that would ask the reader to connect an AI provider, and a toolbar above every cell
  on a phone. The stylesheet hides only what covered the prose.
- Whether the course's essay page should be split as the notebooks are. The course numbers its
  chapters and the platform gives each its own page, so two pages would either renumber the plan
  from Chapter 2 on (33 chapters, with the chapter numbers `CLAUDE.md` and the plan use), or need
  the platform to let one chapter have two pages.
- In a notebook the reader meets code. The visible cells use the shop's three systems (`storage`,
  `warehouse`, `reporting`) and three helpers of the chapter (`shop.run_week`,
  `shop.queries_that_rebuild`, `shop.cleaning_rules_that_fit`); the code that draws the figures
  is in hidden cells. "No lab on the page" (`CLAUDE.md`) holds for the words; whether it should hold
  for the code is the author's call.
