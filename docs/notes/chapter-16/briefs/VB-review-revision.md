# Brief VB: Chapter 16, after its review

Read `docs/notes/chapter-14/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
brief VA's terms. A review found: "reader" meaning both a program and what it produced; a cell
described as running the week twice; a slogan; a requirement section that ended on another change;
several names for one lineage. Use "lineage by datasets" for the graph the week's events make, and
"column lineage" for Chapter 10's. "Reader" is a program or a query; what it produced is its output.
These slots replace paragraphs.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Ask the shop's lineage what renaming a column would affect, by dataset and by column.
- Compare its answers with what each reader produced after the rename.
- Find what the shop made from a return that was withdrawn.
- Question the requirement "Tell us what breaks if `customer_id` is renamed."

### Slot BC: under the heading `## What the lineage lists`

- The next cell follows lineage by datasets, the graph that the week's events make (Chapter 9),
  downstream from `clean_orders`, in a week with the analyst's script.

### Slot C: after that cell

- Step 1 is the programs that read `clean_orders`: `copy_clean_orders` writes `clean_orders_copy.csv`,
  and `build_daily_sales` writes `daily_sales`. Step 2 is the programs that read what step 1 wrote:
  `refresh_dashboard` writes `sales_dashboard`.
- Following lineage from a change to find what it may affect is **impact analysis**. By datasets,
  everything downstream of `clean_orders` may be affected.
- The next cell follows column lineage (Chapter 10) downstream from one column, `customer_id` of
  `clean_orders`.

### Slot E: under the heading `## After the rename`

- The next cell runs the week again with the rename, and sets what each reader produced on Monday
  morning beside the week above.

### Slot F: after that cell

- `daily_sales` and the dashboard are unchanged: 7 rows, 100798 pence, and the same seven values.
- The analyst's copy: its first line, the names of its columns, now names the column `customer`. The
  script ran and succeeded.
- Jo Marsh's query: before, 7 rows, one for each country, 41 orders; after, the error
  `no such column: o.customer_id`.
- Compare these with what you wrote.
- By datasets, the lineage listed `daily_sales` and the dashboard, which did not change. Column
  lineage listed the copy's column, which now has another name, with no error. Neither listed Jo
  Marsh's query, which failed: it sends no events, and the shop does not have its code.

Write the first three as a Markdown list, then two short paragraphs.

### Slot H: after the cell that follows lineage by datasets from `r-206`'s object

- Lineage by datasets lists one step: `record_return` writes `returns`.
- According to the events, no program reads `returns`. `build_daily_sales` reads it only through the
  SQL function `returned_quantity`, and its events do not name the table (Chapter 10).
- The next cell checks every run of `build_daily_sales` whose code calls `returned_quantity` against
  what `returns` held when that run started (Chapter 15).

### Slot READINGS: after the cell for the meaning of "breaks"

- "Breaks" could mean two things, each needing something different:
  - fails: a program or a query stops with an error. This needs every reader that names the column,
    whether or not it is in the shop's records.
  - keeps running and gives a different answer: a reader gets other rows, other values or another
    column name, with no error. This needs the readers of the column, and what each does with it.
- By reading, for the rename:
  - fails: not met. Jo Marsh's query failed, and no record names it.
  - keeps running with a different answer: met for the copy, whose column lineage the shop has.
    Lineage by datasets also listed `daily_sales` and the dashboard, which did not change.
- The requirement does not say which meaning of "breaks" it wants.

Write slot READINGS as one lead sentence, a Markdown list of the two readings, a lead line, a
Markdown list of the two verdicts, then one sentence.

### Slot K: under the heading `## Before Chapter 17`

- Lineage by datasets listed everything downstream of `clean_orders`, and two of the datasets it
  listed did not change. Column lineage listed the copy's column. Neither listed Jo Marsh's query,
  which failed.
- A withdrawn return left Sunday's row of `daily_sales` and the dashboard 1200 pence low, and lineage
  by datasets followed it no further than `returns`.
- Chapter 17 starts from a wrong total and follows it back to where it went wrong.
- Then the same three reflective questions as now, as a Markdown list (keep their wording):
  - Which readers of your most-used table are in no record?
  - Which of your tables are appended to, so that a change to an input never reaches rows already
    written?
  - What would your platform list if you asked what a deleted record was used for?

### Slot L: under the heading `### How this differs from a real platform`

- The rename, the withdrawn return, the analyst's script and Jo Marsh's query are invented for the
  course.
- The shop's lineage by datasets holds only what its producers send, and its column lineage only what
  its parser reads in the code the shop has (Chapters 9 and 10).
- OpenLineage's column lineage facet (Chapter 10) is what would carry, in events, the lineage by column
  that the shop follows here.
- That `daily_sales` is appended to, not rebuilt, is the shop's own design.

Write slot L as a Markdown list.

## Slots

Write the file `docs/notes/chapter-16/drafts/VB.md` with the slots under `## A`, `## BC`, `## C`,
`## E`, `## F`, `## H`, `## READINGS`, `## K` and `## L`, each the exact text to place, and nothing
else in the file. Each slot that has a heading starts with that heading.
