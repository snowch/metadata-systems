## A

- Find whether the lineage changes when one event arrives twice.
- Find what changes when an event arrives again with a new time.
- Tell a repeated event from work done twice.
- Question the requirement "Ingestion must ignore duplicates."

## B

## The same event twice

In Chapter 18, delivery was at least once. A lost acknowledgement made one event arrive twice.

Here, the `COMPLETE` event for the run of `build_daily_sales` early on Thursday 10 arrives twice. The two copies are the same, byte for byte.

Ingestion turns events into runs and edges, job by job (Chapter 9).

Before you read on, write in the next cell whether the lineage will change, and how.

## BB

Will the lineage change, and how?

........

## C

The cell shows `69` and `True`. The collector received 69 events, 1 more than the 68 sent. The job graph built from them is the same as the graph built from the week with each event sent once.

Ingestion keys each run by its id (Chapter 9), and adds an edge to a run only once. A second copy of the same event adds nothing to the graph.

Compare this with what you wrote.

## A retry with a new time

Some programs build an event again when they send it again, with the time of the new sending. The next cell sends the same `COMPLETE` that way, then lists the runs of `build_daily_sales` as ingestion records them.

## D

The run early on Thursday 10 started at 02:30:00 and now ends at 02:30:52. Runs of `build_daily_sales` take 21 seconds. This one seems to take 52 seconds. Ingestion took the end time from the later copy.

Dropping events that repeat one already received is **deduplication**. What counts as a repeat depends on the key it compares.

The next cell drops repeats by content: an event that is the same as one received before, byte for byte.

## E

By content, no event was dropped. The copy has a different time, so its content differs.

Change `"content"` to `"run"` in the cell above. Then select that cell and press **Run below**. By run, a repeat is a second event with the same run id and the same type.

By run, one event is dropped: the `COMPLETE` with the time 02:30:52. The event kept has the time 02:30:21.

An operation is **idempotent** when doing it twice leaves the same result as doing it once. Ingestion keyed by run id is idempotent for the graph's edges. It is not idempotent for a run's end time, unless repeats are dropped by run first.

## F

## A notice delivered twice

The returns desk corrected `r-202` on Thursday 10 at 09:30. Object storage sends a notice of each change, and each notice starts `record_return`.

In the week below, object storage delivers the notice for the correction twice. So `record_return` starts twice for the one change, 25 seconds apart. Each run deletes the return's row from `returns` and writes it again.

Before you read on, write in the next cell what changes in the table `returns`, and what changes in the lineage.

## FF

What changes in `returns`?

........

What changes in the lineage?

........

## G

The cell shows `True`. `returns` is the same as in the week in which the notice came once. `record_return` is idempotent for the table.

The next cell looks for runs started more than once for the same change to the same version of an object. It uses the object facet that each function's events carry.

## H

The output lists 1 version that more than one run started for: `s3://shop-returns/r-202.json`. It is the version the correction wrote, shown as `overwritten`, with 2 runs.

In the lineage, `record_return` now writes `returns` in 6 runs, not 5.

The next cell drops repeats by run and counts what it dropped.

## I

The cell shows 0 dropped. The two runs have different run ids, so deduplication by run keeps both. They are not one event sent twice. They are the same work done twice.

Only a key made from the object and its version finds the two runs.

## RH

## Duplicates

## J

Before you read on, write in the next cell what counts as a duplicate here.

## JJ

What counts as a duplicate here?

........

## K

"Duplicates" could mean three things. Each needs a different key:

- the same event twice: the event's content;
- the same run reported twice, with a new time: the run id and the event type;
- the same work done twice: the object and the version a run read.

Then, for each of the three, here is what the shop's ingestion does:

- the same event: no edge changes, and deduplication by content drops it;
- the same run reported twice: no edge changes, and the run's end time moves, unless repeats are dropped by run;
- the same work done twice: two runs in the lineage, and no event key drops either.

The requirement does not say which of these it means.

## Z

## Before Chapter 20

An event received twice left the graph unchanged, because ingestion keys runs by their id. A retry with a new time moved a run's end time until repeats were dropped by run. A notice delivered twice ran a function twice. That left `returns` the same and added an extra run to the lineage. No event key caught it.

Chapter 20 asks what happens when events arrive in a different order from the order in which they happened.

- Which key does your platform's ingestion use to recognise an event it has seen?
- Which of your programs are idempotent, and which would do the work twice?
- Where would you look to tell a retried event from a second run?

### How this differs from a real platform

- The shop's faults are invented for the course.
- The shop's ingestion keeps every event it has ever received, so it can compare a new event with all of them. A real collector often keeps only recent ones for this.
- The OpenLineage specification says nothing about what a consumer does with an event it receives twice (Chapter 8).
