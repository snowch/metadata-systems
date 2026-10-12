# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Metadata at scale",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 22](chapter_22.ipynb)

    # Chapter 23: Metadata at scale

    **Objectives**

    - Measure the week's metadata.
    - Project it to 10,000,000 assets, and find which way of answering a question passes a limit first.
    - Delete old events, and find what lineage that loses.
    - Question the requirement "Keep lineage for 90 days."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 22's link, in a browser that had opened and run Chapter 22 (measured on a computer). Chapter 22's link opens this page in a new tab. Chapter 22 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 22 leaves more memory for this page.

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
    ## The week, counted

    The shop's metadata system holds the events of one week. The next cell counts what it holds.
    """)
    return


@app.cell
def _(shop):
    week23 = shop.run_week(["returns"])
    shop.scale.measure(week23)
    return (week23,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The week holds 11 assets, 6 jobs, 34 runs, 68 events, 67 edges by run and 14 edges by job, over 7 days. An event takes 1492 bytes on average.

    The week's rate is about 0.9 events per asset per day: 68 events, over 7 days, for 11 assets.

    The next cell lists, for each dataset, how many of the 14 edges by job a traversal downstream from it follows to the end, and the share of all 14 that is.
    """)
    return


@app.cell
def _(shop, week23):
    shop.scale.reach(week23)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From `orders.jsonl`, a traversal downstream follows 6 of the 14 edges by job: 0.43, the widest share. From `clean_orders`, it follows 4: 0.29.

    The projection below grows the platform from 10 assets to 10,000,000, in powers of ten: 10, 100, 1,000 and so on.

    At every size it keeps the week's rates: about 0.9 events per asset per day, the week's number of edges by job per asset, and a widest traversal that follows 0.43 of the edges.

    It keeps every event for 90 days, the time the head of the shop's requirement at the end of the chapter names.

    It counts the records each of three questions reads, each answered in two ways:

    - The latest run of one job: read every stored event, or read the events sorted by job and time.
    - One day's events: read every stored event, or read the events stored day by day.
    - What is downstream of one asset: follow the traversal to the end, or follow it 4 steps. At each step, each dataset leads to at most 3 edges, so 4 steps follow at most 81 edges.

    For each way, the projection gives the first of these sizes at which it reads more than 1,000,000 records.

    The limit of 1,000,000 records, the 4 steps and the 3 edges a step are the shop's own choices.

    Before you read on, write in the next cell which ways pass that limit first.
    """)
    return


@app.cell
def _():
    expected_first = """
Which ways of answering pass the limit first?
........
"""
    return


@app.cell
def _(shop, week23):
    shop.scale.first_over(week23)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The two questions that read every stored event pass the limit first, at 100,000 assets: the latest run of one job, and one day's events, each in its way that reads every stored event. The sizes go up in powers of ten, so each passes it somewhere between 10,000 and 100,000 assets.

    A structure that lets a question go straight to the records it needs, the way a book's index points to pages, is an **index**. The events sorted by job and time are one.

    With that index, the latest run reads 31 records at 10,000,000 assets: about 30 steps down the index, then one record. It never passes the limit.

    Storing records in separate parts by a key is a **partition**. Here the key is the day. One day's events read one part, and that way passes the limit only at 10,000,000 assets.

    Followed to the end, the traversal downstream passes the limit at 10,000,000 assets. Followed 4 steps, it reads at most 81 edges and never passes it.

    Compare this with what you wrote. The next cell lists the projection's numbers at each size.
    """)
    return


@app.cell
def _(shop, week23):
    shop.scale.project(week23)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Keeping less

    At 10,000,000 assets, the projection holds 794,805,210 events.

    Deleting events older than a set time is **retention**.

    The week holds 7 days of events, so 90 days would delete none of them. The next cell keeps the events no older than 3 days, measured at 09:00 on Monday 14, as a stand-in: 90 days deletes the same way, later.

    It lists the edges by run that remain and include `r-201.json`.

    The returns desk recorded the return `r-201` on Tuesday 8 at 14:20, and `record_return` read the file `r-201.json`.
    """)
    return


@app.cell
def _(shop, week23):
    events23 = shop.delivery.week_events(week23)
    kept = shop.scale.retain(events23, 3, "2026-09-14T09:00:00Z")
    found23 = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(kept)))
    print(len(events23), "events,", len(kept), "kept")
    shop.scale.lineage_of(found23.by_run, "r-201.json")
    return (events23,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The output shows 68 events, of which 28 are kept.

    No edge by run still includes `r-201.json`, because the run that read the file is no longer in the kept events.

    With 90 days, that run's events would be deleted after 14:20 on Monday 7 December.

    The next cell reads `r-201`'s row from the table `returns`.
    """)
    return


@app.cell
def _(week23):
    week23.warehouse.sql("SELECT * FROM returns WHERE return_id = 'r-201'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The row is still in `returns`. Chapter 10's SQL function `returned_quantity(7004, 2)` reads it.

    The row is still used. The record of the run that wrote it is gone.

    Folding each run's edges into one edge per job, before the events are deleted, is **compaction**. The folded edge keeps how many runs had it, and the first and last time.

    The next cell applies compaction to the whole week's events, and lists the edges by job that include `r-201.json`.
    """)
    return


@app.cell
def _(events23, shop):
    shop.scale.lineage_of(shop.scale.compact(events23), "r-201.json")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After compaction, `r-201.json` appears in one edge. `record_return` reads it, in 1 run, first and last at 14:20:05 on Tuesday 8.

    The shop keeps edges by job when it deletes events. The cell deleted nothing: keeping this edge is the shop's rule.

    The edge keeps that `record_return` read `r-201.json`, and when. It does not keep which run read the file, or what that run wrote.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Ninety days
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Keep lineage for 90 days."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what the requirement means to you here.
    """)
    return


@app.cell
def _():
    what_90_days_means = """
What does "lineage for 90 days" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The requirement could mean three things. Each is a question the head of the shop might be asking, with what it needs:

    - Can I see the events of the last 90 days? It needs the events kept for 90 days by age: retention.
    - Can I see which jobs read and wrote which assets in the last 90 days? It needs edges by job kept for 90 days, folded before the events are deleted: compaction. It keeps jobs, not runs.
    - Can I see how every asset still in use was made, however old it is? It needs a record of which assets are still in use, and lineage kept by use, not by age.

    The shop records nowhere which assets are in use. With 90 days' retention, the run that wrote `r-201`'s row would be deleted on Monday 7 December, while the row stays in `returns`.

    The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 24

    Kept at the week's rates, the metadata grows to 794,805,210 events at 10,000,000 assets. The ways that read every stored event passed the limit first, at 100,000 assets. The index kept the latest run under the limit at every size, and partitions by day kept one day's events under it until 10,000,000 assets. A traversal limited to 4 steps never passed the limit. Deleting events by age lost the run that wrote a row still in use. Compaction first kept the edge by job showing that `record_return` read `r-201.json`.

    Part V ends here. In Chapter 24, the first chapter of Part VI, you build a metadata store: as JSON documents, then as tables, then as an indexed store, then as a graph.

    - Which of your metadata system's questions read everything it stores?
    - How long does it keep events, and what is kept after?
    - Which of your assets depend on lineage older than that?

    ### How this differs from a real platform

    - The projection keeps the week's rates at every size. A real platform's rates differ by asset: some assets change every second, and many never change.
    - The projection keeps the widest share, 0.43, and 3 edges a step at every size. A real graph's shape changes as it grows.
    - The projection counts the records each question reads. It does not count writes, the work of keeping an index up to date, time, memory or the cost of each read.
    - The limit of 1,000,000 records, the 90 days and the 4 steps are the shop's own choices.
    - The word compaction means other things in other systems. Apache Kafka's log compaction, for example, keeps at least the last record for each key and removes older ones.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 22](chapter_22.ipynb)

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
