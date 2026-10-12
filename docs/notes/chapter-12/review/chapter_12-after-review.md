[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 11](chapter_11.ipynb) · [Next: Chapter 13](chapter_13.ipynb)

# Chapter 12: Identity

**Objectives**

- See a run in a second database of the warehouse join the shop's own graph.
- Decide, for six pairs of names, whether each pair names the same asset, then test each pair.
- Question the head of the shop's requirement about when two names are one table.
- Change ingestion's rule for names, and see the two runs part. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 11's link, in a browser that had opened and run Chapter 11 (measured on a computer). Chapter 11's link opens this page in a new tab. Chapter 11 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 11 leaves more memory for this page.

Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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

On Monday at 10:20 a developer tries a change to `build_daily_sales`. The developer does not run it on the shop's tables. The developer runs it in a second database of the warehouse, `shop_dev`. That database holds tables with the same names and columns as `clean_orders` and `daily_sales`, and Sunday's orders are in `clean_orders`.

A separate set of the platform's data and programs, kept for one purpose, is an **environment**. Production holds the shop's real data and runs its real programs. Development is where changes are tried.

The developer's runner sends OpenLineage events, as the analyst's script did in Chapter 9. Its events name the tables `analytics.clean_orders` and `analytics.daily_sales`, without the database. Its jobs are in the namespace `dev`.

Chapter 9's ingestion gives `shop`, the production database, to a warehouse name that leaves out its database.

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

The graph lists two programs that write `shop.analytics.daily_sales`:

- `shop/build_daily_sales`, in 7 runs, the last at `2026-09-14T02:30:21Z`;
- `dev/build_daily_sales`, in 1 run, at `2026-09-14T10:20:04Z`.

The graph now shows that a run in development wrote production's `daily_sales`, and was the last to write it. 

## The same asset?

What makes two names refer to the same asset is the asset's **identity**.

Six pairs of names, each used somewhere in the shop:

1. `shop.analytics.daily_sales`, in the jobs' events, and `SHOP.ANALYTICS.DAILY_SALES`, in a query Jo Marsh typed in capitals;
2. `daily_sales`, in the code of `refresh_dashboard`, and `shop.analytics.daily_sales`;
3. `shop.analytics.daily_sales` and `shop_dev.analytics.daily_sales`, the same table name in the development database;
4. `shop.analytics.daily_sales` and `shop.analytics.sales_by_day`, a view Jo Marsh made over `daily_sales`;
5. `s3://shop-raw/orders.jsonl` and `s3://shop-raw/Orders.jsonl`, which the supplier wrote on Friday 11 to test a new export;
6. two versions of `s3://shop-returns/r-202.json`: as the desk created it on Wednesday 9, and as it was overwritten on Thursday 10. In the next cells, `@` followed by a version names one version of an object.

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

In pair 1, both names refer to `shop.analytics.daily_sales`. The warehouse reads a name without regard to case.

In pair 5, the names refer to two objects. Object storage reads a key exactly, case included, and the supplier's test file is there.

In pair 2, `daily_sales` refers to production's table, because `refresh_dashboard` runs with production's defaults: the database `shop` and the schema `analytics`, a group of tables inside the database, as Chapter 8 named it. The same code run in development would refer to `shop_dev.analytics.daily_sales`.

In pair 4, a view is a name for a query. `sales_by_day` holds no rows of its own and shows those of `daily_sales`.

A name that holds everything its store needs to find the asset, with no defaults, is a **qualified name**: `shop.analytics.daily_sales`, or `s3://shop-raw/orders.jsonl`. 

## "The same table must have one identity."

The head of the shop's requirement is: "The same table must have one identity."

Before you read on, write in the next cell what "the same table" means to you. 

```python
same_table = """
What does "the same table" mean to you?
........
"""
```

"The same" could mean four things, each needing something different:

- the same name, once qualified and read by its store's rules: qualified names and each store's rules for case;
- the same rows: a way to compare contents;
- the same environment: which environment holds each asset;
- the same version: a version for each asset.

The next cell tests each pair five ways, starting with the plain text of the names:

- same text: the two names as written;
- same object: what each store says the name refers to;
- same rows: the rows of a table, or the contents of an object;
- same environment: from the database, `shop` for production and `shop_dev` for development; the shop's object storage has one environment, production;
- same version: the object's version; the warehouse keeps no versions of a table, so the test is empty for a table. 

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

No pair has the same text, yet pairs 1 and 2 are the same object, with the same rows and environment.

"Same asset?" depends on the test. Pair 4 has the same rows and environment, but is another object. Pair 6 is one object, but not the same rows or version. For pairs like these, "cannot tell yet" was a fair answer until "same" had a meaning.

By reading, against what the shop's graph holds:

- The same name: met in part. Ingestion qualifies a name that leaves out its database, then compares names exactly. It would keep pair 1 apart, which the warehouse reads as one table. It gave the developer's `analytics.daily_sales` the production database, as with pair 2 but with the wrong default, and so joined two tables that no reading joins.
- The same rows: not met. The graph compares no rows.
- The same environment: not met. The graph records no environment for an asset.
- The same version: not met for a table. The warehouse keeps no versions of a table.

The requirement does not say which "same" it means. 

## A database for each producer

The next cell normalises the events again with a database for each producer. As it stands, it lists no producers, so it gives the same answer as before.

Delete the `# ` at the start of the line that gives the developer's runner `shop_dev`. Before you press **Run below**, decide what `dev/build_daily_sales` will write. Then select the cell and press **Run below**. 

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

After the change, `dev/build_daily_sales` writes `shop_dev.analytics.daily_sales`, and `shop/build_daily_sales` is the only program that writes `shop.analytics.daily_sales`.

Only a producer whose names mean another database needs a line. Any other gets `shop`.

The rule ties a database to a producer, which is code, not an environment: the same runner used in production would get `shop_dev` too. A runner that sends qualified names needs no rule. 

## Before Chapter 13

A run in development joined production's graph, because ingestion filled in production's database for a name that left it out. Six pairs of names were tested, and the tests disagreed: a view had the same rows as its table and was another object; two versions were one object with different rows. A qualified name, read by its store's rules, found the object; the warehouse and object storage have different rules for case.

The shop's graph records no environment for an asset, compares no rows, and keeps no versions of a table, so most readings of "the same" cannot be met from it.

Chapter 13 turns from what an asset is to how recent it is: it records what each run did as it ran.

- Which of your platform's programs name a table without its database?
- How would your lineage tell production's table from development's of the same name?
- Which pairs of names in your platform would you join, and by which reading? 

### How this differs from a real platform

- The developer, the view, Jo Marsh's query in capitals and the supplier's test file are invented for the course.
- The shop's rules for case are its own: its warehouse reads names without regard to case, and its object storage reads keys exactly. Each real store has its own rules, set out in its own documentation.
- OpenLineage's naming page gives a namespace for each kind of data store and a name inside it; for several warehouses, the name is `{database}.{schema}.{table}`.
- OpenLineage's `symlinks` facet lists alternative identifiers for one dataset, such as a physical location and a logical table name.
- The shop's warehouse keeps no versions of a table. Some table formats keep a table's earlier states as snapshots.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 11](chapter_11.ipynb) · [Next: Chapter 13](chapter_13.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

