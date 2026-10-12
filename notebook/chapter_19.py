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
    3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.
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

    In Chapter 18, delivery was at least once. A lost acknowledgement made one event arrive twice.

    Here, the `COMPLETE` event for the run of `build_daily_sales` early on Thursday 10 arrives twice. The two copies are the same, byte for byte.

    Ingestion turns events into runs and edges, job by job (Chapter 9).

    Before you read on, write in the next cell whether the lineage will change, and how.
    """)
    return


@app.cell
def _():
    expected_lineage = """
Will the lineage change, and how?
........
"""
    return


@app.cell
def _(shop):
    week19 = shop.run_week(["returns"])
    once = shop.delivery.send(week19)
    twice = shop.delivery.send(week19, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True)
    graph = lambda d: shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(d.events))).by_job
    len(twice.events), graph(twice) == graph(once)
    return (week19,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell shows `69` and `True`. The collector received 69 events, 1 more than the 68 sent. The job graph built from them is the same as the graph built from the week with each event sent once.

    Ingestion keys each run by its id (Chapter 9), and adds an edge to a run only once. A second copy of the same event adds nothing to the graph.

    Compare this with what you wrote.

    ## A retry with a new time

    Some programs build an event again when they send it again, with the time of the new sending. The next cell sends the same `COMPLETE` that way, then lists the runs of `build_daily_sales` as ingestion records them.
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
    The run early on Thursday 10 started at 02:30:00 and now ends at 02:30:52. Runs of `build_daily_sales` take 21 seconds. This one seems to take 52 seconds. Ingestion took the end time from the later copy.

    Dropping events that repeat one already received is **deduplication**. What counts as a repeat depends on the key it compares.

    The next cell drops repeats by content: an event that is the same as one received before, byte for byte.
    """)
    return


@app.cell
def _(retimed, shop):
    shop.ingest.dedupe(retimed.events, "content").dropped
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    By content, no event was dropped. The copy has a different time, so its content differs.

    Change `"content"` to `"run"` in the cell above. Then select that cell and press **Run below**. By run, a repeat is a second event with the same run id and the same type.

    By run, one event is dropped: the `COMPLETE` with the time 02:30:52. The event kept has the time 02:30:21.

    An operation is **idempotent** when doing it twice leaves the same result as doing it once. Ingestion keyed by run id is idempotent for the graph's edges. It is not idempotent for a run's end time, unless repeats are dropped by run first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A notice delivered twice

    The returns desk corrected `r-202` on Thursday 10 at 09:30. Object storage sends a notice of each change, and each notice starts `record_return`.

    In the week below, object storage delivers the notice for the correction twice. So `record_return` starts twice for the one change, 25 seconds apart. Each run deletes the return's row from `returns` and writes it again.

    Before you read on, write in the next cell what changes in the table `returns`, and what changes in the lineage.
    """)
    return


@app.cell
def _():
    expected_twice = """
What changes in returns?
........

What changes in the lineage?
........
"""
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

    The next cell looks for runs started more than once for the same change to the same version of an object. It uses the object facet that each function's events carry.
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
    The output lists 1 version that more than one run started for: `s3://shop-returns/r-202.json`. It is the version the correction wrote, shown as `overwritten`, with 2 runs.

    In the lineage, `record_return` now writes `returns` in 6 runs, not 5.

    The next cell drops repeats by run and counts what it dropped.
    """)
    return


@app.cell
def _(events_t, shop):
    len(shop.ingest.dedupe(events_t, "run").dropped)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell shows 0 dropped. The two runs have different run ids, so deduplication by run keeps both. They are not one event sent twice. They are the same work done twice.

    Only a key made from the object and its version finds the two runs.
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
    mo.md(r"""
    Before you read on, write in the next cell what counts as a duplicate here.
    """)
    return


@app.cell
def _():
    what_duplicates_means = """
What counts as a duplicate here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "Duplicates" could mean three things. Each needs a different key:

    - the same event twice: the event's content;
    - the same run reported twice, with a new time: the run id and the event type;
    - the same work done twice: the object and the version a run read.

    Then, for each of the three, here is what the shop's ingestion does:

    - the same event: no edge changes, and deduplication by content drops it;
    - the same run reported twice: no edge changes, and the run's end time moves, unless repeats are dropped by run;
    - the same work done twice: two runs in the lineage, and no event key drops either.

    The requirement does not say which of these it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 20

    An event received twice left the graph unchanged, because ingestion keys runs by their id. A retry with a new time moved a run's end time until repeats were dropped by run. A notice delivered twice ran a function twice. That left `returns` the same and added an extra run to the lineage. No event key caught it.

    Chapter 20 asks what happens when events arrive in a different order from the order in which they happened.

    - Which key does your platform's ingestion use to recognise an event it has seen?
    - Which of your programs are idempotent, and which would do the work twice?
    - Where would you look to tell a retried event from a second run?

    ### How this differs from a real platform

    - The shop's faults are invented for the course.
    - The shop's ingestion keeps every event it has ever received, so it can compare a new event with all of them.
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
