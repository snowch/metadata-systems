[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 23](chapter_23.ipynb) · [Next: Chapter 25](chapter_25.ipynb)

# Chapter 24: Build the metadata store

**Objectives**

- Keep the week's metadata as JSON documents, as a table, as a table with an index, and as a graph.
- Answer the same question for each shape: what reads a dataset.
- Count the records each shape reads to answer it, and find which questions each shape suits.
- Question the requirement "The metadata store must be fast."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## One question, four shapes

Since Chapter 9, the shop's metadata system has answered questions from the events it ingested. Part VI builds the parts it used, one chapter each, starting here with the store that keeps the metadata.

One store can keep the same metadata in different shapes.

Here the metadata is the 14 edges by job of the week with the returns desk, the week Chapter 23 measured. It also holds the lines Chapter 4 wrote about two datasets: what `daily_sales` means and who is responsible for it, and who is responsible for `sales_dashboard`.

Each shape answers one question: what reads a dataset? You write the answer for each shape.

A check below your code runs it for each of the 11 datasets the edges name, compares each answer with the edges, and counts the items your code read.

The first shape is JSON documents: one for each program that ran (the four jobs and the returns desk's two functions) and one for each dataset. The next cell prints them, one document on each line.

    >>> week24 = shop.run_week(["returns"])
    >>> documents = shop.store.documents(week24)
    >>> print(documents)
      {"job": "shop/build_clean_customers", "runs": 7, "reads": ["s3://shop-raw/customers.jsonl"], "writes": ["warehouse://shop-warehouse/shop.analytics.clean_customers"]}
      {"job": "shop/build_clean_orders", "runs": 7, "reads": ["s3://shop-raw/orders.jsonl"], "writes": ["warehouse://shop-warehouse/shop.analytics.clean_orders"]}
      {"job": "shop/build_daily_sales", "runs": 7, "reads": ["warehouse://shop-warehouse/shop.analytics.clean_orders"], "writes": ["warehouse://shop-warehouse/shop.analytics.daily_sales"]}
      {"job": "shop/record_return", "runs": 5, "reads": ["s3://shop-returns/r-201.json", "s3://shop-returns/r-202.json", "s3://shop-returns/r-203.json", "s3://shop-returns/r-204.json"], "writes": ["warehouse://shop-warehouse/shop.analytics.returns"]}
      {"job": "shop/refresh_dashboard", "runs": 7, "reads": ["warehouse://shop-warehouse/shop.analytics.daily_sales"], "writes": ["reporting://shop-reporting/sales_dashboard"]}
      {"job": "shop/remove_return", "runs": 1, "reads": [], "writes": ["warehouse://shop-warehouse/shop.analytics.returns"]}
      {"dataset": "reporting://shop-reporting/sales_dashboard", "responsible": "j.marsh"}
      {"dataset": "s3://shop-raw/customers.jsonl"}
      {"dataset": "s3://shop-raw/orders.jsonl"}
      {"dataset": "s3://shop-returns/r-201.json"}
      {"dataset": "s3://shop-returns/r-202.json"}
      {"dataset": "s3://shop-returns/r-203.json"}
      {"dataset": "s3://shop-returns/r-204.json"}
      {"dataset": "warehouse://shop-warehouse/shop.analytics.clean_customers"}
      {"dataset": "warehouse://shop-warehouse/shop.analytics.clean_orders"}
      {"dataset": "warehouse://shop-warehouse/shop.analytics.daily_sales", "means": "the value of every completed order placed that day, by its UTC date", "responsible": "j.marsh"}
      {"dataset": "warehouse://shop-warehouse/shop.analytics.returns"}

A program's document holds `job`, its number of runs (`runs`), the datasets it reads (`reads`) and the datasets it writes (`writes`).

A dataset's document holds `dataset` and the lines Chapter 4 wrote about it, where there are any. It has no `reads`.

The 11 datasets are the ones the edges name, so the list includes `r-203.json`, which is no longer in storage. It leaves out `products.csv`, which no program reads or writes. That is why it differs from the map's assets.

The next cell defines `readers_of(documents, dataset)`. Its loop goes through every document and adds nothing to the result.

As it stands, the check below it finds 3 of 11 datasets right: the 3 that no program reads.

Change the line inside the loop so that it adds a program's `job` when its `reads` lists the dataset. Then select the cell and press **Run below**.

    >>> def readers_of(documents, dataset):
    >>>     found = []
    >>>     for doc in documents:
    >>>         pass  # add doc["job"] when the document's "reads" lists the dataset
    >>>     return found

    >>> shop.store.check(week24, documents, readers_of)
      | dataset | yours | read | 
      | sales_dashboard |  | 17 | right
      | customers.jsonl |  | 17 | expected build_clean_customers
      | orders.jsonl |  | 17 | expected build_clean_orders
      | r-201.json |  | 17 | expected record_return
      | r-202.json |  | 17 | expected record_return
      | r-203.json |  | 17 | expected record_return
      | r-204.json |  | 17 | expected record_return
      | clean_customers |  | 17 | right
      | clean_orders |  | 17 | expected build_daily_sales
      | daily_sales |  | 17 | expected refresh_dashboard
      | returns |  | 17 | right

With the loop changed, the check finds 11 of 11 datasets right. The loop reads 187 documents: all 17 documents for each of the 11 datasets.

The loop opens every document because a dataset's readers are named in each program's document, not in the dataset's own.

## A table

The second shape is a table in SQLite, the database the shop's warehouse runs on: `edges`, with one row for each edge by job, and the columns `job`, `edge`, `dataset` and `runs`.

The table has no index. SQLite does not make one unless a statement creates it.

Before you read on, write in the next cell whether a query for one dataset's readers will read every row of `edges`, or only that dataset's rows.

    [WRITE] Will the query read every row of edges, or only the dataset's rows?
    [WRITE] ........

    >>> tables = shop.store.tables(week24)
    >>> tables
           job  edge  dataset  runs      shop/build_clean_customers  reads  s3://shop-raw/customers.jsonl  7    shop/build_clean_customers  writes  warehouse://shop-warehouse/shop.analytics.clean_customers  7    shop/build_clean_orders  reads  s3://shop-raw/orders.jsonl  7    shop/build_clean_orders  writ

The next cell holds the query, as text, in `query`.

As it stands, the query has no `:dataset`, the name the check passes in for each dataset. The check takes that as no readers for any dataset, and finds 3 of 11 right: the 3 that no program reads.

Add a `WHERE` clause that keeps the rows whose `edge` is `reads` and whose `dataset` is `:dataset`. Select the cell and press **Run below**.

The check gets SQLite's own plan for the query. The plan shows whether the query reads the whole table or looks its rows up.

    >>> query = "SELECT job FROM edges"

    >>> shop.store.check(week24, tables, query)
      | dataset | yours | rows read | 
      | sales_dashboard |  | 14 | right
      | customers.jsonl |  | 14 | expected build_clean_customers
      | orders.jsonl |  | 14 | expected build_clean_orders
      | r-201.json |  | 14 | expected record_return
      | r-202.json |  | 14 | expected record_return
      | r-203.json |  | 14 | expected record_return
      | r-204.json |  | 14 | expected record_return
      | clean_customers |  | 14 | right
      | clean_orders |  | 14 | expected build_daily_sales
      | daily_sales |  | 14 | expected refresh_dashboard
      | returns |  | 14 | right

With the `WHERE` clause, the check finds 11 of 11 right. The query reads every row of `edges`: 154 rows, 14 for each of the 11 datasets.

The plan is a scan: SQLite reads each row and tests it against the `WHERE` clause.

Compare this with what you wrote.

## An index

The next cell drops the index `edges_index` if there is one, and creates it on the column `job` of `edges`.

Change `job` to the column your query looks up. Select the cell and press **Run below**: the check below it runs your query again.

    >>> tables.sql("DROP INDEX IF EXISTS edges_index")
    >>> tables.sql("CREATE INDEX edges_index ON edges(job)")

    >>> shop.store.check(week24, tables, query)
      | dataset | yours | rows read | 
      | sales_dashboard |  | 14 | right
      | customers.jsonl |  | 14 | expected build_clean_customers
      | orders.jsonl |  | 14 | expected build_clean_orders
      | r-201.json |  | 14 | expected record_return
      | r-202.json |  | 14 | expected record_return
      | r-203.json |  | 14 | expected record_return
      | r-204.json |  | 14 | expected record_return
      | clean_customers |  | 14 | right
      | clean_orders |  | 14 | expected build_daily_sales
      | daily_sales |  | 14 | expected refresh_dashboard
      | returns |  | 14 | right

With the index on `dataset`, the query reads 14 rows in all. That is, for each dataset, only that dataset's rows. The plan looks them up through the index, and the check names the index.

With the index on `job`, the plan stays a scan, because the query does not look up a job.

An index on `edge` is used too, but it narrows little: each search reads the 8 rows whose `edge` is `reads`, 88 in all.

## A graph

The fourth shape is a graph, as in Chapter 5: a node for each program and each dataset, and an edge for each edge by job.

`graph.edges_at(name)` gives the edges at one node, and the check counts each edge it gives.

The next cell defines `readers_of(graph, dataset)` for the graph. As it stands, it gives the job of every edge at the dataset's node, and the check finds 6 of 11 right.

Keep only the edges whose `edge` is `reads`. Select the cell and press **Run below**.

    >>> def readers_of(graph, dataset):
    >>>     return [e["job"] for e in graph.edges_at(dataset)]

    >>> shop.store.check(week24, shop.store.graph(week24), readers_of)
      | dataset | yours | read | 
      | sales_dashboard | refresh_dashboard | 1 | expected none
      | customers.jsonl | build_clean_customers | 1 | right
      | orders.jsonl | build_clean_orders | 1 | right
      | r-201.json | record_return | 1 | right
      | r-202.json | record_return | 1 | right
      | r-203.json | record_return | 1 | right
      | r-204.json | record_return | 1 | right
      | clean_customers | build_clean_customers | 1 | expected none
      | clean_orders | build_clean_orders, build_daily_sales | 2 | expected build_daily_sales
      | daily_sales | build_daily_sales, refresh_dashboard | 2 | expected refresh_dashboard
      | returns | record_return, remove_return | 2 | expected none

With that condition, the check finds 11 of 11 right, and reads 14 edges: for each dataset, the edges at its node.

For this question, over all 11 datasets: the documents read 187, the table with no index 154, the table with the index on `dataset` 14, and the graph 14.

These counts compare how many items each shape opens, not how big each item is.

The next cell asks each shape two questions, with the shop's own code: what reads `clean_orders`, and what `build_daily_sales` reads. The table has the index on `dataset`, and no index on `job`.

    >>> shop.store.compare(week24, "warehouse://shop-warehouse/shop.analytics.clean_orders", "shop/build_daily_sales")
      | question | documents | table with the index | graph
      | what reads clean_orders | 17 | 2 | 2
      | what build_daily_sales reads | 1 | 14 | 2

What reads `clean_orders`: 17 documents, 2 rows of the table, 2 edges of the graph.

What `build_daily_sales` reads: 1 document, 14 rows of the table, 2 edges of the graph.

The documents are kept one for each program, so a program's question opens 1 document and a dataset's question opens all 17.

The table's 14 rows for the program's question are a scan: the table has no index on `job`. The index on `dataset` serves the dataset's question only.

The graph keeps both ends of every edge, so each question reads only one node's edges: 2 here.

## A fast store

[BOX] The head of the shop's requirement: "The metadata store must be fast."

Before you read on, write in the next cell what "fast" means to you here.

    [WRITE] What does "fast" mean here?
    [WRITE] ........

"Fast" could mean several things:

- fast to find one program or dataset by its name: a key for each document, or a lookup by name. Finding `build_daily_sales` took 1 document.
- fast to find what reads a dataset: an index on `dataset`, or a graph. Each read 2 items for `clean_orders`.
- fast to follow lineage several steps: one node's edges at each step, as in Chapter 5's traversal. This chapter measured one step.
- fast to take each event as it arrives: this chapter did not measure writing.
- fast enough as the store grows: counts at a larger size, which Chapter 23 projected for other questions, and the time each takes, which this chapter did not measure.

Of the shapes here, the documents and the graph met the first reading. The table, with no index on `job`, did not. The table with the index on `dataset` and the graph met the second. The graph met the third, for one step. None was measured against the fourth or the fifth.

The requirement does not say which it means.

## Before Chapter 25

Four shapes answered the same question, and each passed the same check. Where the answer is kept decided how many items it read: in each program's document, every document; in a table with no index, every row; through an index on `dataset` or at a graph's node, only the dataset's own.

The check could not show the time each shape takes, or what each costs to write.

Chapter 25 builds the collector that receives the events the store is filled from.

- Which questions does your metadata store answer most often?
- Which of them read every item?
- Which structure would serve them, and which questions would it not?

### How this differs from a real platform

- The shop's store holds 14 edges. Chapter 23 projected other questions at 10,000,000 assets: the latest run of one job, one day's events, and what is downstream of one asset.
- The check counts items from SQLite's plan and from the shop's own counting, not from the time taken.
- Finding a document by name, a node, or a place in an index counts as nothing here. Chapter 23 counted about 30 steps down an index at 10,000,000 assets.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 23](chapter_23.ipynb) · [Next: Chapter 25](chapter_25.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

