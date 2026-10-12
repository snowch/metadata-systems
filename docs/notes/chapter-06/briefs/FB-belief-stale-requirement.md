# Brief FB: Chapter 6, "What is lineage?": a line from a belief, a line gone stale, the requirement and the close

Read `docs/notes/chapter-05/briefs/common.md` first: its rules hold here. Above these sections the
chapter has introduced **lineage** (records of what was made from what, and by which job),
**downstream** (what is made from an asset, through jobs) and **upstream** (what an asset is made
from); the reader has filled in the two lines for `build_daily_sales` from its code
(`job build_daily_sales reads: clean_orders`, `job build_daily_sales writes: daily_sales`). You may
use all three terms and Chapter 5's (node, edge, graph, traversal). Words you must not use
anywhere: the noun "run" ("run the cell" is fine; for a job, say "each night" or "each time it does
its work"), event, OpenLineage, facet, namespace, producer, impact analysis, provenance, root cause,
identity, environment, observation, freshness, column lineage, lab, engine, Jupyter.

## Facts (each checked against the shop's data)

A line from a belief:

- Jo Marsh says that the daily sales job leaves out test customers, so it reads `clean_customers`.
  Jo has not read the code. Written as a line, the belief is
  `job build_daily_sales reads: clean_customers`.
- The next cell adds that line to your records and walks downstream from `customers.jsonl`.
- With it, downstream of `customers.jsonl` reaches 6 nodes, `daily_sales` and `sales_dashboard`
  among them: a change to `customers.jsonl` now seems to affect the dashboard.
- The next cell compares each job's lines with its code: a line the code does not bear out, and a
  read or write in the code that no line records, one row each.
- It finds one row: Jo's line. The code of `build_daily_sales` does not read `clean_customers`, and
  nothing in it leaves out test customers.
- A line written by hand records what someone believes. The code is evidence of what the job reads
  now.

A line gone stale:

- Suppose that from Saturday the daily sales job is changed to read the analyst's copy of
  `clean_orders` (Chapter 2's `clean_orders_copy.csv`, in the bucket `shop-scratch`) instead of
  `clean_orders`. The analyst's copy holds the same rows.
- Your lines were written from the code as it is today.
- Before you read on, you write whether the comparison will report anything after the change, and
  whether the rows of `daily_sales` will change.
- The next cell runs the week with the change and compares your lines with the code as it is after
  it. It finds 2 rows: your line says `build_daily_sales` reads `clean_orders`, and its code no
  longer does; its code reads `s3://shop-scratch/clean_orders_copy.csv`, and no line says so.
- Your lines went stale when the code changed, and nothing changed them.
- The cell after it compares the rows of `daily_sales` in the changed week with today's: `True`,
  the same rows. The data shows no change; only the code does.
- The code shows only what the job does now. It does not say which nights the job read
  `clean_orders` and which the copy. A record made each time the job does its work would say;
  Chapter 7 makes such records.

The requirement:

- The head of the shop's requirement: "Record the lineage of `daily_sales`."
- You commit first: write in a cell what you would record, and from what.
- It could mean four things:
  - what someone says its job reads: a line like Jo's, a belief;
  - what its job's code reads now: the repository, evidence of today;
  - what its job read each night: a record made each time the job does its work, which nothing on
    the platform makes (Chapter 7);
  - which tables it is made from, or which columns: `revenue_pence` is made from `price_pence` and
    `quantity` of `clean_orders`, and lines between tables do not say so (Chapter 10).
- Your lines meet the requirement as written, and agree with the code today. None of them says what
  the job read on each night, or which columns `revenue_pence` comes from.

The close:

- Showed: lines of what each job reads and writes make the graph answer what a change to a file
  affects and what an asset is made from; a line from a belief made the dashboard seem to depend on
  `customers.jsonl` until the code was compared; a line written from today's code went stale when
  the code changed, and the data did not show it.
- Could not show: what each job read on each night; what the export and the analyst's script read.
- Next: Chapter 7 records each time a job does its work: when it started and ended, which version
  of its code it used, what it read and wrote, and whether it succeeded. (Do not use "run" as a
  noun.)

The note "### How this differs from a real platform":

- The shop, its people, its jobs and its repository are invented for the course.
- The shop's jobs are short, and what each reads is found with a small rule: `read("...")`, and a
  table after `FROM` or `JOIN`. Real code can hide what it reads in functions, variables or SQL
  built at run time, and no small rule finds it all.

## Slots

A. **belief_lead**: the section "## A line from a belief": Jo's belief and its line, and what the
next cell does.

B. **belief_after**: what the walk reached and what that seems to mean; one sentence before the
comparison cell, saying what it lists.

C. **belief_compared**: the comparison's one row, and what the code shows; a line by hand against
the code.

D. **stale_lead**: the section "## A line gone stale": the change, and what to write before you
read on.

E. **stale_cell**: the text inside the expectation cell, between triple quotes: two questions (will
the comparison report anything; will the rows of daily_sales change), each followed by `........`.
At most about 60 characters a line. Plain text.

F. **stale_after**: what the cell did and its 2 rows; that the lines went stale; one sentence before
the next cell, which compares the rows of `daily_sales`.

G. **stale_rows**: `True`; what the data shows and what the code shows; what the code does not say;
Chapter 7.

H. **requirement_lead**: the section `## "Record the lineage of daily_sales."` (with `daily_sales` in
backticks in the heading): the requirement, and what to write in the next cell first.

I. **requirement_cell**: the text inside that cell: what you would record, then `........`; from
what, then `........`. At most about 60 characters a line.

J. **readings**: the four readings as a Markdown list, each with what it needs; then which your lines
meet.

K. **close**: the section "## Before Chapter 7": what the experiments showed and could not show; one
paragraph on Chapter 7; then two or three reflective questions as a Markdown list, the first about a
platform the reader works on, none with its answer.

L. **reality**: the note "### How this differs from a real platform".

Write the slots under `## A` to `## L`, each the exact text to place.
