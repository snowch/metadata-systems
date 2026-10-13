## BI

The query shows how `daily_sales` could have been made. It does not show how it was made. To see the difference, try three what-ifs: three small changes to the shop. Nobody made these changes. None of them happened in the week you have read so far.

You choose one from the menu below. The page runs the shop's week again as if that change had happened, and the cells under the menu show the platform on Monday morning.

- **An analyst copies clean_orders every night**: an analyst copies `clean_orders` to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night, at 02:15, after the job that writes `clean_orders`.
- **From Saturday, the daily_sales job keeps unrefunded orders**: someone on the shop's team edits the job that writes `daily_sales`, so that from Saturday's row on, written early on Sunday 13, it keeps every order that has not been refunded, where it kept completed orders.
- **The daily_sales job fails on the last night**: early on Monday 14, the job that writes `daily_sales` fails and writes nothing.

For each change, the question is the same: does a query over the week's assets still give every row of `daily_sales`, and which of the platform's records show the change?
