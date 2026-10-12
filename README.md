# Metadata Systems: From Raw Files to a Working Metadata Platform

Copyright © 2026 Christopher Snow.

An interactive, browser-based course on metadata and data lineage. You do not read about metadata
systems: you build a small one inside a small data platform that really runs in your browser, and
for each idea you predict, build, run, inspect, break and repair it.

The course is published at <https://snowch.github.io/metadata-systems/>.

**Status.** Each chapter is a Jupyter notebook that runs in your browser (JupyterLite, with a
Python kernel compiled to WebAssembly); the course's front page lists the chapters by part and
opens each written one. Chapters 1 to 13 are written; the others are planned (`docs/plan.md`).
Every push to `main` deploys the site (`.github/workflows/deploy.yml`).

## Read first

- [`CLAUDE.md`](CLAUDE.md): the binding project rules, including originality and what breaks the
  build.
- [`docs/plan.md`](docs/plan.md): the parts and chapters, what each builds and breaks, the terms
  each introduces, the checkpoints and the decisions taken since the brief.
- [`docs/lab.md`](docs/lab.md): the engine, the shop's data platform in Python that computes every
  figure.
- [`docs/authoring.md`](docs/authoring.md): how a chapter is made, the prose process and the tests.
- [`docs/sources.md`](docs/sources.md): the specifications every technical claim is checked
  against, and the licences of what the site ships.
- [`docs/style.md`](docs/style.md): the style checklist every learner-facing string is edited
  against.
- [`docs/checkpoints.md`](docs/checkpoints.md): the reports written for the author at each
  checkpoint.

## Working on it

```sh
npm ci            # once
npm run dev       # the front page at http://localhost:5173/metadata-systems/
npm run check     # exactly what CI's Check runs: Prettier, the copyright line, licences, tsc,
                  # Vitest, the notebooks' tests, the prose check, the build, Playwright
```

The notebooks' site needs JupyterLite's Python packages (`notebook/jupyterlite/requirements.txt`)
and the network once, to fetch Pyodide:

```sh
pip install -r notebook/jupyterlite/requirements.txt
notebook/jupyterlite/build.sh site                # the notebooks, built into ./site
node notebook/jupyterlite/smoke.mjs site          # presses the buttons in a browser, as a phone
```

The repository: `notebook/` (the chapters' sources, `chapter_NN.py`, each built into a notebook;
`shop`, the engine; `tests`, which pin every number and sentence the notebooks state; `buttons`,
the row of Run all, Run below and Save buttons; `jupyterlite`, the site's build), `apps/course`
(the front page), `content/plan` (the plan as data, and which chapters have notebooks), and
`tests/educational` (Playwright, for the front page).
