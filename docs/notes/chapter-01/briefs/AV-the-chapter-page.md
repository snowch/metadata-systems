# Brief AV: Chapter 1's page, "The shop and its platform"

Chapter 1 becomes a page of the course, as Chapter 2 is. It is a tour: the learner reads what the
shop's platform holds, before Chapter 2 investigates Thursday's revenue. It has no prediction,
experiment or challenge to grade. Every fact below was read off the shop's engine on 11 October
2026; nothing else may be stated.

Write each slot as plain sentences, following `docs/style.md` and the writing standard in
`AGENTS.md`. Write only the slots below, each under its key. Do not add facts. Do not mention a
lab, an engine, a simulator, a notebook, Python or code. Do not use these words, which later
chapters introduce: metadata, schema, lineage, job, run (as a noun), event, upstream, downstream,
dataset, entity, attribute, identifier, freshness, owner of a table. Do not say which asset is
made from which, or that any asset is made from another: the learner works that out in Chapter 2.
Do not compare one asset's row count with another's. The reader is "you", a data engineer. British
English. No em dashes. Write names of files, tables and columns in backticks, as `orders.parquet`.
Write amounts as the page shows them, in pounds with two decimals and no currency sign, as 6.50.

## What the page says around the slots, kept word for word

1. The first section's prose, already written: "You start work on Monday 14 September 2026 at
   09:00, as the data engineer of an online shop that sells bicycle parts. ... Before you have sat
   down, the head of the shop sends you one line: Thursday's revenue looks wrong. You cannot yet
   tell whether it is wrong; to find out, you first need to know what the platform holds and what
   happens on it each night." Then: "The platform has three systems: object storage, which holds
   files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard. Every
   night, programs read the files, write the tables and refresh the dashboard. You can read
   everything the three systems hold. You cannot see the programs, when they are due to run, or
   any note anybody kept."
2. Then a figure of the three systems, with: "An asset is one thing the platform holds: here, a
   file, a table or a dashboard." The figure counts 3 files, 3 tables and 1 dashboard: 7 assets.

## Facts

### The files (object storage, in `s3://shop-raw/`)

All three are Parquet files. Each card below opens to show the file's rows.

- `products.parquet`: the shop's catalogue. 8 rows, one per product. Columns: `product_id`,
  `name`, `category`, `list_price` (a price in pounds, such as 6.50), `updated_by` (the member of
  staff who last edited the product, such as `k.adeyemi`). First row: product 1, "Inner tube,
  700x25c", category "tyres and tubes", 6.50.
- `customers.parquet`: the shop's customers. 10 rows, one per customer. Columns: `customer_id`,
  `name`, `email`, `country` (a two-letter code, such as GB or IE), `signed_up` (a date).
- `orders.parquet`: the orders the shop took, as the checkout sent them. 48 rows, one per order
  line. Columns: `order_id`, `customer_id`, `product_id`, `quantity`, `price` (in pounds),
  `status` (completed or cancelled), `ordered_at` (a time). First row: order 7001, customer 101,
  product 1, quantity 2, price 6.50, completed, 08:14 on 7 September.

### The warehouse's tables (in `shop.analytics`)

- `clean_customers`: 9 rows, with the same five columns as `customers.parquet`.
- `clean_orders`: 44 rows, with the same seven columns as `orders.parquet`.
- `daily_sales`: 7 rows, one per day from 7 to 13 September. Columns: `day` and `revenue` (in
  pounds). Monday's row: 2026-09-07, 147.00.

### The dashboard (in the reporting tool)

- Titled "Sales, last 7 days". Created by `j.marsh` on 2 September. It shows one value per day,
  revenue, for 7 to 13 September, as bars. It was last refreshed at 03:00 on Monday 14 September.

### The nights

- The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours
  of the next day, the three files are written again, then programs write the tables and refresh
  the dashboard.
- On the last night, which ended early on Monday 14 September: the files were written between
  01:00 and 01:05, the three tables between 02:00 and 02:31, and the dashboard was refreshed at
  03:00. You start work at 09:00.

## Slots

Section titles: each names the section's subject in at most six words, no colon.

- **title_files**, **title_customers**, **title_orders**, **title_warehouse**, **title_dashboard**,
  **title_nights**, **title_unseen**, **title_task**: the sections below, in order. (The first
  section's title is "Monday morning"; the last's is "Before Chapter 2".)
- **products**: the section on `products.parquet`, before its card. Facts: where the files are
  kept and that they are Parquet files; what `products.parquet` holds, its rows and its columns.
  Two to four sentences.
- **customers**: the section on `customers.parquet`, before its card. Facts: what it holds, its
  rows and its columns. Two or three sentences.
- **orders**: the section on `orders.parquet`, before its card. Facts: what it holds, as the
  checkout sent it; its rows; its columns, including `status` and its two values. Two to four
  sentences.
- **warehouse**: the section on the three tables, before their cards. Facts: the warehouse keeps
  three tables in `shop.analytics`; `clean_customers` and `clean_orders` have the same columns as
  the customer and order files; `daily_sales` has one row per day, a day and that day's revenue.
  Two to four sentences. Give no row counts.
- **dashboard**: the section on the dashboard, before its figure. Facts: its title, who created it
  and when, what it shows, when it was last refreshed. Two or three sentences.
- **nights**: the section on the nights, before a figure of the week. Facts: the nights, as above,
  including the last night's times. Three or four sentences.
- **unseen**: what the tour could not show. Facts: you have read every asset the three systems
  hold, and when each was last written; you have not seen the programs that wrote them, when they
  are due to run, or any note anybody kept; the systems keep what the programs left, not the
  programs. Two or three sentences.
- **task**: an exercise with nothing to grade. Facts: for each of the three tables, write down
  which file or table you think it is made from, and what on this page makes you think so; keep
  what you wrote; Chapter 2 asks what evidence like this can establish. Two or three sentences.
- **reflection**: the chapter's close. Facts: the platform holds 7 assets, 3 files, 3 tables and 1
  dashboard, and records when each was last written; it does not hold the programs, when they are
  due to run, or any note; Chapter 2 goes back to the head of the shop's line and starts with
  Thursday's revenue. Two or three sentences. Do not repeat the line itself.
- **caption_products**, **caption_customers**, **caption_orders**, **caption_warehouse**: each
  figure's caption, saying what the figure shows: one file's card, or the three tables' cards. One
  short sentence each.
- **role_products**, **role_customers**, **role_orders**, **role_clean_customers**,
  **role_clean_orders**, **role_daily_sales**: a card's one-line description of what the asset
  holds, from the facts above. At most ten words each. None may say what the asset is made from.
- **lead_cards**: one sentence before the first card: press a card to open it and see the
  asset's rows.
