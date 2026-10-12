[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 17](chapter_17.ipynb) · [Next: Chapter 19](chapter_19.ipynb)

# Chapter 18: Missing events

**Objectives**

- Send the week's events, lose one, and build the graph from what arrived.
- Find the runs that started and never ended, and what the events cannot tell you about them.
- Send an event again until it is acknowledged, and see what that costs.
- Question the requirement "Lineage must be complete."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

    <<CODE>> mo.Html(figures.figure(figures.pipeline(shop.run_week(["returns"]), "jobs nightly; functions at any hour"), "The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table `returns`."))

## From the programs to the collector

The program that receives the shop's events and keeps them for ingestion is the shop's **collector**. In the earlier chapters, the collector received every event the shop's programs sent, each one once and in order.

Each program sends each event to the collector over the network. In the shop, a program sends an event 1 second after the time the event records, and the collector receives it 2 seconds later.

The path an event takes from a program to the collector, and whether the event arrives, is its **delivery**.

The next cell sends the week's events, with the returns desk's events among them, and counts what the collector received.

    <<CODE>> week18 = shop.run_week(["returns"])
    sent = shop.delivery.send(week18)
    sent

## One COMPLETE lost

The cell sent 68 events, and the collector received 68. None was lost.

Now one event is lost: the `COMPLETE` of the run of `build_daily_sales` early on Thursday 10. Its `START` arrives.

The graph from Chapter 9 lists each job's edges, with how many runs had each one. With every event, `build_daily_sales` has two edges: a `reads` edge to `clean_orders` in 7 runs, and a `writes` edge to `daily_sales` in 7 runs. A run reports its outputs in its `COMPLETE` (Chapter 8).

Before you read on, write in the next cell what the graph will show for `build_daily_sales` when that `COMPLETE` never arrives: which edges, and how many runs each.

    <<CODE>> expected_graph = """
    What will the graph show for build_daily_sales?
    ........
    """

    <<CODE>> lost = shop.delivery.send(week18, lose=["build_daily_sales COMPLETE 2026-09-10"])
    found = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(lost.events)))
    found.of("shop/build_daily_sales")

Both edges are still there. `writes` now has 6 runs, not 7. `reads` still has 7.

The other 6 runs that wrote `daily_sales` carry the edge. The missing `COMPLETE` affects only the run it belongs to.

Compare this with what you wrote.

The next cell lists the runs that have a `START` at the collector and no `COMPLETE`, `ABORT` or `FAIL`, at 09:00 on Monday 14. For each one, it shows how many seconds have passed since it started, and how long that job's runs that ended usually took.

    <<CODE>> shop.delivery.open_runs(lost.events, "2026-09-14T09:00:00Z")

The cell lists one open run: `build_daily_sales`, started at 02:30:00 on Thursday 10. That is 369000 seconds before Monday 09:00, more than four days. The job's runs that ended took 21 seconds.

The collector's events cannot tell a lost `COMPLETE` from a run that is still running. Both leave a `START` and nothing after it.

Other evidence can tell them apart. The run early on Thursday 10 writes Wednesday 9's row of `daily_sales`. The next cell reads that row from the warehouse.

    <<CODE>> week18.warehouse.sql("SELECT * FROM daily_sales WHERE day = '2026-09-09'")

## A job that ran once

The row is there: 15375 pence for Wednesday 9. The run did its work. Only its `COMPLETE` is missing.

`remove_return` ran once in the week: on Saturday 12 at 16:50:02, when the returns desk deleted `r-203`. Its `START` names no dataset. Its `COMPLETE` names what it wrote, `returns`.

The next cell loses that `COMPLETE` and builds the graph from what arrived.

    <<CODE>> lost_once = shop.delivery.send(week18, lose=["remove_return COMPLETE"])
    found_once = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(lost_once.events)))
    found_once.of("shop/remove_return")

`remove_return` has no edge in the graph. With every event, it has one edge: it writes `returns`.

With its one `COMPLETE` lost, nothing the collector holds shows that `remove_return` writes `returns`. The dependency is real, and it cannot be shown.

The next cell lists the open runs again.

    <<CODE>> shop.delivery.open_runs(lost_once.events, "2026-09-14T09:00:00Z")

The open run of `remove_return` started at 16:50:02 on Saturday 12. Its usual time is empty, because the job has no other run to compare with.

## Sending again

So far, each program sends each event once and keeps nothing. A lost event is gone.

The alternative is for the collector to acknowledge each event it receives. The program keeps each event until it is acknowledged. It sends the event again if no acknowledgement comes within 30 seconds. Then every event sent arrives once or more. This delivery is **at least once**.

The next cell loses the same `COMPLETE` once, sends with `at_least_once=True`, and lists the events that were sent or received more than once.

    <<CODE>> again = shop.delivery.send(week18, lose=["remove_return COMPLETE"], at_least_once=True)
    again.retried()

The `COMPLETE` was sent twice and received once. The receipt was at 16:50:37 on Saturday 12, 30 seconds after the first sending.

Now change `lose=` to `lose_ack=` in the cell, select it, and press **Run below**. The `COMPLETE` then arrives, and its acknowledgement is lost.

With `lose_ack`, the `COMPLETE` is sent twice and received twice: at 16:50:07 and at 16:50:37.

At least once trades a lost event for an event that can arrive twice. Chapter 19 takes up the event that arrives twice.

## Complete lineage

[BOX] The head of the shop's requirement: "Lineage must be complete."

Before you read on, write in the next cell what "complete" means to you here.

    <<CODE>> what_complete_means = """
    What does "complete" mean here?
    ........
    """

"Complete" could mean three things, each needing something different:

- Every event a program sends arrives. It needs delivery at least once, or no loss.
- Every program that touches the data sends events. It needs every program instrumented.
- Every run's end and edges are known. It needs a `COMPLETE`, `ABORT` or `FAIL` for each run.

The shop's records meet these as follows:

- Every event sent arrives: met with at least once, not without it. One lost `COMPLETE` left a run open, and for `remove_return`, left no edge.
- Every program: not met. The export and the analyst's copy send no events (Chapter 8).
- Every run's end: met with at least once, as long as each program sends its events at all.

The requirement does not say which of these it means.

## Before Chapter 19

A lost `COMPLETE` left every edge in the graph, because other runs carried them. It left one run open. The events could not tell a lost `COMPLETE` from a run still going. The warehouse's row could tell them apart. For a job that ran once, the lost `COMPLETE` left no edge at all. Sending again until acknowledged delivered the event, and a lost acknowledgement delivered it twice.

Chapter 19 asks what ingestion does with an event it receives twice.

- Which of your platform's programs send no events at all?
- What does your collector do with an event it has already received?
- How would you tell a slow run from a lost event?

### How this differs from a real platform

- The shop's faults are invented for the course.
- The shop's path loses only the events the cell names. A real network loses, delays and repeats events at random.
- The shop's collector is never down. It acknowledges every event it receives at once.
- The OpenLineage specification says nothing about how an event travels, or what a consumer does with an event that never arrives (Chapter 8).

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 17](chapter_17.ipynb) · [Next: Chapter 19](chapter_19.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

