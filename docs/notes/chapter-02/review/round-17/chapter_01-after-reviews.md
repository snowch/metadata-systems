[Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)

# Chapter 1: The shop and its platform

**Objectives**

- Identify what the platform holds: three systems, which hold files, tables and a dashboard.
- Describe what happens on the platform each night, and what you cannot see of it: the export, the jobs, when they are due to run, and any notes.
- Write a guess, for each warehouse table, at what it is made from.

You start work on Monday 14 September 2026 at 09:00, as the data engineer of an online shop that sells bicycle parts. The shop opened its online store a week ago, on Monday 7 September. Nobody who built its data platform is there to ask, and nothing about it is written down. Before you have sat down, the head of the shop sends you a message: "Thursday's revenue looks wrong." You cannot yet tell whether it is wrong; to find out, you first need to know what the platform holds and what happens on it each night.

The platform has three systems: object storage, which holds files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard. Every night, an export from the shop's checkout and catalogue writes three files to object storage. Then jobs read the files, write the tables and refresh the dashboard. You can read everything the three systems hold. You cannot see the export, the jobs, when they are due to run, or any note anybody kept.

In the code cells, three Python variables stand for the shop's three systems: `storage` is object storage, `warehouse` is the warehouse, and `reporting` is the reporting tool.

The three systems, in the order data moves through them each night.

[figure] The shop's three systems and what each holds.

An asset is one thing the platform holds: here, a file, a table or a dashboard.

The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours of the next day, the export writes the three files to object storage again, then jobs write the tables and refresh the dashboard. The last night ends early on Monday 14 September, before you start work.

[figure] The shop's first week: order days, the export and jobs after each, and the morning you start.

[box]
The page runs Python in your browser, and the first time you open it your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

On a computer, running every cell took 10 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

</details>

[box]
**Running and saving the page**

1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.

[hidden code cell]

[hidden code cell]

[hidden code cell]

As you read each file, note which fields could tie it to a table in the warehouse. Note also anything in the rows that a job might have to deal with.

## The product catalogue

`products.csv`, in object storage, holds the shop's product catalogue: 8 products in 6 categories. Each product has an id (`product_id`), a name, a category, a list price in pence (`list_price_pence`) and the member of staff who last edited it (`updated_by`). `products.csv` stores every value as text, and it has no types.

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
6,Rear light,

## The customers

`customers.jsonl` holds the shop's 10 customers, in 7 countries. A customer's record has five fields: `customer_id`, a name, `email`, a country as a two-letter code, and `signed_up`. Each record names its fields. A date such as `signed_up` is just a string: the file has no date type.

The cell below prints `customers.jsonl` exactly as it is stored.

```python
print(storage.read_text("s3://shop-raw/customers.jsonl"))
```

[output]
{"customer_id": 101, "name": "Amara Okafor", "email": "amara.okafor@example.net", "country": "GB", "signed_up": "2025-11-02"}
{"customer_id": 102, "name": "Liam Byrne", "email": "liam.byrne@example.org", "country": "IE", "signed_up": "2026-01-15"}
{"customer_id": 103, "name": "Sofia Marino", "email"

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

The cell below reads the first 7 rows of `clean_orders`, and you can change `LIMIT 7` to read more.

```python
warehouse.sql("SELECT * FROM clean_orders LIMIT 7")
```

[output]
order_id | customer_id | product_id | quantity | price_pence | status | ordered_at
7001 | 101 | 1 | 2 | 650 | completed | 2026-09-07T08:14:00Z
7002 | 104 | 3 | 1 | 3200 | completed | 2026-09-07T09:52:00Z
7003 | 102 | 6 | 1 | 1875 | completed | 2026-09-07T12:30:00Z

The cell below reads every row of `daily_sales`.

```python
warehouse.sql("SELECT * FROM daily_sales")
```

[output]
day | revenue_pence
2026-09-07 | 14700
2026-09-08 | 16225
2026-09-09 | 15375

## The dashboard

The reporting tool holds one dashboard, `sales_dashboard`, titled "Sales, last 7 days", and it shows each day's revenue in pounds for 7 to 13 September.

[figure] Monday morning's dashboard: revenue per day, 7 to 13 September.

## Your guesses about the warehouse tables

For each of the three tables, write in the cell below which file or table you think it is made from, and what on this page makes you think so. Write one line per table, then press **Save** to keep it. Chapter 2 asks what evidence like this can establish.

```python
guesses = """
clean_customers: made from ........ because ........
clean_orders:    made from ........ because ........
daily_sales:     made from ........ because ........
"""
```

[Chapter 2](chapter_02.ipynb) goes back to the head of the shop's message and starts with Thursday's revenue.

### How this differs from a real platform

The shop, its people and its data are invented for the course. All times are UTC.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow
