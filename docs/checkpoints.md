# Checkpoints

The reports written for the author at each checkpoint of the course plan (`docs/plan.md`, "The
checkpoints"), kept so the next stage can read what was decided and why.

## Checkpoint 1: the plan, the lab, the platform move and Chapter 1

Written on 6 October 2026 by the managing session, at the end of the session that took up the
author's brief for this course.

### What exists

- **The course's rules and plan.** `CLAUDE.md` (binding rules, adapted from the digital-design
  course's and the brief's own), `docs/plan.md` (eight parts, 32 chapters, each with what it
  builds into the lab, its central experiment, what it deliberately breaks and the terms it
  introduces), `docs/lab.md` (the lab's design), `docs/sources.md` (what every OpenLineage claim
  rests on), `docs/style.md` (the author's checklist, unchanged), `docs/authoring.md` and
  `docs/platform.md`.
- **The Metadata Lab** (`packages/lab`): a bicycle-parts shop's data platform that really runs in
  the browser. Its programs are written in the course's own SQL subset, which the lab parses and
  runs; its week is simulated night by night; storage records only what each system really would;
  and the lab can search for what the data alone suggests.
- **Chapter 1, The invisible data system**, built end to end: ten sections, seven figures, two
  challenges, five hints each, prose drafted by Haiku from checked facts, an originality note, a
  facts test pinning every stated number to the lab, and browser tests at desktop and phone
  widths. The site's front page lists all 32 chapters by part.
- **The platform move.** The lesson schema, the runtime and the primitives moved from
  `snowch/digital-design` to `snowch/learning-platform`, renamed to `@platform/*`, with three
  backwards-compatible generalisations (a `choice` field, a case-graded `text` or `data`
  artifact, a model named by the course). The digital-design course passes on the moved packages:
  strict tsc clean, 872 of 872 unit and integration tests. The cross-book workflow gained the
  metadata course's job and two jobs that run each course against the platform's current
  packages.

### What the author should look at

1. Chapter 1 as a learner, on the built site (`npm run dev`, then
   `#/chapter/invisible-data-system`), or on Pages once `main` exists and deploys.
2. The plan (`docs/plan.md`): the order of the 32 chapters, the rationed terms, and the decisions
   at its end.
3. The lab's design (`docs/lab.md`), above all the shop's week and its Thursday incident, which
   later chapters measure (13), trace (14) and find (16).
4. `docs/notes/chapter-01.md`: what the prose process caught, and the managing session's read.

### Decisions taken, for approval

- **The course's title**: *Metadata Systems: From Raw Files to a Working Metadata Platform*.
- **The shop**: an invented bicycle-parts retailer, chosen to stay clear of dbt's jaffle shop; its
  week is 7 to 13 September 2026.
- **One SQL subset of the course's own**, parsed and run by the lab, for the programs the learner
  reads now and the column lineage of Chapter 9.
- **The learner's state is derived**: later chapters regrade earlier chapters' stored work instead
  of keeping a separate lab state (`docs/lab.md`, "The learner's state").
- **The platform is copied, not linked**: `platform/` holds the platform's packages at a recorded
  commit, checked unedited on every run, because `snowch/learning-platform` is private and this
  repository is public; a submodule would need a credential in CI and in the deploy.

### Questions only the author can answer

1. **Make `snowch/learning-platform` public?** Then this course can take the platform as a git
   submodule instead of a checked copy, and the digital-design course could do the same.
2. **Switch the digital-design course to the moved packages now, or later?** The recipe is in
   `snowch/learning-platform`'s `docs/adoption.md`; the overlay job proves it on demand.
3. **The language of Part VI** (Chapters 23 to 27, where the learner implements the store, the
   collector, the graph, the queries and the interface): JavaScript run in a Web Worker
   (recommended: no download, every browser), or Python under Pyodide, which a data engineer may
   prefer, at about ten megabytes per visit. Needed by checkpoint 2.
4. **The default branch.** This repository was empty, so its first pushed branch,
   `claude/metadata-systems-agent-promotion-ggb2lv`, may now be its default. The deploy runs from
   `main`; creating `main` from this branch (or merging it there) publishes the site.
5. **Network access.** The build environment cannot reach openlineage.io and the other projects'
   documentation sites; OpenLineage was checked against its repository on GitHub instead. The
   hosts that unblock the later chapters' sources are listed in this session's conversation.

### Known gaps

- Chapters 2 to 32 are planned, not written.
- The bundle is about 860 kB minified, most of it the runtime's Markdown and maths rendering,
  which this course does not use.
- The lab models one week; later chapters extend it as they need.

### What comes next

Chapter 2, *What is metadata?*: the learner writes the first records about the shop's assets, in a
small notation the lab parses and checks, and asks Chapter 1's questions again of storage plus the
records. It needs the platform's case-graded text artifact (added in the move) and the derived
learner state (`docs/lab.md`).
