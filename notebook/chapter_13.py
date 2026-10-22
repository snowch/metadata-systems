# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Runtime metadata",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 12](chapter_12.ipynb) · [Next: Chapter 14](chapter_14.ipynb)

    # Chapter 13: Runtime metadata

    **Objectives**

    - Read what each run recorded while it ran.
    - Measure how recent each asset is, two ways, after a night that failed.
    - Find the nights that wrote nothing, and two clocks that disagree.
    - Question the requirement "The dashboard must be fresh."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 12's link, in a browser that had opened and run Chapter 12 (measured on a computer). Chapter 12's link opens this page in a new tab. Chapter 12 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 12 leaves more memory for this page.

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
    ## Monday after a failed night

    The week is Chapter 2's, with its failed night: on the last night, early on Monday 14, `build_daily_sales` fails and writes nothing. `refresh_dashboard` runs after it, as every night, and redraws the dashboard from `daily_sales`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "The dashboard must be fresh."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which of `orders.jsonl`, `clean_orders`, `daily_sales` and `sales_dashboard` you think are not up to date at 09:00 on Monday, and how you would tell.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What each run recorded

    A fact recorded about a run while it ran is an **observation**: when it started, how long it took, its status, the rows it read and wrote, the size of the table or file after the run, and any error.

    The next cell lists the observations of the week's runs, from the shop's record of each run.

    `size after (bytes)` is the size of the table or file as it stood after the run, not the bytes the run wrote. For a table it is the catalogue's estimate. The dashboard has no size.

    The shop's events (Chapters 7 and 8) carry the times, the status and the row counts. They carry neither the size nor the error.
    """)
    return


@app.cell
def _(shop):
    week13 = shop.run_week(["failed"])
    shop.observe.observations(week13)
    return (week13,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    28 runs. One failed: `run-027`, `build_daily_sales`, at 02:30 on Monday 14, after 21 seconds, with the error `database is locked`.

    A failed run records no counts, so its count columns are blank. Blank is not 0: the record does not show how many rows it wrote.

    `run-028`, `refresh_dashboard`, ran after it and succeeded: it read 6 rows of `daily_sales` and showed 6 days.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How recent each asset is

    How recent an asset's data is, measured one way or another, is its **freshness**.

    There are two measures: when the asset's store records it was last written; and the latest day its data holds.

    The next cell lists both for each asset, and how many hours before 09:00 on Monday it was last written.
    """)
    return


@app.cell
def _(shop, week13):
    shop.observe.freshness(week13)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    By the time it was last written, the dashboard is the most recent of the four: 6.0 hours before 09:00 on Monday.

    By the latest day it holds, the dashboard is a day behind. It holds Saturday 12, and on Monday the day before is Sunday 13. `daily_sales` holds the same latest day.

    Compare these with what you decided.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "The dashboard must be fresh."

    "Fresh" could mean three things, each needing something different:

    - refreshed lately: the reporting tool's record of the last refresh;
    - built from the latest data: along the lineage that feeds the dashboard, each asset written after the asset it is made from, by the times their stores record;
    - showing the latest day: the latest day the dashboard shows, against the day before.

    The next cell tests the dashboard against all three.
    """)
    return


@app.cell
def _(shop, week13):
    shop.observe.readings(week13)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The second and third readings are not met. The next cell shows each step of the second reading.
    """)
    return


@app.cell
def _(shop, week13):
    shop.observe.chain(week13)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `daily_sales` was last written at 02:30:21 on Sunday 13, before `clean_orders` was, at 02:05:52 on Monday 14. It was not written after its input.

    Chapter 2's failed night met the first reading and neither of the others. The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Nights that wrote nothing

    Chapter 11's `renamed` change: from the export that runs early on Sunday 13, `orders.jsonl` has `qty` where it had `quantity`.

    Before you read on, decide which of the three readings the dashboard will meet in this week.

    The next cell lists the runs that wrote no rows. The cell after it tests the dashboard against the three readings.
    """)
    return


@app.cell
def _(shop):
    week13r = shop.run_week(["renamed"])
    shop.observe.observations(week13r, rows_written=0)
    return (week13r,)


@app.cell
def _(shop, week13r):
    shop.observe.readings(week13r)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4 runs: `build_clean_orders` and `build_daily_sales`, on Sunday 13 and on Monday 14. Each succeeded.

    `build_clean_orders` read 43 rows and then 48, and wrote 0 each time. On Saturday 12 it had written 31. A count of 0 stands out only beside the rows read and the counts of earlier nights.

    Refreshed lately and built from the latest data are met. Showing the latest day is not. The dashboard's latest day is Friday 11, two days before Sunday 13.

    By status and by time, the dashboard is up to date. By the rows written against earlier nights, and by its latest day, it is not.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Two clocks

    The next cell runs the week with another change and shows each step of the second reading, by the times each store records.
    """)
    return


@app.cell
def _(shop):
    week13c = shop.run_week(["clock"])
    shop.observe.chain(week13c, by="stores")
    return (week13c,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The reporting tool records the dashboard's last refresh at 02:20:09 on Monday. `daily_sales` was last written at 02:30:21. By these times the dashboard was refreshed before its input.

    Was it? The next cell shows what the dashboard holds.
    """)
    return


@app.cell
def _(week13c):
    week13c.reporting.dashboard()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dashboard shows Sunday 13 (`2026-09-13`). `daily_sales` held a row for Sunday 13 only from 02:30:21, so the refresh came after it.

    In this week the reporting tool's clock runs 40 minutes slow: the `clock` change. Its times are 40 minutes early.

    In the cell before the dashboard's, change `by="stores"` to `by="runs"`, select that cell and press **Run below**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `by="runs"`, each time is when the last run that wrote the asset finished, by the one clock the shop's platform keeps for its runs. That includes the export, which sends no events. Its time is the platform's record of its run.

    By that clock the refresh finished at 03:00:09, after `daily_sales` was written at 02:30:21.

    The order holds only while one clock stamps every run. Where each machine keeps its own clock, two of them can disagree in the same way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A table written at any hour

    The returns desk writes the table `returns` whenever a return changes, at any hour.

    Is `returns` up to date at 09:00 on Monday, and by which measure?

    The next cell prints the time of the last change to the bucket `shop-returns`, then how recent each asset is in the week with the returns desk.
    """)
    return


@app.cell
def _(shop):
    week13d = shop.run_week(["returns"])
    print(
        "last change to shop-returns:", shop.observe.source_changed(week13d)
    )
    shop.observe.freshness(week13d)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `returns` was last written at 16:50:04 on Saturday 12, 40.2 hours before 09:00 on Monday. By the test that "refreshed lately" uses, written within a day, it is not up to date.

    Its latest day, Friday 11, is when the latest return still in the table was made (`r-204`).

    The bucket last changed at 16:50:00 on Saturday 12, when the desk deleted `r-203`. Nothing has changed since. The table was written 4 seconds later.

    For a table written when its source changes, freshness is measured against the source's last change, not against the night.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 14

    After the failed night, `daily_sales` and the dashboard held Saturday 12 as their latest day. By the time it was last written, the dashboard was the most recent asset. Compare these with what you decided at the start.

    "Refreshed lately" was met after the failed night, after the nights that wrote nothing, and with the slow clock. It caught neither fault. "Built from the latest data" failed after the failed night, and with the slow clock until one clock was used. "Showing the latest day" failed after the failed night and after the nights that wrote nothing. The requirement does not choose among them.

    Observations recorded how each run went, the failed run's error included, and a count of 0 stood out against earlier nights. A table written at any hour was measured against its source.

    Neither the observations nor the freshness measures show what the rows each run read held: how many orders had no customer id, or appeared twice.

    Chapter 14, the first chapter of Part IV, records what each run finds in the rows it reads.

    - What does your platform record about a run that succeeded and wrote nothing?
    - Which clocks stamp the times your platform compares?
    - Which of your tables are written when something changes, not on a schedule, and how would you say whether they are up to date?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    - The shop's runs, their times and their errors are invented for the course.
    - OpenLineage defines a run facet, `errorMessage`, for a failed run's message, and the output dataset facet `outputStatistics` holds a row count and the size in bytes written. The shop's events carry the row counts, not the size or the error.
    - The shop's size column is a table's or a file's size after the run, not the bytes the run wrote.
    - The three readings, and the rule of a day for "refreshed lately", are the shop's own choices.
    - The shop's reporting tool keeps its own clock, and in the `clock` change it runs slow. Every machine on a real platform keeps its own clock too.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 12](chapter_12.ipynb) · [Next: Chapter 14](chapter_14.ipynb)

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
