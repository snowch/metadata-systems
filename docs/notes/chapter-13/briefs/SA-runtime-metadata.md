# Brief SA: Chapter 13, "Runtime metadata"

Read `docs/notes/chapter-10/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms. The reader knows **column lineage** (Chapter 10), **schema evolution** and **breaking
change** (Chapter 11), and **environment**, **identity** and **qualified name** (Chapter 12). This
chapter introduces **observation** in slot C and **freshness** in slot E, each in bold once, and
neither before its slot (not in slot A, and not "observed", "observe", "fresh" or "stale" before its
slot either, except inside the head of the shop's requirement, which is quoted). Before slot E, say
"up to date". Words you must not use anywhere in this chapter: data quality, assertion, alias.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Read what each run recorded while it ran.
- Measure how recent each asset is, two ways, after a night that failed.
- Find a night that wrote nothing, and two clocks that disagree.
- Question the requirement "The dashboard must be fresh."

### Slot B: under the heading `## Monday after a failed night`

- The week with Chapter 2's failed night: on the last night, early on Monday 14, `build_daily_sales`
  fails and writes nothing. `refresh_dashboard` runs after it, as every night, and redraws the
  dashboard from `daily_sales`.
- The head of the shop's requirement: "The dashboard must be fresh."
- Before you read on, write in the next cell which of `orders.jsonl`, `clean_orders`, `daily_sales`
  and `sales_dashboard` you think are not up to date at 09:00 on Monday, and how you would tell.

### Slot BB: the text inside that cell (between triple quotes)

One question, then `........` on its own line: which assets are not up to date at 09:00 on Monday,
and how would you tell? At most about 60 characters a line. Plain text.

### Slot C: under the heading `## What each run recorded`

- A fact recorded about a run while it ran is an **observation**: when it started, how long it
  took, its status, the rows it read and wrote, the size in bytes of what it wrote, and any error.
- The next cell lists the observations of the week's runs.

### Slot D: after that cell

- 28 runs. One failed: `run-027`, `build_daily_sales`, at 02:30 on Monday 14, after 21 seconds, with
  the error `database is locked`. It wrote no rows.
- `run-028`, `refresh_dashboard`, ran after it and succeeded: it read 6 rows of `daily_sales` and
  showed 6 days.

### Slot E: under the heading `## How recent each asset is`

- How recent an asset's data is, by some measure, is its **freshness**.
- Two measures: when the asset's store says it was last written; and the latest day its data holds.
- The next cell lists both for each asset, and how many hours before 09:00 on Monday it was last
  written.

### Slot F: after that cell

- `orders.jsonl`: last written 8.0 hours before; latest day Sunday 13.
- `clean_orders`: 6.9 hours; Sunday 13.
- `daily_sales`: 30.5 hours; Saturday 12.
- `sales_dashboard`: 6.0 hours; Saturday 12.
- By the time it was last written, the dashboard is the most recent of the four. By the latest day
  it holds, it is a day behind.

Write slot F as a Markdown list of the four assets, then one short paragraph.

### Slot G: under the heading `## "The dashboard must be fresh."`

- "Fresh" could mean three things, each needing something different:
  - refreshed lately: the reporting tool's record of the last refresh;
  - built from the latest data: along the lineage that feeds the dashboard, each asset written
    after the asset it is made from, by the times their stores record;
  - showing the latest day: the latest day the dashboard shows, against the day before.
- The next cell tests the dashboard against all three.

Write slot G as one Markdown list of the three readings, then the sentence about the next cell.

### Slot H: after that cell

- Refreshed lately: met. Built from the latest data: not met. Showing the latest day: not met.
- The next cell shows each step of the second reading.

### Slot I: after that cell

- `daily_sales` was last written at 02:30:21 on Sunday 13, before `clean_orders` was, at 02:05:52 on
  Monday 14. It was not written after its input.
- Chapter 2's failed night met the first reading and neither of the others. The requirement does not
  say which it means.

### Slot J: under the heading `## A night that wrote nothing`

- Chapter 11's `renamed` change: from the export before Saturday's row, `orders.jsonl` has `qty`
  where it had `quantity`.
- The next cell lists the runs that wrote no rows. The cell after it tests the dashboard against the
  three readings.

### Slot K: after those two cells

- 4 runs: `build_clean_orders` and `build_daily_sales`, on Sunday 13 and on Monday 14. Each succeeded,
  with 0 rows written.
- Refreshed lately: met. Built from the latest data: met. Showing the latest day: not met.
- Every asset was written after its input, and the dashboard shows days up to Friday 11.
- The status and the times say the dashboard is up to date. The rows written and the latest day say
  it is not.

### Slot L: under the heading `## Two clocks`

- In the week with the `clock` change, the reporting tool's clock runs 40 minutes slow.
- The next cell shows each step of the second reading, by the times each store records.

### Slot M: after that cell

- The reporting tool records the dashboard's last refresh at 02:20:09 on Monday. `daily_sales` was
  last written at 02:30:21. By these times the dashboard was refreshed before its input, though it
  ran after it, and the second reading is not met.
- Change `by="stores"` to `by="runs"`, select the cell and press **Run below**. Every time then comes
  from the runs' events, which the shop's programs stamp by one clock. By them the refresh finished
  at 03:00:09, after `daily_sales` was written.

### Slot N: under the heading `## A table written at any hour`

- The returns desk writes the table `returns` whenever a return changes, at any hour.
- The next cell lists how recent each asset is in the week with the returns desk, then the time of
  the last change to the bucket `shop-returns`.

### Slot O: after that cell

- `returns` was last written at 16:50:04 on Saturday 12, 40.2 hours before 09:00 on Monday. A rule
  for the nightly tables, written within a day, says it is not up to date.
- The bucket last changed at 16:50:00 on Saturday 12, when the desk deleted `r-203`. Nothing has
  changed since. The table was written 4 seconds later.
- For a table written when its source changes, freshness is measured against the source's last
  change, not against the night.

### Slot P: under the heading `## Before Chapter 14`

- Showed: observations recorded how each run went: one failed with an error; four succeeded and
  wrote no rows. Freshness by the time of the last write and by the latest day disagreed after the
  failed night. "Fresh" had three readings, and the failed night met one. Two clocks reversed the
  order of two writes until every time came from the runs' events. A table written at any hour was
  measured against its source.
- Could not show: what the rows each run read held: how many orders had no customer id, or appeared
  twice.
- Next: Part IV starts. Chapter 14 records what each run finds in the rows it reads.
- Then three reflective questions, as a Markdown list:
  - What does your platform record about a run that succeeded and wrote nothing?
  - Which clocks stamp the times your platform compares?
  - Which of your tables are written when something changes, not on a schedule, and how would you
    say whether they are up to date?

### Slot Q: under the heading `### How this differs from a real platform`

- The shop's runs, their times and their errors are fixed in the course's code, so every number is
  the same on every machine.
- OpenLineage defines a run facet, `errorMessage`, for a failed run's message, and the
  `outputStatistics` facet holds a row count and a size in bytes. The shop's events send the row
  count only.
- The three readings, and the rule of a day for "refreshed lately", are the shop's own choices.
- The shop's reporting tool keeps its own clock, and in the `clock` change it runs slow. Every
  machine on a real platform keeps its own clock too.

## Slots

Write the file `docs/notes/chapter-13/drafts/SA.md` with the slots under `## A`, `## B`, `## BB`,
`## C`, `## D`, `## E`, `## F`, `## G`, `## H`, `## I`, `## J`, `## K`, `## L`, `## M`, `## N`,
`## O`, `## P` and `## Q`, each the exact text to place, and nothing else in the file. Each slot that
has a heading starts with that heading.
