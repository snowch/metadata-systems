# Metadata Systems: From Raw Files to a Working Metadata Platform

Copyright © 2026 Christopher Snow.

An interactive, browser-based course on metadata and data lineage. You do not read about metadata
systems: you build a small one inside a small data platform that really runs in your browser, and
for each idea you predict, build, run, inspect, break and repair it.

The course is published at <https://snowch.github.io/metadata-systems/>.

**Status.** Chapter 1, *The invisible data system*, is built end to end, with its lab, figures,
challenges, prose and tests. The other 31 chapters are planned (`docs/plan.md`); the site's list
of chapters says which exist, worked out from the chapters themselves. Every push to `main`
deploys the site (`.github/workflows/deploy.yml`).

## Read first

- [`CLAUDE.md`](CLAUDE.md): the binding project rules, including originality and what breaks the
  build.
- [`docs/plan.md`](docs/plan.md): the parts and chapters, what each builds and breaks, the terms
  each introduces, the checkpoints and the decisions taken since the brief.
- [`docs/lab.md`](docs/lab.md): the Metadata Lab, the shop's data platform every figure runs.
- [`docs/platform.md`](docs/platform.md): what the course takes from `snowch/learning-platform`
  and what is its own.
- [`docs/authoring.md`](docs/authoring.md): how a chapter is made, its figures and their props,
  the prose process and the tests.
- [`docs/sources.md`](docs/sources.md): the specifications every technical claim is checked
  against, and the licences of what the site ships.
- [`docs/style.md`](docs/style.md): the style checklist every learner-facing string is edited
  against.
- [`docs/checkpoints.md`](docs/checkpoints.md): the reports written for the author at each
  checkpoint.

## Working on it

```sh
npm ci            # once; .npmrc sets legacy-peer-deps, as in the digital-design course
npm run dev       # the course at http://localhost:5173/metadata-systems/
npm run check     # exactly what CI runs: Prettier, the copyright line, the platform copy,
                  # licences, tsc, Vitest, the build, Playwright
```

The repository is an npm workspace: `apps/course` (the shell), `content/lessons` (the chapters as
data, and the plan as data), `packages/lab` (the Metadata Lab: the shop, its SQL subset, its
storage, and what can be inferred from it), `packages/views` (the figures, the challenge editor,
the grader and the book), `platform/` (the learning platform's packages, copied from
`snowch/learning-platform` at the commit `platform/SOURCE.json` records), and `tests/educational`
(Playwright).
