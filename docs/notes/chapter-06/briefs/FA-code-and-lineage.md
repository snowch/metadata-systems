# Brief FA: Chapter 6, "What is lineage?": the jobs' code, the records of what they read and write, upstream and downstream

Read `docs/notes/chapter-05/briefs/common.md` first: its rules hold here. Chapter 5 gave the reader
**node**, **edge**, **graph** and **traversal** (a walk that starts at a node and follows the edges
of the kinds it is given, each way it is given); you may use them.

This chapter introduces three terms, each where its slot says: **lineage**, **downstream** and
**upstream**. Give the plain idea first, then the term in bold. Do not use any of the three before
its slot, objectives included. Words you must not use anywhere: the noun "run" ("run the cell" is
fine; for a job, say "each night" or "each time it does its work"), event, OpenLineage, facet,
namespace, producer, impact analysis, provenance, root cause, identity, environment, observation,
freshness, column lineage, lab, engine, Jupyter.

## Facts (each checked against the shop's data)

The opening:

- The checkout's developer writes: "Next week we rename `customer_id` in `orders.jsonl` to
  `customer_ref`. What does that affect?" It is Chapter 2's third question.
- The head of the shop gives you access to the repository where the last engineer kept the jobs'
  code. In Chapter 1 you could not see the jobs; now you can read their code. The code says what
  each job does now; it does not say when a job did its work, or what it did on any night.
- Two things that write or read the shop's files are not in the repository: the export, whose code
  belongs to the checkout's supplier, and the analyst's copy of Chapter 2, a script on the
  analyst's laptop.

The code:

- The next cell prints the code of the four jobs, one file each: `jobs/build_clean_customers.py`,
  `jobs/build_clean_orders.py`, `jobs/build_daily_sales.py`, `jobs/refresh_dashboard.py`.
- In each file, `read("...")` reads a file from object storage; a table after `FROM` is read from
  the warehouse; `write("...")` or `refresh("...")` names what the job writes. The SQL is the SQL
  each job runs. `build_daily_sales` appends one row, for the day before.

The records:

- The records cell holds Chapter 5's records, a line for each of the two files no line described
  (so that each is an entity), and, under a `#` note, two lines for each job: what it reads and
  what it writes, with the attributes `reads` and `writes`, taken from the code.
- The two lines for `build_daily_sales` have dots. You fill them in from the job's code, select
  the cell and press **Run below**. Until you do, the cells below show the dots: the check reports
  the two lines, and the walks stop at `clean_orders`.
- The model cell adds a type, `job`, with two attributes: `job reads: dataset` and `job writes:
  dataset or dashboard`. A job, a plain word since Chapter 1, is now an entity: a node between
  the assets it reads and the assets it writes.

The map, and lineage:

- The next cell draws only the `reads` and `writes` edges, with the assets and the jobs: Chapter
  1's platform, drawn with arrows at last, because your lines now record what each job reads and
  writes. An arrow from an asset to a job means the job reads it; an arrow from a job to an asset
  means the job writes it.
- Records of what was made from what, and by which job, are **lineage**.
- The drawing has 3 parts: `orders.jsonl` to `sales_dashboard` through three jobs; `customers.jsonl`
  to `clean_customers` through one job; and `products.csv`, which no job reads.

The developer's question:

- Before you read on, you write which assets a change to `orders.jsonl` affects.
- The next cell walks from `orders.jsonl` to each job that reads it, then to what that job writes,
  and on. What is made from an asset in this way is **downstream** of it.
- Downstream of `orders.jsonl`: 6 nodes: the 3 jobs `build_clean_orders`, `build_daily_sales` and
  `refresh_dashboard`, and the assets `clean_orders`, `daily_sales` and `sales_dashboard`.
- The opposite walk, from an asset to the job that writes it, then to what that job reads, and on,
  gives what the asset is made from: **upstream** of it.
- Upstream of `sales_dashboard`: 6 nodes, back to `orders.jsonl`. `customers.jsonl` and
  `clean_customers` are not upstream of the dashboard.
- Downstream of `products.csv`: nothing. No job in the repository reads it: Chapter 2's second
  question ("Does anything still read it?") has an answer, as far as the lines go.
- The lines record only the jobs in the repository. The export and the analyst's script are not in
  it, and no line records what they read, so "nothing reads `products.csv`" means nothing the
  lines know of.

## Slots

A. **objectives**: four items, each starting with a verb, none using the three new terms: record
what each job reads and writes, from its code; find what a change to one file affects, and what an
asset is made from; test a line written from what a person believes against the code; find what
happens to such lines when a job's code changes.

B. **opening**: the section "## The jobs' code": the developer's message, quoted; the repository;
what code does and does not say; the two things not in it.

C. **code_lead**: one or two sentences before the code cell: what it prints, and how to read a file.

D. **records_lead**: before the records cell: what it holds, the dots to fill and how, and what the
cells below show until you do.

NOTE_CH5. **note_ch5**, NOTE_FILES. **note_files**, NOTE_JOBS. **note_jobs**: the three `#` notes
inside the records cell: Chapter 5's records; the two files; each job's reads and writes, from its
code. Short phrases, under 60 characters, no backticks.

E. **model_lead**: before the model cell: the type and its two attributes; a job as an entity.

F. **lineage**: the section "## Lineage": what the next cell draws, the arrows, then **lineage**,
then the 3 parts.

ALT. **alt**: the drawing's text for a reader who cannot see it: one sentence.

G. **question_lead**: the section "## What a change to orders.jsonl affects" (with `orders.jsonl` in
backticks in the heading): what to write before you read on.

H. **question_cell**: the text inside the expectation cell, between triple quotes: a question
asking which assets a change to orders.jsonl affects, and why, then `........`. At most about 60
characters a line. Plain text.

I. **downstream_after**: what the next cell walked (it is the cell after the expectation), then
**downstream**, then the 6 nodes; then the opposite walk, **upstream**, and one sentence before the
upstream cell.

J. **upstream_after**: the 6 nodes; what is not upstream of the dashboard; one sentence before the
cell for `products.csv`.

K. **products_after**: nothing downstream; Chapter 2's second question; what the lines record and
what "nothing reads" means.

Write the slots under `## A` to `## K` (and `## NOTE_CH5`, `## NOTE_FILES`, `## NOTE_JOBS`,
`## ALT`), each the exact text to place.
