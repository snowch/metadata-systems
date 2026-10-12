# The engine

The shop's data platform, which computes every figure, and the metadata system the learner builds
on top of it. What a figure shows, the engine computed. The page never names the engine: a figure
is a diagram or a figure of the shop's data, with a caption (`CLAUDE.md`, "No lab on the page").
This file is the engine's design; the code is `notebook/shop`, in Python with the standard library
only, so it runs unchanged in a notebook in the browser (Pyodide) and in CI. Where the two differ,
the code and its tests (`notebook/tests`) are right and this file is out of date.

Until 11 October 2026 a TypeScript engine (`packages/lab`) computed the figures of the chapters'
pages, with its own SQL subset and Parquet files modelled as records. The pages went when the
notebooks became the only version of each chapter (`docs/plan.md`, "11 October 2026: only the
notebooks"), and the TypeScript engine with them.

## Two halves

- **The shop**: a small online shop's data platform, which really runs. It has files and tables
  with real rows, jobs written in SQL that really transform them, a
  scheduler, a clock and the storage systems that hold the results.
- **The learner's metadata system**: the records, events, store, graph and queries the learner
  builds, chapter by chapter, about the shop. In Chapter 2 it is empty: the learner has the shop's
  storage and nothing else.

## The shop

An online shop that sells bicycle parts. It is invented for the course; so are its products,
customers and staff.

### Where its data lives

| System | What it holds | What it records about each thing it holds |
| --- | --- | --- |
| Object storage, bucket `shop-raw` | `orders.jsonl`, `customers.jsonl` (JSON Lines) and `products.csv`, written each night by an export from the shop's checkout and catalogue | each file's key, size and last-modified time; the files are real text, so a reader parses them to see their fields |
| The warehouse, database `shop`, schema `analytics` (SQLite, with a catalogue the learner queries as `information_schema.tables` and `.columns`) | `clean_customers`, `clean_orders`, `daily_sales` | each table's columns and declared types, row count, an estimated size, created and last-altered times, and the account that owns it |
| The reporting tool | `sales_dashboard`, a chart of revenue per day | the dashboard's title, who created it, when it last refreshed and the values it shows |

These records are the engine's choice of what a typical system of each kind keeps; the engine does not
model why a system keeps a field. The reporting tool keeps no query: a job fills the
dashboard, as jobs fill the tables. A job that writes no rows still moves its table's
last-written time, so in the engine only a failed write leaves the time stale. Real systems differ:
some table formats keep history the shop's warehouse does not, such as Apache Iceberg's snapshots
and Delta Lake's record of each write (`docs/sources.md`). Each chapter's model-versus-reality
note says which difference matters to it.

### The jobs

Four jobs run each night, in this order, all logged in as the warehouse account `etl_service`.
Their SQL (SQLite's) is in `notebook/shop/week.py`; the platform does not record it.

| Job | Reads | Writes | How |
| --- | --- | --- | --- |
| clean customers | `customers.jsonl` | `clean_customers` | replaces the table: lower-cases every email and drops customers with no email |
| clean orders | `orders.jsonl` | `clean_orders` | replaces the table: keeps one copy of each order, drops orders with no customer id, drops orders whose quantity is 0 or less |
| daily sales | `clean_orders` | `daily_sales` | appends one row for the day before: that day's revenue, the sum of price times quantity over its completed orders |
| dashboard refresh | `daily_sales` | `sales_dashboard` | reads every row and redraws the chart |

`daily_sales` is appended to, not rebuilt: each night adds one row and never revisits the rows
before it. That is common in real platforms, and it is why a change to the job shows only in
the rows written after the change.

### The week

The course's week is Monday 7 to Sunday 13 September 2026. Each night the export writes the
orders placed so far, then the four jobs run. The learner arrives on Monday 14 September,
after the last night's run, and finds the shop as that run left it.

The week's orders are hand-written in `notebook/shop/data.py`, so each property below is
deliberate:

- some days are plain, and on them the raw orders add up to the day's revenue;
- one day has a cancelled order, which the raw file keeps and revenue leaves out;
- one day has an order that the export wrote twice;
- on Thursday the checkout sent some orders with no customer id, and the rule in clean orders
  that drops such orders made Thursday's revenue low. This is the shop's incident: Chapter 2 shows
  its symptom and later chapters measure it, trace it and find its cause;
- no order has a quantity of 0 or less, so nothing in the week's data shows that clean orders
  has a rule for them.

Every number a chapter states about the week is computed by the engine and pinned by
`notebook/tests/test_words.py`; this file states none.

### Changes

A notebook can run the week again with a change to the shop (`run_week(["copy"])`) and compare
what the learner can see before and after. Each change is applied before the week runs, so the
changed week is as deterministic as the plain one. Chapter 2 uses three:

- **An analyst's copy.** A script copies `clean_orders` to `shop-scratch/clean_orders_copy.csv`
  every night, before daily sales runs.
- **A job edited for refunds.** From Saturday's row on, daily sales keeps every order whose
  status is not "refunded", where it kept completed orders. The shop has no refunds yet, so the
  edit changes nothing except on a day with a cancelled order.
- **A failed night.** On the last night, daily sales fails and writes nothing.

Chapter 3 adds a fourth:

- **A new column.** From Saturday's row on, daily sales also writes each day's number of completed
  orders into a new column, `order_count`; the rows before have none. The warehouse's catalogue
  records the column at once, so a check of a person's records against it sees the change.

Later chapters add their own: a renamed column, a late file, a duplicated event, a second
environment.

### Planned: the returns desk

Not built yet; built with Chapter 7, the first chapter that uses it (`docs/plan.md`, "12 October
2026: processing started by objects"). A change, `returns`, adds to the week:

- **A bucket and a table.** `s3://shop-returns/`, holding one small JSON object per return (the
  order, the item, the quantity returned, when), and a warehouse table, `returns`, one row per
  return.
- **Writes at any hour.** The returns desk creates, overwrites and deletes objects during the day,
  at fixed times written in `notebook/shop/data.py` as the orders are, so the week stays
  deterministic. Object storage keeps each object's versions, with the time of each.
- **Notifications and functions.** Each create, overwrite or delete produces a notification, which
  the platform keeps and does not show, and which starts a function: `record_return` for a create
  or an overwrite (it replaces the return's row), `remove_return` for a delete. Each start is a run
  the platform does not record (`Week.executions`, like the jobs').
- **A delivery the chapters can break.** By default each notification is delivered once, in order.
  A chapter can make the delivery lose, repeat or reorder notifications, so that a function runs
  twice for one return, or a delete arrives before its create; the deterministic choice of which
  is the chapter's, written in the change.
- **Data that tests it.** At least one return corrected after its function ran, one return
  withdrawn, and one return of a Thursday order with no customer id, which `clean_orders` left out,
  so that provenance, deletion and a return of an order the warehouse does not hold each have a
  case.

### The repository (Chapter 6)

`repository(week)` gives the jobs' code as the shop's repository holds it on Monday morning: one
file per job, written in the course's own small notation (`read("...")`, `write("...", sql)`,
`refresh("...", sql)`) around the same SQL constants the week runs, so the code shown is the code
that ran. The export and the analyst's copy are not in it. `reads_and_writes` reads a job's code
with a small rule, and `compare_with_code` sets a reader's lineage lines against it. The `source`
change (with `copy`) makes `build_daily_sales` read the analyst's copy from Saturday's row on; the
rows it writes are the same, and only the code differs.

## What a notebook can ask of the engine

`notebook/shop` answers three kinds of question, and the notebooks show each answer with its
evidence:

- **What storage records.** `storage.ls()`, `warehouse.sql(...)` over `information_schema`, and
  `reporting.dashboard()`: for each asset, exactly the fields the table above lists, as of Monday
  morning.
- **What the data suggests.** Inference from contents alone (`notebook/shop/infer.py`):
  `queries_that_rebuild` searches every sum over one asset (which rows to keep, what to add up,
  per what) and reports each one that reproduces a table, so a notebook can show that two sources
  fit equally well; `cleaning_rules_that_fit` searches every setting of the cleaning rules that
  turns the raw orders into `clean_orders`; `day_gap` sets one day's raw orders against the rows
  `clean_orders` keeps.
- **What only a record answers.** The questions whose answers are in neither: who is responsible
  for an asset, what a number's unit is, what changed and why.
- **What a person's records say, and whether they hold** (`notebook/shop/records.py`). Chapter 3's
  records (`records`) are lines of text, `asset [column] field: value`, queryable with SQL as a
  table `records`; their check holds them to what the warehouse and object storage record (every
  column described, every line about an asset and a column that exist) and cannot test what a
  description says. Chapter 4's (`typed_records`) start each line with a type and an identifier,
  and a `model` (each type's attributes, and whether a value is text or names an entity of
  another type) checks them: unknown types and attributes, and values that name nothing the
  records describe. `owners` lists every asset with its `responsible` values under three readings
  of "one owner". Both notations are the course's own.
- **The records as a graph** (`notebook/shop/graph.py`, Chapters 5 and 6). `graph(records, model)`
  makes each entity a node and each line whose value names another entity an edge; `traverse`
  walks the edges it is given, each way it is given; `downstream` and `upstream` walk `reads` and
  `writes`; `drawing` draws the graph as an image a phone can read, each connected part on its own.

Two more things the notebooks draw from it (`notebook/shop/figures.py`), when the site is built,
into Markdown cells (`docs/authoring.md`, "How a figure is drawn"):

- **The platform** (`pipeline`): the three systems in the order data moves through them, the
  assets each holds, and one label for the flow between them. It draws no arrow from one asset to
  another: which asset is made from which is what Chapter 2 shows storage cannot tell.
- **The week, as it ran** (`week_strip`, from `timeline`): the days the shop took orders, the night
  of work after each with when its first write began and its last ended, and the morning the
  learner starts (`ARRIVAL`). It says when the nights were and nothing about what a night wrote.

## SQL

The jobs and the queries a learner runs are SQLite's SQL, run by Python's `sqlite3`.
`warehouse.sql(query, files={...})` reads files from object storage as tables for one query, as
a query engine that reads files would, and `storage.sql(uri, query)` runs a query over one file.
Money is held as whole pence, so sums are exact; `pounds` formats an amount where a person reads
it.

## The learner's state

A notebook runs the shop's week from its definition each time its cells run, so what a figure shows
is a function of the shop's definition and the cells the learner has run or changed. JupyterLite
keeps the learner's edited copy of a notebook in the browser's storage, on that device; nothing is
sent anywhere. When a later chapter needs what the learner built earlier (their records, their
event design), it will say how it gets it; no chapter does yet.

## Determinism

The same code gives the same rows, times and identifiers on every machine. The engine has no wall
clock (its clock is the week's: every writer's start and duration is fixed in `week.py`), no
randomness, and no formatting that depends on a locale or time zone. Every time is UTC.

## What the engine does not model

- Columnar formats: the raw files are JSON Lines and CSV, which carry no types; a Parquet file's
  footer, which would, is not modelled.
- A table's size: the warehouse's figure is a deterministic estimate from the rows.
- Concurrency inside a night: the jobs run one after another.
- Time zones: every time is UTC, and an order's day is its UTC date.
- Permissions, until a chapter needs them.
