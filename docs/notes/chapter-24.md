# Chapter 24: Build the metadata store

A working note. Written on 13 October 2026 with Chapters 25 to 28, as a notebook
(`notebook/chapter_24.py`). It opens Part VI (`docs/notes/part-6/design.md`).

## What the chapter does

The reader keeps the week's metadata (14 edges by job, and Chapter 4's descriptive lines for
`daily_sales` and `sales_dashboard`) in four shapes and writes one question for each, what reads a
dataset; one check runs it for all 11 datasets and counts the records read:

- JSON documents, one per program and one per dataset: the reader completes a loop; 11 of 11, 187
  documents read (17 for each dataset);
- a SQLite table `edges`, with no index: the reader writes the `WHERE` clause; 11 of 11, 154 rows, a
  scan;
- the same table with an index: the starting cell drops `edges_index` and creates it on `job`; the
  reader changes the column to `dataset`; 14 rows, a search through the index (on `edge`, 88);
- a graph: the reader keeps only the `reads` edges at the dataset's node; 11 of 11, 14 edges;

then reads what each shape costs for the reverse question, what `build_daily_sales` reads (1
document, 14 rows, 2 edges), and questions "The metadata store must be fast."

## What was built for it

`notebook/shop/store.py`: the four shapes, the counting, the plan reading, `check` and `compare`;
stubs and references for the four pieces (`docs/lab.md`, "Part VI's pieces").

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `documents`

- **Role:** inspect
- **Serves:** what does a document hold, and where is a dataset's reader named? The 17 documents,
  one a line.
- **Why now:** the reader's loop reads these fields.

### `documents-check`

- **Role:** experiment
- **Objective:** the reader finds that, with documents kept by program, finding a dataset's readers
  means opening every document.
- **Known before:** Chapter 7's JSON events; Chapter 9's edges by job.
- **Driving question:** what reads each dataset, and how many documents does the answer open?
- **The action:** complete the loop's line; press **Run below**.
- **Why the action:** the count is of the reader's own loop.
- **Evidence:** 3 of 11 as it stands; 11 of 11 and 187 documents after.
- **Consequence:** the question's cost is set by where the answer is kept, not by the code.
- **Predictable:** yes.
- **Gives nothing away:** the page says what to add, not how much it reads.
- **Not knowing:** fair.
- **Next question:** does a table read less?

### `table-check`

- **Role:** experiment
- **Objective:** the reader discovers that a `WHERE` clause on a table with no index still reads
  every row.
- **Known before:** SQL from Chapter 2; Chapter 23's index, described.
- **Driving question:** will a query for one dataset's readers read every row, or only that
  dataset's?
- **The action:** write the prediction; add the `WHERE` clause; press **Run below**.
- **Why the action:** the plan answers only for a query the reader wrote.
- **Evidence:** 154 rows; the plan reads every row of `edges`.
- **Consequence:** a reader who expected the clause to narrow the reading learns that filtering is
  not finding.
- **Predictable:** partly; many expect fewer rows.
- **Gives nothing away:** the prediction cell names both outcomes and neither is favoured. The page
  says the table has no index before the prediction, so a reader can reason to an answer; the
  starting query's check below it, which also shows 14 a dataset, has no `WHERE` clause.
- **Not knowing:** a fair answer; the plan settles it.
- **Next question:** what would let the query find the rows?

### `index-check`

- **Role:** experiment (completes `table-check`)
- **Evidence:** an index on `job` leaves a scan; on `dataset`, 14 rows and the index in the plan; on
  `edge`, used, 88 rows. The counting reads the plan's words (`docs/sources.md`, "SQLite's query
  plan").

### `graph-check`

- **Role:** experiment (completes `documents-check`)
- **Evidence:** 6 of 11 as it stands (every edge at the node, writers included); 11 of 11 and 14
  edges with `reads` only.

### `compare`

- **Role:** inspect
- **Serves:** which shape suits which question? Records read for a dataset's question and a
  program's.
- **Why now:** the requirement that follows needs both columns.

## Requirements

"The metadata store must be fast." Readings: fast to find one program or asset by name (a key: one
document); fast to find what reads an asset (an index on `dataset`, or a graph: 2 records for
`clean_orders`); fast to follow lineage several steps (the graph, a node's edges a step); fast to take
each event as it arrives (not measured); fast enough as the store grows (not measured here; Chapter
23 projected other questions). The page names which shape met which: documents and graph the first,
the indexed table and graph the second, the graph the third for one step. The figure that questions it is the
free-text cell after the box.

## Originality

The obvious structure is a textbook's chapter on data models: documents, then relations, then
graphs, each with its own example of people, their jobs and their friends. This chapter keeps one
small set of metadata, the shop's week, asks one question of every shape, counts the records each
reads from the shape's own structure (SQLite's plan for the table), and has the reader add the
index. The documents, the counting and the check are the shop's own.

## What the prose process caught

First draft from brief P24 (`part-6/drafts/P24.md`); the review's changes through brief P24-rev
(`part-6/briefs/P24-rev.md`, draft `part-6/drafts/P24-rev.md`). The first drafts' slips across Part
VI were labels where a statement belonged ("The question:", "Result 1"), single quotes round a
requirement, two joins that left "the next cell" pointing at the wrong cell, *job* where the six
programs were meant, and a total whose scope was missing; each was fixed with the fewest words.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 20 findings (`review/verdicts.md`): 6 upheld, 9 partly, 5 rejected.
Read whole again after the fixes, with each cell's output (`review/chapter_24-after-review.md`).
Acted on:

- the starting index cell had a fixed name, so changing only its column changed nothing (`CREATE
  INDEX IF NOT EXISTS` on an index that existed): it now drops `edges_index` and creates it, and the
  page does not name the index;
- an index on `edge`, or on two columns, counted 0 rows: the count now takes every column the plan
  says the search uses, with the query's own values (8 per dataset on `edge`); tested;
- the week is Chapter 23's (14 edges, 11 datasets), not Chapter 9's (17); the page and docstrings
  say so, and why the store's 11 datasets differ from the map's;
- the slogan about shapes and their questions is gone; the page says where each count came from,
  and that the table has no index on `job`;
- the page says the table has no index before the prediction; a dataset's document has no `reads`;
  the starting query has no `:dataset`;
- "fast" has a fifth reading (as the store grows), and the page says which shape met which reading;
- counts compare items opened, not their size; lookups by name count as nothing, unlike Chapter 23;
- SQLite's plan wording has a source, and the two plans the chapter shows are pinned in a test.

Rejected, with the sceptic: the order of the shapes (the plan's), a new figure for `compare`, a
rename of the two `readers_of`, and the phone-width claim nobody measured.

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
24 to 28"): from Chapter 23's link, 11 files, 0.32 MB, in a new tab; Run all 8.2 to 9.1 s; peak memory 396 to 403 MB alone, 615 MB with Chapter 23
open; no error output, no console error. The browser test (`notebook/jupyterlite/smoke.mjs`) types the
references into each cell and reads the checks' lines.

## Known gaps

- The counts are items opened, from the plan's words and the shop's own counting; the chapter
  measures no time.
- SQLite's page on the plan was not reachable; the source is SQLite's code, and the browser test is
  the check on the SQLite the page runs.
