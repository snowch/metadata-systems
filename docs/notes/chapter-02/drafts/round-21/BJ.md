## BJ1

## How `daily_sales` could have been made, and how it was made

The query above shows how `daily_sales` **could have been** made. It does not show how it **was** made.

To see the difference, try three what-ifs: three small changes to the shop. Nobody made these changes. None of them happened in the week you have read so far.

Each of the three cells below runs the shop's week again with one change. It prints a table with one row for each of the platform's records on Monday morning. The column `the week as it ran` holds the record for the week you have read. The column `with the change` holds the record for the week with the change.

The records, one per row:

- the files in object storage;
- the last-altered time of `clean_orders`;
- the number of rows in `daily_sales`, and its last-altered time;
- the last refresh time of the dashboard, and the values it shows;
- the queries that give every row of `daily_sales`.

The last row comes from a fixed set of simple queries over the week's assets. Each query reads one asset, keeps either all orders or the completed or cancelled ones, and adds up revenue, quantity or rows, per day, customer or product. A query is listed if it gives every row of `daily_sales`, even if it gives one row more. Each is written as the asset it reads, then what it keeps and what it adds up, for example `clean_orders: completed orders, revenue per day`, which is the query you ran above.

For each change, ask the same question: does a query over the week's assets still give every row of `daily_sales`, and which records show the change? Compare the two columns row by row.

## BJ2

**An analyst copies `clean_orders` every night.** The copy goes to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night, at 02:15, after the job that writes `clean_orders`.

The copy is a new file in object storage, `s3://shop-scratch/clean_orders_copy.csv`. The last row now lists two queries: the same query over `clean_orders` and over the copy. Every other record is the same as in the week as it ran. None of the records says which of the two the job that writes `daily_sales` reads. A query that fits is evidence for every source it fits.

## BJ3

**From Saturday, the `daily_sales` job keeps unrefunded orders.** Someone on the shop's team edits the job that writes `daily_sales`, so that from Saturday's row on, written early on Sunday 13, it keeps every order that has not been refunded, where it kept completed orders.

The shop has no refunds, so from Saturday every order counts, cancelled ones included. The dashboard shows £215.49 instead of £191.49 for Saturday, 2026-09-12. The table still has 7 rows and the same last-altered time. The last row says `none`. No query in the set gives the rows of `daily_sales` any more. No record on the platform says the job was edited.

## BJ4

**The `daily_sales` job fails on the last night.** Early on Monday 14, the job that writes `daily_sales` fails and writes nothing.

The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found. The query over `clean_orders` is still listed: it gives every row of `daily_sales`, and one row more, for Sunday. Each record is normal on its own. The gap shows only when you compare the last-altered times. Only a record of the failure would say that a write was due and did not happen.

## BJ5

The last row of each table above tries only the fixed set of simple queries. So `none`, in the second what-if, means none of those queries; it says nothing about others.
