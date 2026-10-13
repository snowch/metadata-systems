# Revision brief P24: Chapter 24, Build the metadata store

Read `rev-common.md` first. Redraft these slots: B, C, D, E, F, G, H, I, K, Z. Terms: none new.
Say "rows" for the table, "documents" for the documents and "edges" for the graph; where a sentence
means all three, say "items". Say "dataset" where one is meant, never "asset".

## B

- Keep the heading `### One question, four shapes`.
- Since Chapter 9, the shop's metadata system has answered questions from the events it ingested.
  Part VI builds the parts it used, one chapter each, starting here with the store that keeps the
  metadata.
- One store can keep the same metadata in different shapes.
- Here the metadata is the 14 edges by job of the week with the returns desk, the week Chapter 23
  measured. It also holds the lines Chapter 4 wrote about two datasets: what `daily_sales` means and
  who is responsible for it, and who is responsible for `sales_dashboard`.
- Each shape answers one question: what reads a dataset? You write the answer for each shape.
- A check below your code runs it for each of the 11 datasets the edges name, compares each answer
  with the edges, and counts the items your code read.
- The first shape is JSON documents: one for each program that ran (the four jobs and the returns
  desk's two functions) and one for each dataset. The next cell prints them, one document on each
  line.

## C

- A program's document holds `job`, its number of runs (`runs`), the datasets it reads (`reads`)
  and the datasets it writes (`writes`).
- A dataset's document holds `dataset` and the lines Chapter 4 wrote about it, where there are any.
  It has no `reads`.
- The 11 datasets are the ones the edges name. So the list includes `r-203.json`, which is no longer
  in storage, and leaves out `products.csv`, which no program reads or writes. That is why it
  differs from the map's assets.
- The next cell defines `readers_of(documents, dataset)`. Its loop goes through every document and
  adds nothing to the result.
- Keep: "As it stands, the check below it finds 3 of 11 datasets right: the 3 that no program reads."
- Change the line inside the loop so that it adds a program's `job` when its `reads` lists the
  dataset. Then select the cell and press **Run below**.

## D

- Keep: "With the loop changed, the check finds 11 of 11 datasets right. The loop reads 187 documents: all 17 documents for each of the 11 datasets."
- The loop opens every document because a dataset's readers are named in each program's document,
  not in the dataset's own.
- Keep the heading `### A table`.
- The second shape is a table in SQLite, the database the shop's warehouse runs on: `edges`, with one
  row for each edge by job, and the columns `job`, `edge`, `dataset` and `runs`.
- The table has no index. SQLite does not make one unless a statement creates it.
- Before you read on, write in the next cell whether a query for one dataset's readers will read
  every row of `edges`, or only that dataset's rows.

## E

- The next cell holds the query, as text, in `query`.
- As it stands, the query has no `:dataset`, the name the check passes in for each dataset. The
  check takes that as no readers for any dataset, and finds 3 of 11 right: the 3 that no program
  reads.
- Add a `WHERE` clause that keeps the rows whose `edge` is `reads` and whose `dataset` is
  `:dataset`. Select the cell and press **Run below**.
- The check gets SQLite's own plan for the query. The plan shows whether the query reads the whole
  table or looks its rows up.

## F

- Keep: "With the `WHERE` clause, the check finds 11 of 11 right. The query reads every row of `edges`: 154 rows, 14 for each of the 11 datasets."
- The plan is a scan: SQLite reads each row and tests it against the `WHERE` clause.
- Compare this with what you wrote.
- Keep the heading `### An index`.
- The next cell drops the index `edges_index` if there is one, and creates it on the column `job` of
  `edges`.
- Change `job` to the column your query looks up. Select the cell and press **Run below**: the check
  below it runs your query again.

## G

- Keep: "With the index on `dataset`, the query reads 14 rows in all".
- That is, for each dataset, only that dataset's rows. The plan looks them up through the index,
  and the check names the index.
- With the index on `job`, the plan stays a scan, because the query does not look up a job.
- An index on `edge` is used too, but it narrows little: each search reads the 8 rows whose `edge`
  is `reads`, 88 in all.
- Keep the heading `### A graph`.
- The fourth shape is a graph, as in Chapter 5: a node for each program and each dataset, and an
  edge for each edge by job.
- `graph.edges_at(name)` gives the edges at one node, and the check counts each edge it gives.
- The next cell defines `readers_of(graph, dataset)` for the graph. As it stands, it gives the job of
  every edge at the dataset's node, and the check finds 6 of 11 right.
- Keep only the edges whose `edge` is `reads`. Select the cell and press **Run below**.

## H

- With that condition, the check finds 11 of 11 right, and reads 14 edges: for each dataset, the
  edges at its node.
- For this question, over all 11 datasets: the documents read 187, the table with no index 154, the
  table with the index on `dataset` 14, and the graph 14.
- These counts compare how many items each shape opens, not how big each item is.
- The next cell asks each shape two questions, with the shop's own code: what reads `clean_orders`,
  and what `build_daily_sales` reads. The table has the index on `dataset`, and no index on `job`.

## I

- Keep: "What reads `clean_orders`: 17 documents, 2 rows of the table, 2 edges of the graph."
- Keep: "What `build_daily_sales` reads: 1 document, 14 rows of the table, 2 edges of the graph."
- The documents are kept one for each program, so a program's question opens 1 document and a
  dataset's question opens all 17.
- The table's 14 rows for the program's question are a scan: the table has no index on `job`. The
  index on `dataset` serves the dataset's question only.
- The graph keeps both ends of every edge, so each question reads only one node's edges: 2 here.

## K

A short list, then two sentences.

- "Fast" could mean several things. A list; each item says what it needs and what this chapter
  measured:
  - fast to find one program or dataset by its name: a key for each document, or a lookup by name.
    Finding `build_daily_sales` took 1 document.
  - fast to find what reads a dataset: an index on `dataset`, or a graph. Each read 2 items for
    `clean_orders`.
  - fast to follow lineage several steps: one node's edges at each step, as in Chapter 5's
    traversal. This chapter measured one step.
  - fast to take each event as it arrives: this chapter did not measure writing.
  - fast enough as the store grows: counts at a larger size, which Chapter 23 projected for other
    questions, and the time each takes, which this chapter did not measure.
- Of the shapes here, the documents and the graph met the first reading, and the table, with no
  index on `job`, did not. The table with the index on `dataset` and the graph met the second. The
  graph met the third, for one step. None was measured against the
  fourth or the fifth.
- The requirement does not say which it means.

## Z

- Keep the heading `### Before Chapter 25`.
- Four shapes answered the same question, and each passed the same check. Where the answer is kept
  decided how many items it read: in each program's document, every document; in a table with no
  index, every row; through an index on `dataset` or at a graph's node, only the dataset's own.
- The check could not show the time each shape takes, or what each costs to write.
- Chapter 25 builds the collector that receives the events the store is filled from.
- Three questions, as a list:
  - Which questions does your metadata store answer most often?
  - Which of them read every record?
  - Which structure would serve them, and which questions would it not?
- Keep the heading `### How this differs from a real platform`, then a list:
  - The shop's store holds 14 edges. Chapter 23 projected other questions at 10,000,000 assets: the
    latest run of one job, one day's events, and what is downstream of one asset.
  - The check counts items from SQLite's plan and from the shop's own counting, not from the time
    taken.
  - Finding a document by name, a node, or a place in an index counts as nothing here. Chapter 23
    counted about 30 steps down an index at 10,000,000 assets.
