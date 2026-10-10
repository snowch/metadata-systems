# Chapter 1 as a notebook: the prototype

The author asked whether the course could be delivered as notebooks that run in the browser, for
readers who are data engineers and think in notebooks, and then for a prototype of Chapter 1. This
note records what was built, why each choice was made, what was measured, and what is still open.
The course itself is unchanged: the prototype is published beside it, under `/notebook/`.

## What was built

- `notebook/chapter_01.py`: Chapter 1 as a marimo notebook. The prose is the chapter's approved
  essay; the four figures are drawn by the notebook's own Python; fifteen cells of code are
  visible, and the reader can change and run every one. The words new to the notebook were drafted
  by Haiku from briefs AK and AL (`docs/notes/chapter-01/briefs/round-15/`).
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
  computed at export time and saved into the page. Then `run_on_load.py` makes the cells run when
  the page loads, and `licences.py` checks the bundled packages' licences.
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

All on 10 October 2026, in Playwright's Chromium 141.0.7390.37 (build 1194), headless, on this
Linux container, from a local HTTP server: no network delay and no CPU throttling. "Phone" is
Chromium's phone emulation (390 by 844 pixels, touch); no real phone was measured.

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

- `build_ipynb.py` builds the Jupyter notebook from `notebook/chapter_01.py`, cell by cell: the same
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
- In a notebook the reader meets code. The visible cells use the shop's three systems (`storage`,
  `warehouse`, `reporting`) and three helpers of the chapter (`shop.run_week`,
  `shop.queries_that_rebuild`, `shop.cleaning_rules_that_fit`); the code that draws the figures
  is in hidden cells. "No lab on the page" (`CLAUDE.md`) holds for the words; whether it should hold
  for the code is the author's call.
