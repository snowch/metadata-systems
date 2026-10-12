## A

- Turn each job's code into lines of what it reads and writes.
- Find what a change to one file affects, and what an asset is made from.
- Test a line written from what a person believes against the code.
- Find what happens to lines written from code when the code changes.

## B

## The jobs' code

The checkout's developer writes:

> Next week we rename `customer_id` in `orders.jsonl` to `customer_ref`. What does that affect?

That is the third question from Chapter 2.

To answer it, the head of the shop gives you access to the repository where the last engineer kept the jobs' code. In Chapter 1 you could not see the jobs. Now you can read their code.

Two kinds of work on the shop's files have no code in the repository. The first is the export, whose code belongs to the checkout's supplier. The second is anything someone does by hand, such as the analyst's copy that Chapter 2 tried.

## C

The next cell prints the code of the four jobs, one file each.

In each file, `read("...")` reads a file from object storage and gives it a name.

A name after `FROM` is either a name that `read` gave, which stands for that file, or a table in the warehouse.

`write("...")` or `refresh("...")` names what the job writes.

## D

The records cell holds Chapter 5's records in full.

It adds one line for each of the two files no line described, `orders.jsonl` and `customers.jsonl`, so that each is an entity.

It adds two lines for each job, taken from the job's code: what the job reads and what it writes, with the attributes `reads` and `writes`.

## NOTE1

These are Chapter 5's records.

## NOTE2

The next two lines: files no line described.

## NOTE3

Next: each job's reads and writes, from its code.

## E

The model cell holds Chapter 5's model and adds a type, `job`, with two attributes:

- `job reads: dataset`: the value of `reads` on a job is a dataset;
- `job writes: dataset or dashboard`: the value of `writes` is a dataset or the dashboard.

Until now, a job has been a plain word. Now it is an entity: a node between the assets it reads and the assets it writes.

## F

## Lineage

The next cell draws only the `reads` and `writes` edges, between the assets and the jobs.

This is the platform from Chapter 1, drawn with arrows at last, because your lines now record what each job reads and writes.

In Chapter 5 every arrow pointed from a line's entity to the entity its value names. This drawing points each arrow the way data moves: from an asset to the job that reads it, and from a job to the asset it writes. So an arrow for a `reads` line points from the asset to the job.

The paths that traversals print keep Chapter 5's form: `<-reads-` is a `reads` line followed against its direction.

Records of what was made from what, and by which job, are **lineage**.

## ALT

The drawing shows a chain from orders.jsonl through three jobs to sales_dashboard, a chain from customers.jsonl through one job to clean_customers, and products.csv with no arrow to a job.

## G

## What the rename affects

Before you read on, write in the next cell which assets the rename of `customer_id` in `orders.jsonl` affects, and why.

You can use the code printed above and the drawing.

## H

Which assets does the rename of customer_id
in orders.jsonl affect, and why?
........

## I

The cell above follows edges from `orders.jsonl` to each job that reads it, then to what that job writes, and on. The assets and jobs it reaches this way are **downstream** of `orders.jsonl`.

Downstream of `orders.jsonl` there are 6 nodes: the jobs `build_clean_orders`, `build_daily_sales` and `refresh_dashboard`, and the assets `clean_orders`, `daily_sales` and `sales_dashboard`.

That is the most the rename could affect. The lines are between files, tables and jobs. They do not say which columns a job uses.

For these short jobs, the code does say which columns a job uses. Only the code of `build_clean_orders` names `customer_id`: in its `SELECT` and in its `WHERE`.

`build_daily_sales` and `refresh_dashboard` do not name it. They read what `build_clean_orders` writes, directly or through `daily_sales`.

Tell the developer that the code of `build_clean_orders` must change with the rename, and that the two jobs after it read what it writes.

Chapter 10 records which columns each column is made from.

The opposite traversal goes from an asset to the job that writes it, then to what that job reads, and on. What it reaches is **upstream** of the asset: what the asset is made from, and the jobs that made it.

The next cell follows edges back from `sales_dashboard`.

## J

Upstream of `sales_dashboard` there are 6 nodes. The farthest back is `orders.jsonl`, 6 steps away.

`customers.jsonl` and `clean_customers` are not upstream of the dashboard.

The next cell follows edges downstream from `products.csv`.

## K

Downstream of `products.csv` there is nothing: the cell shows "No rows." No job in the repository reads it.

Chapter 2 asked "Does anything still read it?" As far as the lines go, the answer is no.

The lines record only the jobs in the repository. The export and anything done by hand have no lines. So "nothing reads `products.csv`" means only that the lines know of no reader.

## L

## A line from a belief

In Chapter 5, Jo Marsh wanted to know where orders with no customer id are lost.

Jo believes the daily sales job counts only orders from customers it knows, and so reads `clean_customers`.

Written as a line, the belief is:

`job build_daily_sales reads: clean_customers`

The next cell adds that line to your records and follows edges downstream from `customers.jsonl`.

## M

With Jo's line, downstream of `customers.jsonl` there are 6 nodes, `daily_sales` and `sales_dashboard` among them. A change to `customers.jsonl` now seems to affect the dashboard.

Before you read on, write in the next cell whether the code of `build_daily_sales` reads `clean_customers`, and which job's code leaves out orders with no customer id. The code is printed near the top of the page.

## N

Does the code of build_daily_sales read clean_customers?
........
Which job's code leaves out orders with no customer id?
........

## O

The next cell is the comparison. It compares each job's lines with its code. It lists one row for each line the code does not bear out, and one row for each read or write in the code that no line records.

## P

The comparison lists one row: Jo's line. The code of `build_daily_sales` reads `clean_orders`, and not `clean_customers`.

The code of `build_clean_orders` has `WHERE customer_id IS NOT NULL`. It leaves out orders with no customer id when it writes `clean_orders`, as the `drops` line on `clean_orders` says.

That answers Jo: the orders are lost in `build_clean_orders`, before `build_daily_sales` reads `clean_orders`.

A line written by hand records what someone believes. The code is evidence of what the job reads now.

## Q

## A line gone stale

Suppose the analyst copies `clean_orders` every night to `clean_orders_copy.csv`, in the bucket `shop-scratch`, as in one of Chapter 2's changes.

And suppose that from Saturday, `build_daily_sales` is changed to read the copy instead of `clean_orders`. The copy holds the same rows.

Your lines were written from the code as it is today.

Before you read on, write in the next cell whether the comparison will report anything after the change, and whether the rows of `daily_sales` will change.

## S

The cell above runs the week with the change, and compares your lines with the code as it is after the change. It lists 2 rows.

Your line says `build_daily_sales` reads `clean_orders`, and its code no longer does. Its code reads `s3://shop-scratch/clean_orders_copy.csv`, and no line says so.

Your lines went stale when the code changed, and nothing changed them.

The next cell compares the rows of `daily_sales` in the changed week with today's.

## T

`True`: the rows of `daily_sales` are the same in the changed week as today.

Storage gains the copy, `clean_orders_copy.csv`. Nothing in storage says which job reads it.

The code shows what the job does now. It does not say which nights the job read `clean_orders` and which nights it read the copy.

A record made each time the job does its work would say so. Chapter 7 makes such records.

## U

## "Record the lineage of `daily_sales`."

After the stale lines, the head of the shop sets a requirement: "Record the lineage of `daily_sales`."

Before you read on, write in the next cell what you would record, and from what.

## V

The requirement could mean four things, each needing something different:

- **What someone says the job reads.** Needs someone to write it down. A line like Jo's records a belief.
- **What the job's code reads now.** Needs the repository, which is evidence of today. Followed back, these lines also say which tables and files `daily_sales` is made from.
- **What the job read on each night.** Needs a record made each time the job does its work. Nothing on the platform makes one (Chapter 7).
- **Which columns each of its columns is made from.** For example, `revenue_pence` is made from `price_pence` and `quantity` of `clean_orders`. Lines between tables do not say so (Chapter 10).

Your lines meet the requirement as written. They meet the second reading today, because they agree with the code. They do not meet the third or the fourth.

## W

## Before Chapter 7

The experiments showed that lines of what each job reads and writes let a traversal answer what a change to a file affects, and what an asset is made from. For the rename, the traversal gave the most it could affect, and the code showed which job uses the column. A line from a belief made the dashboard seem to depend on `customers.jsonl` until the comparison with the code. A line written from today's code went stale when the code changed, and the rows of `daily_sales` did not show it.

The experiments could not show what each job read on each night, or what the export, or anything done by hand, reads.

Chapter 7 records each time a job does its work: when it started and ended, which version of its code it used, what it read and wrote, and whether it succeeded.

- Take a platform you work on. Which of its lines of what reads and writes what were written by hand, and which came from its code? How would you find out that one of them is stale?
- A job reads its input table's name from a configuration file. Which of your lines could be false while the code still looks the same?

## X

### How this differs from a real platform

The shop, its people, its jobs and its repository are invented for the course.

The shop's jobs are short, and what each reads is found with a small rule: `read("...")`, and a name after `FROM` or `JOIN`, which is either a name `read` gave or a warehouse table.

Real code can hide what it reads in functions, variables or SQL built while the job executes. No small rule finds all of it.
