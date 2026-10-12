# Writing a chapter

How a chapter is made, from the engine to the review. A chapter is a Jupyter notebook the learner
runs in the browser. Chapter 2, `notebook/chapter_02.py`, is the worked example; copy its shape.

Until 11 October 2026 a chapter was also a page of the course, written as data for the learning
platform's lesson format and drawn by figures in TypeScript. The author kept only the notebooks
(`docs/plan.md`, "11 October 2026: only the notebooks"); the notes of Chapters 1 and 2 still
describe the pages' figures, as a record of how the chapters were designed.

## The engine first

A chapter starts in `notebook/shop`, not in its prose. Decide what the learner must discover, then
make the engine compute it: a figure shows what the engine computes, and a prediction's answer is
what a cell prints when the learner runs it. If the engine cannot compute what a figure needs, the
engine gains it, with a test in `notebook/tests`, before the figure exists. `docs/lab.md` says what
the engine models and what it does not. The page never names the engine (`CLAUDE.md`, "No lab on
the page").

## A chapter is a source file

A chapter is `notebook/chapter_NN.py`, a Python file of cells in marimo's file format, which keeps
the chapter diffable and lets the tests read every sentence. `notebook/jupyterlite/build_ipynb.py`
turns it into `chapter_NN.ipynb`, cell by cell, and stops on anything it does not know how to
carry over: a markdown cell (`mo.md`) is a markdown cell; a figure (`mo.Html`, from
`notebook/shop/figures.py`) is drawn by the build from the shop's week into a Markdown cell, so it
shows before anything runs; a control (`mo.ui.dropdown`,
`mo.ui.text_area`) is an ipywidget; the setup cells at the foot of the file move to the top. A new
chapter is added to `CHAPTERS` in `build_ipynb.py`, in `notebook/tests/test_words.py`, and to
`NOTEBOOKS` in `content/plan/notebooks.ts`, which the front page reads.

- The first cell links back to the contents (the absolute address of the front page: a relative
  link in JupyterLite opens a file of the site) and on to the next chapter by its notebook's
  name, then gives the heading `# Chapter N: {title}`, the plan's title, and the objectives.
- Then two boxes (`mo.callout`, which the build turns into a box the course's stylesheet in
  `notebook/buttons/style/` draws): the warning about the download and the memory a phone has
  (`kind="warn"`), then the steps for running and saving the page (`kind="info"`). Nothing else
  in a chapter is a box: the story is broken up by its figures, headings and cells.
- Every section is a `## ` heading that names its subject, never the reader's activity.
- The last section closes with what the chapter's experiments showed and could not show, then
  reflective questions, and names the next chapter; the last cell repeats the links.
- A query in a code cell that the reader sees is written over several lines, one clause per line
  (SELECT, FROM, WHERE, GROUP BY, ORDER BY), in a triple-quoted string, so a phone shows it whole
  without scrolling sideways. A query of one short clause, such as `SELECT * FROM daily_sales`,
  stays on one line.
- The page tells the learner to press **Run all**, **Run below** and **Save**, the row of buttons
  `notebook/buttons/` puts above the cells; the tests hold the page to the buttons it has.

The chapter's notes, `docs/notes/chapter-NN.md`, are written in the same commit, with a section
"Figures", a section "Requirements" and a section "Originality" (below).

## How a figure is drawn

A figure the reader does not change is drawn when the site is built, into a Markdown cell, so it
shows before Python has loaded. A Markdown cell drops `<style>` and inline `<svg>`, so:

- a figure of names and values (the platform, the dashboard) is HTML with class names only, styled
  by `notebook/buttons/style/index.css` in the theme's colours, and laid out to restack on a phone;
- a drawing (the week) is an SVG image in a base64 data URI, drawn at a phone's width with text
  that shows at 11 pixels or more in a 360-pixel phone's column, with its own colours for the light
  and dark themes (an image cannot take the page's) and its one-sentence description as `alt`.

A figure that changes with what the reader does stays a code cell, and its output follows the same
rules. The smoke test checks that each chapter's figures show before anything runs, and the size
of the week's words at 360 pixels.

## A diagram carries what prose would make the learner hold

Where a passage would ask the learner to keep a date, a set of systems, a count, a sequence of
nights or their own place in an investigation in mind, a figure carries it, and the prose says
only what the next question needs (`CLAUDE.md`, "Every figure is computed from the shop"). Such
a figure is a diagram with one job, named in its block under "Figures": the platform's
architecture, its assets, time, a flow, or where the learner stands. It is still computed from
the shop's data, and it still shows only what the learner has been told or has built. A chapter's
opening sets up the smallest model its first question needs, and adds structure when the
investigation makes it relevant.

A mechanism is explained from the learner's side first (`CLAUDE.md`, "Interaction is the
explanation"): what the learner does and what happens when they do, then how it is built. In a
notebook the learner asks by running a cell, or by changing one and pressing Run below; the page
says which cells to change and what to look for in what they print.

## Experiments, instruments and references

Every figure's block in the notes says what it asks of the learner (`CLAUDE.md`, "Experiments,
instruments and explanations"): nothing, for a diagram or a figure of the shop's data; a
commitment, for an experiment. A cell the learner changes and runs again is an experiment when the
page asks for an expectation first.

- `experiment`: the learner commits (writes down a prediction, chooses a change, edits a query),
  runs the cell, and the output answers. Prefer it.
- `inspect`: an instrument the learner examines for evidence, such as a cell that lists what
  storage records. Never present it as the activity: put a question in front of it and say what to
  look for.
- `reference`: what the page shows to hold in mind, such as the platform's diagram. It asks
  nothing.

These are a lens for the notes, never labels on the page. On the page, "figure" names a drawing
(a diagram or a figure of the shop's data) and nothing else: a number is a total, a value or a count.

A figure's block in the chapter's notes, under "Figures", in the page's order: a heading with its
name, its role, and for an experiment twelve answers, each under its own label.

```
### `the-thursday-cell`

- **Role:** experiment
- **Objective:** what the learner should understand, discover or be able to do afterwards,
  never what the figure displays.
- **Known before:** what is on the page above it.
- **Driving question:** the question, hypothesis or decision that drives it.
- **The action:** what the learner does.
- **Why the action:** why the learner must act to learn it, and not only look.
- **Evidence:** what the action produces.
- **Consequence:** what they believed before, what the evidence lets them believe after, and what
  a wrong prediction teaches.
- **Predictable:** whether they could reason to the outcome from what is on the page.
- **Gives nothing away:** why no line above it, and no output in view, carries the explanation.
- **Not knowing:** whether "I can't tell yet" could be the right engineering response.
- **Next question:** the question the result raises, and where the chapter takes it.
- **An experiment:** why it is an experiment, and not an instrument or a reference.
```

An instrument or a reference answers two, **Serves** and **Why now**. Review, not a test, holds the
notes to these blocks.

## Predictions

A prediction is an experiment, built around what the learner should learn (`CLAUDE.md`,
"Interaction is the explanation").

- **State the objective first.** If it cannot be said in a sentence, redesign the exercise.
- **Ask for an observable result**, and the belief it reflects. A prediction never says why the
  result will be what it is: that is the explanation, and it comes after the evidence.
- **Establish the effect before asking for its cause.** "Is there a difference?" comes before
  "where is it?", "what could explain it?" and "which explanation fits?".
- **Prefer independent evidence**: a total the learner could add up, rows they could read, not
  a failure inside a job they cannot see.
- **"I can't tell yet" is an answer** where nothing on the page settles the question.
- **A count is asked as what it means.** None, one, or more than one.
- **The output answers, and only after the learner runs it.** A notebook shows a cell's output
  once the cell has run; a page that prints the answer in a cell above the question gives it
  away, and Run all runs every cell. Put the question before the cell that answers it, and say
  in the prose to write the expectation down before running on.

## Requirements

Some exercises question a requirement instead of predicting a result (`CLAUDE.md`, "Question the
requirement"). Look for one in every chapter: `docs/plan.md` lists a candidate for each.

- **State the requirement in words**, as somebody at the shop would write it.
- **List what it could be asking**, each as a question, and what each question needs recorded.
  Every reading must be one a reasonable engineer could hold.
- **Let the learner commit first**, then show the readings, then what the platform records.
- **Say which readings the record answers**, and whether the requirement is met as written, and
  under which meanings.

The chapter's notes get a section, "Requirements", that names the exercise and walks the five
things `CLAUDE.md` keeps apart; a chapter with no requirement to question says why under the same
heading. `notebook/tests/test_notes.py` fails a written chapter whose notes lack the section.

## Originality

The notes' section "Originality" names the obvious textbook or vendor example for the chapter's
topic and says how this chapter's example differs (`CLAUDE.md`, "Originality and copyright").
`notebook/tests/test_notes.py` fails a written chapter whose notes lack it.

## The prose process

`CLAUDE.md` states the rule: every string a learner reads is drafted by a Haiku subagent from a
brief of facts and checked by the managing model for facts only. For a chapter:

1. Write the fact sheet, `docs/notes/chapter-NN/facts.md`, every number read off the engine, with
   the chapter's working words (each with one meaning on the page) and the words it must not use.
2. Write one brief per group of sections (`briefs/`), each a numbered list of facts per string,
   with the keys the drafts come back under. Scan the briefs for banned words before they go out.
3. Run the drafts in parallel. Check facts only: a dropped fact gets the fewest words that carry
   it; a wrong fact goes back with a note; nothing is rewritten. Record what the check caught in
   the chapter's note.
4. Place the strings, then read the whole chapter in the built notebook, start to finish, after
   Run all, and again after each change a cell asks for.
5. Review: a reader on another model, then an independent sceptic on each finding, then fixes:
   code first, fact briefs for wording second, then one more read.

## What the tests hold a chapter to

`npm run check` is exactly what CI's Check runs; the Notebooks workflow builds the site and drives
it.

- `notebook/tests/test_engine.py`: the engine's week, its changes and its inference.
- `notebook/tests/test_words.py`: every number and sentence the notebook states, read off the
  engine; the term gate against the plan; the filler check and the prohibited phrases; no em
  dash; the links between chapters and back to the contents; the closing names the next chapter;
  only the buttons the page has.
- `notebook/tests/test_notes.py`: the notes' "Requirements" and "Originality" sections.
- `notebook/tests/test_jupyterlite.py`: the texts name every button of the row and no other
  control, the build adds the row to the site, and each chapter's warning states what was
  measured.
- `content/plan/notebooks.test.ts` and `plan.test.ts`: the plan against `docs/plan.md`, and each
  notebook headed with its chapter's title.
- `notebook/jupyterlite/smoke.mjs`, as a phone, in the Notebooks workflow: the menu bar and toolbar
  hidden, the row of buttons there and 44 pixels tall, Run all and Run below running every cell
  with no error and keeping the reader's place.

A commit carries the tests for the code it changes, so every commit passes the check on its own.
