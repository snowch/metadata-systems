# Brief Y: Chapter 19, "Duplicate events"

Read `docs/notes/part-5/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms this chapter introduces, in bold, and nowhere before the slot named: **deduplication** (slot
D), **idempotent** (slot E). Terms already introduced, which you may use: delivery, at least once.
Do not write: event time, arrival time, precedence, alias, entity resolution, index, partition,
retention, compaction.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Receive one event twice, and find whether the lineage changes.
- Receive an event again with a new time, and find what that changes.
- Tell a repeated event from work done twice.
- Question the requirement "Ingestion must ignore duplicates."

### Slot B: under the heading `## The same event twice`

- In Chapter 18, with delivery at least once, a lost acknowledgement made one event arrive twice.
- Here the COMPLETE of the run of `build_daily_sales` early on Thursday 10 arrives twice. The two
  copies are the same, byte for byte.
- Ingestion turns events into runs and edges, job by job (Chapter 9).
- Before you read on, write in the next cell whether the lineage will change, and how.

### Slot BB: the text inside that cell

One question, then `........` on its own line: will the lineage change, and how? Plain text.

### Slot C: after the cell that compares the two graphs

- The cell shows `69` and `True`: the collector received 69 events, one more than the 68 sent, and
  the job graph built from them is the same as the graph built from the week sent once.
- Ingestion keys each run by its id (Chapter 9), and adds an edge to a run once. A second copy of the
  same event adds nothing to the graph.
- Compare this with what you wrote.
- Under the heading `## A retry with a new time`: some programs build an event again when they send
  it again, with the time of the new sending. The next cell sends the same COMPLETE that way and lists
  the runs of `build_daily_sales` as ingestion records them.

Write the heading `## A retry with a new time` where the fourth fact starts.

### Slot D: after that cell

- The run early on Thursday 10 started at 02:30:00 and now ends at 02:30:52. Its job's runs take 21
  seconds; this one seems to take 52. Ingestion took the end from the later copy.
- Dropping events that repeat one already received is **deduplication**. What counts as a repeat
  depends on the key it compares.
- The next cell drops repeats by content: an event that is the same as one received before, byte for
  byte.

### Slot E: after that cell

- By content, no event was dropped: the copy has a different time, so its content differs.
- Change `"content"` to `"run"` in the cell, select it and press **Run below**. By run, a repeat is a
  second event with the same run id and the same type.
- By run, one event is dropped: the COMPLETE with the time 02:30:52. The one kept has 02:30:21.
- An operation is **idempotent** when doing it twice leaves the same result as doing it once.
  Ingestion keyed by run id is idempotent for the graph's edges. It is not for a run's end time,
  unless repeats are dropped by run first.

### Slot F: under the heading `## A notice delivered twice`

- The returns desk corrected `r-202` on Thursday 10 at 09:30. Object storage sends a notice of each
  change, and the notice starts `record_return`.
- In the week below, object storage delivers that notice twice, so `record_return` starts twice for
  the one change, 25 seconds apart. Each run deletes the return's row from `returns` and writes it
  again.
- Before you read on, write in the next cell what changes in the table `returns`, and what in the
  lineage.

### Slot FF: the text inside that cell

Two short questions, each followed by `........` on its own line: what changes in returns? What
changes in the lineage? Plain text.

### Slot G: after the cell that compares the two tables

- `True`: `returns` is the same as in the week where the notice came once. `record_return` is
  idempotent for the table.
- The next cell looks for runs started more than once for the same change to the same version of an
  object, from the object facet each function's events carry.

### Slot H: after that cell

- One: `s3://shop-returns/r-202.json`, the version written by the correction, `overwritten`, with 2
  runs.
- In the lineage, `record_return` now writes `returns` in 6 runs, not 5.
- The next cell drops repeats by run, as above, and counts what it dropped.

### Slot I: after that cell

- 0: the two runs have different run ids, so deduplication by run keeps both. They are not one event
  sent twice: they are the same work done twice.
- Only a key on the object and its version finds them.

### Slot RH: the heading of the requirement's section

Exactly `## Duplicates`. A box holding the requirement comes after this heading.

### Slot J: after the box (do not quote the requirement again)

- Before you read on, write in the next cell what counts as a duplicate here.

### Slot JJ: the text inside that cell

One question, then `........` on its own line: what counts as a duplicate here? Plain text.

### Slot K: after that cell

- "Duplicates" could mean three things, each needing a different key. Write them as a Markdown list:
  - the same event twice: the event's content;
  - the same run reported twice, with a new time: the run id and the event type;
  - the same work done twice: the object and the version a run read.
- Then, as a second list, what the shop's ingestion does with each:
  - the same event: no edge changes; deduplication by content drops it;
  - the same run reported twice: no edge changes, the run's end time moves, unless repeats are dropped
    by run;
  - the same work twice: two runs in the lineage; no event key drops either.
- The requirement does not say which it means.

### Slot Z: the closing (a heading `## Before Chapter 20`, a summary, a lead, three questions)

- Summary: an event received twice left the graph unchanged, because ingestion keys runs by their id;
  a retry with a new time moved a run's end until repeats were dropped by run; a notice delivered
  twice ran a function twice, which left `returns` the same and the lineage with an extra run, and no
  event key caught it.
- Chapter 20 asks what happens when events arrive in a different order from the one they happened in.
- Three questions, as a list: Which key does your platform's ingestion use to recognise an event it
  has seen? Which of your programs are idempotent, and which would do the work twice? Where would you
  look to tell a retried event from a second run?

Then a heading `### How this differs from a real platform` and a list:

- The shop's faults are invented for the course.
- The shop's ingestion keeps every event it has ever received, so it can compare a new event with all
  of them. A real collector often keeps only recent ones for this.
- The OpenLineage specification says nothing about what a consumer does with an event it receives
  twice (Chapter 8).
