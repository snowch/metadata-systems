# Brief P24: Chapter 24, Build the metadata store

Read `common.md` in this folder first, and `docs/style.md`. Write
`docs/notes/part-6/drafts/P24.md`, with one `## key` heading per slot below, in this order. The
chapter introduces no new term. Words it may use from earlier chapters: *index* (Chapter 23),
*traversal* (Chapter 5), *edges by job* (Chapter 9).

## A

A list of four objectives:

- Keep the week's metadata as JSON documents, as a table, as a table with an index, and as a graph.
- Write the same question for each: what reads a dataset.
- Count the records each one reads to answer it, and find which questions each one suits.
- Question the requirement "The metadata store must be fast."

## B

- The heading `## One question, four shapes`.
- Since Chapter 9, the shop's metadata system has answered questions from the events it ingested.
  Part VI builds the parts it used, one chapter each, starting here with the store that keeps the
  metadata.
- One store can keep the same metadata in different shapes. Here the metadata is the week's 14 edges
  by job (Chapter 9, the week with the returns desk) and the descriptive lines Chapter 4 ended with
  for `daily_sales` and `sales_dashboard`.
- Each shape answers one question: what reads a dataset? You write the answer for each shape. A
  check below your code asks it for each of the week's 11 datasets, compares the answer with
  Chapter 9's edges, and counts the records your code read.
- The first shape is JSON documents, one for each job and one for each dataset. The next cell prints
  them, one document a line.

## C

- Each job's document holds its number of runs (`runs`), the datasets it reads (`reads`) and the
  datasets it writes (`writes`). Each dataset's document holds its descriptive lines, where it has
  any.
- The next cell defines `readers_of(documents, dataset)`. Its loop goes through every document and
  adds nothing. As it stands, the check below it finds 3 of 11 datasets right: the 3 that no job
  reads.
- Change the line inside the loop so that it adds the document's `job` when the document's `reads`
  lists the dataset. Then select the cell and press **Run below**.

## D

- With the loop changed, the check finds 11 of 11 datasets right. It reads 187 documents: all 17
  for each of the 11 datasets.
- The loop opens every document because a dataset's readers are named inside each job's document,
  not in the dataset's own.
- Then this heading: `## A table`
- The second shape is a table in SQLite, the database the shop's warehouse runs on: `edges`, with one
  row for each edge by job, and the columns `job`, `edge`, `dataset` and `runs`.
- Before you read on, write in the next cell whether a query for one dataset's readers will read
  every row of `edges`, or only that dataset's rows.

## DD

This slot is the text of a cell the reader writes in. Write exactly two lines: the question, then a
line of eight full stops.

- The question: will the query read every row of `edges`, or only the dataset's rows?

## E

- The next cell holds the query, as text, in `query`. As it stands, it selects every row's `job`,
  and the check finds 3 of 11 right.
- Add a `WHERE` clause that keeps the rows whose `edge` is `reads` and whose `dataset` is
  `:dataset`, the name the check passes in. Select the cell and press **Run below**.
- The check reads SQLite's own plan for the query. The plan says whether the query reads the whole
  table or looks its rows up.

## F

- With the `WHERE` clause, the check finds 11 of 11 right. The query reads every row of `edges`:
  154 rows, 14 for each of the 11 datasets.
- The plan is a scan: SQLite reads each row and tests it against the `WHERE` clause.
- Compare this with what you wrote.
- Then this heading: `## An index`
- The next cell creates an index on the column `job` of `edges`. Change `job` to the column your
  query looks up. Select the cell and press **Run below**: the check below it runs your query again.

## G

- With the index on `dataset`, the query reads 14 rows in all: for each dataset, only that dataset's
  rows. The plan looks the rows up through the index `edges_by_dataset`.
- With the index on `job`, the plan was still a scan, because the query does not look up a job.
- Then this heading: `## A graph`
- The fourth shape is a graph, as in Chapter 5: a node for each job and each dataset, and an edge
  for each edge by job. `graph.edges_at(name)` gives the edges at one node, and the check counts each
  edge it gives.
- The next cell defines `readers_of(graph, dataset)` for the graph. As it stands, it gives the job
  of every edge at the dataset's node, and the check finds 6 of 11 right.
- Keep only the edges whose `edge` is `reads`. Select the cell and press **Run below**.

## H

- With that condition, the check finds 11 of 11 right, and reads 14 edges: for each dataset, the
  edges at its node.
- For this question, the table with the index and the graph each read 14 records, the documents
  187, and the table with no index 154.
- The next cell asks each shape two questions, with the shop's own code: what reads `clean_orders`,
  and what `build_daily_sales` reads. The table has the index on `dataset`.

## I

- What reads `clean_orders`: 17 documents, 2 rows of the table, 2 edges of the graph.
- What `build_daily_sales` reads: 1 document, 14 rows of the table, 2 edges of the graph.
- The documents are kept one for each job, so a job's question opens one document and a dataset's
  question opens all of them. The index on `dataset` serves the dataset's question and not the
  job's. The graph keeps both ends of every edge, so both questions read only one node's edges.
- Each shape reads few records for the questions its structure was built for, and many for the
  others.

## RH

- The heading `## A fast store`.

## J

- Before you read on, write in the next cell what "fast" means to you here.

## JJ

Two lines: the question, then a line of eight full stops.

- The question: what does "fast" mean here?

## K

- "Fast" could mean several things, and each needs a different structure. Then a list:
  - fast to find one job or asset by its name: a key for each document, or a lookup by name; the
    documents found `build_daily_sales`'s in 1 document read;
  - fast to find what reads an asset: an index on `dataset`, or a graph; each read 2 records for
    `clean_orders`;
  - fast to follow lineage several steps: each step quick; the graph reads one node's edges a step,
    as Chapter 5's traversal did;
  - fast to take each event as it arrives: this chapter did not measure writing.
- Each shape here meets some of these readings and not others.
- The requirement does not say which it means.

## Z

- The heading `## Before Chapter 25`.
- Summary facts, in order: four shapes answered the same question, and each passed the same check;
  for every dataset, the documents read 187 records, the table with no index 154, the table with an
  index on `dataset` 14 and the graph 14; the index on `dataset` did not help the question about a
  job; what the check could not show is time, the size of each shape, or what each costs to write.
- Chapter 25 builds the collector that receives the events the store is filled from.
- Three questions, as a list: Which questions does your metadata store answer most often? Which of
  them read every record? Which structure would serve them, and which questions would it not?
- The heading `### How this differs from a real platform`, and two bullets:
  - The shop's store holds 14 edges. Chapter 23 projected what the same questions read at 10,000,000
    assets.
  - The check counts records from SQLite's plan and from the shop's own counting, not from time
    taken.
