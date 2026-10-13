# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="OpenLineage in practice",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 28](chapter_28.ipynb) · [Next: Chapter 30](chapter_30.ipynb)

    # Chapter 29: OpenLineage in practice

    **Objectives**

    - See the names a real producer, Airflow's OpenLineage provider, gives the shop's nightly jobs.
    - Send the week's events, with Part V's faults, through Marquez's rules and through your collector, and compare what each keeps.
    - Change the order in which the events arrive, and find which differences that removes.
    - Question the requirement "Use the reference consumer."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 28's link, in a browser that had opened and run Chapter 28 (measured on a computer). Chapter 28's link opens this page in a new tab. Chapter 28 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 28 leaves more memory for this page.

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
    ## A real producer

    Parts II to VI built the shop's own producers, its collector and its graph. Real producers and consumers of OpenLineage events follow rules of their own.

    None of them runs on this page. Each cell applies a system's rule, as its code states it in the version read, to the shop's week.

    Suppose the shop's four nightly jobs ran as tasks of one Airflow Dag, `shop_nightly`, and sent their events through Airflow's OpenLineage provider, version 2.20.3.

    The provider names each task's job `{dag_id}.{task_id}`. It takes the job's namespace from its settings, and uses `default` when none is set.

    The next cell lists the shop's four nightly jobs as the shop names them and as the provider would, with the parent the provider gives each.
    """)
    return


@app.cell
def _(shop):
    week29 = shop.run_week(["returns"])
    shop.consumers.provider(week29)
    return (week29,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every name differs: the namespace is `default`, not `shop`, and the job is `shop_nightly.build_daily_sales`, not `build_daily_sales`.

    The shop's lineage would take the provider's four jobs as four new programs. Chapter 12 compared names this way, and Chapter 22 joined two names with an alias.

    The next cell shows the `START` of the run early on Friday 11 of `build_daily_sales` as the provider would send it. These differ from the shop's own event:

    - `producer` is the provider's address;
    - the facet `parent` names the Dag's run, in the job `default/shop_nightly`;
    - the facet `jobType` gives `AIRFLOW`, `BATCH` and `TASK`.

    The datasets keep the shop's names: the provider takes them from what each task reports.

    The cell after it runs Chapter 8's check on the event.
    """)
    return


@app.cell
def _(shop, week29):
    event29 = shop.consumers.provider_event(week29)
    print(shop.openlineage.show(event29))
    return (event29,)


@app.cell
def _(event29, shop):
    shop.openlineage.check(event29)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The event breaks none of the rules Chapter 8's check tests.

    ## The reference consumer

    OpenLineage's own README calls Marquez "the reference implementation of the OpenLineage API".

    Marquez's rules for a run's events, as its code states them:

    - it rejects an event with no `eventTime`;
    - it keeps every event it takes as a row, and nothing makes a row unique;
    - for each event with a type, it writes a state row and sets the run's current state from that event, in the order it takes the events, without comparing their times;
    - `COMPLETE` gives the state `COMPLETED`, `FAIL` gives `FAILED`, and `START` gives `RUNNING`, as does any type it does not know;
    - `COMPLETE`, `ABORT` or `FAIL` moves the run's end time to the event's own time.

    The next two cells send Chapter 25's arrivals, Part V's faults included, to your collector (the shop's versions of your three pieces from Chapter 25) and through Marquez's rules, in the order the events arrived.

    The run early on Friday 11 of `build_daily_sales` sent its `START` at 02:30:00 and its `COMPLETE` at 02:30:21. The `START` arrived at 02:31:03, after the `COMPLETE`.

    Before you read on, write in the next cell which state Marquez's rules set for that run after every arrival.
    """)
    return


@app.cell
def _():
    expected_state = """
Which state will Marquez's rules set for the run early on Friday 11?
........
"""
    return


@app.cell
def _(shop, week29):
    shop.consumers.compare(week29)
    return


@app.cell
def _(shop, week29):
    shop.consumers.totals(week29)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Friday 11: your collector's state is `COMPLETE`. By Marquez's rules, the state is `RUNNING`. The late `START` was the last event taken, so it set the state.

    Compare this with what you wrote.

    Thursday 10: the run's `COMPLETE` arrived again with a new time. Your collector dropped the repeat and kept the end at 02:30:21. Marquez's rules kept 3 event rows for the run and moved its end to 02:30:52.

    Saturday 12: `remove_return`'s `COMPLETE` arrived twice. Your collector kept 2 events for the run; Marquez's rules kept 3 rows.

    Over the week, both rejected the developer's event with no `eventTime`. Your collector stored 68 events, and Marquez's rules kept 70.

    The next cell holds `order`, the order in which the events reach Marquez's rules and your collector: `"arrival"`.

    Change it to `"event time"`: a buffer then holds the week's events and sends them sorted by their event time, Chapter 20's rule. Select the cell and press **Run below**.

    The check below tests whether Friday 11's run is in the same state in both.
    """)
    return


@app.cell
def _():
    order = "arrival"
    return (order,)


@app.cell
def _(order, shop, week29):
    shop.consumers.check(week29, order)
    return


@app.cell
def _(order, shop, week29):
    shop.consumers.compare(week29, order)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `"event time"`, the check passes: the run early on Friday 11 is `COMPLETED` by Marquez's rules and `COMPLETE` in your collector.

    The run early on Thursday 10 still ends at 02:30:52 by Marquez's rules: sorting does not drop a repeat with a new time. Saturday's repeat is still 3 rows.

    Putting events in order and dropping repeats are two separate jobs.

    The buffer here sorted the whole week before sending anything. A real buffer can hold events only for a while, and an event later than that still arrives out of order.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Using the reference consumer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Use the reference consumer."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "use the reference consumer" means to you here.
    """)
    return


@app.cell
def _():
    what_reference_means = """
What does "use the reference consumer" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "Use the reference consumer" could mean three things. Each item says what it needs:

    - use Marquez, the consumer the OpenLineage project names as its reference implementation: it needs nothing more, and the shop would hold Friday 11's run as `RUNNING` unless something sorts the events first;
    - use a consumer that does what the specification requires: the OpenLineage specification says nothing about repeats, late events or order, so Marquez's rules and your collector both meet it;
    - check your own consumer against the reference: it needs a way to decide which is right where they differ, and for Friday 11 that is a choice about order the specification leaves open.

    The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 30

    The provider gave the shop's jobs new names in a new namespace, so its events would start new programs in the shop's lineage.

    By Marquez's rules, a late `START` left a finished run `RUNNING`, and a repeat with a new time moved the run's end. Your collector kept `COMPLETE` and the first end time.

    Sorting the events by event time fixed the state, not the repeat.

    The page could not show Marquez itself: each result is Marquez's rules, as its code states them, applied here.

    Chapter 30 looks at where four systems' metadata comes from: Airflow, Spark, dbt and Trino.

    Three questions:

    - Which consumer takes your events, and in what order does it apply them?
    - What does it do with an event it has taken before?
    - Which of your jobs would a new scheduler rename?

    ### How this differs from a real platform

    - The cells apply the rules as Marquez's code states them in the version read. Marquez also keeps versions of jobs and datasets, facets and more, which the cells leave out.
    - The provider's run ids here are the shop's own, made from the values the provider uses.
    - No Marquez document says what it does with a repeated, late or out-of-order event: the rules here are its code's.
    - The OpenLineage specification says nothing about what a consumer does with a repeat or a late event.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 28](chapter_28.ipynb) · [Next: Chapter 30](chapter_30.ipynb)

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
