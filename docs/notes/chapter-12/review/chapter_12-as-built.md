[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 11](chapter_11.ipynb) · [Next: Chapter 13](chapter_13.ipynb)

# Chapter 12: Identity

**Objectives**

- See a run on a copy of the shop's tables join the shop's own graph.
- Decide, for six pairs of names, whether each pair names the same asset, then test each pair.
- Change ingestion's rule for names, and see the two runs separate.
- Question the head of the shop's requirement about when two names are one table. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 11's link, in a browser that had opened and run Chapter 11 (measured on a computer). Chapter 11's link opens this page in a new tab. Chapter 11 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 11 leaves more memory for this page.

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

## A run in development

On Monday at 10:20 a developer tries a change to `build_daily_sales`. The developer does not run it on the shop's tables. The developer runs it on copies of `clean_orders` and `daily_sales` in a second database of the warehouse, `shop_dev`, which holds Sunday's orders.

A separate copy of the platform's data and programs, kept for one purpose, is an **environment**. Production holds the shop's real data and runs its real programs. Development is where changes are tried.

The developer's runner sends OpenLineage events, as the analyst's script did in Chapter 9. It names the tables `analytics.clean_orders` and `analytics.daily_sales`, without the database. Its jobs are in the namespace `dev`.

Before you read on, write in the next cell which programs you expect the graph to show writing `shop.analytics.daily_sales`, production's table.

The cell after it runs the week with the returns desk and the development run, and ingests the events as Chapter 9 did. 

```python
expected_writers = """
Which programs will the graph show
writing shop.analytics.daily_sales?
........
"""
```

```python
week12 = shop.run_week(["returns", "dev", "view"])
parsed = shop.ingest.parse(shop.ingest.event_lines(week12))
found = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(parsed)))
found.of("analytics.daily_sales")
```

[output]
job | edge | dataset | runs | first | last | 
shop/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 7 | 2026-09-08T02:30:21Z | 2026-09-14T02:30:21Z | 
shop/refresh_dashboard | reads | warehouse://shop-warehouse/shop.analytics.daily_sales | 7 | 2026-09-08T03:00:09Z | 2026-09-14T03:00:09Z | 
dev/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 1 | 2026-09-14T10:20:04Z | 2026-09-14T10:20:04Z |

The cell lists two programs that write `daily_sales`:

- `shop/build_daily_sales`, in 7 runs, the last at `2026-09-14T02:30:21Z`;
- `dev/build_daily_sales`, in 1 run, at `2026-09-14T10:20:04Z`.

Chapter 9's rule for names gave the developer's names `shop`, production's database.

The graph now records that a run in development wrote production's `daily_sales`, and was the last to write it. 

## The same asset?

What makes two names refer to the same asset is the asset's **identity**.

Six pairs of names, each used somewhere in the shop:

1. `shop.analytics.daily_sales`, in the jobs' events, and `SHOP.ANALYTICS.DAILY_SALES`, in a query Jo Marsh typed in capitals;
2. `daily_sales`, in the code of `refresh_dashboard`, and `shop.analytics.daily_sales`;
3. `shop.analytics.daily_sales` and `shop_dev.analytics.daily_sales`, the developer's table;
4. `shop.analytics.daily_sales` and `shop.analytics.sales_by_day`, a view Jo Marsh made over `daily_sales`: a name for a query, which holds no rows of its own;
5. `s3://shop-raw/orders.jsonl` and `s3://shop-raw/Orders.jsonl`, which the supplier wrote on Friday 11 to test a new export;
6. two versions of `s3://shop-returns/r-202.json`: as the desk created it on Wednesday 9, and as the desk overwrote it on Thursday 10.

Before you read on, write in the next cell, for each pair, whether the two names refer to the same asset: yes, no, or you cannot tell yet. 

```python
same_asset = """
Do the two names in each pair refer to the same asset?
1 ....
2 ....
3 ....
4 ....
5 ....
6 ....
"""
```

The next cell looks up what each name refers to in the store that holds it. 

```python
v1, v2 = [v["version"] for v in week12.storage.versions("s3://shop-returns/r-202.json")]
pairs = [
    ("shop.analytics.daily_sales", "SHOP.ANALYTICS.DAILY_SALES"),
    ("daily_sales", "shop.analytics.daily_sales"),
    ("shop.analytics.daily_sales", "shop_dev.analytics.daily_sales"),
    ("shop.analytics.daily_sales", "shop.analytics.sales_by_day"),
    ("s3://shop-raw/orders.jsonl", "s3://shop-raw/Orders.jsonl"),
    (f"s3://shop-returns/r-202.json@{v1}", f"s3://shop-returns/r-202.json@{v2}"),
]
shop.identity.references(week12, pairs)
```

[output]
pair | reference | names | 
1 | shop.analytics.daily_sales | shop.analytics.daily_sales | 
1 | SHOP.ANALYTICS.DAILY_SALES | shop.analytics.daily_sales | 
2 | daily_sales | shop.analytics.daily_sales | 
2 | shop.analytics.daily_sales | shop.analytics.daily_sales | 
3 | shop.analytics.daily_sales | shop.analytics.daily_sales | 
3 | shop_dev.analytics.daily_sales | shop_dev.analytics.daily_sales | 
4 | shop.analytics.daily_sales | shop.analytics.daily_sales | 
4 | shop.analytics.sales_by_day | shop.analytics.sales_by_day | 
5 | s3://shop-raw/orders.jsonl | s3://shop-raw/orders.jsonl | 
5 | s3://shop-raw/Orders.jsonl | s3://shop-raw/Orders.jsonl | 
6 | s3://shop-returns/r-202.json@dce9388ac585 | s3://shop-returns/r-202.json | 
6 | s3://shop-returns/r-202.json@68d7454802de | s3://shop-returns/r-202.json |

Pair 1: both refer to `shop.analytics.daily_sales`. The warehouse reads a name without regard to case.

Pair 5 names two objects. Object storage reads a key exactly, case included, and the supplier's test file, `s3://shop-raw/Orders.jsonl`, is there.

Pair 2: `daily_sales` refers to production's table because `refresh_dashboard` runs with production's defaults: the database `shop` and the schema `analytics`. The same code run in development would refer to `shop_dev.analytics.daily_sales`.

A name that holds everything its store needs to find the asset, with no defaults, is a **qualified name**: `shop.analytics.daily_sales`, or `s3://shop-raw/orders.jsonl`.

The next cell tests each pair five ways: the same text, the same object, the same rows, the same environment, and the same version. 

```python
shop.identity.compare(week12, pairs)
```

[output]
pair | same text | same object | same rows | same environment | same version | 
1 | no | yes | yes | yes |  | 
2 | no | yes | yes | yes |  | 
3 | no | no | no | no |  | 
4 | no | no | yes | yes |  | 
5 | no | no | no | yes | no | 
6 | no | yes | no | yes | no |

- Pairs 1 and 2: the same object, rows and environment.
- Pair 3: none of these.
- Pair 4: the same rows and environment, but not the same object.
- Pair 5: the same environment only.
- Pair 6: the same object and environment, but not the same rows or version.

The warehouse keeps no versions of a table, so the version test is empty for pairs 1 to 4. 

## "The same table must have one identity."

The head of the shop's requirement: "The same table must have one identity."

Before you read on, write in the next cell what "the same table" means to you. 

```python
same_table = """
What does "the same table" mean to you?
........
"""
```

"The same" could mean four things, each needing something different:

- The same name, once qualified and read by its store's rules: pairs 1, 2 and 6. It needs qualified names and each store's rules for case.
- The same rows: pairs 1, 2 and 4. It needs a way to compare contents.
- The same environment: pairs 1, 2, 4, 5 and 6. It needs to know which environment holds each asset.
- The same version: none of the pairs is shown to be. It needs versions, which the warehouse does not keep for a table.

The shop's ingestion joins two datasets when their namespace and name are the same, after it normalises them. That is the first reading. It compares names exactly, so it would keep pair 1 apart, which the warehouse reads as one table. Its rule for names joined pair 3, which no reading joins.

The requirement does not say which "same" it means. 

## A database for each producer

Chapter 9's rule gives `shop` to every name that leaves out its database.

The next cell normalises the events again with a database for each producer. As it stands, it lists none, so the cell gives the same answer as before.

Delete the `# ` at the start of the line that gives the developer's runner `shop_dev`, select the cell and press **Run below**. 

```python
databases = {}
# databases[shop.openlineage.DEV_PRODUCER] = "shop_dev"
parted = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(parsed, databases)))
parted.of("analytics.daily_sales")
```

[output]
job | edge | dataset | runs | first | last | 
shop/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 7 | 2026-09-08T02:30:21Z | 2026-09-14T02:30:21Z | 
shop/refresh_dashboard | reads | warehouse://shop-warehouse/shop.analytics.daily_sales | 7 | 2026-09-08T03:00:09Z | 2026-09-14T03:00:09Z | 
dev/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 1 | 2026-09-14T10:20:04Z | 2026-09-14T10:20:04Z |

After the change, `dev/build_daily_sales` writes `shop_dev.analytics.daily_sales`. `shop/build_daily_sales` is the only program that writes `shop.analytics.daily_sales`.

The rule now lives in ingestion, and it has to list each producer. A runner that sends qualified names needs no rule. 

## Before Chapter 13

A run in development joined production's graph, because a rule for names filled in production's database. Six pairs of names were tested five ways, and the tests disagreed. A view had the same rows as its table and was another object. Two versions were one object with different rows. A qualified name, read by its store's rules, found the object. The warehouse and object storage have different rules for case.

Nothing here shows whether the dashboard is up to date, or by which clock.

Chapter 13 records what each run did as it ran, and asks how recent each asset is.

- Which of your platform's programs name a table without its database?
- How would your lineage tell production's table from development's of the same name?
- Which pairs of names in your platform would you join, and by which reading? 

### How this differs from a real platform

The developer, the view and the supplier's test file are invented for the course.

The shop's rules for case are its own. Its warehouse reads names without regard to case, and its object storage reads keys exactly. Each real store has its own rules, set out in its own documentation.

OpenLineage's naming page gives a namespace for each kind of data store and a name inside it. For several warehouses, the name is `{database}.{schema}.{table}`.

OpenLineage's `symlinks` facet lists other names for one dataset, such as a file's location and the table name a catalogue gives it.

The shop's warehouse keeps no versions of a table. Some table formats keep a table's earlier states as snapshots.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 11](chapter_11.ipynb) · [Next: Chapter 13](chapter_13.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

