[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 2](chapter_02.ipynb) · [Next: Chapter 4](chapter_04.ipynb)

# Chapter 3: What is metadata?

**Objectives**

- Write a record of `daily_sales` from what the shop's people tell you.
- Find which of Chapter 2's four questions the record answers.
- Tell the information that says what an asset is from the information about what happened to it.
- Question the requirement "Every column must have a description."
- Find what a check against the warehouse catches when the shop changes. 

## Monday afternoon

It is still Monday 14 September 2026, in the afternoon. In Chapter 2 you found that `daily_sales` leaves out Thursday's three orders with no customer id (7021, 7023 and 7025, worth 15400 pence together), and nothing on the platform says whether they should be left out. You sent the head of the shop what Chapter 2 found.

The head of the shop replied:

> For `daily_sales` and the dashboard, ask Jo Marsh in finance, who built the dashboard and decides what counts as revenue. Sam Lund keeps the product catalogue. The two cleaned tables, `clean_customers` and `clean_orders`, were the last engineer's and are now yours.

Jo Marsh's answer, about a day's revenue:

> The value of every completed order placed that day, taking the day from the order's time in UTC, in pence.

None of this is on the platform. The next engineer to look at `daily_sales` would have to ask again. 

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

`clean_orders price_pence unit: pence`

The cells use three fields:

- `means`: what the asset or the column means.
- `responsible`: who to ask about it.
- `unit`: the unit the values are in.

A value of `........` is one not yet written.

The record cell below holds five lines for `daily_sales`, each with `........` as its value. Replace each `........` with what the head of the shop and Jo Marsh told you. Then select the cell and press **Run below**. The cell shows the record as a table, one row per line. **Save** keeps what you wrote. Until you fill in the dots and press **Run below**, the cells below the record show the dots, and the checks list them as problems. 

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
1 | daily_sales |  | means | ........ | 
2 | daily_sales |  | responsible | ........ | 
3 | daily_sales | day | means | ........ | 
4 | daily_sales | revenue_pence | means | ........ | 
5 | daily_sales | revenue_pence | unit | ........ |

The check cell lists each column of `daily_sales` that has no description, meaning no `means` line with a value. With every line written, it finds no problems. 

```python
records.check(warehouse, "daily_sales")
```

[output]
line | asset | column | problem | 
3 | daily_sales | day | Replace the dots on the column's means line with what the column holds. | 
4 | daily_sales | revenue_pence | Replace the dots on the column's means line with what the column holds. |

## The four questions again

Chapter 2 opened with four questions the platform could not answer:

- Is Thursday's total wrong, and since when?
- Can we delete `products.csv`? Does anything still read it?
- If the checkout renames a column in `orders.jsonl`, what stops working?
- Who should I ask about `daily_sales`?

Before you read on, write in the next cell, for each question, whether your record answers it, in part or not at all, and why. **Save** keeps what you wrote. 

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

The record answers the fourth question with Jo Marsh, the name you wrote from the head of the shop's reply, now kept where the next engineer can query it. The next cell takes Jo Marsh's words about a day's revenue and turns them into a query over `orders.jsonl`. It keeps each completed order once, even an order the export wrote twice. It adds up price times quantity for each UTC day, and puts that total beside each row of `daily_sales`, marked `same` or `different`. 

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

Thursday is the only day that differs: `daily_sales` shows 5150 pence, and Jo Marsh's meaning gives 20550. Every other day is the same. Tuesday, Wednesday and Saturday agree because the query leaves out cancelled orders and counts the order the export wrote twice once; Thursday differs, because its three orders with no customer id are completed orders, which Jo Marsh's meaning counts. By that meaning, Thursday's total is wrong.

The record says nothing about since when. It has no time in it, and nothing about what happened each night.

The file holds order 7015 on two lines. The words "every completed order" do not say whether a line or an order is counted. The query counts orders. A query that counted every line would find Wednesday different too. 

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

Every day is the same, Thursday included. A description written from the data is Chapter 2's query, which was chosen because it reproduces `daily_sales`. So it agrees with the table on every day, and it cannot show any day wrong. Jo Marsh's description came from the person who decides what counts as revenue, not from `daily_sales`, so `daily_sales` can be checked against it. 

The cell lists each line of your record that names `products.csv` or `orders.jsonl`. 

```python
records.sql("""
    SELECT * FROM records
    WHERE asset LIKE '%products.csv%' OR asset LIKE '%orders.jsonl%'
       OR value LIKE '%products.csv%' OR value LIKE '%orders.jsonl%'
""")
```

[output]
No rows.

It finds none. Every line of the record is about `daily_sales`, so none could say what reads a file. The second and third questions ask what reads those files. A record of what each asset is does not say what reads it. Chapter 6 keeps information about what reads each asset. 

## What the platform keeps

The warehouse, object storage and the reporting tool keep the following information.

- The warehouse: its columns, their types and its owner (an account) say what the table is and who controls it now. Its row count and size measure the table as the last write left it. Its last-altered time gives when that write happened, and its created time gives when the table was created.
- Object storage: a file's key gives its name and where it is. Its size and last-modified time come from its last write.
- The reporting tool: a dashboard's title says what the dashboard is. The creator, the creation time and the last refresh are work done to it.

Information about what an asset is, or who controls it now, is **descriptive**. Information about work done on the platform (who did something, when, and what it left) is **operational**. The warehouse keeps the last of each, not a history. Your record of `daily_sales` is descriptive.

A table's columns and their types make up its structure. That list is the table's **schema**. The word has a second use: in `information_schema`, its column `table_schema` names a group of tables in a database, such as `analytics`. The next cell lists the schema of the warehouse's three tables: 14 columns in all, 5 in `clean_customers`, 7 in `clean_orders` and 2 in `daily_sales`.

`orders.jsonl` declares no schema. Each line of the file names its fields, and a reader works out their types. `products.csv`'s first line names its columns and gives no types. 

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

Does the column `updated_by`, whose values include `s.lund`, say who to ask about `products.csv`? The head of the shop said Sam Lund keeps the product catalogue. `products.csv` has a column, `updated_by`, that holds a member of staff's login for each product. The next cell counts the products each login last edited. 

```python
storage.sql("s3://shop-raw/products.csv", "SELECT updated_by, COUNT(*) AS products FROM file GROUP BY updated_by")
```

[output]
updated_by | products | 
k.adeyemi | 3 | 
r.novak | 2 | 
s.lund | 3 |

Three people last edited the 8 products.

`updated_by` describes each product in the shop's catalogue: who last edited it there. Each edit was made in the catalogue, which is not one of the platform's assets. The export copies the values into the file. So `updated_by` is the shop's data. A field that said who last wrote `products.csv` would be metadata about the file.

The file's first line, `product_id,name,category,list_price_pence,updated_by`, names the file's columns. That line describes the file, so it is metadata, kept inside the same file as the data.

Chapter 2's definition holds: metadata is information about an asset or about the platform. Where the information is kept does not decide whether it is metadata. The warehouse keeps its tables' schemas inside itself, and you keep your record beside the data. Both describe assets, so both are metadata. 

## "Every column must have a description."

Suppose the shop sets the requirement: "Every column must have a description." Before you read on, write in the next cell whether the line `daily_sales revenue_pence means: the revenue in pence` describes the column `revenue_pence` as the requirement asks, and why. 

```python
verdict = """
daily_sales revenue_pence means: the revenue in pence
Does this line meet the requirement for revenue_pence? Why?
........
"""
```

The requirement could ask five different things. Each needs a different line:

- As written: the check's rule. It needs a `means` line with a value.
- The column's meaning: which orders it counts. It needs a line saying which orders, such as completed orders, each once, by UTC day.
- The unit. It needs a `unit` line that says pence.
- Where its values come from: which asset and which columns. It needs a line naming them. Your record holds nothing of this.
- Whether it may be empty. It needs a line saying so, which a check could test against the rows.

The line already says "in pence". Under the reading about meaning, it says nothing the name `revenue_pence` did not.

The next cell runs the check over all three tables. Your record describes only the columns of `daily_sales`, so the check lists the 12 columns of `clean_customers` and `clean_orders` that have no description. 

```python
records.check(warehouse)
```

[output]
line | asset | column | problem | 
 | clean_customers | customer_id | Your record has no means line for the column, so add one. | 
 | clean_customers | name | Your record has no means line for the column, so add one. | 
 | clean_customers | email | Your record has no means line for the column, so add one. | 
 | clean_customers | country | Your record has no means line for the column, so add one. | 
 | clean_customers | signed_up | Your record has no means line for the column, so add one. | 
 | clean_orders | order_id | Your record has no means line for the column, so add one. | 
 | clean_orders | customer_id | Your record has no means line for the column, so add one. | 
 | clean_orders | product_id | Your record has no means line for the column, so add one. | 
 | clean_orders | quantity | Your record has no means line for the column, so add one. | 
 | clean_orders | price_pence | Your record has no means line for the column, so add one. | 
 | clean_orders | status | Your record has no means line for the column, so add one. | 
 | clean_orders | ordered_at | Your record has no means line for the column, so add one. | 
3 | daily_sales | day | Replace the dots on the column's means line with what the column holds. | 
4 | daily_sales | revenue_pence | Replace the dots on the column's means line with what the column holds. |

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

With a description for each of the 14 columns, the check finds no problems. Its rule, the requirement as written, is met.

The next cell shows the two lines it wrote for `daily_sales`. 

```python
by_name.about("daily_sales")
```

[output]
line | asset | column | field | value | 
13 | daily_sales | day | means | day | 
14 | daily_sales | revenue_pence | means | revenue pence |

Under the readings about what a column means, its unit, where its values come from and whether it may be empty, these descriptions say nothing the names did not. They do not say which orders a column counts, where its values come from, or whether it may be empty. A check can count descriptions. It cannot tell whether a description says more than the column's name. 

## When the platform changes

Your record describes `daily_sales` as it is this Monday. The shop could make two changes. Each applies from Saturday's row of `daily_sales` on.

1. The job that writes `daily_sales` also writes each day's number of completed orders, in a new column, `order_count`. The rows before Saturday have no value in `order_count`.
2. The job is edited to keep every order that has not been refunded, as in Chapter 2. The shop has no refunds, so from Saturday a cancelled order counts too.

Before you read on, write in the next cell, for each change, whether the check of `daily_sales` will report a problem. 

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
3 | daily_sales | day | Replace the dots on the column's means line with what the column holds. | 
4 | daily_sales | revenue_pence | Replace the dots on the column's means line with what the column holds. | 
 | daily_sales | order_count | Your record has no means line for the column, so add one. |

```python
refunds_week = shop.run_week(["refunds"])
records.check(refunds_week.warehouse, "daily_sales")
```

[output]
line | asset | column | problem | 
3 | daily_sales | day | Replace the dots on the column's means line with what the column holds. | 
4 | daily_sales | revenue_pence | Replace the dots on the column's means line with what the column holds. |

For change 1, the check reports `order_count`, which has no description in your record. The check compares the columns of your record with the warehouse's, so the record is now incomplete.

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

Saturday now differs too: 21549 pence in `daily_sales`, against 19149 by Jo's meaning. Thursday still differs. Jo's query compares the values with Jo's meaning. It finds that the table no longer matches the meaning the record holds, although neither the record nor Jo's meaning has changed.

Neither comparison says what changed in the job, when it changed, or who changed it. Information made when the job changed, saying which version of the job's code ran each night, would show the change. Chapter 7 makes that kind of information. 

## Before Chapter 4

The experiments showed that your record answered who to ask about `daily_sales`: Jo Marsh. It answered whether Thursday is wrong by its stated meaning. A description written from the data could not have shown Thursday wrong, because it agrees with the data on every day. The requirement was met as written by four lines of code, and by no description that says more than the column's name. The check caught the new column. Jo's meaning caught the edit's effect on the table, but not the edit that caused it. The experiments could not show since when Thursday is wrong, or what reads `products.csv` or `orders.jsonl`.

Chapter 4 begins from two values. Your record names Jo Marsh as responsible for `daily_sales`. The reporting tool gives `j.marsh` as the dashboard's creator. Neither your record nor the reporting tool says that the two names refer to one person. Chapter 4 asks what each set of information is about, and how one set can point to what another describes.

- Pick a platform you work on. Which of its information says what a table is, and which says what happened to it?
- What would a description of a column have to say for a reader to learn something its name does not?
- How could two sets of information say that two names refer to one person? 

### How this differs from a real platform

The shop, its people and its data are invented for the course. All times are UTC.

Some real databases keep a description with a table or column. In PostgreSQL, the command `COMMENT ON` stores one comment for a table or a column, and a new one replaces the old. The comment is kept inside the database. The `\d` family of `psql` commands shows it. For most objects, only the owner can set it. The shop's warehouse keeps no descriptions.

The record notation is the course's own.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 2](chapter_02.ipynb) · [Next: Chapter 4](chapter_04.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

