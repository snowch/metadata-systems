[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 18](chapter_18.ipynb) · [Next: Chapter 20](chapter_20.ipynb)

# Chapter 19: Duplicate events

**Objectives**

- Find whether the lineage changes when one event arrives twice.
- Find what changes when an event arrives again with a new time.
- Tell a repeated event from work done twice.
- Question the requirement "Ingestion must ignore duplicates."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## The same event twice

In the last cells of Chapter 18, delivery was at least once, and a lost acknowledgement made one event arrive twice.

The `COMPLETE` event for the run of `build_daily_sales` early on Thursday 10 arrives twice, and the two copies are the same, byte for byte.

Ingestion turns events into runs and edges, job by job (Chapter 9).

Before you read on, write in the next cell whether the lineage will change, and how.

    [WRITE] Will the lineage change, and how?
    [WRITE] ........

    >>> week19 = shop.run_week(["returns"])
    >>> once = shop.delivery.send(week19)
    >>> twice = shop.delivery.send(week19, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True)
    >>> graph = lambda d: shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(d.events)))
    >>> print(len(twice.events), "events received")
    >>> print("The same graph as with each event received once:", graph(twice).by_job == graph(once).by_job)
    >>> graph(twice).of("shop/build_daily_sales")
      69 events received
      The same graph as with each event received once: True
      | job | edge | dataset | runs | first | last
      | shop/build_daily_sales | reads | warehouse://shop-warehouse/shop.analytics.clean_orders | 7 | 2026-09-08T02:30:21Z | 2026-09-14T02:30:21Z
      | shop/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 7 | 2026-09-08T02:30:21Z | 2026-09-14T02:30:21Z

The collector received 69 events, 1 more than the 68 sent.

The cell compares every job's edges, with how many runs had each and the first and last time, against the graph built when each event was received once. They are the same: `True`.

The cell then lists the edges of `build_daily_sales`: `reads` `clean_orders` in 7 runs, and `writes` `daily_sales` in 7 runs, the counts Chapter 18 showed with every event.

Ingestion merges events into runs by their run id. The copy names the same run and the same datasets, so it adds nothing to the graph.

Compare this with what you wrote.

## A retry with a new time

A program can build an event again when it sends it again, with the time of the new sending. The next cell sends the same `COMPLETE` that way, then lists the runs of `build_daily_sales` as ingestion records them.

    >>> retimed = shop.delivery.send(week19, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True, restamp=True)
    >>> shop.ingest.objects(shop.ingest.normalise(retimed.events)).runs_of(job="shop/build_daily_sales", columns=["started", "ended"])
      | started | ended
      | 2026-09-08T02:30:00Z | 2026-09-08T02:30:21Z
      | 2026-09-09T02:30:00Z | 2026-09-09T02:30:21Z
      | 2026-09-10T02:30:00Z | 2026-09-10T02:30:52Z
      | 2026-09-11T02:30:00Z | 2026-09-11T02:30:21Z
      | 2026-09-12T02:30:00Z | 2026-09-12T02:30:21Z
      | 2026-09-13T02:30:00Z | 2026-09-13T02:30:21Z
      | 2026-09-14T02:30:00Z | 2026-09-14T02:30:21Z

The run early on Thursday 10 started at 02:30:00 and now ends at 02:30:52. Runs of `build_daily_sales` take 21 seconds. This one seems to take 52 seconds.

Ingestion takes a run's end from the time its last terminal event records. The copy records 02:30:52, later than the first's 02:30:21.

The OpenLineage specification describes `eventTime` as "the time the event occurred at". The copy states the time it was sent again, so its time is wrong.

Dropping events that repeat one already received is **deduplication**. What counts as a repeat depends on the key it compares.

The next cell drops repeats by content: an event with the same content as one received before.

    >>> deduped = shop.ingest.dedupe(retimed.events, "content")
    >>> deduped.dropped
      []

By content, no event was dropped: the copy's time differs, so its content differs.

The next cell ingests the events kept and lists the runs of `build_daily_sales`. The run early on Thursday 10 still ends at 02:30:52.

    >>> shop.ingest.objects(shop.ingest.normalise(deduped)).runs_of(job="shop/build_daily_sales", columns=["started", "ended"])
      | started | ended
      | 2026-09-08T02:30:00Z | 2026-09-08T02:30:21Z
      | 2026-09-09T02:30:00Z | 2026-09-09T02:30:21Z
      | 2026-09-10T02:30:00Z | 2026-09-10T02:30:52Z
      | 2026-09-11T02:30:00Z | 2026-09-11T02:30:21Z
      | 2026-09-12T02:30:00Z | 2026-09-12T02:30:21Z
      | 2026-09-13T02:30:00Z | 2026-09-13T02:30:21Z
      | 2026-09-14T02:30:00Z | 2026-09-14T02:30:21Z

Change `"content"` to `"run"` in the cell that starts `deduped =`. Select that cell and press **Run below**.

By run, a repeat is a second event with the same run id and the same type.

By run, one event is dropped: the `COMPLETE` with the time 02:30:52. The event kept has the time 02:30:21.

Deduplication keeps the first event it meets of each key, and the first copy arrived first.

In the cell below it, the run early on Thursday 10 ends at 02:30:21 again.

An operation is **idempotent** when doing it twice leaves the same result as doing it once. Here the operation is ingesting what the collector received.

Ingesting an exact copy is idempotent for the graph. Ingesting a copy with a new time is not idempotent for the run's end time, unless repeats are dropped by run first.

## A notice delivered twice

The returns desk corrected `r-202` on Thursday 10 at 09:30. Object storage sends a notice of each change, and each notice starts `record_return`.

In the week below, object storage delivers the notice for the correction twice. So `record_return` starts twice for the one change, 25 seconds apart. Each run deletes the return's row from `returns` and writes it again.

Before you read on, write in the next cell what changes in the table `returns`, and what changes in the lineage.

    [WRITE] What changes in returns?
    [WRITE] ........
    [WRITE] 
    [WRITE] What changes in the lineage?
    [WRITE] ........

    >>> week19t = shop.run_week(["returns", "twice"])
    >>> query = "SELECT * FROM returns ORDER BY return_id"
    >>> week19t.warehouse.sql(query) == week19.warehouse.sql(query)
      True

The cell shows `True`. `returns` is the same as in the week in which the notice came once. `record_return` is idempotent for the table.

The next cell looks for runs started more than once for the same change to the same version of an object. It reads `shop_objectChange`, the facet each function's events carry (Chapter 9): the object, its version and the change.

    >>> events_t = shop.delivery.week_events(week19t)
    >>> shop.delivery.repeated_work(events_t)
      | object | version | change | runs
      | s3://shop-returns/r-202.json | 68d7454802de | overwritten | 2

The output lists 1 version that more than one run started for: `s3://shop-returns/r-202.json`, the version the correction wrote, with the change `overwritten` and 2 runs.

The next cell lists the edges of `record_return` in the week in which the notice came once and in the week in which it came twice.

    >>> shop.ingest.edges_side_by_side("shop/record_return", label="notice", once=shop.delivery.week_events(week19), twice=events_t)
      | notice | edge | dataset | runs
      | once | reads | s3://shop-returns/r-201.json | 1
      | once | writes | warehouse://shop-warehouse/shop.analytics.returns | 5
      | once | reads | s3://shop-returns/r-202.json | 2
      | once | reads | s3://shop-returns/r-203.json | 1
      | once | reads | s3://shop-returns/r-204.json | 1
      | twice | reads | s3://shop-returns/r-201.json | 1
      | twice | writes | warehouse://shop-warehouse/shop.analytics.returns | 6
      | twice | reads | s3://shop-returns/r-202.json | 3
      | twice | reads | s3://shop-returns/r-203.json | 1
      | twice | reads | s3://shop-returns/r-204.json | 1

In the lineage, `record_return` now writes `returns` in 6 runs, not 5.

It reads `r-202.json` in 3 runs, not 2.

The next cell drops repeats by run, and counts what it drops.

    >>> len(shop.ingest.dedupe(events_t, "run").dropped)
      0

The cell shows 0 dropped. The two runs have different run ids, so deduplication by run keeps both.

They are not one event sent twice. They are the same work done twice.

Deduplication by content and by run drops neither run. Only a key made from the object, its version and the change, from `shop_objectChange`, finds the two runs.

## Duplicates

[BOX] The head of the shop's requirement: "Ingestion must ignore duplicates."

Before you read on, write in the next cell what counts as a duplicate here.

    [WRITE] What counts as a duplicate here?
    [WRITE] ........

"Duplicates" could mean three things. Each needs a different key:

- the same event twice: the event's content;
- the same run reported twice, with a new time: the run id and the event type;
- the same work done twice: the object, its version and the change.

The shop's ingestion does not drop anything itself. Deduplication is a step you applied in these cells. Whether "Ingestion must ignore duplicates" is met, for each reading:

- The same event: met for the graph by ingestion alone: the copy adds nothing. Deduplication by content also drops it.
- The same run with a new time: not met by ingestion alone: the run's end time moves. Met when repeats are dropped by run before ingestion.
- The same work: not met. The lineage holds two runs, and neither key of deduplication drops either.

The requirement does not say which of these it means.

## Before Chapter 20

An event received twice left the graph unchanged, because ingestion merges events into runs by run id. A retry with a new time moved a run's end time until repeats were dropped by run. A notice delivered twice ran a function twice, which left `returns` the same and added a second run to the lineage. Deduplication by content and by run did not drop the second run.

Chapter 20 asks what happens when events arrive in a different order from the order in which they happened.

- Which key does your platform's ingestion use to recognise an event it has seen?
- Which of your programs are idempotent, and which would do the work twice?
- Where would you look to tell a retried event from a second run?

### How this differs from a real platform

- The shop's faults are invented for the course.
- The shop's deduplication compares each event with every event kept before it, with no time limit.
- The shop's programs send one `START` and one `COMPLETE` for each run. The OpenLineage specification allows a run to send `RUNNING` and `OTHER` events as well, and several of them, so a key of run id and event type would drop real events there.
- The OpenLineage specification says nothing about what a consumer does with an event it receives twice (Chapter 8).

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 18](chapter_18.ipynb) · [Next: Chapter 20](chapter_20.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

