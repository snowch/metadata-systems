# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="OpenLineage",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 7](chapter_07.ipynb) · [Next: Chapter 9](chapter_09.ipynb)

    # Chapter 8: OpenLineage

    **Objectives**

    - Find where each of Chapter 7's fields goes in an open standard's events.
    - Find what a program that receives the events holds after each one.
    - Check an event written by hand, and find why two names for one table do not join.
    - Question a requirement about the events the shop's programs must send.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A form other programs can read

    The head of the shop wants to see the shop's runs in a tool the shop did not write.

    Chapter 7's events use field names the shop chose. A tool written elsewhere would have to learn them, and the field names of every other shop it reads from.

    **OpenLineage** is an open specification for events about data processing. It sets their form, so that a program written by one team can send them and a program written by another can read them. It defines three kinds of event. This chapter uses one, the run event, which describes a run of a job. The other two describe a job, or a dataset, on its own.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head's requirement reads "Our programs must emit OpenLineage."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To emit an event is to send it.
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

    The page downloaded less than 1 MB when opened from Chapter 7's link, in a browser that had opened and run Chapter 7 (measured on a computer). Chapter 7's link opens this page in a new tab. Chapter 7 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 7 leaves more memory for this page.

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
    ## One run as OpenLineage events

    The next cell runs the week with the returns desk and with the `failed` change, in which `build_daily_sales` fails on its last night, as in Chapter 2.

    It makes every run's events in OpenLineage's form. It prints the two events of `build_clean_orders`'s run on Friday 11, which read the orders up to Thursday. It prints the first event in full. Of the second, it prints only the fields that differ from the first: its type, its time, its inputs and its outputs.
    """)
    return


@app.cell  # reader-id: cell-13
def _(shop):
    week8 = shop.run_week(["returns", "failed"])
    events = shop.openlineage.run_events(week8)
    friday = [
        e
        for e in events
        if e["job"]["name"] == "build_clean_orders"
        and e["eventTime"].startswith("2026-09-11")
    ]
    print(shop.openlineage.show(friday[0]))
    print(
        shop.openlineage.show(
            {
                k: friday[1][k]
                for k in ("eventType", "eventTime", "inputs", "outputs")
            }
        )
    )
    return (events, friday,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The events have these fields:

    - **`eventType`:** `START` for the first event and `COMPLETE` for the second. A run that fails sends `FAIL` in place of `COMPLETE`.
    - **`eventTime`:** when the event happened.
    - **`schemaURL`:** the address of the version of the specification's schema that the event follows.

    `run.runId` is the run's identifier. The specification requires a UUID, a standard form of identifier. The shop makes UUIDs of version 7, which begin with the run's start time. The specification's documentation recommends that version.

    A job is named by a **namespace** and a name inside it. Here the namespace is `shop` and the name is `build_clean_orders`.

    A dataset is named the same way. `orders.jsonl` is named `orders.jsonl` in the namespace `s3://shop-raw`, its bucket. The shop's producers name `clean_orders` as `shop.analytics.clean_orders` in the namespace `warehouse://shop-warehouse`. That name is the shop's choice: a database `shop`, a schema `analytics`, then the table.

    `producer` is the address of the code that made the event. Here it is `https://example.org/shop/jobs/tree/v1`, which makes the events of all four jobs. That code is the event's **producer**.

    Further metadata comes in a **facet**. A facet is a named object that holds its own fields. Each facet has `_producer`, the code that made it, and `_schemaURL`, the address of the facet's own schema.

    In these events, the facets hold:

    - **`jobType`:** says the job is a batch job, one that starts and finishes.
    - **`sourceCodeLocation`:** holds the code version, `47190f1`. The shop fills it with its own hash of the code, which is Chapter 7's `code_version`, not a commit.
    - **`nominalTime`:** holds the time the run was due to start.
    - **`inputStatistics`:** holds the rows read, 27.
    - **`outputStatistics`:** holds the rows written, 23.

    The next cell lists where each of Chapter 7's fields went.
    """)
    return


@app.cell  # reader-id: cell-15
def _(shop):
    shop.openlineage.mapping()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What a consumer knows

    A program that receives events is a consumer. The cell below sends the `START` alone to a consumer: the shop's own, a small one. It keeps one row for each run, and it adds to that row what each event says.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide what the consumer knows about the run after the `START` alone, and what it knows about `clean_orders`.
    """), kind="info")
    return


@app.cell  # reader-id: cell-18
def _(friday, shop):
    consumer = shop.openlineage.Consumer()
    consumer.send(friday[0])
    consumer.runs()
    return (consumer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    The consumer writes each name as its namespace, then `/`, then the name.

    Its row holds the state `START`, the start time, and the input `orders.jsonl`. It holds no output and no end time. The START named the input and no output.

    From this row alone, a run still working and a run that stopped without sending another event look the same.

    </details>

    The next cell sends the COMPLETE.
    """)
    return


@app.cell  # reader-id: cell-20
def _(consumer, friday):
    consumer.send(friday[1])
    consumer.runs()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The row now holds the state `COMPLETE`, the end time `2026-09-11T02:05:52Z`, the output `warehouse://shop-warehouse/shop.analytics.clean_orders`, and 2 events.

    The COMPLETE named the input again, with its row count, and added the output.

    The specification says that events about one run add to each other. Its words: "All metadata is additive". A facet sent again under the same name replaces the earlier one.

    The consumer lists the repeated input once, matching it by its namespace and name. The shop's consumer is written that way.

    The next cell sends every event of the week to a new consumer, prints how many runs it holds, and lists the runs whose state is `FAIL`.
    """)
    return


@app.cell  # reader-id: cell-22
def _(events, shop):
    everything = shop.openlineage.Consumer().send(*events)
    print(len(everything.runs()), "runs")
    everything.runs(state="FAIL")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The consumer holds 34 runs. One of them has the state `FAIL`: `build_daily_sales` on Monday 14. It has no output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## An event written by hand

    The analyst's copy sends no events. The analyst writes the two events of Friday 11's copy by hand.

    The next cell holds them as Python dictionaries, `start` and `complete`.

    The `runId` comes from `shop.openlineage.uuid7`, which makes a version 7 UUID from a start time.

    The cell checks `start` against the specification's rules:

    - the fields every run event must have: `eventTime`, `producer`, `schemaURL`, `run` with a `runId`, and `job` with a namespace and a name;
    - a `runId` that is a UUID;
    - an `eventType` from the specification's list, where the event has one;
    - a time in the specification's date-time form;
    - addresses that are URIs;
    - in each facet, a `_producer` and a `_schemaURL`.
    """)
    return


@app.cell  # reader-id: cell-25
def _(shop):
    start = {
        "eventType": "START",
        "eventTime": "2026-09-11T02:15:00Z",
        "run": {
            "runId": shop.openlineage.uuid7("2026-09-11T02:15:00Z", "copy")
        },
        "job": {"namespace": "analyst", "name": "copy_clean_orders"},
        "inputs": [
            {
                "namespace": "warehouse://shop-warehouse",
                "name": "analytics.clean_orders",
            }
        ],
        "outputs": [],
        "producer": "https://example.org/analyst/copy-script/v1",
        "schemaURL": shop.openlineage.SCHEMA_URL,
    }
    complete = {
        **start,
        "eventType": "COMPLETE",
        "eventTime": "2026-09-11T02:15:17Z",
        "outputs": [
            {
                "namespace": "s3://shop-scratch",
                "name": "clean_orders_copy.csv",
            }
        ],
    }
    shop.openlineage.check(start)
    return (complete, start,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The check finds no problems in `start`.

    The cell below sends the week's events and the analyst's two events to a new consumer, and follows edges upstream from the copy, `s3://shop-scratch/clean_orders_copy.csv`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide whether that traversal will reach `orders.jsonl`.
    """), kind="info")
    return


@app.cell  # reader-id: cell-28
def _(complete, events, shop, start):
    joined = shop.openlineage.Consumer().send(*events, start, complete)
    joined.lineage().upstream("s3://shop-scratch/clean_orders_copy.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    The traversal reaches 2 nodes, `analyst/copy_clean_orders` and `warehouse://shop-warehouse/analytics.clean_orders`, and stops. It does not reach `orders.jsonl`.

    Compare the analyst's input in the cell above with the name the jobs' events gave `clean_orders` earlier: `analytics.clean_orders` against `shop.analytics.clean_orders`. The analyst left out the database.

    The consumer joins two datasets only when their namespace and their name are the same. To the consumer, the two names are two datasets.

    </details>

    Change the analyst's input to the jobs' name, `"shop.analytics.clean_orders"`, select that cell and press **Run below**. The traversal then reaches 4 nodes, through `shop/build_clean_orders`, to `orders.jsonl`.

    <details><summary>The printed result, explained</summary>

    The specification's naming page gives a namespace and a name for each kind of data store it lists. It lists no form for the store the shop's warehouse runs on, so the shop's producers must agree on one.

    The page warns of the same failure for a store it lists: names made under Snowflake's older form of account name do not connect to names made under the newer form, so the lineage does not join.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## An event that breaks a rule

    The next cell copies `start`, sets its `runId` to `"copy-friday"`, deletes its `producer`, and checks it.
    """)
    return


@app.cell  # reader-id: cell-31
def _(shop, start):
    broken = {**start, "run": {"runId": "copy-friday"}}
    del broken["producer"]
    shop.openlineage.check(broken)
    return (broken,)



@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The check lists 2 problems: `producer` is missing, and `run.runId` is not a UUID.

    The next cell sends this invalid event to a new consumer.
    """)
    return


@app.cell  # reader-id: cell-32
def _(broken, shop):
    refusing = shop.openlineage.Consumer().send(broken)
    print(
        len(refusing.refused),
        "event set aside;",
        len(refusing.runs()),
        "runs",
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell above sent the event to a new consumer. The consumer set it aside and holds no run from it.

    Setting such an event aside is how the shop's consumer is written. The specification says what an event must hold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Our programs must emit OpenLineage."

    The head of the shop set this requirement at the start of the chapter.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the block below, which holds four readings of the requirement "Our programs must emit OpenLineage", decide what you would check to say the shop meets the requirement.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Four readings of the requirement</summary>

    The requirement could mean four things:

    - which programs: a list of every program that touches the shop's data, and whether each sends events;
    - which events: for each run, one START and one COMPLETE, ABORT or FAIL, as the specification requires (ABORT is for a run stopped abnormally, FAIL for one that failed); RUNNING and OTHER are optional;
    - which facets: a list of the facets each event must carry; the specification requires none;
    - which names: one namespace and name for each dataset, which every producer uses.

    Each reading needs something different.

    </details>

    The next cell counts, job by job, the runs, the events of each type, and the events that break the specification's rules.
    """)
    return


@app.cell  # reader-id: cell-37
def _(events, shop):
    shop.openlineage.summary(events)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    In all, 6 programs sent events: the four jobs and the two functions. Every run sent a START and a COMPLETE, except the run of `build_daily_sales` on Monday 14, which sent a FAIL. No event breaks the specification's rules.

    Taken one reading at a time:

    - which programs: not met for every program; the export and the analyst's copy send nothing;
    - which events: met, for the jobs and the functions;
    - which facets: the shop sends some of the standard facets and one of its own, `shop_objectChange`, for a function's file change, named with the shop's prefix as the specification asks of a facet that is not standard. Whether these are the facets meant, the requirement does not say;
    - which names: met within the shop's own producers; the analyst's hand-written events used another name until you changed it.

    As written, "Our programs" covers every program, so the shop does not meet the requirement until the export and the analyst's copy send events too.

    One of the standard facets, `ownership`, holds a dataset's owners. Each owner is an identifier, which can name a user, a team or an application. As Chapter 2 showed, an owner's identifier alone does not establish whom to contact about a wrong number. The shop does not send it.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 9

    The shop's runs, in OpenLineage's form, showed the following. After a START, the consumer held the run's input and no output. The output came with the COMPLETE. A failed run sent a FAIL. An event written by hand passed the check, but two names for one table did not join until you changed one. An event that broke two rules was set aside.

    The experiments could not show how a consumer keeps a week of events and turns them into a graph that answers questions. They could not show what a consumer does with an event that arrives damaged.

    Chapter 9 builds that consumer, one stage at a time, from the events as received to a graph.

    - Which programs on a platform you work on would need to send events for its lineage to be whole?
    - How should your platform name its warehouse's tables, and who must agree on the names?
    - What should a consumer do with a `START` whose run never sends another event?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its programs, its producers and their addresses are invented for the course. The addresses at `example.org` lead nowhere.

    Here the shop's own code makes each event and hands it straight to the consumer. A real producer is usually a library inside the program that runs the job. The specification also defines an HTTP interface for sending events to a consumer.

    The consumer is the shop's own, not a product. It takes a run's state from the last event it received. The OpenLineage documentation calls Marquez the reference implementation of its API. Chapter 29 compares real consumers.

    The specification does not say what a consumer does with a missing, repeated or late event. Chapters 18 to 20 take that up.

    The specification's schema and its page on the run cycle disagree on one point. The schema allows OTHER events, which carry extra metadata, after a run's COMPLETE, ABORT or FAIL. The run cycle page says no event follows those.

    The namespaces `warehouse://shop-warehouse` and `reporting://shop-reporting` are the shop's choice.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 7](chapter_07.ipynb) · [Next: Chapter 9](chapter_09.ipynb)

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
