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
shows before anything runs; the setup cells at the foot of the file move to the top. A new
chapter is added to `CHAPTERS` in `build_ipynb.py`, in `notebook/tests/test_words.py`, and to
`NOTEBOOKS` in `content/plan/notebooks.ts`, which the front page reads.

- The first cell links back to the contents (the absolute address of the front page: a relative
  link in JupyterLite opens a file of the site) and on to the next chapter by its notebook's
  name, then gives the heading `# Chapter N: {title}`, the plan's title, and the objectives.
- Then two boxes (`mo.callout`, which the build turns into a box the course's stylesheet in
  `notebook/buttons/style/` draws): the warning about the download and the memory a phone has
  (`kind="warn"`), then the steps for running and saving the page (`kind="info"`). A blue box of
  that kind, with its "touch_app" icon, means something the reader does: in every chapter, to
  decide before reading on ("Before you read on, decide …") or before opening the readings of a
  requirement, which sit in a closed `<details>` block ("Readings of …"); Chapter 2 also boxes
  what it asks the reader to look for, compare or open. No code cell holds answers that nothing
  reads: a prediction is decided, not typed into a string. The paragraphs that state the result
  a reader has just run sit in a closed block, "The printed result, explained", so the result is
  not in view while they decide; an instruction ("Change …, select the cell and press **Run
  below**") and a lead into the next cell stay outside it, and the result of a rerun gets a block
  of its own. A block cannot span two cells, so a figure that belongs with a result is written into
  its Markdown cell as `<!-- figure: figures.figure(...) -->`, which the build draws there
  (Change 1 in Chapter 2). The requirement a
  chapter questions has a box of its own (`kind="neutral"`, purple, with the "rule" icon). The only
  other box is a box of findings
  (`kind="success"`), which Chapter 2 sets after each of its three investigations: what the
  evidence established beside what it did not, as two paragraphs in `<div class="ms-found">` and
  `<div class="ms-open">`, side by side on a wide screen. It goes only where a reader needs the
  line drawn, never after every cell. Otherwise the story is broken up by its figures, headings
  and cells.
- A chapter may close with a short check of the kind Chapter 2 has: a scenario, then each answer as
  `<details class="ms-choice"><summary>A. ...</summary> feedback </details>` in a Markdown cell.
  It needs no code and no widget; every answer looks the same until opened, a wrong one says why
  and asks for another, and the one that holds ends with the point in a `<div class="ms-takeaway">`.
- A table shows each date with its weekday after it (`2026-09-10 (Thu)`): the engine's tables do
  this for every date that stands as a word, so a chapter's text may name the shop's days freely.
  Printed raw data (a file's lines, an event's JSON) stays as the system holds it; where the text
  names a day beside it, give the date too.
- A link from the opening to a section is the heading's text with its spaces as hyphens
  (`[Test an explanation](#3.-Test-an-explanation)`): JupyterLite scrolls the notebook to it, even
  when the heading is far below; the smoke test follows two of Chapter 2's.
- Every section is a `## ` heading that names its subject, never the reader's activity.
- The last section closes with what the chapter's experiments showed and could not show, then
  reflective questions (Chapter 2 has its check in their place), and names the next chapter; the
  last cell repeats the links.
- A query in a code cell that the reader sees is written over several lines, one clause per line
  (SELECT, FROM, WHERE, GROUP BY, ORDER BY), in a triple-quoted string, so a phone shows it whole
  without scrolling sideways. A query of one short clause, such as `SELECT * FROM daily_sales`,
  stays on one line.
- The page tells the learner to press **Run all**, **Run below** and **Save**, the row of buttons
  `notebook/buttons/` puts above the cells; the tests hold the page to the buttons it has.

The chapter's notes, `docs/notes/chapter-NN.md`, are written in the same commit, with a section
"Figures", a section "Requirements" and a section "Originality" (below).

## Answers used by later chapters

Use a Markdown cell with `<!-- answer: guesses -->` for Chapter 1's table guesses,
`<!-- answer: daily_sales -->` or `<!-- answer: clean_orders -->` for the comparisons in
Chapter 2, and `<!-- answer: report -->` for its reply to the head of the shop. The notebook
builder removes the marker and stores its value in the cell's `ms.answer` metadata.
`notebook/buttons/answers.js` mounts labelled text fields on that cell widget, outside its
Markdown renderer. These fields do not execute Python or become notebook source.

Each response has a stable exercise ID and its own `ms:metadata-systems:answers:v1:` browser
storage key. Do not derive IDs from cell positions, headings or published notebook versions.
Writes happen on each input event, with explicit failure feedback and an in-memory draft for
export. Chapter 2 displays the Chapter 1 answers read-only and saves revisions separately.
An explicit reset stores an empty value so recovery from an old notebook cannot undo the reset.
Import restores missing or empty answers and preserves nonempty current answers. Export includes
unsaved in-memory drafts. Both use a course-identified, versioned JSON document.

On opening either chapter, recovery reads old `guesses` strings from Chapter 1 and its saved
copies, newest first, without executing Python. Existing answer-store entries take precedence.
Keep the notebook's normal Save/update handling intact: it still protects changes to code cells.
The answer text is separate and survives published notebook replacement.

Run `node --test notebook/buttons/answers.test.mjs` for storage and recovery behaviour.
`notebook/jupyterlite/answer-smoke.mjs`, called by the normal smoke suite, exercises typing,
refresh, Run all, chapter navigation, revisions, export/import, failed storage, reset and a
published-notebook update in the built JupyterLite site. UI words live in `answer-words.js` and
are checked by the prose regression script as well as the editorial pass.

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

- **State the requirement in words**, as somebody at the shop would write it, in one sentence that
  quotes it, in a box of its own: a callout of the kind `"neutral"`, which the build draws as the
  requirement's box, in a colour no other box uses and with an icon of its own (Material Symbols'
  "rule"; `docs/sources.md`). One per chapter, where the requirement arrives;
  a heading straight above it names the section's subject and does not repeat the requirement's
  words. `notebook/tests/test_jupyterlite.py` and `smoke.mjs` check that each chapter from 2 has
  one.
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

## Code the reader writes (Part VI on)

A piece the reader writes is short enough for a phone: a few lines at most. Its cell starts as a
version that runs and answers wrong, never one that fails to run, and the cell below it calls the
shop's check, which prints one line per test with what the reader's code gave and, where it differs,
what was expected. The engine keeps the starting version and a reference for every piece (`STUBS`
and `REFERENCE` in the chapter's module); `notebook/tests/test_engine.py` holds each starting
version failing its check and each reference passing it, and `notebook/jupyterlite/smoke.mjs` types
the reference in and finds the check passing. The page says what the code must do, never the code
itself, and says what the check shows before and after.

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
  hidden, the row of buttons there and 44 pixels tall, with arrows to the chapters either side that
  open in a new tab and a row that fits 360 pixels, Run all and Run below running every cell with no
  error and keeping the reader's place.

A commit carries the tests for the code it changes, so every commit passes the check on its own.

## Python startup feedback

`notebook/buttons/startup.js` tracks startup separately from run progress and chapter-update
notices. The row below the notebook controls shows loading, chapter preparation, and readiness.
It uses an indeterminate indicator because the worker's kernel interface exposes no download
byte totals. After ten seconds it adds slow-connection guidance; after two minutes it offers
Retry while allowing the current attempt to finish. A rejected startup, dead kernel, or failed
setup reply shows an error immediately.

Retry replaces the Python worker within the existing notebook session and shuts down the old
worker. It preserves the document and answer controls; it does not reload the page. An early
Run all waits for setup to succeed. A failed or superseded startup releases that queued run.
Closing the panel cancels timers and listeners.

`startup.test.mjs` checks timing, cancellation and stale callbacks. `startup-smoke.mjs`, called by
the notebook browser suite, delays the real WebAssembly download, breaks the course-package
download, and checks retry, queued runs, retained edits, answer fields and a narrow dark view.

## Offline course

Chapter 1b is a comparison view generated from Chapter 1's source, with fixed prose, per-example
Run/Reset controls and synchronous code drafts. Its words for the replacement running/saving
instructions live in `notebook/jupyterlite/reader.json`; the examples and all other prose remain
in Chapter 1. See `docs/notes/chapter-01b.md` for the persistence contract. Run
`node notebook/jupyterlite/reader-smoke.mjs SITE_DIR` to check the reading view against a built
JupyterLite site. The normal notebook browser suite and the deployment also run this check.

The contents page offers an explicit full-course download with the size calculated from the
assembled site. It includes the front page, all published notebooks, Python and all bundled
packages. No first visit or successful Python startup alone is called offline-ready. A user must
finish the download while connected, then can close the browser and return without a network.
Browser storage can be evicted; the UI checks that all files are still present before reporting
readiness. Removing downloaded files does not remove answers, notebook saves or another course's
data. The browser can still remove site data, so the UI recommends exporting answers.

After building both apps and adding redirects, run `node scripts/build-offline.mjs SITE_DIR`.
It writes `offline-manifest.json` with a release digest, file sizes and SHA-256 hashes, omitting
source maps. The client validates downloads before storing them, resumes incomplete downloads
and reuses unchanged files during updates. A single metadata write switches to a complete new
version. An interrupted update leaves the previous complete version active. The offline copy
remains on that version while an update is prepared; only an explicit Restart to update selects the new release.
Other open chapters stay on their pinned release until the reader restarts them. No page reload is forced and learner data is never deleted for an
update. A cross-tab Web Lock serialises download/removal operations.

`offline/worker.js` serves the selected snapshot under the course's own URL scope, including
notebook navigation query strings and package checksum URLs. It imports the pinned JupyterLite
worker for its filesystem and stdin protocol. `notebook/buttons/service-worker.js` uses
JupyterLite's manager but disables its origin-wide unregister-on-version-change method; the
browser updates registrations normally. The download client migrates only this course's old
JupyterLite registration. Other GitHub Pages projects on the origin keep their workers and caches.

`node scripts/offline-smoke.mjs SITE_DIR` tests the full production build under a project subpath.
It cancels and resumes downloads, restarts a persistent browser with an empty HTTP cache and no
network, opens previously unvisited notebooks, runs Python, checks answer persistence, simulates
a failed and successful release update, rejects a checksum mismatch, detects an evicted asset,
and removes the download without removing answers, saved notebooks or unrelated workers and
caches. Both the Notebooks and deploy workflows run it;
the deploy verifies the exact artifact it publishes.


## SQL layout

Keep short lookups compact. For longer queries, put each selected expression on its own line,
align the outer clauses, and use four spaces for nested expressions and subqueries. Put `CASE`,
its branches and `END` on separate lines. Break long conditions at `AND` or `OR` without changing
their grouping. Do not add horizontal padding merely because SQL is inside a Python string:
check the exported notebook, whose code has the marimo function's four spaces removed.

Apply the same layout to SQL shown from the shop's repository. Formatting that program text
changes its code-version hash, so recompute any versions quoted in prose and pinned by tests.
Check SQL tokens as well as execution results; do not change aliases, parameters, expressions,
filters, column order or row order while improving layout.


## Reference tables in the reader

Chapter 2's header offers four named query results through **Tables**. The matching permanent
reader IDs and labels are in `notebook/buttons/table-words.json`; the notebook build validates
them and adds the list to its metadata. A Markdown link such as
`[View daily revenue comparison](#ms-table-cell-16)` opens the same result beside an explanation.

`notebook/buttons/tables.js` opens a native modal dialog over the current reading position. It
copies table text and structure from Jupyter's rendered output, without copying active HTML or
moving the original output. Opening the chooser does not execute code. **Run query** uses the
current editor content and the existing Python session. A changed query, or a changed or rerun
earlier example, marks its result as out of date. Closing the dialog restores focus and the
reading position. Results are not persisted; saved code and exercise answers keep their existing
storage keys.

`tables-smoke.mjs`, called by the reader suite, runs the real queries, checks outdated and empty
states, errors and recovery, reset, busy execution, nearby links and mobile layout.

## Permanent reader identities

Every code example has a `# reader-id: ...` marker on its `@app.cell`
decorator. This is a permanent browser save key, not a position in the notebook. Preserve it when
editing or moving the example. Give a new example a unique new ID; never copy another example's
marker or reuse an ID from a deleted example. Keep the marker outside the function so readers do
not see this implementation detail. Chapter 1 retains its six named IDs on the same kind of marker.

The initial IDs deliberately retain the existing `cell-NN` values to preserve current drafts.
The notebook's own positional cell ID may change; the reader ID must not. The build rejects
missing or duplicate reader IDs, and its regression tests insert prose and code before an example
to verify that its save key stays unchanged.

## App status and release identity

Issue #2 replaces the separate home offline card and notebook release line with a shared native
App status dialog (`offline/status.js`), mounted by a React adapter on the contents and a Lumino
adapter on notebooks. Learner words are drafted in `offline/status-words.json`. Version checking
and offline completeness have separate states. Only a successful network-only, validated,
time-limited check can report Up to date. Focus/reconnect/visibility checks are throttled;
visible pages repeat checks every minute. No asset download starts from a release check.

The complete-course assembly writes identical `release.json` and `jupyterlite/release.json`:
`{schema: 1, commit: <40 hex source commit>, build: <20 hex content digest>}`. `build` hashes the
sorted assembled runtime files and course worker before inserting `ms-build` HTML tags. Existing
build tags are stripped before hashing, so repeating assembly is deterministic. The loaded
identity comes only from HTML meta tags, never fetched metadata. The standalone notebook build
also emits this schema for its own artifact; complete-course assembly replaces it with the
whole-course identity. A standalone build is not a full-course offline artifact.

The offline manifest retains its existing 20-hex `version` and includes `release`. Its size is
the sum of exact bytes, including Python, wheels, chapters, shell and fonts. Resume validates
stored bytes before reusing them. A prepared update writes a `pending` snapshot without changing
the selected snapshot. Restart activates the scoped worker, verifies the pending copy, selects
it atomically and reloads the same URL. Other windows receive a pending notice, never a forced
reload. Existing clients retain persistent release pins in the course metadata cache, and
missing pinned assets fail safely instead of falling through to a different published version.
Older snapshots remain until explicit removal, so open windows can keep their release.
Removal touches only this course's offline caches and preserves notebook and answer storage.

Existing saved manifests remain readable; unchanged verified assets can be reused into the new
snapshot. Worker registrations outside this course are untouched. The old notebook-only worker
is migrated only when a full course download requires the root scope. Restart guards check
running Python, failed saves and text composition again immediately before reload. There is no
automatic restart on controller change.

Verification: `scripts/offline-smoke.mjs` tests real assembled releases and a persistent browser
with an empty HTTP cache. `notebook/jupyterlite/release-smoke.mjs` covers malformed/failed checks,
loaded identity, independent states, focus and narrow layout. Production byte totals, exact
commands, review evidence and screenshots belong in the PR's delivery record.
