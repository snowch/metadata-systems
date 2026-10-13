# Chapter 26: Build the lineage graph

A working note. Written on 13 October 2026 with Chapters 24, 25, 27 and 28
(`notebook/chapter_26.py`).

## What the chapter does

The reader builds the lineage graph one stored event at a time, from the collector's file (82
events, the week with the returns desk, the `source` change and Part V's faults):

- writes `add(edges, event)`, which keeps each edge's runs and first and last times;
- predicts what the graph shows at 09:00 on Thursday 10 for `build_daily_sales` writing
  `daily_sales`, with `add` taking each arriving event's time as the last; finds Wednesday's, because
  Wednesday's COMPLETE arrived late; takes the earlier and the later of two times; 3 of 3;
- reads the edges of `build_daily_sales`: `clean_orders` in 5 runs, last on Saturday 12; the copy in
  2, Sunday and Monday;
- questions "Lineage must show the platform as it is now."

## What was built for it

`notebook/shop/lineage_graph.py`: `edges_of`, `stored` (the collector's file with the shop's
pieces), `build` with a save and load at the restart, `table`, `check`, `now`.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `late-last-time`

- **Role:** experiment
- **Objective:** the reader discovers that a graph updated in arrival order lets a late event make an
  edge look older, and that keeping the later of two times fixes it. The same check shows the graph
  saved as lines and loaded after the restart keeps its edges, runs and times.
- **Known before:** Chapter 20's late COMPLETE.
- **Driving question:** at 09:00 on Thursday 10, when does the graph say `daily_sales` was last
  written?
- **The action:** write the prediction; read the check; change `add`; press **Run below**.
- **Why the action:** the reader's own `add` sets the time.
- **Evidence:** Wednesday 9's time as `add` stands; 3 of 3 after.
- **Consequence:** an edge's time must come from the events, compared, not from their order.
- **Predictable:** yes, from Chapter 20.
- **Gives nothing away:** the cell asks for a time.
- **Not knowing:** fair.
- **Next question:** which edges does the platform have now?

### `edges-of-build-daily-sales`

- **Role:** inspect
- **Serves:** what does the graph hold about Sunday's change of input? The three edges with their runs
  and times, `START`s' times included.
- **Why now:** the requirement's readings are read off these times.

### `now`

- **Role:** experiment (completes the requirement): each edge of `build_daily_sales` and
  `record_return` under three readings of "now"; for `record_return`, idle since Friday, the latest
  run and the window disagree.

## Requirements

"Lineage must show the platform as it is now." Readings: each program's latest run's edges; every
edge ever seen; edges seen in the last 2 days. `clean_orders` is in "ever" only; `record_return`'s last run's edges
are in its latest run and not in the window. Chapter 9 asked the same of edges with no times. Time-stamped edges
answer all three; a graph with no times answers only "ever". The figure that questions it is the
free-text cell after the box.

## Originality

The obvious example is a lineage tool's documentation of a graph that shows the latest version of
each job. This chapter's graph is built one event at a time from the shop's own collector, with the
shop's late event, and the three readings are read from its own times.

## What the prose process caught

First draft from brief P26 (`part-6/drafts/P26.md`); the review's changes through brief P26-rev
(`part-6/briefs/P26-rev.md`, draft `part-6/drafts/P26-rev.md`). The first drafts' slips across Part
VI were labels where a statement belonged ("The question:", "Result 1"), single quotes round a
requirement, two joins that left "the next cell" pointing at the wrong cell, *job* where the six
programs were meant, and a total whose scope was missing; each was fixed with the fewest words.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 14 findings (`review/verdicts.md`): 5 upheld, 6 partly, 3 rejected.
Read whole again after the fixes (`review/chapter_26-after-review.md`). Acted on:

- the page describes the tests in the order the check prints them;
- the 82 events are Chapter 25's collector over a week with the analyst's copy job (14 more events);
- the match with Chapter 9 is with its way of building edges, over this file, which has no cut line
  (7 runs, not Chapter 9's 6); the check's lines say so too;
- "now" is tied to Chapter 9's "current", and a second program, idle since Friday, shows the latest
  run and the window disagree (`now` takes the programs; tested);
- save and load are explained before the check (lines per edge, after Chapter 25's restart);
- the week never tests the first time, and the page says so;
- the graph's times are event times; arrival order only orders the updates;
- the closing says what the graph could not show, and the reality note says what differs.

Rejected, with the sceptic: hiding the check's output behind a control (a Part VI convention),
renaming "program", and the phone width of `add`'s long line.

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
24 to 28"): from Chapter 25's link, 11 files, 0.32 MB, in a new tab; Run all 8.1 to 8.5 s; peak memory 394 to 400 MB alone, 611 MB with Chapter 25
open; no error output, no console error. The browser test (`notebook/jupyterlite/smoke.mjs`) types the
references into each cell and reads the checks' lines.

## Known gaps

- No late event creates an edge in the shop's week, so the first time's rule is stated, not shown.
