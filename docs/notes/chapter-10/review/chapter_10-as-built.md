[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 9](chapter_09.ipynb) · [Next: Chapter 11](chapter_11.ipynb)

# Chapter 10: Column-level lineage

**Objectives**

- Find which columns of the raw orders the dashboard's revenue depends on, by reading the programs' SQL.
- Find what the SQL alone does not name.
- See what a function in a query hides.
- Question the requirement: "Show which columns `revenue_pence` depends on." 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 9's link, in a browser that had opened and run Chapter 9 (measured on a computer). Chapter 9's link opens this page in a new tab. Chapter 9 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 9 leaves more memory for this page.

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

## Which columns

Chapter 9's graph joins datasets: `build_daily_sales` reads `clean_orders` and writes `daily_sales`. It does not say which columns of `clean_orders` make which column of `daily_sales`.

Jo Marsh is checking the checkout's data and asks which fields of `orders.jsonl` matter to the revenue the dashboard shows.

The head of the shop's requirement: "Show which columns `revenue_pence` depends on."

Lineage between columns, which columns each column is made from, is **column lineage**.

Before you read on, write in the next cell which columns of `orders.jsonl` you expect `revenue_pence` to depend on, and why. 

```python
expected_columns = """
Which columns of `orders.jsonl` does `revenue_pence`
depend on, and why?
........
"""
```

## The program's SQL

The next cell prints the code of `build_daily_sales`, from the shop's repository (Chapter 6). 

```python
week10 = shop.run_week()
code = [p["code"] for p in shop.columns.programs(week10) if p["job"] == "build_daily_sales"][0]
print(code)
```

[output]
write("daily_sales", """
SELECT date(ordered_at), SUM(price_pence * quantity)
FROM clean_orders
WHERE status = 'completed' AND date(ordered_at) = :day
GROUP BY date(ordered_at)
""", append=True, day=yesterday)



"Depends on" could mean two things:

- the columns its value is computed from, which are in the expressions the SELECT lists;
- also the columns that decide which rows count, which are in the WHERE and GROUP BY clauses, and in DISTINCT.

Either reading can stop at the program that writes `daily_sales`, or go back through every program to `orders.jsonl`.

The next cell gives the code to the shop's parser. For each column the program writes, it lists each column it reads, with `kind` and `how`. 

```python
catalogue = None
# catalogue = warehouse
shop.columns.lineage(code, catalogue)
```

[output]
column | from | kind | how | 
daily_sales.column 1 | clean_orders.ordered_at | rows | filter | 
daily_sales.column 1 | clean_orders.ordered_at | rows | grouping | 
daily_sales.column 1 | clean_orders.ordered_at | value | computed | 
daily_sales.column 1 | clean_orders.status | rows | filter | 
daily_sales.column 2 | clean_orders.ordered_at | rows | filter | 
daily_sales.column 2 | clean_orders.ordered_at | rows | grouping | 
daily_sales.column 2 | clean_orders.price_pence | value | aggregated | 
daily_sales.column 2 | clean_orders.quantity | value | aggregated | 
daily_sales.column 2 | clean_orders.status | rows | filter |

The parser lists `column 1` and `column 2`. The SELECT names no column of `daily_sales`.

The warehouse puts the SELECT's first value in the table's first column, the second in the second. To name them, the parser needs the columns of `daily_sales`, from the catalogue.

In the cell above, delete the `# ` at the start of the line `# catalogue = warehouse`, select the cell and press **Run below**.

Then the parser names them `day` and `revenue_pence`.

`kind` is `value` for a column the value is computed from, and `rows` for a column that decides which rows count. `how` says the way: for `value`, `copied`, `computed` or `aggregated` (by SUM, COUNT and the like, over many rows); for `rows`, `filter` (WHERE), `grouping` (GROUP BY) or `distinct`. These names are the shop's own.

For `revenue_pence` the parser lists:

- `price_pence` and `quantity`: `value`, `aggregated`;
- `status`: `rows`, `filter`;
- `ordered_at`: `rows`, `filter` and `grouping`. 

## Back to the raw orders

The next cell follows `revenue_pence` back through every program whose code the shop has, to `orders.jsonl`. The export that writes `orders.jsonl` is not in the repository, so the parser stops there.

For each column it finds: `value` says whether `revenue_pence` is computed from it, through every step; `rows` says in which steps it decides which rows count. 

```python
shop.columns.upstream(week10, "daily_sales", "revenue_pence", week10.warehouse)
```

[output]
dataset | column | value | rows | 
clean_orders | ordered_at | no | filter in build_daily_sales; grouping in build_daily_sales | 
clean_orders | price_pence | yes |  | 
clean_orders | quantity | yes |  | 
clean_orders | status | no | filter in build_daily_sales | 
orders.jsonl | customer_id | no | distinct in build_clean_orders; filter in build_clean_orders | 
orders.jsonl | order_id | no | distinct in build_clean_orders | 
orders.jsonl | ordered_at | no | distinct in build_clean_orders; filter in build_daily_sales; grouping in build_daily_sales | 
orders.jsonl | price_pence | yes | distinct in build_clean_orders | 
orders.jsonl | product_id | no | distinct in build_clean_orders | 
orders.jsonl | quantity | yes | distinct in build_clean_orders; filter in build_clean_orders | 
orders.jsonl | status | no | distinct in build_clean_orders; filter in build_daily_sales |

The cell lists 11 columns: 4 of `clean_orders` and 7 of `orders.jsonl`. `revenue_pence` is computed from 2 columns of `orders.jsonl`: `price_pence` and `quantity`.

All 7 decide which rows count. `build_clean_orders` keeps one row of each set of equal rows (`distinct`), so every column takes part; its filter reads `customer_id` and `quantity`. The filter of `build_daily_sales` reads `status` and `ordered_at`. Each of the week's three oddities reached the revenue through a column that decides which rows count. Wednesday's second copy of order 7015 was removed by `distinct`. Thursday's 3 orders with no `customer_id` were removed by the filter of `build_clean_orders`. The cancelled orders of Tuesday and Saturday were left out by the filter on `status`.

By reading:

- the columns its value is computed from: `price_pence` and `quantity`;
- also the columns that decide which rows count: all 7.

The shop's parser records both kinds, so it answers either reading. The requirement does not say which. The first reading leaves out `customer_id`, the column behind Thursday's low revenue. 

## `SELECT *`

In Chapter 6's `source` change, `build_daily_sales` reads the analyst's copy, `clean_orders_copy.csv`, from Saturday's row on.

The analyst's script is not in the repository. The analyst sends its code: it writes the result of `SELECT * FROM clean_orders` to the copy.

The next cell gives that code to the parser without the catalogue; the cell after it, with it. 

```python
week10s = shop.run_week(["source"])
print(shop.columns.ANALYST_COPY)
shop.columns.lineage(shop.columns.ANALYST_COPY)
```

[output]
write("s3://shop-scratch/clean_orders_copy.csv", """
SELECT * FROM clean_orders
""")



[output]
column | from | kind | how | 
clean_orders_copy.csv.* | clean_orders.* | value | copied |

```python
shop.columns.lineage(shop.columns.ANALYST_COPY, week10s.warehouse)
```

[output]
column | from | kind | how | 
clean_orders_copy.csv.order_id | clean_orders.order_id | value | copied | 
clean_orders_copy.csv.customer_id | clean_orders.customer_id | value | copied | 
clean_orders_copy.csv.product_id | clean_orders.product_id | value | copied | 
clean_orders_copy.csv.quantity | clean_orders.quantity | value | copied | 
clean_orders_copy.csv.price_pence | clean_orders.price_pence | value | copied | 
clean_orders_copy.csv.status | clean_orders.status | value | copied | 
clean_orders_copy.csv.ordered_at | clean_orders.ordered_at | value | copied |

Without the catalogue: one row, `clean_orders_copy.csv.*` from `clean_orders.*`. `*` names no column, and the parser does not guess one.

With the catalogue: 7 rows, one for each column of `clean_orders`, each `copied`.

The next cell follows `revenue_pence` back in the week with the `source` change: 15 columns, through the copy (4), then `clean_orders` (4), to `orders.jsonl` (7). 

```python
shop.columns.upstream(week10s, "daily_sales", "revenue_pence", week10s.warehouse)
```

[output]
dataset | column | value | rows | 
clean_orders_copy.csv | ordered_at | no | filter in build_daily_sales; grouping in build_daily_sales | 
clean_orders_copy.csv | price_pence | yes |  | 
clean_orders_copy.csv | quantity | yes |  | 
clean_orders_copy.csv | status | no | filter in build_daily_sales | 
clean_orders | ordered_at | no | filter in build_daily_sales; grouping in build_daily_sales | 
clean_orders | price_pence | yes |  | 
clean_orders | quantity | yes |  | 
clean_orders | status | no | filter in build_daily_sales | 
orders.jsonl | customer_id | no | distinct in build_clean_orders; filter in build_clean_orders | 
orders.jsonl | order_id | no | distinct in build_clean_orders | 
orders.jsonl | ordered_at | no | distinct in build_clean_orders; filter in build_daily_sales; grouping in build_daily_sales | 
orders.jsonl | price_pence | yes | distinct in build_clean_orders | 
orders.jsonl | product_id | no | distinct in build_clean_orders | 
orders.jsonl | quantity | yes | distinct in build_clean_orders; filter in build_clean_orders | 
orders.jsonl | status | no | distinct in build_clean_orders; filter in build_daily_sales |

The catalogue gives the columns of `clean_orders` as they are on Monday.

`SELECT *` copies whatever columns its source has when it runs. A record made from Monday's catalogue does not say which columns an earlier run copied, if they were different then. Chapter 11 changes a dataset's columns. 

## A function

In the week with the `net` change, the shop's developer edits `build_daily_sales`, from Saturday's row on, to take away what was returned.

The developer added a function to the warehouse, `returned_quantity(order_id, product_id)`. It reads the table `returns` and gives how many of one product of an order came back.

The query also gains a `WITH` clause. It names a SELECT `lines`, and the query then reads from `lines`.

No order of Saturday or Sunday was returned, so the rows are the same.

The next cell prints the edited code. 

```python
week10n = shop.run_week(["net"])
print([p["code"] for p in shop.columns.programs(week10n) if p["job"] == "build_daily_sales"][0])
```

[output]
write("daily_sales", """
WITH lines AS (
    SELECT date(ordered_at) AS day, price_pence * (quantity - returned_quantity(order_id, product_id)) AS line_pence, status
    FROM clean_orders
)
SELECT day, SUM(line_pence)
FROM lines
WHERE status = 'completed' AND day = :day
GROUP BY day
""", append=True, day=yesterday)



Before you read on, write in the next cell whether the parser's answer for `revenue_pence` will include the table `returns`, and why. 

```python
expected_returns = """
Will the parser's answer for `revenue_pence` include
the table `returns`, and why?
........
"""
```

```python
shop.columns.upstream(week10n, "daily_sales", "revenue_pence", week10n.warehouse)
```

[output]
dataset | column | value | rows | 
clean_orders | order_id | yes |  | 
clean_orders | ordered_at | no | filter in build_daily_sales; grouping in build_daily_sales | 
clean_orders | price_pence | yes |  | 
clean_orders | product_id | yes |  | 
clean_orders | quantity | yes |  | 
clean_orders | status | no | filter in build_daily_sales | 
orders.jsonl | customer_id | no | distinct in build_clean_orders; filter in build_clean_orders | 
orders.jsonl | order_id | yes | distinct in build_clean_orders | 
orders.jsonl | ordered_at | no | distinct in build_clean_orders; filter in build_daily_sales; grouping in build_daily_sales | 
orders.jsonl | price_pence | yes | distinct in build_clean_orders | 
orders.jsonl | product_id | yes | distinct in build_clean_orders | 
orders.jsonl | quantity | yes | distinct in build_clean_orders; filter in build_clean_orders | 
orders.jsonl | status | no | distinct in build_clean_orders; filter in build_daily_sales |

13 columns. None is in `returns`.

The parser followed `lines` back to `clean_orders`. The value of `line_pence` is computed from `price_pence`, `quantity`, `order_id` and `product_id`: the last two are the function's arguments.

The parser cannot read inside the function. It takes the function's value to depend on its arguments and nothing else.

The run's events also name `clean_orders` as the only input.

A record that the function reads `returns` has to come from somewhere other than the query: from whoever wrote the function, or from the warehouse as the query runs. 

## In an event

OpenLineage defines a facet for column lineage, `columnLineage`, on an output dataset.

Under `fields`, it lists each output column with the input columns its value comes from. Under `dataset`, it lists input columns that affect the whole dataset, such as a filter's.

Each input carries a transformation `type`: `DIRECT` where the output's value is derived from the input, `INDIRECT` where the input affects the output without the value coming from it. A `subtype` says how: among them `TRANSFORMATION`, `AGGREGATION`, `FILTER` and `GROUP_BY`.

The shop writes `value` as `DIRECT` and `rows` as `INDIRECT`.

The next cell makes the facet the shop's producer would add to `daily_sales` in a run's `COMPLETE`, and prints it. 

```python
print(shop.columns.show(shop.columns.facet(week10, "daily_sales")))
```

[output]
{
  "_producer": "https://example.org/shop/jobs/tree/v1",
  "_schemaURL": "https://openlineage.io/spec/facets/1-2-0/ColumnLineageDatasetFacet.json#/$defs/ColumnLineageDatasetFacet",
  "fields": {
    "day": {"inputFields": [
      {"namespace": "warehouse://shop-warehouse", "name": "shop.analytics.clean_orders", "field": "ordered_at", "transformations": [{"type": "DIRECT", "subtype": "TRANSFORMATION"}]}
    ]},
    "revenue_pence": {"inputFields": [
      {"namespace": "warehouse://shop-warehouse", "name": "shop.analytics.clean_orders", "field": "price_pence", "transformations": [{"type": "DIRECT", "subtype": "AGGREGATION"}]},
      {"namespace": "warehouse://shop-warehouse", "name": "shop.analytics.clean_orders", "field": "quantity", "transformations": [{"type": "DIRECT", "subtype": "AGGREGATION"}]}
    ]}
  },
  "dataset": [
    {"namespace": "warehouse://shop-warehouse", "name": "shop.analytics.clean_orders", "field": "ordered_at", "transformations": [{"type": "INDIRECT", "subtype": "FILTER"}]},
    {"namespace": "warehouse://shop-warehouse", "name": "shop.analytics.clean_orders", "field": "ordered_at", "transformations": [{"type": "INDIRECT", "subtype": "GROUP_BY"}]},
    {"namespace": "warehouse://shop-warehouse", "name": "shop.analytics.clean_orders", "field": "status", "transformations": [{"type": "INDIRECT", "subtype": "FILTER"}]}
  ]
}


- Under `fields`: `day`, from `ordered_at` (`TRANSFORMATION`); `revenue_pence`, from `price_pence` and `quantity` (`AGGREGATION`).
- Under `dataset`: `ordered_at` (`FILTER` and `GROUP_BY`) and `status` (`FILTER`).

The facet keeps both kinds, so a program that receives it can answer either reading of the requirement. 

## Before Chapter 11

The shop's parser read the programs' SQL and listed, for each column, the columns it is computed from and the columns that decide which rows count. `revenue_pence` is computed from 2 columns of `orders.jsonl`, and all 7 decide which rows count, `customer_id` among them. The SQL did not name the columns of `daily_sales` or what `*` stands for; the catalogue did. A function hid the table it reads.

It could not show what happens to the programs downstream when a dataset's columns change.

Chapter 11 changes the columns of `orders.jsonl` and follows what each change does.

- Which of your platform's queries use `SELECT *`, and what would their column lineage need?
- Which functions in your warehouse read a table their callers do not name?
- When someone asks what a column depends on, which of the two readings do they need? 

### How this differs from a real platform

- The shop's parser is the course's own, and reads only the course's small SQL: one source per SELECT, and no joins.
- OpenLineage's project has its own SQL parser, a library written in Rust that reads several dialects, SQLite's among them.
- The facet's documentation lists no subtype for `DISTINCT`. The shop writes it as `INDIRECT` with no subtype: that is the shop's choice.
- The shop's warehouse keeps no record of which columns a query read while it ran.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 9](chapter_09.ipynb) · [Next: Chapter 11](chapter_11.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

