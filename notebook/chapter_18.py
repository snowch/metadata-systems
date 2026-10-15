# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Missing events",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 17](chapter_17.ipynb) · [Next: Chapter 19](chapter_19.ipynb)

    # Chapter 18: Missing events

    **Objectives**

    - Send the week's events, lose one, and build the graph from what arrived.
    - Find the runs that started and never ended, and what the events cannot tell you about them.
    - Send an event again until it is acknowledged, and see what that costs.
    - Question the requirement "Lineage must be complete."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 17's link, in a browser that had opened and run Chapter 17 (measured on a computer). Chapter 17's link opens this page in a new tab. Chapter 17 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 17 leaves more memory for this page.

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
    ## From the programs to the collector

    The program that receives the shop's events and keeps them for ingestion is the shop's **collector**. In the earlier chapters, the collector received every event the shop's programs sent, each one once and in order.

    Each program sends each event to the collector over the network. In the shop, a program sends an event 1 second after the time the event records, and the collector receives it 2 seconds later.

    The path an event takes from a program to the collector, and whether the event arrives, is its **delivery**.

    The next cell sends the week's events, with the returns desk's events among them, and counts what the collector received.
    """)
    return


@app.cell
def _(shop):
    week18 = shop.run_week(["returns"])
    sent = shop.delivery.send(week18)
    sent
    return sent, week18


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell sent 68 events, and the collector received 68. None was lost.

    Now one event is lost: the `COMPLETE` of the run of `build_daily_sales` early on Thursday 10. Its `START` arrives.

    The graph from Chapter 9 lists each job's edges, with how many runs had each one. With every event, `build_daily_sales` has two edges: `reads` to `clean_orders` in 7 runs, and `writes` to `daily_sales` in 7 runs. A run reports its outputs in its `COMPLETE` (Chapter 8).

    In Chapter 9, a `COMPLETE` line was cut short inside the shop's own store of events. Here the `COMPLETE` is lost on its way to the collector, before anything stores it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide what the graph will show for `build_daily_sales` when that `COMPLETE` never arrives: which edges, and how many runs each.
    """), kind="info")
    return


@app.cell
def _(shop, week18):
    lost = shop.delivery.send(week18, lose=["build_daily_sales COMPLETE 2026-09-10"])
    found = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(lost.events)))
    found.of("shop/build_daily_sales")
    return (lost,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both edges are still there. `writes` now has 6 runs, not 7. `reads` still has 7.

    The other 6 runs that wrote `daily_sales` carry the `writes` edge. The lost `COMPLETE` changes only the count of runs, as in Chapter 9.

    Compare this with what you decided.

    A run with a `START` at the collector and no `COMPLETE`, `ABORT` or `FAIL` is an open run.

    The next cell lists the open runs at 09:00 on Monday 14. For each one it shows the seconds since the run started (`seconds since`), and how many seconds that job's runs that ended usually took (`usual seconds`).
    """)
    return


@app.cell
def _(lost, shop):
    shop.delivery.open_runs(lost.events, "2026-09-14T09:00:00Z")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell lists one open run: `build_daily_sales`, started at 02:30:00 on Thursday 10. That is 369000 seconds before Monday 09:00, more than four days. The job's runs that ended took 21 seconds.

    That gap suggests the `COMPLETE` was lost. It does not prove it: a run that hangs and never ends leaves the same events at the collector, a `START` and nothing after it.

    So the events at the collector cannot settle whether the run ended. Evidence from outside the events can: what the run wrote.

    The run early on Thursday 10 writes Wednesday 9's row of `daily_sales`, and each run of `build_daily_sales` writes one row. The next cell reads that row from the warehouse.
    """)
    return


@app.cell
def _(week18):
    week18.warehouse.sql("SELECT * FROM daily_sales WHERE day = '2026-09-09'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The row is there: 15375 pence for Wednesday 9.

    The row shows that the run wrote it. It does not show how the run ended: a run can write its row and then fail.

    ## A function that ran once

    `remove_return` ran once in the week: on Saturday 12 at 16:50:02, when the returns desk deleted `r-203`.

    Its `START` names no dataset. It carries the object it was started for, `s3://shop-returns/r-203.json`, in its `shop_objectChange` facet. Its `COMPLETE` names the dataset it wrote, `returns`.

    The next cell loses that `COMPLETE` and builds the graph from what arrived.
    """)
    return


@app.cell
def _(shop, week18):
    lost_once = shop.delivery.send(week18, lose=["remove_return COMPLETE"])
    found_once = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(lost_once.events)))
    found_once.of("shop/remove_return")
    return (lost_once,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `remove_return` has no edge in the graph. With every event, it has one edge: it writes `returns`.

    The `START` that arrived names the object `r-203.json`, not the table `returns`.

    The graph now shows `record_return` as the only program that writes `returns`.

    The next cell lists the open runs again.
    """)
    return


@app.cell
def _(lost_once, shop):
    shop.delivery.open_runs(lost_once.events, "2026-09-14T09:00:00Z")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The open run of `remove_return` started at 16:50:02 on Saturday 12. Its `usual seconds` is empty: the function has no other run that ended.

    ## Sending again

    So far, each program sends each event once and keeps nothing. A lost event is gone.

    The alternative is for the collector to acknowledge each event it receives. The program keeps each event until it is acknowledged. It sends the event again if no acknowledgement comes within 30 seconds. Then every event sent arrives once or more. This delivery is **at least once**.

    The next cell loses the same `COMPLETE` once, sends with `at_least_once=True`, and lists the events that were sent or received more than once.
    """)
    return


@app.cell
def _(shop, week18):
    again = shop.delivery.send(week18, lose=["remove_return COMPLETE"], at_least_once=True)
    again.retried()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `COMPLETE` records the time 16:50:04 on Saturday 12.

    The program sent it at 16:50:05. No acknowledgement came, so it sent it again at 16:50:35, 30 seconds later.

    The collector received it once, at 16:50:37.

    Next, the `COMPLETE` arrives and its acknowledgement is lost instead.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you change the cell, decide how many times the collector will receive the `COMPLETE`.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the cell that ends `again.retried()`, change `lose=` to `lose_ack=`. Select that cell and press **Run below**.

    With `lose_ack`, the `COMPLETE` is sent twice and received twice: at 16:50:07 and at 16:50:37.

    The first copy arrived, and its acknowledgement was lost, so the program sent it again at 16:50:35.

    Compare this with what you decided.

    At least once delivers every event the program sends, and can deliver one twice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Complete lineage
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Lineage must be complete."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "complete" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "complete"</summary>

    "Complete" could mean three things, each needing something different:

    - Every event a program sends arrives. It needs delivery at least once, or a path that loses nothing.
    - Every program that changes the data sends events. It needs each such program to send them.
    - Every run's end is known, and so its edges. It needs a `COMPLETE`, `ABORT` or `FAIL` at the collector for each run that has ended.

    The shop's records meet these as follows:

    - Every event sent arrives: met with at least once, not without it. One lost `COMPLETE` left a run open, and for `remove_return` left no edge.
    - Every program that changes the data: not met. The export sends no events (Chapter 13).
    - Every run's end: met with at least once for a run whose program sent its end. Not met for a program that stops before it sends its `COMPLETE`, `ABORT` or `FAIL`, or for a run that has not ended: there is no end to send again.

    Compare these with what you decided.

    The requirement does not say which of these it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 19

    The lost `COMPLETE` of `build_daily_sales` left both its edges in the graph, because the job's other runs carried them. It left one run open. The events at the collector could not tell a lost `COMPLETE` from a run that never ended. The time since it started suggested a loss, and the warehouse's row showed that the run had written its row, not how the run ended. For `remove_return`, which ran once, the lost `COMPLETE` left no edge. Sending again until acknowledged delivered the event. A lost acknowledgement delivered it twice.

    Chapter 19 asks what ingestion does with an event it receives twice.

    - Which of your platform's programs send no events at all?
    - What does your collector do with an event it has already received?
    - How would you tell a slow run from a lost event?

    ### How this differs from a real platform

    - The shop's faults are invented for the course.
    - The shop's path loses only the events the cell names. A real network loses, delays and repeats events at random.
    - The shop's collector is never down. It acknowledges every event it receives at once.
    - The OpenLineage specification says nothing about how an event travels, or what a consumer does with an event that never arrives (Chapter 8).
    - The OpenLineage documentation's run-cycle page says a streaming job's runs have no expected terminal event under normal operation. For such a job, an open run is normal.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 17](chapter_17.ipynb) · [Next: Chapter 19](chapter_19.ipynb)

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
