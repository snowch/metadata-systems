[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb)

# Chapter 2: The invisible data system

**Objectives**

- Read what the shop's three systems record about a file, a table and a dashboard.
- Work out from the data how `daily_sales` could have been made, and see what that does and does not establish.
- Follow three changes to the shop that leave the data unable to say what happened.
- Name the records that would have answered the questions the platform could not.

## Monday morning

It is Monday 14 September 2026, your first morning as the shop's data engineer. You have looked round the shop's platform in [Chapter 1](chapter_01.ipynb). The head of the shop has sent you a message: "Thursday's revenue looks wrong."

The three systems, in the order data moves through them each night.

[figure] The shop's three systems and what each holds.

[figure] Monday morning's dashboard: revenue per day, 7 to 13 September.

Thursday shows £51.50, against £153.75 on Wednesday and £204.24 on Friday.

[box]
The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 1's link, in a browser that had opened Chapter 1 (measured on a computer). Chapter 1's link opens this page in a new tab. Chapter 1 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 1 leaves more memory for this page.

Running every cell took 10 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

</details>

[box]
Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.

[hidden code cell]

[hidden code cell]

[hidden code cell]

## Questions the platform cannot answer

Messages like the head's arrive every week on a platform you did not build. Each one raises questions like these:

- Is Thursday's total wrong, and since when?
- Can we delete `products.csv`? Does anything still read it?
- If the checkout renames a column in `orders.jsonl`, what stops working?
- Who should I ask about `daily_sales`?

The rows show whether Thursday's total differs from Thursday's orders. Why it differs, and since when, depends on the rules the jobs apply. Whether `products.csv` can be deleted, and what a renamed column in `orders.jsonl` breaks, depends on which files the jobs read. Who is responsible for `daily_sales` depends on what people decided and took on. The rows a table holds today record none of these.

## Thursday

Thursday's orders in `orders.jsonl` add up to 20550 pence. `daily_sales` says 5150 for Thursday, and the dashboard shows £51.50. The two totals differ by 15400 pence, £154.00.

The cell below reads every order in `orders.jsonl` and adds up `price_pence` times `quantity` for one day. The day is set to Thursday, `2026-09-10`, and you can change it and run the cell again.

```python
orders = storage.records("s3://shop-raw/orders.jsonl")
day = "2026-09-10"
sum(o["price_pence"] * o["quantity"] for o in orders if o["ordered_at"].startswith(day))
```

[output]
20550

The cell below reads the row from `daily_sales` for the day that the cell above sets. If you change the day in the cell above, run the cell below too. It does not run again by itself. Select the cell above and press **Run below**.

```python
warehouse.sql("SELECT * FROM daily_sales WHERE day = :day", day=day)
```

[output]
day | revenue_pence
2026-09-10 | 5150

It is not only Thursday. On Monday, Friday and Sunday the raw orders add up to the day's row in `daily_sales`. On Tuesday, Wednesday, Thursday and Saturday they do not. The platform holds both sets of numbers and nothing that connects them: no record of which orders `daily_sales` counts, which job decided that, or why.

The cell below puts, for every day, the total of the raw orders in `orders.jsonl` beside that day's row in `daily_sales`. It shows whether the two are the same. The `files=` argument of `warehouse.sql` lets the query read `orders.jsonl` from object storage as a table called `raw_orders`.

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

The cell below lists Thursday's orders in `orders.jsonl` that `clean_orders` does not have. Look at what these orders have in common, then compare their total with Thursday's gap of 15400 pence.

```python
warehouse.sql(
    """
    SELECT * FROM raw_orders
    WHERE date(ordered_at) = '2026-09-10'
      AND order_id NOT IN (SELECT order_id FROM clean_orders)
    """,
    files={"raw_orders": "s3://shop-raw/orders.jsonl"},
)
```

[output]
order_id | customer_id | product_id | quantity | price_pence | status | ordered_at
7021 | NULL | 4 | 2 | 3850 | completed | 2026-09-10T09:47:00Z
7023 | NULL | 5 | 1 | 4500 | completed | 2026-09-10T13:58:00Z
7025 | NULL | 3 | 1 | 3200 | completed | 2026-09-10T18:40:00Z

Orders 7021, 7023 and 7025 have no customer id. Together they are worth 15400 pence, the whole of Thursday's gap. `clean_orders` does not have them. Their absence from `clean_orders` shows which orders are missing, not why: nothing on the platform records the rule that left them out.

## What the platform holds

What does the warehouse record about `daily_sales`? The two cells below read `information_schema` with SQL, the warehouse's own record of its tables: `information_schema.tables` has one row per table, and `information_schema.columns` has one row per column, with the column's type.

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

The cells showed the two columns of `daily_sales`, `day` and `revenue_pence`, with their types. They also showed 7 rows, a size in bytes, a created time of 1 September, and a last-altered time of 02:30 on Monday 14 September. The warehouse lists `etl_service` as the owner. It records nothing else about the table.

Object storage records three things about a file: its key, its size in bytes and when it was last modified. A key is the file's full name, such as `s3://shop-raw/orders.jsonl`, where `shop-raw` is the bucket: the container the file sits in. The reporting tool records the dashboard's title, who created it and when, when it last refreshed, and the values it shows.

The cell below lists the files in the bucket `shop-raw`.

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

Everything here describes the asset as it is this morning. No field describes how it got that way: which job wrote it, what it read, what its rows were yesterday, or who decided its rules. The platform records the current state of each asset and none of its history.

## What the fields are for

These fields exist because the systems need them. The warehouse keeps column names and types so that it can run a query; object storage keeps a file's location so that it can serve the file; the reporting tool keeps the values so that it can draw the chart. In the shop's platform, a system records what its own work needs and nothing more. The questions you want answered are not its work.

The owner field shows how far that goes. "Who should I ask about `daily_sales`?" wants a person or a team. The requirement is: "Every table must have an owner." The warehouse records `etl_service` as the owner of all three tables. The name looks like an account a program logs in as, and the warehouse records nothing more about it. The field is called owner, but the question it answers is which account controls the table. The requirement is met as written, and your question is not.

The cell below lists the owner of every table in the warehouse.

```python
warehouse.sql("SELECT table_name, table_owner FROM information_schema.tables")
```

[output]
table_name | table_owner
clean_customers | etl_service
clean_orders | etl_service
daily_sales | etl_service

## Reconstruction

When the platform records no history, the usual move is to infer it from the data. For `daily_sales`, that means finding a query over another asset that gives the same rows. One does: read `clean_orders`, keep the completed orders, add up price times quantity per day. It reproduces `daily_sales` exactly, all seven rows. It also explains Thursday.

Compare the guess you wrote for `daily_sales` in Chapter 1's last cell with the query in the cell below, which the data supports.

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

On the last night the job that writes `daily_sales` fails and writes nothing. The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found. Each record is normal on its own. The gap shows only when you compare the last-altered times. Only a record of the failure would say that a write was due and did not happen.

[hidden code cell]

[output]
For each change, find which of the platform's records show it, and whether a query still gives every row of daily_sales . Choose a change to the shop from the menu below. Then select the first cell below the menu and press Run below . The cells below show the platform on Monday morning, after the we

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

The cell below lists each query, from a fixed set of simple ones over the week's assets, that gives every row of `daily_sales`, even if it gives a row more. Each row of its result is one query: `source` names the asset it reads; `keep` says which orders it keeps (all, completed or cancelled); `measure` says what it adds up (revenue, quantity or rows); `per` says what it groups by (day, customer or product); and `sql` is the query itself.

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

A reconstruction can be checked against the data, but only where the data has something to check. In the shop's design, which the platform does not record and you cannot see, `clean_orders` is made from `orders.jsonl` by four rules: keep one row of an order the export wrote twice, drop orders with no customer id, keep cancelled orders, and drop orders with a quantity of 0 or less. No order in the week has a quantity of 0 or less, so the rule never removes a row, and a version of the job without it would have produced the same table. From the data, you cannot tell whether the rule exists. The data can confirm a rule only where some row would have triggered it.

Your guess for `clean_orders` from Chapter 1 meets the same limit.

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
- what happened: each night's write of `daily_sales`, when it ran, which version of the job's code ran, what it read, and whether it succeeded;
- what was made from what: such a record would say that `daily_sales` is built from the completed orders in `clean_orders`, and that the dashboard reads `daily_sales`.

A record of what the job read would have answered the analyst's copy. A record of which version of the job's code ran each night would have answered the edit. A record of whether each night's write succeeded would have answered the failed night.

Information of this kind, about an asset or about the platform, is called metadata: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets. Some of it the systems already keep for their own purposes: the names, types, counts and times you read above. The systems do not keep what an asset means, what happened to it or what it was made from; somebody has to record those, and the second and third have to be recorded when the thing happens. A note of what a job read, written the next morning from the data, is a reconstruction, with the limits shown above.

Real platforms keep more history than the shop's: query logs, table snapshots, audit trails. Those are records made at the time too, kept by the system rather than by a person, and later chapters use them where they exist.

## The handover

Suppose you had been the engineer who built the platform, handing it over on the Friday before you started. Write down, for `daily_sales` alone, what you would leave: what the table means and who to ask about it; what runs each night, reading what and writing what; and what the next engineer should do when a night fails. Then compare it with what the warehouse records: two column names, a row count, a size, two times and an account.

```python
note = """
Write what daily_sales means and who to ask about it. Include what
runs each night, what it reads and writes, and what to do if a night fails.
"""
```

You write your handover note in the cell above, between the triple quotes, and press **Save** to keep it. The cell below shows only what the warehouse records about `daily_sales`, to compare with your note.

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

Chapter 3 starts making them: a description of each asset, kept beside the data, with what the asset means and who is responsible for it. It then asks the four questions at the start again, to see which of them that record answers. Chapter 6 records what was made from what, which is called lineage. Chapter 7 records each run of a job: when it started and ended, which version of its code ran, what it read and wrote, and whether it succeeded.

Nothing in this chapter tested your guess for `clean_customers`. What would test it?

- Pick a table on a platform you work on. What does its record say about who is responsible for it, and what does it say about what the table is made from?
- What would a description of `daily_sales` have to hold to answer "Who should I ask about `daily_sales`?"

### How this differs from a real platform

The shop, its people and its data are invented for the course.

Some real systems keep history that the shop's warehouse does not. An Apache Iceberg table keeps snapshots, each the state of the table at some time. A Delta Lake table keeps, for each write, the operation, the user and the time, for 30 days by default. The shop's systems keep only the current rows.

In some real databases, a table's owner is an account too. In PostgreSQL, for example, a new table's owner is normally the account that created it. At first, only the owner (or a superuser) can do anything with the table; other accounts can use it once they are given the right to. The right to alter or drop the table comes with being its owner. The shop's warehouse records the owning account and no such rights.

A file's size is its real size in bytes. A table's size is an estimate from its rows. All times are UTC. A real platform has hundreds or thousands of assets; searching for queries that rebuild one would cost far more. "No simple query over the week's assets reproduces it" means none of the simple queries the menu's last cell tries. A query with a condition on the date could still reproduce the edited table.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow
