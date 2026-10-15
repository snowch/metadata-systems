# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Airflow, Spark, dbt and Trino",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 29](chapter_29.ipynb) · [Next: Chapter 31](chapter_31.ipynb)

    # Chapter 30: Airflow, Spark, dbt and Trino

    **Objectives**

    - Read what the OpenLineage integrations of four systems, Airflow, Spark, dbt and Trino, make an OpenLineage job and an OpenLineage run.
    - Find what each integration would send for the shop's `build_daily_sales`.
    - Change the name Trino's events give a job, and find which programs one name format merges.
    - Question the requirement "Capture lineage from Airflow, Spark, dbt and Trino."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 29's link, in a browser that had opened and run Chapter 29 (measured on a computer). Chapter 29's link opens this page in a new tab. Chapter 29 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 29 leaves more memory for this page.

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
    ## Four systems, four records

    Suppose the shop's nightly work ran in each of four systems: as Airflow tasks, as Spark jobs, as dbt models and as Trino queries.

    Each system keeps its own record of its work. Each has an OpenLineage integration, a part that sends OpenLineage events from that record.

    As in Chapter 29, nothing runs here. Each cell applies the rules each project's code states, in the version read, to the shop's week: Airflow 3.3.0 with its OpenLineage provider 2.20.3, Spark 4.0.0 with OpenLineage's Spark integration, dbt's files as dbt 1.11 writes them with OpenLineage's dbt integration, and Trino's OpenLineage listener.

    The next cell sets out, for each system, what its integration makes an OpenLineage job and an OpenLineage run, where it takes a job's inputs from, and when it sends the events.
    """)
    return


@app.cell
def _(shop):
    shop.integrations.rules()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The four OpenLineage jobs are four different things: a task in a Dag, a Spark action, a dbt model, and, by default, a single Trino query.

    Airflow's provider takes a task's inputs and outputs from the extractor for the task's operator, from hooks' lineage, or from the task's declared inlets and outlets. Here the shop's tasks are supposed to report theirs.

    In Airflow, a task instance is one task in one Dag run. The scheduler raises its `try_number` by one for each try. The shop's Dag tries a failed task once more.

    Airflow's OpenLineage provider, from Chapter 29, makes each try's run id from the namespace, the Dag, the task, the try number and the map index, with the logical date.

    Early on Monday 14, `build_daily_sales` fails, as in Chapter 13.

    The next cell lists the 7 task instances of `build_daily_sales`, one for each night, with the OpenLineage runs each makes. Compare the number of task instances with the number of runs.
    """)
    return


@app.cell
def _(shop):
    week30 = shop.run_week(["returns", "source", "failed"])
    shop.integrations.airflow(week30)
    return (week30,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Monday 14's task instance failed on both tries: one row, `try_number` 2, state `failed`.

    Its two tries are 2 OpenLineage runs. So the week's 7 nights give the job 8 runs in the lineage, 2 of them on Monday 14.

    In Spark, a job is one action. Spark's OpenLineage integration names its OpenLineage job from the application's name, the top node of the plan Spark ran, and the output.

    For an insert into a table kept as files, the top node is `Execute InsertIntoHadoopFsRelationCommand`, and the output's part of the name is the last two parts of the path the files are written to, joined with `_`.

    Suppose the application is named `shop_nightly`, and the files of `daily_sales` are kept under `s3://shop-warehouse/analytics/daily_sales`. Where the files are kept is the shop's assumption.

    The next cell prints the OpenLineage job name of an insert into `daily_sales`. Find the part of it that names what the job wrote.
    """)
    return


@app.cell
def _(shop):
    print(shop.integrations.spark())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The name is `shop_nightly.execute_insert_into_hadoop_fs_relation_command.analytics_daily_sales`.

    The plan's node is written in lower case with `_` between its words.

    `analytics_daily_sales` comes from the path, not from the table's name. A program that wrote files under another path would be another job.

    In dbt, the integration's wrapper runs dbt first. Then it reads the files dbt wrote, `manifest.json` and `run_results.json`, and sends every event at the end.

    A model's OpenLineage job name is its database, schema, project and model, joined with `.`. Each reading of the files makes new run ids.

    Suppose the shop's three warehouse jobs ran as one dbt invocation in the project `shop_models`.

    The next cell lists one night's three models, early on Sunday 13: each model's job, its `START` time, its end time, and when its events are sent. Compare when each model's work happened with when its events are sent.
    """)
    return


@app.cell
def _(shop, week30):
    shop.integrations.dbt(week30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The events of all three models are sent at 02:30:21, at the earliest, when the last model ends. The table gives that earliest time.

    The `START` of `clean_customers`, at 02:00:00, is sent at least 30 minutes after it happened. The delay is the length of the dbt invocation, here the span of the shop's nightly schedule.

    These are late events of the kind Chapter 20 handled, and they are late by design.

    If the files are read twice, one model run gets two run ids, and Chapter 25's key of run id and event type keeps both.

    ## Trino's job names

    Trino's listener sends `START` when a query is created, and `COMPLETE` or `FAIL` when it ends. The inputs and the output come with the second only. By default, a `SELECT` sends nothing.

    A job's name follows the setting `openlineage-event-listener.job.name-format`. Its default is `$QUERY_ID`, the query's id, so each query is its own job. The other values it can use are `$SOURCE`, the name the client gives, `$USER` and `$CLIENT_IP`. The format can combine these values with fixed text; the cell here takes one value.

    Suppose each of the shop's four nightly programs ran as one query a night, all from clients with the same source, `shop-nightly`, the same user, `svc_nightly_etl`, and the same address, `10.0.0.5`.

    The shop's lineage wants one job for the 7 runs of `build_daily_sales`, holding no other program's runs.

    Before you read on, write in the next cell how many jobs the 7 queries of `build_daily_sales` would make with the name format `$SOURCE`, and whose runs those jobs would hold.
    """)
    return


@app.cell
def _():
    expected_jobs = """
With the name format $SOURCE, how many jobs will the 7 queries of build_daily_sales make, and whose runs will those jobs hold?
........
"""
    return


@app.cell
def _():
    name_format = "$QUERY_ID"
    source_of = {
        "build_clean_customers": "shop-nightly",
        "build_clean_orders": "shop-nightly",
        "build_daily_sales": "shop-nightly",
        "refresh_dashboard": "shop-nightly",
    }
    return name_format, source_of


@app.cell
def _(name_format, shop, source_of, week30):
    shop.integrations.check_trino(week30, name_format, source_of)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell above the check holds `name_format`, `"$QUERY_ID"`, and `source_of`, the source each program's client gives.

    As it stands, the check finds 7 jobs: each query is its own job, named by its id.

    Change `name_format` to `"$SOURCE"`. Select the cell and press **Run below**.

    The check then finds 1 job for the 7 runs, and that job also holds the runs of the other three programs.

    Compare this with what you wrote.

    Then give each program its own source in `source_of`, and press **Run below** again. Both tests pass: one job, holding the runs of `build_daily_sales` only.

    The next cell counts the jobs each name format makes from the week's 28 nightly queries, with the sources in your cell.
    """)
    return


@app.cell
def _(shop, source_of, week30):
    shop.integrations.jobs_by_format(week30, source_of)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With a source for each program, the 28 nightly queries make 28 jobs under `$QUERY_ID`, one for each query. `$SOURCE` makes 4, one for each program.

    `$USER` and `$CLIENT_IP` each make 1 job. All four programs share the user `svc_nightly_etl` and the address `10.0.0.5`, so neither value can tell the programs apart.

    Suppose the analyst's copy from Sunday 13 were made in Trino: a `SELECT` on `clean_orders` whose result a client saves as a file.

    By default the `SELECT` sends no events, so the read of `clean_orders` would be missing.

    The file is not a Trino table, so the write of `clean_orders_copy.csv` would be missing even if the `SELECT` sent its events.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Capturing lineage from four systems
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Capture lineage from Airflow, Spark, dbt and Trino."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "capture lineage from Airflow, Spark, dbt and Trino" means to you here.
    """)
    return


@app.cell
def _():
    what_capture_means = """
What does "capture lineage from Airflow, Spark, dbt and Trino" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "Capture lineage from Airflow, Spark, dbt and Trino" could mean three things. Each item says what it needs:

    - by each system's own OpenLineage jobs (a task, a Spark action and its output, a model, a query): it needs nothing more, and gives four kinds of job, each named its own way. It also gets jobs the cells here leave out: the Dag's own job, and the job dbt's integration sends for the whole invocation;
    - by the shop's programs, as Part II meant a job: it needs a rule that maps each system's job names to the program, as Chapter 22's aliases mapped two names of one dataset to one, because none of the four systems' default names is the program's name;
    - by the datasets each system reads and writes, whatever the jobs are called: it needs each system to name the same dataset the same way (Chapter 12), and it misses what a system does not send, such as Trino's `SELECT`.

    The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 31

    Airflow made a retried task two OpenLineage runs. Spark's job name held the plan's top node and the last two parts of the output's path. dbt's integration sent each night's events after dbt finished, `START`s included. Trino named a job by its query's id by default, and one shared source merged four programs into one job.

    Chapter 31 compares four metadata platforms that receive this kind of metadata.

    Three questions:

    - What does each system on your platform call a job?
    - Which of your systems send their events late by design?
    - Which of your queries send no events at all?

    ### How this differs from a real platform

    - Each result applies the rules as each project's code states them in the version read. The integrations also send facets the cells leave out, and jobs: the Dag's own job, and dbt's job for the whole invocation.
    - The Dag's second try, the tasks reporting their inputs and outputs, where the files of `daily_sales` are kept, the dbt project, the Trino clients' sources, user and address, and the query ids are the shop's assumptions.
    - The Spark job name assumes an insert into a table kept as files. Another kind of write has another top node.
    - Trino's name format can combine its values with fixed text. The cell takes one value.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 29](chapter_29.ipynb) · [Next: Chapter 31](chapter_31.ipynb)

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
