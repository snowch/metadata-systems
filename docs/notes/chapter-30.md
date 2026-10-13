# Chapter 30: Airflow, Spark, dbt and Trino

A working note. Written on 13 October 2026 with Chapters 29, 31 and 32 (`notebook/chapter_30.py`).

## What the chapter does

The shop's nightly work, imagined in four systems, over the week with the returns desk, the
analyst's copy and Monday's failed night. The reader:

- reads what each system calls a job and a run, where its inputs come from and when it sends;
- reads Airflow's 7 task instances of `build_daily_sales`: Monday's failed twice, `try_number` 2,
  2 OpenLineage runs, so 8 in all;
- reads Spark's job name for an insert into `daily_sales`
  (`shop_nightly.execute_insert_into_hadoop_fs_relation_command.shop_analytics_daily_sales`);
- reads one night's dbt run: three models' events all sent at 02:30:21 or later;
- predicts how many jobs Trino's events make of the 7 nightly queries; finds 7 (28 for four
  programs); changes the name format to `$SOURCE` and finds one job holding four programs' runs; gives
  each program its own source; 2 of 2;
- questions "Capture lineage from Airflow, Spark, dbt and Trino."

## What was built for it

`notebook/shop/integrations.py`: `rules`, `airflow`, `spark`, `dbt`, `trino`, `check_trino`,
`jobs_by_format`, with the name format and sources as the reader's piece. Every rule is cited in
`docs/sources.md`, "Read for Part VII".

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `rules`, `airflow`, `spark`, `dbt`

- **Role:** inspect, each
- **Serves:** where does each system's metadata come from? Its own job and run, and what its
  integration sends for the shop's `build_daily_sales`.
- **Why now:** the Trino prediction is reasoned from the rule set out in the same way.

### `trino-jobs`

- **Role:** experiment
- **Objective:** the reader finds that a job's identity in the lineage is whatever the integration's
  name format makes it: one job per query by default, one job for every program with a shared
  source.
- **Known before:** Chapter 12's identity; Chapter 22's over-merge.
- **Driving question:** how many jobs do the 7 nightly queries of `build_daily_sales` make?
- **The action:** write the prediction; read the check; change `name_format`; then `source_of`.
- **Why the action:** each change shows one consequence of the format.
- **Evidence:** 7 jobs; then 1 job with four programs' runs; then 1 job with its own runs.
- **Consequence:** a job's name in an integration's events is a setting, not a fact about the work.
- **Predictable:** yes, from the default the page states.
- **Gives nothing away:** the cell asks for a count; the rule is stated, the count is not.
- **Not knowing:** fair.
- **Next question:** which meaning of "capture lineage" does the shop want?

## Requirements

"Capture lineage from Airflow, Spark, dbt and Trino." (the plan's). Readings: by each system's own
job; by the shop's programs (needs a mapping, as Chapter 22's aliases); by the datasets read and
written (needs consistent dataset names, and misses what a system does not send). The figure that
questions it is the free-text cell after the box.

## Originality

The obvious examples are each integration's quickstart: a sample Dag, a Spark word count, a dbt
starter project and a sample query. This chapter runs none: it applies each integration's naming and
timing rules, as their code states them, to the shop's own nightly work, and every name shown (the
Dag, the application, the dbt project, the sources) is the shop's.

## What the prose process caught

Brief P30 (`part-7/briefs/`), draft `part-7/drafts/P30.md`. Fixed with the fewest words, as
placement edits (`place_p7.py`): a "The question:" label at the head of two of the reader's cells in
Chapters 31 and 32; a fragment introducing Chapter 31's list of rules; "sets" for "holds" of a cell in
Chapter 29; and Chapter 30's first mention of the provider, which now names it and Chapter 29. In
Chapter 32 the draft put "the forecast" for "a trained model", following the brief's rule on "model";
kept.

## Measured

Locally, 13 October 2026, before the review (`docs/notes/notebook-prototype.md`, "Chapters 29 to
32"): from Chapter 29's link, 11 files, 0.32 MB, in a new tab; Run all 8.4 to 8.8 s; peak memory 394 to 404 MB alone, 610 MB with Chapter 29 open; no
error output, no console error. The browser test types the reference into the chapter's cell and
reads the check.
