## BK6.1

### Could have been made, or was made

## BK6.2

The query shows how `daily_sales` **could have been** made, not how it **was** made. Three what-ifs test that difference. Each describes one of three small changes to the shop. None of them happened in the week you have read.

Each cell below runs the week again with one change, and prints Monday morning's records in a table. The column `the week as it ran` holds the record for the week you have read. The column `with the change` holds the record for the week with the change.

For each change, ask: does a query over the week's assets still give every row of `daily_sales`, and which records show the change?

## BK6.3

<details><summary>How the last row is found</summary>

The last row comes from a fixed set of simple queries over the week's assets. Each reads one asset, keeps all, completed or cancelled orders, and adds up revenue, quantity or rows, per day, customer or product. A query is listed if it gives every row of `daily_sales`, even if it gives one row more. The listed queries include, for example `clean_orders: completed orders, revenue per day`, which is the query you ran above.

</details>

## BK7.1

### A rule the week never tests

## BK7.2

A reconstruction can be checked only where the data has something to check.

In the shop's design, `clean_orders` is made from `orders.jsonl` by four rules. No system records them:

- keep one row of an order the export wrote twice
- drop orders with no customer id
- keep cancelled orders
- drop orders with a quantity of 0 or less

The first cell counts the orders in `orders.jsonl` with a quantity of 0 or less. The second lists every setting of the four rules that turns the raw orders into `clean_orders` exactly, one setting per row.

## BK7.3

The count is 0. No order in the week has a quantity of 0 or less.

So the last rule never removes a row. Two settings fit: one with the rule and one without.

From the data you cannot tell whether the rule exists. The data can confirm a rule only where some row would have triggered it.

Your guess for `clean_orders` from Chapter 1 meets the same limit.

## BK8.1

## Records made at the time

Each question the investigation could not settle needs its own kind of record, and the platform keeps none of them. The table below sets them side by side.

## BK8.2

For `daily_sales`, each question beside what the platform holds and the record that would answer it.

| The question | What the platform holds | The record that would answer it |
| --- | --- | --- |
| What is `daily_sales`, and whom do I ask? | [columns] columns, [rows] rows, last altered [time]; owner `[owner]`, an account | A description of the asset: what it means, who is responsible for it. |
| What is it made from? | Nothing; a query over `clean_orders` fits, and with the analyst's copy, one over the copy fits too | A record of what was made from what (Chapter 6 calls this lineage). |
| What did each night's job do? | Nothing; after a failed night, each record looks normal | A record of each time a job ran: its code version, inputs, output, time, and whether it succeeded (Chapter 7). |

## BK8.3

A record of what the job read would have answered the analyst's copy. A record of which version of the job's code ran each night would have answered the edit. A record of whether each night's write succeeded would have answered the failed night.

## BK9.1

## Check: evidence of what a job read

## BK9.2

A data engineer wants to know which inputs one particular run of a job read.

They have three pieces of evidence. Which is the strongest evidence of what that run read?

Open an answer to see whether it holds; you can open the others after.

## BK9.3

<details class="ms-choice"><summary>A. The current table schema and its last-modified timestamp.</summary>

Not the strongest. A schema and a last-modified time describe the table as it is now. The time says when the table last changed, not what the job that wrote it read. With the analyst's copy, every one of these records stayed the same, whichever file the job read.

Try another answer.

</details>

<details class="ms-choice"><summary>B. A SQL query that reproduces the dashboard's current totals.</summary>

Not the strongest. A query that matches supports a hypothesis about how the totals could be produced. Another source can fit as well: with the analyst's copy, the same query over `clean_orders_copy.csv` gives the same rows. It matches today's totals, not what a past run did: after the edit to the job, no simple query fitted, and nothing said why.

Try another answer.

</details>

<details class="ms-choice"><summary>C. A recorded job-run event identifying the run ID, code version, input tables, output table, timestamp and status.</summary>

The strongest. It was recorded when the run happened, and it names that run, its code version, the tables it read and wrote, when, and whether it succeeded.

It is evidence of what the run's instrumentation captured. It is only as complete as that instrumentation: a read the instrumentation did not capture would be missing from the record. So it shows which inputs were recorded, not that the job read nothing else.

**Current metadata describes an asset. A matching reconstruction supports a hypothesis. Recorded execution events provide evidence of a particular run.**

</details>
