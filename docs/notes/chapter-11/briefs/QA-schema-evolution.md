# Brief QA: Chapter 11, "Schema evolution"

Read `docs/notes/chapter-10/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms. The reader knows **column lineage** (Chapter 10) and the two kinds the shop's parser records:
`value` (a column its value is computed from) and `rows` (a column that decides which rows count).
This chapter introduces **schema evolution** in slot D and **breaking change** in slot H, each in
bold once, and neither before its slot (not in slot A, not "breaking" or "breaks" before slot H
either: before it, say "changes what ... holds" or "gives a different answer"). Words you must not
use anywhere in this chapter: identity, environment, observation, freshness, rename detection.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Record a dataset's schema each time it is written, and compare two versions.
- Find which readers each of three changes to a file affects.
- Find what column lineage says about a change, and what it cannot say.
- Question the requirement "Warn us of breaking changes."

### Slot B: under the heading `## The supplier's three changes`

- The checkout's supplier writes `orders.jsonl` each night: the export (Chapter 1). Its code is not
  in the shop's repository.
- The supplier plans one of three changes to the file, from the export before Saturday's row, and
  asks whether the shop can take it:
  - `added`: a new field, `coupon_code`;
  - `renamed`: `quantity` renamed to `qty`;
  - `retyped`: each customer id written as text, `C101` where it was `101`.
- Before you read on, write in the next cell, for each change, whether you expect it to change what
  `daily_sales` holds on Monday, and why.

Write the three changes as a Markdown list.

### Slot C: the text inside that cell (between triple quotes)

The three change names, `added`, `renamed` and `retyped`, each on its own line followed by `....`,
under one line asking whether each changes what `daily_sales` holds, and why. At most about 60
characters a line. Plain text.

### Slot D: under the heading `## The schema over time`

- Neither system keeps a dataset's past schemas. Object storage records nothing about a file's
  fields; the catalogue holds each table's columns as they are now.
- The shop records a schema each time a program writes a dataset: for a file, the fields a reader
  finds and the type of their values; for a table, its columns and declared types from the
  catalogue, just after the write.
- How a dataset's schema changes over time, version after version, is **schema evolution**.
- The next cell runs the week with the `renamed` change and lists the versions of the schema of
  `orders.jsonl`.

### Slot E: after that cell

- 2 versions. Version 1 was written 5 times, from Tuesday 8 to Saturday 12; version 2 twice, on
  Sunday 13 and Monday 14.
- The next cell compares the two versions.

### Slot F: after that cell

- The comparison lists `quantity` as removed and `qty` as added.
- The shop's records match columns by name. A rename looks like a removal and an addition: nothing
  in the records says `qty` is `quantity` under a new name. Only the supplier's notice says so.
- The next cell compares the versions under each of the three changes, and counts the versions of
  the schema of `clean_orders` under each.

### Slot G: after that cell

- `added`: `coupon_code` added, its values `string`. `retyped`: `customer_id` from `integer` to
  `string`.
- Under every change, `clean_orders` has 1 version: its columns and declared types are the same.
- The next cell asks the warehouse for the type of each value in `customer_id` of `clean_orders`,
  in the week with the `retyped` change.

### Slot GG: after that cell

- All 44 values are `text`, in a column the catalogue declares `INTEGER`. The warehouse keeps the
  text; the catalogue's record does not change.

### Slot H: under the heading `## What each reader gets`

- The next cell prints Jo Marsh's own query, which runs in a spreadsheet that reads the warehouse.
  It counts orders by the customer's country. It is not in the shop's repository and sends no
  events.
- The cell after it counts what three readers get on Monday, in the plain week and with each
  change: the rows of `daily_sales`, the days the dashboard shows, and the rows of Jo Marsh's
  query.

### Slot I: after the counts

- `added`: 7, 7 and 7, as in the plain week. `renamed`: 5, 5 and 0. `retyped`: 7, 7 and 0.
- Compare these with what you wrote.
- `renamed`: `build_clean_orders` reads `quantity` by name. The file has no `quantity`, so the value
  is empty, and the filter `quantity > 0` keeps no order. `clean_orders` has no rows after the last
  two nights, though the program succeeded each time. `daily_sales` has no row for Saturday or
  Sunday.
- `retyped`: `daily_sales` is the same. Jo Marsh's query joins `clean_orders` to `clean_customers`
  on `customer_id`; `C101` never equals `101`, so it finds no rows.
- A change to a dataset after which a program or a person that reads it fails or gets a different
  answer is a **breaking change**.
- The new name broke all three readers. The new type broke Jo Marsh's query only. The new field
  broke none.

### Slot J: under the heading `## Who reads the column`

- The next cell uses Chapter 10's column lineage to list the programs whose code the shop has that
  read one column of `orders.jsonl`, and how.

### Slot K: after that cell

- `build_clean_orders` reads `quantity`: its value is copied, and it decides which rows count, by
  the filter and by `distinct`.
- Change `column = "quantity"` to `column = "customer_id"`, select the cell and press
  **Run below**. The same program reads `customer_id`, in the same three ways.
- From column lineage, a change to `customer_id` reaches `build_clean_orders`, and through it
  `daily_sales`. But `daily_sales` did not change. Column lineage says which programs read a column,
  not whether a change breaks them.
- Jo Marsh's query, the one reader the new type broke, is in no record the shop keeps.

### Slot L: under the heading `## "Warn us of breaking changes."`

- The head of the shop's requirement: "Warn us of breaking changes."
- Before you read on, write in the next cell whom you would warn of each of the three changes.

### Slot M: the text inside that cell (between triple quotes)

One question, then `........` on its own line: whom would you warn of each change, and why? At most
about 60 characters a line. Plain text.

### Slot READINGS: after that cell

- "Breaking" could mean breaking for three kinds of reader, each needing something different:
  - a program that reads the dataset: the column lineage of every program whose code the shop has,
    and the comparison of the schema's versions;
  - the dashboard: lineage downstream from those programs to it;
  - somebody's own query: a record of the queries people run, which the shop does not keep.
- By reading:
  - a program that reads it: met for the new name (`build_clean_orders` reads `quantity`). For the
    new type, the warning reaches `build_clean_orders`, which did not break;
  - the dashboard: met, by following lineage from `build_clean_orders` to the dashboard;
  - somebody's own query: not met. Jo Marsh's query is in no record.
- The requirement does not say breaking for whom.

Write slot READINGS as one Markdown list of the three readings, a second Markdown list of the three
verdicts, then one sentence.

### Slot N: under the heading `## Before Chapter 12`

- Showed: the shop recorded a schema each time a dataset was written, and compared versions by
  name, so a rename was a removal and an addition. The new name gave every reader less; the new type
  changed nothing for `daily_sales` and emptied Jo Marsh's query; the new field changed nothing.
  Column lineage named the program that reads each column, not whether the change broke it, and no
  record named Jo Marsh's query.
- Could not show: when two names refer to the same table, or to two different ones.
- Next: Chapter 12 asks when two references name the same asset.
- Then three reflective questions, as a Markdown list:
  - Where does your platform record a dataset's past schemas, if anywhere?
  - Who reads your most-used table without being in any record?
  - Would a change that empties a table without an error be caught on your platform?

### Slot O: under the heading `### How this differs from a real platform`

- The supplier, its changes and Jo Marsh's query are invented for the course.
- Apache Iceberg, a table format, gives each column an id and keeps it when the column is renamed,
  so its schemas can tell a rename from a removal and an addition. The shop's records hold names
  only.
- OpenLineage defines a `schema` facet for a dataset, which lists its fields with a name and a type.
- The shop's warehouse keeps a text value in a column declared `INTEGER`. A warehouse that enforces
  declared types would refuse the value, and the program would fail instead.
- `build_clean_orders` reads the fields it names, and a field the file does not have is empty. A
  reader that refuses a file without a field it names would fail instead.

## Slots

Write the file `docs/notes/chapter-11/drafts/QA.md` with the slots under `## A`, `## B`, `## C`,
`## D`, `## E`, `## F`, `## G`, `## GG`, `## H`, `## I`, `## J`, `## K`, `## L`, `## M`, `## READINGS`,
`## N` and `## O`, each the exact text to place, and nothing else in the file. Each slot that has a
heading starts with that heading.
