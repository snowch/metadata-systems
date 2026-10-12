[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 8](chapter_08.ipynb)

# Chapter 9: From events to graphs

**Objectives**

- Turn a week of received events into a graph, one stage at a time.
- Find what a line that cannot be read takes out of the graph.
- Give a stage a facet it does not know, and see what it adds.
- Question the requirement "The graph must show the current lineage." 

## From events to a graph

The shop's collector keeps every event it receives, each as one line of JSON, in the order it received them. The events come from the jobs, from the functions, and now from the analyst's script, which has sent its own since Chapter 8.

The head of the shop wants a graph of the platform kept up to date from these events, not drawn from lines written by hand as in Chapter 6.

Turning received events into stored records and graph edges is **ingestion**.

The shop's ingestion has four stages: parse, a stage that rewrites the events in one form, objects and edges. Each is a function you run and inspect. 

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them. 

[figure] The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table returns. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 8's link, in a browser that had opened and run Chapter 8 (measured on a computer). Chapter 8's link opens this page in a new tab. Chapter 8 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 8 leaves more memory for this page.

Running every cell took 9 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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

The next cell runs the week with the returns desk and the `source` change, in which `build_daily_sales` reads the analyst's copy from Saturday's row on. It collects the week's event lines, and prints how many there are and the start of the first. 

```python
week9 = shop.run_week(["returns", "source"])
lines = shop.ingest.event_lines(week9)
print(len(lines), "lines")
print(lines[0][:120], "...")
```

[output]
82 lines
{"eventType":"START","eventTime":"2026-09-08T02:00:00Z","run":{"runId":"01a07ebe-5d00-765e-a35b-340e90e9f837","facets":{ ...


## Parse

Parsing turns each line of text into an event. A line that is not JSON, or that breaks the specification's rules, is refused, with its line number and why.

The next cell cuts one line short, as if part of it were lost on the way: the COMPLETE of `build_daily_sales`'s run on Wednesday 9. It then parses every line and lists the lines refused. 

```python
damaged = list(lines)
k = next(i for i, line in enumerate(damaged) if '"build_daily_sales"' in line and '"COMPLETE"' in line and "2026-09-09" in line)
damaged[k] = damaged[k][:150]
parsed = shop.ingest.parse(damaged)
parsed.refused
```

[output]
line | problem | starts | 
20 | The line is not JSON. | {"eventType":"COMPLETE","eventTime":"202 |

The week has 82 lines. One is refused: line 20, which is not JSON. 81 events pass.

Before you read on, write in the next cell what the graph will lose because of that line. 

```python
expected_loss = """
What will the graph lose because of that line?
........
"""
```

## Normalise

Producers write the same thing in different ways. The functions' producer writes times with `+00:00`; the jobs' producer writes `Z`. Both mean UTC.

The analyst's script names `clean_orders` without its database: it writes `analytics.clean_orders`.

To **normalise** events is to rewrite such things in one form, so that the same thing is written the same way.

The shop's stage writes every time in UTC with `Z`, and adds the database `shop` to a warehouse name that leaves it out.

The next cell normalises the events and lists every change it made. 

```python
normal = shop.ingest.normalise(parsed)
normal.changes
```

[output]
line | where | before | after | 
5 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
6 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
11 | eventTime | 2026-09-08T14:20:02+00:00 | 2026-09-08T14:20:02Z | 
12 | eventTime | 2026-09-08T14:20:05+00:00 | 2026-09-08T14:20:05Z | 
17 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
18 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
23 | eventTime | 2026-09-09T10:05:02+00:00 | 2026-09-09T10:05:02Z | 
24 | eventTime | 2026-09-09T10:05:05+00:00 | 2026-09-09T10:05:05Z | 
25 | eventTime | 2026-09-09T15:40:02+00:00 | 2026-09-09T15:40:02Z | 
26 | eventTime | 2026-09-09T15:40:05+00:00 | 2026-09-09T15:40:05Z | 
31 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
32 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
37 | eventTime | 2026-09-10T09:30:02+00:00 | 2026-09-10T09:30:02Z | 
38 | eventTime | 2026-09-10T09:30:05+00:00 | 2026-09-10T09:30:05Z | 
43 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
44 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
49 | eventTime | 2026-09-11T13:15:02+00:00 | 2026-09-11T13:15:02Z | 
50 | eventTime | 2026-09-11T13:15:05+00:00 | 2026-09-11T13:15:05Z | 
55 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
56 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
61 | eventTime | 2026-09-12T16:50:02+00:00 | 2026-09-12T16:50:02Z | 
62 | eventTime | 2026-09-12T16:50:04+00:00 | 2026-09-12T16:50:04Z | 
67 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
68 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
77 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders | 
78 | inputs[0].name | analytics.clean_orders | shop.analytics.clean_orders |

The stage made 26 changes: 12 times, in the functions' events (6 runs, 2 events each), and 14 names, in the analyst's events (7 nights, 2 events each).

Without the change to the names, the analyst's copy would not join `clean_orders`, as in Chapter 8.

The rule for names is the shop's. It fits a warehouse with one database; where two databases hold tables of the same name, it would join tables that are not the same. 

## Objects

The next stage makes jobs, runs and datasets from the events. A run's state is the type of its latest event, by time.

It reads fields only from the facets it knows: `nominalTime`, `jobType`, `sourceCodeLocation`, `inputStatistics`, `outputStatistics` and `version`. It lists any other facet and does not read it.

The next cell builds the objects and shows how many of each it made. 

```python
known = dict(shop.ingest.KNOWN)
# known["shop_objectChange"] = ["object", "version", "change"]
objs = shop.ingest.objects(normal, known)
objs
```

[output]
jobs | runs | datasets | unknown facets | 
7 | 41 | 12 | 6 |

The stage made 7 jobs (the four jobs, the two functions and the analyst's copy), 41 runs and 12 datasets. It also found 6 facets it does not know.

The next cell lists the runs whose latest event is a START. 

```python
objs.runs_of(state="START")
```

[output]
job | state | started | ended | reads | writes | nominalTime.nominalStartTime | jobType.processingType | jobType.jobType | sourceCodeLocation.version | 
shop/build_daily_sales | START | 2026-09-09T02:30:00Z |  | warehouse://shop-warehouse/shop.analytics.clean_orders |  | 2026-09-09T02:30:00Z | BATCH | JOB | 256e271 |

One run is `build_daily_sales` on Wednesday 9. Its COMPLETE was the line cut short. To the stage, the run looks as though it is still working. 

## A facet the stage does not know

The next cell lists the facets the stage does not know. The cell after it lists the runs of `record_return`: when each started, what it read, and the change and the version from the facet `shop_objectChange`. 

```python
objs.unknown
```

[output]
run | job | facet | 
01a08163-e250-708e-8668-33dd3646cb78 | shop/record_return | shop_objectChange | 
01a085a0-c8b0-7635-9397-47861beda0ce | shop/record_return | shop_objectChange | 
01a086d3-7c50-707d-819f-a9513347c345 | shop/record_return | shop_objectChange | 
01a08aa7-1990-7ea9-bdbd-49a662107171 | shop/record_return | shop_objectChange | 
01a0909b-73f0-7e13-b94e-8fdada3806db | shop/record_return | shop_objectChange | 
01a09686-a690-729f-afb9-f1d592416ebe | shop/remove_return | shop_objectChange |

```python
objs.runs_of("shop/record_return", columns=["started", "reads", "shop_objectChange.change", "shop_objectChange.version"])
```

[output]
started | reads | 
2026-09-08T14:20:02Z | s3://shop-returns/r-201.json | 
2026-09-09T10:05:02Z | s3://shop-returns/r-202.json | 
2026-09-09T15:40:02Z | s3://shop-returns/r-203.json | 
2026-09-10T09:30:02Z | s3://shop-returns/r-202.json | 
2026-09-11T13:15:02Z | s3://shop-returns/r-204.json |

All 6 are `shop_objectChange`, on the runs of the two functions. The table of `record_return`'s runs shows when each started and what it read, and no change or version: the stage did not read the facet.

In the cell that starts `known = dict(`, delete the `# ` at the start of the line `known["shop_objectChange"] = ...`, select that cell and press **Run below**.

The stage then knows the facet. The list of facets it does not know is empty, and each run of `record_return` shows whether its file was created or overwritten, and its version. 

## Edges

The last stage makes edges. For each run, one edge to each dataset the run read or wrote. For each job, the same edge once, with how many runs had it, and the first and last time one did.

The week has 41 runs over 7 nights.

Before you read on, write in the next cell how many edges between jobs and datasets you expect, and why: about as many as one night's reads and writes, or about seven times as many. 

```python
expected_edges = """
How many edges between jobs and datasets, and why?
........
"""
```

```python
found = shop.ingest.edges(objs)
found
```

[output]
run edges | job edges | 
80 | 17 |

There are 80 edges by run and 17 by job.

Each night's runs repeat the same reads and writes, so they add edges by run and not edges by job. An edge by job counts its runs instead.

The functions add an edge by job for each file `record_return` read.

The next cell lists the edges of `build_daily_sales`. 

```python
found.of("shop/build_daily_sales")
```

[output]
job | edge | dataset | runs | first | last | 
shop/build_daily_sales | reads | warehouse://shop-warehouse/shop.analytics.clean_orders | 5 | 2026-09-08T02:30:21Z | 2026-09-12T02:30:21Z | 
shop/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 6 | 2026-09-08T02:30:21Z | 2026-09-14T02:30:21Z | 
shop/build_daily_sales | reads | s3://shop-scratch/clean_orders_copy.csv | 2 | 2026-09-13T02:30:21Z | 2026-09-14T02:30:21Z |

`build_daily_sales` has 3 edges. It reads `clean_orders` in 5 runs, the first at `2026-09-08T02:30:21Z` and the last at `2026-09-12T02:30:21Z`. It reads the analyst's copy in 2 runs, on Sunday 13 and Monday 14. It writes `daily_sales` in 6 runs.

It counts 6 runs, not 7, because the COMPLETE of Wednesday's run was the line cut short, so to the graph that run wrote nothing.

The edge to `daily_sales` stays, because other runs had it. Only its count of runs, and the missing edge for Wednesday's run, show the loss.

The next cell draws the edges by job, in the order data flows, as Chapter 6's drawing did. 

```python
found.graph().drawing(label="orders.jsonl goes through build_clean_orders to shop.analytics.clean_orders, which copy_clean_orders reads to write clean_orders_copy.csv, and which build_daily_sales reads as well as the copy, to write shop.analytics.daily_sales, which refresh_dashboard reads to write sales_dashboard. Four return files are read by record_return, which with remove_return writes shop.analytics.returns; customers.jsonl goes through build_clean_customers to shop.analytics.clean_customers.")
```

[output]
[image: orders.jsonl goes through build_clean_orders to shop.analytics.clean_orders, which copy_clean_orders reads to write clean_orders_copy.csv, and which build_daily_sales reads as well as the copy, to write shop.analytics.daily_sales, which refresh_dashboard reads to write sales_dashboard. Four return files are read by record_return, which with remove_return writes shop.analytics.returns; customers.jsonl goes through build_clean_customers to shop.analytics.clean_customers.]

## "The graph must show the current lineage."

The head of the shop's requirement reads: "The graph must show the current lineage."

Before you read on, write in the next cell what "current" means to you.

The cell after it lists, for each job, the edges its latest run had. 

```python
reading = """
What does "current" mean to you?
........
"""
```

```python
found.latest()
```

[output]
job | edge | dataset | runs | first | last | 
shop/build_clean_customers | reads | s3://shop-raw/customers.jsonl | 7 | 2026-09-08T02:00:38Z | 2026-09-14T02:00:38Z | 
shop/build_clean_customers | writes | warehouse://shop-warehouse/shop.analytics.clean_customers | 7 | 2026-09-08T02:00:38Z | 2026-09-14T02:00:38Z | 
shop/build_clean_orders | reads | s3://shop-raw/orders.jsonl | 7 | 2026-09-08T02:05:52Z | 2026-09-14T02:05:52Z | 
shop/build_clean_orders | writes | warehouse://shop-warehouse/shop.analytics.clean_orders | 7 | 2026-09-08T02:05:52Z | 2026-09-14T02:05:52Z | 
analyst/copy_clean_orders | reads | warehouse://shop-warehouse/shop.analytics.clean_orders | 7 | 2026-09-08T02:15:17Z | 2026-09-14T02:15:17Z | 
analyst/copy_clean_orders | writes | s3://shop-scratch/clean_orders_copy.csv | 7 | 2026-09-08T02:15:17Z | 2026-09-14T02:15:17Z | 
shop/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 6 | 2026-09-08T02:30:21Z | 2026-09-14T02:30:21Z | 
shop/refresh_dashboard | reads | warehouse://shop-warehouse/shop.analytics.daily_sales | 7 | 2026-09-08T03:00:09Z | 2026-09-14T03:00:09Z | 
shop/refresh_dashboard | writes | reporting://shop-reporting/sales_dashboard | 7 | 2026-09-08T03:00:09Z | 2026-09-14T03:00:09Z | 
shop/record_return | writes | warehouse://shop-warehouse/shop.analytics.returns | 5 | 2026-09-08T14:20:05Z | 2026-09-11T13:15:05Z | 
shop/record_return | reads | s3://shop-returns/r-204.json | 1 | 2026-09-11T13:15:05Z | 2026-09-11T13:15:05Z | 
shop/remove_return | writes | warehouse://shop-warehouse/shop.analytics.returns | 1 | 2026-09-12T16:50:04Z | 2026-09-12T16:50:04Z | 
shop/build_daily_sales | reads | s3://shop-scratch/clean_orders_copy.csv | 2 | 2026-09-13T02:30:21Z | 2026-09-14T02:30:21Z |

Counting each job's latest run only, 13 of the 17 edges by job remain. Four are dropped: `build_daily_sales` reads `clean_orders` (its last such run was on Saturday 12), and `record_return` reads `r-201.json`, `r-202.json` and `r-203.json` (its latest run read `r-204.json` only).

"Current" could mean three things, each needing something different:

- as of the last event received: every edge received so far, all 17, so `build_daily_sales` reads both `clean_orders` and the copy;
- as of each job's latest run: the 13 edges. That drops `clean_orders` for `build_daily_sales`, as the code since Saturday does. For `record_return` it also drops `r-201.json` and `r-202.json`, whose rows are still in the table `returns`;
- as of the last change to a job's code: the edges of the runs since the code changed. That needs the code version of each run, which the stage keeps from `sourceCodeLocation`.

The edges by job keep the first and last time, so a query can choose. The requirement does not say which "current" it means. 

## Before Chapter 10

Four stages turned the week's events into a graph. A line cut short was refused at the first stage; its run then looked as though it were still working, and the edge to `daily_sales` counted 6 runs, not 7. Normalising joined the analyst's names to the jobs'. A facet the stage did not know was listed and not read, until you added it. The same reads and writes, night after night, made 80 edges by run and 17 by job. "Current" had three readings.

The events do not show which columns each column is made from. Chapter 6 noted that `revenue_pence` is made from `price_pence` and `quantity`; no event here says so.

Chapter 10 reads the jobs' SQL to find which columns each column is made from.

- What does a platform you work on do with an event it cannot read?
- Which two producers on that platform might name one table differently, and which rule would join them?
- Which reading of "current" does your own team need, and for what? 

### How this differs from a real platform

The shop, its collector and its four stages are the course's own. Every rule in them is the shop's choice: the forms it normalises to, a run's state from its latest event, and the facets it reads.

Here the week's events are made at once, after the week has run. A real collector receives them one at a time, over a network, while the jobs run.

Chapter 29 compares how real consumers store events.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 8](chapter_08.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

