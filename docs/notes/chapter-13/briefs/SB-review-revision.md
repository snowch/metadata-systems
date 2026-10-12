# Brief SB: Chapter 13, "Runtime metadata", after its review

Read `docs/notes/chapter-10/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
brief SA's terms. A review found: a size column described as what a run wrote, though it is the
table's size after the run; the clock experiment stating its cause and its result before the reader
acted; a claim that every time came from the runs' events, though the export sends none; sentences
restating tables; blanks read as zeros; a section with no question in front of it; and a closing that
did not return to the reader's first answer. These slots replace paragraphs.

Words: do not say a number, a table or a record "says" anything; say what it shows or holds.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Read what each run recorded while it ran.
- Measure how recent each asset is, two ways, after a night that failed.
- Find the nights that wrote nothing, and two clocks that disagree.
- Question the requirement "The dashboard must be fresh."

### Slot C: under the heading `## What each run recorded`

- A fact recorded about a run while it ran is an **observation**: when it started, how long it took,
  its status, the rows it read and wrote, the size of the table or file it wrote, and any error.
- The next cell lists the observations of the week's runs, from the shop's record of each run.
- `size after (bytes)` is the size of the table or file as it stood after the run, not the bytes the
  run wrote; for a table it is the catalogue's estimate. The dashboard has none.
- The shop's events (Chapters 7 and 8) carry the times, the status and the row counts. They carry
  neither the size nor the error.

### Slot D: after that cell

- 28 runs. One failed: `run-027`, `build_daily_sales`, at 02:30 on Monday 14, after 21 seconds, with
  the error `database is locked`.
- A failed run records no counts, so its cells are empty. Empty is not 0: the record does not say
  how many rows it wrote.
- `run-028`, `refresh_dashboard`, ran after it and succeeded: it read 6 rows of `daily_sales` and
  showed 6 days.

### Slot E: under the heading `## How recent each asset is`

- How recent an asset's data is, measured one way or another, is its **freshness**.
- Two measures: when the asset's store records it was last written; and the latest day its data
  holds.
- The next cell lists both for each asset, and how many hours before 09:00 on Monday it was last
  written.

### Slot F: after that cell

- By the time it was last written, the dashboard is the most recent of the four: 6.0 hours before.
- By the latest day it holds, Saturday 12, it is a day behind: on Monday the day before is Sunday 13.
  `daily_sales` holds the same latest day.
- Compare these with what you wrote.

### Slot H: after the cell that tests the three readings

- The second and third readings are not met. The next cell shows each step of the second reading.

### Slot J: under the heading `## Nights that wrote nothing`

- Chapter 11's `renamed` change: from the export that runs early on Sunday 13, `orders.jsonl` has
  `qty` where it had `quantity`.
- Before you read on, decide which of the three readings the dashboard will meet in this week.
- The next cell lists the runs that wrote no rows. The cell after it tests the dashboard against the
  three readings.

### Slot K: after those two cells

- 4 runs: `build_clean_orders` and `build_daily_sales`, on Sunday 13 and on Monday 14. Each succeeded.
- `build_clean_orders` read 43 rows and then 48, and wrote 0 each time. On Saturday 12 it had
  written 31. A count of 0 stands out only beside the rows read and the counts of earlier nights.
- Refreshed lately and built from the latest data are met; showing the latest day is not. The
  dashboard's latest day is Friday 11, two days before Sunday 13.
- By status and by time, the dashboard is up to date. By the rows written against earlier nights,
  and by its latest day, it is not.

### Slot L: under the heading `## Two clocks`

- The next cell runs the week with another change and shows each step of the second reading, by the
  times each store records.

### Slot M: after that cell

- The reporting tool records the dashboard's last refresh at 02:20:09 on Monday. `daily_sales` was
  last written at 02:30:21. By these times the dashboard was refreshed before its input.
- Was it? The next cell shows what the dashboard holds.

### Slot MM: after that cell

- The dashboard shows Sunday 13 (`2026-09-13`). `daily_sales` held a row for Sunday 13 only from
  02:30:21, so the refresh came after it.
- In this week the reporting tool's clock runs 40 minutes slow: the `clock` change. Its times are
  40 minutes early.
- In the cell before the dashboard's, change `by="stores"` to `by="runs"`, select that cell and press
  **Run below**.

### Slot MMM: after slot MM, as its own paragraph group

- With `by="runs"`, each time is when the last run that wrote the asset finished, by the one clock the
  shop's platform keeps for its runs. That includes the export, which sends no events; its time is
  the platform's record of its run.
- By that clock the refresh finished at 03:00:09, after `daily_sales` was written at 02:30:21.
- The order holds only while one clock stamps every run. Where each machine keeps its own clock, two
  of them can disagree in the same way.

### Slot N: under the heading `## A table written at any hour`

- The returns desk writes the table `returns` whenever a return changes, at any hour.
- Is `returns` up to date at 09:00 on Monday, and by which measure?
- The next cell prints the time of the last change to the bucket `shop-returns`, then how recent each
  asset is in the week with the returns desk.

### Slot O: after that cell

- `returns` was last written at 16:50:04 on Saturday 12, 40.2 hours before 09:00 on Monday. By the
  test that "refreshed lately" uses, written within a day, it is not up to date.
- Its latest day, Friday 11, is when the latest return still in the table was made (`r-204`).
- The bucket last changed at 16:50:00 on Saturday 12, when the desk deleted `r-203`. Nothing has
  changed since. The table was written 4 seconds later.
- For a table written when its source changes, freshness is measured against the source's last
  change, not against the night.

### Slot P: under the heading `## Before Chapter 14`

- After the failed night, `daily_sales` and the dashboard held Saturday 12 as their latest day. By
  the time it was last written, the dashboard was the most recent asset. Compare these with what you
  wrote at the start.
- "Refreshed lately" was met after the failed night, after the nights that wrote nothing, and with
  the slow clock. It caught neither fault. "Built from the latest data" failed after the failed
  night, and with the slow clock until one clock was used. "Showing the latest day" failed after the
  failed night and after the nights that wrote nothing. The requirement does not choose among them.
- Observations recorded how each run went, the failed run's error included, and a count of 0 stood
  out against earlier nights. A table written at any hour was measured against its source.
- They could not show what the rows each run read held: how many orders had no customer id, or
  appeared twice.
- Chapter 14, the first chapter of Part IV, records what each run finds in the rows it reads.
- Then the same three reflective questions as now, as a Markdown list (keep their wording):
  - What does your platform record about a run that succeeded and wrote nothing?
  - Which clocks stamp the times your platform compares?
  - Which of your tables are written when something changes, not on a schedule, and how would you
    say whether they are up to date?

### Slot Q: under the heading `### How this differs from a real platform`

- The shop's runs, their times and their errors are invented for the course.
- OpenLineage defines a run facet, `errorMessage`, for a failed run's message, and the output dataset
  facet `outputStatistics` holds a row count and the size in bytes written. The shop's events carry
  the row counts, not the size or the error.
- The shop's size column is a table's or a file's size after the run, not the bytes the run wrote.
- The three readings, and the rule of a day for "refreshed lately", are the shop's own choices.
- The shop's reporting tool keeps its own clock, and in the `clock` change it runs slow. Every machine
  on a real platform keeps its own clock too.

Write slot Q as a Markdown list.

## Slots

Write the file `docs/notes/chapter-13/drafts/SB.md` with the slots under `## A`, `## C`, `## D`,
`## E`, `## F`, `## H`, `## J`, `## K`, `## L`, `## M`, `## MM`, `## MMM`, `## N`, `## O`, `## P` and
`## Q`, each the exact text to place, and nothing else in the file. Each slot that has a heading
starts with that heading.
