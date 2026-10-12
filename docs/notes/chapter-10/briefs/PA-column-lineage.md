# Brief PA: Chapter 10, "Column-level lineage"

Read `docs/notes/chapter-10/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms. This chapter introduces **column lineage** in slot B, in bold once, and nowhere before it
(not in slot A). Words you must not use anywhere in this chapter: identity, environment,
observation, freshness, schema evolution, breaking change, IDENTITY.

The shop's parser records two kinds of input for each column a program writes. In the parser's
output they are `value` and `rows`. In prose say "a column its value is computed from" and "a
column that decides which rows count"; you may then use `value` and `rows`, in backticks, as the
names the output gives them.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Find which columns of the raw orders the dashboard's revenue depends on, by reading the programs'
  SQL.
- Find what the SQL alone does not name.
- See what a function in a query hides.
- Question the requirement "Show which columns `revenue_pence` depends on."

### Slot B: under the heading `## Which columns`

- Chapter 9's graph joins datasets: `build_daily_sales` reads `clean_orders` and writes
  `daily_sales`. It does not say which columns of `clean_orders` make which column of
  `daily_sales`.
- Jo Marsh is checking the checkout's data and asks which fields of `orders.jsonl` matter to the
  revenue the dashboard shows.
- The head of the shop's requirement: "Show which columns `revenue_pence` depends on."
- Lineage between columns, which columns each column is made from, is **column lineage**.
- Before you read on, write in the next cell which columns of `orders.jsonl` you expect
  `revenue_pence` to depend on, and why.

### Slot C: the text inside that cell (between triple quotes)

One question, then `........` on its own line: which columns of `orders.jsonl` does `revenue_pence`
depend on, and why? At most about 60 characters a line. Plain text.

### Slot D: under the heading `## The program's SQL`

- The next cell prints the code of `build_daily_sales`, from the shop's repository (Chapter 6).

### Slot E: after that cell

- "Depends on" could mean two things, each needing something different:
  - the columns its value is computed from: these are in the expressions the SELECT lists;
  - also the columns that decide which rows count: these are in the WHERE and GROUP BY clauses,
    and in DISTINCT.
- Either reading can stop at the program that writes `daily_sales`, or go back through every
  program to `orders.jsonl`.
- The next cell gives the code to the shop's parser. For each column the program writes, it lists
  each column it reads, with `kind` and `how`.

Write slot E as one Markdown list of the two readings, then two short paragraphs.

### Slot F: after the parser's cell

- The parser lists `column 1` and `column 2`. The SELECT names no column of `daily_sales`.
- The warehouse puts the SELECT's first value in the table's first column, the second in the
  second. To name them, the parser needs the columns of `daily_sales`, from the catalogue.
- In the cell above, delete the `# ` at the start of the line `# catalogue = warehouse`, select the
  cell and press **Run below**.
- Then the parser names them `day` and `revenue_pence`.
- `kind` is `value` for a column the value is computed from, and `rows` for a column that decides
  which rows count. `how` says the way: for `value`, `copied`, `computed` or `aggregated` (by SUM,
  COUNT and the like, over many rows); for `rows`, `filter` (WHERE), `grouping` (GROUP BY) or
  `distinct`. These names are the shop's own.
- `revenue_pence`: `price_pence` and `quantity`, `value`, `aggregated`; `status`, `rows`, `filter`;
  `ordered_at`, `rows`, `filter` and `grouping`.

### Slot G: under the heading `## Back to the raw orders`

- The next cell follows `revenue_pence` back through every program whose code the shop has, to
  `orders.jsonl`. The export that writes `orders.jsonl` is not in the repository, so the parser
  stops there.
- For each column it finds: `value` says whether `revenue_pence` is computed from it, through every
  step; `rows` says where it decides which rows count.

### Slot H: after that cell

- 11 columns: 4 of `clean_orders` and 7 of `orders.jsonl`.
- `revenue_pence` is computed from 2 columns of `orders.jsonl`: `price_pence` and `quantity`.
- All 7 decide which rows count. `build_clean_orders` keeps one row of each set of equal rows
  (`distinct`), so every column takes part; its filter reads `customer_id` and `quantity`. The filter
  of `build_daily_sales` reads `status` and `ordered_at`.
- Each of the week's three oddities reached the revenue through a column that decides which rows
  count: Wednesday's second copy of order 7015, removed by `distinct`; Thursday's 3 orders with no
  `customer_id`, removed by the filter of `build_clean_orders`; the cancelled orders of Tuesday and
  Saturday, left out by the filter on `status`.
- By reading:
  - the columns its value is computed from: `price_pence` and `quantity`;
  - also the columns that decide which rows count: all 7.
- The shop's parser records both kinds, so it answers either reading. The requirement does not say
  which. The first leaves out `customer_id`, the column behind Thursday's low revenue.

Write slot H as two short paragraphs, one Markdown list of the two readings, then one short
paragraph.

### Slot I: under the heading `## SELECT *` (write the heading as ``## `SELECT *` ``)

- In Chapter 6's `source` change, from Saturday's row on `build_daily_sales` reads the analyst's
  copy, `clean_orders_copy.csv`.
- The analyst's script is not in the repository. The analyst sends its code: it writes the result
  of `SELECT * FROM clean_orders` to the copy.
- The next cell gives that code to the parser without the catalogue; the cell after it, with it.

### Slot J: after those two cells

- Without the catalogue: one row, `clean_orders_copy.csv.*` from `clean_orders.*`. `*` names no
  column, and the parser does not guess one.
- With the catalogue: 7 rows, one for each column of `clean_orders`, each `copied`.
- The next cell follows `revenue_pence` back in the week with the `source` change: 15 columns,
  through the copy (4), then `clean_orders` (4), to `orders.jsonl` (7).

### Slot K: after that cell

- The catalogue gives the columns of `clean_orders` as they are on Monday.
- `SELECT *` copies whatever columns its source has when it runs. A record made from Monday's
  catalogue does not say which columns an earlier run copied, if they were different then.
  Chapter 11 changes a dataset's columns.

### Slot L: under the heading `## A function`

- In the week with the `net` change, the shop's developer edits `build_daily_sales`, from Saturday's
  row on, to take away what was returned.
- The developer added a function to the warehouse, `returned_quantity(order_id, product_id)`. It
  reads the table `returns` and gives how many of one product of an order came back.
- The query also gains a `WITH` clause, which names a SELECT `lines` that the query then reads from.
- No order of Saturday or Sunday was returned, so the rows are the same.
- The next cell prints the edited code.

### Slot M: after that cell

- Before you read on, write in the next cell whether the parser's answer for `revenue_pence` will
  include the table `returns`, and why.

### Slot N: the text inside that cell (between triple quotes)

One question, then `........` on its own line: will the parser's answer for `revenue_pence` include
the table `returns`, and why? At most about 60 characters a line. Plain text.

### Slot O: after the cell that follows `revenue_pence` back in that week

- 13 columns. None is in `returns`.
- The parser followed `lines` back to `clean_orders`. The value of `line_pence` is computed from
  `price_pence`, `quantity`, `order_id` and `product_id`: the last two are the function's arguments.
- The parser cannot read inside the function. It takes the function's value to depend on its
  arguments and nothing else.
- The run's events name `clean_orders` as the only input, too.
- A record that the function reads `returns` has to come from somewhere other than the query: from
  whoever wrote the function, or from the warehouse as the query runs.

### Slot P: under the heading `## In an event`

- OpenLineage defines a facet for column lineage, `columnLineage`, on an output dataset.
- Under `fields`, it lists each output column with the input columns its value comes from. Under
  `dataset`, it lists input columns that affect the whole dataset, such as a filter's.
- Each input carries a transformation `type`: `DIRECT` where the output's value is derived from the
  input, `INDIRECT` where the input affects the output without the value coming from it. A
  `subtype` says how: among them `TRANSFORMATION`, `AGGREGATION`, `FILTER` and `GROUP_BY`.
- The shop writes `value` as `DIRECT` and `rows` as `INDIRECT`.
- The next cell makes the facet the shop's producer would add to `daily_sales` in a run's
  `COMPLETE`, and prints it.

### Slot Q: after that cell

- Under `fields`: `day`, from `ordered_at` (`TRANSFORMATION`); `revenue_pence`, from `price_pence`
  and `quantity` (`AGGREGATION`).
- Under `dataset`: `ordered_at` (`FILTER` and `GROUP_BY`) and `status` (`FILTER`).
- The facet keeps both kinds, so a program that receives it can answer either reading of the
  requirement.

### Slot R: under the heading `## Before Chapter 11`

- Showed: the shop's parser read the programs' SQL and listed, for each column, the columns it is
  computed from and the columns that decide which rows count. `revenue_pence` is computed from 2
  columns of `orders.jsonl`, and all 7 decide which rows count, `customer_id` among them. The SQL did
  not name the columns of `daily_sales` or what `*` stands for; the catalogue did. A function hid
  the table it reads.
- Could not show: what happens to the programs downstream when a dataset's columns change.
- Next: Chapter 11 changes the columns of `orders.jsonl` and follows what each change does.
- Then three reflective questions, as a Markdown list:
  - Which of your platform's queries use `SELECT *`, and what would their column lineage need?
  - Which functions in your warehouse read a table their callers do not name?
  - When someone asks what a column depends on, which of the two readings do they need?

### Slot S: under the heading `### How this differs from a real platform`

- The shop's parser is the course's own, and reads only the course's small SQL: one source per
  SELECT, and no joins.
- OpenLineage's project has its own SQL parser, a library written in Rust that reads several
  dialects, SQLite's among them.
- The facet's documentation lists no subtype for `DISTINCT`. The shop writes it as `INDIRECT` with no
  subtype: that is the shop's choice.
- The shop's warehouse keeps no record of which columns a query read while it ran.

## Slots

Write the file `docs/notes/chapter-10/drafts/PA.md` with the slots under `## A`, `## B`, `## C`,
`## D`, `## E`, `## F`, `## G`, `## H`, `## I`, `## J`, `## K`, `## L`, `## M`, `## N`, `## O`,
`## P`, `## Q`, `## R` and `## S`, each the exact text to place, and nothing else in the file. Each
slot that has a heading starts with that heading.
