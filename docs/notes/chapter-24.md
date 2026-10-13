# Chapter 24: Build the metadata store

A working note. Written on 13 October 2026 with Chapters 25 to 28, as a notebook
(`notebook/chapter_24.py`). It opens Part VI (`docs/notes/part-6/design.md`).

## What the chapter does

The reader keeps the week's metadata (14 edges by job, and Chapter 4's descriptive lines for
`daily_sales` and `sales_dashboard`) in four shapes and writes one question for each, what reads a
dataset; one check runs it for all 11 datasets and counts the records read:

- JSON documents, one per program and one per dataset: the reader completes a loop; 11 of 11, 187
  documents read (17 for each dataset);
- a SQLite table `edges`: the reader writes the `WHERE` clause; 11 of 11, 154 rows, a scan;
- the same table with an index: the reader changes the indexed column from `job` to `dataset`; 14
  rows, a search through `edges_by_dataset`;
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
- **Gives nothing away:** the prediction cell names both outcomes and neither is favoured; the stub's
  check below it, which also shows 14 a dataset, has no `WHERE` clause.
- **Not knowing:** a fair answer; the plan settles it.
- **Next question:** what would let the query find the rows?

### `index-check`

- **Role:** experiment (completes `table-check`)
- **Evidence:** an index on `job` leaves a scan; on `dataset`, 14 rows and the index in the plan.

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
each event as it arrives (not measured). Each shape meets some. The figure that questions it is the
free-text cell after the box.

## Originality

The obvious structure is a textbook's chapter on data models: documents, then relations, then
graphs, each with its own example of people, their jobs and their friends. This chapter keeps one
small set of metadata, the shop's week, asks one question of every shape, counts the records each
reads from the shape's own structure (SQLite's plan for the table), and has the reader add the
index. The documents, the counting and the check are the shop's own.
