# Chapter 6: What is lineage?

A working note. Written on 12 October 2026 with Chapter 5, as a notebook (`notebook/chapter_06.py`).

## What the chapter does

The checkout's developer asks what renaming `customer_id` in `orders.jsonl` affects (Chapter 2's
third question). To answer it, the head of the shop gives the reader the repository of the jobs'
code; the export and anything done by hand are not in it. The reader:

- reads the four jobs' code, and the records gain lines from it for what each job reads and writes
  (`job ... reads:`, `job ... writes:`), beside Chapter 5's records in full; the model gains the type
  `job`, so a job, a plain word since Chapter 1, becomes a node between assets;
- sees the platform's map with arrows for the first time, drawn from those lines in the direction
  data moves (unlike Chapter 5's arrows, and the page says so): records of what was made from what,
  and by which job, are **lineage**;
- writes which assets the rename affects, then reads the traversal **downstream** of `orders.jsonl`
  (3 jobs, 3 assets): the most the rename could affect; the code narrows it, since only
  `build_clean_orders` names `customer_id`; columns wait for Chapter 10. Then **upstream** from the
  dashboard, and downstream from `products.csv`: nothing, as far as the lines go (Chapter 2's
  second question);
- adds Jo Marsh's belief as a line (the daily sales job counts only known customers, so reads
  `clean_customers`), sees the dashboard seem to depend on `customers.jsonl`, writes from the code
  whether the belief holds and which job leaves out orders with no customer id, then compares the
  lines with the code: the line is not borne out, and `build_clean_orders`' `WHERE` answers Jo's
  Chapter 5 question;
- tries the `source` change, in which `build_daily_sales` reads the analyst's copy from Saturday:
  the lines written from today's code go stale (2 rows), while `daily_sales` holds the same rows;
- questions "Record the lineage of `daily_sales`." (below).

## What was built for it

- `notebook/shop/week.py`: `repository(week)`, the jobs' code as the shop's repository holds it,
  built from the same SQL the week runs, so the code shown is the code that runs; `reads_and_writes`
  (a small rule: `read("...")`, a name after `FROM` or `JOIN`, which is a name `read` gave or a
  warehouse table, and `write` or `refresh`); and the
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
- **Serves:** the evidence for what each job reads and writes, which columns it names, and what it
  leaves out.
- **Why now:** the developer's and Jo's questions are both answered from it.

### `lineage-map`

- **Role:** reference, drawn from the reader's lines
- **Serves:** the platform's map gains its relations, because something the reader built now records
  them (`CLAUDE.md`, "A figure shows only what the learner has been told or has built").
- **Why now:** the rename's traversal is read against it. The prose above it does not list its
  parts; the prediction below it asks about a column, which the drawing does not show.

### `downstream`

- **Role:** experiment
- **Objective:** the reader learns that a traversal along lineage between files and tables gives the
  most a change could affect, and that which assets a column's rename reaches needs more than these
  lines.
- **Known before:** the code; the map.
- **Driving question:** which assets does renaming `customer_id` in `orders.jsonl` affect?
- **The action:** write the expectation and why; read the traversal; read which jobs' code names the
  column; then the upstream traversal and the one from `products.csv`.
- **Why the action:** the reader commits to an impact list, as the developer needs, and sees the
  traversal and the code disagree on how far it reaches.
- **Evidence:** 6 nodes downstream; only `build_clean_orders` names `customer_id`; 6 upstream from the
  dashboard; none downstream of `products.csv`.
- **Consequence:** a reader who listed every asset downstream learns it is an upper bound; one who
  listed only `clean_orders` learns the jobs after it still read what it writes.
- **Predictable:** in part, from the code and the map.
- **Gives nothing away:** the prose above names the question, not the nodes or the columns.
- **Not knowing:** right for `products.csv`'s readers outside the repository, and the prose says so.
- **Next question:** what if a line is wrong?
- **An experiment:** commit, run, compare.

### `belief`

- **Role:** experiment
- **Objective:** the reader discovers that a line written by hand records a belief, which the code
  can refute, and that the code answers the question the belief was about.
- **Known before:** the code; Jo's Chapter 5 question; the `drops` line.
- **Driving question:** does `build_daily_sales` read `clean_customers`, and which job leaves out
  orders with no customer id?
- **The action:** see the belief's effect on a traversal; write both answers from the code; read
  the comparison.
- **Why the action:** the effect first (the dashboard seems to depend on `customers.jsonl`), then
  the evidence from an independent source, the code.
- **Evidence:** one row, Jo's line; `WHERE customer_id IS NOT NULL` in `build_clean_orders`.
- **Consequence:** the reader can tell Jo where the orders are lost.
- **Predictable:** yes, from the code.
- **Gives nothing away:** the page states Jo's belief and its effect, not whether it holds.
- **Not knowing:** not the right answer: the code settles it.
- **Next question:** what happens to a line written from the code when the code changes?
- **An experiment:** commit, run, compare.

### `stale`

- **Role:** experiment
- **Objective:** the reader discovers that lines written from code go stale when the code changes,
  and that the rows of the table made do not show it.
- **Known before:** the lines, the code, the comparison.
- **Driving question:** will the comparison report anything after the change, and will the rows of
  `daily_sales` change?
- **The action:** write both expectations, then run the changed week, the comparison and the rows'
  comparison.
- **Why the action:** the two outcomes differ (the comparison reports, the rows do not).
- **Evidence:** 2 rows from the comparison; `True` for the rows; storage gains the copy.
- **Consequence:** the code shows the change, and only as it is now, which motivates Chapter 7.
- **Predictable:** yes; the prose says the copy holds the same rows, which the reader needs to
  reason.
- **Gives nothing away:** it does not say what the comparison reports.
- **Not knowing:** right for "which nights read which source", which the chapter leaves to Chapter 7.
- **Next question:** what did the job read each night?
- **An experiment:** commit, run, compare.

## Requirements

The chapter questions "Record the lineage of `daily_sales`.", the plan's candidate.

1. **What it says:** record the lineage of `daily_sales`.
2. **What it might mean:** what someone says its job reads; what its job's code reads now (and,
   followed back, which tables and files it is made from); what it read each night; which columns
   each of its columns is made from.
3. **What each needs:** a person's line; the repository; a record made each time the job does its
   work; the input columns of each output column.
4. **What the records hold:** lines written from today's code.
5. **Whether it is met:** as written, yes; under the code reading, today; under the other two, no.

The head sets the requirement after the stale lines.

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
| HB | | |

Brief HB, after the review: every fact present and right. The three `#` notes came back with their
`#`, which the cell already has, and lost it in placing. The agent tried one message, which the
permissions refused; nothing was sent.

## The review

A reviewer on another model read the chapter as a learner (`review/findings.md`, 16 findings) and an
independent sceptic attacked each finding (`review/verdicts.md`). Acted on: the rename answered, the
traversal an upper bound and the code the narrower answer (1); the parts list above the prediction
cut, and the prediction moved to a question the drawing does not answer (2); Chapter 5's records and
model in full (3); the two lines for `build_daily_sales` written in, so no output contradicts the
prose before an edit (4); the arrows' direction said (5); Jo's belief grounded in Jo's Chapter 5
question, with a prediction from the code (7); the analyst's copy as Chapter 2's change, not a
script that exists (8); the rows of `daily_sales`, not "the data" (9); the rule for names after
`FROM` (10); "the code shows only now" said once (11); the tab title (12); "traversal" and "the
comparison" (13); the requirement's situation and its readings (14); why the repository now (15);
the fourth objective (16). Rejected by the sceptic: 6 (the definition of lineage is the general idea
that Chapters 7 and 10 need).

The reader no longer writes the two lines for `build_daily_sales`: the dots made every output below
them contradict the prose until the reader filled them in, and the transcription taught nothing the
code above does not show.

## Measured

12 October 2026, local build: Run all 8.0 to 9.3 s; peak memory 398 to 418 MB; 0.32 MB from Chapter
5's link.

## Known gaps

- The published page's run time is to be measured after the deploy.
- `reads_and_writes` is a small rule over the shop's own notation; Chapter 10 parses SQL properly.
