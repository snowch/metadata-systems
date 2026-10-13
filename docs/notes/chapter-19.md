# Chapter 19: Duplicate events

A working note. Written on 12 October 2026 with Chapters 18 and 20 to 23
(`notebook/chapter_19.py`).

## What the chapter does

Chapter 18 ended with an event received twice. The reader:

- predicts whether the lineage doubles when the COMPLETE of Thursday's `build_daily_sales` run
  arrives twice, then builds it: no edge changes, because ingestion merges events into runs by run
  id; the cell shows `build_daily_sales`'s two edges, 7 runs each;
- meets a retry that differs in its time only: the program built the event again when it sent it
  again, and the run now seems to end at 02:30:52, not 02:30:21;
- meets **deduplication** by content, which drops the exact repeat and not the retry, and by run and
  event type, which drops the retry, and sees the run end at 02:30:21 again; and **idempotent**: an
  operation done twice leaves what it leaves done once, here ingesting what the collector received;
- runs the week with a storage notice delivered twice: `record_return` starts twice for one change
  of `r-202`, the table `returns` ends the same, `record_return`'s edges show 6 runs writing
  `returns`, not 5, and 3 reading `r-202.json`, not 2; deduplication drops nothing, because these
  are two runs; `repeated_work` finds them by the object, version and change in
  `shop_objectChange`;
- questions "Ingestion must ignore duplicates."

## What was built for it

`delivery.send` with `lose_ack` and `restamp`; `ingest.dedupe`; the `twice` change;
`delivery.repeated_work`; `ingest.edges_side_by_side`, one job's edges from two weeks in one table.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `repeat-and-graph`

- **Role:** experiment
- **Objective:** the reader discovers that keying runs by their id keeps the graph the same when an
  event repeats.
- **Known before:** Chapter 9's objects stage; Chapter 18's repeat.
- **Driving question:** will the lineage change, and how?
- **The action:** write in a free-text cell; read the cell that sends with the acknowledgement lost,
  compares its graph with the graph of the week received once, and lists `build_daily_sales`'s
  edges.
- **Why the action:** the comparison answers whether; the edges answer how, in run counts the
  reader saw in Chapter 18.
- **Evidence:** 69 events received; `True`; `reads` and `writes` in 7 runs each.
- **Consequence:** an "it doubles" answer meets the run key.
- **Predictable:** yes, from Chapter 9.
- **Gives nothing away:** the cell names no result.
- **Not knowing:** fair.
- **Next question:** what if the repeat is not identical?

### `retry-with-a-new-time`

- **Role:** experiment
- **Objective:** the reader finds a repeat that changes a run's recorded end, and that the key a
  deduplication uses decides whether it is caught.
- **The action:** change `"content"` to `"run"` in the cell that starts `deduped =`, press
  **Run below**; the cell below it ingests what was kept.
- **Evidence:** the run ends at 02:30:52; by content, 0 dropped and the end unchanged; by run and
  type, 1 dropped, and the end is 02:30:21 again.

### `trigger-twice`

- **Role:** experiment
- **Objective:** the reader tells a repeated event from repeated work: two runs that each did the
  work, which no event key merges.
- **Known before:** the returns desk (Chapter 7); `record_return` deletes the return's row and writes
  it again.
- **Driving question:** with the notice of r-202's correction delivered twice, what changes in
  `returns`, and what in the lineage?
- **The action:** write in a free-text cell; read the cells that compare the table, list repeated
  work, set `record_return`'s edges from both weeks side by side, and drop repeats by run.
- **Evidence:** `returns` the same; `repeated_work` lists r-202's version with 2 runs;
  `record_return` with 6 runs writing `returns`, not 5, and 3 reading `r-202.json`, not 2;
  deduplication by run drops 0.
- **Consequence:** the function is idempotent for the table; the lineage holds an extra run.
- **Predictable:** partly.
- **Gives nothing away:** asks what changes, not why; the edges are shown after the commitment.
- **Not knowing:** fair.
- **Next question:** what if events arrive in the wrong order?

## Requirements

"Ingestion must ignore duplicates." Readings: the same event twice; the same run reported twice;
the same work done twice. Each needs a different key: the event's content; the run id and event
type; the object, version and change in `shop_objectChange`. The shop's ingestion drops nothing
itself: the first is met for the graph by ingestion alone; the second is not met unless repeats are
dropped by run first; the third is not met, and neither key of deduplication drops it. The
requirement does not say which. The figure that questions it is the free-text cell after the box.

## Originality

The obvious example is a stream processor's exactly-once tutorial with a deduplication window on a
message id. This chapter uses the shop's own events and one of its own functions, and separates a
repeated event, a repeated event with a new time, and repeated work, each with the key that would
catch it.

## What the prose process caught

Brief Y, draft `part-5/drafts/Y.md`; the review's changes through brief Y-rev, draft
`part-5/drafts/Y-rev.md`. In the revision, Haiku kept the brief's "Result 1," labels; cut. "The
event time of its last terminal event" used Chapter 20's term; it now says the time the event
records.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 16 findings (`review/verdicts.md`): 5 upheld, 8 partly, 3 rejected. Read whole again after the fixes, with each
cell's output (`review/chapter_19-after-review.md`). Acted on:

- the 6 runs, not 5, were stated and never shown; a cell now sets `record_return`'s edges from both
  weeks side by side, with `r-202.json` read in 3 runs, not 2;
- the first prediction asked "how" and showed a boolean; the cell now lists `build_daily_sales`'s
  edges, and the page says what the comparison covers;
- the end time returning to 02:30:21 after deduplication by run was claimed and never shown; a
  cell below the edited one ingests what was kept;
- ingestion merges by run id and takes the end from the latest terminal event, said plainly; the
  "(Chapter 9)" over-attribution is gone; the restamped copy states a wrong `eventTime`;
- the requirement's readings now say which are met, and deduplication is a step applied, not the
  shop's ingestion;
- "the last cells of Chapter 18"; "a program can", not "some programs"; "same content", not "byte for
  byte", for the rule; a reality bullet on `RUNNING` and `OTHER`; plan row 19's readings updated.

Rejected, with the sceptic: moving the requirement earlier (the Part V convention), and an identity
key framework.

## Measured

Locally, 12 October 2026, before the review's changes (`docs/notes/notebook-prototype.md`,
"Chapters 18 to 23"): from Chapter 18's link, 11 files, 0.31 MB, in a new tab; Run all 7.6 to 8.5 s;
peak memory 393 to 402 MB alone, 608 MB with Chapter 18 open; no error output.
Live, 12 October 2026, published at `b15b63a`, opened alone at desktop and phone widths: Run all
10.4 to 11.2 s; peak memory 408 to 411 MB; no error output, no console error. The warning's 9 to 12 seconds and about 400 MB
hold.

## Known gaps

- Deduplication compares with every event ever kept; a real window is not modelled.
