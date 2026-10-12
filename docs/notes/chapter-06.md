# Chapter 6: What is lineage?

A working note. Written on 12 October 2026 with Chapter 5, as a notebook (`notebook/chapter_06.py`).

## What the chapter does

The checkout's developer asks what renaming `customer_id` in `orders.jsonl` affects (Chapter 2's
third question). The head of the shop gives the reader the repository of the jobs' code; the export
and the analyst's script are not in it. The reader:

- reads the four jobs' code, then records what each reads and writes as lines (`job ... reads:`,
  `job ... writes:`), filling in the two for `build_daily_sales` from its code; the model gains the
  type `job`, so a job, a plain word since Chapter 1, becomes a node between assets;
- sees the platform's map with arrows for the first time, drawn from those lines: records of what
  was made from what, and by which job, are **lineage**;
- writes what a change to `orders.jsonl` affects, then walks **downstream** (3 jobs, 3 assets, to
  the dashboard), **upstream** from the dashboard, and downstream from `products.csv`: nothing, as
  far as the lines go (Chapter 2's second question);
- adds Jo Marsh's belief as a line (`build_daily_sales` reads `clean_customers`), sees the
  dashboard seem to depend on `customers.jsonl`, and compares the lines with the code: the line is
  not borne out;
- tries a change, the `source` change, in which `build_daily_sales` reads the analyst's copy from
  Saturday: the lines written from today's code go stale (2 rows), while `daily_sales` holds the same
  rows, so only the code shows it, and the code shows only now;
- questions "Record the lineage of `daily_sales`." (below).

## What was built for it

- `notebook/shop/week.py`: `repository(week)`, the jobs' code as the shop's repository holds it,
  built from the same SQL the week runs, so the code shown is the code that runs; `reads_and_writes`
  (a small rule: `read("...")`, a table after `FROM` or `JOIN`, `write` or `refresh`); and the
  `source` change, which brings `copy` with it.
- `notebook/shop/graph.py`: `downstream` and `upstream` (walks over `reads` and `writes`), `only`
  (the lineage edges and the assets and jobs alone, for the map), the drawing in the order data
  flows when the graph has jobs, and `compare_with_code`, whose messages are Haiku's drafts of brief
  FC.

## Figures

### `platform`

- **Role:** reference
- **Serves:** the assets before any arrow; the lineage drawing below is the same platform with
  arrows.
- **Why now:** the comparison is the chapter's first payoff.

### `code`

- **Role:** inspect
- **Serves:** the evidence the reader records lines from: what each job reads and writes.
- **Why now:** the records cell asks the reader to fill in two lines from it.

### `lineage-map`

- **Role:** reference, drawn from the reader's lines
- **Serves:** the platform's map gains its relations, because something the reader built now records
  them (`CLAUDE.md`, "A figure shows only what the learner has been told or has built").
- **Why now:** the developer's question is answered by walking it.

### `downstream`

- **Role:** experiment
- **Objective:** the reader learns that what a change affects is a walk along recorded lineage, and
  only as good as the lines.
- **Known before:** the map; the code.
- **Driving question:** which assets does a change to `orders.jsonl` affect?
- **The action:** write the expectation and why, then read the walk, then the upstream walk and the
  walk from `products.csv`.
- **Why the action:** the reader commits to an impact list, as the developer would need.
- **Evidence:** 6 nodes downstream; 6 upstream from the dashboard; none downstream of `products.csv`.
- **Consequence:** the answer for `products.csv` is "nothing the lines know of", not "nothing".
- **Predictable:** yes, from the map.
- **Gives nothing away:** the prose above names the question, not the nodes.
- **Not knowing:** right for `products.csv`'s readers outside the repository, and the prose says so.
- **Next question:** what if a line is wrong?
- **An experiment:** commit, run, compare.

### `belief` and `stale`

- **Role:** experiment
- **Objective:** the reader discovers that lineage written by hand records a belief, which the code
  can refute, and goes stale when the code changes, which the data does not show.
- **Known before:** the lines, the code, the comparison's rule.
- **Driving question:** will the comparison report anything after the change, and will the rows of
  `daily_sales` change?
- **The action:** write both expectations, then run the changed week, the comparison and the rows'
  comparison.
- **Why the action:** the two outcomes differ (the comparison reports, the rows do not), which is
  the lesson.
- **Evidence:** 2 rows from the comparison; `True` for the rows.
- **Consequence:** the reader sees that code, not data, shows the change, and that code shows only
  now, which motivates Chapter 7.
- **Predictable:** yes.
- **Gives nothing away:** the prose above says the copy holds the same rows, which the reader needs
  to reason; it does not say what the comparison reports.
- **Not knowing:** not the right answer for these two questions; it is for "which nights read which
  source", which the chapter leaves to Chapter 7.
- **Next question:** what did the job read each night?
- **An experiment:** commit, run, compare.

## Requirements

The chapter questions "Record the lineage of `daily_sales`.", the plan's candidate.

1. **What it says:** record the lineage of `daily_sales`.
2. **What it might mean:** what someone says its job reads; what its job's code reads now; what it
   read each night; between tables or between columns.
3. **What each needs:** a person's line; the repository; a record made each time the job does its
   work; the input columns of each output column.
4. **What the records hold:** lines written from today's code, and a person's belief once added.
5. **Whether it is met:** as written, yes; under the code reading, today; under the other two, no.

## Originality

The obvious examples are a lineage tool's demo graph over a sample warehouse, or dbt's generated
dependency diagram of a staging-and-marts project. Here the reader writes the lineage lines
themselves from four short jobs of an invented shop, sees the shop's map gain arrows only then, and
meets lineage's two failures in the shop's own terms: a manager's belief written as a line, and a
line left behind by a code change that the data cannot reveal. The jobs, their code and the
repository are invented for the course; the code's `read`, `write` and `refresh` are the course's
own notation, not any library's.

## What the prose process caught

Briefs FA, FB and FC (`docs/notes/chapter-06/briefs/`), and GA for both chapters' warnings.

| Draft | Dropped, restored with the fewest words | Wrong, sent back |
| --- | --- | --- |
| FA | | |
| FB | | slot D stated the change to the job as a fact; the brief has it as a supposition the cell tries |
| FC | | |
| GA | | |

## Measured

12 October 2026, local build: Run all 8.0 to 9.3 s; peak memory 398 to 418 MB; 0.32 MB from Chapter
5's link.

## Known gaps

- The published page's run time is to be measured after the deploy.
- `reads_and_writes` is a small rule over the shop's own notation; Chapter 10 parses SQL properly.
