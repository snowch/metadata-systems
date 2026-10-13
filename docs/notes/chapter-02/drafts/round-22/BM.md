## BM1

The usual move is to infer how `daily_sales` was made: find a query over another asset that gives the same rows. The hypothesis below comes with the evidence for each part. Compare it with your guess for `daily_sales` at the end of Chapter 1.

## BM2

The query shows how `daily_sales` **could have been** made, not how it **was** made.

The difference is tested by three small changes to the shop. None of them happened in the week you have read.

Each cell below runs the week again with one change. It prints Monday morning's records in three columns: `the week as it ran`, `with the change`, and `changed`, which says `yes` where the two differ.

## BM3

### before

Can a query that fits tell two possible sources apart?

### after

Two records change: object storage has a new file, `s3://shop-scratch/clean_orders_copy.csv`, and the last row lists a second query that fits, over the copy. No record says which of the two the job that writes `daily_sales` reads, and a query that fits is evidence for every source it fits. Only a record of what the job read would settle it.

## BM4

### before

Does an edit to a job leave a trace in the platform's records?

### after

Two records change: the dashboard shows £215.49 instead of £191.49 for Saturday 12 September, and no query in the set fits any more (the last row says `none`). Saturday changes because the shop has no refunds: every order's `status` is `completed` or `cancelled`, so from Saturday cancelled orders count too. The row count, 7, and the last-altered time do not change, and no record says the job was edited. Only a record of which version of the job's code ran each night would show it.

## BM5

### before

Does a job that fails show up as a failure?

### after

Three records change: `daily_sales` has 6 rows, none for Sunday; it was last altered on Sunday at 02:30, a day earlier than `clean_orders`; and the dashboard shows 6 values. The dashboard still refreshed at 03:00 on Monday, and the query over `clean_orders` still fits, with one row more, for Sunday. The shortfall is there to see if you expect 7 rows or compare the last-altered times, but no record says a write was due and did not happen. Only a record of whether each night's write succeeded would.

## BM6

### The owner the warehouse records

Each system records what its own work needs: column types so that the warehouse can run a query, a key so that object storage can serve a file, and the values so that the reporting tool can draw a chart.

"Who should I ask about `daily_sales`?" wants a person or a team.
