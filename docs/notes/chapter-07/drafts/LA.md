## E

The lines say what the job reads and what it writes. They do not say when it did its work, or how many rows it read or wrote.

The warehouse records that `clean_orders` has 44 rows and was last written at `2026-09-14T02:05:52Z`. That is the work of the last night only.

Each night, `build_clean_orders` replaces the whole table. Nothing on the platform records what the job did on an earlier night.

## I

Each row is one night: the rows read and the rows written, from the run on Tuesday 8 to the run on Monday 14.

Rows read minus rows written gives the rows left out: 0, 0, 1, 4, 4, 4 and 4.

Each night the job rebuilds the table from every order so far, so the count for a night includes the rows left out on earlier nights. The run on Thursday 10 left out 1. The run on Friday 11, which read the orders up to Thursday, left out 3 more. After it, the count stays at 4.

That is what the events show: how many rows each run left out, and that the count of rows left out rose by 3 on Friday 11. They do not say which orders, or why.

Which orders comes from earlier chapters. The 1 is the export's second copy of order 7015, which Chapter 2's rules keep once. The 3 are Thursday's 3 orders with no customer id.

For Jo, the answer is 3 orders, all placed on Thursday, left out from the run on Friday 11 onwards.

## K

The next cell runs the week with the returns desk and groups `record_return`'s events by `job` and `day`. Its design adds `object` and `object_change`.

On Wednesday 9 the desk created 2 returns: `r-202` at 10:05 and `r-203` at 15:40.

Before you read on, write in the next cell what the grouping will show for Wednesday 9: how many rows, and how many times `record_return` did its work.

## M

Wednesday 9 shows 1 row with 4 events, 2 objects (`r-202.json` and `r-203.json`), 2 rows read and 2 written, starting at `10:05:02` and finishing at `15:40:05`. The 2 runs of `record_return` were merged into one row.

Grouping by `job` and `day` worked for the jobs because each job does its work once a night. Grouping by `job` and `day` tells runs apart only for a program that does its work at most once a day.

`time` does not tell them apart either: a run's start and its finish have different times. Pairing each start with the next finish works on Wednesday, because the 2 runs did not overlap. It fails when 2 runs of one program overlap, or when a run never sends its finish.

What ties the events of one run together is `run`: an identifier the program makes when it starts and repeats in each event it sends.

The next cell adds `run` and `object_version` to the design, groups the events by `run`, and lists the runs of both functions.

## O

## What each run read

Chapter 6 left a question: with the `source` change, on which nights did `build_daily_sales` read `clean_orders`, and on which did it read the analyst's copy? The code shows only what the job does now.

The next cell runs the week with the returns desk and the `source` change. Its design is `run`, `job`, `type`, `time`, `reads` and `code_version`. It lists the runs of `build_daily_sales` and of `remove_return`.

## P

The runs on Tuesday 8 to Saturday 12 read `clean_orders`, with code version `256e271`.

The runs on Sunday 13 and Monday 14 read `s3://shop-scratch/clean_orders_copy.csv`, with code version `c715bde`.

Chapter 6's change took effect from Saturday's row. The run on Sunday 13, early in the morning, writes Saturday's row, so it is the first run that reads the copy.

The events record what each run read when it ran. The code in the repository shows only what the job does now.

The run of `remove_return` on Saturday 12 has an empty `reads`: the file it removed was gone when it started, and it read nothing.

The next cell makes a graph from what each run read and wrote in the week with no changes, as Chapter 6 made one from its lines, and follows edges upstream from `sales_dashboard`. Its events carry `run`, `job`, `type`, `reads` and `writes`.

Before you read on, write in the next cell what that traversal would reach if the events carried no `reads`.

## S

With `reads`, the traversal reaches 6 nodes, back to `orders.jsonl`.

Delete `"reads"` from the list in the cell above, select that cell and press **Run below**.

Without `reads`, the traversal reaches only `refresh_dashboard`. The graph shows no input for `daily_sales`, or for anything else.

A run that read nothing, as `remove_return`'s did, also gives the graph no input. From the graph, a run that read nothing and a run whose events left `reads` out look the same.

Put `"reads"` back and press **Run below** again.

## V

The table sets your design against 4 readings. Each needs its own fields, which the table lists.

As the cell first stands, `yours` holds `run`, `job`, `type`, `time` and `status`, and meets the first reading only.

As written, a design meets "Record every run." if each run sends events and the events keep each run apart. That needs `run`: without it, 2 runs of one function on one day became one row.

Which of the readings a design meets depends on its fields. A field's name does not say which reading it serves: `time` is when an event was sent, not when the data was written.

## W

## Before Chapter 8

Chapter 6's lines and the warehouse could not say what each night did. Events grouped into runs gave Jo the count, 3 orders, left out from the run on Friday 11. Earlier chapters said which orders. Grouping by `job` and `day` merged 2 runs of `record_return` on Wednesday 9, and `run` told them apart. The runs showed which nights `build_daily_sales` read the analyst's copy. Without `reads`, the graph showed no input for `daily_sales`, as it shows none for a run that read nothing.

The experiments could not show how a program the shop did not write would know what each field means.

Chapter 8 writes the same runs in the form an open standard sets, which programs written elsewhere can read.

- What does a platform you work on record about each time a job does its work?
- In your design, which events exist for a program that stops before it finishes?
- What should a run of a function record when a file is deleted and then created again with the same name?
