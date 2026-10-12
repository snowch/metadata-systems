# Brief CB: Chapter 3's two kinds of record, the column that names a person, the requirement, the record nobody updates, and the close

Chapter 3, "What is metadata?", is a Jupyter notebook for a data engineer. The reader is "you". Above
these sections, you wrote a record of `daily_sales` (lines of text, one fact per line, with the
fields `means`, `responsible` and `unit`) from what the head of the shop and Jo Marsh in finance told
you, and found that it answers "Who should I ask about `daily_sales`?" (Jo Marsh) and shows Thursday
wrong against Jo's meaning, but not since when, and not what reads `products.csv` or
`orders.jsonl`. Write each slot below, following `docs/style.md` and `AGENTS.md` (attached): British
English, short plain sentences, no em dashes, no filler, no reassurance, nothing that personifies a
system or a record. Keep every name in backticks exactly as written. A block of code is a "cell".
The buttons are **Run all**, **Run below** and **Save**, in bold, and no other control is named.

Words you must not use anywhere: entity, attribute, identifier, dataset, graph, node, edge, lineage,
upstream, downstream, event, observation, freshness, identity, environment, assertion, namespace,
the noun "run" ("run the cell" is fine; say "night" or "write" for what the jobs do), "lab",
"engine", "simulator", "Jupyter", "Pyodide". Never refer to Jo Marsh or Sam Lund with "he" or "she":
repeat the name. Do not use "record" for one line of a file: say "line".

This section introduces three terms, each where its slot says: **descriptive**, **operational** and
**schema**. Give the plain idea first, then the term.

Write the file once. Do not change it after you reply.

## Facts (each checked against the shop's data)

Two kinds of record:

- Your record says what `daily_sales` is: what it means, who is responsible for it, what its columns
  mean and their unit.
- The warehouse records, about each table: its columns and their types, its owner (an account),
  its created time; and its row count, its size and its last-altered time. The row count, the size
  and the last-altered time change with every write of the table: they, and the created time,
  record what happened to the table. The columns, their types and the owner say what the table is.
- Object storage records a file's key, which says what and where the file is, and its size and
  last-modified time, which record the file's last write.
- The reporting tool records the dashboard's title, which says what it is; who created it and when,
  and when it last refreshed, which record what happened to it.
- A record of what an asset is is called **descriptive**. A record of what happened to an asset is
  called **operational**. Your record of `daily_sales` is descriptive.
- The list of a table's columns with their types is called the table's **schema**.
- The cell after this paragraph lists the schema of the warehouse's three tables: 14 columns in all
  (5 in `clean_customers`, 7 in `clean_orders`, 2 in `daily_sales`).
- `orders.jsonl` declares no schema: each line names its fields, and a reader works out their types.
  `products.csv`'s first line names its columns and gives no types.

The column that names a person:

- The head of the shop said Sam Lund keeps the product catalogue.
- `products.csv` has a column, `updated_by`, holding a member of staff's login for each product.
- The cell counts the products each login last edited: `k.adeyemi` 3, `r.novak` 2, `s.lund` 3.
  Three people last edited the 8 products.
- `updated_by` says who last changed each product: a fact about each product, which the shop's
  catalogue keeps and the export copies into the file. It says nothing about who is responsible for
  `products.csv`: the column would hold the same logins whoever that was. It is data about the
  shop's business.
- The file's first line, `product_id,name,category,list_price_pence,updated_by`, names the file's
  columns. That line describes the file, so it is metadata, kept inside the same file as the data.
- So what makes information metadata is what it describes (an asset, or the work done on the
  platform), not where it is kept or who wrote it: the warehouse keeps its tables' schemas inside
  itself, and you keep your record beside the data.

The requirement:

- Suppose the shop sets the requirement: "Every column must have a description."
- First you write, in a cell, whether the line `daily_sales revenue_pence means: the revenue in
  pence` meets it, and why.
- It could be asking for four things, each needing a different line:
  - what the column means: which orders it counts (completed orders, each once, by UTC day);
  - its unit: a `unit` line (pence);
  - where its values come from: which asset and which columns (your record holds nothing of this);
  - whether it may be empty: a line saying so, which a check could test against the rows.
- The line `the revenue in pence` repeats the column's name: `revenue_pence` already said
  "revenue" and "pence".
- The next cell runs the check over all three tables. Your record describes only the columns of
  `daily_sales`, so the check lists the 12 columns of `clean_customers` and `clean_orders`.
- The cell after it meets the requirement the quick way: for each of the 14 columns it writes a
  description made from the column's name (underscores become spaces), and runs the same check.
  The check finds no problems: the requirement is met as written.
- The cell after that shows the two lines it wrote for `daily_sales`: `day means: day` and
  `revenue_pence means: revenue pence`.
- Under the other readings, these descriptions say nothing the names did not: not which orders a
  column counts, where its values come from, or whether it may be empty. A check can count
  descriptions; it cannot tell whether a description says more than the column's name.

The record nobody updates:

- Your record describes `daily_sales` as it is this Monday.
- Two changes the shop could make, each from Saturday's row of `daily_sales` on:
  1. the job that writes `daily_sales` also writes each day's number of completed orders, in a new
     column, `order_count`; the rows before Saturday have no value in it;
  2. the job is edited to keep every order that has not been refunded, as in Chapter 2. The shop
     has no refunds, so from Saturday a cancelled order counts too.
- First you write, in a cell, for each change, whether the check of `daily_sales` will report a
  problem.
- The cells run the week with each change and check your record of `daily_sales` against the
  warehouse each change leaves.
- The check reports the new column, `order_count`, with no description: the warehouse records its
  columns, so a check can compare them with your record. It reports nothing for the edit: no
  column changed.
- The next cell compares the edited week's `daily_sales` with Jo's meaning, the query from above.
  Saturday now differs too: 21549 pence in `daily_sales` against 19149 by Jo's meaning. Thursday
  still differs.
- Your record still says what Jo means by revenue. From Saturday the table counts a cancelled order,
  and nothing on the platform recorded the edit, so nothing prompted a change to the record and the
  check could not see it. A record written by hand stays as written while the platform changes.
  An operational record made when the job changed, saying which version of the job's code wrote
  each row, would have shown the edit. Chapter 7 makes such records.

The close (section "## Before Chapter 4"):

- What the experiments showed: the record answered who to ask about `daily_sales`, and whether
  Thursday is wrong by its stated meaning; a description written from the data could not have; the
  check caught a new column but not a changed meaning.
- What they could not show: since when Thursday is wrong, and what reads `products.csv` or
  `orders.jsonl`.
- Next: your record names Jo Marsh as responsible for `daily_sales`; the reporting tool records
  `j.marsh` as the dashboard's creator. Whether those are one person, and how a record could say
  so, is where Chapter 4 starts: what the records are about, and how one record can point to what
  another describes.

The note "### How this differs from a real platform":

- The shop, its people and its data are invented for the course. All times are UTC.
- Some real databases keep a description with a table or column. In PostgreSQL, the command
  `COMMENT ON` stores one comment for a table or a column (a new one replaces the old), inside the
  database; `psql`'s `\d` commands show it; for most objects only the owner can set it. The shop's
  warehouse keeps no descriptions.
- The record notation is the course's own.

## Slots

A. **kinds**: the section "## What the platform records already": a paragraph that sets your
record beside what the three systems record (facts above), then introduces **descriptive** and
**operational**, and says your record is descriptive.

B. **schema_lead**: introduces **schema**, says what the next cell lists and how many columns, and
says what `orders.jsonl` and `products.csv` declare.

C. **person_lead**: the section "## A column that names a person": Sam Lund, `updated_by`, and one
sentence on what the next cell counts.

D. **person_after**: the cell's result; what `updated_by` is and is not; the first line of the file
as metadata; and what makes information metadata.

E. **requirement_lead**: the section `## "Every column must have a description."`: the requirement,
and what to write in the next cell before reading on.

F. **verdict_cell**: the text inside that cell, between triple quotes: the line
`daily_sales revenue_pence means: the revenue in pence` (plain, no backticks), then a question
asking whether it meets the requirement, followed by `........`. At most about 60 characters a line.

G. **readings**: after the cell: the four readings as a Markdown list, each with what it needs; and
that the line repeats the column's name.

H. **full_check_lead**: one or two sentences before the check over all three tables.

I. **by_name_lead**: one or two sentences before the cell that writes a description from each
column's name.

J. **by_name_after**: its result, then one sentence before the cell that shows the two lines for
`daily_sales`.

K. **by_name_meaning**: after that cell: what the descriptions do not say, and what a check can and
cannot tell.

L. **stale_lead**: the section "## A record nobody updates": the two changes, and what to write in
the next cell before running the cells below it.

M. **stale_cell**: the text inside that cell, between triple quotes: one line per change, short,
each followed by `........`. At most about 60 characters a line.

N. **stale_after**: after the two check cells: what the check reported for each, and why.

O. **stale_meaning_lead**: one sentence before the cell that compares the edited week with Jo's
meaning.

P. **stale_meaning_after**: its result and what it means (facts above), ending with Chapter 7.

Q. **close**: the section "## Before Chapter 4": one short paragraph of what the experiments showed
and could not show; one paragraph on Chapter 4; then two or three reflective questions as a
Markdown list, the first about a platform the reader works on, none with its answer.

R. **reality**: the note "### How this differs from a real platform", from its facts.

Write the slots under `## A` to `## R`, each the exact text to place.
