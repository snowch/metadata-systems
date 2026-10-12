# Chapter 7: Jobs, runs and events

A working note. Written on 12 October 2026, at the author's request to "complete part 2", as a
notebook (`notebook/chapter_07.py`) in the form of Chapters 3 to 6.

## What the chapter does

Jo Marsh, told in Chapter 6 that `build_clean_orders` leaves out orders with no customer id, asks
how many it left out, and on which nights. Chapter 6's lines say what the job reads and writes; the
warehouse records only the last night's row count and time. The head of the shop has each program
send a message when it starts and when it finishes: an **event**; one time a program does its work
is a **run**. The reader:

- reads the fields the shop's programs can fill in, and a first design for Jo's question (`job`,
  `type`, `time`, `rows_read`, `rows_written`); groups `build_clean_orders`'s 14 events by job and
  day, and reads the rows left out each night: 0, 0, 1, 4, 4, 4, 4. The 1 is the export's second
  copy of order 7015; the run on Friday 11 adds Thursday's three orders with no customer id. Jo's
  answer: 3;
- meets the returns desk and its two functions, writes how many rows grouping by job and day will
  show for `record_return` on Wednesday 9, and finds one row holding two runs; adds `run`, the
  identifier a program makes when it starts, and reads the functions' 6 runs with the object, its
  version and the change;
- answers Chapter 6's leftover question with the `source` change: the runs on 13 and 14 September
  read the copy, under a new code version;
- writes what upstream of the dashboard would reach without `reads`, deletes `reads`, presses
  **Run below**, and sees `daily_sales` seem made from nothing;
- questions "Record every run." (below), with the design they choose.

It introduces the plan's two terms: *event* in "Events" (the term test holds it there), *run* as a
noun in the same section (the term gate exempts "run", the verb, so no test can hold the noun).

## What was built for it

- `notebook/shop/data.py`: `RETURNS_DESK`, six changes to returns' files at fixed times: three
  creates, a correction (`r-202` overwritten), a return of Thursday's order 7021 (no customer id),
  and a withdrawal (`r-203` deleted).
- `notebook/shop/platform.py`: object storage keeps each object's versions, with a delete marker
  where one is deleted (`versions`, `delete`); a JSON object is a file it can read; the warehouse can
  create a table and change some of its rows (`create_table`, `change`).
- `notebook/shop/week.py`: the `returns` change (the bucket `shop-returns`, the table `returns`, the
  functions `record_return` and `remove_return`, each started 2 seconds after its change); every
  execution now records its program's name in the repository, what it read and how many rows, its
  code as it was that day, and for a function the object, version and change; `job_code` gives a
  program's code on a given day, and the repository holds the functions with the `returns` change.
- `notebook/shop/runs.py`: `event_fields`, `events` (the reader's design filled in from the
  executions), `runs` (grouped by any fields, `day` included), `readings` and `lineage`.
- `notebook/shop/figures.py`: the platform figure lists the returns' files; a caption sets
  backticked names in the code font.
- `notebook/shop/graph.py`: the drawing in data-flow order bends an edge that skips a layer through
  each layer it crosses, places a node nothing flows into just above what it feeds, sizes boxes by
  their text, and draws a wide layer tighter before it wraps (Chapter 9's graph needed all four).

## Figures

### `platform` and `platform-with-returns`

- **Role:** reference
- **Serves:** the assets before the returns desk; then the same platform with its bucket's files and
  the table `returns`, when the chapter introduces them.
- **Why now:** the second appears where the functions first matter (`CLAUDE.md`, "A chapter's
  opening sets up the smallest model its first question needs").

### `lines-and-catalogue`

- **Role:** inspect
- **Serves:** Jo's question: what the shop already holds about each night.
- **Why now:** it is the evidence for the reader's first expectation, that neither answers.

### `fields`

- **Role:** reference
- **Serves:** the design: what each field holds, and which event carries it.
- **Why now:** every design below chooses from it.

### `first-design`

- **Role:** experiment
- **Objective:** the reader learns that a record of each run answers a question about each night
  that a record of the job cannot, and that a count from a rebuilt table needs subtracting.
- **Known before:** Chapter 6's lines; the warehouse's last row count; Chapter 2's rules.
- **Driving question:** how many orders did `build_clean_orders` leave out, and on which nights?
- **The action:** write what the lines and the warehouse can tell; read the events; group them.
- **Why the action:** the expectation commits the reader to what the shop already holds; the
  grouped runs then show what it lacked.
- **Evidence:** 14 events; per night rows read and written; left out 0, 0, 1, 4, 4, 4, 4.
- **Consequence:** the reader can answer Jo (3, from the run on Friday 11), and sees that each count
  includes earlier nights'.
- **Predictable:** that the lines cannot answer, yes; the counts, no: they are evidence.
- **Gives nothing away:** the prose above names the two sources, not what they lack.
- **Not knowing:** a fair answer before the events exist, and the right one about each night.
- **Next question:** what tells one run from another?
- **An experiment:** commit, run, inspect.

### `telling-runs-apart`

- **Role:** experiment
- **Objective:** the reader discovers that a program and a day do not identify a run once a program
  can run more than once a day, and that an identifier carried in each event does.
- **Known before:** grouping by job and day gave one row a night; the desk created two returns on
  Wednesday 9, at 10:05 and 15:40.
- **Driving question:** how many rows will grouping by job and day show for `record_return` on
  Wednesday 9?
- **The action:** write the number and why; read the row; then group by `run`.
- **Why the action:** the reader holds the belief a nightly world taught them, and tests it.
- **Evidence:** one row of 4 events and two objects, 10:05:02 to 15:40:05; then 6 runs, each its
  own object change and version.
- **Consequence:** a reader who said 2 learns why the grouping gives 1; one who said 1 learns what
  ties a run's events instead (`time` cannot: start and finish differ).
- **Predictable:** yes, from the two times given.
- **Gives nothing away:** the prose gives the two creates, not how the grouping treats them.
- **Not knowing:** not the right answer: the facts above settle it.
- **Next question:** what did each run read?
- **An experiment:** commit, run, compare, change the key.

### `what-each-run-read`

- **Role:** inspect
- **Serves:** Chapter 6's question, which nights read the copy: 13 and 14 September, under code
  version `c715bde`.
- **Why now:** the design has just gained `reads` and `code_version`.

### `without-reads`

- **Role:** experiment
- **Objective:** the reader discovers that an event listing nothing read cannot be told from a run
  that read nothing, and what that does to a graph built from runs.
- **Known before:** Chapter 6's upstream traversal; `remove_return` read 0 rows.
- **Driving question:** what will upstream of `sales_dashboard` reach if the events carry no
  `reads`?
- **The action:** write the expectation; delete `"reads"`, press **Run below**; put it back.
- **Why the action:** the change is the reader's own, and the graph answers it.
- **Evidence:** 6 nodes with `reads`; `refresh_dashboard` alone without.
- **Consequence:** the reader sees `daily_sales` seem made from nothing, and why absence of a field
  is not evidence.
- **Predictable:** yes.
- **Gives nothing away:** the prose above asks the question only.
- **Not knowing:** not the right answer.
- **Next question:** what must "every run" be recorded with?
- **An experiment:** commit, change, run again.

## Requirements

The chapter questions "Record every run.", the plan's candidate, with the reader's own design
(`yours`) set against four readings by `readings`.

1. **What it says:** record every run.
2. **What it might mean:** to find the runs that failed; to know when each asset was last written;
   to know which version of the code each run used; to know which object change started a run.
3. **What each needs:** `run` and `status`; `time` and `writes`; `run` and `code_version`; `run`,
   `object`, `object_version` and `object_change`.
4. **What the platform records:** whatever the design sends; the cell starts with `run`, `job`,
   `type`, `time` and `status`.
5. **Whether it is met:** as written, by any design that sends events for each run; the first design
   meets the first reading only.

## Originality

The obvious examples are a scheduler's task-instance table (an orchestrator's runs of a DAG), a
tutorial that emits start and end events from a toy pipeline, or OpenLineage's own run-cycle
diagram. Here the reader designs the events' fields themselves, for a question about an invented
shop's Thursday, and finds a run's identity by merging two runs of an invented function started by
a returns desk; nothing follows a standard's field names, which arrive in Chapter 8 as a mapping
from the reader's own. The shop, its returns and its programs are invented for the course.

## What the prose process caught

Brief IA (`docs/notes/chapter-07/briefs/`, with `common.md` for Chapters 7 to 9), draft under
`drafts/`: every fact present and right. The figure's flow label came back shorter than the brief's
sentence, as its limit asked; the caption's backticks were lost in placing and put back.

## The review

A reviewer on another model read the chapter as a learner (`review/findings.md`, 10 findings) and an
independent sceptic attacked each one (`review/verdicts.md`). Acted on: the answer to Jo separates
what the events show (counts per run, the rise of 3 on Friday 11) from what earlier chapters say
(which orders) (1); the clause that explained the grouping moved after the Wednesday prediction, which
now asks how many rows and how many runs (2); the "without reads" conclusion rests on something shown,
`remove_return`'s empty `reads`, in a narrower table (3, 10); one sentence ties the first run on the
copy, Sunday 13, to Saturday's row (4); merged runs now add their row counts, so Wednesday's row shows
2 and 2 (8); "five and a half hours", a number the engine did not produce, went (9); "any design meets
it as written" now needs `run` (6); and `rows_written` covers a removal. Rejected by the sceptic: the
figure's date (5) and the objective (7). Brief LA drafted the new paragraphs; the draft wrote every
small number as a figure, and five that were not counts went back to words, and "every night" back to
the brief's "once a night". One stray session listing by the drafting agent changed nothing.

## Measured

12 October 2026, local build (`docs/notes/notebook-prototype.md`, "Chapters 7, 8 and 9"): Run all 8.0 to 9.3 s; peak memory 397 to 421 MB;
0.29 MB from Chapter 6's link.

12 October 2026, the published page after the review (opened alone, measured twice at each
width): Run all 11.0 and 9.6 s on a desktop, 10.2 and 10.2 s as a phone; peak memory
427 and 427 MB on a desktop, 410 and 407 MB as a phone. A second desktop attempt whose Run all did not start, 0.6 s, is left out and measured again.

## Known gaps

- Each change to a return's file starts its function exactly once, in order; Chapters 19 and 20
  break that.
- The run identifiers are the shop's numbering in time order, assigned after the week runs.
