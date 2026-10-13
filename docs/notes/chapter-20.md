# Chapter 20: Out-of-order events

A working note. Written on 12 October 2026 with Chapters 18, 19 and 21 to 23
(`notebook/chapter_20.py`).

## What the chapter does

- meets **event time**, the time the producer says the event occurred (OpenLineage's `eventTime`),
  and **arrival time**, when the collector received it;
- holds up the COMPLETE of the run early on Wednesday 9 by 26 hours, predicts when `daily_sales`
  was last written as the collector sees it at 09:00 on Thursday 10, and reads it both ways: by
  event time, 02:30 on Thursday 10; by arrival, 02:30 on Wednesday 9, a day stale; reads when each
  COMPLETE arrived; then shortens the hold-up to 20 hours and finds the last write right again,
  because the late event now arrives before the next one;
- holds up a START by a minute, past its own COMPLETE: by arrival the run has an end and the state
  START, and Chapter 9's list of runs whose latest event is a START would hold it;
- runs the week with `withdrawn` and holds up Sunday evening's `record_return` events for `r-206`
  by 12 hours, past Monday morning's delete: by arrival the return exists; by event time it is gone;
- questions "Show the latest state of each run."

## What was built for it

`send(delay=...)`, `Delivery.until`, `Delivery.received(job=, type=)`, `ingest.objects(order=...)`
with `written` and `last_write`, `delivery.object_states`.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `late-complete`

- **Role:** experiment
- **Objective:** the reader discovers that taking the last event to arrive as the latest overwrites
  newer state with older.
- **Known before:** Chapter 9's run state by event time; Chapter 13's freshness; Chapter 18's
  delivery. The page states only the hold-up, 26 hours, not the arrival times.
- **Driving question:** at 09:00 on Thursday, when does the collector say `daily_sales` was last
  written?
- **The action:** write in a free-text cell; read `daily_sales`'s last write by event time; change
  `order="event"` to `order="arrival"` and press **Run below**; read when each COMPLETE arrived;
  then change `26` to `20` and press **Run below** again.
- **Why the action:** the order is the only thing that changes between the two answers, and the
  hold-up is the only thing that changes between the second and third.
- **Evidence:** 2026-09-10T02:30:21Z by event time; 2026-09-09T02:30:21Z by arrival, the late
  COMPLETE arriving at 04:30:24 on Thursday 10; held up 20 hours, it arrives at 22:30:24 on Wednesday
  9 and the last write by arrival is Thursday's.
- **Consequence:** an order rule is needed, and event time is the producer's clock.
- **Predictable:** yes, once the two times are named.
- **Gives nothing away:** the cell asks for two times and names none.
- **Not knowing:** fair.
- **Next question:** what else does arrival order break?

### `start-after-complete` and `delete-before-create`

- **Role:** experiment (completes `late-complete`): the same rule, applied to a run's state and to
  an object's existence.
- **The action:** read the runs by arrival; for r-206, change `"arrival"` to `"event"` and press
  **Run below**.
- **Evidence:** the Wednesday run with an end and the state START by arrival, COMPLETE by event
  time; r-206 exists by arrival, not by event time.
- **Next question:** whose clock sets event time?

## Requirements

"Show the latest state of each run." Latest by when it happened, or by when it arrived. The shop's
ingestion orders by event time unless told otherwise; the first reading needs `eventTime` on every
event and clocks that agree, the second only the order the collector received events in, which the
shop keeps. Both are computed from what the shop records, and each answers its own question. Event
time depends on each program's clock; a slow clock sorts its events early. The figure that
questions the requirement is the free-text cell after the box.

## Originality

The obvious example is a streaming textbook's event-time and processing-time diagram with
watermarks and late data. This chapter uses one late event of the shop's own week and reads one
table's last write both ways, with no window or watermark; a return deleted before it is created is
the shop's own case.

## What the prose process caught

Brief Z, draft `part-5/drafts/Z.md`; the review's changes through brief Z-rev, draft
`part-5/drafts/Z-rev.md`. In the revision, "In the first cell" was ambiguous on a page whose first
cell is the contents link; it names the cell that starts `week20 =`. A sentence that two programs'
clocks "can disagree in the same way" pointed at nothing once Chapter 13's clock was gone; cut.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 13 findings (`review/verdicts.md`): 4 upheld, 7 partly, 2 rejected. Read whole again after the fixes, with each
cell's output (`review/chapter_20-after-review.md`). Acted on:

- the page said the reporting tool's clock in Chapter 13 set early event times; it changed what the
  reporting store records, and no event time in the shop moves; the clock is now a general caution;
- the requirement's readings say what each needs, that both are computed from what the shop
  records, and neither is a defect;
- arrival times are shown in a cell, after the commitment, and only the hold-up comes before it;
- Chapter 9 is cited for run state only; the dataset's last write is defined here;
- only `daily_sales`'s last write is shown, not five datasets with a `rows` column;
- the learner now holds the event up: 26 hours, then 20;
- "seems to have started again" is replaced by what the table shows, and Chapter 9's list of START
  runs; the specification's silence is worded as in Chapters 18 and 19, with the run-cycle page's
  rule on terminal events.

Rejected, with the sceptic: a skewed-clock experiment; a third reading by run cycle, which rests on
a disputed claim (`docs/sources.md`).

## Measured

Locally, 12 October 2026, before the review's changes (`docs/notes/notebook-prototype.md`,
"Chapters 18 to 23"): from Chapter 19's link, 11 files, 0.31 MB, in a new tab; Run all 8.2 to 8.5 s;
peak memory 392 to 395 MB alone, 608 MB with Chapter 19 open; no error output.
Live, 12 October 2026, published at `b15b63a`, opened alone at desktop and phone widths: Run all
9.8 to 10.0 s; peak memory 394 to 401 MB; no error output, no console error. The warning's 9 to 12 seconds and about 400 MB
hold.

## Known gaps

- No program's clock in the shop is wrong; a skewed event time is described, not shown.
