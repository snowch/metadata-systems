## title_files

The files in object storage

## title_customers

The customers file

## title_orders

The orders file

## title_warehouse

The warehouse tables

## title_dashboard

The dashboard

## title_nights

What happens each night

## title_unseen

What the tour cannot show

## title_task

Your guesses about the warehouse tables

## products

The three files are kept in object storage, at `s3://shop-raw/`. All three are Parquet files. `products.parquet` is the shop's catalogue, with 8 rows, one per product. Its five columns are `product_id`, `name`, `category`, `list_price` (a price in pounds) and `updated_by`, the member of staff who last edited the product, such as `k.adeyemi`.

## customers

`customers.parquet` holds the shop's customers. It has 10 rows, one per customer, and five columns: `customer_id`, `name`, `email`, `country` (a two-letter code, such as GB or IE) and `signed_up` (a date).

## orders

`orders.parquet` holds the orders the shop took, as the checkout sent them. It has 48 rows, one per order line, and seven columns: `order_id`, `customer_id`, `product_id`, `quantity`, `price` (in pounds), `status` and `ordered_at` (a time). Each row's `status` is either `completed` or `cancelled`.

## warehouse

The warehouse keeps three tables in `shop.analytics`: `clean_customers`, `clean_orders` and `daily_sales`. `clean_customers` has the same columns as `customers.parquet`, and `clean_orders` has the same columns as `orders.parquet`. `daily_sales` has one row per day, with a `day` column and a `revenue` column in pounds.

## dashboard

The dashboard is titled "Sales, last 7 days", and `j.marsh` created it on 2 September. It shows one value per day, the revenue, for 7 to 13 September, drawn as bars. It was last refreshed at 03:00 on Monday 14 September.

## nights

The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours of the next day, the three files are written again, and then programs write the tables and refresh the dashboard. On the last night, which ended early on Monday 14 September, the files were written between 01:00 and 01:05, the three tables between 02:00 and 02:31, and the dashboard was refreshed at 03:00. You start work at 09:00.

## unseen

You have read every asset the three systems hold, and you know when each was last written. You have not seen the programs that wrote them, when they are due to run, or any note anybody kept. The systems keep what the programs left behind, not the programs themselves.

## task

For each of the three tables, write down which file or table you think it is made from, and what on this page makes you think so. Keep what you wrote. Chapter 2 asks what evidence like this can establish.

## reflection

The platform holds 7 assets, 3 files, 3 tables and 1 dashboard, with the time each was last written. It does not hold the programs, when they are due to run, or any note. Chapter 2 goes back to the head of the shop's line and starts with Thursday's revenue.

## caption_products

The card for `products.parquet`, one of the three files in object storage.

## caption_customers

The card for `customers.parquet`, one of the three files in object storage.

## caption_orders

The card for `orders.parquet`, one of the three files in object storage.

## caption_warehouse

The cards for the three tables in `shop.analytics`.

## role_products

The shop's product catalogue, with prices and last editors.

## role_customers

The shop's customers, with their countries and sign-up dates.

## role_orders

Checkout orders, one row per order line.

## role_clean_customers

The shop's customers, in the warehouse, with five columns.

## role_clean_orders

The shop's orders, in the warehouse, with seven columns.

## role_daily_sales

Revenue for each day, from 7 to 13 September.

## lead_cards

Press a card to open it and see the asset's rows.
