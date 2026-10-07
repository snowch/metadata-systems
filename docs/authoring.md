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
  `role` (what it asks of the learner: `experiment`, `inspect` or `reference`; "Experiments,
  instruments and references", below), a `kind` from the book's registry, a `timeModel` (`lab`,
  or `none` for a figure that runs nothing), a plain-text `caption`, Markdown `lead` and `after`,
  and `props` its schema checks.
- `challenges`: built from choices for now (`gradedDirection: "answer"` with `choice` fields and
  `answers` tests naming a grader the book has). Each has five hints, a starting point that fails
  and a reference that passes.
- `modelVsReality` and `originalityNote`, written in the same commit as the chapter.

Keep the words out of the structure file: the chapter's paragraphs go in `<id>.prose.ts`, its
titles, captions and labels in `<id>.labels.ts`. Captions, titles and option labels render as plain
text: no Markdown in them.

A figure's `lead` and `after` are chapter prose: the page draws them outside the figure's card, at
the prose's measure, and the card holds the caption and the lab's view. Write a lead as the text
that brings the reader to the figure, not as part of the figure. In the figures' own strings
(`packages/views/src/strings.ts`), a name between backticks is set as code wherever the figure
draws the sentence itself.

## The figures

The registry is `INTERACTIVES` in `packages/views/src/book.tsx`. Each figure parses its props with
a zod schema and says so in its place when they do not fit.

| kind | props | what it does |
| --- | --- | --- |
| `platform-map` | `changes?`, `dock?` | the platform as the lab's `platformMap` computes it: the systems in the order data moves through them, the assets each holds, and between two systems the programs the learner cannot see, never a link from one asset to another; once the learner scrolls past it, a button at the foot of the window opens the same map over the page, unless `dock` is false |
| `dashboard` | `changes?` | the reporting tool's chart as Monday morning shows it, one bar per value, from the lab's week |
| `lab-prediction` | `question`, `options` (each a value, a label, and either `means`, the answers of a naming probe it stands for, or `range`, the counts of a counting probe), `probe` (`owner-kind` of an asset; `day-total` of a source, a filter, a target and a day; `clean-fits`), `explain?`, `changes?`, `requires?` (a challenge id), `mode?` (`predict`, the default, or `choose`), `compare?` (for a choice: its button, `commit`, in words about what it shows, and the line after it, `mine` with `{choice}` and `lab` with `{answer}`), `undecided?` (the option "I can't tell yet": a value, a label, and the `line` shown after it, with `{answer}`) | the learner commits to an option, and the commitment stays (no "Predict again"); the lab runs the probe and answers with the option that stands for what it found, with its evidence; a prediction is marked right or not, "I can't tell yet" and a choice are set beside what the lab found and marked neither; `explain` shows only after the commit; with `requires`, the figure waits until the learner's own work on that challenge passes |
| `requirement` | `requirement` (its words, as written), `question`, `options` (each a value, a label, `short`, what it needs stored, `asks`, the question it asks with names between backticks, and `means`, the probe's answers that answer it), `undecided` (the option to store nothing until the requirement says what it is for), `probe` (`owner-kind` of an asset), `buttons` (`choose` and `show`), `headings` (`asks`, `store`, `answers`), `text` (`mine` with `{choice}`, `undecided`, `meanings`, `lab` with `{value}`, `{owned}` and `{tables}`, `explain?`) | a requirement questioned (`CLAUDE.md`, "Question the requirement"): the learner chooses what to store, or nothing yet; the figure then shows the questions the requirement could be asking, each beside what it needs stored, with their own row marked; at a second press the lab runs the probe, says what the platform records, and the same table gains a column saying which questions that record answers, in words and without colour; no reading is called wrong, and both presses stay |
| `decision` | `question`, `options` (each a value, a label, `means?`, for an explanation a check will read, the findings that support it: `left`, `lower`, `moved`, and `after?`, a line on what the option can show, never what it leads to), `commit`, `mine` (with `{choice}`), `test?` (how to go on with the figures that follow), `waits?` (an earlier figure that takes a commitment) | a decision in an investigation: where to look first, or which explanation to test; the figure keeps the choice and reveals nothing of the answer: after the choice it shows the learner's line, the chosen option's `after` and `test`, and the testing is theirs; with `waits`, a line stands in its place until the learner has committed their answer in that figure, so a decision that states what a prediction found cannot give it away |
| `hypothesis-check` | `of` (the `decision` figure it checks), `options` (the same explanations, in the same order), `requires` (a challenge id), `probe` (`day-gap`: a source, the asset a rebuild reads and the rows it keeps, a target and a day), `button`, `headings` (`explanation`, `supported`), `text` (`mine` with `{choice}`, `none`, `lab` with `{orders}`, `{kept}`, `{left}` and `{leftTotal}`, `explain?`) | waits until the learner's own work on the challenge passes; at a press, reads the day's rows against the rows the rebuild keeps, and marks which explanations they support, the learner's choice marked; says what the rows show, never why |
| `storage-inspector` | `initial?`, `from?` (a `decision` figure, and for each of its options the asset to open), `changes?` | every asset by the system that holds it; for the one chosen, what its system records, what storage says about each of the chapter's eight questions (the same eight for every asset), its columns and its rows; a table wider than its box says so; with `from`, it opens on the asset the learner chose in that decision, until they choose another here |
| `change-lab` | `changes` (each an id, a label and an outcome), `afterAll?`, `challengeId`, `target?`, `prediction` (a question and options with count ranges) | waits until the learner's own query passes; for each change, takes a committed prediction of how many queries in the builder's choices will rebuild the target, then runs the week with it and shows those queries (the lab's answer), what storage holds on Monday morning with the comparison against the first run labelled as the lab's, and the learner's query against the new target; each outcome shows once its prediction is committed, and `afterAll` once all are |
| `question-map` | `asset?`, `challengeId`, `weeks?` (each a change id and its label) | the learner places the chapter's questions about one asset in three groups and commits, for good; the lab then places them (storage, the data, only a record), each with its evidence and, for a question only a record answers, the kind of record that would; a week selector runs the placement on each change and marks the questions that moved; a query and its source are named only once the learner's own query passes |
| `challenge` | `challengeId` | the runtime's challenge runner with the book's choice editor, which shows the SQL the choices mean and its result |

The book's graders are `reproduces` (a sum compared with a target day by day) and `same-rows` (a
set of cleaning rules compared with `clean_orders` as multisets).

## Experiments, instruments and references

Every figure says what it asks of the learner (`CLAUDE.md`, "Experiments, instruments and
explanations"), in its `role`, which its badge names; the note the badge opens gives a line on
what to do with that kind of figure, where there is one, and nothing else: the lab is explained
once, where Chapter 1 first names it (`roleNotes` on the book, `roles` and
`roleBadgeLabel` in `packages/views/src/strings.ts`).

- `experiment`: the learner commits (to a prediction, a choice, a decision or a query they build),
  acts, and the lab's evidence answers. Every figure that takes a commitment before the lab
  answers (`PREDICTION_KINDS` in `packages/views/src/book.tsx`: a prediction, a requirement, a
  decision, a change run after a prediction, a sort) is one, and so is a challenge. Prefer it.
- `inspect`: an instrument the learner examines for evidence, such as the inspector or the
  dashboard. Never present it as the activity: put a question in front of it and say what to look
  for. Chapter 1's inspector follows a decision about where to look first (`where-first`) and
  opens on the asset chosen there (`from`).
- `reference`: what the learner has been told, kept to hand, such as the platform map. It asks
  nothing.

Before a figure is built, it gets a block in the chapter's notes, under "Figures", in the page's
order: a heading with its id, its role, and for an experiment twelve answers, each under its own
label.

```
### `predict-days`

- **Role:** experiment
- **Objective:** what the learner should understand, discover or be able to do afterwards.
- **Known before:** what is on the page above the figure, not what the lab knows.
- **Driving question:** the question, hypothesis or decision that drives it.
- **The action:** what the learner does.
- **Why the action:** why the learner must act to learn it, and not only look.
- **Evidence:** what the action produces.
- **Consequence:** what they believed before, what the evidence lets them believe after, and what
  a wrong prediction teaches.
- **Predictable:** whether they could reason to the outcome from what is on the page.
- **Gives nothing away:** why no option, caption or line above it carries the explanation.
- **Not knowing:** whether "I can't tell yet" could be the right engineering response, and
  whether the figure offers it.
- **Next question:** the question the result raises, and where the chapter takes it.
- **An experiment:** why it is an experiment, and not an instrument or a reference.
```

An instrument or a reference answers two, **Serves** (the question it serves) and **Why now**
(why the learner needs it at that point). A figure that completes another experiment, such as a
check after the learner's own work, gives **Part of** and that experiment's id instead of the
twelve. The content tests fail a figure without a role, a commitment that is not an experiment, a
block missing, out of the page's order or not repeating the figure's role, and an answer missing.

## Predictions

A prediction is an experiment, built around what the learner should learn (`CLAUDE.md`,
"Interaction is the explanation").

- **State the objective first.** If it cannot be said in a sentence, redesign the exercise.
- **Ask for an observable result.** Each option names a result and the belief it reflects ("51.50:
  `daily_sales` holds the total of Thursday's orders"), in parallel form and length, so that none
  is chosen for its wording. An option never says why the result will be what it is: that is the
  explanation, and it comes after the evidence.
- **Establish the effect before asking for its cause.** "Is there a difference?" comes before
  "where is it?", "what could explain it?" and "which explanation fits?", and the later questions
  are an investigation, not a reveal: the learner decides where to look first (a `decision` whose
  choice opens the inspector), chooses an explanation to test (another `decision`), tests it with
  the figures that follow, and the rows are read against their choice only after their own work
  passes (`hypothesis-check`). Chapter 1's Thursday is the example. Each decision waits for the
  answer before it (`waits`): the first states the difference the prediction found, and the
  figure just below a prediction is in view while the learner is still choosing.
- **Prefer independent evidence**: a total the learner could add up, rows they could read, not
  a failure inside a program they cannot see.
- **Offer "I can't tell yet"** where nothing on the page settles the question (`undecided` on the
  figure). It is marked neither right nor wrong, and its line says what the lab found.
- **A count is asked as what it means.** None, one, or more than one are explanations; "four or
  five" is a number to hit.
- **Where the page gives no grounds, ask a choice.** If nothing above the figure lets a learner
  tell the options apart (how this shop happened to set up its warehouse), ask what they would do
  in the shop's place, with `mode: "choose"`: the lab shows what the shop does beside their
  choice, and neither is called right. Chapter 1's owner question began as one; when the question
  is what a requirement means, the requirement figure ("Requirements", below) asks it better.
- **The lab answers.** A naming probe's answer is a word the option lists under `means`; a
  counting probe's is a count inside the option's `range`. The lesson never stores the answer.

The content tests also fail a prediction whose option stands for no answer at all, other than
"I can't tell yet".

## Requirements

Some exercises question a requirement instead of predicting the lab (`CLAUDE.md`, "Question the
requirement"). Look for one in every chapter: `docs/plan.md` lists a candidate for each, a
requirement that sounds settled in that chapter's material. To build one:

- **State the requirement in words**, as somebody at the shop would write it, and say nothing yet
  about what it means. The figure shows it apart, as a quotation.
- **List what it could be asking**, each as a question, and what each question needs recorded.
  Every reading must be one a reasonable engineer could hold; none is there to be wrong.
- **Let the learner commit first**, to what they would record, or to nothing until they know what
  the requirement is for. Only then show the readings, and only after a second press what the
  platform records.
- **Let the lab say which readings the record answers.** A probe reads what the platform records,
  each reading names the answers that satisfy it under `means`, and the figure marks them. The
  record should answer some readings and not others: that is the gap the learner experiences. The
  explanation then says whether the requirement is met as written, and under which meanings.

The chapter's notes get a section, "Requirements", that names the figure and walks the five things
`CLAUDE.md` keeps apart; a chapter with no requirement to question says why under the same
heading. The content tests fail notes without the section, a requirement figure the section does
not name, a requirement figure whose record answers every reading or none, and one that names the
platform's record in any text the learner reads before the second press.

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
   (`docs/notes/chapter-NN/review/page.md`), start to finish, in every state its figures reach:
   before and after each commitment, and after each change.
5. Review: a reader on another model, then an independent sceptic on each finding, then fixes:
   code first, fact briefs for wording second, then one more read.

## What the tests hold a chapter to

`npm run check` is exactly what CI runs.

- The schema and the platform's checks: ten sections in order, five hints, a reference, an
  originality note, every challenge mounted, every choice's reference one of its options.
- The term gate against the whole plan, and the plan's list against `docs/plan.md`.
- The model gate: every figure runs a model the book has a note for.
- `content/lessons/lessons.test.tsx`: every reference passes and every starting point fails; no
  prediction's answer appears in its question, caption, lead or after-text; every figure has a
  role and its block in the chapter's notes, in the page's order, with every answer its role
  needs; a prediction's result is stated below it only in a figure that waits for its answer;
  every option stands for an answer or a count, other than "I can't tell yet"; the notes
  have a "Requirements" section naming every requirement figure; a requirement figure's record
  answers some readings and not all, and no text before its second press names that record; the
  whole chapter renders in jsdom with no figure problem.
- `content/lessons/<id>.facts.test.ts`: every number the chapter's words state, read off the lab.
- `tests/educational/chapter.spec.ts`, at desktop and phone widths: the chapter renders whole with
  no console error and no horizontal scroll, even after every figure is used; each challenge is
  completable through the page with its reference and refuses its starting point; saved work is
  graded again on load and a tampered mark earns nothing; a reset takes two steps; hints come one
  rung at a time; a prediction is committed before the lab answers; a requirement's meanings come
  after the learner's choice and before what the platform records; a change's outcome waits for
  its run; every figure's badge names its role; the inspector opens where the learner chose to
  look first.
- `tests/educational/aesthetics.spec.ts`: no visible text under 11 pixels, every phone control at
  least 40 pixels tall, no line of prose much over 85 characters; the map's names whole and its
  systems even at every width; the map's button clear of the page's foot on a phone; a
  challenge's choices filling their rows.
- `apps/course/src/tokens.test.ts`: text at 4.5:1 on every surface it sits on, and a control's
  edge at 3:1, in both themes, computed from `tokens.css`.

A commit carries the tests for the code it changes, so every commit passes the check on its own.
