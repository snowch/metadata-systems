# Chapter 28: Build the metadata interface

A working note. Written on 13 October 2026 with Chapters 24 to 27 (`notebook/chapter_28.py`). It
closes Part VI.

## What the chapter does

The reader draws a page for `daily_sales` from the pieces Chapters 24 to 27 built (the shop's
versions), for Chapter 27's week:

- reads the program that writes `daily_sales` and the 41 runs in the file;
- predicts whether a run history built from what each run wrote includes Monday's failed run; finds
  6 runs, without it; builds it from the programs that write the asset; 7 runs, the FAIL among them;
- chooses the page's sections from seven, and sees the page name the ones it leaves out;
- questions "The asset page must show everything about an asset."

## What was built for it

`notebook/shop/interface.py`: `SECTIONS`, `runs`, `writers`, each section's rows, `Page`, `page`,
`check`.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `writers-and-runs`

- **Role:** inspect
- **Serves:** what can a run history be built from? The writers of `daily_sales`, and the number of
  runs in the file.
- **Why now:** the two ways of building it use these.

### `run-history`

- **Role:** experiment
- **Objective:** the reader discovers that a run that failed wrote nothing, so a history built from
  what runs wrote hides it.
- **Known before:** Chapter 13's failed night; Chapter 27's week.
- **Driving question:** will the history include Monday's run?
- **The action:** write the prediction; read the check; change `run_history`; press **Run below**.
- **Evidence:** 6 runs as it stands; 7, the FAIL among them, after. The check asks for each run of the
  programs that write the asset, once: a history of the FAIL alone, or of each run twice, fails.
- **Consequence:** a view must be built from the record that holds what it shows.
- **Predictable:** partly.
- **Gives nothing away:** the cell asks yes or no.
- **Not knowing:** fair.
- **Next question:** what should the page show?

### `page`

- **Role:** instrument, with a question in front of it (Jo Marsh asks why `daily_sales` ends on
  Saturday 12); the reader chooses its sections, and the requirement then reads it. A name it cannot
  draw is listed as such, not as left out (tested).

## Requirements

"The asset page must show everything about an asset." Readings: every section the shop can draw;
what a person asking about the asset needs; the whole history. The first is met by all seven names
and shows nothing more; the second by the sections the question needs; the third by no list of
sections. The page names the sections it leaves out, not what a drawn section leaves out.
The figure that questions it is the free-text cell after the box.

## Originality

The obvious examples are a catalogue product's asset page and its screenshots. This page is drawn
from the shop's own pieces, its sections are named in a list the reader edits, and the failed run is
the shop's.

## What the prose process caught

First draft from brief P28 (`part-6/drafts/P28.md`); the review's changes through brief P28-rev
(`part-6/briefs/P28-rev.md`, draft `part-6/drafts/P28-rev.md`). The first drafts' slips across Part
VI were labels where a statement belonged ("The question:", "Result 1"), single quotes round a
requirement, two joins that left "the next cell" pointing at the wrong cell, *job* where the six
programs were meant, and a total whose scope was missing; each was fixed with the fewest words.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 15 findings (`review/verdicts.md`): 3 upheld, 9 partly, 3 rejected.
Read whole again after the fixes (`review/chapter_28-after-review.md`). Acted on:

- the check passed a history of the failed run alone, or of each run twice: it now asks for each
  run once, and says which are missing or repeated; "1 runs" is gone;
- a mistyped section was listed as left out; the page names it as one it cannot draw; the unused
  sections test is gone from `check`;
- the page's last line is described as what it is (the names not drawn), not as meeting the
  requirement; each reading says what meets it;
- the sections' sources are named accurately, and the earlier pieces are said once to be the shop's;
- a question (Jo Marsh's) stands in front of the sections cell;
- the history's completeness depends on the graph's edges, and the closing says so;
- the reality note says the failed run's empty outputs are the shop's choice under the specification.

Rejected, with the sceptic: the prediction's guessability (it can be reasoned from Chapters 8 and
13), the map, and the warning's numbers (now measured and pinned for Chapters 24 to 28).

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
24 to 28"): from Chapter 27's link, 11 files, 0.31 MB, in a new tab; Run all 8.6 to 9.0 s; peak memory 393 to 397 MB alone, 615 MB with Chapter 27
open; no error output, no console error. The browser test (`notebook/jupyterlite/smoke.mjs`) types the
references into each cell and reads the checks' lines.

## Known gaps

- A program whose every run failed would not appear in `writers`, so its runs would be missing from
  the history; the shop's week has none.
