# Chapter 14: Data quality as metadata

A working note. Written on 12 October 2026 with Chapters 15, 16 and 17, as a notebook
(`notebook/chapter_14.py`). It opens Part IV.

## What the chapter does

Chapter 13 ended on what its observations could not show: what the rows each run read held. The
reader:

- reads what each run of `build_clean_orders` counted in the file it read: rows, rows with no
  customer id, rows that repeat an order, rows with a quantity of 0 or less; and meets **data
  quality**;
- meets the head of the shop's requirement "No order without a customer." as the developer's
  **assertion** on `clean_orders`, writes which runs will fail it, and finds that none does: the
  rule `customer_id IS NOT NULL` removed the rows first;
- changes the assertion's dataset to `orders.jsonl`, presses **Run below**, and sees 4 runs fail;
- sets rows read against rows written, and finds 3 rows left out from Friday 11, a test that reads
  both datasets of one run;
- writes what the requirement means, then reads three readings (in the file, in `clean_orders`, on
  the dashboard) and the shop's verdict on each: not met, met, not met;
- reads the same counts and assertion as OpenLineage's `dataQualityMetrics` and
  `dataQualityAssertions` on the input of `run-014`.

## What was built for it

- `Execution.quality`: each run of `build_clean_orders` counts four things in the file it read and
  the table it wrote, as it runs (`week.measure`, `week.METRICS`).
- `notebook/shop/quality.py`: `measurements`, `check`, `reconcile`, `left_out`, `readings` and
  `facets`. The facets validate against the published schemas (below).

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** where `orders.jsonl` and `clean_orders` sit.
- **Why now:** every chapter opens with the map.

### `counts`

- **Role:** inspect
- **Serves:** what each run counted in the file, before any rule is tested.
- **Why now:** the assertion's prediction needs the file's counts in view.

### `assertion-after-the-rule`

- **Role:** experiment
- **Objective:** the reader discovers that an assertion on a table written after a filter cannot
  find the rows the filter removed, and that where an assertion runs decides what it can find.
- **Known before:** Chapter 2's rule that drops orders with no customer id; the file's counts just
  above.
- **Driving question:** which runs fail "no customer_id in `clean_orders` is at most 0"?
- **The action:** write the expectation; read the result; change the dataset to `orders.jsonl` and
  press **Run below**.
- **Why the action:** the same assertion, moved from the table to the file, fails where it passed.
- **Evidence:** 7 passes on the table; 4 failures on the file, from Friday 11.
- **Consequence:** a reader who expected Friday's run to fail learns why it did not, and where it
  would have.
- **Predictable:** yes, by a reader who connects Chapter 2's rule to the table.
- **Gives nothing away:** the prompt names the table and the count, not the rule.
- **Not knowing:** a fair first answer, which the result settles.
- **Next question:** can one test catch it from the run's own two datasets?
- **An experiment:** commit, run, change, run again.

### `rows-read-and-written`

- **Role:** inspect
- **Serves:** a test over one run's input and output, which shows rows left out but not why.
- **Why now:** it answers the next question above.

### `three-readings`

- **Role:** inspect (the evidence of the requirement exercise)
- **Serves:** the shop's verdict on each reading, after the reader has written theirs.
- **Why now:** the readings are listed first, each with what it needs.

### `facets`

- **Role:** reference
- **Serves:** the counts and the assertion in an open standard's form.
- **Why now:** Part II made the events; the counts belong in them.

## Requirements

The chapter questions "No order without a customer.", the plan's candidate.

1. **What it says:** no order without a customer.
2. **What it might mean:** none in the file the checkout sends; none in `clean_orders`; every
   completed order counted on the dashboard against its customer. And, unsaid, what should happen to
   one: dropped, kept, or the night's work stopped.
3. **What each needs:** a count in the file on every run; a count in the table on every run; the
   file's orders set against the dashboard's totals.
4. **What the shop records:** the counts of each run of `build_clean_orders`, in both datasets.
5. **Whether it is met:** in the file, not (4 runs); in `clean_orders`, on every run, because the
   rule removes the orders first; on the dashboard, not (Thursday's 3 orders, 15400 pence). The
   requirement does not say which reading it means.

## Originality

The obvious examples are a data testing tool's `not_null` and `unique` tests on an orders model,
and a data quality library's expectation that a column has no nulls, run on a sample dataset. This
chapter tests the shop's own requirement on the shop's own run, places the same assertion before and
after the shop's own filter to show it cannot fail after it, and sets one run's input against its
output. The counts, their names and the readings are the shop's own.

## What the prose process caught

Brief TA, draft `drafts/T.md`. One fact wrong: "The shop's requirement" for the head of the
shop's; corrected. One sentence of mine changed in reading the chapter whole: "From this chapter,
each run…" narrated the course, and became "Each run … now also counts". Haiku wrote "total" for a
number on the dashboard where the brief wrote "figure", which the course keeps for an interactive
box; the briefs of Chapters 15 to 17 had the same fault, corrected there.

## Sources

OpenLineage's `DataQualityMetricsDatasetFacet` (1-0-1) and `DataQualityAssertionsDatasetFacet`
(1-1-0), read at commit `07864a6b5f` (`docs/sources.md`). The facets of four runs, and each inside
a whole run event, validated against the published schemas with `jsonschema` 4.26 outside the
repository: 12 checked, 0 problems; an assertion with `success` removed was refused.

## The review

To be done with the review of Part IV.

## Measured

Locally, 12 October 2026 (`docs/notes/notebook-prototype.md`, "Chapters 14 to 17"): from Chapter 13's link, 11 files, 0.32 MB, in a new tab; Run all 8.3 to 8.9 s; peak memory 395 to 402 MB alone, 619 MB with Chapter 13 open; no error output. Live: to be measured once published.

## Known gaps

- The shop counts only what `build_clean_orders` reads and writes.
- The count of repeats does not name the order that repeats (7015), and the page does not either.
