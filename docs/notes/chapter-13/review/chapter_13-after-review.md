[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 12](chapter_12.ipynb)

# Chapter 13: Runtime metadata

**Objectives**

- Read what each run recorded while it ran.
- Measure how recent each asset is, two ways, after a night that failed.
- Find the nights that wrote nothing, and two clocks that disagree.
- Question the requirement "The dashboard must be fresh." 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 12's link, in a browser that had opened and run Chapter 12 (measured on a computer). Chapter 12's link opens this page in a new tab. Chapter 12 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 12 leaves more memory for this page.

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

## Monday after a failed night

- The week is Chapter 2's, with its failed night: on the last night, early on Monday 14, `build_daily_sales` fails and writes nothing. `refresh_dashboard` runs after it, as every night, and redraws the dashboard from `daily_sales`.
- The head of the shop's requirement: "The dashboard must be fresh."
- Before you read on, write in the next cell which of `orders.jsonl`, `clean_orders`, `daily_sales` and `sales_dashboard` you think are not up to date at 09:00 on Monday, and how you would tell. 

```python
expected_stale = """
Which assets are not up to date at 09:00 on Monday,
and how would you tell?
........
"""
```

## What each run recorded

A fact recorded about a run while it ran is an **observation**: when it started, how long it took, its status, the rows it read and wrote, the size of the table or file after the run, and any error.

The next cell lists the observations of the week's runs, from the shop's record of each run.

`size after (bytes)` is the size of the table or file as it stood after the run, not the bytes the run wrote. For a table it is the catalogue's estimate. The dashboard has no size.

The shop's events (Chapters 7 and 8) carry the times, the status and the row counts. They carry neither the size nor the error. 

```python
week13 = shop.run_week(["failed"])
shop.observe.observations(week13)
```

[output]
run | program | started | seconds | status | rows read | rows written | size after (bytes) | error | 
run-001 | build_clean_customers | 2026-09-08T02:00:00Z | 38 | succeeded | 10 | 9 | 1463 |  | 
run-002 | build_clean_orders | 2026-09-08T02:05:00Z | 52 | succeeded | 6 | 6 | 1446 |  | 
run-003 | build_daily_sales | 2026-09-08T02:30:00Z | 21 | succeeded | 6 | 1 | 662 |  | 
run-004 | refresh_dashboard | 2026-09-08T03:00:00Z | 9 | succeeded | 1 | 1 |  |  | 
run-005 | build_clean_customers | 2026-09-09T02:00:00Z | 38 | succeeded | 10 | 9 | 1463 |  | 
run-006 | build_clean_orders | 2026-09-09T02:05:00Z | 52 | succeeded | 13 | 13 | 2013 |  | 
run-007 | build_daily_sales | 2026-09-09T02:30:00Z | 21 | succeeded | 13 | 1 | 684 |  | 
run-008 | refresh_dashboard | 2026-09-09T03:00:00Z | 9 | succeeded | 2 | 2 |  |  | 
run-009 | build_clean_customers | 2026-09-10T02:00:00Z | 38 | succeeded | 10 | 9 | 1463 |  | 
run-010 | build_clean_orders | 2026-09-10T02:05:00Z | 52 | succeeded | 20 | 19 | 2499 |  | 
run-011 | build_daily_sales | 2026-09-10T02:30:00Z | 21 | succeeded | 19 | 1 | 706 |  | 
run-012 | refresh_dashboard | 2026-09-10T03:00:00Z | 9 | succeeded | 3 | 3 |  |  | 
run-013 | build_clean_customers | 2026-09-11T02:00:00Z | 38 | succeeded | 10 | 9 | 1463 |  | 
run-014 | build_clean_orders | 2026-09-11T02:05:00Z | 52 | succeeded | 27 | 23 | 2823 |  | 
run-015 | build_daily_sales | 2026-09-11T02:30:00Z | 21 | succeeded | 23 | 1 | 728 |  | 
run-016 | refresh_dashboard | 2026-09-11T03:00:00Z | 9 | succeeded | 4 | 4 |  |  | 
run-017 | build_clean_customers | 2026-09-12T02:00:00Z | 38 | succeeded | 10 | 9 | 1463 |  | 
run-018 | build_clean_orders | 2026-09-12T02:05:00Z | 52 | succeeded | 35 | 31 | 3471 |  | 
run-019 | build_daily_sales | 2026-09-12T02:30:00Z | 21 | succeeded | 31 | 1 | 750 |  | 
run-020 | refresh_dashboard | 2026-09-12T03:00:00Z | 9 | succeeded | 5 | 5 |  |  | 
run-021 | build_clean_customers | 2026-09-13T02:00:00Z | 38 | succeeded | 10 | 9 | 1463 |  | 
run-022 | build_clean_orders | 2026-09-13T02:05:00Z | 52 | succeeded | 43 | 39 | 4119 |  | 
run-023 | build_daily_sales | 2026-09-13T02:30:00Z | 21 | succeeded | 39 | 1 | 772 |  | 
run-024 | refresh_dashboard | 2026-09-13T03:00:00Z | 9 | succeeded | 6 | 6 |  |  | 
run-025 | build_clean_customers | 2026-09-14T02:00:00Z | 38 | succeeded | 10 | 9 | 1463 |  | 
run-026 | build_clean_orders | 2026-09-14T02:05:00Z | 52 | succeeded | 48 | 44 | 4524 |  | 
run-027 | build_daily_sales | 2026-09-14T02:30:00Z | 21 | failed |  |  |  | database is locked | 
run-028 | refresh_dashboard | 2026-09-14T03:00:00Z | 9 | succeeded | 6 | 6 |  |  |

28 runs. One failed: `run-027`, `build_daily_sales`, at 02:30 on Monday 14, after 21 seconds, with the error `database is locked`.

A failed run records no counts, so its count columns are blank. Blank is not 0: the record does not show how many rows it wrote.

`run-028`, `refresh_dashboard`, ran after it and succeeded: it read 6 rows of `daily_sales` and showed 6 days. 

## How recent each asset is

How recent an asset's data is, measured one way or another, is its **freshness**.

There are two measures: when the asset's store records it was last written; and the latest day its data holds.

The next cell lists both for each asset, and how many hours before 09:00 on Monday it was last written. 

```python
shop.observe.freshness(week13)
```

[output]
asset | last written | hours before | latest day | 
orders.jsonl | 2026-09-14T01:00:41Z | 8.0 | 2026-09-13 | 
clean_orders | 2026-09-14T02:05:52Z | 6.9 | 2026-09-13 | 
daily_sales | 2026-09-13T02:30:21Z | 30.5 | 2026-09-12 | 
sales_dashboard | 2026-09-14T03:00:09Z | 6.0 | 2026-09-12 |

By the time it was last written, the dashboard is the most recent of the four: 6.0 hours before 09:00 on Monday.

By the latest day it holds, the dashboard is a day behind. It holds Saturday 12, and on Monday the day before is Sunday 13. `daily_sales` holds the same latest day.

Compare these with what you wrote. 

## "The dashboard must be fresh."

"Fresh" could mean three things, each needing something different:

- refreshed lately: the reporting tool's record of the last refresh;
- built from the latest data: along the lineage that feeds the dashboard, each asset written after the asset it is made from, by the times their stores record;
- showing the latest day: the latest day the dashboard shows, against the day before.

The next cell tests the dashboard against all three. 

```python
shop.observe.readings(week13)
```

[output]
reading | test | met | 
refreshed lately | last refreshed 2026-09-14T03:00:09Z, within a day | yes | 
built from the latest data | each asset feeding it written after its input | no | 
showing the latest day | latest day shown 2026-09-12, the day before is 2026-09-13 | no |

The second and third readings are not met. The next cell shows each step of the second reading. 

```python
shop.observe.chain(week13)
```

[output]
made | last written | from | which was last written | written after it | 
clean_orders | 2026-09-14T02:05:52Z | orders.jsonl | 2026-09-14T01:00:41Z | yes | 
daily_sales | 2026-09-13T02:30:21Z | clean_orders | 2026-09-14T02:05:52Z | no | 
sales_dashboard | 2026-09-14T03:00:09Z | daily_sales | 2026-09-13T02:30:21Z | yes |

`daily_sales` was last written at 02:30:21 on Sunday 13, before `clean_orders` was, at 02:05:52 on Monday 14. It was not written after its input.

Chapter 2's failed night met the first reading and neither of the others. The requirement does not say which it means. 

## Nights that wrote nothing

Chapter 11's `renamed` change: from the export that runs early on Sunday 13, `orders.jsonl` has `qty` where it had `quantity`.

Before you read on, decide which of the three readings the dashboard will meet in this week.

The next cell lists the runs that wrote no rows. The cell after it tests the dashboard against the three readings. 

```python
week13r = shop.run_week(["renamed"])
shop.observe.observations(week13r, rows_written=0)
```

[output]
run | program | started | seconds | status | rows read | rows written | size after (bytes) | error | 
run-022 | build_clean_orders | 2026-09-13T02:05:00Z | 52 | succeeded | 43 | 0 | 960 |  | 
run-023 | build_daily_sales | 2026-09-13T02:30:00Z | 21 | succeeded | 0 | 0 | 750 |  | 
run-026 | build_clean_orders | 2026-09-14T02:05:00Z | 52 | succeeded | 48 | 0 | 960 |  | 
run-027 | build_daily_sales | 2026-09-14T02:30:00Z | 21 | succeeded | 0 | 0 | 750 |  |

```python
shop.observe.readings(week13r)
```

[output]
reading | test | met | 
refreshed lately | last refreshed 2026-09-14T03:00:09Z, within a day | yes | 
built from the latest data | each asset feeding it written after its input | yes | 
showing the latest day | latest day shown 2026-09-11, the day before is 2026-09-13 | no |

4 runs: `build_clean_orders` and `build_daily_sales`, on Sunday 13 and on Monday 14. Each succeeded.

`build_clean_orders` read 43 rows and then 48, and wrote 0 each time. On Saturday 12 it had written 31. A count of 0 stands out only beside the rows read and the counts of earlier nights.

Refreshed lately and built from the latest data are met. Showing the latest day is not. The dashboard's latest day is Friday 11, two days before Sunday 13.

By status and by time, the dashboard is up to date. By the rows written against earlier nights, and by its latest day, it is not. 

## Two clocks

The next cell runs the week with another change and shows each step of the second reading, by the times each store records. 

```python
week13c = shop.run_week(["clock"])
shop.observe.chain(week13c, by="stores")
```

[output]
made | last written | from | which was last written | written after it | 
clean_orders | 2026-09-14T02:05:52Z | orders.jsonl | 2026-09-14T01:00:41Z | yes | 
daily_sales | 2026-09-14T02:30:21Z | clean_orders | 2026-09-14T02:05:52Z | yes | 
sales_dashboard | 2026-09-14T02:20:09Z | daily_sales | 2026-09-14T02:30:21Z | no |

The reporting tool records the dashboard's last refresh at 02:20:09 on Monday. `daily_sales` was last written at 02:30:21. By these times the dashboard was refreshed before its input.

Was it? The next cell shows what the dashboard holds. 

```python
week13c.reporting.dashboard()
```

[output]
name | sales_dashboard | 
title | Sales, last 7 days | 
created_by | j.marsh | 
created | 2026-09-02T15:41:00Z | 
last_refreshed | 2026-09-14T02:20:09Z | 
values | day: 2026-09-07, revenue: £147.00; day: 2026-09-08, revenue: £162.25; day: 2026-09-09, revenue: £153.75; day: 2026-09-10, revenue: £51.50; day: 2026-09-11, revenue: £204.24; day: 2026-09-12, revenue: £191.49; day: 2026-09-13, revenue: £97.75 |

The dashboard shows Sunday 13 (`2026-09-13`). `daily_sales` held a row for Sunday 13 only from 02:30:21, so the refresh came after it.

In this week the reporting tool's clock runs 40 minutes slow: the `clock` change. Its times are 40 minutes early.

In the cell before the dashboard's, change `by="stores"` to `by="runs"`, select that cell and press **Run below**. 

With `by="runs"`, each time is when the last run that wrote the asset finished, by the one clock the shop's platform keeps for its runs. That includes the export, which sends no events. Its time is the platform's record of its run.

By that clock the refresh finished at 03:00:09, after `daily_sales` was written at 02:30:21.

The order holds only while one clock stamps every run. Where each machine keeps its own clock, two of them can disagree in the same way. 

## A table written at any hour

The returns desk writes the table `returns` whenever a return changes, at any hour.

Is `returns` up to date at 09:00 on Monday, and by which measure?

The next cell prints the time of the last change to the bucket `shop-returns`, then how recent each asset is in the week with the returns desk. 

```python
week13d = shop.run_week(["returns"])
print("last change to shop-returns:", shop.observe.source_changed(week13d))
shop.observe.freshness(week13d)
```

[output]
last change to shop-returns: 2026-09-12T16:50:00Z


[output]
asset | last written | hours before | latest day | 
orders.jsonl | 2026-09-14T01:00:41Z | 8.0 | 2026-09-13 | 
clean_orders | 2026-09-14T02:05:52Z | 6.9 | 2026-09-13 | 
daily_sales | 2026-09-14T02:30:21Z | 6.5 | 2026-09-13 | 
sales_dashboard | 2026-09-14T03:00:09Z | 6.0 | 2026-09-13 | 
returns | 2026-09-12T16:50:04Z | 40.2 | 2026-09-11 |

`returns` was last written at 16:50:04 on Saturday 12, 40.2 hours before 09:00 on Monday. By the test that "refreshed lately" uses, written within a day, it is not up to date.

Its latest day, Friday 11, is when the latest return still in the table was made (`r-204`).

The bucket last changed at 16:50:00 on Saturday 12, when the desk deleted `r-203`. Nothing has changed since. The table was written 4 seconds later.

For a table written when its source changes, freshness is measured against the source's last change, not against the night. 

## Before Chapter 14

After the failed night, `daily_sales` and the dashboard held Saturday 12 as their latest day. By the time it was last written, the dashboard was the most recent asset. Compare these with what you wrote at the start.

"Refreshed lately" was met after the failed night, after the nights that wrote nothing, and with the slow clock. It caught neither fault. "Built from the latest data" failed after the failed night, and with the slow clock until one clock was used. "Showing the latest day" failed after the failed night and after the nights that wrote nothing. The requirement does not choose among them.

Observations recorded how each run went, the failed run's error included, and a count of 0 stood out against earlier nights. A table written at any hour was measured against its source.

Neither the observations nor the freshness measures show what the rows each run read held: how many orders had no customer id, or appeared twice.

Chapter 14, the first chapter of Part IV, records what each run finds in the rows it reads.

- What does your platform record about a run that succeeded and wrote nothing?
- Which clocks stamp the times your platform compares?
- Which of your tables are written when something changes, not on a schedule, and how would you say whether they are up to date? 

### How this differs from a real platform

- The shop's runs, their times and their errors are invented for the course.
- OpenLineage defines a run facet, `errorMessage`, for a failed run's message, and the output dataset facet `outputStatistics` holds a row count and the size in bytes written. The shop's events carry the row counts, not the size or the error.
- The shop's size column is a table's or a file's size after the run, not the bytes the run wrote.
- The three readings, and the rule of a day for "refreshed lately", are the shop's own choices.
- The shop's reporting tool keeps its own clock, and in the `clock` change it runs slow. Every machine on a real platform keeps its own clock too.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 12](chapter_12.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

