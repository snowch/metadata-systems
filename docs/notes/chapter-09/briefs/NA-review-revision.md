# Brief NA: Chapter 9, "From events to graphs", after its review

Read `docs/notes/chapter-07/briefs/common.md` first, and `docs/style.md`. Its rules hold here. Terms
as brief KA: **ingestion** in slot B; **normalise** keeps its place in the section "Normalise",
after slot B, so slot B must not use "normalise" in any form. Do not write "collector". Do not say a
stage or a graph "knows", "sees" or "thinks"; say what the stored record holds. Call the four jobs,
the two functions and the analyst's script together "programs", never "jobs".

A review found a contradiction with Chapter 8, a requirement section without its readings before
the record or a verdict after it, a prediction misaligned with its counts, and some wording that
gave a stage a will. These slots replace paragraphs of the chapter.

## Facts (each checked against the shop's data)

### Slot B: under the heading `## From events to a graph`

- The shop keeps every event it receives, each as one line of JSON, in the order it received them.
- The events come from the jobs and from the functions. In Chapter 8 the analyst wrote one night's
  events by hand; the analyst's script now sends its own events, each night.
- The head of the shop wants a graph of the platform kept up to date from these events, not drawn
  from lines written by hand as in Chapter 6.
- Turning received events into stored records and graph edges is **ingestion**.
- The shop's ingestion has four stages, each a function you run and inspect: parse, which reads each
  line; a stage that writes the same thing the same way; objects, which makes jobs, runs and
  datasets; and edges.

### Slot J: after the cell that builds the objects

- The stage made 7 jobs, one for each program that sent events (the four jobs, the two functions and
  the analyst's script), 41 runs and 12 datasets. It also listed 6 facets it does not read.
- The next cell lists the runs whose latest event is a START.

### Slot K: after that cell

- One run: `build_daily_sales` on Wednesday 9. Its COMPLETE was the line cut short.
- Its stored record has the state `START`, a start time, an input, no end time and no output: the
  same record as a run still working.

### Slot L: under the heading `## A facet the stage does not read`

- (Use that heading exactly.)
- The next cell lists the facets the stage does not read.
- The cell after it asks for the runs of `record_return`: when each started, what it read, and the
  change and the version of the file from the facet `shop_objectChange`.

### Slot M: after those two cells

- All 6 are `shop_objectChange`, on the runs of the two functions.
- The table of `record_return`'s runs has two columns, when each started and what it read. The change
  and the version are missing: the stage did not read the facet.
- In the cell that starts `known = dict(`, delete the `# ` at the start of the line
  `known["shop_objectChange"] = ...`, select that cell and press **Run below**. Then compare the two
  tables with what they showed before.

### Slot N: under the heading `## Edges`

- The last stage makes edges of two kinds. An edge by run joins one run to a dataset it read or
  wrote. An edge by job joins a job to a dataset any of its runs read or wrote, once, with how many
  runs had it and the first and last time one did.
- The week has 41 runs: 35 by night (7 nights, each with the four jobs and the analyst's script) and
  6 by the functions, during the day.
- Before you read on, write in the next cell how many edges of each kind you expect, and why.

### Slot P: after the cell that counts the edges

- 80 edges by run, and 17 by job.
- Each night's runs repeat the same reads and writes. They add edges by run, about one night's worth
  each night; they add no edge by job, which counts its runs instead.
- `record_return` adds an edge by job for each file it read.
- The next cell lists the edges by job of `build_daily_sales`.

### Slot Q: after that cell

- 3 edges: it reads `clean_orders` in 5 runs, the first at `2026-09-08T02:30:21Z` and the last at
  `2026-09-12T02:30:21Z`; it reads the analyst's copy in 2 runs, on Sunday 13 and Monday 14; it writes
  `daily_sales` in 6 runs.
- 6, not 7: the COMPLETE of Wednesday's run was the line cut short, so the stored record of that run
  has no output. Its START named its input, so its read is counted.
- The edge to `daily_sales` stays, because other runs had it. Only its count of runs, and the missing
  edge by run for Wednesday, show the loss.
- The next cell draws the edges by job, in the order data flows, as Chapter 6's drawing did.

### Slot R: under the heading `## "The graph must show the current lineage."`

- The head of the shop's requirement: "The graph must show the current lineage."
- Before you read on, write in the next cell what "current" means to you.

### Slot READINGS: after that cell, before the cell that lists edges

- "Current" could mean three things, each needing something different:
  - as of the last event received: every edge by job;
  - as of each job's latest run: each edge's last time, set against the time of its job's latest run;
  - as of the last change to a job's code: the code version of each run, set against the runs on
    each edge.
- The readings differ for `record_return`. Its code did not change during the week, so the third
  reading keeps every file it read; its latest run read only `r-204.json`, so the second keeps that
  one file alone.
- The next cell lists, for each job, the edges its latest run had: the second reading's answer.

Write slot READINGS as one Markdown list of the three readings, then two short paragraphs.

### Slot T: after that cell

- 13 of the 17 edges by job. It leaves out `build_daily_sales` reading `clean_orders` (the last such
  run was on Saturday 12), and `record_return` reading `r-201.json`, `r-202.json` and `r-203.json`.
  The rows of `r-201` and `r-202` are still in the table `returns`; the row of `r-203` was removed
  when its file was deleted.
- By reading:
  - as of the last event received: met; the edges by job hold all 17;
  - as of each job's latest run: met; the cell above gives it;
  - as of the last change to a job's code: not met by the edges by job alone; the stage keeps each
    run's code version (from `sourceCodeLocation`), and a query would have to join the runs to the
    edges.
- The requirement does not say which "current" it means.

Write slot T as a short paragraph, one Markdown list of the three verdicts, then one sentence.

## Slots

Write the file `docs/notes/chapter-09/drafts/NA.md` with the slots under `## B`, `## J`, `## K`,
`## L`, `## M`, `## N`, `## P`, `## Q`, `## R`, `## READINGS` and `## T`, each the exact text to place,
and nothing else in the file. Each slot that has a heading starts with that heading.
