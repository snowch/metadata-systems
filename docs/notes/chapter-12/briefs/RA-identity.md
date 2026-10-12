# Brief RA: Chapter 12, "Identity"

Read `docs/notes/chapter-10/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms. The reader knows **column lineage** (Chapter 10), **schema evolution** and **breaking
change** (Chapter 11). This chapter introduces **environment** in slot B, **identity** in slot D and
**qualified name** in slot F, each in bold once, and none before its slot (not in slot A). Words you
must not use anywhere in this chapter: observation, freshness, alias, entity resolution, symlink
(except in slot P, where the brief gives it).

In this chapter, and only here, *schema* means what Chapter 8 called it in a warehouse name: a group
of tables inside a database, as `analytics` in `shop.analytics.daily_sales`. Do not use *schema* for
a dataset's columns anywhere in this chapter.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- See a run on a copy of the shop's tables join the shop's own graph.
- Decide, for six pairs of names, whether each pair names the same asset, then test each pair.
- Change ingestion's rule for names, and see the two runs part.
- Question the requirement "The same table must have one identity."

### Slot B: under the heading `## A run in development`

- On Monday at 10:20 a developer tries a change to `build_daily_sales`. The developer does not run it
  on the shop's tables but on copies of `clean_orders` and `daily_sales` in a second database of the
  warehouse, `shop_dev`, which holds Sunday's orders.
- A separate copy of the platform's data and programs, kept for one purpose, is an **environment**.
  Production holds the shop's real data and runs its real programs; development is where changes
  are tried.
- The developer's runner sends OpenLineage events, as the analyst's script did in Chapter 9: it
  names the tables `analytics.clean_orders` and `analytics.daily_sales`, without the database. Its
  jobs are in the namespace `dev`.
- The next cell runs the week with the returns desk and the development run, and ingests the events
  as Chapter 9 did.
- Before you read on, write in the next cell which programs you expect the graph to show writing
  `shop.analytics.daily_sales`, production's table.

### Slot C: the text inside that cell (between triple quotes)

One question, then `........` on its own line: which programs will the graph show writing
`shop.analytics.daily_sales`? At most about 60 characters a line. Plain text.

### Slot CC: after the cell that lists the edges of `daily_sales`

- Two: `shop/build_daily_sales`, in 7 runs, the last at `2026-09-14T02:30:21Z`; and
  `dev/build_daily_sales`, in 1 run, at `2026-09-14T10:20:04Z`.
- Chapter 9's rule for names gave the developer's names `shop`, production's database.
- The graph now says a run in development wrote production's `daily_sales`, and was the last to
  write it.

### Slot D: under the heading `## The same asset?`

- What makes two names refer to the same asset is the asset's **identity**.
- Six pairs of names, each used somewhere in the shop:
  1. `shop.analytics.daily_sales`, in the jobs' events, and `SHOP.ANALYTICS.DAILY_SALES`, in a
     query Jo Marsh typed in capitals;
  2. `daily_sales`, in the code of `refresh_dashboard`, and `shop.analytics.daily_sales`;
  3. `shop.analytics.daily_sales` and `shop_dev.analytics.daily_sales`, the developer's table;
  4. `shop.analytics.daily_sales` and `shop.analytics.sales_by_day`, a view Jo Marsh made over
     `daily_sales`: a name for a query, which holds no rows of its own;
  5. `s3://shop-raw/orders.jsonl` and `s3://shop-raw/Orders.jsonl`, which the supplier wrote on
     Friday 11 to test a new export;
  6. two versions of `s3://shop-returns/r-202.json`: as the desk created it on Wednesday 9, and as it
     overwrote it on Thursday 10.
- Before you read on, write in the next cell, for each pair, whether the two names refer to the same
  asset: yes, no, or you cannot tell yet.

Write the pairs as a numbered Markdown list.

### Slot E: the text inside that cell (between triple quotes)

One line asking whether each pair names the same asset, then the numbers 1 to 6, each on its own
line followed by `....`. At most about 60 characters a line. Plain text.

### Slot EE: after that cell

- The next cell asks each name's store what the name refers to.

### Slot F: after that cell

- Pair 1: both refer to `shop.analytics.daily_sales`. The warehouse reads a name without regard to
  case.
- Pair 5: two objects. Object storage reads a key exactly, case included, and the supplier's test
  file is there.
- Pair 2: `daily_sales` refers to production's table because `refresh_dashboard` runs with
  production's defaults, the database `shop` and the schema `analytics`. The same code run in
  development would refer to `shop_dev.analytics.daily_sales`.
- A name that holds everything its store needs to find the asset, with no defaults, is a
  **qualified name**: `shop.analytics.daily_sales`, or `s3://shop-raw/orders.jsonl`.
- The next cell tests each pair five ways: the same text, the same object, the same rows, the same
  environment, and the same version.

### Slot G: after that cell

- Pairs 1 and 2: the same object, rows and environment.
- Pair 3: none of these.
- Pair 4: the same rows and environment, but not the same object.
- Pair 5: the same environment only.
- Pair 6: the same object and environment, but not the same rows or version.
- The warehouse keeps no versions of a table, so that test is empty for pairs 1 to 4.

Write slot G as a Markdown list of the pairs, then one sentence.

### Slot H: under the heading `## "The same table must have one identity."`

- The head of the shop's requirement: "The same table must have one identity."
- Before you read on, write in the next cell what "the same table" means to you.

### Slot I: the text inside that cell (between triple quotes)

One question, then `........` on its own line: what does "the same table" mean to you? At most about
60 characters a line. Plain text.

### Slot READINGS: after that cell

- "The same" could mean four things, each needing something different:
  - the same name, once qualified and read by its store's rules: pairs 1, 2 and 6. It needs qualified
    names and each store's rules for case;
  - the same rows: pairs 1, 2 and 4. It needs a way to compare contents;
  - the same environment: pairs 1, 2, 4, 5 and 6. It needs to know which environment holds each
    asset;
  - the same version: none of the pairs is shown to be. It needs versions, which the warehouse does
    not keep for a table.
- The shop's ingestion joins two datasets when their namespace and name are the same, after it
  normalises them: the first reading. It compares names exactly, so it would keep pair 1 apart,
  which the warehouse reads as one table. Its rule for names joined pair 3, which no reading joins.
- The requirement does not say which "same" it means.

Write slot READINGS as one Markdown list of the four readings, then two short paragraphs.

### Slot J: under the heading `## A database for each producer`

- Chapter 9's rule gives `shop` to every name that leaves out its database.
- The next cell normalises the events again with a database for each producer. As it stands it
  lists none, so it gives the same answer as before.
- Delete the `# ` at the start of the line that gives the developer's runner `shop_dev`, select the
  cell and press **Run below**.

### Slot K: after that cell

- After the change, `dev/build_daily_sales` writes `shop_dev.analytics.daily_sales`, and
  `shop/build_daily_sales` is the only program that writes `shop.analytics.daily_sales`.
- The rule now lives in ingestion, and has to list each producer. A runner that sends qualified
  names needs no rule.

### Slot L: under the heading `## Before Chapter 13`

- Showed: a run in development joined production's graph because a rule for names filled in
  production's database. Six pairs of names were tested five ways, and the tests disagreed: a view
  had the same rows as its table and was another object; two versions were one object with
  different rows. A qualified name, read by its store's rules, found the object; the warehouse and
  object storage have different rules for case.
- Could not show: whether the dashboard is up to date, and by which clock.
- Next: Chapter 13 records what each run did as it ran, and asks how recent each asset is.
- Then three reflective questions, as a Markdown list:
  - Which of your platform's programs name a table without its database?
  - How would your lineage tell production's table from development's of the same name?
  - Which pairs of names in your platform would you join, and by which reading?

### Slot P: under the heading `### How this differs from a real platform`

- The developer, the view and the supplier's test file are invented for the course.
- The shop's rules for case are its own: its warehouse reads names without regard to case, and its
  object storage reads keys exactly. Each real store has its own rules, set out in its own
  documentation.
- OpenLineage's naming page gives a namespace for each kind of data store and a name inside it; for
  several warehouses, the name is `{database}.{schema}.{table}`.
- OpenLineage's `symlinks` facet lists other names for one dataset, such as a file's location and the
  table name a catalogue gives it.
- The shop's warehouse keeps no versions of a table. Some table formats keep a table's earlier
  states as snapshots.

## Slots

Write the file `docs/notes/chapter-12/drafts/RA.md` with the slots under `## A`, `## B`, `## C`,
`## CC`, `## D`, `## E`, `## EE`, `## F`, `## G`, `## H`, `## I`, `## READINGS`, `## J`, `## K`,
`## L` and `## P`, each the exact text to place, and nothing else in the file. Each slot that has a
heading starts with that heading.
