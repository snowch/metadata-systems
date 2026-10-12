## A

## A line from a belief

Jo Marsh says that the daily sales job leaves out test customers, so it reads `clean_customers`. Jo has not read the code. Written as a line, the belief is:

`job build_daily_sales reads: clean_customers`

The next cell adds that line to your records and walks downstream from `customers.jsonl`.

## B

With that line, downstream of `customers.jsonl` reaches 6 nodes, `daily_sales` and `sales_dashboard` among them. A change to `customers.jsonl` now seems to affect the dashboard.

The next cell compares each job's lines with its code. It lists one row for each line the code does not bear out, and one row for each read or write in the code that no line records.

## C

The comparison lists one row: Jo's line. The code of `build_daily_sales` does not read `clean_customers`, and nothing in it leaves out test customers.

A line written by hand records what someone believes. The code is evidence of what the job reads now.

## D

## A line gone stale

Suppose that from Saturday, the daily sales job, `build_daily_sales`, is changed to read the analyst's copy of `clean_orders` instead of `clean_orders`. The copy is Chapter 2's `clean_orders_copy.csv`, in the bucket `shop-scratch`. It holds the same rows.

Your lines were written from the code as it is today.

Before you read on, write in the next cell whether the comparison will report anything after the change, and whether the rows of `daily_sales` will change.

## E

Will the comparison report anything after the change?
........
Will the rows of daily_sales change?
........

## F

The cell runs the week with the change, and compares your lines with the code as it is after the change. It finds 2 rows. Your line says `build_daily_sales` reads `clean_orders`, and its code no longer does. Its code reads `s3://shop-scratch/clean_orders_copy.csv`, and no line says so.

Your lines went stale when the code changed, and nothing changed them.

The next cell compares the rows of `daily_sales` in the changed week with today's.

## G

`True`: the rows of `daily_sales` are the same in the changed week as today. The data shows no change. Only the code does.

The code shows what the job does now. It does not say which nights the job read `clean_orders` and which nights it read the copy. A record made each time the job does its work would say so. Chapter 7 makes such records.

## H

## "Record the lineage of `daily_sales`."

The head of the shop's requirement is "Record the lineage of `daily_sales`." Before you read on, write in the next cell what you would record, and from what.

## I

What would you record?
........
From what?
........

## J

The requirement could mean four things:

- **What someone says the job reads.** Needs someone to write it down. A line like Jo's records a belief.
- **What the job's code reads now.** Needs the repository, which is evidence of today.
- **What the job read on each night.** Needs a record made each time the job does its work. Nothing on the platform makes one (Chapter 7).
- **Which tables, or which columns, `daily_sales` is made from.** Needs the input columns of each output column. For example, `revenue_pence` is made from `price_pence` and `quantity` of `clean_orders`. Lines between tables do not say so (Chapter 10).

Your lines meet the requirement as written, and agree with the code today. None of them says what the job read on each night, or which columns `revenue_pence` comes from.

## K

## Before Chapter 7

The experiments showed three things. Lines of what each job reads and writes let the graph answer what a change to a file affects, and what an asset is made from. A line from a belief made the dashboard seem to depend on `customers.jsonl`, until the code was compared with the line. A line written from today's code went stale when the code changed, and the data did not show it.

The experiments could not show what each job read on each night, or what the export and the analyst's script read.

Chapter 7 records each time a job does its work: when it started and ended, which version of its code it used, what it read and wrote, and whether it succeeded.

- Take a platform you work on. Which of its lineage lines were written by hand, and which came from its code? How would you find out that one of them is stale?
- A job reads its input table's name from a configuration file. Which of your lines could be false while the code still looks the same?
- Which nights did the job read `clean_orders`, and which nights did it read the copy? What would you need in order to find out?

## L

### How this differs from a real platform

The shop, its people, its jobs and its repository are invented for the course.

The shop's jobs are short, and what each reads is found with a small rule: `read("...")`, and a table after `FROM` or `JOIN`. Real code can hide what it reads in functions, variables or SQL built while the job executes. No small rule finds all of it.
