REVIEW OF CHAPTER 24, "Build the metadata store"

Numbers checked: I ran every stub and every REFERENCE piece in `notebook/shop/store.py` through `store.check` and `store.compare` on `shop.run_week(["returns"])` (from `/home/user/metadata-systems/notebook`, with `PYTHONPATH=.`). I also ran several plausible wrong attempts. I also checked edge and dataset counts against Chapters 9 and 23, the map's text against `figures.pipeline`, and the notes, `docs/plan.md`, `docs/lab.md`, `docs/sources.md` and `docs/notes/part-6/design.md`.

These figures match the engine:
- 17 documents (6 programs and 11 datasets), 3/11 then 11/11, 187 documents read.
- Table: 3/11, then 11/11 with 154 rows read.
- Index on `dataset`: 14 rows, with `edges_by_dataset`.
- Graph: 6/11, then 11/11 with 14 edges.
- `compare`: 17/2/2 and 1/14/2.

The as-built file drops the check's summary line (for example "3 of 11 datasets right; 154 rows read in all. The query reads every row of `edges`."). I read those lines from the engine instead.

## BLOCKING

**1. The index cell breaks when you do what the page says.**
- Page: "The next cell creates an index on the column `job` of `edges`. Change `job` to the column your query looks up. Select the cell and press **Run below**".
- Page, after the check: "The plan looks the rows up through the index `edges_by_dataset`."
- The starting cell is `tables.sql("CREATE INDEX IF NOT EXISTS edges_by_job ON edges(job)")`. Run all has already created `edges_by_job` on `job`.
- If the reader changes only the column, the statement becomes `edges_by_job ON edges(dataset)`. `IF NOT EXISTS` then makes it do nothing.
- I ran it: the check stays at "reads every row of `edges`", 154 rows, with the index apparently corrected.
- Only a reader who also renames the index sees the result the page describes. Even on a fresh run, the plan line would name `edges_by_job`, not the `edges_by_dataset` the page names.
- Direction: the page must say the index name matters, or the starting cell must not collide with the finished one. There is also no way to drop the index.

**2. The row count is wrong for other indexes a reader might reasonably choose.**
- `rows_read` takes the first column of the index and looks it up in the query's parameters. Only `:dataset` is a parameter.
- The page lists `edge` first in the WHERE conditions, and says "the column your query looks up", which is ambiguous with two conditions.
- I ran `CREATE INDEX i ON edges(edge)` and `edges(edge, dataset)`. Both reach 11/11 and print "0 rows read" with "uses the index `i`". That is wrong: the plan really does search by `edge`, which would read the 7 `reads` rows per query (11 of 11 right, so the count is the only error).
- `edges(dataset, edge)` prints 14, but the rows matching both conditions are fewer.
- A plausible attempt gets a false number and no message. Fix the engine counting (or the check's message). Name the column unambiguously on the page.

**3. A conclusion contradicts the chapter's own result.**
- Page: "Each shape reads few records for the questions its structure was built for, and many for the others."
- The graph reads 2 and 2 for both questions in `compare`, and the page says so just above: "both questions read only one node's edges."
- The table's 14 for the program question comes from having no index on `job`, not from its shape. The learner's own starting cell was an index on `job`, which would serve that question.
- The sentence is false for the graph and misleading for the table. It is also a slogan-style generalisation (AGENTS rules 3 and 9).
- The same applies to "The index on `dataset` helps the dataset's question, not the program's". Say what the table reads without an index on `job`, and that an index on `job` is possible.

**4. Cross-references to Chapter 9 and Chapter 23 are wrong.**
- Page: "the week's 14 edges by job (Chapter 9, the week with the returns desk)" and "compares each answer with Chapter 9's edges".
  - Chapter 9's week is `run_week(["returns","source"])`, with 17 edges by job and 12 datasets, because of the analyst's script. I ran both weeks.
  - The 14 is Chapter 23's week (`run_week(["returns"])`).
- Page: "Chapter 23 projected what the same questions read at 10,000,000 assets."
  - Chapter 23 projected three different questions: the latest run of one job, one day's events, and what is downstream of an asset. None of them is "what reads a dataset".

## SHOULD

**5. The prediction before the table cannot be answered from the page.**
- Page: "write in the next cell whether a query for one dataset's readers will read every row of `edges`, or only that dataset's rows."
- Whether it reads every row depends on whether the table has an index. The page does not say it has none until the index section.
- Direction: state the table's condition before asking, so the learner can reason to a belief.
- The follow-up, "Compare this with what you wrote.", does not say what a reader who wrote the other option should conclude (AGENTS rule 7). It is also filler.

**6. A natural first attempt crashes with a bare KeyError.**
- Page: "adds the document's `job` when the document's `reads` lists the dataset".
- Dataset documents have no `reads` key, and the page only says they hold "descriptive lines, where it has any".
- `if dataset in doc["reads"]` raised `KeyError: 'reads'` in my run, with nothing from the check.
- Direction: say that only program documents have `reads`.

**7. The 11 datasets in the store are not the 11 assets on the map.**
- Caption: "object storage holds three return files". The map I rendered shows `customers.jsonl`, `orders.jsonl`, `products.csv`, `r-201`, `r-202` and `r-204` ("6 files + 4 tables + 1 dashboard = 11 assets").
- The store's 11 datasets include `r-203.json` (deleted) and exclude `products.csv`. Four return files are listed in the printed documents.
- The numbers happen to agree, so the difference is invisible. A reader will compare the printed list with the map.
- Direction: say which datasets the store holds and why. Datasets are those named by edges.

**8. Unmeasured claims in "A fast store".**
- Page: "Finding `build_daily_sales` takes 1 document read" and "a key for each document, or a lookup by name".
  - No key is built.
  - `Documents.get` scans the list but is counted as 1 by fiat.
  - The `compare` cell measured what the program reads, not finding it by name.
- Page: "Each reads 2 records for `clean_orders`".
  - This is measured, but only for the one question.
- Page: "fast to follow lineage several steps: each step is quick."
  - Nothing here measures it. It is circular: a step is "quick" because the step is quick.
- Page: "Each shape here meets some of these readings and not others."
  - `design.md` promises that "the page says which"; the page does not.
- The graph's node lookup and the document key are counted as free, which gives them an index nobody built. The "How this differs" note should say so.
- Chapter 23 counted index steps ("about 30 steps down the index, then one record"). Chapter 24 counts only the matching rows. Say so.

**9. The requirement exercise leaves out the reading its own check cannot reach.**
- "Fast" most plainly means time, how fast and for how many assets. All four listed readings are about which operation is fast.
- The chapter closes with "The check could not show the time each shape takes", so it measured nothing about time and does not link "records read" to "fast".
- The five-step pattern (what it needs, what the platform records, which readings are met) is only half done compared with Chapter 23's box.

**10. Unlike units are summed as if equal.**
- Page: "the documents read 187 records, the table with no index 154, the table with an index on `dataset` 14 and the graph 14."
- A document (whole program, with lists), a row and an edge are not the same size. The page says nothing about that, though it does say "the size of each shape" was not shown.
- Also: "records" is used for all three, and the table's "154 rows" is 14 rows read 11 times. Say "rows read".

**11. "Four shapes" is really three.** "One question, four shapes" and "The fourth shape is a graph". The table with an index is the same table, and the index section never calls it a shape. The Objectives and "Before Chapter 25" repeat the four.

**12. The totals are repeated.**
- Page, after the graph: "For this question, over all 11 datasets, the table with the index and the graph each read 14 records, the documents read 187, and the table with no index reads 154."
- Page, in the closing section: "Over all 11 datasets, the documents read 187 records, the table with no index 154, the table with an index on `dataset` 14 and the graph 14."
- "each passed the same check" and "The index on `dataset` did not help the question about a program." are also said twice. CLAUDE.md: the summary is said once.

**13. The "stub query" description does not match the output.**
- Page: "As it stands, it selects every row's `job`, and the check finds 3 of 11 right."
- The check never runs that query, because it has no `:dataset`. The "yours" column is blank. The 3 are right only because the expected answer is empty.
- The check line "The query must take the dataset as :dataset." is good. The page's sentence should match what the learner sees.

**14. Source claim not recorded.** Reading "SCAN" and "SEARCH … USING INDEX" from SQLite's `EXPLAIN QUERY PLAN` is a claim about SQLite. It is not in `docs/sources.md`; I grepped for "chapter 24" and "explain".

## COULD

**15. Descriptive lines are never used.** The chapter says "the descriptive lines that Chapter 4 ended with, for `daily_sales` and `sales_dashboard`". The documents carry only `means` and `responsible`; Chapter 4's other lines (`day means`, `revenue_pence means`, the `clean_*` responsible lines) are omitted. No question uses the descriptions table. Either use them or drop the claim.

**16. The page nearly gives the code.**
- "keeps the rows whose `edge` is `reads` and whose `dataset` is `:dataset`".
- "Keep only the edges whose `edge` is `reads`."
- The learner supplies syntax, not a decision. The thinking sits in the prediction.

**17. Wording.**
- "Each shape answers one question" and "the graph keeps both ends" are mild personification.
- "edge" means both the thing and the column (`edge` = `reads`/`writes`).
- "dataset" and "asset" are used interchangeably in the "fast" bullets.
- "The check could not show … the size of each shape" is unprompted.

**18. The two `readers_of` definitions share one name.** Rerunning only the documents check after the graph cell has run calls the graph version and fails with an AttributeError, not an "expected" row. This works only because Run below is the instruction.

**19. Phone layout.** The `print(documents)` lines run to about 500 characters (`record_return`), and the `edges` table has long URIs. This is probably fine under the smoke tests but worth checking at 360 px.

**20. No prediction before `compare`.** The surprising result (an index that does not help a program's question) is only explained after, not predicted. The page could ask the reader to commit first.

Reviewed: the whole built chapter (prose, code stubs, check output, requirement box). Not inspected: the rendered browser layout, because the review has no browser.
