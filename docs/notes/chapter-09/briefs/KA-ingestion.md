# Brief KA: Chapter 9, "From events to graphs"

Read `docs/notes/chapter-07/briefs/common.md` first, and `docs/style.md`. Its rules hold here.

Terms. The reader knows **run**, **event**, **function** (Chapter 7), and **OpenLineage**,
**namespace**, **producer** and **facet** (Chapter 8), and that a consumer is a program that
receives events. This chapter introduces **ingestion** (slot B) and **normalise** (slot G), each in
bold once, and neither before its slot (not even "normalised" or "normalising"). Words you must not
use anywhere: impact analysis, provenance, root cause, column lineage, identity, freshness.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Turn a week of received events into a graph, one stage at a time.
- Find what a line that cannot be read takes out of the graph.
- Give a stage a facet it does not know, and see what it adds.
- Question the requirement "The graph must show the current lineage."

### Slot B: under the heading `## From events to a graph`

- The shop's collector keeps every event it receives, each as one line of JSON, in the order it
  received them. The events come from the jobs, from the functions, and now from the analyst's
  script, which since Chapter 8 sends its own.
- The head of the shop wants a graph of the platform kept up to date from these events, not drawn
  from lines written by hand as in Chapter 6.
- Turning received events into stored records and graph edges is **ingestion**.
- The shop's ingestion has four stages: parse, normalise, objects and edges. Each is a function you
  run and inspect.

### Slot C: above the first code cell

- The next cell runs the week with the returns desk and the `source` change, in which
  `build_daily_sales` reads the analyst's copy from Saturday's row on.
- It collects the week's event lines, and prints how many there are and the start of the first.

### Slot D: under the heading `## Parse`

- Parsing turns each line of text into an event.
- A line that is not JSON, or that breaks the specification's rules, is refused, with its line
  number and why.
- The next cell cuts one line short, as if part of it were lost on the way: the COMPLETE of
  `build_daily_sales`'s run on Wednesday 9. It then parses every line and lists the lines refused.

### Slot E: after that cell

- The week has 82 lines. One is refused: line 20, which is not JSON. 81 events pass.
- Before you read on, write in the next cell what the graph will lose because of that line.

### Slot F: the text inside that cell (between triple quotes)

One question, then `........` on its own line: what the graph will lose because of that line. At
most about 60 characters a line. Plain text.

### Slot G: under the heading `## Normalise`

- Producers write the same thing in different ways.
- The functions' producer writes times with `+00:00`; the jobs' producer writes `Z`. Both mean UTC.
- The analyst's script names `clean_orders` without its database: `analytics.clean_orders`.
- To **normalise** events is to rewrite such things in one form, so that the same thing is written
  the same way.
- The shop's stage writes every time in UTC with `Z`, and adds the database `shop` to a warehouse
  name that leaves it out.
- The next cell normalises the events and lists every change it made.

### Slot H: after that cell

- 26 changes: 12 times, in the functions' events (6 runs, 2 events each), and 14 names, in the
  analyst's events (7 nights, 2 events each).
- Without the change to the names, the analyst's copy would not join `clean_orders`, as in
  Chapter 8.
- The rule for names is the shop's. It fits a warehouse with one database; where two databases hold
  tables of the same name, it would join tables that are not the same.

### Slot I: under the heading `## Objects`

- The next stage makes jobs, runs and datasets from the events.
- A run's state is the type of its latest event, by time.
- It reads fields only from the facets it knows: `nominalTime`, `jobType`, `sourceCodeLocation`,
  `inputStatistics`, `outputStatistics` and `version`. It lists any other facet and does not read it.
- The next cell builds the objects and shows how many of each it made.

### Slot J: after that cell

- 7 jobs (the four jobs, the two functions and the analyst's copy), 41 runs, 12 datasets, and 6
  facets the stage does not know.
- The next cell lists the runs whose latest event is a START.

### Slot K: after that cell

- One run: `build_daily_sales` on Wednesday 9. Its COMPLETE was the line cut short.
- To the stage, the run looks as though it is still working.

### Slot L: under the heading `## A facet the stage does not know`

- The next cell lists the facets the stage does not know.
- The cell after it lists the runs of `record_return`: when each started, what it read, and the change
  and the version from the facet `shop_objectChange`.

### Slot M: after those two cells

- All 6 are `shop_objectChange`, on the runs of the two functions.
- The table of `record_return`'s runs shows when each started and what it read, and no change or
  version: the stage did not read the facet.
- In the cell that starts `known = dict(`, delete the `# ` at the start of the line
  `known["shop_objectChange"] = ...`, select that cell and press **Run below**.
- The stage then knows the facet. The list of facets it does not know is empty, and each run of
  `record_return` shows whether its file was created or overwritten, and its version.

### Slot MSG: what the stages print, one sentence each

Write each under its own sub-heading (`### json`, `### rules` and so on), the exact text only:

- `json`: in the list of refused lines: the line is not JSON
- `rules`: in the list of refused lines: the line is JSON but breaks the specification's rules for a
  run event
- `no_refused`: printed in place of the list when no line was refused
- `no_changes`: printed in place of the list when normalising changed nothing
- `no_unknown`: printed in place of the list when the stage knows every facet in the events
- `no_runs`: printed in place of the list when no run matches

### Slot N: under the heading `## Edges`

- The last stage makes edges. For each run, one edge to each dataset the run read or wrote. For each
  job, the same edge once, with how many runs had it, and the first and last time one did.
- The week has 41 runs over 7 nights.
- Before you read on, write in the next cell how many edges between jobs and datasets you expect,
  and why: about as many as one night's reads and writes, or about seven times as many.

### Slot O: the text inside that cell

One question, then `........`: how many edges between jobs and datasets, and why. At most about 60
characters a line. Plain text.

### Slot P: after that cell

- 80 edges by run, and 17 by job.
- Each night's runs repeat the same reads and writes, so they add edges by run and not edges by job.
  An edge by job counts its runs instead.
- The functions add an edge by job for each file `record_return` read.
- The next cell lists the edges of `build_daily_sales`.

### Slot Q: after that cell

- 3 edges: it reads `clean_orders` in 5 runs, the first at `2026-09-08T02:30:21Z` and the last at
  `2026-09-12T02:30:21Z`; it reads the analyst's copy in 2 runs, on Sunday 13 and Monday 14; it writes
  `daily_sales` in 6 runs.
- 6, not 7: the COMPLETE of Wednesday's run was the line cut short, so to the graph that run wrote
  nothing.
- The edge to `daily_sales` stays, because other runs had it. Only its count of runs, and the missing
  edge for Wednesday's run, show the loss.
- The next cell draws the edges by job, in the order data flows, as Chapter 6's drawing did.

### Slot ALT: the drawing's description for a screen reader

One or two plain sentences, no backticks: three parts. orders.jsonl through build_clean_orders to
shop.analytics.clean_orders, which copy_clean_orders reads to write clean_orders_copy.csv, and which
build_daily_sales reads as well as the copy, to write shop.analytics.daily_sales, which
refresh_dashboard reads to write sales_dashboard. Four return files read by record_return, which
with remove_return writes shop.analytics.returns. customers.jsonl through build_clean_customers to
shop.analytics.clean_customers.

### Slot R: under the heading `## "The graph must show the current lineage."`

- The head of the shop's requirement: "The graph must show the current lineage."
- Before you read on, write in the next cell what "current" means to you.
- The cell after it lists, for each job, the edges its latest run had.

### Slot S: the text inside that cell

One question, then `........`: what "current" means to you. At most about 60 characters a line.
Plain text.

### Slot T: after that cell

- 13 of the 17 edges by job. Four are dropped: `build_daily_sales` reads `clean_orders` (its last
  such run was on Saturday 12), and `record_return` reads `r-201.json`, `r-202.json` and
  `r-203.json` (its latest run read `r-204.json` only).
- "Current" could mean three things, each needing something different:
  - as of the last event received: every edge received so far, all 17, so `build_daily_sales`
    reads both `clean_orders` and the copy;
  - as of each job's latest run: the 13 edges. That drops `clean_orders` for `build_daily_sales`, as
    the code since Saturday does. For `record_return` it also drops `r-201.json` and `r-202.json`,
    whose rows are still in the table `returns`;
  - as of the last change to a job's code: the edges of the runs since the code changed. That needs
    the code version of each run, which the stage keeps from `sourceCodeLocation`.
- The edges by job keep the first and last time, so a query can choose. The requirement does not say
  which "current" it means.

Write slot T as a short paragraph, one Markdown list of the three readings, then a short paragraph.

### Slot U: under the heading `## Before Chapter 10`

- Showed: four stages turned the week's events into a graph. A line cut short was refused at the
  first stage; its run then looked as though it were still working, and the edge to `daily_sales`
  counted 6 runs, not 7. Normalising joined the analyst's names to the jobs'. A facet the stage did
  not know was listed and not read, until you added it. The same reads and writes, night after night,
  made 80 edges by run and 17 by job. "Current" had three readings.
- Could not show: which columns each column is made from. Chapter 6 noted that `revenue_pence` is
  made from `price_pence` and `quantity`; no event here says so.
- Next: Chapter 10 reads the jobs' SQL to find which columns each column is made from.
- Then three reflective questions as a Markdown list, none with its answer: the first asks what a
  platform the reader works on does with an event it cannot read; the second asks which two
  producers on that platform might name one table differently, and which rule would join them; the
  third asks which reading of "current" the reader's own team would need, and for what.

### Slot V: under the heading `### How this differs from a real platform`

- The shop, its collector and its four stages are the course's own. Every rule in them is the
  shop's choice: the forms it normalises to, a run's state from its latest event, and the facets it
  reads.
- Here the week's events are made at once, after the week has run. A real collector receives them
  one at a time, over a network, while the jobs run.
- Chapter 29 compares how real consumers store events.

## Slots

Write the file `docs/notes/chapter-09/drafts/KA.md` with the slots under `## A`, `## B`, `## C`,
`## D`, `## E`, `## F`, `## G`, `## H`, `## I`, `## J`, `## K`, `## L`, `## M`, `## MSG` (with its six
`###` sub-headings), `## N`, `## O`, `## P`, `## Q`, `## ALT`, `## R`, `## S`, `## T`, `## U` and
`## V`, each the exact text to place, and nothing else in the file. Each slot that has a heading
starts with that heading.
