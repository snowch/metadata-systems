## BH

The query shows how `daily_sales` could have been made. It does not show how it was made. You can test that difference with three small changes to the shop. Each changes the shop's week in one way, and you apply them one at a time. None of the three happened in the week you have read so far.

- **An analyst copies clean_orders every night**: the analyst copies `clean_orders` to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night.
- **From Saturday, the daily_sales job keeps unrefunded orders**: the job that writes `daily_sales` is edited, from Saturday's row on, to keep every order that has not been refunded, where it kept completed orders.
- **The daily_sales job fails on the last night**: it writes nothing that night.

For each change, the question is the same: does a query over the week's assets still give every row of `daily_sales`, and which of the platform's records show the change?

The menu below applies one change at a time.
