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
  widths. The site's front page lists all 32 chapters by part. It has been reviewed once by a
  reader on another model and revised (below).
- **The platform move.** The lesson schema, the runtime and the primitives moved from
  `snowch/digital-design` to `snowch/learning-platform`, renamed to `@platform/*`, with three
  backwards-compatible generalisations (a `choice` field, a case-graded `text` or `data`
  artifact, a model named by the course). The digital-design course passes on the moved packages:
  strict tsc clean, 872 of 872 unit and integration tests. The cross-book workflow gained the
  metadata course's job and two jobs that run each course against the platform's current
  packages. Its run on the platform's branch (run 6, 6 October 2026) passed all eight jobs: the
  three new ones, the digital-design course's own full check, and the four books.

### The review of Chapter 1

A reviewer on another model read the built chapter as its learner and wrote 32 findings (3 high,
17 medium, 12 low); an independent sceptic attacked each against the lab and the build, upholding
10, upholding 20 in part, rejecting 1 and finding 1 already fixed
(`docs/notes/chapter-01/review/`). The three high findings were real: the page said a failed
night looks like a quiet one, which the lab contradicts; it said the reporting tool keeps the query
behind its chart, which the lab does not model; and it used "rebuild" in two senses. Two of those
false statements, and a third, came from the managing session's own briefs, written without being
read off the lab; the redraft's facts were probed from the lab first.

The revision, code first and then the prose process:

- every prediction is now committed before the lab answers, including one per change in the
  failure experiment and one after the second challenge, and the days prediction asks for a count
  that most learners will get wrong (six expected, three found);
- the learner sorts the chapter's questions before the lab places them, and the map moves as the
  learner switches between the changed weeks, so a question visibly leaves the data's group;
- the failure experiment opens once the learner's own query passes, and nothing names the first
  challenge's answer before then;
- the kinds of record, and *metadata* with them, are derived from the questions only a record can
  answer; the opening question about Thursday is closed, its cause left to later chapters as the
  plan says;
- on a phone, a wide table says that it scrolls, dates do not break, and SQL wraps;
- the closing note's two unsourced claims about real systems became two sourced ones (Iceberg's
  snapshots, Delta Lake's history).

`docs/notes/chapter-01.md` records what each finding got and what the second prose pass caught.

### What the author should look at

1. Chapter 1 as a learner, on the published site
   (<https://snowch.github.io/metadata-systems/#/chapter/invisible-data-system>, deployed from
   `main`), or locally with `npm run dev`.
2. The plan (`docs/plan.md`): the order of the 32 chapters, the rationed terms, and the decisions
   at its end.
3. The lab's design (`docs/lab.md`), above all the shop's week and its Thursday incident, which
   later chapters measure (13), trace (14) and find (16).
4. `docs/notes/chapter-01.md`: what the prose process caught, the managing session's read, and
   the review with what each finding got.

### Decisions taken, for approval

- **The course's title**: *Metadata Systems: From Raw Files to a Working Metadata Platform*.
- **The shop**: an invented bicycle-parts retailer, chosen to stay clear of dbt's jaffle shop; its
  week is 7 to 13 September 2026.
- **One SQL subset of the course's own**, parsed and run by the lab, for the programs the learner
  reads now and the column lineage of Chapter 9.
- **The learner's state is derived**: later chapters regrade earlier chapters' stored work instead
  of keeping a separate lab state (`docs/lab.md`, "The learner's state").
- **The platform is copied, not linked**: `platform/` holds the platform's packages at a recorded
  commit, checked unedited on every run. It began as a copy because `snowch/learning-platform`
  was private; it is public since checkpoint 1, and the copy stays because cloning, building and
  deploying the course then need no second checkout (`docs/platform.md`).

### The author's answers

1. **Make `snowch/learning-platform` public?** Yes, and the author made it public on 6 October
   2026: its code was already public through this course's copy. This course keeps its checked
   copy (`docs/platform.md`).
2. **Switch the digital-design course to the moved packages now, or later?** The author asked for
   a proposal and agreed to it: now, because two copies of one runtime drift with every fix, and
   the overlay job already shows that course passing on the moved packages. The switch is made in
   `snowch/digital-design`: its three packages replaced by the platform's, taken the way this
   course takes them, `@dd/` renamed to `@platform/`, and its full check run, Playwright
   included.
3. **The language of Part VI?** Python under Pyodide: the learner reads and writes this code, and
   Python is a data engineer's language. Pyodide's core is about 5.3 MB compressed, once, served
   from the course's own site (`docs/plan.md`).
4. **"Predict again"?** What serves the learner is a commitment that stays: the prediction is
   worth its surprise, and a re-answer after the reveal erases it. The platform's prediction
   control now offers "Predict again" only to a figure that asks for it (the digital-design course
   keeps it); this course drops it, and the sort's "Sort again" with it, and offers "start this
   chapter again" at the foot of each chapter instead, after a second press.

Settled since this report was first drafted: `main` exists and the site deploys from it; and the
documentation hosts are reachable, so OpenLineage was compared with its published site (the same
as its repository's pages, with one disagreement between its schema and its run-cycle page, now
recorded) and the plan's product claims were checked against each project's own documentation
(`docs/sources.md`).

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
