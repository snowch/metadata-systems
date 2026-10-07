# The platform

What this course takes from the author's learning platform, how it takes it, and what is its own.

## What the platform is

`snowch/learning-platform` holds three packages, written for the digital-design course and moved
there when this course became their second consumer (`docs/plan.md`, decision 4):

| Package | What it holds |
| --- | --- |
| `@platform/lesson-schema` | the lesson data format: ten sections in a fixed order, interactives by kind, challenges with tests, five hints and a reference, the originality note, the term gate, the model gate, and the format as JSON Schema |
| `@platform/lesson-runtime` | a lesson rendered from its data: the sections, the model badges and notes, the challenge runner, the hint ladder, and learner state kept in the browser and graded again on every load |
| `@platform/primitives` | the shared interaction primitives: `PredictionChallenge`, `FaultInjector`, `Stepper`, `Timeline`, `StateInspector`, `DrillDown` |

The runtime knows a course only through the `Book` it is given: the lessons, a registry of figures
by kind, a challenge editor, a grader, and a note per model. This course's book is `createBook` in
`packages/views/src/book.tsx`.

## How this course takes it

`platform/` is a copy of the platform's `packages/` at one commit, which `platform/SOURCE.json`
records with a hash of every file. `npm run check` fails if any file there differs, so the copy
changes only by syncing it:

```sh
node scripts/sync-platform.mjs ../learning-platform   # a clean checkout of the platform
```

A fix to the platform is made in `snowch/learning-platform`, checked there, and then synced here.

A copy and not a git submodule. `snowch/learning-platform` is public (since checkpoint 1, when the
author made it so: its code was already public through this copy), so anybody can check
`SOURCE.json`'s commit against it. The copy stays: cloning, building and deploying the course need
no second checkout, and the check above already fails on any edit. A submodule at `platform/` could still replace the copy
and the sync script without changing anything else, because the workspaces and the imports
already name `platform/*`.

## What this course needed the platform to generalise

Five general shapes were added beside the digital-design course's, and nothing that course uses
changed (its full unit suite passes on the moved packages; `snowch/learning-platform`'s
`docs/adoption.md`):

- **A challenge built from choices.** An answer field may be a `choice` among options, and the
  schema holds the reference to one of them. Both of Chapter 1's challenges are built from
  choices, graded case by case by the book.
- **An artifact that is text or data.** A written or drawn challenge may be graded case by case
  when its reference is `text` or `data`, with no circuit rules. Chapters 2 (records), 6 and 7
  (events) and 9 (SQL) need it.
- **A model the book names.** A figure's model is a name the book chooses, here `lab`; `none` stays
  reserved for a figure that runs nothing, and `modelProblems` holds the lessons to the models the
  book declares. A book may give no note for a model: this course gives none, because Chapter 1
  explains the lab in its own prose, where it first names it, and the runtime then states no note
  at the foot of a page.
- **A figure's role.** A figure may say what it asks of the reader (`role`, a name the book
  chooses); the runtime's badge then names the role instead of the model, and the note it opens
  is the book's note for the role (`roleNotes`) alone; a role with no note, here `reference`, has
  a badge that opens nothing. Every figure in this course
  has one: an experiment, an instrument to inspect with, or a reference (`CLAUDE.md`,
  "Experiments, instruments and explanations"). A figure without a role keeps the model's badge,
  as the digital-design course's do.
- **A section's details.** A section may carry `details`: the words of a control and the Markdown
  it opens, shown closed after the section's prose and before its figures (the platform, at
  8c2f186). Chapter 1 keeps how the lab runs there, where it first names the lab, so the learner
  reaches the first question sooner; the course styles it as it styles every disclosure.

## What is this course's own

- The lab, its SQL subset, its storage model and its inference searches (`packages/lab`).
- The figures, the choice editor and the grader (`packages/views`).
- The shell, its look and its words (`apps/course`): the platform shares an interaction
  vocabulary and a lesson format with the author's other courses, not a look.
- The runtime's words where this course names things differently: the model's badge, the roles'
  badges and notes, and the labels of a failed test (`runtimeStrings` and `createBook` in
  `packages/views/src/book.tsx`).

## Shared primitives in use

`PredictionChallenge` (every commitment before the lab answers: the predictions, the requirement,
the decisions and the change lab's prediction), `FaultInjector` (the change lab's changes and the
question map's weeks) and `StateInspector` (the record, column and day tables). `Stepper`, `Timeline` and `DrillDown` wait for the chapters
that need them: runs over time (Chapter 6), event delivery (Part V) and drilling from an asset to
its columns (Chapter 9).
