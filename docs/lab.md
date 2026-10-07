# The Metadata Lab

The data platform every figure runs, and the metadata system the learner builds on top of it. A
figure is a view of the lab: what it shows, the lab computed. This file is the lab's design; the
code is `packages/lab`, and where the two differ, the code and its tests are right and this file
is out of date.

## Two halves

- **The shop**: a small online shop's data platform, which really runs. It has files and tables
  with real rows, programs written in the course's SQL subset that really transform them, a
  scheduler, a clock and the storage systems that hold the results.
- **The learner's metadata system**: the records, events, store, graph and queries the learner
  builds, chapter by chapter, about the shop. In Chapter 1 it is empty: the learner has the shop's
  storage and nothing else.

## The shop

An online shop that sells bicycle parts. It is invented for the course; so are its products,
customers and staff.

### Where its data lives

| System | What it holds | What it records about each thing it holds |
| --- | --- | --- |
| Object storage, bucket `shop-raw` | `customers.parquet`, `orders.parquet`, `products.parquet`, written each night by an export from the shop's checkout and catalogue | the object's key, size and last-modified time; a Parquet file's own footer holds its column names and types and its row count |
| The warehouse, database `shop`, schema `analytics` | `clean_customers`, `clean_orders`, `daily_sales` | each table's columns and types, row count, last-altered time and the role that owns it |
| The reporting tool | `sales_dashboard`, a chart of revenue per day | the dashboard's title, who created it, when it last refreshed and the values it shows |

These records are the lab's choice of what a typical system of each kind keeps; the lab does not
model why a system keeps a field. The reporting tool keeps no query: a program fills the
dashboard, as programs fill the tables. A program that writes no rows still moves its table's
last-written time, so in the lab only a failed write leaves the time stale. Real systems differ:
some table formats keep history the lab's warehouse does not, such as Apache Iceberg's snapshots
and Delta Lake's record of each write (`docs/sources.md`). Each chapter's model-versus-reality
note says which difference matters to it.

### The programs

Four programs run each night, in this order, all as the warehouse role `etl_service`. Their code
is in `packages/lab/src/shop/programs.ts`, in the course's SQL subset.

| Program | Reads | Writes | How |
| --- | --- | --- | --- |
| clean customers | `customers.parquet` | `clean_customers` | replaces the table: lower-cases every email and drops customers with no email |
| clean orders | `orders.parquet` | `clean_orders` | replaces the table: keeps one copy of each order, drops orders with no customer id, drops orders whose quantity is 0 or less |
| daily sales | `clean_orders` | `daily_sales` | appends one row for the day before: that day's revenue, the sum of price times quantity over its completed orders |
| dashboard refresh | `daily_sales` | `sales_dashboard` | reads every row and redraws the chart |

`daily_sales` is appended to, not rebuilt: each night adds one row and never revisits the rows
before it. That is common in real platforms, and it is why a change to the program shows only in
the rows written after the change.

### The week

The course's week is Monday 7 to Sunday 13 September 2026. Each night the export writes the
orders placed so far, then the four programs run. The learner arrives on Monday 14 September,
after the last night's run, and finds the lab as that run left it.

The week's orders are hand-written in `packages/lab/src/shop/data.ts`, so each property below is
deliberate:

- some days are plain, and on them the raw orders add up to the day's revenue;
- one day has a cancelled order, which the raw file keeps and revenue leaves out;
- one day has an order that the export wrote twice;
- on Thursday the checkout sent some orders with no customer id, and the rule in clean orders
  that drops such orders made Thursday's revenue low. This is the shop's incident: Chapter 1 shows
  its symptom and later chapters measure it, trace it and find its cause;
- no order has a quantity of 0 or less, so nothing in the week's data shows that clean orders
  has a rule for them.

Every number a chapter states about the week is computed by the lab and pinned by that chapter's
facts test; this file states none.

### Changes

A figure can run the week again with a change to the shop and compare what the learner can see
before and after. Each change is a function of the shop's definition, so the changed week is as
deterministic as the plain one. Chapter 1 uses three:

- **An analyst's copy.** A script copies `clean_orders` to `shop-scratch/clean_orders_copy.parquet`
  every night, before daily sales runs.
- **A program edited for refunds.** From Saturday's row on, daily sales keeps every order whose
  status is not "refunded", where it kept completed orders. The shop has no refunds yet, so the
  edit changes nothing except on a day with a cancelled order.
- **A failed night.** On the last night, daily sales fails and writes nothing.

Later chapters add their own: a renamed column, a late file, a duplicated event, a second
environment.

## What a learner can ask of the lab

`packages/lab` answers three kinds of question, and the figures show each answer with its
evidence:

- **What storage records.** The storage view: for each asset, exactly the fields the table above
  lists, as of Monday morning.
- **What the data suggests.** Inference from contents alone: which queries over the other assets
  reproduce an asset's rows, which assets show the same numbers as another, what a last-written
  time implies. The lab searches a fixed space of queries and reports every one that fits, so a
  figure can show that two different sources fit equally well.
- **What only a record answers.** The questions whose answers are in neither: who is responsible
  for an asset, what a number's unit is, what changed and why.

Each question's classification is computed by running the storage view and the inference search,
never written into the lesson.

Three more things the figures ask of it:

- **The map of the platform** (`platformMap`): the systems in the order data moves through them
  (a system nothing flows into first), the assets each holds in the week asked about, and the
  flows between systems, each from what a program reads to what it writes. A flow names two
  systems and nothing else: never a program, never an asset. The map shows what a newcomer is
  told on the first morning, and nothing Chapter 1 finds storage cannot tell. `mapTally` counts
  what it holds, kind by kind and in all, for the count under the opening's map.
- **The week, as it ran** (`weekTimeline`): the days the shop took orders, the night of work after
  each with when its first write began and its last ended, and the morning the learner starts
  (`ARRIVAL`). It says when the nights were and nothing about what a night wrote, which writer ran
  when, or which asset is made from which.
- **A prediction's answer** (`runProbe`): the owner a table's system records, what kind of
  name it is, and how many of the warehouse's tables record an owner at all (`owner-kind`, which
  the requirement figure reads as well); one day's total over an asset against the target's row for that day,
  as the same, more or less, with every day's two totals for the evidence (`day-total`); how many
  settings of the cleaning rules rebuild `clean_orders` (`clean-fits`). A prediction's option
  names the answers it stands for, so the lesson never stores the answer.

## The course's SQL subset

The programs, the queries a learner builds and, from Chapter 9, the queries the learner writes
are all in one small SQL dialect, parsed and run by the lab (`packages/lab/src/sql`): `SELECT`
with expressions and aliases, `DISTINCT`, `FROM` one table or file, `WHERE`, `GROUP BY`, `ORDER
BY`, `CAST`, `SUM`, `COUNT`, `MIN`, `MAX`, `LOWER`, `COALESCE`, three-valued logic with `NULL`, and
named parameters such as `:day`. Money is held as whole pennies, so sums are exact. Joins arrive
with the chapter that needs them. A construct outside the subset is refused with a plain message,
not a parse error.

## The learner's state

The lab a figure runs is a pure function of two things: the shop's definition, and the learner's
graded work from every earlier chapter.

- Each chapter's work is stored by the platform's runtime, one key per chapter
  (`ms:v1:<chapter id>`), and is graded again every time it is read, as the runtime grades a
  challenge on load.
- When a figure needs what the learner built earlier (their records in Chapter 3, their event
  design in Chapter 7), the book reads that chapter's stored work, grades it, and uses it only if
  it passes. Otherwise the figure uses the course's reference and says so on the page.
- So there is no separate "lab state" to drift from the learner's work or to be edited into a
  pass, and resetting a chapter's work resets what later chapters see of it.

## Determinism

The same code gives the same rows, times and identifiers on every machine. The lab has no wall
clock (its clock is the week's), no `Math.random` (an identifier the lab needs, such as a run's
UUID from Chapter 6, is derived from the run's job and time), and no formatting that depends on
the browser's locale or time zone. Every time is UTC.

## What the lab does not model

- Real storage formats: a Parquet file's footer is modelled as the fields it records, not as
  bytes. Sizes are estimated from the rows.
- Concurrency inside a night: the programs run one after another.
- Time zones: every time is UTC, and an order's day is its UTC date.
- Permissions, until a chapter needs them.
