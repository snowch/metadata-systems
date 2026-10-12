# Chapter 13: Runtime metadata

A working note. Written on 12 October 2026 with Chapters 10, 11 and 12, as a notebook
(`notebook/chapter_13.py`). It ends Part III.

## What the chapter does

Chapter 2's failed night returns: `build_daily_sales` fails early on Monday 14 and the dashboard is
refreshed after it. The head of the shop's requirement is "The dashboard must be fresh." The
reader:

- writes which assets are not up to date at 09:00 on Monday, and how they would tell;
- meets **observation** and reads the week's 28 runs: one failed, with `database is locked`, and the
  refresh after it read 6 rows and showed 6 days;
- meets **freshness** with two measures (when the store says the asset was last written; the latest
  day its data holds) and finds them disagree: the dashboard is the most recent by the first and a
  day behind by the second;
- reads the three readings of "fresh" (refreshed lately; built from the latest data; showing the
  latest day), the dashboard against each (met, not met, not met), and the lineage step that fails;
- finds, under Chapter 11's `renamed` change, 4 runs that succeeded with 0 rows, and a dashboard that
  passes the first two readings and fails the third;
- finds, under the `clock` change, a dashboard refreshed "before" its input by the reporting tool's
  slow clock, changes `by="stores"` to `by="runs"`, presses **Run below**, and sees one clock put the
  writes in order;
- measures the returns table, written at any hour, against its source's last change.

## What was built for it

- `notebook/shop/observe.py`: `observations` (with a filter for rows written), `freshness`,
  `last_written` (each store's own clock), `last_run` (the runs' clock), `latest_day`, `chain` (by
  stores or by runs), `readings` and `source_changed`.
- `Execution.bytes` and `Execution.error`; the failed night's error.
- The `clock` change: the reporting tool's clock runs 40 minutes slow.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the assets measured, the returns table among them.
- **Why now:** every chapter opens with the map.

### `failed-monday`

- **Role:** experiment (with `freshness` and `three-readings`, which answer it)
- **Objective:** the reader learns that "up to date" has measures that disagree, and that the
  failed night left the dashboard newest by one and a day behind by another.
- **Known before:** Chapter 2's failed night; the nights' order.
- **Driving question:** which assets are not up to date at 09:00 on Monday, and how would you tell?
- **The action:** write the expectation and the test; read the observations, the measures and the
  readings.
- **Why the action:** the "how would you tell" half commits the reader to a measure.
- **Evidence:** 30.5 hours and Saturday 12 for `daily_sales`; 6.0 hours and Saturday 12 for the
  dashboard; met, not met, not met.
- **Consequence:** a reader who measured by refresh time learns it passed the dashboard.
- **Predictable:** yes, from Chapter 2.
- **Gives nothing away:** the prompt names the assets, not a measure.
- **Not knowing:** the right answer until "up to date" is defined, which the requirement section
  does.
- **Next question:** what if a run succeeds and writes nothing?
- **An experiment:** commit, run, compare.

### `observations`, `freshness`, `three-readings`, `chain`

- **Role:** inspect
- **Serves:** the evidence for the failed Monday, each with the question above it.
- **Why now:** the terms are given against them.

### `wrote-nothing`

- **Role:** inspect
- **Serves:** a status and a time that pass while the rows and the latest day do not.
- **Why now:** Chapter 11's change gives the case; it tests the readings again.

### `two-clocks`

- **Role:** experiment
- **Objective:** the reader learns that comparing times from two stores compares two clocks, and
  that one clock, the runs' events, puts the writes in order.
- **Known before:** the second reading's steps; the clock change.
- **Driving question:** was the dashboard refreshed before its input?
- **The action:** change `by="stores"` to `by="runs"`, press **Run below**, compare.
- **Why the action:** the same writes, compared by another clock, give the other answer.
- **Evidence:** 02:20:09 against 02:30:21, then 03:00:09.
- **Consequence:** a freshness check is only as right as the clocks it compares.
- **Predictable:** yes, once the clock is known to be slow.
- **Gives nothing away:** the reversal is shown first, with no cause; the dashboard's latest day is the evidence; the slow clock is named only after it.
- **Not knowing:** not the right answer.
- **Next question:** what of a table written at any hour?
- **An experiment:** change, run again, compare.

### `any-hour`

- **Role:** inspect
- **Serves:** a table measured against its source, not the night.
- **Why now:** the nightly rule's failure on the returns desk.

## Requirements

The chapter questions "The dashboard must be fresh.", the plan's candidate, with the failed night.

1. **What it says:** the dashboard must be fresh.
2. **What it might mean:** refreshed lately; built from the latest data; showing the latest day.
3. **What each needs:** the reporting tool's refresh time; each asset's last write along the lineage
   that feeds the dashboard, by one clock; the latest day the dashboard shows.
4. **What the shop records:** each store's last write by its own clock, the runs' times by one
   clock, the rows each run wrote, and the data itself.
5. **Whether it is met:** after the failed night, the first reading only; after the night that wrote
   nothing, the first two; with the slow clock, the second fails by the stores' clocks and passes by
   the runs'. The requirement does not say which reading it means.

## Originality

The obvious examples are a data observability product's "freshness, volume, schema" checks and an
orchestrator's documentation of a source freshness test with warn and error thresholds. This
chapter measures the shop's own assets after its own failed night, with readings taken from what
the head of the shop could mean, a run that succeeded and wrote nothing from Chapter 11's rename, a
clock fault in the shop's own reporting tool, and a table written on change. Its rules are the
shop's, labelled so.

## What the prose process caught

Brief SA, draft under `drafts/`. Every fact was right and no edit was needed. A cell that printed
raw Python dictionaries now prints a table (`observations(..., rows_written=0)`).

## The review

A reviewer on another model read the chapter as a learner (`review/findings.md`, 14 findings and
smaller ones) and an independent sceptic attacked each (`review/verdicts.md`). Acted on: the size
column is the table's or file's size after the run, renamed `size after (bytes)` (2); the clock
experiment shows the reversal first, asks whether it happened, uses the dashboard's latest day as
evidence, and only then names the slow clock; after the edit it says what one clock can and cannot
settle, and that the export's time is the platform's record, not an event's (1, 3); where the
observations come from, and what the events carry (4); a question before the nights that wrote
nothing, and what makes 0 stand out (5); no figure "says" (6); blank is not 0 (7); the closing
compares with the reader's first answer and says "refreshed lately" was met in every case (8);
questions before the instruments (9); restated tables went (10); the returns section's order, its
rule and its latest day (12); a sources entry for the facets named (14); "nights", "invented for
the course", and Part IV's mention folded into the next chapter. Rejected: a separate commit cell
for the requirement, and a figure of time (11). Brief SB drafted the new paragraphs; the draft named
the `clock` change and added a question before the reversal, and both were taken out. The drafting
agent tried one message, which was refused.

## Measured

See `docs/notes/notebook-prototype.md`, "Chapters 10 to 13".

## Known gaps

- The shop's events carry the times, the status and the row counts, not a size or the error;
  OpenLineage's `outputStatistics` (`size`) and `errorMessage` facets would carry them.
- Part IV records what the rows held (Chapter 14).
