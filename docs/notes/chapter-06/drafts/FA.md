## A

- Record what each job reads and writes, from its code.
- Find what a change to one file affects, and what an asset is made from.
- Test a line written from what a person believes against the code.
- Find what happens to such lines when a job's code changes.

## B

## The jobs' code

The checkout's developer writes:

> Next week we rename `customer_id` in `orders.jsonl` to `customer_ref`. What does that affect?

That is the third question from Chapter 2.

The head of the shop gives you access to the repository where the last engineer kept the jobs' code. In Chapter 1 you could not see the jobs. Now you can read their code.

The code says what each job does now. It does not say when a job did its work, or what it did on any night.

Two things that write or read the shop's files are not in the repository:

- the export, whose code belongs to the checkout's supplier;
- the analyst's copy of Chapter 2, a script on the analyst's laptop.

## C

The next cell prints the code of the four jobs, one file each. In each file, `read("...")` reads a file from object storage, a table after `FROM` is read from the warehouse, and `write("...")` or `refresh("...")` names what the job writes.

## D

The records cell holds Chapter 5's records, with one line for each of the two files that no line described, so that each is an entity. Under a `#` note, it also has two lines for each job: what the job reads and what it writes, with the attributes `reads` and `writes`, taken from the job's code.

The two lines for `build_daily_sales` have dots. Fill them in from that job's code, select the cell and press **Run below**. Until you do, the cells below show the dots: the check reports the two lines, and the walks stop at `clean_orders`.

## NOTE_CH5

Chapter 5's records

## NOTE_FILES

The two files no line described

## NOTE_JOBS

Each job's reads and writes, from its code

## E

The model cell adds a type, `job`, with two attributes:

- `job reads: dataset`: the value of `reads` on a job is a dataset.
- `job writes: dataset or dashboard`: the value of `writes` is a dataset or the dashboard.

Until now, a job has been a plain word. Now it is an entity: a node between the assets it reads and the assets it writes.

## F

## Lineage

The next cell draws only the `reads` and `writes` edges, between the assets and the jobs. This is the platform from Chapter 1, drawn with arrows at last, because your lines now record what each job reads and writes. An arrow from an asset to a job means the job reads it. An arrow from a job to an asset means the job writes it.

Records of what was made from what, and by which job, are **lineage**.

The drawing has 3 parts:

- `orders.jsonl` to `sales_dashboard` through three jobs;
- `customers.jsonl` to `clean_customers` through one job;
- `products.csv`, which no job reads.

## ALT

The drawing shows the chain from `orders.jsonl` through three jobs to `sales_dashboard`, the chain from `customers.jsonl` through one job to `clean_customers`, and `products.csv` with no arrow to a job.

## G

## What a change to `orders.jsonl` affects

Before you read on, write which assets a change to `orders.jsonl` affects, in the next cell. The cell gives no result. Write your answer in its dots.

## H

"""
Which assets does a change to orders.jsonl affect,
and why?
........
"""

## I

The cell above walked from `orders.jsonl` to each job that reads it, then to what that job writes, and on. What is made from an asset in this way is **downstream** of it.

Downstream of `orders.jsonl` there are 6 nodes. The 3 jobs are `build_clean_orders`, `build_daily_sales` and `refresh_dashboard`. The 3 assets are `clean_orders`, `daily_sales` and `sales_dashboard`.

The opposite walk goes from an asset to the job that writes it, then to what that job reads, and on. What an asset is made from in this way is **upstream** of it.

The next cell walks back from `sales_dashboard`.

## J

Upstream of `sales_dashboard` there are 6 nodes. The farthest back is `orders.jsonl`. `customers.jsonl` and `clean_customers` are not upstream of the dashboard.

The next cell walks downstream from `products.csv`.

## K

Downstream of `products.csv` there is nothing. No job in the repository reads it. Chapter 2 asked "Does anything still read it?" As far as the lines go, the answer is no.

The lines record only the jobs in the repository. The export and the analyst's script are not in the repository, and no line records what they read. So "nothing reads `products.csv`" means only that the lines know of no reader.
