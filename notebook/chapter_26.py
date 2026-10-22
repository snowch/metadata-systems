# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Build the lineage graph",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 25](chapter_25.ipynb) · [Next: Chapter 27](chapter_27.ipynb)

    # Chapter 26: Build the lineage graph

    **Objectives**

    - Build the lineage graph one stored event at a time, with each edge's runs and its first and last time.
    - Find what a late event does to an edge's last time.
    - Save the graph and load it after the collector's restart, with its edges and times kept.
    - Question the requirement "Lineage must show the platform as it is now."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 25's link, in a browser that had opened and run Chapter 25 (measured on a computer). Chapter 25's link opens this page in a new tab. Chapter 25 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 25 leaves more memory for this page.

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
    ## Edges with their times

    Chapter 9 built the edges by job from all the week's events at once. Here the lineage graph is kept up to date as each event is stored, one event at a time, from the collector's file.

    The file is the collector's file from Chapter 25, with the shop's own versions of your three pieces, run over a longer week: the returns desk, Part V's faults, and the analyst's job `copy_clean_orders`, which copies `clean_orders` every night.

    From Sunday 13, `build_daily_sales` reads the analyst's copy instead of `clean_orders` (Chapter 9).

    The next cell reads the file: 82 events. That is 14 more than Chapter 25's 68. The copy job's 7 runs account for those, with 2 events each.
    """)
    return


@app.cell
def _(shop):
    week26 = shop.run_week(["returns", "source"])
    stored26 = shop.lineage_graph.stored(week26)
    print(len(stored26), "events in the file")
    return (week26,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each edge in the graph is one program reading or writing one dataset. For each edge, the graph keeps the runs that had it, and the first and last time an event named it.

    Those times are the events' own times, set by the programs that sent them. The order the events arrived in decides only the order in which the graph takes them (Chapter 20).

    `shop.lineage_graph.edges_of(event)` gives the edges that one event names. You write `add(edges, event)`, which updates the graph for one event.

    The next cell holds the function `add` as it stands. It creates an edge the first time an event names it, adds the event's run to that edge, and sets the edge's last time to the time of each event it takes.
    """)
    return


@app.cell
def _(shop):
    def add(edges, event):
        for key in shop.lineage_graph.edges_of(event):
            edge = edges.setdefault(
                key,
                {
                    "runs": set(),
                    "first": event["eventTime"],
                    "last": event["eventTime"],
                },
            )
            edge["runs"].add(event["run"]["runId"])
            edge["last"] = event["eventTime"]
    return (add,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The events reach the graph in the order they arrived. Wednesday 9's `COMPLETE` of `build_daily_sales` was held up. It arrived at 04:30:24 on Thursday 10, after Thursday 10's `COMPLETE` of `build_daily_sales` (Chapter 20).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide when the graph, as it stands at 09:00 on Thursday 10, will show that `build_daily_sales` last wrote `daily_sales`.
    """), kind="info")
    return


@app.cell
def _(add, shop, week26):
    shop.lineage_graph.check(week26, add)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The check runs 3 tests, in this order:

    1. The graph built from the whole file
    2. The graph as it stands at 09:00 on Thursday 10
    3. The graph saved and loaded again

    The third test saves the graph as one line for each edge (its runs, first time and last time) and loads it again after Chapter 25's restart, on Saturday 12 at 16:50:20. The graph is held in memory, like the collector's keys, so a restart loses it unless it is saved.

    <details><summary>The printed result, explained</summary>

    As `add` stands, 2 pass.

    The first test passes: built from the whole file, the graph has the same edges and run counts as Chapter 9's way of building edges by job gives for this file. This file has no line cut short, so `daily_sales` is written in 7 runs, not Chapter 9's 6.

    The third test passes: the loaded graph holds the same edges, runs and times as the one that was never saved.

    The second test fails: at 09:00 on Thursday 10, the graph shows `build_daily_sales` last wrote `daily_sales` at 02:30:21 on Wednesday 9, not on Thursday 10. Wednesday's `COMPLETE` arrived last, so `add` took it last and set the edge's last time from it.

    Compare this with what you decided.

    </details>

    Change `add` so that an edge's first time is the earlier of its first time and the event's time, and its last time is the later of its last time and the event's time. Select the cell with `add` and press **Run below**. All 3 tests pass.

    <details><summary>The printed result, explained</summary>

    No event in this week names an edge for the first time after a later event has named it, so the check cannot tell whether the first time is right. The earlier of the two times is still the rule that keeps it right when that happens.

    </details>

    The next cell builds the graph from the whole file and lists the edges of `build_daily_sales`, to show what the graph holds about Sunday's change of input.
    """)
    return


@app.cell
def _(add, shop, week26):
    graph26 = shop.lineage_graph.build(week26, add)
    shop.lineage_graph.table(graph26, "build_daily_sales")
    return (graph26,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `build_daily_sales` reads `clean_orders` in 5 runs, first at 02:30:00 on Tuesday 8 and last at 02:30:21 on Saturday 12.

    `build_daily_sales` reads the analyst's copy, `clean_orders_copy.csv`, in 2 runs, from 02:30:00 on Sunday 13 to 02:30:21 on Monday 14.

    `build_daily_sales` writes `daily_sales` in 7 runs.

    A first time of 02:30:00 is a run's `START`: the graph takes every event's time, `START`s included.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The platform now
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Lineage must show the platform as it is now."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "as it is now" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of the requirement</summary>

    Chapter 9 asked what "current" means for the edges by job, which kept no times. This graph keeps each edge's times, which allows one more reading: a window.

    "Now" could mean three things. Each item below says what it needs:

    - The edges of each program's latest run: needs each edge's last time and each program's latest run.
    - Every edge ever seen: needs every edge kept, and nothing removed.
    - The edges seen in the last 2 days: needs each edge's last time, and the length of the window.

    </details>

    The next cell shows, for each edge of `build_daily_sales` and of `record_return` at 09:00 on Monday 14, which of the three readings includes it.
    """)
    return


@app.cell
def _(graph26, shop):
    shop.lineage_graph.now(graph26, "2026-09-14T09:00:00Z")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    `build_daily_sales`'s reads of `clean_orders` are in "ever" only. Its reads of the analyst's copy, and its writes to `daily_sales`, are in all three readings.

    `record_return` last ran on Friday 11 at 13:15. Its read of `r-204.json` and its write to `returns` are in its latest run, but not in the last 2 days. Its reads of the other three return files are in "ever" only.

    So the latest run and the window disagree for a program that has not run for 2 days.

    The graph keeps each edge's first and last time, so it answers all three readings. Without times on its edges, the graph alone answers only "ever".

    The requirement does not say which reading it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 27

    - The graph, built one stored event at a time, had the same edges and run counts as Chapter 9's way of building them from the same file.
    - Setting an edge's last time from each event as it was taken let Wednesday's late `COMPLETE` make Thursday's write look older: Wednesday's 02:30:21.
    - Taking the earlier and the later of two times fixed the edge's last time.
    - Saved as lines and loaded after the restart, the graph kept its edges, runs and times.
    - The graph's times answered three readings of "now".

    The graph could not show whether an edge that has not been seen for a while has stopped or is only idle: `record_return` had not run for 2 days.

    Chapter 27 asks questions of this graph.

    - Does your lineage graph keep when each edge was last seen?
    - Which of your edges have not been seen for a week?
    - Which reading of "now" do your lineage views show?

    ### How this differs from a real platform

    - The shop's graph is held in memory and saved as a list of lines, one for each of its 17 edges. Chapter 23 projected what a platform of 10,000,000 assets holds.
    - The graph takes its times from the events' own times, which is the shop's choice. Those times give the order things happened in only while the programs' clocks agree (Chapter 20).
    - The window of 2 days is the shop's choice.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 25](chapter_25.ipynb) · [Next: Chapter 27](chapter_27.ipynb)

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
