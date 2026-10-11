[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb)

# Chapter 2: The invisible data system

**Objectives**

- Read what the shop's three systems record about a file, a table and a dashboard.
- Work out from the data how `daily_sales` could have been made, and see what that does and does not establish.
- Follow three changes to the shop that leave the data unable to say what happened.
- Name the records that would have answered the questions the platform could not.

[box: warning]
The page runs Python in your browser, and the first time you open it on its own, your browser downloads about 13 MB. Measured on a computer, the page downloaded less than 1 MB when opened from Chapter 1's link, in a browser that had opened Chapter 1. Chapter 1's link opens this page in a new tab, and Chapter 1 stays open in its own tab. On a computer, running every cell took 10 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

[box: steps]
Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.

[hidden code cell]

[hidden code cell]

[hidden code cell]

## Monday morning

It is Monday 14 September 2026, your first morning as the shop's data engineer. You have looked round the shop's platform in [Chapter 1](chapter_01.ipynb). The head of the shop has sent you one line: "Thursday's revenue looks wrong."

The three systems, in the order data moves through them each night.

[figure] The shop's three systems and what each holds.
[figure shows] Object storage customers.jsonl file orders.jsonl file products.csv file unseen jobs move data each night → Warehouse clean_customers table clean_orders table daily_sales table unseen jobs move data each night → Reporting tool sales_dashboard dashboard 3 files + 3 tables + 1 dashboard = 7 assets

[figure] Monday morning's dashboard: revenue per day, 7 to 13 September.
[figure shows] Sales, last 7 days Last refreshed 2026-09-14 03:00:09 UTC. Mon 7 £147.00 Tue 8 £162.25 Wed 9 £153.75 Thu 10 £51.50 Fri 11 £204.24 Sat 12 £191.49 Sun 13 £97.75

Thursday shows £51.50, against £153.75 on Wednesday and £204.24 on Friday.

## Questions the platform cannot answer

Questions like the head of the shop's arrive every week on a platform you did not build:

- Is Thursday's total wrong, and since when?
- Can we delete `products.csv`? Does anything still read it?
- If the checkout renames a column in `orders.jsonl`, what stops working?
- Who should I ask about `daily_sales`?

Each is answered by something that happened, or by a decision somebody made: a job that reads a file, a rule somebody chose, a person who took responsibility. None of them is answered by the rows a table holds today.

## Thursday

Start with the arithmetic. `orders.jsonl` holds every order the shop took, as the checkout sent it. Thursday's orders add up to 20550 pence. `daily_sales` holds one row per day, with amounts in pence, and its Thursday row says 5150; the dashboard shows £51.50. Somewhere between the file and the table, 15400 pence, £154.00, went missing.

The cell below reads every order in `orders.jsonl` and adds up `price_pence` times `quantity` for one day. The day is set to Thursday, `2026-09-10`, and you can change it and run the cell again.

```python
orders = storage.records("s3://shop-raw/orders.jsonl")
day = "2026-09-10"
sum(o["price_pence"] * o["quantity"] for o in orders if o["ordered_at"].startswith(day))
```

[output]
20550

The code cell below reads the row from `daily_sales` for the day that the code cell above sets. If you change the day in the code cell above, run the code cell below too. It does not run again by itself. Select the code cell above and press **Run below**, which runs that cell and every cell below it.

```python
warehouse.sql("SELECT * FROM daily_sales WHERE day = :day", day=day)
```

[output]
day | revenue_pence
2026-09-10 | 5150

It is not only Thursday. On Monday, Friday and Sunday the raw orders add up to the day's row in `daily_sales`. On Tuesday, Wednesday, Thursday and Saturday they do not. The platform holds both sets of numbers and nothing that connects them: no record of which orders `daily_sales` counts, which job decided that, or why.

The cell below puts, for every day, the total of the raw orders in `orders.jsonl` beside that day's row in `daily_sales`. It shows whether the two are the same.

```python
warehouse.sql(
    """
    SELECT d.day, r.raw_orders_pence, d.revenue_pence,
           CASE WHEN r.raw_orders_pence = d.revenue_pence THEN 'same' ELSE 'different' END AS compared
    FROM daily_sales AS d
    JOIN (
        SELECT date(ordered_at) AS day, SUM(price_pence * quantity) AS raw_orders_pence
        FROM raw_orders
        GROUP BY day
    ) AS r USING (day)
    ORDER BY d.day
    """,
    files={"raw_orders": "s3://shop-raw/orders.jsonl"},
)
```

[output]
day | raw_orders_pence | revenue_pence | compared
2026-09-07 | 14700 | 14700 | same
2026-09-08 | 19224 | 16225 | different
2026-09-09 | 19875 | 15375 | different
2026-09-10 | 20550 | 5150 | different
2026-09-11 | 20424 | 20424 | same
2026-09-12 | 21549 | 19149 | different
2026-09-13 | 9775 | 9775 | same

## What the platform holds

Take `daily_sales`. The warehouse records two columns, `day` and `revenue_pence`, with their types; 7 rows and a size in bytes; a created time, 1 September, and a last-altered time, 02:30 on Monday 14 September; and an owner, `etl_service`. It records nothing else about the table.

The cell below reads the warehouse's record of `daily_sales` from its catalogue, which you query with SQL. `information_schema.tables` has one row per table, and `information_schema.columns` has one row per column, with the column's type.

```python
warehouse.sql("SELECT * FROM information_schema.tables WHERE table_name = 'daily_sales'")
```

[output]
table_catalog | table_schema | table_name | table_type | table_owner | row_count | bytes | created | last_altered
shop | analytics | daily_sales | BASE TABLE | etl_service | 7 | 794 | 2026-09-01T10:20:00Z | 2026-09-14T02:30:21Z

```python
warehouse.sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'daily_sales'")
```

[output]
column_name | data_type
day | DATE
revenue_pence | INTEGER

Object storage records as much about a file: its location, its size and when it was last modified. The reporting tool records the dashboard's title, who created it and when, when it last refreshed, and the values it shows.

The cell below lists the files in the bucket `shop-raw`. For each file, object storage records its key, its size in bytes and when it was last modified.

```python
storage.ls("s3://shop-raw/")
```

[output]
key | size_bytes | last_modified
s3://shop-raw/customers.jsonl | 1219 | 2026-09-14T01:02:41Z
s3://shop-raw/orders.jsonl | 7338 | 2026-09-14T01:00:41Z
s3://shop-raw/products.csv | 389 | 2026-09-14T01:04:41Z

The cell below shows what the reporting tool records about `sales_dashboard`.

```python
reporting.dashboard("sales_dashboard")
```

[output]
name | sales_dashboard
title | Sales, last 7 days
created_by | j.marsh
created | 2026-09-02T15:41:00Z
last_refreshed | 2026-09-14T03:00:09Z
values | day: 2026-09-07, revenue: £147.00day: 2026-09-08, revenue: £162.25day: 2026-09-09, revenue: £153.75day: 2026-09-10, revenue: £51.50day: 2026-09-11, revenue: £204.24day: 2026-09-12, revenue: £191.49day: 2026-09-13, revenue: £97.75

Everything here describes the asset as it is this morning. No field describes how it got that way: which job wrote it, what it read, what its rows were yesterday, or who decided its rules. The platform has a complete picture of its own state and no account of its history.

## What the fields are for

These fields exist because the systems need them. The warehouse keeps column names and types so that it can run a query; object storage keeps a file's location so that it can serve the file; the reporting tool keeps the values so that it can draw the chart. In the shop's platform, and in most real ones, a system records what its own work needs and nothing more. The questions you want answered are not its work.

The owner field shows how far that goes. "Who should I ask about `daily_sales`?" wants a person or a team. The warehouse answers `etl_service`, the account that all four of the shop's jobs log in as. The field is called owner, but the question it answers is which account controls the table. The requirement that every table has an owner is met, and your question is not.

The cell below lists the owner of every table in the catalogue.

```python
warehouse.sql("SELECT table_name, table_owner FROM information_schema.tables")
```

[output]
table_name | table_owner
clean_customers | etl_service
clean_orders | etl_service
daily_sales | etl_service

## Reconstruction

When the platform records no history, the usual move is to infer it from the data. For `daily_sales`, that means finding a query over another asset that gives the same rows. One does: read `clean_orders`, keep the completed orders, add up price times quantity per day. It reproduces `daily_sales` exactly, all seven rows. It also explains Thursday: three of Thursday's orders arrived with no customer id, `clean_orders` does not have them, and they are worth 15400 pence, £154.00.

The cell below runs a query over `clean_orders` that adds up price times quantity, in pence, for each day, counting only completed orders. It compares the query's rows with the rows of `daily_sales`; `True` means every row is the same.

```python
rebuilt = warehouse.sql("""
    SELECT date(ordered_at) AS day, SUM(price_pence * quantity) AS revenue_pence
    FROM clean_orders
    WHERE status = 'completed'
    GROUP BY day
    ORDER BY day
""")
rebuilt == warehouse.sql("SELECT * FROM daily_sales ORDER BY day")
```

[output]
True

The query is evidence of how the table could have been made, not a record of how it was made, and three small changes to the shop show the difference.

An analyst copies `clean_orders` to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night. Now the same query over the copy reproduces `daily_sales` too. None of the platform's records says which of the two the job reads. A query that fits is evidence for every source it fits.

The job that writes `daily_sales` is edited, from Saturday's row on, to keep every order that has not been refunded. The shop has no refunds, so from Saturday every order counts, cancelled ones included. Saturday's row in `daily_sales` becomes 21549 instead of 19149, in pence. The dashboard shows £215.49 instead of £191.49. The table still has 7 rows and the same last-altered time, and no simple query over the week's assets reproduces it any more. The evidence has gone, and the platform records nothing about the edit.

On the last night the job that writes `daily_sales` fails and writes nothing. The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found. Everything the platform records looks like a normal morning with one row fewer. Only a record of the failure would say that a write was due and did not happen.

[hidden code cell]

[output]
Choose a change to the shop from the menu below. Then select the first cell below the menu and press Run below . The cells below show the platform on Monday morning, after the week ran with the change you chose. The cells above the menu keep showing the week as it ran. Choose a change to the shop

[output]
Dropdown(layout=Layout(width='100%'), options=(('The shop stays as it is', []), ('An analyst copies clean_orde…

**What object storage holds**

```python
changed = shop.run_week(change.value)
changed.storage.ls()
```

[output]
key | size_bytes | last_modified
s3://shop-raw/customers.jsonl | 1219 | 2026-09-14T01:02:41Z
s3://shop-raw/orders.jsonl | 7338 | 2026-09-14T01:00:41Z
s3://shop-raw/products.csv | 389 | 2026-09-14T01:04:41Z

**The warehouse's record of `daily_sales`**

```python
changed.warehouse.sql("SELECT * FROM information_schema.tables WHERE table_name = 'daily_sales'")
```

[output]
table_catalog | table_schema | table_name | table_type | table_owner | row_count | bytes | created | last_altered
shop | analytics | daily_sales | BASE TABLE | etl_service | 7 | 794 | 2026-09-01T10:20:00Z | 2026-09-14T02:30:21Z

**The dashboard**

```python
changed.reporting.dashboard("sales_dashboard")
```

[output]
name | sales_dashboard
title | Sales, last 7 days
created_by | j.marsh
created | 2026-09-02T15:41:00Z
last_refreshed | 2026-09-14T03:00:09Z
values | day: 2026-09-07, revenue: £147.00day: 2026-09-08, revenue: £162.25day: 2026-09-09, revenue: £153.75day: 2026-09-10, revenue: £51.50day: 2026-09-11, revenue: £204.24day: 2026-09-12, revenue: £191.49day: 2026-09-13, revenue: £97.75

**Queries that give every row of `daily_sales`**

```python
shop.queries_that_rebuild(changed, "daily_sales", fit="covers")
```

[output]
source | keep | measure | per | sql
clean_orders | completed | revenue | day | SELECT date(ordered_at) AS key, SUM(price_pence * quantity) AS value
FROM clean_orders
WHERE status = 'completed'
GROUP BY date(ordered_at)
ORDER BY key

## A rule the week never tests

A reconstruction can be checked against the data, but only where the data has something to check. `clean_orders` is made from `orders.jsonl` by a few rules: keep one row of an order the export wrote twice, drop orders with no customer id, keep cancelled orders, and drop orders with a quantity of 0 or less. The last rule is in the job. No order in the week has a quantity of 0 or less, so the rule never removes a row, and a version of the job without it would have produced the same table. From the data, you cannot tell whether the rule exists. The data can confirm a rule only where some row would have triggered it.

The cell below counts the orders in `orders.jsonl` with a quantity of 0 or less.

```python
sum(1 for o in orders if o["quantity"] <= 0)
```

[output]
0

The cell below lists the settings of the four cleaning rules that turn the raw orders into `clean_orders` exactly, with one setting on each row. The rules cover orders written twice, orders with no customer id, cancelled orders, and orders with a quantity of 0 or less.

```python
shop.cleaning_rules_that_fit(week)
```

[output]
duplicates | missing_customer | cancelled | quantity
one | drop | keep | keep
one | drop | keep | drop

## Records made at the time

The questions at the start need three kinds of record, none of which the platform keeps:

- what an asset is: what `daily_sales` means, what it is for, and who is responsible for it;
- what happened: each night's write of `daily_sales`, when it ran, what it read, and whether it succeeded;
- what was made from what: `daily_sales` is built from the completed orders in `clean_orders`, and the dashboard reads `daily_sales`.

Information of this kind, about an asset or about the platform, is called metadata: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets. Some of it the systems already keep for their own purposes: the names, types, counts and times you read above. The systems do not keep what an asset means, what happened to it or what it was made from; somebody has to record those, and the second and third have to be recorded when the thing happens. A note of what a job read, written the next morning from the data, is a reconstruction, with the limits shown above.

Real platforms keep more history than the shop's: query logs, table snapshots, audit trails. Those are records made at the time too, kept by the system rather than by a person, and later chapters use them where they exist.

## The handover

Suppose you had been the engineer who built the platform, handing it over on the Friday before you started. Write down, for `daily_sales` alone, what you would leave: what the table means and who to ask about it; what runs each night, reading what and writing what; and what the next engineer should do when a night fails. Then compare it with what the warehouse records: two column names, a row count, a size, two times and an account.

[hidden code cell]

[output]
VBox(children=(HTML(value='<p>Your handover note for <code>daily_sales</code></p>'), Textarea(value='', layout…

You write your handover note in the box above. The cell below shows only what the warehouse records about `daily_sales`, so you can compare it with your note.

[hidden code cell]

[output]
table_catalog | table_schema | table_name | table_type | table_owner | row_count | bytes | created | last_altered
shop | analytics | daily_sales | BASE TABLE | etl_service | 7 | 794 | 2026-09-01T10:20:00Z | 2026-09-14T02:30:21Z

[output]
column_name | data_type
day | DATE
revenue_pence | INTEGER

## Before Chapter 3

The platform's state answers what exists. It does not answer what happened or why. Inferring the history from the data gave an explanation that fitted, and three ordinary changes made it ambiguous, made it wrong, or left a failed night looking like a normal one. The records that would have answered had to be made when the work was done.

Chapter 3 starts making them: a description of each asset, kept beside the data, with what the asset means and who is responsible for it. It then asks the four questions at the start again, to see which of them that record answers.

### How this differs from a real platform

The shop, its people and its data are invented for the course.

Some real systems keep history that the shop's warehouse does not. An Apache Iceberg table keeps snapshots, each the state of the table at some time. A Delta Lake table keeps, for each write, the operation, the user and the time, for 30 days by default. The shop's systems keep only the current rows.

In some real databases, a table's owner is an account too. In PostgreSQL, for example, a new table's owner is normally the account that created it. At first, only the owner (or a superuser) can do anything with the table; other accounts can use it once they are given the right to. The right to alter or drop the table comes with being its owner. The shop's warehouse records the owning account and no such rights.

A file's size is its real size in bytes. A table's size is an estimate from its rows. All times are UTC. A real platform has hundreds or thousands of assets; searching for queries that rebuild one would cost far more. "No simple query reproduces it" means none that keeps every row, completed orders or cancelled orders of one asset; a query with a condition on the date would.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow
