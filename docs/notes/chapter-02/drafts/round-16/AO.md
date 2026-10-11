## title_1

Chapter 1, part 1: The shop and its platform

## app_title_1

The invisible data system, part 1

## objectives_1

- Name the shop's three systems, and what each one holds: files, tables or a dashboard.
- Read the shop's products, customers and orders as their files store them.
- Read the rows of the warehouse's three tables, and the values the dashboard shows.
- Say what happens on the platform each night, and what you cannot see of it: the programs, when they are due to run, and any notes.

## task

Before anyone asks you about the shop's numbers, find out what the platform holds and what happens on it each night.

## names

In the cells, `storage`, `warehouse` and `reporting` name the shop's three systems: object storage, the warehouse and the reporting tool.

## products

Heading: The product catalogue

Paragraph: `products.csv`, in object storage, holds the shop's catalogue: 8 products in 6 categories. Each product has an id (`product_id`), a name, a category, a list price in pence (`list_price_pence`) and the member of staff who last edited it (`updated_by`). `products.csv` names its columns once, in its first line, and has no types: every value is text.

Lead: The cell below prints `products.csv` exactly as it is stored.

## customers

Heading: The customers

Paragraph: `customers.jsonl` holds the shop's 10 customers, in 7 countries. A customer's record has five fields: an id (`customer_id`), a name, an email address (`email`), a country as a two-letter code, and the date the customer signed up (`signed_up`). `orders.jsonl` and `customers.jsonl` are JSON Lines, with one record per line, and every record names its fields. A JSON value has one of a few types, such as a string, a number, true or false, or null, and a date or an amount is just a string or a number.

Lead: The cell below prints `customers.jsonl` exactly as it is stored.

## orders

Heading: The orders

Paragraph: `orders.jsonl` holds every order the shop took, as the checkout sent it. Each night, the file is written again, with every order taken since the online store opened. An order's record has seven fields: its id (`order_id`), the customer (`customer_id`), the product (`product_id`), the number of items (`quantity`), the price of one item in pence (`price_pence`), a status (`status`) and the time it was placed (`ordered_at`, in UTC). In this week's file, `status` is `completed` or `cancelled`.

Lead: The cell below shows one day's orders as a table, and the day is set to Monday, `2026-09-07`. You can change it to any day from `2026-09-07` to `2026-09-13` and run the cell again.

## warehouse

Heading: The warehouse

Paragraph: The warehouse holds three tables: `clean_customers`, `clean_orders` and `daily_sales`. You read a table by writing SQL in `warehouse.sql`. `daily_sales` has one row per day: the day and that day's revenue in pence (`revenue_pence`).

Lead (a): The cell below reads every row of `clean_customers`.

Lead (b): The cell below reads the first 7 rows of `clean_orders`, and you can change `LIMIT 7` to read more.

Lead (c): The cell below reads every row of `daily_sales`.

## dashboard

Heading: The dashboard

Lead: The reporting tool holds one dashboard, `sales_dashboard`, titled "Sales, last 7 days", and it shows each day's revenue in pounds for 7 to 13 September.

## message

Before you have finished looking round the platform, the head of the shop sends you one line: "Thursday's revenue looks wrong." [Part 2](part-2.html) starts from that line.

## title_2

Chapter 1, part 2: Thursday's revenue and what the platform cannot say

## app_title_2

The invisible data system, part 2

## opening_2

Heading: Monday morning

Paragraph: It is Monday 14 September 2026, your first morning as the shop's data engineer. You have looked round the shop's platform in [part 1](./). The head of the shop has sent you one line: "Thursday's revenue looks wrong."
