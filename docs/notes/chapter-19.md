# Chapter 19: Duplicate events

A working note. Written on 12 October 2026 with Chapters 18 and 20 to 23
(`notebook/chapter_19.py`).

## What the chapter does

Chapter 18 ended with an event received twice. The reader:

- predicts whether the lineage doubles when the COMPLETE of Thursday's `build_daily_sales` run
  arrives twice, then builds it: no edge changes, because ingestion keys a run by its id;
- meets a retry that differs in its time only: the program built the event again when it sent it
  again, and the run now seems to end at 02:30:52, not 02:30:21;
- meets **deduplication** by content, which drops the exact repeat and not the retry, and by run and
  event type, which drops both; and **idempotent**: an operation done twice leaves what it leaves
  done once;
- runs the week with a storage notice delivered twice: `record_return` starts twice for one change
  of `r-202`, the table `returns` ends the same, and deduplication drops nothing, because these are
  two runs; `repeated_work` finds them by the object and version they read;
- questions "Ingestion must ignore duplicates."

## What was built for it

`delivery.send` with `lose_ack` and `restamp`; `ingest.dedupe`; the `twice` change;
`delivery.repeated_work`.

## Figures

### `platform-with-returns`

- **Role:** reference

### `repeat-and-graph`

- **Role:** experiment
- **Objective:** the reader discovers that keying runs by their id keeps the graph the same when an
  event repeats.
- **Known before:** Chapter 9's objects stage, which keys runs by `runId`; Chapter 18's repeat.
- **Driving question:** does the lineage double?
- **The action:** commit in a cell; run the cell that sends with the acknowledgement lost and builds
  the graph beside the graph of the week sent whole.
- **Why the action:** only the two graphs side by side answer it.
- **Evidence:** 69 events received; the same 14 job edges with the same run counts.
- **Consequence:** an "it doubles" answer meets the run key.
- **Predictable:** yes, from Chapter 9.
- **Gives nothing away:** the options are results.
- **Not knowing:** fair.
- **Next question:** what if the repeat is not identical?

### `retry-with-a-new-time`

- **Role:** experiment
- **Objective:** the reader finds a repeat that changes a run's recorded end, and that the key a
  deduplication uses decides whether it is caught.
- **Evidence:** the run ends at 02:30:52; by content, 0 dropped; by run and type, 1 dropped, and the
  end is 02:30:21 again.

### `trigger-twice`

- **Role:** experiment
- **Objective:** the reader tells a repeated event from repeated work: two runs that each did the
  work, which no event key merges.
- **Known before:** the returns desk (Chapter 7); `record_return` deletes the return's row and writes
  it again.
- **Driving question:** with the notice of r-202's correction delivered twice, what changes in
  `returns`, and what in the lineage?
- **The action:** run the week with `twice`; compare the table and the runs.
- **Evidence:** `returns` the same; `record_return` with 6 runs writing `returns`, not 5;
  deduplication drops 0; `repeated_work` lists r-202's version with 2 runs.
- **Consequence:** the function is idempotent for the table; the lineage holds an extra run.
- **Predictable:** partly.
- **Gives nothing away:** asks what changes, not why.
- **Not knowing:** fair.
- **Next question:** what if events arrive in the wrong order?

## Requirements

"Ingestion must ignore duplicates." Readings: the same event twice; the same run reported twice;
the same work done twice. Each needs a different key: the event's content; the run id and event
type; the object and version the run read. The shop's ingestion, by run id, ignores the first for
edges, not the second (the end time moves) unless deduplicated by run and type, and does not see the
third as a duplicate at all. The requirement does not say which.

## Originality

The obvious example is a stream processor's exactly-once tutorial with a deduplication window on a
message id. This chapter uses the shop's own events and one of its own functions, and separates a
repeated event, a repeated event with a new time, and repeated work, each with the key that would
catch it.
