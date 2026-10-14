# Draft BR

## BR1

Section 1 read the shop's data: the orders in `orders.jsonl`, and the rows of `clean_orders` and `daily_sales`.

Besides that data, each system keeps records about the assets it holds: a record describes the file, the table or the dashboard, and is not an order or a day's revenue.

The cells below read three of these records: the warehouse's `information_schema` for `daily_sales` (the table, then its columns), the listing of the bucket `shop-raw`, and the reporting tool's record of `sales_dashboard`.

As you read them, look for whether any record says which job made `daily_sales`, or what that job read.

## BR2

Some of it the systems already keep for their own purposes: the names, types, counts and times you read in section 2, *What the platform records about its assets*.
