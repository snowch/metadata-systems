# Chapter 9: From events to graphs

A working note. Written on 12 October 2026 with Chapters 7 and 8, as a notebook
(`notebook/chapter_09.py`). It ends Part II, and checkpoint 2 (`docs/plan.md`, "The checkpoints")
falls after it.

## What the chapter does

The head of the shop wants a graph kept up to date from the events, not drawn from lines written by
hand. Turning received events into stored records and edges is **ingestion**; the shop's has four
stages, each a function the reader runs and inspects. With the `returns` and `source` changes, the
week's collector holds 82 lines from three producers. The reader:

- parses them, with one line cut short (the COMPLETE of `build_daily_sales` on Wednesday 9): 81
  events and one refused line; writes what the graph will lose;
- meets **normalise**: 26 changes, 12 times written with an offset and 14 analyst's names without
  the database;
- builds objects (7 jobs, 41 runs, 12 datasets, 6 facets not known) and finds the damaged run still
  looking as though it works;
- sees `shop_objectChange` listed and not read, removes a `# `, presses **Run below**, and sees the
  change and version on `record_return`'s runs;
- writes how many edges the week will make, and finds 80 by run and 17 by job; `build_daily_sales`
  writes `daily_sales` in 6 runs, not 7, which answers the line cut short;
- reads the job graph drawn in data-flow order;
- questions "The graph must show the current lineage." (below).

## What was built for it

- `notebook/shop/ingest.py`: `event_lines`, `parse`, `normalise`, `objects` (with `KNOWN`, the
  facets it reads, and `runs_of`), `edges` (by run and by job, with `of` and `latest`, and `graph`
  at either level). Its messages are Haiku's drafts of brief KA.
- `notebook/shop/openlineage.py`: `analyst_events`, the analyst's script as a third producer, naming
  `clean_orders` without its database.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the assets the events name.
- **Why now:** as Chapter 8.

### `parse`

- **Role:** experiment (with `edges-of-daily-sales`, which completes it)
- **Objective:** the reader discovers that a line lost before parsing takes one run's output out of
  the graph, and that a graph by job hides the loss in a count.
- **Known before:** Chapter 8's START and COMPLETE; that the cut line is a COMPLETE.
- **Driving question:** what will the graph lose because of that line?
- **The action:** write the expectation; read on to the objects and the edges.
- **Why the action:** the reader commits before the stages show where the loss lands.
- **Evidence:** line 20 refused; one run whose latest event is a START; `writes daily_sales` in 6
  runs, not 7; the edge itself still there.
- **Consequence:** a reader who expected the edge to vanish learns that other nights keep it; one
  who expected nothing lost learns the run looks still working.
- **Predictable:** in part, from Chapter 8.
- **Gives nothing away:** the prose names the line, not what follows from it.
- **Not knowing:** reasonable before the edges stage, and the page answers it there.
- **Next question:** what makes two producers' events agree?
- **An experiment:** commit, run, compare.

### `normalise`

- **Role:** inspect
- **Serves:** every change the stage made, and the reason the analyst's copy now joins.
- **Why now:** the term is given against it.

### `objects` and `still-working`

- **Role:** inspect
- **Serves:** the counts, and the damaged run in state START.
- **Why now:** the parse experiment's first consequence shows here.

### `unknown-facet`

- **Role:** experiment
- **Objective:** the reader learns that a stage reads only what it was told to, and that teaching
  it a facet adds fields without changing any event.
- **Known before:** Chapter 8's custom facet; the list of facets the stage knows.
- **Driving question:** why do `record_return`'s runs show no change or version?
- **The action:** remove a `# `, press **Run below**, read the runs again.
- **Why the action:** the change is the reader's, and the same events give more.
- **Evidence:** 6 unknown facets, then none; the change and version columns appear.
- **Consequence:** the reader sees that what a graph holds depends on the parser as well as the
  events.
- **Predictable:** yes.
- **Gives nothing away:** the prose says what to remove, not what appears.
- **Not knowing:** not the right answer.
- **Next question:** how many edges does the week make?
- **An experiment:** change, run again, compare.

### `edges`

- **Role:** experiment
- **Objective:** the reader learns that repeated runs add edges by run and not edges by job, and that
  both levels are needed.
- **Known before:** 41 runs over 7 nights; Chapter 6's 8 edges by job for the nightly jobs.
- **Driving question:** how many edges between jobs and datasets, and why?
- **The action:** write the expectation; read the counts and `build_daily_sales`'s three edges.
- **Why the action:** the two choices offered are the two levels; the reader commits to one.
- **Evidence:** 80 by run, 17 by job; the copy's 2 runs and `clean_orders`'s 5.
- **Consequence:** either answer was half right.
- **Predictable:** roughly.
- **Gives nothing away:** the prompt offers both readings, not which the stage keeps.
- **Not knowing:** a fair answer.
- **Next question:** which edges are current?
- **An experiment:** commit, run, compare.

### `job-graph`

- **Role:** reference
- **Serves:** the week's lineage from events, in data-flow order, with the copy and both of
  `build_daily_sales`'s reads.
- **Why now:** the edges are built; the drawing is what the head asked for.

## Requirements

The chapter questions "The graph must show the current lineage.", the plan's candidate, with the
reader's expectation and the edges each job's latest run had.

1. **What it says:** show the current lineage.
2. **What it might mean:** as of the last event received; as of each job's latest run; as of the last
   change to a job's code.
3. **What each needs:** every edge; each edge's last time against its job's latest run; each run's
   code version.
4. **What the graph records:** edges by job with their first and last time and count of runs, and
   each run's code version from `sourceCodeLocation`.
5. **Whether it is met:** each reading can be queried; the latest-run reading is right for
   `build_daily_sales` and drops `record_return`'s earlier files, whose rows are still in `returns`.

## Originality

The obvious examples are a lineage product's ingestion architecture diagram, a Kafka-to-graph-database
tutorial, or Marquez's own ingestion path. Here the stages are four functions over the invented
shop's week of events, from three of its producers, and every rule (what is normalised, how a run's
state is taken, which facets are read) is the shop's own and labelled so; the failure cases are a
line the reader sees cut and a facet the reader's own Chapter 8 introduced.

## What the prose process caught

Brief KA, draft under `drafts/`.

## Measured

12 October 2026, local build (`docs/notes/notebook-prototype.md`, "Chapters 7, 8 and 9"): Run all 8.3 to 9.0 s; peak memory 403 to 411 MB;
0.29 MB from Chapter 8's link. The published page is measured after the deploy.

## Known gaps

- The week's events are made at once after the week runs; a real collector receives them one at a
  time. Part V delivers them late, twice and out of order.
- The normalising rule for names fits one database.
