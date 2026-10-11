[Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)

# Chapter 1: The shop and its platform

**Objectives**

- Name the shop's three systems, and what each one holds: files, tables or a dashboard.
- Read the shop's products, customers and orders as their files store them.
- Read the rows of the warehouse's three tables, and the values the dashboard shows.
- Say what happens on the platform each night, and what you cannot see of it: the jobs, when they are due to run, and any notes.

[box: warning]
The page runs Python in your browser. The first time you open it, your browser downloads about 13 MB. On a computer, running every cell took 10 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

[box: steps]
**Running and saving the page**

1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.

[hidden code cell]

[hidden code cell]

[hidden code cell]

You start work on Monday 14 September 2026 at 09:00, as the data engineer of an online shop that sells bicycle parts. The shop opened its online store a week ago, on Monday 7 September. Nobody who built its data platform is there to ask, and nothing about it is written down. Before you have sat down, the head of the shop sends you one line: "Thursday's revenue looks wrong." You cannot yet tell whether it is wrong; to find out, you first need to know what the platform holds and what happens on it each night.

The platform has three systems: object storage, which holds files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard. Every night, jobs read the files, write the tables and refresh the dashboard. You can read everything the three systems hold. You cannot see the jobs, when they are due to run, or any note anybody kept.

In the code cells, three Python variables stand for the shop's three systems: `storage` is object storage, `warehouse` is the warehouse, and `reporting` is the reporting tool.

The three systems, in the order data moves through them each night.

[figure] The shop's three systems and what each holds.
[figure shows] Object storage customers.jsonl file orders.jsonl file products.csv file unseen jobs move data each night → Warehouse clean_customers table clean_orders table daily_sales table unseen jobs move data each night → Reporting tool sales_dashboard dashboard 3 files + 3 tables + 1 dashboard = 7 assets

An asset is one thing the platform holds: here, a file, a table or a dashboard.

The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours of the next day, an export from the shop's checkout and catalogue writes the three files to object storage again, then jobs write the tables and refresh the dashboard. The last night ends early on Monday 14 September, before you start work.

[figure] The shop's first week: order days, the export and jobs after each, and the morning you start.
[figure shows] The shop's first week: the shop took orders from Mon 7 to Sun 13 September; each night's export and jobs ran in the early hours of the next day; you start work at 09:00 on Mon 14.

## The product catalogue

`products.csv`, in object storage, holds the shop's product catalogue: 8 products in 6 categories. Each product has an id (`product_id`), a name, a category, a list price in pence (`list_price_pence`) and the member of staff who last edited it (`updated_by`). `products.csv` names its columns once, in its first line, and has no types: every value is text.

The cell below prints `products.csv` exactly as it is stored.

```python
print(storage.read_text("s3://shop-raw/products.csv"))
```

[output]
product_id,name,category,list_price_pence,updated_by
1,"Inner tube, 700x25c",tyres and tubes,650,k.adeyemi
2,"Brake pads, pair",brakes,1200,k.adeyemi
3,"Chain, 11-speed",drivetrain,3200,r.novak
4,"Folding tyre, 700x28c",tyres and tubes,3850,k.adeyemi
5,Saddle,contact points,4500,s.lund
6,Rear light,lights,1875,r.novak
7,Floor pump,tools,2999,s.lund
8,Bar tape,contact points,1425,s.lund

## The customers

`customers.jsonl` holds the shop's 10 customers, in 7 countries. A customer's record has five fields: an id (`customer_id`), a name, an email address (`email`), a country as a two-letter code, and the date the customer signed up (`signed_up`). `orders.jsonl` and `customers.jsonl` are JSON Lines, with one record per line, and every record names its fields. A JSON value has one of a few types, such as a string, a number, true or false, or null, and a date or an amount is just a string or a number.

The cell below prints `customers.jsonl` exactly as it is stored.

```python
print(storage.read_text("s3://shop-raw/customers.jsonl"))
```

[output]
{"customer_id": 101, "name": "Amara Okafor", "email": "amara.okafor@example.net", "country": "GB", "signed_up": "2025-11-02"}
{"customer_id": 102, "name": "Liam Byrne", "email": "liam.byrne@example.org", "country": "IE", "signed_up": "2026-01-15"}
{"customer_id": 103, "name": "Sofia Marino", "email": "SOFIA.MARINO@example.net", "country": "IT", "signed_up": "2026-02-20"}
{"customer_id": 104, "name": "Jonas Weber", "email": "jonas.weber@example.org", "country": "DE", "signed_up": "2025-08-30"}
{"customer_id": 105, "name": "Chloe Martin", "email": "chloe.martin@example.net", "country": "FR", "signed_up": "2026-03-04"}
{"customer_id": 106, "name": "Ravi Patel", "email": "ravi.patel@example.org", "country": "GB", "signed_up": "2026-04-11"}
{"customer_id": 107, "name": "Emma de Vries", "email": "emma.devries@example.net", "country": "NL", "signed_up": "2025-12-01"}
{"customer_id": 108, "name": "Tom Hughes", "email": null, "country": "GB", "signed_up": "2026-05-19"}
{"customer_id": 109, "name": "Hana Novak", "email": "hana.novak@example.org", "country": "CZ", "signed_up": "2026-06-23"}
{"customer_id": 110, "name": "Ben Carter", "email": "ben.carter@example.net", "country": "GB", "signed_up": "2026-06-07"}

## The orders

`orders.jsonl` holds every order the shop took, as the checkout sent it. Each night, the file is written again, with every order taken since the online store opened. An order's record has seven fields: its id (`order_id`), the customer (`customer_id`), the product (`product_id`), the number of items (`quantity`), the price of one item in pence (`price_pence`), a status (`status`) and the time it was placed (`ordered_at`, in UTC). In this week's file, `status` is `completed` or `cancelled`.

The cell below shows one day's orders as a table, and the day is set to Monday, `2026-09-07`. You can change it to any day from `2026-09-07` to `2026-09-13` and run the cell again.

```python
day = "2026-09-07"
storage.sql("s3://shop-raw/orders.jsonl", "SELECT * FROM file WHERE date(ordered_at) = :day", day=day)
```

[output]
order_id | customer_id | product_id | quantity | price_pence | status | ordered_at
7001 | 101 | 1 | 2 | 650 | completed | 2026-09-07T08:14:00Z
7002 | 104 | 3 | 1 | 3200 | completed | 2026-09-07T09:52:00Z
7003 | 102 | 6 | 1 | 1875 | completed | 2026-09-07T12:30:00Z
7004 | 107 | 2 | 2 | 1200 | completed | 2026-09-07T15:07:00Z
7005 | 110 | 8 | 1 | 1425 | completed | 2026-09-07T18:45:00Z
7006 | 103 | 5 | 1 | 4500 | completed | 2026-09-07T20:31:00Z

## The warehouse

The warehouse holds three tables: `clean_customers`, `clean_orders` and `daily_sales`. You read a table by writing SQL in `warehouse.sql`. `daily_sales` has one row per day: the day and that day's revenue in pence (`revenue_pence`).

The cell below reads every row of `clean_customers`.

```python
warehouse.sql("SELECT * FROM clean_customers")
```

[output]
customer_id | name | email | country | signed_up
101 | Amara Okafor | amara.okafor@example.net | GB | 2025-11-02
102 | Liam Byrne | liam.byrne@example.org | IE | 2026-01-15
103 | Sofia Marino | sofia.marino@example.net | IT | 2026-02-20
104 | Jonas Weber | jonas.weber@example.org | DE | 2025-08-30
105 | Chloe Martin | chloe.martin@example.net | FR | 2026-03-04
106 | Ravi Patel | ravi.patel@example.org | GB | 2026-04-11
107 | Emma de Vries | emma.devries@example.net | NL | 2025-12-01
109 | Hana Novak | hana.novak@example.org | CZ | 2026-06-23
110 | Ben Carter | ben.carter@example.net | GB | 2026-06-07

The cell below reads the first 7 rows of `clean_orders`, and you can change `LIMIT 7` to read more.

```python
warehouse.sql("SELECT * FROM clean_orders LIMIT 7")
```

[output]
order_id | customer_id | product_id | quantity | price_pence | status | ordered_at
7001 | 101 | 1 | 2 | 650 | completed | 2026-09-07T08:14:00Z
7002 | 104 | 3 | 1 | 3200 | completed | 2026-09-07T09:52:00Z
7003 | 102 | 6 | 1 | 1875 | completed | 2026-09-07T12:30:00Z
7004 | 107 | 2 | 2 | 1200 | completed | 2026-09-07T15:07:00Z
7005 | 110 | 8 | 1 | 1425 | completed | 2026-09-07T18:45:00Z
7006 | 103 | 5 | 1 | 4500 | completed | 2026-09-07T20:31:00Z
7007 | 105 | 4 | 2 | 3850 | completed | 2026-09-08T07:58:00Z

The cell below reads every row of `daily_sales`.

```python
warehouse.sql("SELECT * FROM daily_sales")
```

[output]
day | revenue_pence
2026-09-07 | 14700
2026-09-08 | 16225
2026-09-09 | 15375
2026-09-10 | 5150
2026-09-11 | 20424
2026-09-12 | 19149
2026-09-13 | 9775

## The dashboard

The reporting tool holds one dashboard, `sales_dashboard`, titled "Sales, last 7 days", and it shows each day's revenue in pounds for 7 to 13 September.

[figure] Monday morning's dashboard: revenue per day, 7 to 13 September.
[figure shows] Sales, last 7 days Last refreshed 2026-09-14 03:00:09 UTC. Mon 7 £147.00 Tue 8 £162.25 Wed 9 £153.75 Thu 10 £51.50 Fri 11 £204.24 Sat 12 £191.49 Sun 13 £97.75

## Your guesses about the warehouse tables

For each of the three tables, write down which file or table you think it is made from, and what on this page makes you think so. Keep what you wrote. Chapter 2 asks what evidence like this can establish.

[Chapter 2](chapter_02.ipynb) goes back to the head of the shop's line and starts with Thursday's revenue.

### How this differs from a real platform

The shop, its people and its data are invented for the course. All times are UTC.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow
