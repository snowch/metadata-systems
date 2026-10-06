# Writing a chapter

How a chapter is made, from the lab to the review. Chapter 1, `content/lessons/invisible-system.ts`,
is the worked example; copy its shape.

## The lab first

A chapter starts in `packages/lab`, not in its prose. Decide what the learner must discover, then
make the lab compute it: a figure shows what the lab computes, a prediction's answer is a probe the
lab runs, and a challenge's expected values come from the lab's grader. If the lab cannot compute
what a figure needs, the lab gains it, with a test, before the figure exists. `docs/lab.md` says
what the lab models and what it does not.

## A chapter is data

A chapter is one module in `content/lessons/` exporting a `LessonInput` (from
`@platform/lesson-schema`), listed in `content/lessons/index.ts`. Its `module` is its part and its
`order` is its chapter number, both as `content/lessons/plan.ts` gives them; the content tests hold
the title and the introduced terms to the plan as well.

- `objectives`: what the learner can do afterwards, each starting with a verb.
- `introduces`: the terms the plan gives the chapter; the term gate fails any earlier chapter that
  uses one, including chapters not yet written. `termExemptions` lists a word used in another
  sense, with the reason (Chapter 1 uses "run" as a verb; the noun is Chapter 6's).
- `sections`: exactly ten, in the platform's order. A figure (`interactives`) has an `id`, a
  `kind` from the book's registry, a `timeModel` (`lab`, or `none` for a figure that runs nothing),
  a plain-text `caption`, Markdown `lead` and `after`, and `props` its schema checks.
- `challenges`: built from choices for now (`gradedDirection: "answer"` with `choice` fields and
  `answers` tests naming a grader the book has). Each has five hints, a starting point that fails
  and a reference that passes.
- `modelVsReality` and `originalityNote`, written in the same commit as the chapter.

Keep the words out of the structure file: the chapter's paragraphs go in `<id>.prose.ts`, its
titles, captions and labels in `<id>.labels.ts`. Captions, titles and option labels render as plain
text: no Markdown in them.

## The figures

The registry is `INTERACTIVES` in `packages/views/src/book.tsx`. Each figure parses its props with
a zod schema and says so in its place when they do not fit.

| kind | props | what it does |
| --- | --- | --- |
| `dashboard` | `changes?` | the reporting tool's chart as Monday morning shows it, one bar per value, from the lab's week |
| `lab-prediction` | `question`, `options`, `probe` (`owner-kind` of an asset; `days-matching` of a source, a filter and a target), `explain?`, `changes?` | the learner commits to an option; the lab runs the probe and answers, with its evidence; `explain` shows only after the commit |
| `storage-inspector` | `initial?`, `changes?` | every asset by the system that holds it; for the one chosen, what its system records, its columns, its rows, and what storage says about the chapter's questions |
| `change-lab` | `changes` (each an id, a label and an outcome), `afterAll?`, `challengeId`, `target?` | runs the week again with one change; shows what storage shows differently, the learner's passing query (or the course's) against the new target, and every query in the builder's choices that rebuilds it; each outcome shows once its change has run, and `afterAll` once all have |
| `question-map` | `asset?`, `changes?`, `challengeId` | the chapter's questions about one asset, placed by what can answer them (storage, the data, only a record), each with its evidence, all computed |
| `challenge` | `challengeId` | the runtime's challenge runner with the book's choice editor, which shows the SQL the choices mean and its result |

The book's graders are `reproduces` (a sum compared with a target day by day) and `same-rows` (a
set of cleaning rules compared with `clean_orders` as multisets).

## The prose process

`CLAUDE.md` states the rule: every string a learner reads is drafted by a Haiku subagent from a
brief of facts and checked by the managing model for facts only. For a chapter:

1. Write the fact sheet, `docs/notes/chapter-NN/facts.md`, every number read off the lab, with the
   chapter's working words (each with one meaning on the page) and the words it must not use.
2. Write one brief per group of sections (`briefs/`), each a numbered list of facts per string,
   with the keys the drafts come back under. Scan the briefs for banned words before they go out.
3. Run the drafts in parallel. Check facts only: a dropped fact gets the fewest words that carry
   it; a wrong fact goes back with a note; nothing is rewritten. Record what the check caught in
   the chapter's note.
4. Place the strings, then read the whole chapter from a dump of the built page
   (`docs/notes/chapter-NN/review/page.md`), start to finish.
5. Review: a reader on another model, then an independent sceptic on each finding, then fixes:
   code first, fact briefs for wording second, then one more read.

## What the tests hold a chapter to

`npm run check` is exactly what CI runs.

- The schema and the platform's checks: ten sections in order, five hints, a reference, an
  originality note, every challenge mounted, every choice's reference one of its options.
- The term gate against the whole plan, and the plan's list against `docs/plan.md`.
- The model gate: every figure runs a model the book has a note for.
- `content/lessons/lessons.test.tsx`: every reference passes and every starting point fails; no
  prediction's answer appears in its question, caption, lead or after-text; the whole chapter
  renders in jsdom with no figure problem.
- `content/lessons/<id>.facts.test.ts`: every number the chapter's words state, read off the lab.
- `tests/educational/chapter.spec.ts`, at desktop and phone widths: the chapter renders whole with
  no console error and no horizontal scroll, even after every figure is used; each challenge is
  completable through the page with its reference and refuses its starting point; saved work is
  graded again on load and a tampered mark earns nothing; a reset takes two steps; hints come one
  rung at a time; a prediction is committed before the lab answers; a change's outcome waits for
  its run.
- `tests/educational/aesthetics.spec.ts`: no visible text under 11 pixels, every phone control at
  least 40 pixels tall, no line of prose much over 85 characters.

A commit carries the tests for the code it changes, so every commit passes the check on its own.
