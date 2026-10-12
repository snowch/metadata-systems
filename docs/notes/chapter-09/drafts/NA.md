## B

## From events to a graph

The shop keeps every event it receives, each as one line of JSON, in the order it received them. The events come from the four jobs and the two functions. In Chapter 8 the analyst wrote one night's events by hand. Now the analyst's script sends its own events, each night.

The head of the shop wants a graph of the platform kept up to date from these events, not drawn from lines written by hand as in Chapter 6.

Turning received events into stored records and graph edges is **ingestion**. The shop's ingestion has four stages, each a function you run and inspect: parse, which reads each line; a stage that writes the same thing the same way; objects, which makes jobs, runs and datasets; and edges.

## J

The stage made 7 job records, one for each program that sent events: the four jobs, the two functions and the analyst's script. It made 41 run records and 12 dataset records, and it listed 6 facets it does not read.

The next cell lists the runs whose latest event is a `START`.

## K

One run is `build_daily_sales` on Wednesday 9. Its `COMPLETE` line was cut short.

Its stored record has the state `START`, a start time, an input, no end time and no output. That is the same stored record as a run still working.

## L

## A facet the stage does not read

The next cell lists the facets the stage does not read. The cell after it asks for the runs of `record_return`: when each started, what it read, and the change and the version of the file from the facet `shop_objectChange`.

## M

All 6 facets are `shop_objectChange`, on the runs of the two functions.

The table of `record_return`'s runs has two columns: when each started, and what it read. The change and the version are missing: the stage did not read the facet.

In the cell that starts `known = dict(`, delete the `# ` at the start of the line `known["shop_objectChange"] = ...`. Select that cell and press **Run below**. Then compare the two tables with what they showed before.

## N

## Edges

The last stage makes edges of two kinds. An edge by run joins one run to a dataset it read or wrote. An edge by job joins a job to a dataset that any of its runs read or wrote. It is made once per dataset. It records how many runs had it, and the first and last time one did.

The week has 41 runs: 35 by night (7 nights, each with the four jobs and the analyst's script) and 6 by the functions, during the day.

Before you read on, write in the next cell how many edges of each kind you expect, and why.

## P

There are 80 edges by run and 17 edges by job.

Each night's runs repeat the same reads and writes. They add edges by run, about one night's worth each night. They add no edge by job, which counts its runs instead.

`record_return` adds an edge by job for each file it read.

The next cell lists the edges by job of `build_daily_sales`.

## Q

`build_daily_sales` has 3 edges by job. It reads `clean_orders` in 5 runs, the first at `2026-09-08T02:30:21Z` and the last at `2026-09-12T02:30:21Z`. It reads the analyst's copy in 2 runs, on Sunday 13 and Monday 14. It writes `daily_sales` in 6 runs, not 7. The `COMPLETE` line of the run on Wednesday 9 was cut short, so the stored record of that run has no output. Its `START` named its input, so its read is counted.

The edge to `daily_sales` stays, because other runs had it. Only its count of runs, and the missing edge by run for Wednesday, show the loss.

The next cell draws the edges by job, in the order data flows, as Chapter 6's drawing did.

## R

## "The graph must show the current lineage."

The head of the shop's requirement: "The graph must show the current lineage."

Before you read on, write in the next cell what "current" means to you.

## READINGS

"Current" could mean three things, each needing something different:

- As of the last event received: every edge by job;
- As of each job's latest run: each edge's last time, set against the time of its job's latest run;
- As of the last change to a job's code: the code version of each run, set against the runs on each edge.

The readings differ for `record_return`. Its code did not change during the week, so the third reading keeps every file it read. Its latest run read only `r-204.json`, so the second keeps that one file alone.

The next cell lists, for each job, the edges its latest run had: the second reading's answer.

## T

That cell lists 13 of the 17 edges by job. It leaves out `build_daily_sales` reading `clean_orders` (the last such run was on Saturday 12), and `record_return` reading `r-201.json`, `r-202.json` and `r-203.json`. The rows of `r-201` and `r-202` are still in the table `returns`. The row of `r-203` was removed when its file was deleted.

By reading:

- As of the last event received: met; the edges by job hold all 17;
- As of each job's latest run: met; the cell above gives it;
- As of the last change to a job's code: not met by the edges by job alone; the stage keeps each run's code version (from `sourceCodeLocation`), and a query would have to join the runs to the edges.

The requirement does not say which "current" it means.
