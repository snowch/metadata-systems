// Copyright © 2026 Christopher Snow

// The words of Chapter 1, "The shop and its platform": a tour of what the shop's platform holds,
// before Chapter 2 investigates Thursday's revenue. The opening, the map's lead and the sentence
// that gives the word "asset" moved here from Chapter 2, word for word; the rest is Haiku's draft
// of brief AV, checked for facts. Every number is pinned by shop-and-platform.facts.test.ts, read
// off the engine (packages/lab), which the page never names.

export const PROSE = {
  question:
    "You start work on Monday 14 September 2026 at 09:00, as the data engineer of an online shop that sells bicycle parts. The shop opened its online store a week ago, on Monday 7 September. Nobody who built its data platform is there to ask, and nothing about it is written down. Before you have sat down, the head of the shop sends you one line: Thursday's revenue looks wrong. You cannot yet tell whether it is wrong; to find out, you first need to know what the platform holds and what happens on it each night.\n\nThe platform has three systems: object storage, which holds files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard. Every night, programs read the files, write the tables and refresh the dashboard. You can read everything the three systems hold. You cannot see the programs, when they are due to run, or any note anybody kept.",
  platformLead:
    "The three systems, in the order data moves through them each night. The button at the foot of the window reopens this figure once you have scrolled past it.",
  platformAfter: "An asset is one thing the platform holds: here, a file, a table or a dashboard.",
  products:
    "The three files are kept in object storage, at `s3://shop-raw/`. All three are Parquet files. `products.parquet` is the shop's catalogue, with 8 rows, one per product. Its five columns are `product_id`, `name`, `category`, `list_price` (a price in pounds) and `updated_by`, the member of staff who last edited the product, such as `k.adeyemi`.",
  cardsLead: "Press a card to open it and see the asset's rows.",
  customers:
    "`customers.parquet` holds the shop's customers. It has 10 rows, one per customer, and five columns: `customer_id`, `name`, `email`, `country` (a two-letter code, such as GB or IE) and `signed_up` (a date).",
  orders:
    "`orders.parquet` holds the orders the shop took, as the checkout sent them. It has 48 rows, one per order line, and seven columns: `order_id`, `customer_id`, `product_id`, `quantity`, `price` (in pounds), `status` and `ordered_at` (a time). Each row's `status` is either `completed` or `cancelled`.",
  warehouse:
    "The warehouse keeps three tables in `shop.analytics`: `clean_customers`, `clean_orders` and `daily_sales`. `clean_customers` has the same columns as `customers.parquet`, and `clean_orders` has the same columns as `orders.parquet`. `daily_sales` has one row per day, with a `day` column and a `revenue` column in pounds.",
  dashboard:
    'The dashboard is titled "Sales, last 7 days", and `j.marsh` created it on 2 September. It shows one value per day, the revenue, for 7 to 13 September, drawn as bars. It was last refreshed at 03:00 on Monday 14 September.',
  nights:
    "The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours of the next day, the three files are written again, and then programs write the tables and refresh the dashboard. On the last night, which ended early on Monday 14 September, the files were written between 01:00 and 01:05, the three tables between 02:00 and 02:31, and the dashboard was refreshed at 03:00. You start work at 09:00.",
  unseen:
    "You have read every asset the three systems hold, and you know when each was last written. You have not seen the programs that wrote them, when they are due to run, or any note anybody kept. The systems keep what the programs left behind, not the programs themselves.",
  task: "For each of the three tables, write down which file or table you think it is made from, and what on this page makes you think so. Keep what you wrote. Chapter 2 asks what evidence like this can establish.",
  reflection:
    "The platform holds 7 assets, 3 files, 3 tables and 1 dashboard, with the time each was last written. It does not hold the programs, when they are due to run, or any note. Chapter 2 goes back to the head of the shop's line and starts with Thursday's revenue.",
  modelVsReality:
    "The shop, its people and its data are invented for the course.\n\nAll times are UTC. A real platform has hundreds or thousands of assets.",
} as const;
