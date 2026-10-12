[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 12](chapter_12.ipynb)

# Chapter 13: Runtime metadata

**Objectives**

- Read what each run recorded while it ran.
- Measure how recent each asset is, two ways, after a night that failed.
- Find a night that wrote nothing, and two clocks that disagree.
- Question the requirement "The dashboard must be fresh." 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 12's link, in a browser that had opened and run Chapter 12 (measured on a computer). Chapter 12's link opens this page in a new tab. Chapter 12 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 12 leaves more memory for this page.

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

A fact recorded about a run while it ran is an **observation**: when it started, how long it took, its status, the rows it read and wrote, the size in bytes of what it wrote, and any error.

The next cell lists the observations of the week's runs. 

```python
week13 = shop.run_week(["failed"])
shop.observe.observations(week13)
```

[output]
run | program | started | seconds | status | rows read | rows written | bytes | error | 
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

The week has 28 runs. One failed: `run-027`, `build_daily_sales`, at 02:30 on Monday 14, after 21 seconds, with the error `database is locked`. It wrote no rows.

`run-028`, `refresh_dashboard`, ran after it and succeeded: it read 6 rows of `daily_sales` and showed 6 days. 

## How recent each asset is

How recent an asset's data is, by some measure, is its **freshness**. There are two measures: when the asset's store says it was last written, and the latest day its data holds.

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

- `orders.jsonl`: last written 8.0 hours before; latest day Sunday 13.
- `clean_orders`: 6.9 hours; Sunday 13.
- `daily_sales`: 30.5 hours; Saturday 12.
- `sales_dashboard`: 6.0 hours; Saturday 12.

By the time it was last written, the dashboard is the most recent of the four. By the latest day it holds, it is a day behind. 

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

Refreshed lately: met. Built from the latest data: not met. Showing the latest day: not met.

The next cell shows each step of the second reading. 

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

## A night that wrote nothing

Chapter 11's `renamed` change: from the export before Saturday's row, `orders.jsonl` has `qty` where it had `quantity`.

The next cell lists the runs that wrote no rows. The cell after it tests the dashboard against the three readings. 

```python
week13r = shop.run_week(["renamed"])
shop.observe.observations(week13r, rows_written=0)
```

[output]
run | program | started | seconds | status | rows read | rows written | bytes | error | 
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

4 runs: `build_clean_orders` and `build_daily_sales`, on Sunday 13 and on Monday 14. Each succeeded, with 0 rows written.

Refreshed lately: met. Built from the latest data: met. Showing the latest day: not met.

Every asset was written after its input, and the dashboard shows days up to Friday 11.

The status and the times say the dashboard is up to date. The rows written and the latest day say it is not. 

## Two clocks

In the week with the `clock` change, the reporting tool's clock runs 40 minutes slow.

The next cell shows each step of the second reading, by the times each store records. 

```python
week13c = shop.run_week(["clock"])
shop.observe.chain(week13c, by="stores")
```

[output]
made | last written | from | which was last written | written after it | 
clean_orders | 2026-09-14T02:05:52Z | orders.jsonl | 2026-09-14T01:00:41Z | yes | 
daily_sales | 2026-09-14T02:30:21Z | clean_orders | 2026-09-14T02:05:52Z | yes | 
sales_dashboard | 2026-09-14T02:20:09Z | daily_sales | 2026-09-14T02:30:21Z | no |

The reporting tool records the dashboard's last refresh at 02:20:09 on Monday. `daily_sales` was last written at 02:30:21. By these times the dashboard was refreshed before its input, though it ran after it, and the second reading is not met.

Change `by="stores"` to `by="runs"`, select the cell and press **Run below**. Every time then comes from the runs' events, which the shop's programs stamp by one clock. By them the refresh finished at 03:00:09, after `daily_sales` was written. 

## A table written at any hour

The returns desk writes the table `returns` whenever a return changes, at any hour.

The next cell lists how recent each asset is in the week with the returns desk, then the time of the last change to the bucket `shop-returns`. 

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

`returns` was last written at 16:50:04 on Saturday 12, 40.2 hours before 09:00 on Monday. A rule for the nightly tables, written within a day, says it is not up to date.

The bucket last changed at 16:50:00 on Saturday 12, when the desk deleted `r-203`. Nothing has changed since. The table was written 4 seconds later.

For a table written when its source changes, freshness is measured against the source's last change, not against the night. 

## Before Chapter 14

Observations showed how each run went: one run failed with an error, and four succeeded and wrote no rows. Freshness, measured by the time of the last write and by the latest day, disagreed after the failed night. "Fresh" had three readings, and the failed night met one. Two clocks reversed the order of two writes until every time came from the runs' events. A table written at any hour was measured against its source.

The observations could not show what the rows each run read held: how many orders had no customer id, or appeared twice.

Next, Part IV starts. Chapter 14 records what each run finds in the rows it reads.

- What does your platform record about a run that succeeded and wrote nothing?
- Which clocks stamp the times your platform compares?
- Which of your tables are written when something changes, not on a schedule, and how would you say whether they are up to date? 

### How this differs from a real platform

The shop's runs, their times and their errors are fixed in the course's code, so every number is the same on every machine.

OpenLineage defines a run facet, `errorMessage`, for a failed run's message, and the `outputStatistics` facet holds a row count and a size in bytes. The shop's events send the row count only.

The three readings, and the rule of a day for "refreshed lately", are the shop's own choices.

The shop's reporting tool keeps its own clock, and in the `clock` change it runs slow. Every machine on a real platform keeps its own clock too.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 12](chapter_12.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

