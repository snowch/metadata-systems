## titles.investigation
What storage records

## inspectorCaption
Browse the seven assets and what storage records about each.

## inspectorLead
Choose an asset from the list. The figure shows what its storage system records about it: the rows, column names and types, and the answers to eight questions about it.

Things to try:

- In `orders.parquet`, find the rows whose `customer_id` is NULL, and their day.
- Find an `order_id` that appears twice.
- Find the orders whose `status` is cancelled.
- Compare the number of rows in `orders.parquet` with the number in `clean_orders`.
- Open `daily_sales` and read what storage says about each question.

## inspectorAfter
Storage recorded names, types, row counts, sizes, times and an owning account. It does not say which program wrote an asset, from what, or why some orders in `orders.parquet` are missing from `clean_orders`.

## titles.construction
Rebuilding `daily_sales`

## construction
Storage does not say where `daily_sales` comes from. The data might. If a query over another asset gives exactly the same rows as `daily_sales`, that query is a candidate for how it was made.

Build one with the query builder. Choose an asset to read, which rows to keep, what to add up, and per what. The builder writes your choices as SQL and runs the query on Monday morning's data.

## c1Title
Rebuild `daily_sales`

## c1Task
Build a query that makes `daily_sales` from another asset. Choose an asset to read, which rows to keep, what to add up, and per what. The tests compare your result with `daily_sales` for each day: your row for that day must be exactly equal to its row.

## c1Fields
source
keep
measure
per

## c1Options
keep.all: every row
keep.completed: completed orders only
keep.cancelled: cancelled orders only
measure.revenue: price times quantity
measure.quantity: quantity
measure.rows: the number of rows
per.day: the day the order was placed
per.customer: customer
per.product: product

## c1Hints
A query that rebuilds `daily_sales` must count exactly the orders it counts and add up the same total per day.

Reading `orders.parquet` does not work. The raw file holds rows that `daily_sales` does not: an order written twice, orders with no customer id, and cancelled orders.

From `orders.parquet`, Monday already matches. Monday had none of those rows. Pick a day that does not match and compare.

Read from `clean_orders`.

Read from `clean_orders`, keep completed orders only, add up price times quantity, per the day the order was placed.

## c1Lead
Your query appears below as SQL, with its result, before you run the tests.

## c1Caption
Use the query builder to find what builds `daily_sales`.

## caseLabels
Monday 7 September
Tuesday 8 September
Wednesday 9 September
Thursday 10 September
Friday 11 September
Saturday 12 September
Sunday 13 September
