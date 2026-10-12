[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 10](chapter_10.ipynb) · [Next: Chapter 12](chapter_12.ipynb)

# Chapter 11: Schema evolution

**Objectives**

- Record a dataset's schema each time it is written, and compare two versions.
- Find which readers each of three changes to a file affects.
- Find what column lineage says about a change, and what it cannot say.
- Question the head of the shop's requirement about changes to datasets. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 10's link, in a browser that had opened and run Chapter 10 (measured on a computer). Chapter 10's link opens this page in a new tab. Chapter 10 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 10 leaves more memory for this page.

Running every cell took 9 to 12 seconds, and the page used about 410 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them. 

[figure] The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table returns. 

## The supplier's three changes

The checkout's supplier writes `orders.jsonl` each night. This is the export from Chapter 1. The supplier's code is not in the shop's repository.

The supplier plans one of three changes to the file, from the export before Saturday's row. It asks whether the shop can take the change.

- `added`: a new field, `coupon_code`;
- `renamed`: `quantity` renamed to `qty`;
- `retyped`: each customer id written as text, `C101` where it was `101`.

Before you read on, write in the next cell, for each change, whether you expect it to change what `daily_sales` holds on Monday, and why. 

```python
expected_changes = """
Does each change alter what daily_sales holds
on Monday, and why?
added ....
renamed ....
retyped ....
"""
```

## The schema over time

Object storage and the catalogue do not keep a dataset's past schemas. Object storage records nothing about a file's fields. The catalogue holds each table's columns as they are now.

The shop records a schema each time a program writes a dataset. For a file, it records the fields a reader finds and the type of their values. For a table, it records its columns and declared types from the catalogue, just after the write.

How a dataset's schema changes over time, version after version, is **schema evolution**.

The next cell runs the week with the `renamed` change and lists the versions of the schema of `orders.jsonl`. 

```python
week11 = shop.run_week(["renamed"])
shop.schemas.versions(week11, "orders.jsonl")
```

[output]
version | columns | first written | last written | writes | 
1 | order_id integer, customer_id integer, product_id integer, quantity integer, price_pence integer, status string, ordered_at string | 2026-09-08T01:00:41Z | 2026-09-12T01:00:41Z | 5 | 
2 | order_id integer, customer_id integer, product_id integer, qty integer, price_pence integer, status string, ordered_at string | 2026-09-13T01:00:41Z | 2026-09-14T01:00:41Z | 2 |

2 versions. Version 1 was written 5 times, from Tuesday 8 to Saturday 12. Version 2 was written twice, on Sunday 13 and Monday 14.

The next cell compares the two versions. 

```python
shop.schemas.diff(week11, "orders.jsonl")
```

[output]
column | change | before | after | 
quantity | removed | integer |  | 
qty | added |  | integer |

The comparison lists `quantity` as removed and `qty` as added.

The shop's records match columns by name. A rename looks like a removal and an addition. Nothing in the records says `qty` is `quantity` under a new name. Only the supplier's notice says so.

The next cell compares the versions under each of the three changes, and counts the versions of the schema of `clean_orders` under each. 

```python
shop.schemas.diffs()
```

[output]
supplier's change | column | change | before | after | versions of clean_orders | 
added | coupon_code | added |  | string | 1 | 
renamed | quantity | removed | integer |  | 1 | 
renamed | qty | added |  | integer | 1 | 
retyped | customer_id | retyped | integer | string | 1 |

`added`: `coupon_code` added, its values `string`. `retyped`: `customer_id` from `integer` to `string`.

Under every change, `clean_orders` has 1 version. Its columns and declared types are the same.

The next cell asks the warehouse for the type of each value in `customer_id` of `clean_orders`, in the week with the `retyped` change. 

```python
shop.run_week(["retyped"]).warehouse.sql("SELECT typeof(customer_id) AS type, COUNT(*) AS n FROM clean_orders GROUP BY 1")
```

[output]
type | n | 
text | 44 |

All 44 values are `text`, in a column the catalogue declares `INTEGER`. The warehouse keeps the text. The catalogue's record does not change. 

## What each reader gets

The next cell prints Jo Marsh's own query, which runs in a spreadsheet that reads the warehouse. It counts orders by the customer's country. It is not in the shop's repository and sends no events.

The cell after it counts what three readers get on Monday, in the plain week and with each change: the rows of `daily_sales`, the days the dashboard shows, and the rows of Jo Marsh's query. 

```python
print(shop.schemas.JO_QUERY)
```

[output]
SELECT c.country, COUNT(*) AS orders
FROM clean_orders o JOIN clean_customers c ON o.customer_id = c.customer_id
GROUP BY c.country


```python
shop.schemas.compare_all()
```

[output]
reader | plain week | added | renamed | retyped | 
rows of daily_sales | 7 | 7 | 5 | 7 | 
days on the dashboard | 7 | 7 | 5 | 7 | 
rows of Jo Marsh's query | 7 | 7 | 0 | 0 |

`added`: 7, 7 and 7, as in the plain week. `renamed`: 5, 5 and 0. `retyped`: 7, 7 and 0.

Compare these with what you wrote.

`renamed`: `build_clean_orders` reads `quantity` by name. The file has no `quantity`, so the value is empty, and the filter `quantity > 0` keeps no order. `clean_orders` has no rows after the last two nights, though the program succeeded each time. `daily_sales` has no row for Saturday or Sunday.

`retyped`: `daily_sales` is the same. Jo Marsh's query joins `clean_orders` to `clean_customers` on `customer_id`. `C101` never equals `101`, so it finds no rows.

A change to a dataset after which a program or a person that reads it fails or gets a different answer is a **breaking change**.

The new name broke all three readers. The new type broke Jo Marsh's query only. The new field broke none. 

## Who reads the column

The next cell uses Chapter 10's column lineage to list the programs whose code the shop has that read one column of `orders.jsonl`, and how. 

```python
column = "quantity"
shop.schemas.readers(week11, "orders.jsonl", column)
```

[output]
column | program | writes | reads it for | 
quantity | build_clean_orders | clean_orders | rows: distinct; rows: filter; value: copied |

`build_clean_orders` reads `quantity`: its value is copied, and it decides which rows count, by the filter and by `distinct`.

Change `column = "quantity"` to `column = "customer_id"`, select the cell and press **Run below**. The same program reads `customer_id`, in the same three ways.

From column lineage, a change to `customer_id` reaches `build_clean_orders`, and through it `daily_sales`. But `daily_sales` did not change. Column lineage says which programs read a column, not whether a change breaks them.

Jo Marsh's query, the one reader the new type broke, is in no record the shop keeps. 

## "Warn us of breaking changes."

The head of the shop's requirement: "Warn us of breaking changes."

Before you read on, write in the next cell whom you would warn of each of the three changes. 

```python
whom_to_warn = """
Whom would you warn of each change, and why?
........
"""
```

"Breaking" could mean breaking for three kinds of reader, each needing something different:

- a program that reads the dataset: it needs the column lineage of every program whose code the shop has, and the comparison of the schema's versions;
- the dashboard: it needs lineage downstream from those programs to the dashboard;
- somebody's own query: it needs a record of the queries people run, which the shop does not keep.

Checked against the shop's records, each reading gives one verdict:

- a program that reads it: met for the new name (`build_clean_orders` reads `quantity`). For the new type, the warning reaches `build_clean_orders`, which did not break;
- the dashboard: met, by following lineage from `build_clean_orders` to the dashboard;
- somebody's own query: not met. Jo Marsh's query is in no record.

The requirement does not say breaking for whom. 

## Before Chapter 12

The shop recorded a schema each time a dataset was written, and compared versions by name, so a rename was a removal and an addition. The new name gave every reader less. The new type changed nothing for `daily_sales` and emptied Jo Marsh's query. The new field changed nothing. Column lineage named the program that reads each column, not whether the change broke it, and no record named Jo Marsh's query.

It could not show when two names refer to the same table, or to two different ones.

Chapter 12 asks when two references name the same asset.

- Where does your platform record a dataset's past schemas, if anywhere?
- Who reads your most-used table without being in any record?
- Would a change that empties a table without an error be caught on your platform? 

### How this differs from a real platform

- The supplier, its changes and Jo Marsh's query are invented for the course.
- Apache Iceberg, a table format, gives each column an id and keeps it when the column is renamed, so its schemas can tell a rename from a removal and an addition. The shop's records hold names only.
- OpenLineage defines a `schema` facet for a dataset, which lists its fields with a name and a type.
- The shop's warehouse keeps a text value in a column declared `INTEGER`. A warehouse that enforces declared types would refuse the value, and the program would fail instead.
- `build_clean_orders` reads the fields it names, and a field the file does not have is empty. A reader that refuses a file without a field it names would fail instead.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 10](chapter_10.ipynb) · [Next: Chapter 12](chapter_12.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

