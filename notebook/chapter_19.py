# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Duplicate events",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 18](chapter_18.ipynb) · [Next: Chapter 20](chapter_20.ipynb)

    # Chapter 19: Duplicate events

    **Objectives**

    - Find whether the lineage changes when one event arrives twice.
    - Find what changes when an event arrives again with a new time.
    - Tell a repeated event from work done twice.
    - Question the requirement "Ingestion must ignore duplicates."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 18's link, in a browser that had opened and run Chapter 18 (measured on a computer). Chapter 18's link opens this page in a new tab. Chapter 18 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 18 leaves more memory for this page.

    Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

    </details>
    """), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    **Running and saving the page**

    1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
    2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
    3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser. When the chapter is updated, the page shows the new version instead. If you changed a cell, your copy is kept under the chapter's name with "(your copy)" added, and [the list of files in this browser](https://snowch.github.io/metadata-systems/jupyterlite/tree/) opens it.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, shop):
    mo.Html(figures.figure(figures.pipeline(shop.run_week(["returns"]), "jobs nightly; functions at any hour"), "The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table `returns`."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The same event twice

    In the last cells of Chapter 18, delivery was at least once, and a lost acknowledgement made one event arrive twice.

    The `COMPLETE` event for the run of `build_daily_sales` early on Thursday 10 arrives twice, and the two copies are the same, byte for byte.

    Ingestion turns events into runs and edges, job by job (Chapter 9).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide whether the lineage will change, and how.
    """), kind="info")
    return


@app.cell
def _(shop):
    week19 = shop.run_week(["returns"])
    once = shop.delivery.send(week19)
    twice = shop.delivery.send(week19, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True)
    graph = lambda d: shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(d.events)))
    print(len(twice.events), "events received")
    print("The same graph as with each event received once:", graph(twice).by_job == graph(once).by_job)
    graph(twice).of("shop/build_daily_sales")
    return (week19,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The collector received 69 events, 1 more than the 68 sent.

    The cell compares every job's edges, with how many runs had each and the first and last time, against the graph built when each event was received once. They are the same: `True`.

    The cell then lists the edges of `build_daily_sales`: `reads` `clean_orders` in 7 runs, and `writes` `daily_sales` in 7 runs, the counts Chapter 18 showed with every event.

    Ingestion merges events into runs by their run id. The copy names the same run and the same datasets, so it adds nothing to the graph.

    Compare this with what you decided.

    ## A retry with a new time

    A program can build an event again when it sends it again, with the time of the new sending. The next cell sends the same `COMPLETE` that way, then lists the runs of `build_daily_sales` as ingestion records them.
    """)
    return


@app.cell
def _(shop, week19):
    retimed = shop.delivery.send(week19, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True, restamp=True)
    shop.ingest.objects(shop.ingest.normalise(retimed.events)).runs_of(job="shop/build_daily_sales", columns=["started", "ended"])
    return (retimed,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The run early on Thursday 10 started at 02:30:00 and now ends at 02:30:52. Runs of `build_daily_sales` take 21 seconds. This one seems to take 52 seconds.

    Ingestion takes a run's end from the time its last terminal event records. The copy records 02:30:52, later than the first's 02:30:21.

    The OpenLineage specification describes `eventTime` as "the time the event occurred at". The copy states the time it was sent again, so its time is wrong.

    Dropping events that repeat one already received is **deduplication**. What counts as a repeat depends on the key it compares.

    The next cell drops repeats by content: an event with the same content as one received before.
    """)
    return


@app.cell
def _(retimed, shop):
    deduped = shop.ingest.dedupe(retimed.events, "content")
    deduped.dropped
    return (deduped,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    By content, no event was dropped: the copy's time differs, so its content differs.

    The next cell ingests the events kept and lists the runs of `build_daily_sales`. The run early on Thursday 10 still ends at 02:30:52.
    """)
    return


@app.cell
def _(deduped, shop):
    shop.ingest.objects(shop.ingest.normalise(deduped)).runs_of(job="shop/build_daily_sales", columns=["started", "ended"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Change `"content"` to `"run"` in the cell that starts `deduped =`. Select that cell and press **Run below**.

    By run, a repeat is a second event with the same run id and the same type.

    By run, one event is dropped: the `COMPLETE` with the time 02:30:52. The event kept has the time 02:30:21.

    Deduplication keeps the first event it meets of each key, and the first copy arrived first.

    In the cell below it, the run early on Thursday 10 ends at 02:30:21 again.

    An operation is **idempotent** when doing it twice leaves the same result as doing it once. Here the operation is ingesting what the collector received.

    Ingesting an exact copy is idempotent for the graph. Ingesting a copy with a new time is not idempotent for the run's end time, unless repeats are dropped by run first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A notice delivered twice

    The returns desk corrected `r-202` on Thursday 10 at 09:30. Object storage sends a notice of each change, and each notice starts `record_return`.

    In the week below, object storage delivers the notice for the correction twice. So `record_return` starts twice for the one change, 25 seconds apart. Each run deletes the return's row from `returns` and writes it again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide what changes in the table `returns`, and what changes in the lineage.
    """), kind="info")
    return


@app.cell
def _(shop, week19):
    week19t = shop.run_week(["returns", "twice"])
    query = "SELECT * FROM returns ORDER BY return_id"
    week19t.warehouse.sql(query) == week19.warehouse.sql(query)
    return (week19t,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell shows `True`. `returns` is the same as in the week in which the notice came once. `record_return` is idempotent for the table.

    The next cell looks for runs started more than once for the same change to the same version of an object. It reads `shop_objectChange`, the facet each function's events carry (Chapter 9): the object, its version and the change.
    """)
    return


@app.cell
def _(shop, week19t):
    events_t = shop.delivery.week_events(week19t)
    shop.delivery.repeated_work(events_t)
    return (events_t,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The output lists 1 version that more than one run started for: `s3://shop-returns/r-202.json`, the version the correction wrote, with the change `overwritten` and 2 runs.

    The next cell lists the edges of `record_return` in the week in which the notice came once and in the week in which it came twice.
    """)
    return


@app.cell
def _(events_t, shop, week19):
    shop.ingest.edges_side_by_side("shop/record_return", label="notice", once=shop.delivery.week_events(week19), twice=events_t)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the lineage, `record_return` now writes `returns` in 6 runs, not 5.

    It reads `r-202.json` in 3 runs, not 2.

    The next cell drops repeats by run, and counts what it drops.
    """)
    return


@app.cell
def _(events_t, shop):
    len(shop.ingest.dedupe(events_t, "run").dropped)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell shows 0 dropped. The two runs have different run ids, so deduplication by run keeps both.

    They are not one event sent twice. They are the same work done twice.

    Deduplication by content and by run drops neither run. Only a key made from the object, its version and the change, from `shop_objectChange`, finds the two runs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Duplicates
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Ingestion must ignore duplicates."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what counts as a duplicate here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "duplicates"</summary>

    "Duplicates" could mean three things. Each needs a different key:

    - the same event twice: the event's content;
    - the same run reported twice, with a new time: the run id and the event type;
    - the same work done twice: the object, its version and the change.

    The shop's ingestion does not drop anything itself. Deduplication is a step you applied in these cells. Whether "Ingestion must ignore duplicates" is met, for each reading:

    - The same event: met for the graph by ingestion alone: the copy adds nothing. Deduplication by content also drops it.
    - The same run with a new time: not met by ingestion alone: the run's end time moves. Met when repeats are dropped by run before ingestion.
    - The same work: not met. The lineage holds two runs, and neither key of deduplication drops either.

    The requirement does not say which of these it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell(hide_code=True)
def _(shop):
    week = shop.run_week()
    storage, warehouse, reporting = week.storage, week.warehouse, week.reporting
    return reporting, storage, warehouse, week


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import shop
    from shop import figures
    return figures, mo, shop


if __name__ == "__main__":
    app.run()
