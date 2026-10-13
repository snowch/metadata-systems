# Chapter 27: Build the query layer

A working note. Written on 13 October 2026 with Chapters 24 to 26 and 28
(`notebook/chapter_27.py`).

## What the chapter does

Over Chapter 26's graph (the shop's version) for the week with the returns desk, `source` and
Chapter 13's failed night, the reader:

- writes `downstream(graph, asset)` as a traversal over `next_assets`; 1 of 3 as it stands, 3 of 3
  after; downstream of `orders.jsonl` are `clean_orders`, the copy, `daily_sales` and
  `sales_dashboard`;
- predicts whether the shop's query for stale assets (last written more than 24 hours before Monday
  09:00) lists `sales_dashboard`; it does not: written at 03:00:09 on Monday, showing Saturday 12;
- reads the shop's answers to four other questions, of which only upstream follows the graph, and the
  freshness measure the stale query reads (the dashboard written at 03:00:09, showing Saturday 12);
- writes `owner(asset)`, which must say which of three meanings it gives, then reads every asset
  with each meaning's owner: account 4 of 12, responsible 5, team 1, and 6 with none; and questions
  "The query layer must answer who owns each asset."

## What was built for it

`notebook/shop/query.py`: `graph`, `next_assets`, `previous_assets`, `upstream`, `owners` (each
meaning from its own source; `responsible` from Chapter 4's records, `the data engineer` for
`clean_orders` and `clean_customers` included), `coverage`, `check_downstream`, `check_owner`,
`answers`. `week.py`: the failed
night reads the copy when `source` applies.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `one-step`

- **Role:** inspect
- **Serves:** what does `next_assets` give? One step from `orders.jsonl`.
- **Why now:** the traversal is built on it.

### `downstream-check`

- **Role:** experiment
- **Objective:** the reader builds a traversal and sees one step answer too little.
- **Known before:** Chapter 5's traversal; Chapter 6's `downstream`.
- **Driving question:** what is downstream of each of three assets?
- **The action:** change `downstream`; press **Run below**.
- **Evidence:** 1 of 3, then 3 of 3.
- **Consequence:** the reader owns the traversal the shop's pages used.
- **Predictable:** yes.
- **Gives nothing away:** the page describes the loop, not the code.
- **Not knowing:** fair.
- **Next question:** what do the other questions find in the same week?

### `answers`

- **Role:** experiment (its prediction: is the dashboard stale?)
- **Objective:** the reader finds that a query by write time calls the dashboard recent while it
  shows Saturday.
- **Known before:** Chapter 13's two freshnesses and its failed night.
- **Driving question:** will the query list `sales_dashboard`?
- **The action:** write the prediction; read the four answers.
- **Evidence:** `daily_sales` and `returns`, not the dashboard; then the freshness measure (an
  instrument shown after the reader's answer) with its last written time and latest day.
- **Consequence:** a query answers the question it was written for.
- **Predictable:** yes, from Chapter 13.
- **Gives nothing away:** the cell asks yes or no.
- **Not knowing:** fair.
- **Next question:** whose owner does the query give?

### `owners` and `owner-check`

- **Role:** inspect, then experiment: the three meanings, framed as the questions they answer, and the
  reader's `owner`, which fails until it names its meaning.

### `coverage`

- **Role:** inspect (completes the requirement).
- **Serves:** does any meaning give an owner for each asset? Every asset of the platform with each
  meaning's owner: none covers all 12, and 6 have no owner at all.
- **Why now:** the check tested `daily_sales` only; the requirement says "each asset".

## Requirements

The plan's: the query layer must answer who owns each asset (`docs/plan.md`, requirements table).
Readings: the account (Chapter 2), the person responsible (Chapter 4), the team (Chapter 21). The
check passes any, as long as the query names its meaning; `coverage` shows that no
meaning's source covers every asset. The figure that questions it is the
free-text cell after the box.

## Originality

The obvious examples are a catalogue's search page and its API for lineage. This chapter's queries
are written over the shop's own graph, its failed night and its three sources of an owner, and the
check is the shop's.

## What the prose process caught

First draft from brief P27 (`part-6/drafts/P27.md`); the review's changes through brief P27-rev
(`part-6/briefs/P27-rev.md`, draft `part-6/drafts/P27-rev.md`). The first drafts' slips across Part
VI were labels where a statement belonged ("The question:", "Result 1"), single quotes round a
requirement, two joins that left "the next cell" pointing at the wrong cell, *job* where the six
programs were meant, and a total whose scope was missing; each was fixed with the fewest words. In the revision, two of the reader's question cells began with a small
letter; capitalised.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 12 findings (`review/verdicts.md`): 5 upheld, 6 partly, 1 rejected.
Read whole again after the fixes (`review/chapter_27-after-review.md`). Acted on:

- "met by any of them" was false for each asset: `coverage` lists every asset, and Chapter 4's
  `responsible` lines for `clean_orders` and `clean_customers` were missing from the engine;
- Chapter 14 is quality: downstream is Chapters 6 and 16; "since Part III" is gone;
- the page and notes say which questions follow the graph (one) and which read other records;
- the freshness measure is shown before the prose that reads it, and the redraw is in the result,
  not the setup; the stale query covers the assets the shop measures;
- the owner meanings are framed as questions; the unsupported "team that still exists" is gone;
- the page says what `downstream` returns and that the graph is built with the shop's `add`;
- the reality note says what Chapter 23 found for a traversal to the end, and that `downstream`
  ignores the edges' times.

Rejected, with the sceptic: catching the learner's exceptions, the map's caption, and the part's
shared requirement opener.

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
24 to 28"): from Chapter 26's link, 11 files, 0.32 MB, in a new tab; Run all 8.3 to 8.6 s; peak memory 391 to 404 MB alone, 615 MB with Chapter 26
open; no error output, no console error. The browser test (`notebook/jupyterlite/smoke.mjs`) types the
references into each cell and reads the checks' lines.

## Known gaps

- The team sheet names a team for `daily_sales` only; the chapter does not say whether a sheet with
  more rows would change the answer.
