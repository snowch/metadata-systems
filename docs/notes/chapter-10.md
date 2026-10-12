# Chapter 10: Column-level lineage

A working note. Written on 12 October 2026 with Chapters 11, 12 and 13, as a notebook
(`notebook/chapter_10.py`). It opens Part III.

## What the chapter does

Chapter 9's graph joins datasets, not columns. Jo Marsh asks which fields of `orders.jsonl` matter
to the dashboard's revenue, and the head of the shop sets the requirement "Show which columns
`revenue_pence` depends on." The reader:

- writes which columns of `orders.jsonl` they expect `revenue_pence` to depend on, and meets
  **column lineage**;
- reads `build_daily_sales`'s code and the two readings of "depends on" (the columns its value is
  computed from; also the columns that decide which rows count), then the shop's parser's answer:
  `column 1` and `column 2`, because the SELECT names no column of `daily_sales`; deletes a `# `,
  presses **Run below**, and sees the catalogue name them;
- follows `revenue_pence` back to `orders.jsonl`: 11 columns, 2 its value is computed from, all 7
  deciding which rows count, and each of the week's three oddities (Wednesday's duplicate,
  Thursday's orders with no customer id, the cancelled orders) arriving through the second kind;
  the requirement's verdict per reading, the first leaving out `customer_id`;
- gives the analyst's `SELECT *` to the parser without and with the catalogue, and follows the
  revenue through the copy (Chapter 6's `source` change): 15 columns;
- writes whether the parser's answer will include `returns` once a function that reads it enters
  the query (the `net` change), and finds it does not: 13 columns, none in `returns`, and the run's
  events name only `clean_orders`;
- reads the `columnLineage` facet the shop's producer would send.

## What was built for it

- `notebook/shop/columns.py`: the shop's own parser for the course's SQL inside a program's code
  (one source per SELECT, `WITH`, `DISTINCT`, `WHERE`, `GROUP BY`; `ORDER BY` records nothing), two
  kinds of dependency (`value`: copied, computed, aggregated; `rows`: filter, grouping, distinct),
  `lineage`, `upstream` through every program whose code the shop has, `facet` and `show`.
- The `net` change (`notebook/shop/week.py`): `returned_quantity(order_id, product_id)`, a function
  registered in the warehouse that reads `returns`; `daily_sales`'s rows do not change.
- The analyst's copy runs `SELECT * FROM clean_orders`; `ANALYST_COPY` is its code as the analyst
  sends it.
- The facet was validated against the published `ColumnLineageDatasetFacet` 1-2-0 with `jsonschema`
  4.26, outside the repository: nine facets (three weeks, three tables), no error; a facet with an
  input's `field` removed failed.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the assets the chapter's programs read and write, the returns table among them.
- **Why now:** every chapter opens with the map; the `net` change reads `returns`.

### `which-columns`

- **Role:** experiment (with `back-to-the-raw-orders`, which answers it)
- **Objective:** the reader discovers that "depends on" has two readings, and that the column behind
  Thursday's low revenue, `customer_id`, is in the second only.
- **Known before:** Chapter 2's Thursday; Chapter 6's code; Chapter 9's graph between datasets.
- **Driving question:** which columns of `orders.jsonl` does `revenue_pence` depend on?
- **The action:** write the columns and why; read the readings; read the parser's answer.
- **Why the action:** a reader who writes `price_pence` and `quantity` commits to the first reading
  without knowing it.
- **Evidence:** 2 columns its value is computed from; all 7 deciding which rows count, with where.
- **Consequence:** the reader sees that the week's three oddities all entered through columns that
  decide which rows count, and that the requirement as written does not say which reading it
  means.
- **Predictable:** in part: the value's columns from the SELECT, the rest from Chapter 2's rules.
- **Gives nothing away:** the readings are given before the answer, not which one the shop needs.
- **Not knowing:** a fair answer to how far back "depends on" goes.
- **Next question:** what does the SQL not name?
- **An experiment:** commit, run, compare.

### `the-catalogue`

- **Role:** experiment
- **Objective:** the reader learns that column lineage from SQL needs the schema of what a program
  writes, because an INSERT matches columns by position.
- **Known before:** the code printed above; the catalogue (Chapter 3).
- **Driving question:** which columns of `daily_sales` does the SELECT make?
- **The action:** delete a `# `, press **Run below**, read the names.
- **Why the action:** the reader gives the parser the one thing it lacked.
- **Evidence:** `column 1` and `column 2`, then `day` and `revenue_pence`.
- **Consequence:** the parser's answer depends on what it is given beside the SQL.
- **Predictable:** yes, once the prose names the position rule.
- **Gives nothing away:** the prose says what to delete and to read the names, not what they are.
- **Not knowing:** not the right answer.
- **Next question:** how far back does the dependency go?
- **An experiment:** change, run again, compare.

### `back-to-the-raw-orders`

- **Role:** inspect
- **Serves:** the answer to the requirement, per reading, back to the export's file.
- **Why now:** it completes `which-columns`.

### `select-star`

- **Role:** inspect
- **Serves:** the question above it, which columns of `clean_orders` the parser can say the copy
  holds from the code alone; what `*` leaves out of the SQL, and that the catalogue fills it with Monday's
  columns.
- **Why now:** Chapter 6's `source` change runs the revenue through the analyst's copy.

### `a-function`

- **Role:** experiment
- **Objective:** the reader learns that a parser of SQL cannot see into a function, so a table the
  function reads is in no record made from the query, nor in the run's events.
- **Known before:** the function and what it reads, stated above the cell; the parser follows names
  it can read.
- **Driving question:** will the parser's answer for `revenue_pence` include `returns`?
- **The action:** write the expectation; read the 13 columns.
- **Why the action:** a reader who expects a lineage tool to find every read commits to that.
- **Evidence:** 13 columns, none in `returns`; the function's arguments listed as columns the value
  is computed from.
- **Consequence:** what a system records depends on where it reads from; a function's reads need
  their own record.
- **Predictable:** yes, from "the shop's parser reads the SQL".
- **Gives nothing away:** the prose says what the function reads, not what the parser finds.
- **Not knowing:** a fair answer before the parser's rule for functions is known.
- **Next question:** how does a real event carry column lineage?
- **An experiment:** commit, run, compare.

### `the-facet`

- **Role:** reference
- **Serves:** the question of what a program that receives the events can know without the code; OpenLineage's form for both kinds, against the shop's own names.
- **Why now:** the requirement's verdict rests on keeping both kinds, and the facet does.

## Requirements

The chapter questions "Show which columns `revenue_pence` depends on.", the plan's candidate, with
the reader's list, the parser's answer and its verdict.

1. **What it says:** show the columns `revenue_pence` depends on.
2. **What it might mean:** the columns its value is computed from; also the columns that decide
   which rows count; either for one program or back through every program.
3. **What each needs:** the SELECT's expressions; also WHERE, GROUP BY and DISTINCT; the code of
   every program upstream.
4. **What the shop records:** both kinds, per column, with where each arises, through every program
   whose code it has; the export is not among them.
5. **Whether it is met:** either reading can be answered; the requirement does not say which, and
   the first leaves out `customer_id`, the column behind Thursday.

## Originality

The obvious examples are the OpenLineage documentation's column lineage example (a table of
delivery times with a date difference and a sort), dbt's column-level lineage in its documentation,
and textbook "customer revenue" queries with a join. This chapter uses the shop's own nightly SQL,
traced back through two programs to a file the shop does not write; its surprise is that every one
of the shop's week of oddities arrives through a column that decides which rows count; its failure
cases are the shop's own `SELECT *` (the analyst's script) and a function the shop's developer
registered to read the returns desk's table. The parser, its two kinds and their names are the
course's own; OpenLineage's facet is named and its form produced by the shop's code, not copied.

## What the prose process caught

Brief PA (with `chapter-10/briefs/common.md`, shared by Part III), draft under `drafts/`. Every fact
was right. Three edits: "The shop's requirement, as written" lost who set it, and became the head of
the shop's; the closing's labels ("Showed:", "Could not show:", "Next:") went, as labels where
statements belong; the code cell's line is `# catalogue = warehouse`, as the draft said, where the
first skeleton had another name. The drafting agent made one stray tool call (a list of
environments), which changed nothing.

## The review

A reviewer on another model read the chapter as a learner (`review/findings.md`, 12 findings and a
group of smaller ones) and an independent sceptic attacked each (`review/verdicts.md`). Acted on:
the reader can now see that a row's value depends on `returns`, by asking the SQL function about
two returned orders (1); the `source` answer is said to be for the code as it stands, with the
earlier rows written by code that read `clean_orders` (2); "the catalogue" is defined where it is
first used, as the warehouse's `information_schema` (3); "made from" is the general relation and
`computed` only the parser's value, "SQL function" is distinct from the returns desk's functions,
and the parser is introduced (4); column lineage's definition covers both kinds (5); "oddities" gave
way to the three named cases (6); the result of the catalogue edit is no longer told before the
reader runs it (7); `SELECT *` has a question in front of it, and its limit is said not to show in
this week (9); the facet section starts from the problem, `transformations` is optional, and the
facet answers for one program (10); the warnings were measured (11); `build_clean_orders`'s code is
printed before the trace (12); personification and an overbroad claim about where a function's
reads can be recorded were scoped to the shop. Rejected: that Chapter 9's last page answers the
first prediction, which is the requirement exercise's design (8); a figure of the column graph;
letting the reader give the parser their own SQL. Brief PB drafted the new paragraphs; every fact
was right, and "the shop's requirement reads" became the head of the shop's.

## Measured

See `docs/notes/notebook-prototype.md`, "Chapters 10 to 13".

12 October 2026, the published page after the review (opened alone, desktop and phone): Run all 10.8 and 11.4 s on a desktop, 9.8 s as a phone; peak memory 412 and 415 MB, and
408 MB. One desktop run logged a 503 from the host for one file while the page loaded, and ran
with no error output; it is kept.

## Known gaps

- The parser reads one source per SELECT: no joins, no subqueries in FROM, no CASE. Part VI's query
  layer needs more.
- `ORDER BY` is not recorded; OpenLineage records it as `SORT`.
