# Part VI: design

A working note, 12 October 2026, written before the engine for Chapters 24 to 28. It says what the
learner writes in each chapter, what checks it, which requirement each chapter questions, and why.

## What is the same in every chapter of the part

- **The learner writes code, small.** Each chapter asks for one short function, query or statement
  at a time, in a cell that starts as a stub: a working shape that returns the wrong answer, never a
  syntax error. A phone keyboard is the constraint: no piece is longer than about eight lines.
- **A check runs the chapter's tests against it.** The cell below each piece calls the shop's check
  for that piece with the learner's function. It prints one line per test: what was asked, what the
  learner's code gave, and, where it differs, what was expected. The check's lines are
  learner-facing strings and go through Haiku.
- **The stub fails and the reference passes.** The engine keeps a reference for every piece. A test
  in `notebook/tests` runs the check with the reference (every test passes) and with the stub (at
  least one fails), so the check proves something. The smoke test types the reference into the cell
  and finds the check passing, as Part V's smoke test makes each chapter's edit.
- **What an earlier chapter built arrives as the shop's.** A notebook cannot read another notebook's
  cells, and a learner's code is not graded twice. So Chapter 25 uses "the store as Chapter 24
  built it", which is the engine's reference, and says so in one sentence. This keeps the plan's
  rule that the course's state is derived, not stored.
- **No new terms** (the plan). Every word Part VI needs was introduced in Parts I to V.
- **Every chapter questions a requirement**, in its box. The plan's row for Chapters 24 to 28 gives
  one, "who owns X?", to Chapter 27; the others take a requirement their own material raises, below.

## Chapter 24: Build the metadata store

The week's metadata as one store, in four shapes, each passing the same tests.

- **The data.** The week with the returns desk (`run_week(["returns"])`): Chapter 4's descriptive
  records for the assets, Chapter 9's runs, and Chapter 9's edges by job (14).
- **The question all four shapes answer:** what reads a dataset? The learner writes
  `readers_of(store, dataset)` four times, once per shape, and the same test runs it for every
  dataset in the week against the answer from Chapter 9's graph.
- **Shapes and what the learner writes:**
  1. *JSON documents*, one per job and one per dataset, as Chapter 7's events gave them: a loop over
     the documents that collects each job whose `reads` lists the dataset. The check counts the
     documents the loop touched: all of them, for every dataset.
  2. *Tables*, in SQLite: `edges(job, edge, dataset, runs)`. The learner writes the `SELECT`. The
     check shows SQLite's query plan, `SCAN edges`: every row.
  3. *An indexed store*: the same table; the learner writes `CREATE INDEX ... ON edges(dataset)`.
     The plan becomes a search using the index: only the matching rows. This is Chapter 23's index,
     built.
  4. *A graph*, Chapter 5's: nodes and edges. The learner follows the edges into the dataset's node.
     The check counts the edges read: only that node's.
- **The experiment:** before the table, predict whether the table reads fewer records than the
  documents for the same question. Without an index, it does not. Then the reverse question, what
  does a job read, costs one document, a scan of the table even with the index on `dataset`, and
  one node's edges in the graph. A shape is quick for the questions it was built around.
- **Requirement:** "The metadata store must be fast." Readings: fast to find one asset by name; fast
  to find what reads an asset; fast to follow lineage several steps; fast to take each event as it
  arrives. Each needs a different structure. The learner's store meets some and not others, and the
  page says which.

## Chapter 25: Build the event collector

The collector that Chapter 18 named, built: it receives the week's events with Part V's faults and
keeps what ingestion needs.

- **The faults, all at once:** an event that breaks the specification (no `eventTime`), a COMPLETE
  received twice (a lost acknowledgement), a retry with a new time, a COMPLETE held up 26 hours, and
  a restart of the collector part-way through the week.
- **What the learner writes:** the key that recognises a repeat, `key(event)`, and the order the
  stored events are read in. Validation is Chapter 8's check, given; persistence is a JSON Lines file
  in object storage, given.
- **The tests:** every valid event kept once; the broken one refused with its reason; the graph
  built from what was kept equals the graph of the week with no faults; no run left open; the run's
  end time 02:30:21, not 02:30:52.
- **The surprise:** after the restart, a repeat that arrives is kept twice. The collector's memory
  of what it has seen was in the process, not in the file. The learner rebuilds it from the file on
  start, and the test passes.
- **Requirement:** "The collector must reject invalid events." Readings: events that break the
  specification; events from a producer the shop does not know; events that arrive out of order (a
  COMPLETE before its START). The third would refuse Chapter 20's START that arrived after its
  COMPLETE, which is a valid event.

## Chapter 26: Build the lineage graph

Persistent, time-stamped edges from the stored events.

- **What the learner writes:** `add(edges, event)`, which updates the edge for each input and
  output of the event: create it, or widen its first and last time and count its run.
- **The tests:** built one event at a time from the collector's file, the edges equal Chapter 9's
  edges by job; built from events in arrival order, with the late COMPLETE, the first and last
  times are the same (the stub that sets `last` to each event's time fails here); reloaded from its
  file after a restart, the graph continues.
- **The week:** with `source`, so `build_daily_sales` reads `clean_orders` in 5 runs, last on
  Saturday 12, and the analyst's copy in 2, Sunday 13 and Monday 14.
- **Requirement:** "Lineage must show the platform as it is now." Readings: the edges of each job's
  latest run (only the copy); every edge ever seen (both); the edges seen in the last N days. The
  time-stamped edges answer all three; a graph that keeps only the latest answers only the first.

## Chapter 27: Build the query layer

Questions over the learner's store and graph: what depends on X, where did X come from, who owns X,
which assets are stale, which jobs failed, what a schema change affects.

- **What the learner writes:** `downstream(graph, asset)`, a traversal over Chapter 26's edges
  (about eight lines), and `owner(asset)`, which returns an owner and says which meaning it holds.
  The other four questions are the shop's, built on the same graph, and shown answering.
- **The tests:** downstream of `orders.jsonl` is Chapter 14's set; upstream by reversing the edges;
  the owner query must name its meaning.
- **Requirement (the plan's):** the query layer must answer "who owns X?". Whichever meaning the
  learner's records keep, the query says which: Chapter 2's account, Chapter 4's responsible person,
  Chapter 21's claims.

## Chapter 28: Build the metadata interface

Views of the learner's own store: an asset page with its description, runs, lineage, schema and
quality, as HTML in the page.

- **What the learner writes:** which sections the asset page shows, as a list, and one section's
  rows, `run_history(asset)`. The page is drawn from them.
- **The tests:** each section's rows come from the store, not from the engine's own answers; the
  page for `daily_sales` shows Thursday's run and its row count.
- **Requirement:** "The asset page must show everything about an asset." Readings: every field the
  store holds; everything a person asking about the asset needs; the asset's full history. The first
  is a dump, the third unbounded; the learner chooses, and the page says what it leaves out.

## Originality

The obvious structure for Chapter 24 is a textbook's chapter on data models: documents, then
relations, then graphs, each with its own worked example of people and their jobs. This part's
example is the shop's own metadata, one question measured in records read across the shapes, and
the index the learner adds to the table. The collector, graph, query layer and interface are the
shop's, built on its week and Part V's faults, not a reference consumer's code or API.
