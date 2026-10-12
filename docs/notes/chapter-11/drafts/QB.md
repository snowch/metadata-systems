## A

- Read the shop's record of a dataset's schema at each write, and compare two schema versions.
- Find which readers each of three changes to a file affects.
- Find what column lineage says about a change, and what it cannot say.
- Question the head of the shop's requirement about changes to datasets.

## B

## The supplier's three changes

The checkout's supplier writes `orders.jsonl` each night: the export (Chapter 1). Its code is not in the shop's repository.

Chapters 2 and 3 asked: if the checkout renames a column in `orders.jsonl`, what stops working?

The supplier proposes three changes to the file. The page runs the week three times, once with each, as if the change had reached the export that runs early on Sunday 13, before Saturday's row is written:

- `added`: a new field, `coupon_code`;
- `renamed`: `quantity` renamed to `qty`;
- `retyped`: each customer id written in a new format, as text: `C101` where it was `101`.

Before you read on, write in the next cell, for each change, whether you expect it to change what `daily_sales` holds on Monday, and why.

## D

## The schema over time

Object storage keeps each earlier version of `orders.jsonl` (Chapter 7), but records nothing about its fields. The catalogue holds each table's columns as they are now. Neither keeps a record of a dataset's past schemas.

The shop records a schema each time a program writes a dataset: for a file, the fields a reader finds and the type of their values; for a table, its columns and declared types from the catalogue, just after the write. Consecutive writes with the same schema make one schema version.

How a dataset's schema changes over time, schema version after schema version, is **schema evolution**.

The next cell runs the week with the `renamed` change and lists the schema versions of `orders.jsonl`.

## E

The changed export first appears on Sunday 13, and its schema version is the second.

The next cell compares the two schema versions.

## F

The shop's records match columns by name: `quantity` is removed and `qty` added. Nothing in the records says `qty` is `quantity` under a new name. Only the supplier could say so.

The next cell compares the schema versions under each of the three changes, and counts the schema versions of `clean_orders` under each.

## G

Under every change, `clean_orders` has 1 schema version: its columns and declared types stay the same.

Under `retyped`, is `customer_id` in `clean_orders` still a number? The next cell asks the warehouse for the type of each value in that column.

## GG

All 44 values are `text`, in a column the catalogue declares `INTEGER`.

The shop's warehouse turns text that looks like a number into a number when it stores it in a column declared `INTEGER`: `"101"` would be stored as `101`. `C101` is not a number, so the warehouse keeps it as text. That behaviour belongs to the shop's warehouse.

The catalogue's record does not change.

## H

## What each reader gets

The next cell prints Jo Marsh's own query, which runs in a spreadsheet that reads the warehouse. It counts orders by the customer's country. It is not in the shop's repository and sends no events.

The cell after it counts what three readers get on Monday, in the plain week and with each change: the rows of `daily_sales`, the days the dashboard shows, and the rows of Jo Marsh's query.

## I

Compare the counts with what you wrote.

`renamed`: `build_clean_orders` reads `quantity` by name. The file has no `quantity`, so the value is empty, and the filter `quantity > 0` keeps no order. The export writes every order so far each night, so `clean_orders` has no rows after each of the last two nights, though the program succeeded each time. `daily_sales` has no row for Saturday or Sunday, and Jo Marsh's query finds no order.

`retyped`: `daily_sales` is the same. Jo Marsh's query joins `clean_orders` to `clean_customers` on `customer_id`; `C101` never equals `101`, so it finds no rows.

A change to a dataset's structure or format after which a program or a person that reads it fails or gets a different answer is a **breaking change**. The definition is by its effect on a reader.

The new name broke all three readers. The new ids broke Jo Marsh's query only. The new field broke none.

## J

## Who reads the column

The next cell uses Chapter 10's column lineage to list the programs whose code the shop has that read one column of `orders.jsonl`, and how.

## K

`build_clean_orders` reads `quantity`: its value is copied, and it decides which rows count, by the filter and by `distinct`.

Change `column = "quantity"` to `column = "customer_id"`. Before you press **Run below**, decide which programs the cell will list, and whether that means `daily_sales` changes under `retyped`. Then select the cell and press **Run below**.

## KK

The same program reads `customer_id`, in the same three ways.

Chapter 10 showed that `customer_id` reaches `revenue_pence` only as a column that decides which rows count. A warning by lineage would reach `build_clean_orders` and, through it, `daily_sales` and the dashboard. Under `retyped` none of them changed.

Column lineage says which programs read a column, not whether a change breaks them. Jo Marsh's query, the one reader the new ids broke, is not in the shop's code.

## L

## "Warn us of breaking changes."

The head of the shop's requirement: "Warn us of breaking changes."

Before you read on, write in the next cell what the shop would have to record to warn each kind of reader.

## M

What would the shop have to record to warn each kind of reader?
........

## READINGS

"Breaking" could mean breaking for three kinds of reader, each needing something different:

- a program that reads the dataset: the column lineage of every program whose code the shop has, and the comparison of the schema versions;
- the dashboard: lineage downstream from those programs to it;
- somebody's own query: a record of the queries people run, which the shop does not keep.

A reading is met when the shop's records would raise a warning for every reader of that kind that broke.

By reading:

- A program that reads the dataset: met. For `renamed` the warning reaches `build_clean_orders`, which broke. For `retyped` it reaches `build_clean_orders` too, which did not break: a warning with no break behind it.
- The dashboard: met. For `renamed` the warning reaches it, and it broke. For `retyped` it reaches it too, and it did not break.
- Somebody's own query: not met. Jo Marsh's query broke under `renamed` and `retyped`, and no record names it.

The requirement does not say breaking for whom.

## N

## Before Chapter 12

The shop recorded a schema each time a dataset was written and compared schema versions by name, so a rename was a removal and an addition. The new name broke all three readers without an error; the new ids changed nothing for `daily_sales` and emptied Jo Marsh's query; the new field changed nothing. Column lineage named the program that reads each column, not whether a change broke it.

The records compared `quantity` and `qty` as two names, and could not say whether they were one column. The same question for whole tables, two names that may refer to one table, is next.

Chapter 12 asks when two references name the same asset.

- Where does your platform record a dataset's past schemas, if anywhere?
- Who reads your most-used table without being in any record?
- Would a change that empties a table without an error be caught on your platform?

## O

### How this differs from a real platform

- The supplier, its changes and Jo Marsh's query are invented for the course.
- Apache Iceberg, a table format, gives each column an id and keeps it when the column is renamed, so its schemas can tell a rename from a removal and an addition. The shop's records hold names only.
- OpenLineage defines a `schema` facet for a dataset, which lists its fields, each with a name and, optionally, a type.
- A warehouse that enforces declared types would refuse `C101` in an `INTEGER` column, and the program would fail instead.
- `build_clean_orders` reads the fields it names, and a field the file does not have is empty. A reader that refuses a file without a field it names would fail instead.
