# Brief V: Chapter 16, "Impact analysis"

Read `docs/notes/chapter-14/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
the terms of Chapters 14 and 15 (*data quality*, *assertion*, *provenance*) may be used.

Term this chapter introduces, in bold in slot C and nowhere before it: **impact analysis**. Do not
write: root cause.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Ask the shop's lineage what renaming a column would affect, by dataset and by column.
- Compare its answers with what each reader got after the rename.
- Find what the shop made from a return that was withdrawn.
- Question the requirement "Tell us what breaks if `customer_id` is renamed."

### Slot B: under the heading `## A column to rename`

- The shop's developer wants to rename the column `customer_id` of `clean_orders` to `customer`. The
  change, `customer`, would take effect from Sunday's night: `build_clean_orders` would write the
  column as `customer`, and the warehouse would rename it.
- The head of the shop asks: "Tell us what breaks if `customer_id` is renamed."
- Three readers of `clean_orders` are known from earlier chapters:
  - `build_daily_sales`, which writes `daily_sales`, which the dashboard shows;
  - the analyst's script, `copy_clean_orders`, which copies `clean_orders` every night to
    `clean_orders_copy.csv` in the bucket `shop-scratch` and sends events (Chapters 6 and 9);
  - Jo Marsh's query, which joins `clean_orders` to `clean_customers` on `customer_id` in a
    spreadsheet and sends no events (Chapter 11).
- Before you read on, write in the next cell which of `daily_sales`, the dashboard, the analyst's copy
  and Jo Marsh's query you expect to break, and how.

Write the three readers as a Markdown list.

### Slot BB: the text inside that cell (between triple quotes)

One question, then `........` on its own line: which readers break, and how? At most about 60
characters a line. Plain text.

### Slot BC: before the first cell of the next section, under the heading `## What the lineage lists`

- The next cell follows the graph that the week's events make (Chapter 9) downstream from
  `clean_orders`, in a week with the analyst's script.

### Slot C: after that cell

- Step 1: `copy_clean_orders` writes `clean_orders_copy.csv`, and `build_daily_sales` writes
  `daily_sales`. Step 2: `refresh_dashboard` writes `sales_dashboard`.
- Following lineage from a change to find what it may affect is **impact analysis**. By datasets,
  everything downstream of `clean_orders` may be affected.
- The next cell follows column lineage (Chapter 10) downstream from one column, `customer_id` of
  `clean_orders`.

### Slot D: after that cell

- One column: `customer_id` of `clean_orders_copy.csv`, copied by `copy_clean_orders`.
- `build_daily_sales` does not read `customer_id`. It reads `ordered_at`, `price_pence`, `quantity`
  and `status` (Chapter 10).
- Change `"customer_id"` to `"status"`, select the cell and press **Run below**: the cell lists every
  column downstream of `status`. Then change it back.

### Slot DD: after slot D, as its own paragraph group

- With `"status"`, the cell lists `day` and `revenue_pence` of `daily_sales`, where `status` decides
  which rows count (the filter in `build_daily_sales`), `status` of the copy, and `day` and
  `revenue_pence` of `sales_dashboard`.

### Slot E: under the heading `## After the rename`

- The next cell runs the week twice, without the rename and with it, and sets what each reader got on
  Monday morning side by side.

### Slot F: after that cell

- `daily_sales` and the dashboard: unchanged. 7 rows, 100798 pence, and the same seven values.
- The analyst's copy: its first line now names the column `customer`. The script ran and succeeded.
- Jo Marsh's query: before, 7 rows, one for each country, 41 orders; after, the error
  `no such column: o.customer_id`.
- Compare these with what you wrote.
- By datasets, the lineage listed `daily_sales` and the dashboard, which did not change. By columns,
  it listed the copy's column, which now has another name, with no error. Neither listed Jo Marsh's
  query, which failed: it sends no events, and the shop does not have its code.
- An impact analysis can list only what the lineage it follows holds.

### Slot G: under the heading `## A return withdrawn`

- The next week has the change `withdrawn`. On Sunday 13 at 21:15 the returns desk records `r-206`:
  the brake pads of order 7047 back. Early on Monday 14 at 02:30, `build_daily_sales` writes Sunday's
  row, less what was returned. At 08:50 on Monday the desk withdraws `r-206` and deletes its object,
  and `remove_return` removes its row from `returns`.
- What did the shop make from `r-206`? Before you run the next cell, decide what the graph will list
  downstream of its object.

### Slot H: after the cell that follows the graph from `r-206`'s object

- One step: `record_return` writes `returns`.
- By the events, no program reads `returns`. `build_daily_sales` reads it only through the function
  `returned_quantity`, and its events do not name the table (Chapter 10).
- The next cell checks every run of `build_daily_sales` whose code calls `returned_quantity`
  against what `returns` held when that run started (Chapter 15).

### Slot I: after that cell

- `returns`, the row for `r-206`, written by `run-031`, `record_return`: no longer there.
- `daily_sales`, the row for Sunday 13, written by `run-034`: still there, still 1200 pence less. It
  holds 8575 pence, where Sunday's five orders add up to 9775.
- The dashboard's value for Sunday 13: still there, £85.75.
- Nothing failed. Every run succeeded, and Sunday's figure counts a return the desk withdrew.
- `daily_sales` is appended to: no run writes Sunday's row again.

### Slot J: under the heading `## "Tell us what breaks if customer_id is renamed."`

- Before you read on, write in the next cell what you take "breaks" to mean.

### Slot JJ: the text inside that cell (between triple quotes)

One question, then `........` on its own line: what does "breaks" mean here? At most about 60
characters a line. Plain text.

### Slot READINGS: after that cell

- "Breaks" could mean two things, each needing something different:
  - fails: a program or a query stops with an error. This needs every reader, whether or not it is
    in the shop's records.
  - keeps running and gives a different answer: a reader gets other rows, other values or another
    column name, with no error. This needs the readers of each column, and what each does with it.
- By reading, for the rename:
  - fails: not met. Jo Marsh's query failed, and no record names it.
  - keeps running with a different answer: met for the copy, whose column lineage the shop has. The
    lineage by datasets also listed `daily_sales` and the dashboard, which did not change.
- The withdrawn return gave a different answer in `daily_sales` and on the dashboard, and the
  graph of events did not list either.
- The requirement does not say which meaning of "breaks" it wants.

Write slot READINGS as one lead sentence, a Markdown list of the two readings, a lead line, a
Markdown list of the two verdicts, then two sentences.

### Slot K: under the heading `## Before Chapter 17`

- Lineage by datasets listed everything downstream of `clean_orders`, two readers of which did not
  change. Column lineage listed the copy's column. Neither listed Jo Marsh's query, which failed.
- A withdrawn return left Sunday's row of `daily_sales` and the dashboard 1200 pence low, and the
  graph of events followed it no further than `returns`.
- Neither shows where a wrong figure went wrong.
- Chapter 17 starts from a wrong figure and follows it back to where it went wrong.
- Then three reflective questions, as a Markdown list:
  - which readers of your most-used table are in no record;
  - which of your tables are appended to, so that a change to an input never reaches rows already
    written;
  - what your platform would list if you asked what a deleted record was used for.

### Slot L: under the heading `### How this differs from a real platform`

- The rename, the withdrawn return, the analyst's script and Jo Marsh's query are invented for the
  course.
- The shop's graph holds only what its producers send, and its column lineage only what its parser
  reads in the code the shop has (Chapters 9 and 10).
- OpenLineage's column lineage facet (Chapter 10) is what would carry, in events, the lineage by
  column that the shop follows here.
- In the shop's warehouse, a query that names a column the table does not have fails with an error.

Write slot L as a Markdown list.

## Slots

Write the file `docs/notes/chapter-16/drafts/V.md` with the slots under `## A`, `## B`, `## BB`,
`## BC`, `## C`, `## D`, `## DD`, `## E`, `## F`, `## G`, `## H`, `## I`, `## J`, `## JJ`,
`## READINGS`, `## K` and `## L`, each the exact text to place, and nothing else in the file. Each
slot that has a heading starts with that heading.
