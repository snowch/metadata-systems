# Revision brief Y: Chapter 19, Duplicate events

Letter Y. Read `rev-common.md` first. Redraft these slots: B, C, D, E, E2, G, H, H2, I, K, Z.
Terms: **deduplication** is introduced in slot D, **idempotent** in slot E2, each in bold there and
nowhere before. Do not write "byte for byte" anywhere except slot B.

## B

- Keep the heading `## The same event twice`.
- In the last cells of Chapter 18, delivery was at least once, and a lost acknowledgement made one
  event arrive twice.
- Keep: the `COMPLETE` event for the run of `build_daily_sales` early on Thursday 10 arrives twice,
  and the two copies are the same, byte for byte.
- Ingestion turns events into runs and edges, job by job (Chapter 9).
- Before you read on, write in the next cell whether the lineage will change, and how.

## C

- Keep: "The collector received 69 events, 1 more than the 68 sent."
- The cell compares every job's edges, with how many runs had each and the first and last time,
  against the graph built when each event was received once. They are the same: `True`.
- The cell then lists the edges of `build_daily_sales`: `reads` `clean_orders` in 7 runs, and
  `writes` `daily_sales` in 7 runs, the counts Chapter 18 showed with every event.
- Ingestion merges events into runs by their run id. The copy names the same run and the same
  datasets, so it adds nothing to the graph.
- Compare this with what you wrote.
- Then this heading: `## A retry with a new time`
- A program can build an event again when it sends it again, with the time of the new sending.
  The next cell sends the same `COMPLETE` that way, then lists the runs of `build_daily_sales` as
  ingestion records them.

## D

- Keep: "The run early on Thursday 10 started at 02:30:00 and now ends at 02:30:52. Runs of
  `build_daily_sales` take 21 seconds. This one seems to take 52 seconds."
- Ingestion takes a run's end from the event time of its last terminal event. The copy's event
  time, 02:30:52, is later than the first's, 02:30:21.
- The OpenLineage specification describes `eventTime` as "the time the event occurred at". The
  copy states the time it was sent again, so its time is wrong.
- Dropping events that repeat one already received is **deduplication**. What counts as a repeat
  depends on the key it compares.
- The next cell drops repeats by content: an event with the same content as one received before.

## E

- By content, no event was dropped: the copy's time differs, so its content differs.
- The next cell ingests the events kept and lists the runs of `build_daily_sales`. The run early on
  Thursday 10 still ends at 02:30:52.

## E2

- Change `"content"` to `"run"` in the cell that starts `deduped =`. Select that cell and press
  **Run below**.
- By run, a repeat is a second event with the same run id and the same type.
- Keep: "By run, one event is dropped: the `COMPLETE` with the time 02:30:52. The event kept has the
  time 02:30:21."
- Deduplication keeps the first event it meets of each key, and the first copy arrived first.
- In the cell below it, the run early on Thursday 10 ends at 02:30:21 again.
- An operation is **idempotent** when doing it twice leaves the same result as doing it once. Here
  the operation is ingesting what the collector received.
- Ingesting an exact copy is idempotent for the graph. Ingesting a copy with a new time is not
  idempotent for the run's end time, unless repeats are dropped by run first.

## G

- The cell shows `True`: `returns` is the same as in the week in which the notice came once.
  `record_return` is idempotent for the table.
- The next cell looks for runs started more than once for the same change to the same version of an
  object. It reads `shop_objectChange`, the facet each function's events carry (Chapter 9): the
  object, its version and the change.

## H

- The output lists 1 version that more than one run started for: `s3://shop-returns/r-202.json`,
  the version the correction wrote, with the change `overwritten` and 2 runs.
- The next cell lists the edges of `record_return` in the week in which the notice came once and in
  the week in which it came twice.

## H2

- Keep: "In the lineage, `record_return` now writes `returns` in 6 runs, not 5."
- It reads `r-202.json` in 3 runs, not 2.
- The next cell drops repeats by run, and counts what it drops.

## I

- The cell shows 0 dropped. The two runs have different run ids, so deduplication by run keeps both.
- They are not one event sent twice. They are the same work done twice.
- Deduplication by content and by run drops neither run. Only a key made from the object, its
  version and the change, from `shop_objectChange`, finds the two runs.

## K

A list of three readings, then a list of three results, then one sentence.

- Keep the opening: "Duplicates" could mean three things. Each needs a different key:
- Readings, each with its key: the same event twice (the event's content); the same run reported
  twice, with a new time (the run id and the event type); the same work done twice (the object, its
  version and the change).
- Then: the shop's ingestion does not drop anything itself. Deduplication is a step you applied in
  these cells. Whether "Ingestion must ignore duplicates" is met, for each reading:
- Result 1, the same event: met for the graph by ingestion alone: the copy adds nothing.
  Deduplication by content also drops it.
- Result 2, the same run with a new time: not met by ingestion alone: the run's end time moves. Met
  when repeats are dropped by run before ingestion.
- Result 3, the same work: not met. The lineage holds two runs, and neither key of deduplication
  drops either.
- The requirement does not say which of these it means.

## Z

- Keep the heading `## Before Chapter 20`.
- Summary facts, in order: an event received twice left the graph unchanged, because ingestion
  merges events into runs by run id; a retry with a new time moved a run's end time until repeats
  were dropped by run; a notice delivered twice ran a function twice, which left `returns` the same
  and added a second run to the lineage; deduplication by content and by run did not drop it.
- Keep: "Chapter 20 asks what happens when events arrive in a different order from the order in
  which they happened."
- Keep the first draft's three questions as a list.
- Keep the heading `### How this differs from a real platform` and these bullets:
  - The shop's faults are invented for the course.
  - The shop's deduplication compares each event with every event kept before it, with no time
    limit.
  - The shop's programs send one `START` and one `COMPLETE` for each run. The OpenLineage
    specification allows a run to send `RUNNING` and `OTHER` events as well, and several of them,
    so a key of run id and event type would drop real events there.
  - The OpenLineage specification says nothing about what a consumer does with an event it
    receives twice (Chapter 8).
