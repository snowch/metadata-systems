# VERDICTS ON THE CHAPTER 24 FINDINGS

6 upheld, 9 partly upheld, 5 rejected (findings 1 to 20).

What I ran, from `/home/user/metadata-systems/notebook` with `PYTHONPATH=.`:
- `store.check` on `run_week(["returns"])` with the index variants quoted below.
- `run_week(["returns"])` against `run_week(["returns","source"])`.
- The map's text, from `figures.pipeline`.
- `app.run()` on `chapter_24.py` under marimo.

I read the chapter source, the as-built file, `shop/store.py`, the chapter's notes, `part-6/design.md`, `docs/authoring.md`, `docs/plan.md`, and Chapters 4, 7, 9 and 23.

## BLOCKING

**1. UPHELD.**
- I ran `CREATE INDEX IF NOT EXISTS edges_by_job ON edges(job)`, then the same statement with `(dataset)`. The second does nothing. The check stays at "reads every row of `edges`", 154 rows.
- The stub is the only way the learner can follow the page's "Change `job` to the column your query looks up". A reader who does exactly that sees nothing change.
- The page also says the plan names `edges_by_dataset`. The plan names whatever the learner called the index.
- Fix: the starting cell must not collide with the finished one, so changing only the column works. A starting index name that cannot pre-exist is one way. The page then must not name the index, or must say the plan shows the learner's own index name.
- `STUBS["index"]`, `REFERENCE["index"]` and their tests, and the smoke test that types the reference in, change with it.
- Authoring rule: the starting cell runs and answers wrong. It must stay that way.

**2. UPHELD, on the engine count. The page change is not needed.**
- Confirmed. For a query with `edge = 'reads' AND dataset = :dataset`:

  | Index | Result printed | Plan | Real count |
  |---|---|---|---|
  | `edges(edge)` | 11/11, "0 rows read" | `SEARCH ... (edge=?)` | 8 per query |
  | `edges(edge, dataset)` | 11/11, "0 rows read" | `SEARCH ... (edge=? AND dataset=?)` | fewer than 8 per query |
  | `edges(dataset, edge)` | 11/11, 14 | `SEARCH ... (dataset=? AND edge=?)` | fewer than 14 |

- `rows_read` looks the first index column up in `params`. `edge` is never a parameter, so it counts `edge = NULL`.
- A plausible attempt gets a false number with no message. That breaks "a number is a number the engine produced".
- Fix: count the rows the index search matches, from every column the plan binds, using the query's own values (including the literal `'reads'`). Add a test for an index on `edge` and one for a two-column index.
- Two corrections to the finding. The `reads` rows number 8, not 7. I would also not change the page's "the column your query looks up". With a correct count, an index on `edge` is an instructive result: it is used, and it narrows little.

**3. UPHELD.**
- "Each shape reads few records for the questions its structure was built for, and many for the others" is false for the graph, which reads 2 and 2 in `compare`.
- It is misleading for the table. The 14 for a program's question comes from there being no index on `job`, not from the table's shape. The learner's own starting cell was an index on `job`.
- It is also a slogan (AGENTS rules 3 and 9).
- Fix: delete the sentence. Say what each measured count came from. State, without a new number, that the table has no index on `job`. The "helps the dataset's question, not the program's" sentence needs that qualifier.

**4. UPHELD.**
- Both cross-references are wrong.
- Chapter 9's week is `["returns","source"]`: 17 edges by job, 12 datasets (`chapter_09.py` lines 97 and 298). The 14 edges and 11 datasets are Chapter 23's week (`chapter_23.py` lines 83 and 91).
- Chapter 23's three projected questions (latest run of a job, one day's events, what is downstream) do not include "what reads a dataset".
- Fix: attribute the 14 edges to Chapter 23's week, or say it is Chapter 9's week without `source`. Say what Chapter 23 projected in its own terms.
- The same wording is in `shop/store.py`'s docstrings, `docs/notes/chapter-24.md` and `part-6/design.md` ("Chapter 9's edges (14)"). Update them too.

## SHOULD

**5. PARTLY UPHELD.**
- Stands: the prediction cannot be reasoned to. The page never says the table has no index, and the learner might assume SQLite builds one. State the table's condition before asking.
- Chapter 23's "ways that read every stored event" lets the learner infer the answer once it is stated, so nothing is given away.
- Rejected: "Compare this with what you wrote" is the convention of Chapters 18 and 19 and 21 to 28. The following sentence ("The plan is a scan: SQLite reads each row...") already states the correct conclusion for someone who predicted the other way.

**6. PARTLY UPHELD.**
- `doc["reads"]` does raise `KeyError` on dataset documents.
- One clause is enough: only a program's document has `job` and `reads`. The printed list already shows it.
- No change to the check. A traceback the learner can read is fair engineering.

**7. UPHELD.**
- Confirmed. The store's 11 datasets include `r-203.json` (removed in Chapter 9's week) and exclude `products.csv`.
- The map shows `r-201`, `r-202`, `r-204` and `products.csv`. The printed list shows four return files against the map's three.
- The counts agree (11), so the reader is unlikely to see why the lists differ.
- Fix: one sentence saying the store holds the datasets that the edges name, so the lists differ from the map's assets.
- Folds in finding 15's wording (see 15).

**8. PARTLY UPHELD.**
- Stands:
  - `Documents.get` scans the list but counts 1. No key is built.
  - `Graph.edges_at` scans all edges but counts only the matches.
  - Index steps are not counted. Chapter 23 counted about 30.
  - So "Finding `build_daily_sales` takes 1 document read" assumes a keyed lookup nobody built.
- Fix: add a bullet to "How this differs" saying that finding a document, a node or an index entry is counted as free, unlike Chapter 23.
- Stands: "fast to follow lineage several steps: each step is quick" is circular and unmeasured. Say what it needs (a node's edges per step) and that the chapter measured one step.
- Stands: "Each shape here meets some of these readings and not others" never says which. `design.md` promises that it does, and CLAUDE.md's step 5 requires it. Name, from the measured counts, which shape serves which reading, and the one reading not measured.
- Rejected: "Each reads 2 records for `clean_orders`" is measured and is labelled as such.

**9. PARTLY UPHELD.**
- Stands: all four readings are about which operation is fast. None is about time or size, though "fast" most plainly means those.
- Add one reading with what it needs: fast enough as the assets grow. That needs counts at size, which Chapter 23 projected, and time, which this chapter does not measure. A bullet is enough.
- Rejected: a new figure or measurement. The step-5 half is covered by 8.

**10. PARTLY UPHELD.**
- Stands: a document, a row and an edge are different sizes, and the closing sentence adds them as "records".
- One clause fixes it: the counts compare how many items are opened, not their size.
- Say "rows" for the table.
- This also removes the unprompted "the size of each shape" in the closing (finding 17).
- Rejected: "154 is 14 read 11 times". The page already says "14 for each of the 11 datasets".

**11. REJECTED.** `docs/plan.md` line 163 lists "JSON documents, then tables, then an indexed store, then a graph". The chapter follows the recorded design. Chapter 23's closing says the same.

**12. PARTLY UPHELD.**
- Confirmed: the four totals appear twice, after the graph and in "Before Chapter 25". "The index did not help the program's question" also appears twice.
- CLAUDE.md allows the closing summary but says "said once". Keep the numbers where the evidence first arrives, after the graph, and have the closing state the conclusions without repeating the totals.
- Which of the two to cut is the author's call.

**13. PARTLY UPHELD.**
- Confirmed. The check never runs a query that has no `:dataset`. It treats it as giving no readers, and the "yours" column is blank.
- "It selects every row's `job`, and the check finds 3 of 11 right" describes a result that was not computed.
- Fix: say that the check does not run a query without `:dataset`, and that the 3 are the datasets no job reads.
- The engine's message is fine.

**14. UPHELD.**
- `docs/sources.md` has nothing on `EXPLAIN QUERY PLAN`, `SCAN` or `SEARCH ... USING INDEX`. I grepped for "plan", "explain", "SCAN" and "Chapter 24". Its only SQLite entries are about the warehouse (line 134) and the Pyodide build (line 414).
- The page and the engine rely on the plan's wording, and CLAUDE.md requires a source for each technical claim.
- Add an entry from SQLite's own documentation, and record what it says about the plan's output format being for humans and not stable between versions. I believe it says so, but I could not check it here, so read the source.
- Add a test that pins the plan text the engine parses for the scan and the search case. Pyodide's SQLite may differ from CPython's.

## COULD

**15. PARTLY UPHELD.**
- Confirmed. The documents carry only `means` and `responsible` for two datasets. Chapter 4's other lines (column meanings, `clean_*` and `products.csv` responsible lines) are not in the store. The `descriptions` table is created but never queried on the page.
- Stands: the claim "the descriptive lines that Chapter 4 ended with" overstates. Say it holds two datasets' `means` and `responsible` lines. Do this in the sentence from 7.
- Rejected: adding a question that uses the descriptions. That is a new feature the chapter does not need.

**16. REJECTED.**
- `docs/authoring.md` says "The page says what the code must do, never the code itself". The sentences name conditions and not syntax.
- The chapter's decisions are the prediction and the requirement.
- Part VI's design deliberately keeps each piece to a few lines.

**17. PARTLY UPHELD.**
- Stands: "asset" and "dataset" are used interchangeably in the fast bullets, and "the size of each shape" is unprompted. Make the bullets say "dataset" where they mean one, and drop the size mention as in 10.
- Rejected:
  - "Each shape answers one question" and "keeps both ends" are idiomatic descriptions of a structure, not personification.
  - Renaming the `edge` column touches the engine, tests and Chapter 9's vocabulary for little gain.

**18. REJECTED.**
- Rerunning only the documents check after the graph cell does call the wrong `readers_of`. Run below is the instruction, so the order is always right.
- The duplicate name stops `marimo run` with `MultipleDefinitionError`, but the chapter is built to ipynb and marimo never reaches the reader (`build_ipynb.py` header). A rename touches prose, stubs, tests and smoke for a rare path.

**19. REJECTED.**
- The reviewer did not inspect a browser and offers no evidence.
- The Notebooks smoke test already holds "a printed file keeping one record per line" at phone width.

**20. REJECTED.**
- `compare` is an instrument. The chapter already has a prediction on the same mechanism (a `WHERE` clause without an index).
- The result follows from "an index on a column serves a lookup on that column", and findings 1 and 3 make the page state it exactly. A second prediction cell and a new notes block cost more than they add.

## Order of work
1. Code first: findings 1 and 2, with their tests, and the plan-text pin from 14.
2. Fact briefs for the page changes: 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15 and 17.
3. Add the source entry (14) and fix the notes and docstrings (4).
4. Read the whole chapter once more from the built notebook.

Pinned sentences in `notebook/tests/test_words.py::test_chapter_24` will need updating with the wording changes.
