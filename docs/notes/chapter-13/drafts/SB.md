## A

- Read what each run recorded while it ran.
- Measure how recent each asset is, two ways, after a night that failed.
- Find the nights that wrote nothing, and two clocks that disagree.
- Question the requirement "The dashboard must be fresh."

## C
## What each run recorded

A fact recorded about a run while it ran is an **observation**: when it started, how long it took, its status, the rows it read and wrote, the size of the table or file after the run, and any error.

The next cell lists the observations of the week's runs, from the shop's record of each run.

`size after (bytes)` is the size of the table or file as it stood after the run, not the bytes the run wrote. For a table it is the catalogue's estimate. The dashboard has no size.

The shop's events (Chapters 7 and 8) carry the times, the status and the row counts. They carry neither the size nor the error.

## D

28 runs. One failed: `run-027`, `build_daily_sales`, at 02:30 on Monday 14, after 21 seconds, with the error `database is locked`.

A failed run records no counts, so its count columns are blank. Blank is not 0: the record does not show how many rows it wrote.

`run-028`, `refresh_dashboard`, ran after it and succeeded: it read 6 rows of `daily_sales` and showed 6 days.

## E
## How recent each asset is

How recent an asset's data is, measured one way or another, is its **freshness**.

There are two measures: when the asset's store records it was last written; and the latest day its data holds.

The next cell lists both for each asset, and how many hours before 09:00 on Monday it was last written.

## F

By the time it was last written, the dashboard is the most recent of the four: 6.0 hours before 09:00 on Monday.

By the latest day it holds, the dashboard is a day behind. It holds Saturday 12, and on Monday the day before is Sunday 13. `daily_sales` holds the same latest day.

Compare these with what you wrote.

## H

The second and third readings are not met. The next cell shows each step of the second reading.

## J
## Nights that wrote nothing

Chapter 11's `renamed` change: from the export that runs early on Sunday 13, `orders.jsonl` has `qty` where it had `quantity`.

Before you read on, decide which of the three readings the dashboard will meet in this week.

The next cell lists the runs that wrote no rows. The cell after it tests the dashboard against the three readings.

## K

4 runs: `build_clean_orders` and `build_daily_sales`, on Sunday 13 and on Monday 14. Each succeeded.

`build_clean_orders` read 43 rows and then 48, and wrote 0 each time. On Saturday 12 it had written 31. A count of 0 stands out only beside the rows read and the counts of earlier nights.

Refreshed lately and built from the latest data are met. Showing the latest day is not. The dashboard's latest day is Friday 11, two days before Sunday 13.

By status and by time, the dashboard is up to date. By the rows written against earlier nights, and by its latest day, it is not.

## L
## Two clocks

The next cell runs the week with another change and shows each step of the second reading, by the times each store records.

## M

The reporting tool records the dashboard's last refresh at 02:20:09 on Monday. `daily_sales` was last written at 02:30:21. By these times the dashboard was refreshed before its input.

Was it? The next cell shows what the dashboard holds.

## MM

The dashboard shows Sunday 13 (`2026-09-13`). `daily_sales` held a row for Sunday 13 only from 02:30:21, so the refresh came after it.

In this week the reporting tool's clock runs 40 minutes slow: the `clock` change. Its times are 40 minutes early.

In the cell before the dashboard's, change `by="stores"` to `by="runs"`, select that cell and press **Run below**.

## MMM

With `by="runs"`, each time is when the last run that wrote the asset finished, by the one clock the shop's platform keeps for its runs. That includes the export, which sends no events. Its time is the platform's record of its run.

By that clock the refresh finished at 03:00:09, after `daily_sales` was written at 02:30:21.

The order holds only while one clock stamps every run. Where each machine keeps its own clock, two of them can disagree in the same way.

## N
## A table written at any hour

The returns desk writes the table `returns` whenever a return changes, at any hour.

Is `returns` up to date at 09:00 on Monday, and by which measure?

The next cell prints the time of the last change to the bucket `shop-returns`, then how recent each asset is in the week with the returns desk.

## O

`returns` was last written at 16:50:04 on Saturday 12, 40.2 hours before 09:00 on Monday. By the test that "refreshed lately" uses, written within a day, it is not up to date.

Its latest day, Friday 11, is when the latest return still in the table was made (`r-204`).

The bucket last changed at 16:50:00 on Saturday 12, when the desk deleted `r-203`. Nothing has changed since. The table was written 4 seconds later.

For a table written when its source changes, freshness is measured against the source's last change, not against the night.

## P
## Before Chapter 14

After the failed night, `daily_sales` and the dashboard held Saturday 12 as their latest day. By the time it was last written, the dashboard was the most recent asset. Compare these with what you wrote at the start.

"Refreshed lately" was met after the failed night, after the nights that wrote nothing, and with the slow clock. It caught neither fault. "Built from the latest data" failed after the failed night, and with the slow clock until one clock was used. "Showing the latest day" failed after the failed night and after the nights that wrote nothing. The requirement does not choose among them.

Observations recorded how each run went, the failed run's error included, and a count of 0 stood out against earlier nights. A table written at any hour was measured against its source.

Neither the observations nor the freshness measures show what the rows each run read held: how many orders had no customer id, or appeared twice.

Chapter 14, the first chapter of Part IV, records what each run finds in the rows it reads.

- What does your platform record about a run that succeeded and wrote nothing?
- Which clocks stamp the times your platform compares?
- Which of your tables are written when something changes, not on a schedule, and how would you say whether they are up to date?

## Q
### How this differs from a real platform

- The shop's runs, their times and their errors are invented for the course.
- OpenLineage defines a run facet, `errorMessage`, for a failed run's message, and the output dataset facet `outputStatistics` holds a row count and the size in bytes written. The shop's events carry the row counts, not the size or the error.
- The shop's size column is a table's or a file's size after the run, not the bytes the run wrote.
- The three readings, and the rule of a day for "refreshed lately", are the shop's own choices.
- The shop's reporting tool keeps its own clock, and in the `clock` change it runs slow. Every machine on a real platform keeps its own clock too.
