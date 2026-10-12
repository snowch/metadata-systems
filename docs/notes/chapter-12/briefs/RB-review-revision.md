# Brief RB: Chapter 12, "Identity", after its review

Read `docs/notes/chapter-10/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
brief RA's terms and its rule for *schema* (in this chapter only, a group of tables inside a
database). A review found: a sentence that blamed the wrong step of ingestion; verdicts given for
one reading of four; the readings shown as table headings before the reader committed; an
environment test whose answers come from the shop's naming, unsaid; descriptions of two pairs that
gave their answers away; Chapter 9's rule stated only after the prediction that rests on it; "copies"
that are not copies; and a closing about the next chapter's subject. The page's order changes: the
requirement section now comes before the five tests. These slots replace paragraphs.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- See a run in a second database of the warehouse join the shop's own graph.
- Decide, for six pairs of names, whether each pair names the same asset, then test each pair.
- Question the head of the shop's requirement about when two names are one table.
- Change ingestion's rule for names, and see the two runs part.

### Slot B: under the heading `## A run in development`

- On Monday at 10:20 a developer tries a change to `build_daily_sales`, not on the shop's tables but
  in a second database of the warehouse, `shop_dev`. It holds tables of the same names and columns
  as `clean_orders` and `daily_sales`, with Sunday's orders in `clean_orders`.
- A separate set of the platform's data and programs, kept for one purpose, is an **environment**.
  Production holds the shop's real data and runs its real programs; development is where changes are
  tried.
- The developer's runner sends OpenLineage events, as the analyst's script did in Chapter 9: it names
  the tables `analytics.clean_orders` and `analytics.daily_sales`, without the database. Its jobs are
  in the namespace `dev`.
- Chapter 9's ingestion gives `shop`, the production database, to a warehouse name that leaves out
  its database.
- Before you read on, write in the next cell which programs you expect the graph to show writing
  `shop.analytics.daily_sales`, production's table.
- The cell after it runs the week with the returns desk and the development run, and ingests the
  events as Chapter 9 did.

### Slot CC: after the cell that lists the edges of `daily_sales`

- Two: `shop/build_daily_sales`, in 7 runs, the last at `2026-09-14T02:30:21Z`; and
  `dev/build_daily_sales`, in 1 run, at `2026-09-14T10:20:04Z`.
- The graph now says a run in development wrote production's `daily_sales`, and was the last to
  write it.

Write the two programs as a Markdown list after one lead sentence.

### Slot D: under the heading `## The same asset?`

- What makes two names refer to the same asset is the asset's **identity**.
- Six pairs of names, each used somewhere in the shop:
  1. `shop.analytics.daily_sales`, in the jobs' events, and `SHOP.ANALYTICS.DAILY_SALES`, in a query
     Jo Marsh typed in capitals;
  2. `daily_sales`, in the code of `refresh_dashboard`, and `shop.analytics.daily_sales`;
  3. `shop.analytics.daily_sales` and `shop_dev.analytics.daily_sales`, the same table name in the
     development database;
  4. `shop.analytics.daily_sales` and `shop.analytics.sales_by_day`, a view Jo Marsh made over
     `daily_sales`;
  5. `s3://shop-raw/orders.jsonl` and `s3://shop-raw/Orders.jsonl`, which the supplier wrote on
     Friday 11 to test a new export;
  6. two versions of `s3://shop-returns/r-202.json`: as the desk created it on Wednesday 9, and as it
     overwrote it on Thursday 10. In the next cells, `@` followed by a version names one version of
     an object.
- Before you read on, write in the next cell, for each pair, whether the two names refer to the same
  asset: yes, no, or you cannot tell yet.

Write the pairs as a numbered Markdown list.

### Slot F: after the cell that asks each store what each name refers to

- Pair 1: both refer to `shop.analytics.daily_sales`. The warehouse reads a name without regard to
  case.
- Pair 5: two objects. Object storage reads a key exactly, case included, and the supplier's test
  file is there.
- Pair 2: `daily_sales` refers to production's table because `refresh_dashboard` runs with
  production's defaults: the database `shop` and the schema `analytics`, a group of tables inside the
  database, as Chapter 8 named it. The same code run in development would refer to
  `shop_dev.analytics.daily_sales`.
- Pair 4: a view is a name for a query; `sales_by_day` holds no rows of its own and shows those of
  `daily_sales`.
- A name that holds everything its store needs to find the asset, with no defaults, is a **qualified
  name**: `shop.analytics.daily_sales`, or `s3://shop-raw/orders.jsonl`.

### Slot H: under the heading `## "The same table must have one identity."`

- The head of the shop's requirement: "The same table must have one identity."
- Before you read on, write in the next cell what "the same table" means to you.

### Slot READINGS: after that cell

- "The same" could mean four things, each needing something different:
  - the same name, once qualified and read by its store's rules: qualified names and each store's
    rules for case;
  - the same rows: a way to compare contents;
  - the same environment: which environment holds each asset;
  - the same version: a version for each asset.
- The next cell tests each pair against each reading, after a test of the plain text:
  - same text: the two names as written;
  - same object: what each store says the name refers to;
  - same rows: the rows of a table, or the contents of an object;
  - same environment: from the database, `shop` for production and `shop_dev` for development; the
    shop's object storage has one environment, production;
  - same version: the object's version; the warehouse keeps no versions of a table, so the test is
    empty for a table.

Write slot READINGS as one Markdown list of the four readings, then a lead sentence and a second
Markdown list of the five tests.

### Slot G: after that cell

- No pair has the same text, yet pairs 1 and 2 are the same object, with the same rows and
  environment.
- "Same asset?" depends on the test. Pair 4 has the same rows and environment, but is another object.
  Pair 6 is one object, but not the same rows or version. For pairs like these, "cannot tell yet" was
  a fair answer until "same" had a meaning.
- By reading, against what the shop's graph holds:
  - the same name: met in part. Ingestion qualifies a name that leaves out its database, then
    compares names exactly. It would keep pair 1 apart, which the warehouse reads as one table. It
    gave the developer's `analytics.daily_sales` the production database, as with pair 2 but with the
    wrong default, and so joined two tables that no reading joins;
  - the same rows: not met. The graph compares no rows;
  - the same environment: not met. The graph records no environment for an asset;
  - the same version: not met for a table. The warehouse keeps no versions of a table.
- The requirement does not say which "same" it means.

Write slot G as two short paragraphs, a lead line, a Markdown list of the four verdicts, then one
sentence.

### Slot J: under the heading `## A database for each producer`

- The next cell normalises the events again with a database for each producer. As it stands it lists
  none, so it gives the same answer as before.
- Delete the `# ` at the start of the line that gives the developer's runner `shop_dev`. Before you
  press **Run below**, decide what `dev/build_daily_sales` will write. Then select the cell and press
  **Run below**.

### Slot K: after that cell

- After the change, `dev/build_daily_sales` writes `shop_dev.analytics.daily_sales`, and
  `shop/build_daily_sales` is the only program that writes `shop.analytics.daily_sales`.
- Only a producer whose names mean another database needs a line; any other gets `shop`.
- The rule ties a database to a producer, which is code, not an environment: the same runner used in
  production would get `shop_dev` too. A runner that sends qualified names needs no rule.

### Slot L: under the heading `## Before Chapter 13`

- A run in development joined production's graph, because ingestion filled in production's database
  for a name that left it out. Six pairs of names were tested, and the tests disagreed: a view had
  the same rows as its table and was another object; two versions were one object with different
  rows. A qualified name, read by its store's rules, found the object; the warehouse and object
  storage have different rules for case.
- The shop's graph records no environment for an asset, compares no rows, and keeps no versions of a
  table, so most readings of "the same" cannot be met from it.
- Chapter 13 turns from what an asset is to how recent it is: it records what each run did as it ran.
- Then the same three reflective questions as now, as a Markdown list (keep their wording):
  - Which of your platform's programs name a table without its database?
  - How would your lineage tell production's table from development's of the same name?
  - Which pairs of names in your platform would you join, and by which reading?

### Slot P: under the heading `### How this differs from a real platform`

- The developer, the view, Jo Marsh's query in capitals and the supplier's test file are invented for
  the course.
- The shop's rules for case are its own: its warehouse reads names without regard to case, and its
  object storage reads keys exactly. Each real store has its own rules, set out in its own
  documentation.
- OpenLineage's naming page gives a namespace for each kind of data store and a name inside it; for
  several warehouses, the name is `{database}.{schema}.{table}`.
- OpenLineage's `symlinks` facet lists alternative identifiers for one dataset, such as a physical
  location and a logical table name.
- The shop's warehouse keeps no versions of a table. Some table formats keep a table's earlier
  states as snapshots.

Write slot P as a Markdown list.

## Slots

Write the file `docs/notes/chapter-12/drafts/RB.md` with the slots under `## A`, `## B`, `## CC`,
`## D`, `## F`, `## H`, `## READINGS`, `## G`, `## J`, `## K`, `## L` and `## P`, each the exact text
to place, and nothing else in the file. Each slot that has a heading starts with that heading.
