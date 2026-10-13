[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 29](chapter_29.ipynb) · [Next: Chapter 31](chapter_31.ipynb)

# Chapter 30: Airflow, Spark, dbt and Trino

**Objectives**

- Read what four systems call a job and a run: Airflow, Spark, dbt and Trino.
- Find what each system's OpenLineage integration would send for the shop's `build_daily_sales`.
- Change the name Trino's events give a job, and find what one name format merges.
- Question the requirement "Capture lineage from Airflow, Spark, dbt and Trino."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## Four systems, four records

Suppose the shop's nightly work ran in four systems in turn: as Airflow tasks, as Spark jobs, as dbt models and as Trino queries.

Each system keeps its own record of its work. Each has an OpenLineage integration, a part that sends OpenLineage events from that record.

As in Chapter 29, nothing runs here: each cell applies the rules the system's code states, in the version read, to the shop's week.

The next cell sets out, for each system, what it calls a job and a run, where the inputs come from, and when its events are sent.

    >>> shop.integrations.rules()
      | system | its job | a run | inputs from | sent
      | Airflow | a task in a Dag | a try of a task instance | what each task's operator reports | as each try starts and ends
      | Spark | an action, named with its plan's top node and output table | one execution | the query plan | as the execution starts and ends
      | dbt | a model | one reading of the files dbt wrote | the manifest's parents of the model | after dbt has finished
      | Trino | a query, by default | one query | the tables the query names | as the query is created and ends

The four systems' jobs are four different things: a task in a Dag, a Spark action named with its plan's top node and its output table, a dbt model, and, by default, a single Trino query.

The week has the returns desk, the analyst's copy from Sunday 13, and Monday 14's failed night.

In Airflow, a task instance is one task in one Dag run. The scheduler raises its `try_number` by one for each try. The shop's Dag tries a failed task once more.

Airflow's OpenLineage provider, from Chapter 29, makes each try's run id from its try number, among other values.

The next cell lists the 7 task instances of `build_daily_sales`, one for each night.

    >>> week30 = shop.run_week(["returns", "source", "failed"])
    >>> shop.integrations.airflow(week30)
      | Dag run | task instance | try_number | state | OpenLineage job | OpenLineage runs
      | 2026-09-08 | shop_nightly.build_daily_sales | 1 | success | default/shop_nightly.build_daily_sales | 1
      | 2026-09-09 | shop_nightly.build_daily_sales | 1 | success | default/shop_nightly.build_daily_sales | 1
      | 2026-09-10 | shop_nightly.build_daily_sales | 1 | success | default/shop_nightly.build_daily_sales | 1
      | 2026-09-11 | shop_nightly.build_daily_sales | 1 | success | default/shop_nightly.build_daily_sales | 1
      | 2026-09-12 | shop_nightly.build_daily_sales | 1 | success | default/shop_nightly.build_daily_sales | 1
      | 2026-09-13 | shop_nightly.build_daily_sales | 1 | success | default/shop_nightly.build_daily_sales | 1
      | 2026-09-14 | shop_nightly.build_daily_sales | 2 | failed | default/shop_nightly.build_daily_sales | 2

Monday 14's task instance failed on both tries: one row, `try_number` 2, state `failed`.

Its two tries are 2 OpenLineage runs. So the week's 7 nights give the job 8 runs in the lineage, 2 of them on Monday 14.

In Spark, a job is one action. Spark's OpenLineage integration names the job from the application's name, the top node of the plan Spark ran, and the output table.

For an insert into a table kept as files, the top node is `Execute InsertIntoHadoopFsRelationCommand`.

The next cell prints the job name for an insert into `shop.analytics.daily_sales` by an application named `shop_nightly`.

    >>> print(shop.integrations.spark())
      shop_nightly.execute_insert_into_hadoop_fs_relation_command.shop_analytics_daily_sales

The name is `shop_nightly.execute_insert_into_hadoop_fs_relation_command.shop_analytics_daily_sales`.

The plan's node is written in lower case with `_` between its words, and the table's dots become `_`. A program that wrote another table would be another job.

In dbt, the integration's wrapper runs dbt first. Then it reads the files dbt wrote, `manifest.json` and `run_results.json`, and sends every event at the end.

A model's job name is its database, schema, project and model, joined with `.`. Each reading of the files makes new run ids.

Suppose the shop's three warehouse jobs ran as one dbt run in the project `shop_models`.

The next cell lists one night's three models, early on Sunday 13: each model's job, its `START` time, its end time, and when its events are sent.

    >>> shop.integrations.dbt(week30)
      | model | OpenLineage job | START time | end time | events sent at
      | model.shop_models.clean_customers | dbt/shop.analytics.shop_models.clean_customers | 02:00:00 | 02:00:38 | 02:30:21
      | model.shop_models.clean_orders | dbt/shop.analytics.shop_models.clean_orders | 02:05:00 | 02:05:52 | 02:30:21
      | model.shop_models.daily_sales | dbt/shop.analytics.shop_models.daily_sales | 02:30:00 | 02:30:21 | 02:30:21

The events of all three models are sent at 02:30:21, when the dbt run ends, or later.

The `START` of `clean_customers`, at 02:00:00, is sent at least 30 minutes after it happened. These are late events of the kind Chapter 20 handled, and they are late by design.

If the files are read twice, one model run gets two run ids, and Chapter 25's key of run id and event type keeps both.

## Trino's job names

Trino's listener sends `START` when a query is created, and `COMPLETE` or `FAIL` when it ends. The inputs and the output come with the second only.

A job's name follows the setting `openlineage-event-listener.job.name-format`. Its default is `$QUERY_ID`. The other values it can use are `$SOURCE`, the name the client gives, `$USER` and `$CLIENT_IP`.

By default, a `SELECT` sends nothing.

Suppose each of the shop's four nightly jobs ran as one query a night, from one client whose source is `shop-nightly`.

Before you read on, write in the next cell how many jobs the 7 nightly queries of `build_daily_sales` make in Trino's events, with the default name format.

    [WRITE] How many jobs will the 7 nightly queries of build_daily_sales make in Trino's events?
    [WRITE] ........

    >>> name_format = "$QUERY_ID"
    >>> source_of = {
    >>>     "build_clean_customers": "shop-nightly",
    >>>     "build_clean_orders": "shop-nightly",
    >>>     "build_daily_sales": "shop-nightly",
    >>>     "refresh_dashboard": "shop-nightly",
    >>> }

    >>> shop.integrations.check_trino(week30, name_format, source_of)
      | test | passes
      | The 7 runs of `build_daily_sales` are 7 jobs in Trino's events. | no

    >>> shop.integrations.jobs_by_format(week30, source_of)
      | name format | jobs
      | $QUERY_ID | 28
      | $SOURCE | 1
      | $USER | 1
      | $CLIENT_IP | 1

The check finds 7 jobs: each query is its own job, named by its id.

Over the four programs, the 28 nightly queries make 28 jobs, as the table below the check lists.

Compare this with what you wrote.

The cell above the check holds `name_format` and `source_of`, the source each program's client gives.

Change `name_format` to `"$SOURCE"`. Select the cell and press **Run below**. The 7 runs make 1 job, but the check shows that job also holds the runs of the other three programs: too many runs merged, as in Chapter 22.

Then give each program its own source in `source_of`, and press **Run below** again. Both tests pass: one job, holding the runs of `build_daily_sales` only.

The listener can name a job only from those four values, so a job's name depends on how each client is set up.

The analyst's copy is a `SELECT` whose result a client saves as a file. By default it sends nothing, so the edge to `clean_orders_copy.csv` would be missing.

## Capturing lineage from four systems

[BOX] The head of the shop's requirement: "Capture lineage from Airflow, Spark, dbt and Trino."

Before you read on, write in the next cell what "capture lineage from Airflow, Spark, dbt and Trino" means to you here.

    [WRITE] What does "capture lineage from Airflow, Spark, dbt and Trino" mean here?
    [WRITE] ........

It could mean three things. Each item says what it needs:

- by each system's own job (a task, an action and its table, a model, a query): it needs nothing more, and gives four kinds of job, each with its own name.
- by the shop's programs, as Part II meant a job: it needs a rule that maps each system's names to the program, as Chapter 22's aliases did, because none of the four systems' default names is the program's name.
- by the datasets each system reads and writes, whatever the jobs are called: it needs each system to name the same dataset the same way (Chapter 12), and it misses what a system does not send, such as Trino's `SELECT`.

The requirement does not say which it means.

## Before Chapter 31

Airflow made a retried task two OpenLineage runs. Spark's job name held the plan's top node and the output table. dbt sent each night's events after the run, `START`s included. Trino named a job by its query by default, and one shared source merged four programs.

The page could not show the four systems themselves: each result is a system's rules, as its code states them, applied here.

Chapter 31 compares four metadata platforms that receive this kind of metadata.

- What does each system on your platform call a job?
- Which of your systems send their events late by design?
- Which of your queries send no events at all?

### How this differs from a real platform

- Each result applies the rules as each project's code states them in the version read. The systems also send facets the cells leave out.
- The Dag's second try, the dbt project, the Trino client's sources and the query ids are the shop's assumptions.
- The Spark job name assumes an insert into a table kept as files. Another kind of write has another top node.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 29](chapter_29.ipynb) · [Next: Chapter 31](chapter_31.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

