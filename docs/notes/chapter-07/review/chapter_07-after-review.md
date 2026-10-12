[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 6](chapter_06.ipynb) · [Next: Chapter 8](chapter_08.ipynb)

# Chapter 7: Jobs, runs and events

**Objectives**

- Find what the lines from Chapter 6 and the warehouse cannot say about each night.
- Design the messages a program sends as it works, and put each time it works on one row.
- Tell apart two times one program worked on the same day.
- Question the requirement "Record every run." 

## How many orders, each night

In Chapter 6 you told Jo Marsh that `build_clean_orders` leaves out orders with no customer id when it writes `clean_orders`.

Jo asks:

> How many orders did it leave out, and on which nights? 

The three systems, in the order data moves through them each night. 

[figure] The shop's three systems and what each holds. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 6's link, in a browser that had opened and run Chapter 6 (measured on a computer). Chapter 6's link opens this page in a new tab. Chapter 6 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 6 leaves more memory for this page.

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

The two cells below the next one show what the shop already holds about this: Chapter 6's two lines for `build_clean_orders`, and what the warehouse records about `clean_orders`.

Before you read on, write in the next cell what they can tell you about the orders `build_clean_orders` left out each night. 

```python
expected = """
What can the two lines and the warehouse tell you
about the orders left out each night?
........
"""
```

```python
lines = shop.typed_records("""
job build_clean_orders reads: s3://shop-raw/orders.jsonl
job build_clean_orders writes: clean_orders
""")
lines
```

[output]
line | type | identifier | attribute | value | 
1 | job | build_clean_orders | reads | s3://shop-raw/orders.jsonl | 
2 | job | build_clean_orders | writes | clean_orders |

```python
warehouse.sql("SELECT table_name, row_count, last_altered FROM information_schema.tables WHERE table_name = 'clean_orders'")
```

[output]
table_name | row_count | last_altered | 
clean_orders | 44 | 2026-09-14T02:05:52Z |

The lines say what the job reads and what it writes. They do not say when it did its work, or how many rows it read or wrote.

The warehouse records that `clean_orders` has 44 rows and was last written at `2026-09-14T02:05:52Z`. That is the work of the last night only.

Each night, `build_clean_orders` replaces the whole table. Nothing on the platform records what the job did on an earlier night. 

## Events

The head of the shop has agreed to change the shop's programs. From now on, each one sends a message when it starts and another when it finishes.

Such a message is an **event**.

One time a program does its work, from its start to its finish, is a **run**. Its two events describe the run.

Which fields the events carry is your design.

The export and the analyst's copy send no events: their code is not in the shop's repository.

The next cell lists the fields the shop's programs can fill in: which event carries each (the start, the finish, or both), and what each holds. 

```python
shop.event_fields()
```

[output]
field | sent at | holds | 
run | both | an identifier the program makes when it starts and repeats in each event of the run | 
job | both | the program's name in the shop's repository | 
type | both | start or finish | 
time | both | when the program sent the event, in UTC | 
status | finish | succeeded or failed | 
code_version | start | the first seven characters of a hash of the program's code | 
reads | start | what the program is about to read | 
writes | finish | what the program wrote | 
rows_read | finish | how many rows the program read | 
rows_written | finish | how many rows the program wrote or removed | 
object | start | for a program started by a change to a file, that file | 
object_version | start | the identifier object storage gave that version of the file | 
object_change | start | created, overwritten or deleted |

The next cell holds a first design for Jo's question: `job`, `type`, `time`, `rows_read` and `rows_written`.

A design is a Python list of field names. To change it, edit the list.

The cell makes the week's events with those fields only, and lists those of `build_clean_orders`. 

```python
design = ["job", "type", "time", "rows_read", "rows_written"]
events = shop.events(week, design)
events.where(job="build_clean_orders")
```

[output]
job | type | time | rows_read | rows_written | 
build_clean_orders | start | 2026-09-08T02:05:00Z |  |  | 
build_clean_orders | finish | 2026-09-08T02:05:52Z | 6 | 6 | 
build_clean_orders | start | 2026-09-09T02:05:00Z |  |  | 
build_clean_orders | finish | 2026-09-09T02:05:52Z | 13 | 13 | 
build_clean_orders | start | 2026-09-10T02:05:00Z |  |  | 
build_clean_orders | finish | 2026-09-10T02:05:52Z | 20 | 19 | 
build_clean_orders | start | 2026-09-11T02:05:00Z |  |  | 
build_clean_orders | finish | 2026-09-11T02:05:52Z | 27 | 23 | 
build_clean_orders | start | 2026-09-12T02:05:00Z |  |  | 
build_clean_orders | finish | 2026-09-12T02:05:52Z | 35 | 31 | 
build_clean_orders | start | 2026-09-13T02:05:00Z |  |  | 
build_clean_orders | finish | 2026-09-13T02:05:52Z | 43 | 39 | 
build_clean_orders | start | 2026-09-14T02:05:00Z |  |  | 
build_clean_orders | finish | 2026-09-14T02:05:52Z | 48 | 44 |

`build_clean_orders` sent 14 events: a start and a finish on each of the 7 nights.

The start carries no row counts; the finish carries both.

The next cell puts each night's two events on one row by grouping them by `job` and `day`. A `day` is the UTC date of an event's `time`. 

```python
shop.runs(events.where(job="build_clean_orders"), by=["job", "day"])
```

[output]
job | day | events | started | finished | rows_read | rows_written | 
build_clean_orders | 2026-09-08 | 2 | 2026-09-08T02:05:00Z | 2026-09-08T02:05:52Z | 6 | 6 | 
build_clean_orders | 2026-09-09 | 2 | 2026-09-09T02:05:00Z | 2026-09-09T02:05:52Z | 13 | 13 | 
build_clean_orders | 2026-09-10 | 2 | 2026-09-10T02:05:00Z | 2026-09-10T02:05:52Z | 20 | 19 | 
build_clean_orders | 2026-09-11 | 2 | 2026-09-11T02:05:00Z | 2026-09-11T02:05:52Z | 27 | 23 | 
build_clean_orders | 2026-09-12 | 2 | 2026-09-12T02:05:00Z | 2026-09-12T02:05:52Z | 35 | 31 | 
build_clean_orders | 2026-09-13 | 2 | 2026-09-13T02:05:00Z | 2026-09-13T02:05:52Z | 43 | 39 | 
build_clean_orders | 2026-09-14 | 2 | 2026-09-14T02:05:00Z | 2026-09-14T02:05:52Z | 48 | 44 |

Each row is one night: the rows read and the rows written, from the run on Tuesday 8 to the run on Monday 14.

Rows read minus rows written gives the rows left out: 0, 0, 1, 4, 4, 4 and 4.

Each night the job rebuilds the table from every order so far, so the count for a night includes the rows left out on earlier nights. The run on Thursday 10 left out 1. The run on Friday 11, which read the orders up to Thursday, left out 3 more. After it, the count stays at 4.

That is what the events show: how many rows each run left out, and that the count of rows left out rose by 3 on Friday 11. They do not say which orders, or why.

Which orders comes from earlier chapters. The 1 is the export's second copy of order 7015, which Chapter 2's rules keep once. The 3 are Thursday's 3 orders with no customer id.

For Jo, the answer is 3 orders, all placed on Thursday, left out from the run on Friday 11 onwards. 

## Telling runs apart

The shop also has a returns desk. It keeps each return as one small file in the bucket `shop-returns`, written at any hour of the day.

Creating a return's file, or overwriting it with a correction, starts a program called `record_return`, which writes the return's row in a table, `returns`.

Deleting the file, when a return is withdrawn, starts `remove_return`, which removes the row.

A program that starts when something happens, here a change to a file, and not on a schedule, is a function. Both functions are in the repository and send events as the jobs do.

The figure below shows the platform with the returns desk on Monday morning: three return files in object storage, and the table `returns` in the warehouse. 

[figure] The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table returns. 

The next cell runs the week with the returns desk and groups `record_return`'s events by `job` and `day`. Its design adds `object` and `object_change`.

On Wednesday 9 the desk created 2 returns: `r-202` at 10:05 and `r-203` at 15:40.

Before you read on, write in the next cell what the grouping will show for Wednesday 9: how many rows, and how many times `record_return` did its work. 

```python
expected_wednesday = """
How many rows will the grouping show for Wednesday 9,
and why?
........
"""
```

```python
returns_week = shop.run_week(["returns"])
design_for_returns = ["job", "type", "time", "rows_read", "rows_written", "object", "object_change"]
returns_events = shop.events(returns_week, design_for_returns)
shop.runs(returns_events.where(job="record_return"), by=["job", "day"])
```

[output]
job | day | events | started | finished | rows_read | rows_written | object | object_change | 
record_return | 2026-09-08 | 2 | 2026-09-08T14:20:02Z | 2026-09-08T14:20:05Z | 1 | 1 | s3://shop-returns/r-201.json | created | 
record_return | 2026-09-09 | 4 | 2026-09-09T10:05:02Z | 2026-09-09T15:40:05Z | 2 | 2 | s3://shop-returns/r-202.json, s3://shop-returns/r-203.json | created | 
record_return | 2026-09-10 | 2 | 2026-09-10T09:30:02Z | 2026-09-10T09:30:05Z | 1 | 1 | s3://shop-returns/r-202.json | overwritten | 
record_return | 2026-09-11 | 2 | 2026-09-11T13:15:02Z | 2026-09-11T13:15:05Z | 1 | 1 | s3://shop-returns/r-204.json | created |

Wednesday 9 shows 1 row with 4 events, 2 objects (`r-202.json` and `r-203.json`), 2 rows read and 2 written, starting at `10:05:02` and finishing at `15:40:05`. The 2 runs of `record_return` were merged into one row.

Grouping by `job` and `day` worked for the jobs because each job does its work once a night. Grouping by `job` and `day` tells runs apart only for a program that does its work at most once a day.

`time` does not tell them apart either: a run's start and its finish have different times. Pairing each start with the next finish works on Wednesday, because the 2 runs did not overlap. It fails when 2 runs of one program overlap, or when a run never sends its finish.

What ties the events of one run together is `run`: an identifier the program makes when it starts and repeats in each event it sends.

The next cell adds `run` and `object_version` to the design, groups the events by `run`, and lists the runs of both functions. 

```python
with_run = design_for_returns + ["run", "object_version"]
returns_runs = shop.runs(shop.events(returns_week, with_run), by=["run"])
returns_runs.where(job=["record_return", "remove_return"])
```

[output]
run | events | job | started | finished | rows_read | rows_written | object | object_change | object_version | 
run-005 | 2 | record_return | 2026-09-08T14:20:02Z | 2026-09-08T14:20:05Z | 1 | 1 | s3://shop-returns/r-201.json | created | db9924f28dfe | 
run-010 | 2 | record_return | 2026-09-09T10:05:02Z | 2026-09-09T10:05:05Z | 1 | 1 | s3://shop-returns/r-202.json | created | dce9388ac585 | 
run-011 | 2 | record_return | 2026-09-09T15:40:02Z | 2026-09-09T15:40:05Z | 1 | 1 | s3://shop-returns/r-203.json | created | 3eda8083818e | 
run-016 | 2 | record_return | 2026-09-10T09:30:02Z | 2026-09-10T09:30:05Z | 1 | 1 | s3://shop-returns/r-202.json | overwritten | 68d7454802de | 
run-021 | 2 | record_return | 2026-09-11T13:15:02Z | 2026-09-11T13:15:05Z | 1 | 1 | s3://shop-returns/r-204.json | created | 7a928ca23ccc | 
run-026 | 2 | remove_return | 2026-09-12T16:50:02Z | 2026-09-12T16:50:04Z | 0 | 1 | s3://shop-returns/r-203.json | deleted | 5cfe9d0e2392 |

There are 6 runs of the two functions, one for each change to a return's file.

`record_return` ran twice for `r-202`: once when it was created, on Wednesday 9, and once when it was overwritten, on Thursday 10. Each run has its own `object_version`.

Without `object_version`, nothing would say which version of the file each run read.

`remove_return` ran once, for `r-203`, deleted on Saturday 12. It read 0 rows: the file was gone when it started. 

## What each run read

Chapter 6 left a question: with the `source` change, on which nights did `build_daily_sales` read `clean_orders`, and on which did it read the analyst's copy? The code shows only what the job does now.

The next cell runs the week with the returns desk and the `source` change. Its design is `run`, `job`, `type`, `time`, `reads` and `code_version`. It lists the runs of `build_daily_sales` and of `remove_return`. 

```python
changed = shop.run_week(["returns", "source"])
with_reads = ["run", "job", "type", "time", "reads", "code_version"]
shop.runs(shop.events(changed, with_reads), by=["run"]).where(job=["build_daily_sales", "remove_return"])
```

[output]
run | events | job | started | finished | reads | code_version | 
run-003 | 2 | build_daily_sales | 2026-09-08T02:30:00Z | 2026-09-08T02:30:21Z | clean_orders | 256e271 | 
run-008 | 2 | build_daily_sales | 2026-09-09T02:30:00Z | 2026-09-09T02:30:21Z | clean_orders | 256e271 | 
run-014 | 2 | build_daily_sales | 2026-09-10T02:30:00Z | 2026-09-10T02:30:21Z | clean_orders | 256e271 | 
run-019 | 2 | build_daily_sales | 2026-09-11T02:30:00Z | 2026-09-11T02:30:21Z | clean_orders | 256e271 | 
run-024 | 2 | build_daily_sales | 2026-09-12T02:30:00Z | 2026-09-12T02:30:21Z | clean_orders | 256e271 | 
run-026 | 2 | remove_return | 2026-09-12T16:50:02Z | 2026-09-12T16:50:04Z |  | cb19d8c | 
run-029 | 2 | build_daily_sales | 2026-09-13T02:30:00Z | 2026-09-13T02:30:21Z | s3://shop-scratch/clean_orders_copy.csv | c715bde | 
run-033 | 2 | build_daily_sales | 2026-09-14T02:30:00Z | 2026-09-14T02:30:21Z | s3://shop-scratch/clean_orders_copy.csv | c715bde |

The runs on Tuesday 8 to Saturday 12 read `clean_orders`, with code version `256e271`.

The runs on Sunday 13 and Monday 14 read `s3://shop-scratch/clean_orders_copy.csv`, with code version `c715bde`.

Chapter 6's change took effect from Saturday's row. The run on Sunday 13, early in the morning, writes Saturday's row, so it is the first run that reads the copy.

The events record what each run read when it ran. The code in the repository shows only what the job does now.

The run of `remove_return` on Saturday 12 has an empty `reads`: the file it removed was gone when it started, and it read nothing.

The next cell makes a graph from what each run read and wrote in the week with no changes, as Chapter 6 made one from its lines, and follows edges upstream from `sales_dashboard`. Its events carry `run`, `job`, `type`, `reads` and `writes`.

Before you read on, write in the next cell what that traversal would reach if the events carried no `reads`. 

```python
expected_without_reads = """
What would the traversal reach if the events
carried no `reads`?
........
"""
```

```python
lineage = shop.lineage(shop.runs(shop.events(week, ["run", "job", "type", "reads", "writes"])))
lineage.upstream("sales_dashboard")
```

[output]
node | type | steps | path | 
refresh_dashboard | job | 1 | sales_dashboard <-writes- refresh_dashboard | 
daily_sales | dataset | 2 | sales_dashboard <-writes- refresh_dashboard -reads-> daily_sales | 
build_daily_sales | job | 3 | sales_dashboard <-writes- refresh_dashboard -reads-> daily_sales <-writes- build_daily_sales | 
clean_orders | dataset | 4 | sales_dashboard <-writes- refresh_dashboard -reads-> daily_sales <-writes- build_daily_sales -reads-> clean_orders | 
build_clean_orders | job | 5 | sales_dashboard <-writes- refresh_dashboard -reads-> daily_sales <-writes- build_daily_sales -reads-> clean_orders <-writes- build_clean_orders | 
s3://shop-raw/orders.jsonl | dataset | 6 | sales_dashboard <-writes- refresh_dashboard -reads-> daily_sales <-writes- build_daily_sales -reads-> clean_orders <-writes- build_clean_orders -reads-> s3://shop-raw/orders.jsonl |

With `reads`, the traversal reaches 6 nodes, back to `orders.jsonl`.

Delete `"reads"` from the list in the cell above, select that cell and press **Run below**.

Without `reads`, the traversal reaches only `refresh_dashboard`. The graph shows no input for `daily_sales`, or for anything else.

A run that read nothing, as `remove_return`'s did, also gives the graph no input. From the graph, a run that read nothing and a run whose events left `reads` out look the same.

Put `"reads"` back and press **Run below** again. 

## "Record every run."

The head of the shop sets a requirement: "Record every run."

Before you read on, change the list `yours` in the next cell to the fields you would record, write what you take the requirement to mean where the cell shows `........`, select the cell and press **Run below**.

The cell sets your design against four readings of the requirement, and says which it meets. 

```python
yours = ["run", "job", "type", "time", "status"]
meaning = """
What does "Record every run." mean to you?
........
"""
shop.readings(yours)
```

[output]
reading | needs | missing | met | 
find the runs that failed | run, status |  | yes | 
know when each asset was last written | time, writes | writes | no | 
know which version of the code each run used | run, code_version | code_version | no | 
know which object change started a run | run, object, object_version, object_change | object, object_version, object_change | no |

The table sets your design against 4 readings. Each needs its own fields, which the table lists.

As the cell first stands, `yours` holds `run`, `job`, `type`, `time` and `status`, and meets the first reading only.

As written, a design meets "Record every run." if each run sends events and the events keep each run apart. That needs `run`: without it, 2 runs of one function on one day became one row.

Which of the readings a design meets depends on its fields. A field's name does not say which reading it serves: `time` is when an event was sent, not when the data was written. 

## Before Chapter 8

Chapter 6's lines and the warehouse could not say what each night did. Events grouped into runs gave Jo the count, 3 orders, left out from the run on Friday 11. Earlier chapters said which orders. Grouping by `job` and `day` merged 2 runs of `record_return` on Wednesday 9, and `run` told them apart. The runs showed which nights `build_daily_sales` read the analyst's copy. Without `reads`, the graph showed no input for `daily_sales`, as it shows none for a run that read nothing.

The experiments could not show how a program the shop did not write would know what each field means.

Chapter 8 writes the same runs in the form an open standard sets, which programs written elsewhere can read.

- What does a platform you work on record about each time a job does its work?
- In your design, which events exist for a program that stops before it finishes?
- What should a run of a function record when a file is deleted and then created again with the same name? 

### How this differs from a real platform

The shop, its people, its programs and its returns desk are invented for the course. The fields and their names are the course's own.

The shop numbers its runs in time order (`run-001`, `run-002`, and so on). A real program makes its own identifier when it starts.

Here each change to a return's file starts its function exactly once, in order. Chapters 19 and 20 take up changes whose functions start twice, or in another order.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 6](chapter_06.ipynb) · [Next: Chapter 8](chapter_08.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

