# Chapter 18: Missing events

A working note. Written on 12 October 2026 with Chapters 19 to 23, as a notebook
(`notebook/chapter_18.py`). It opens Part V.

## What the chapter does

Every chapter so far gave the collector every event the programs sent. The reader:

- sends the week's events down the path to the collector and reads what arrived: 68 sent, 68
  received; and meets **delivery**, the path an event takes and whether it arrives;
- predicts what the job graph shows for `build_daily_sales` when the COMPLETE of its run early on
  Thursday 10 is lost, then builds it: the same two edges, `writes` now with 6 runs, not 7;
- finds that run open (a START and no end at the collector): started at 02:30 on Thursday, 369000
  seconds before Monday 09:00, where the job's runs that ended took 21 seconds. The gap suggests a
  loss and proves nothing: a run that hangs leaves the same events. The warehouse's row for
  Wednesday 9 shows the run wrote it, not how the run ended;
- loses the COMPLETE of `remove_return`'s only run, and finds the function with no edge at all: its
  START names the object `r-203.json` in `shop_objectChange`, not the table, so the graph shows
  `record_return` as the only writer of `returns`;
- sends again until acknowledged and meets **at least once**: the COMPLETE, sent at 16:50:05 and
  again at 16:50:35, arrives once at 16:50:37; then predicts, and finds, that a lost acknowledgement
  makes it arrive twice, at 16:50:07 and 16:50:37;
- questions "Lineage must be complete."

## What was built for it

`notebook/shop/delivery.py`: `send`, `open_runs`, `Delivery.retried`; `ingest.objects` and `edges`
as Chapter 9 built them.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map: the shop's three systems and the returns desk. It does not draw
  the path to the collector; the timings are four numbers, and the prose carries them.
- **Why now:** every chapter opens with the map.

### `sent-and-received`

- **Role:** inspect
- **Serves:** what arrived when nothing is lost: the baseline the experiments change.
- **Why now:** the reader needs the count before one event goes missing.

### `lost-complete`

- **Role:** experiment
- **Objective:** the reader discovers that a job's graph, built from all its runs, hides a lost
  event, which shows only in the run it belonged to.
- **Known before:** Chapter 9's graph, job by job, with how many runs had each edge; Chapter 8's
  START and COMPLETE, and that outputs come in the COMPLETE.
- **Driving question:** what will the graph show for `build_daily_sales` when one COMPLETE never
  arrives?
- **The action:** write a prediction in a free-text cell; read the cell below it, which loses the
  event and builds the graph.
- **Why the action:** the graph is built from the events received; only building it shows which
  edges survive.
- **Evidence:** both edges kept; `writes` with 6 runs; one run left START.
- **Consequence:** a reader who expected the edge to vanish learns that other runs carry it; one
  who expected nothing to change finds the run left open.
- **Predictable:** yes, from Chapter 9's runs per edge, where a line cut short gave the same 6; the
  page says so. What is new is the next question, which the events cannot settle.
- **Gives nothing away:** the cell asks for edges and runs, and names no result.
- **Not knowing:** a fair first answer.
- **Next question:** is that run lost, or still running?

### `open-runs`

- **Role:** inspect
- **Serves:** is the run lost, or still going? The open runs, with the seconds since each started
  and the job's `usual seconds`.
- **Why now:** the gap suggests a loss; the page says it proves nothing, and goes to the row.

### `row-written`

- **Role:** inspect (completes `open-runs`)
- **Serves:** evidence from outside the events: the run early on Thursday 10 writes Wednesday 9's
  row, one row a run. The row shows the write, not how the run ended.

### `only-run`

- **Role:** experiment (completes `lost-complete`)
- **Objective:** the reader finds that a job that ran once leaves no edge when its one COMPLETE is
  lost: a dependency the graph cannot show.
- **Evidence:** `remove_return` with no edge; its open run with no `usual seconds`. Its START
  names the object, not the table.

### `at-least-once`

- **Role:** experiment
- **Objective:** the reader sees what sending again until acknowledged buys (the event arrives)
  and costs (an event can arrive twice).
- **Known before:** the lost COMPLETE above.
- **Driving question:** if the program keeps the event until the collector acknowledges it, does
  the COMPLETE arrive, and how many times?
- **The action:** read the cell that sends with `at_least_once=True`; write how many times the
  COMPLETE will arrive with its acknowledgement lost; change `lose=` to `lose_ack=` in that cell and
  press **Run below**.
- **Why the action:** losing the event and losing the acknowledgement are the two failures a retry
  answers, and only the second makes a repeat.
- **Evidence:** sent twice, received once; with the acknowledgement lost, sent twice and received
  twice.
- **Consequence:** the reader trades a loss for a repeat, which Chapter 19 takes up.
- **Predictable:** yes, from the rule on the page; the repeat is the surprise for a reader who
  thinks of a retry as replacing a lost event.
- **Gives nothing away:** the cell asks how many times, and nothing more.
- **Not knowing:** fair.
- **Next question:** what does ingestion do with an event it has seen?

## Requirements

The chapter questions "Lineage must be complete.", the plan's candidate.

1. **What it says:** lineage must be complete.
2. **What it might mean:** every event each program sends arrives; every program that touches the
   data sends events; every run's edges are known.
3. **What each needs:** delivery that does not lose (or that sends again); every program that
   changes the data sending events; a COMPLETE, ABORT or FAIL at the collector for each run that
   has ended.
4. **What the shop records:** what arrived, and runs left open.
5. **Whether it is met:** with at least once, every event sent arrives; the export sends no events
   (Chapter 13), so not every program; a run's end only where its program sent it, not for a
   program that stops first or a run that has not ended. The requirement does not say which it
   means. The figure that questions it is the free-text cell after the requirement's box.

## Originality

The obvious examples are a message queue's tutorial on at-least-once delivery with producer acks,
and a lineage tool's documentation of a job stuck in a running state. This chapter loses one named
event of the shop's own week, builds the shop's own graph from what arrived, and contrasts a job
with seven runs against one with a single run. The path's timings and the open-run listing are the
shop's own.

## What the prose process caught

Brief X, draft `part-5/drafts/X.md`; the review's changes through brief X-rev, draft
`part-5/drafts/X-rev.md`. In the revision, my brief told Haiku not to bold *at least once* again,
though slot H is its home; the term gate failed it and I restored the bold. "The `COMPLETE`'s event
time" used Chapter 20's term; it now says the time the event records.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 19 findings (`review/verdicts.md`): 7 upheld, 9 partly, 3 rejected. Read whole again after the fixes, with each cell's output (`review/chapter_18-after-review.md`).
Acted on:

- the receipt was 32 seconds after the first sending, not 30; the page gives both sendings and the
  receipt, and the test pins each;
- the analyst's copy sends events since Chapter 9; only the export sends none (Chapter 13);
- reading 3 no longer claims at least once delivers every run's end;
- the gap of 369000 seconds suggests a loss and proves nothing; the row shows the write, not the
  end; the summary is scoped the same way;
- `remove_return`'s START carries `shop_objectChange`; the slogan about a dependency that cannot be
  shown is gone; the graph credits `returns` to `record_return` alone;
- a prediction before `lose_ack`; "open run" named once; "function", not "job"; `usual seconds`;
  "instrumented" gone; "Compare these with what you wrote." after the readings; the early pointer
  to Chapter 19 cut; the run-cycle page's streaming jobs in the reality note.

Rejected, with the sceptic: a figure of the path, new readings of "complete", the house wording of
the requirement. The "Time and memory" warning was measured for the whole part (below).

## Measured

Locally, 12 October 2026, before the review's changes (`docs/notes/notebook-prototype.md`,
"Chapters 18 to 23"): from Chapter 17's link, 11 files, 0.32 MB, in a new tab; Run all 7.8 to 8.5 s;
peak memory 395 to 402 MB alone, 611 MB with Chapter 17 open; no error output.

## Known gaps

- The shop's path loses only what a cell names; nothing here is random.
