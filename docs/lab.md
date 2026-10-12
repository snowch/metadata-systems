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

Chapter 6 adds `source`, and Chapter 7 `returns` (below). Part III adds seven:

- **`net`** (Chapter 10). From Saturday's row on, daily sales takes away what was returned, through a
  function the shop's developer added to the warehouse, `returned_quantity(order_id, product_id)`,
  which reads the table `returns`; the query names the table nowhere. It brings `returns` with it.
  No order of Saturday or Sunday was returned, so the rows are the same.
- **`added`, `renamed` and `retyped`** (Chapter 11). From the export before Saturday's row, the
  checkout's supplier changes `orders.jsonl`: a new field `coupon_code`; `quantity` renamed `qty`;
  or every customer id written as text (`C101`). Clean orders reads the fields it names: after the
  rename `quantity` is empty, its filter keeps no order, and the program still succeeds with no
  rows. After the retype the warehouse keeps `C101` as text in a column declared INTEGER: it turns text that looks like a number into a number, and `C101` is not one.
- **`dev`** (Chapter 12). A development database, `shop_dev`, beside production's, where a developer
  runs the daily sales program on Monday at 10:20 over Sunday's orders; the developer's runner sends
  events that name tables without their database. It also writes the supplier's test export,
  `Orders.jsonl`, into `shop-raw` on Friday.
- **`view`** (Chapter 12). Jo Marsh's view `sales_by_day` over `daily_sales`.
- **`clock`** (Chapter 13). The reporting tool's clock runs 40 minutes slow.

The failed night (`failed`) also records the error the warehouse gave, `database is locked`. The
analyst's copy (`copy`) runs `SELECT * FROM clean_orders` and writes the result's columns.

Part IV adds three:

- **`corrected`** (Chapter 15). On Sunday at 18:10 the returns desk records two rolls of bar tape back
  from order 7044 (`r-205`), and on Monday at 08:40, after the night's work, corrects it to one. With
  `net`, which it brings, Sunday's row of `daily_sales` subtracted two.
- **`withdrawn`** (Chapter 16). On Sunday at 21:15 the desk records the brake pads of order 7047 back
  (`r-206`), and on Monday at 08:50 withdraws the return, deleting its object. Sunday's row counted it.
- **`customer`** (Chapter 16). From Sunday's night on, `build_clean_orders` names the customer's
  column `customer`: the warehouse renames the column, and the program's code says so.

The returns desk's changes of a day reach `returns` before that night's work, and Monday morning's
after the last night's and before you start. Chapters 7 to 13 state nothing this order changes.

Part V adds one:

- **`twice`** (Chapter 19). Object storage delivers its notice of the desk's correction of `r-202`
  (Thursday 09:30) twice, so `record_return` starts twice for it, 25 seconds apart. Each run deletes
  the return's row and writes it again, so `returns` ends the same; the events hold two runs.

### The returns desk (Chapter 7 on)

Built with Chapter 7 (`docs/plan.md`, "12 October 2026: processing started by objects"). The change
`returns` adds to the week:

- **A bucket and a table.** `s3://shop-returns/`, one small JSON object per return (the return, the
  order, the product, the quantity returned, when it was first returned), and a warehouse table,
  `returns`, one row per return.
- **Writes at any hour.** The returns desk creates, overwrites and deletes objects during the day,
  at the fixed times in `RETURNS_DESK` (`notebook/shop/data.py`), so the week stays deterministic.
  Object storage keeps every version of every object, with a delete marker where one was deleted
  (`storage.versions`); a version's identifier is a hash of the object's key, time and text.
- **Functions.** Each change starts a function 2 seconds later: `record_return` for a create or an
  overwrite (it replaces the return's row), `remove_return` for a delete (it reads nothing; the
  object is gone). Each start is an execution like the jobs', with the object, its version and the
  change. The repository holds both functions' code with the change.
- **Delivery.** Each change starts its function exactly once, in order. Chapters 19 and 20 will make
  the delivery repeat or reorder; that is not built yet.
- **The data.** Three creates, one correction (`r-202`, overwritten the next morning), one return of
  Thursday's order 7021 (no customer id, so `clean_orders` does not hold it), and one withdrawal
  (`r-203`, deleted).

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
- **Runs and events** (`notebook/shop/runs.py`, Chapter 7). Every execution of a program in the
  repository records its program, what it read and how many rows, its code as it was that day, and
  for a function the object change that started it (`Week.executions`). `events(week, fields)` gives
  the events a reader's design would have sent: a start and a finish per run, each carrying the
  chosen fields where their value is known. `runs` groups them by any fields; `readings` sets a
  design against four readings of "Record every run."; `lineage` makes a graph from what runs read
  and wrote.
- **OpenLineage** (`notebook/shop/openlineage.py`, Chapter 8). `run_events` gives each run as a
  START and a COMPLETE or FAIL, in the specification's form, with standard facets and one of the
  shop's own; `check` holds an event to the specification's rules (`docs/sources.md`); `Consumer`
  accumulates events as the shop's own consumer. Every event was validated against the published
  schema outside the repository (`docs/notes/chapter-08.md`).
- **Ingestion** (`notebook/shop/ingest.py`, Chapter 9). `event_lines`, then `parse`, `normalise`,
  `objects` and `edges`, each a stage a notebook shows, every rule the shop's own.
- **Column lineage** (`notebook/shop/columns.py`, Chapter 10). The shop's own parser for the
  course's SQL, inside a program's code: for every column a program writes, the columns it reads, of
  two kinds, `value` (copied, computed, aggregated) and `rows` (filter, grouping, distinct). A
  table's columns are matched by position, so naming them needs the warehouse's catalogue; `*`
  names no column without it; a function is taken to depend on its arguments only. `upstream`
  follows every program whose code the shop has; `facet` writes OpenLineage's column lineage facet.
- **Schema versions** (`notebook/shop/schemas.py`, Chapter 11). Every write records the schema of
  what it wrote (`Execution.schema`: a file's fields and the JSON types of their values, or a
  table's declared columns); `versions`, `diff` (by name), `readers` (by column lineage) and
  `compare` (what three readers get with and without a change).
- **References** (`notebook/shop/identity.py`, Chapter 12). `resolve` finds what a reference names
  by its store's rules (the warehouse ignores case and fills in production's defaults; object
  storage reads keys exactly); `compare` tests pairs for the same text, object, rows, environment and
  version. Ingestion's `normalise` takes a database per producer.
- **Observations and freshness** (`notebook/shop/observe.py`, Chapter 13). What each run recorded as
  it ran (`Execution.bytes`, `Execution.error`), each asset's last write by its store's clock and the
  latest day its data holds, and the dashboard against three readings of "fresh", by the stores'
  clocks or by the runs'.
- **Quality** (`notebook/shop/quality.py`, Chapter 14). Each run of `build_clean_orders` counts, as it
  runs, the rows, the rows with no customer id, the rows that repeat an order and the rows with a
  quantity of 0 or less, in the file it read and the table it wrote (`Execution.quality`); `check`
  holds one count to a limit on every run, `reconcile` sets rows read against rows written, and
  `facets` writes OpenLineage's `dataQualityMetrics` and `dataQualityAssertions`.
- **Provenance** (`notebook/shop/provenance.py`, Chapter 15). `trace` follows one day's figure back
  to the lines of the version of `orders.jsonl` the run read, summing each step; files by the version
  read, tables as they are now, or `returns` as it was, rebuilt from the object versions the desk's
  functions read (`returns_as_of`). With `dropped`, the rows each run left out and why.
- **Impact** (`notebook/shop/impact.py`, Chapter 16). `downstream` walks the graph the week's events
  make; `downstream_columns` walks column lineage forward; `readers` sets what four readers got in
  two weeks side by side; `made_from` lists what the shop made from one return.
- **A backwards search** (`notebook/shop/cause.py`, Chapter 17). `search` measures one day's revenue,
  as the dashboard's program defines it, at each step back to the export, with whether each step
  differs from its input and whether its program's code changed since the night before.
- **Delivery** (`notebook/shop/delivery.py`, Chapters 18 to 20). `send` sends the week's events down
  a path to the collector, each a second after its event time and received two seconds later,
  with faults picked by job, type and day: an event lost, held up, or received with its
  acknowledgement lost; with `at_least_once`, a program sends an event again every 30 seconds until
  it is acknowledged, and with `restamp` builds it again with the new time. `open_runs` lists runs
  started and not ended, with how long the job's ended runs usually took; `repeated_work` finds a
  function started more than once for one change of one object; `object_states` gives each
  return's object its last change, by event time or by arrival. Ingestion gains `dedupe` (by
  content, or by run and type) and an arrival order for `objects`, which also keeps the run that
  last wrote each dataset (`written`).
- **Claims** (`notebook/shop/claims.py`, Chapter 21). Three sources' claims about `daily_sales`'s
  owner and columns (the warehouse's catalogue, read nightly; your records; the previous engineer's
  team sheet, imported nightly), each with when it was sent and when its source last changed, and
  `resolve` by `newest`, `as of`, `ranked` or `all`.
- **References across systems** (`notebook/shop/aliases.py`, Chapter 22). Six references to
  `daily_sales` or a thing named like it, and `merge` by `exact`, `qualified`, `last part` or
  `aliases`.
- **Scale** (`notebook/shop/scale.py`, Chapter 23). `measure` counts the week's metadata; `reach`
  measures how much of the job graph a traversal from each dataset follows; `project` scales the
  week's rates to ten million assets and counts the records four questions read, with and without
  an index, partitions or a depth limit; `first_over` gives the size at which each passes a budget
  of a million records. `retain` deletes events older than a number of days; `compact` folds runs'
  edges into job edges with their first and last times.
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
sent anywhere. When a later chapter needs what the learner built earlier, it restates it in a cell
of its own (Chapter 5 Chapter 4's records, Chapter 6 Chapter 5's, Chapter 8 Chapter 7's design as a
mapping), so each chapter runs on its own.

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
