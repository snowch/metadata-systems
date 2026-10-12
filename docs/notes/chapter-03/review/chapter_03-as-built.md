[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 2](chapter_02.ipynb) · [Next: Chapter 4](chapter_04.ipynb)

# Chapter 3: What is metadata?

**Objectives**

- Write a record of `daily_sales` from what the shop's people tell you.
- Find which of Chapter 2's four questions the record answers.
- Tell what a record of an asset holds, from what the systems record about it.
- Test a requirement about descriptions, and a check, against changes to the shop. 

## Monday afternoon

It is still Monday 14 September 2026, in the afternoon. In Chapter 2 you found that `daily_sales` leaves out Thursday's three orders with no customer id (7021, 7023 and 7025, worth 15400 pence together), and nothing on the platform records whether they should be left out. You asked the head of the shop who decides what `daily_sales` should count.

The head of the shop replied:

> Jo Marsh, in finance, built the dashboard and decides what counts as revenue. Sam Lund keeps the product catalogue. The two cleaned tables, `clean_customers` and `clean_orders`, were the last engineer's and are now yours.

Jo Marsh's answer, about a day's revenue:

> The value of every completed order placed that day, taking the day from the order's time in UTC, in pence.

Next, you write what you have learnt as a record kept beside the data, then ask Chapter 2's four questions again. 

The three systems, in the order data moves through them each night. 

[figure] The shop's three systems and what each holds. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 2's link, in a browser that had opened and run Chapter 2 (measured on a computer). Chapter 2's link opens this page in a new tab. Chapter 2 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 2 leaves more memory for this page.

Running every cell took 9 to 11 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

</details>

</div> 

<div class="ms-box ms-box-steps">

**Running and saving the page**

1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.

</div> 

[hidden code cell]

[hidden code cell]

[hidden code cell]

## A record of `daily_sales`

A record is a set of lines of text that you write and keep beside the data. Each line holds one fact. It starts with the asset's name. If the fact is about a column, the column's name comes next. Then come a field, a colon and the value. For example:

`daily_sales revenue_pence unit: pence`

The cells use three fields:

- `means`: what the asset or the column means.
- `responsible`: who to ask about it.
- `unit`: the unit the values are in.

A value of `........` is one not yet written.

The record cell below holds five lines for `daily_sales`, each with `........` as its value. Replace each `........` with what the head of the shop and Jo Marsh told you. Then select the cell and press **Run below**. The cell shows the record as a table, one row per line. **Save** keeps what you wrote. 

```python
records = shop.records("""
daily_sales means: ........
daily_sales responsible: ........
daily_sales day means: ........
daily_sales revenue_pence means: ........
daily_sales revenue_pence unit: ........
""")
records
```

[output]
line | asset | column | field | value | 
2 | daily_sales |  | means | ........ | 
3 | daily_sales |  | responsible | ........ | 
4 | daily_sales | day | means | ........ | 
5 | daily_sales | revenue_pence | means | ........ | 
6 | daily_sales | revenue_pence | unit | ........ |

The check cell lists each column of `daily_sales` that has no description, meaning no `means` line with a value. It also lists each line that names a column the warehouse does not have. With every line written, it finds no problems. 

```python
records.check(warehouse, "daily_sales")
```

[output]
line | asset | column | problem | 
 | daily_sales | day | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | daily_sales | revenue_pence | The records do not describe this column, because there is no means line for it or its value is still only dots. |

## The four questions again

Chapter 2 opened with four questions the platform could not answer:

- Is Thursday's total wrong, and since when?
- Can we delete `products.csv`? Does anything still read it?
- If the checkout renames a column in `orders.jsonl`, what stops working?
- Who should I ask about `daily_sales`?

Before you run the cells below, write in the next cell, for each question, whether your record answers it, in part or not at all, and why. **Save** keeps what you wrote. 

```python
expected = """
Is Thursday's total wrong, and since when? ........
Can we delete products.csv? Does anything still read it? ........
If the checkout renames a column in orders.jsonl, what stops working? ........
Who should I ask about daily_sales? ........
"""
```

The next cell looks up who the record names as responsible for `daily_sales`. 

```python
records.sql("SELECT value FROM records WHERE asset = 'daily_sales' AND field = 'responsible'")
```

[output]
value | 
........ |

The record answers the fourth question: it names Jo Marsh as responsible for `daily_sales`. The next cell takes Jo Marsh's words about a day's revenue and turns them into a query over `orders.jsonl`. It keeps each completed order once, even an order the export wrote twice. It adds up price times quantity for each UTC day, and puts that total beside each row of `daily_sales`, marked `same` or `different`. 

```python
by_jos_meaning = """
    SELECT d.day, d.revenue_pence, m.meant_pence,
           CASE WHEN d.revenue_pence = m.meant_pence THEN 'same' ELSE 'different' END AS compared
    FROM daily_sales AS d
    JOIN (
        SELECT date(ordered_at) AS day, SUM(price_pence * quantity) AS meant_pence
        FROM (SELECT DISTINCT * FROM raw_orders)
        WHERE status = 'completed'
        GROUP BY day
    ) AS m USING (day)
    ORDER BY d.day
"""
warehouse.sql(by_jos_meaning, files={"raw_orders": "s3://shop-raw/orders.jsonl"})
```

[output]
day | revenue_pence | meant_pence | compared | 
2026-09-07 | 14700 | 14700 | same | 
2026-09-08 | 16225 | 16225 | same | 
2026-09-09 | 15375 | 15375 | same | 
2026-09-10 | 5150 | 20550 | different | 
2026-09-11 | 20424 | 20424 | same | 
2026-09-12 | 19149 | 19149 | same | 
2026-09-13 | 9775 | 9775 | same |

Thursday is the only day that differs: `daily_sales` shows 5150 pence, and Jo Marsh's meaning gives 20550. Every other day is the same. By that meaning, Thursday's total is wrong.

The record says nothing about since when. It has no time in it, and nothing about what happened each night.

The words "every completed order" do not say what to do with an order the export wrote twice. The query had to decide, and it counts each order once. A query that counted every line of the file would also find Wednesday different, because order 7015 is in the file twice. 

The next cell compares `daily_sales` with a meaning you could write from the data alone: the completed orders in `clean_orders`, added up per day, as in Chapter 2. 

```python
warehouse.sql("""
    SELECT d.day, d.revenue_pence, m.meant_pence,
           CASE WHEN d.revenue_pence = m.meant_pence THEN 'same' ELSE 'different' END AS compared
    FROM daily_sales AS d
    JOIN (
        SELECT date(ordered_at) AS day, SUM(price_pence * quantity) AS meant_pence
        FROM clean_orders
        WHERE status = 'completed'
        GROUP BY day
    ) AS m USING (day)
    ORDER BY d.day
""")
```

[output]
day | revenue_pence | meant_pence | compared | 
2026-09-07 | 14700 | 14700 | same | 
2026-09-08 | 16225 | 16225 | same | 
2026-09-09 | 15375 | 15375 | same | 
2026-09-10 | 5150 | 5150 | same | 
2026-09-11 | 20424 | 20424 | same | 
2026-09-12 | 19149 | 19149 | same | 
2026-09-13 | 9775 | 9775 | same |

Every day is the same, Thursday included. A description written from the data agrees with the data on every day, so it cannot show that any day is wrong. Jo Marsh's description came from the person who decides what counts as revenue, not from `daily_sales`, so `daily_sales` can be checked against it. 

The last cell lists each line of your record that names `products.csv` or `orders.jsonl`. 

```python
records.sql("""
    SELECT * FROM records
    WHERE asset LIKE '%products.csv%' OR asset LIKE '%orders.jsonl%'
       OR value LIKE '%products.csv%' OR value LIKE '%orders.jsonl%'
""")
```

[output]
No rows.

It finds none. The second and third questions ask what reads those files. A record of what each asset is does not say what reads it. Chapter 6 records what reads each asset. 

## What the platform records already

Your record says what `daily_sales` is: what it means, who is responsible for it, and what its columns mean and their unit. The warehouse, object storage and the reporting tool record other things.

The warehouse records each table's columns and their types, its owner (an account) and its created time. It also records the table's row count, size and last-altered time. The row count, the size and the last-altered time change with every write to the table. Together with the created time, they record what happened to the table. The columns, their types and the owner say what the table is.

Object storage records a file's key, which says what the file is and where it is. Its size and last-modified time record the file's last write.

The reporting tool records a dashboard's title, which says what the dashboard is. It also records who created the dashboard and when, and when it last refreshed. The creator, the creation time and the last refresh record what happened to the dashboard.

Records of the first kind say what an asset is. Records of the second kind say what happened to it. The first kind is **descriptive**. The second is **operational**. Your record of `daily_sales` is descriptive.

A table's columns and their types make up its structure. That list is the table's **schema**. The next cell lists the schema of the warehouse's three tables: 14 columns in all, 5 in `clean_customers`, 7 in `clean_orders` and 2 in `daily_sales`.

`orders.jsonl` declares no schema. Each line names its fields, and a reader works out their types. `products.csv`'s first line names its columns and gives no types. 

```python
warehouse.sql("SELECT table_name, column_name, data_type FROM information_schema.columns")
```

[output]
table_name | column_name | data_type | 
clean_customers | customer_id | INTEGER | 
clean_customers | name | TEXT | 
clean_customers | email | TEXT | 
clean_customers | country | TEXT | 
clean_customers | signed_up | DATE | 
clean_orders | order_id | INTEGER | 
clean_orders | customer_id | INTEGER | 
clean_orders | product_id | INTEGER | 
clean_orders | quantity | INTEGER | 
clean_orders | price_pence | INTEGER | 
clean_orders | status | TEXT | 
clean_orders | ordered_at | TIMESTAMP | 
daily_sales | day | DATE | 
daily_sales | revenue_pence | INTEGER |

## A column that names a person

The head of the shop said Sam Lund keeps the product catalogue. `products.csv` has a column, `updated_by`, that holds a member of staff's login for each product. The next cell counts the products each login last edited. 

```python
storage.sql("s3://shop-raw/products.csv", "SELECT updated_by, COUNT(*) AS products FROM file GROUP BY updated_by")
```

[output]
updated_by | products | 
k.adeyemi | 3 | 
r.novak | 2 | 
s.lund | 3 |

The cell counts `k.adeyemi` 3, `r.novak` 2 and `s.lund` 3. Three people last edited the 8 products.

`updated_by` says who last changed each product. It is a fact about each product: the shop's catalogue keeps it, and the export copies it into the file. It says nothing about who is responsible for `products.csv`. The column would hold the same logins whoever that was. It is data about the shop's business.

The file's first line, `product_id,name,category,list_price_pence,updated_by`, names the file's columns. That line describes the file, so it is metadata, kept inside the same file as the data.

So what makes information metadata is what it describes: an asset, or the work done on the platform. Where the information is kept, and who wrote it, does not decide that. The warehouse keeps its tables' schemas inside itself. You keep your record beside the data. 

## "Every column must have a description."

Suppose the shop sets the requirement: "Every column must have a description." Before you read on, write in the next cell whether the line `daily_sales revenue_pence means: the revenue in pence` meets it, and why. 

```python
verdict = """
daily_sales revenue_pence means: the revenue in pence
Does this line meet the requirement? Why?
........
"""
```

The requirement could ask four different things. Each needs a different line:

- The column's meaning: which orders it counts. It needs a line saying which orders, such as completed orders, each once, by UTC day.
- The unit. It needs a `unit` line that says pence.
- Where its values come from: which asset and which columns. It needs a line naming them. Your record holds nothing of this.
- Whether it may be empty. It needs a line saying so, which a check could test against the rows.

The words `the revenue in pence` repeat the column's name: `revenue_pence` already said "revenue" and "pence".

The next cell runs the check over all three tables. Your record describes only the columns of `daily_sales`, so the check lists the 12 columns of `clean_customers` and `clean_orders` that have no description. 

```python
records.check(warehouse)
```

[output]
line | asset | column | problem | 
 | clean_customers | customer_id | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_customers | name | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_customers | email | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_customers | country | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_customers | signed_up | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_orders | order_id | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_orders | customer_id | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_orders | product_id | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_orders | quantity | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_orders | price_pence | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_orders | status | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | clean_orders | ordered_at | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | daily_sales | day | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | daily_sales | revenue_pence | The records do not describe this column, because there is no means line for it or its value is still only dots. |

The next cell meets the requirement the quick way. It writes a description for each of the 14 columns from the column's name, with underscores changed to spaces, and then runs the same check. 

```python
columns = warehouse.sql("SELECT table_name, column_name FROM information_schema.columns")
by_name = shop.records("\n".join(
    f"{c['table_name']} {c['column_name']} means: {c['column_name'].replace('_', ' ')}"
    for c in columns
))
by_name.check(warehouse)
```

[output]
No problems found.

With a description for each of the 14 columns, the check finds no problems: the requirement is met as written.

The next cell shows the two lines it wrote for `daily_sales`. 

```python
by_name.about("daily_sales")
```

[output]
line | asset | column | field | value | 
13 | daily_sales | day | means | day | 
14 | daily_sales | revenue_pence | means | revenue pence |

Under the other readings, these descriptions say nothing the names did not. They do not say which orders a column counts, where its values come from, or whether it may be empty. A check can count descriptions. It cannot tell whether a description says more than the column's name. 

## A record nobody updates

Your record describes `daily_sales` as it is this Monday. The shop could make two changes. Each applies from Saturday's row of `daily_sales` on.

1. The job that writes `daily_sales` also writes each day's number of completed orders, in a new column, `order_count`. The rows before Saturday have no value in `order_count`.
2. The job is edited to keep every order that has not been refunded, as in Chapter 2. The shop has no refunds, so from Saturday a cancelled order counts too.

Before you run the cells below, write in the next cell, for each change, whether the check of `daily_sales` will report a problem. 

```python
expected_changes = """
Change 1, new column: a problem? ........
Change 2, edited job: a problem? ........
"""
```

```python
column_week = shop.run_week(["column"])
records.check(column_week.warehouse, "daily_sales")
```

[output]
line | asset | column | problem | 
 | daily_sales | day | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | daily_sales | revenue_pence | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | daily_sales | order_count | The records do not describe this column, because there is no means line for it or its value is still only dots. |

```python
refunds_week = shop.run_week(["refunds"])
records.check(refunds_week.warehouse, "daily_sales")
```

[output]
line | asset | column | problem | 
 | daily_sales | day | The records do not describe this column, because there is no means line for it or its value is still only dots. | 
 | daily_sales | revenue_pence | The records do not describe this column, because there is no means line for it or its value is still only dots. |

For change 1, the check reports the new column, `order_count`, with no description. The warehouse records its columns, so the check can compare them with your record, and your record has no line for `order_count`.

For change 2, the check reports nothing: the edit changed no column.

The next cell compares the edited week's `daily_sales` with Jo's meaning, using the query from above. 

```python
refunds_week.warehouse.sql(by_jos_meaning, files={"raw_orders": "s3://shop-raw/orders.jsonl"})
```

[output]
day | revenue_pence | meant_pence | compared | 
2026-09-07 | 14700 | 14700 | same | 
2026-09-08 | 16225 | 16225 | same | 
2026-09-09 | 15375 | 15375 | same | 
2026-09-10 | 5150 | 20550 | different | 
2026-09-11 | 20424 | 20424 | same | 
2026-09-12 | 21549 | 19149 | different | 
2026-09-13 | 9775 | 9775 | same |

Saturday now differs too: 21549 pence in `daily_sales`, against 19149 by Jo's meaning. Thursday still differs.

Your record still says what Jo means by revenue. From Saturday the table counts a cancelled order. Nothing on the platform recorded the edit. So nothing prompted a change to your record, and the check could not see the edit. A record written by hand stays as written while the platform changes. An operational record, made when the job changed and saying which version of the job's code wrote each row, would have shown the edit. Chapter 7 makes such records. 

## Before Chapter 4

The experiments showed that your record answered who to ask about `daily_sales`: Jo Marsh. It answered whether Thursday is wrong by its stated meaning. A description written from the data could not have shown Thursday wrong, because it agrees with the data on every day. The check caught a new column, but not a changed meaning. The experiments could not show since when Thursday is wrong, or what reads `products.csv` or `orders.jsonl`.

Your record names Jo Marsh as responsible for `daily_sales`. The reporting tool records `j.marsh` as the dashboard's creator. Whether those are one person, and how a record could say so, is where Chapter 4 starts. Chapter 4 asks what each record is about, and how one record can point to what another describes.

- Pick a platform you work on. Which of its records say what a table is, and which say what happened to it?
- Which question does a column's description need to answer before a check can tell it apart from the column's name?
- If a job changed and nothing recorded the change, how would you find out when a table's meaning changed? 

### How this differs from a real platform

The shop, its people and its data are invented for the course. All times are UTC.

Some real databases keep a description with a table or column. In PostgreSQL, the command `COMMENT ON` stores one comment for a table or a column, and a new one replaces the old. The comment is kept inside the database. `psql`'s `\d` commands show it. For most objects, only the owner can set it. The shop's warehouse keeps no descriptions.

The record notation is the course's own.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 2](chapter_02.ipynb) · [Next: Chapter 4](chapter_04.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

