## A

- Read what each run of `build_clean_orders` counted in the file it read.
- Test a rule against every run, and find why it passed on every night.
- Set the rows each run read against the rows it wrote.
- Question the requirement "No order without a customer."

## B

## What each run counted

Chapter 13's observations recorded how many rows each run read and wrote. They did not show what those rows held.

From this chapter, each run of `build_clean_orders` also counts four things as it runs, in the file it read (`orders.jsonl`) and in the table it wrote (`clean_orders`):

- `rows`: the rows.
- `no customer_id`: the rows with no customer id.
- `order_id twice`: the rows beyond the first with the same order id.
- `quantity 0 or less`: the rows with a quantity of 0 or less.

The next cell lists the counts for `orders.jsonl`, run by run. `orders up to` is the last day of orders the night's file holds.

## C

The file grows each night, because each export holds every order so far: 6 rows on Tuesday 8, 48 on Monday 14.

From Thursday 10, `order_id twice` is 1. One order appears twice in the file, and it stays twice.

From Friday 11, `no customer_id` is 3. These are Thursday's three orders with no customer id (Chapter 2). They stay in every later file.

`quantity 0 or less` is 0 on every run.

Whether data is fit for the use made of it is its **data quality**. Counts like these, recorded by each run, are measurements of it.

## D

## A rule tested on every run

The shop's requirement is: "No order without a customer."

The shop's developer writes it as a rule tested on every run of `build_clean_orders`: in `clean_orders`, `no customer_id` must be at most 0.

A rule that a measurement must meet on every run, with whether it held recorded, is an **assertion**.

Before you read on, write in the next cell which runs you expect to fail the assertion, and why.

## DD

Which runs do you expect to fail the assertion, and why?
........

## E

It passed on all 7 runs.

`build_clean_orders` drops every order with no customer id before it writes the table. Its rule is `customer_id IS NOT NULL` (Chapter 2). The assertion tests the table after that rule, so it finds no such order on any night. While the rule stays, this assertion cannot fail.

Change `dataset = "clean_orders"` to `dataset = "orders.jsonl"`. Before you press **Run below**, decide which runs will fail. Then select the cell and press **Run below**.

## F

On `orders.jsonl`, 4 runs fail: Friday 11, Saturday 12, Sunday 13 and Monday 14, each with a count of 3. Tuesday 8 to Thursday 10 pass: their files hold no order of Thursday's.

Each of the four runs counts 3. The count does not show whether they are the same 3 orders.

## G

## Rows read and rows written

A third test sets what each run read against what it wrote.

The next cell lists, for each run, the rows it read and wrote, the rows that repeat an order, and the rows it left out beyond those. The assertion here: `left out` is 0.

## H

Tuesday 8 to Thursday 10 pass. On Thursday 10 the run read 20 rows and wrote 19: 1 row repeated an order, and none was left out.

From Friday 11, every run left 3 rows out. On Friday 11: 27 read, 23 written, 1 repeat, 3 left out.

This test reads both datasets of one run. It shows that the run left rows out. It does not show which rule left them out, or whether it should have.

## I

## "No order without a customer."

Before you read on, write in the next cell what you take the requirement to mean: where must there be no order without a customer, and what should happen to one?

## J

Where must there be no order without a customer,
and what should happen to one?
........

## READINGS

"No order without a customer" could mean three things, each needing a different measurement:

- In the file the checkout sends: `no customer_id` in `orders.jsonl`, on every run.
- In `clean_orders`: `no customer_id` in the table, on every run.
- On the dashboard: every completed order the shop took is counted in a day's revenue, against its customer. This needs the file's orders set against the dashboard's totals.

The next cell tests each reading.

## K

- In the file: not met; 4 runs failed.
- In `clean_orders`: met on every run, because the rule removes the orders before the table is written.
- On the dashboard: not met. Thursday's total leaves out 3 completed orders, worth 15400 pence (Chapter 2).

Compare these with what you wrote. The requirement does not say which reading it means. Nor does it say what should happen to an order without a customer: dropped, kept without a customer, or the night's work stopped.

## L

## The counts in the shop's events

OpenLineage defines two facets for this. `dataQualityMetrics` holds counts for a dataset and for each of its columns. `dataQualityAssertions` holds each assertion and whether it succeeded.

The next cell prints the input `orders.jsonl` of `run-014`, the run on Friday 11, as the shop's producer would send it with both facets.

## M

`rowCount` is 27. For the column `customer_id`, `nullCount` is 3: rows where it is empty. For `order_id`, `distinctCount` is 26.

The assertion is `not_null` on `customer_id`, with `success` false, `expected` 0 and `actual` 3.

Both facets go with the dataset the run read.

## N

## Before Chapter 15

Each run of `build_clean_orders` counted four things in the file it read and the table it wrote. The assertion on `clean_orders` passed on every run, because the rule had removed the orders it was meant to find. On the file, it failed from Friday 11. Comparing the rows each run read with the rows it wrote showed 3 rows left out on every run from Friday 11.

The counts could not show which orders were left out, or where a total on the dashboard came from.

Chapter 15 follows one total on the dashboard back to the rows it was made from.

- Where do your platform's checks run: on what a program reads, or on what it writes?
- Which of your checks could not fail, because a program removes the rows first?
- What does your platform do when a check fails: stop the work, or warn?

## O

### How this differs from a real platform

- The shop's counts, its developer's assertion and its runs are invented for the course.
- OpenLineage's `dataQualityMetrics` facet holds a row count, a size, and for each column counts such as how many values are empty and how many are distinct. Its `dataQualityAssertions` facet holds each assertion's kind, whether it succeeded and, optionally, its column, its severity and the expected and actual values.
- An assertion's severity in that facet shows whether a failure stops the work (`error`) or only warns (`warn`). The shop's assertion stops nothing: the runs that failed it still wrote their tables.
- The shop counts only what `build_clean_orders` reads and writes. A real platform counts what someone has set up a check for.
