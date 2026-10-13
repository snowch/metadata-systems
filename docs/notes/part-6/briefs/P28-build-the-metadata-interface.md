# Brief P28: Chapter 28, Build the metadata interface

Read `common.md` in this folder first, and `docs/style.md`. Write
`docs/notes/part-6/drafts/P28.md`, with one `## key` heading per slot below, in this order. A
heading inside a slot that this brief gives as `## ...` must be written as `### ...`. The chapter
introduces no new term.

## A

A list of four objectives:

- Build a page for one asset from the store, the collector's file, the lineage graph and the
  queries that Chapters 24 to 27 built.
- Write the page's run history, and find which run a first version leaves out.
- Choose the page's sections, and see what the page leaves out.
- Question the requirement "The asset page must show everything about an asset."

## B

- The heading `## A page for one asset`.
- The page is made of sections, each drawn from what the earlier chapters of Part VI built, in the
  shop's own versions: `description` and `owner` from the store and the owners' sources, `runs` from
  the collector's file, `upstream` and `downstream` from the lineage graph and the queries, `columns`
  from the warehouse, and `freshness` from Chapter 13's measure.
- The week is Chapter 27's, with Monday's failed run of `build_daily_sales`.
- You write one section's rows, `run_history(asset)`. `shop.interface.runs()` gives every run in the
  collector's file: its program, state, start, end, and the datasets it wrote. `shop.interface.writers
  (asset)` gives the programs the lineage graph records writing the asset. Write the second name as
  `shop.interface.writers(asset)`, on one line.
- The next cell lists the programs that write `daily_sales`: one, `build_daily_sales`. The file holds
  41 runs in all.

## C

- The next cell holds `run_history` as it stands: it keeps the runs whose written datasets include
  the asset.
- Before you read on, write in the next cell whether that run history for `daily_sales` will include
  Monday's run.

## CC

Two lines: the question, then a line of eight full stops.

- The question: will the run history include Monday's run of `build_daily_sales`?

## D

- The check finds 6 runs, and not Monday's. Monday's run failed and wrote nothing, so the datasets it
  wrote are none, and a run history built from what each run wrote leaves it out.
- Compare this with what you wrote.
- Change `run_history` so that it keeps the runs of the programs that write the asset, from
  `shop.interface.writers(asset)`. Select the cell and press **Run below**. The check finds 7 runs,
  the `FAIL` among them.
- Then this heading: `## The sections`
- The next cell holds the page's sections as a list, `sections`. As it stands, it has `description`,
  `owner` and `runs`. The cell after it draws the page for `daily_sales`, and ends with the sections
  the page leaves out: `upstream`, `downstream`, `columns` and `freshness`.
- Add the sections you would want on the page, from the seven names. Select the cell and press
  **Run below**.

## RH

- The heading `## Everything about an asset`.

## E

- Before you read on, write in the next cell what "everything" means to you here.

## EE

Two lines: the question, then a line of eight full stops.

- The question: what does "everything about an asset" mean here?

## F

- "Everything" could mean three things, and each needs something different. Then a list:
  - every section the shop can draw: the seven names, all on one page;
  - everything a person asking about the asset needs: the sections that answer their question. Who
    to ask about `daily_sales` needs `owner`; why its latest day is Saturday 12 needs `runs` and
    `freshness`;
  - the asset's whole history: every run and every claim, which grows every night.
- The page draws the sections you chose and says which it leaves out, so whoever reads it can tell
  what it does not show.
- The requirement does not say which it means.

## Z

- The heading `## Before Chapter 29`.
- Summary facts, in order: the page took its sections from the store, the collector's file, the
  lineage graph and the queries of Chapters 24 to 27; a run history built from what each run wrote
  left out Monday's failed run, which wrote nothing; built from the programs that write the asset, it
  held all 7 runs; the page named the sections it left out.
- Part VI ends here. Chapter 29 starts Part VII, where real producers and a real consumer of
  OpenLineage events meet the shop's own collector.
- Three questions, as a list: Which runs does your catalogue's history of an asset leave out? Which
  sections of your asset pages does anyone read? What does your asset page not show, and does it
  say so?
- The heading `### How this differs from a real platform`, and one bullet:
  - The shop's page is drawn in the notebook from the shop's own code, for one asset at a time.
