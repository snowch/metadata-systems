# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="From events to graphs",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 8](chapter_08.ipynb) · [Next: Chapter 10](chapter_10.ipynb)

    # Chapter 9: From events to graphs

    **Objectives**

    - Turn a week of received events into a graph, one stage at a time.
    - Find what a line that cannot be read takes out of the graph.
    - Give a stage a facet it does not know, and see what it adds.
    - Question the requirement "The graph must show the current lineage."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## From events to a graph

    The shop keeps every event it receives, each as one line of JSON, in the order it received them. The events come from the four jobs and the two functions. In Chapter 8 the analyst wrote one night's events by hand. Now the analyst's script sends its own events, each night.

    The head of the shop wants a graph of the platform kept up to date from these events, not drawn from lines written by hand as in Chapter 6.

    Turning received events into stored records and graph edges is **ingestion**. The shop's ingestion has four stages, each a function you run and inspect: parse, which reads each line; a stage that writes the same thing the same way; objects, which makes jobs, runs and datasets; and edges.
    """)
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
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 8's link, in a browser that had opened and run Chapter 8 (measured on a computer). Chapter 8's link opens this page in a new tab. Chapter 8 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 8 leaves more memory for this page.

    Running every cell took 9 to 12 seconds, and the page used about 410 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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
    The next cell runs the week with the returns desk and the `source` change, in which `build_daily_sales` reads the analyst's copy from Saturday's row on. It collects the week's event lines, and prints how many there are and the start of the first.
    """)
    return


@app.cell
def _(shop):
    week9 = shop.run_week(["returns", "source"])
    lines = shop.ingest.event_lines(week9)
    print(len(lines), "lines")
    print(lines[0][:120], "...")
    return (lines,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Parse

    Parsing turns each line of text into an event. A line that is not JSON, or that breaks the specification's rules, is refused, with its line number and why.

    The next cell cuts one line short, as if part of it were lost on the way: the COMPLETE of `build_daily_sales`'s run on Wednesday 9. It then parses every line and lists the lines refused.
    """)
    return


@app.cell
def _(lines, shop):
    damaged = list(lines)
    k = next(i for i, line in enumerate(damaged) if '"build_daily_sales"' in line and '"COMPLETE"' in line and "2026-09-09" in line)
    damaged[k] = damaged[k][:150]
    parsed = shop.ingest.parse(damaged)
    parsed.refused
    return (parsed,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The week has 82 lines. One is refused: line 20, which is not JSON. 81 events pass.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide what the graph will lose because of that line.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Normalise

    Producers write the same thing in different ways. The functions' producer writes times with `+00:00`; the jobs' producer writes `Z`. Both mean UTC.

    The analyst's script names `clean_orders` without its database: it writes `analytics.clean_orders`.

    To **normalise** events is to rewrite such things in one form, so that the same thing is written the same way.

    The shop's stage writes every time in UTC with `Z`, and adds the database `shop` to a warehouse name that leaves it out.

    The next cell normalises the events and lists every change it made.
    """)
    return


@app.cell
def _(parsed, shop):
    normal = shop.ingest.normalise(parsed)
    normal.changes
    return (normal,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    The stage made 26 changes: 12 times, in the functions' events (6 runs, 2 events each), and 14 names, in the analyst's events (7 nights, 2 events each).

    Without the change to the names, the analyst's copy would not join `clean_orders`, as in Chapter 8.

    The rule for names is the shop's. It fits a warehouse with one database; where two databases hold tables of the same name, it would join tables that are not the same.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Objects

    The next stage makes jobs, runs and datasets from the events. A run's state is the type of its latest event, by time.

    It reads fields only from the facets it knows: `nominalTime`, `jobType`, `sourceCodeLocation`, `inputStatistics`, `outputStatistics` and `version`. It lists any other facet and does not read it.

    The next cell builds the objects and shows how many of each it made.
    """)
    return


@app.cell
def _(normal, shop):
    known = dict(shop.ingest.KNOWN)
    # known["shop_objectChange"] = ["object", "version", "change"]
    objs = shop.ingest.objects(normal, known)
    objs
    return (objs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The stage made 7 job records, one for each program that sent events: the four jobs, the two functions and the analyst's script. It made 41 run records and 12 dataset records, and it listed 6 facets it does not read.

    The next cell lists the runs whose latest event is a `START`.
    """)
    return


@app.cell
def _(objs):
    objs.runs_of(state="START", columns=["job", "state", "started", "ended", "reads", "writes"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One run is `build_daily_sales` on Wednesday 9. Its `COMPLETE` line was cut short.

    Its stored record has the state `START`, a start time, an input, no end time and no output. That is the same stored record as a run still working.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A facet the stage does not read

    The next cell lists the facets the stage does not read. The cell after it asks for the runs of `record_return`: when each started, what it read, and the change and the version of the file from the facet `shop_objectChange`.
    """)
    return


@app.cell
def _(objs):
    objs.unknown
    return


@app.cell
def _(objs):
    objs.runs_of("shop/record_return", columns=["started", "reads", "shop_objectChange.change", "shop_objectChange.version"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All 6 facets are `shop_objectChange`, on the runs of the two functions.

    The table of `record_return`'s runs has two columns: when each started, and what it read. The change and the version are missing: the stage did not read the facet.

    In the cell that starts `known = dict(`, delete the `# ` at the start of the line `known["shop_objectChange"] = ...`. Select that cell and press **Run below**. Then compare the two tables with what they showed before.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Edges

    The last stage makes edges of two kinds. An edge by run joins one run to a dataset it read or wrote. An edge by job joins a job to a dataset that any of its runs read or wrote. It is made once per dataset. It records how many runs had it, and the first and last time one did.

    The week has 41 runs: 35 by night (7 nights, each with the four jobs and the analyst's script) and 6 by the functions, during the day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide how many edges of each kind you expect, and why.
    """), kind="info")
    return


@app.cell
def _(objs, shop):
    found = shop.ingest.edges(objs)
    found
    return (found,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    There are 80 edges by run and 17 edges by job.

    Each night's runs repeat the same reads and writes. They add edges by run, about one night's worth each night. They add no edge by job, which counts its runs instead.

    `record_return` adds an edge by job for each file it read.

    </details>

    The next cell lists the edges by job of `build_daily_sales`.
    """)
    return


@app.cell
def _(found):
    found.of("shop/build_daily_sales")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `build_daily_sales` has 3 edges by job. It reads `clean_orders` in 5 runs, the first at `2026-09-08T02:30:21Z` and the last at `2026-09-12T02:30:21Z`. It reads the analyst's copy in 2 runs, on Sunday 13 and Monday 14. It writes `daily_sales` in 6 runs, not 7. The `COMPLETE` line of the run on Wednesday 9 was cut short, so the stored record of that run has no output. Its `START` named its input, so its read is counted.

    The edge to `daily_sales` stays, because other runs had it. Only its count of runs, and the missing edge by run for Wednesday, show the loss.

    The next cell draws the edges by job, in the order data flows, as Chapter 6's drawing did.
    """)
    return


@app.cell
def _(found):
    found.graph().drawing(label="orders.jsonl goes through build_clean_orders to shop.analytics.clean_orders, which copy_clean_orders reads to write clean_orders_copy.csv, and which build_daily_sales reads as well as the copy, to write shop.analytics.daily_sales, which refresh_dashboard reads to write sales_dashboard. Four return files are read by record_return, which with remove_return writes shop.analytics.returns; customers.jsonl goes through build_clean_customers to shop.analytics.clean_customers.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Three meanings of "current"
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "The graph must show the current lineage."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the block below, which holds three readings of "current", decide what you take "current" to mean.
    """), kind="info")
    return



@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Three readings of "current"</summary>

    "Current" could mean three things, each needing something different:

    - As of the last event received: every edge by job;
    - As of each job's latest run: each edge's last time, set against the time of its job's latest run;
    - As of the last change to a job's code: the code version of each run, set against the runs on each edge.

    The readings differ for `record_return`. Its code did not change during the week, so the third reading keeps every file it read. Its latest run read only `r-204.json`, so the second keeps that one file alone.

    </details>

    The next cell lists, for each job, the edges its latest run had: the second reading's answer.
    """)
    return

@app.cell
def _(found):
    found.latest()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    That cell lists 13 of the 17 edges by job. It leaves out `build_daily_sales` reading `clean_orders` (the last such run was on Saturday 12), and `record_return` reading `r-201.json`, `r-202.json` and `r-203.json`. The rows of `r-201` and `r-202` are still in the table `returns`. The row of `r-203` was removed when its file was deleted.

    By reading:

    - As of the last event received: met; the edges by job hold all 17;
    - As of each job's latest run: met; the cell above gives it;
    - As of the last change to a job's code: not met by the edges by job alone; the stage keeps each run's code version (from `sourceCodeLocation`), and a query would have to join the runs to the edges.

    The requirement does not say which "current" it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 10

    Four stages turned the week's events into a graph. A line cut short was refused at the first stage; its run then looked as though it were still working, and the edge to `daily_sales` counted 6 runs, not 7. Normalising joined the analyst's names to the jobs'. A facet the stage did not know was listed and not read, until you added it. The same reads and writes, night after night, made 80 edges by run and 17 by job. "Current" had three readings.

    The events do not show which columns each column is made from. Chapter 6 noted that `revenue_pence` is made from `price_pence` and `quantity`; no event here says so.

    Chapter 10 reads the jobs' SQL to find which columns each column is made from.

    - What does a platform you work on do with an event it cannot read?
    - Which two producers on that platform might name one table differently, and which rule would join them?
    - Which reading of "current" does your own team need, and for what?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop and its four stages are the course's own. Every rule in them is the shop's choice: the forms it normalises to, a run's state from its latest event, and the facets it reads.

    Here the week's events are made at once, after the week has run. A real platform receives them one at a time, over a network, while the jobs run.

    Chapter 29 compares how real consumers store events.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 8](chapter_08.ipynb) · [Next: Chapter 10](chapter_10.ipynb)

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
