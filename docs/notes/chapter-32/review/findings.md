REVIEW OF CHAPTER 32, "Metadata for ML and AI"

Numbers checked: I ran Python from `/home/user/metadata-systems/notebook` and compared the output with the as-built text. I ran `shop.ml.record`, `today`, `cap` and `train` on `shop.run_week(["returns"])`, and `check` with the stub, the `REFERENCE` condition and 8 other conditions. I also ran `rows_at` and the `daily_sales` executions. The page's numbers all match the engine, except where I say below that no cell shows them:
- Forecast: 13650 pence.
- Digests: `60ba54ee` and `6b0727dc`.
- Rows: 5 and 7.
- Cap table: `b54985ab` and `ebf8f1e4`.
- The stub keeps 7 rows and fails. Friday 11's date passes with 5 rows.

I confirmed the nightly `build_daily_sales` run appends one row and never rewrites earlier ones (`week.py`, `append=True`). I read the MLflow code at `9d651c2` (`digest_utils.py`, `spark_dataset.py`, `pandas_dataset.py`) and OpenLineage `DatasetTypeDatasetFacet.json` at `60261f0` directly from raw.githubusercontent. I also read chapters 29 to 31, chapter 2's closing note, the notes, the research note and `sources.md` "Read for Part VII". Not checked: no browser run, so the callouts and the figure are read from the source only.

## BLOCKING

1. **The page never says no real system runs here, and it names no commit.** This breaks the Part VII design rule (`design.md`, "A real system does not run in the page").
   - Chapters 29 to 31 say it ("As in Chapters 29 and 30, none of them runs here"; "The page could not show the platforms themselves"). Chapter 32 does not.
   - Quotes: "The run is recorded with the fields MLflow, an experiment tracker, keeps for a run's input" and "The forecast is registered as version 1 of `next_day_revenue`".
   - Read alone, these say MLflow recorded and registered something. The shop's code did.
   - The model-versus-reality note says "The shop's digest follows MLflow's rule" but not that every cell applies a rule and is not MLflow.
   - Direction: say once, near the first cell, that the cell applies MLflow's rule as its code states it in the version read. Name the commit, as chapter 31 does for its sources. Add the same line to the closing summary and the note.

2. **"A digest shows a change only within the rows it reads."** This is wrong, and the section's own heading contradicts it ("The digest reads only the first 10,000 rows, with the row count").
   - I read `compute_pandas_digest`. It also hashes `np.int64(len(df))` and every column name.
   - So a row appended after row 10,000 does change the digest, and so does a renamed column. Only an edit in place beyond the cap goes unseen.
   - The closing line "A digest that reads the first 10,000 rows did not change when a later row did" has the same fault.
   - This matters because the shop's table only ever grows by appending, and a reader may conclude that growth past the cap goes unnoticed.
   - Direction: say exactly what is outside the digest (a value changed in place after row 10,000). Name the row count and column names as inside it. Say that columns of other types are also left out; the code drops everything that is not text or numeric. That would also answer the closing question "what does it leave out?".

3. **"The record has 5 rows and the digest `60ba54ee`."** The next paragraph says "The record lists no rows." The record holds a count of 5, not rows.
   - The `today` table's column "rows" and the sentence "The table has 7 rows" repeat the muddle. "The table" is here both the printed table and `daily_sales`.
   - Direction: separate what the record holds (a count) from what `daily_sales` holds (rows). Use one noun for each.

## SHOULD

4. **"MLflow computes it from the first 10,000 rows, the number of rows and the column names, through MD5".** This is stated of MLflow in general.
   - `sources.md` supports it only for a pandas table. In `spark_dataset.py` the digest is `get_normalized_md5_digest([np.int64(semantic_hash)])`, a hash of the query plan that reads no rows.
   - The record's `source` is a warehouse table, which is the Spark case in MLflow.
   - Direction: say "for a pandas table". Say which MLflow dataset type the shop's record imitates.

5. **"The shop computes its digest the same way from its own rows ... because MLflow reads the rows with a library the shop does not use."** This understates the differences.
   - The shop hashes JSON text of values plus `str(len)`.
   - MLflow hashes the pandas row hashes (`hash_pandas_object`), `int64` bytes, drops non-text and non-numeric columns, and hashes the index.
   - "The same way" overclaims. The module docstring says "in MLflow's manner".

6. **The record's fields are the shop's simplified versions, and the page never says so.**
   - MLflow's `schema` is JSON with column types, `{"mlflow_colspec": ...}`. The shop's is `["day", "revenue_pence"]`.
   - MLflow's pandas `profile` also has `num_elements`.
   - MLflow has a `source_type` field the page omits.
   - `warehouse://shop-warehouse/...` is not an MLflow source form.
   - Direction: add one line to the model-versus-reality note.

7. **"The forecast is registered as version 1 ... the version names the run" and "It comes to 13650 pence": no cell shows either.**
   - `record` prints only the input.
   - `train()` computes the version and the forecast, but nothing on the page prints them or uses them again.
   - Show them, or cut the figure. If the registry link is kept, add it to `sources.md`; the research note 1.13 has it, but "Read for Part VII" does not.

8. **The central term is used for two sets of rows.**
   - The page says "the mean of the last 3 days", but the record and the check cover all 5 rows the table held. Jo's question is "which rows the forecast was trained on".
   - A learner who answers "the last 3 days" and writes `day in ('2026-09-09','2026-09-10','2026-09-11')` gets "Your rows (3) give the digest `750e36ed`, not the run's `60ba54ee`." The check gives no hint why.
   - The page does not distinguish the dataset read (5 rows) from the rows that affected the value (3), and not flagging it blurs the conclusion.
   - Related: "The same text run on Monday reads 7 rows, not 5" assumes a query that the page never states. A "last 3 days" query would read 3 rows on Monday.
   - Direction: say which query read the table, or drop the number.

9. **The first prediction is answerable from the table above it.**
   - "Can the run's record tell you which rows the forecast was trained on?" follows a printed record of six fields, none of them rows, and the line "The profile holds the number of rows: 5".
   - It tests no belief the learner cannot already read off the page. The belief that carries the chapter is about the table (whether the rows are still there and unchanged), which the prediction does not ask about.
   - Direction: ask for a belief about something not yet on the page. Do not put an answer in the options.

10. **The page never says what the passing check does not show.**
    - The guess works only because the shop's `daily_sales` is append-only. If rows had been updated or deleted, no condition would match, and the record would not say why.
    - The only caveat is the 8-character collision note.
    - The notes state the consequence ("a snapshot or a version is needed to give the rows back") but the page does not. The surprise CLAUDE.md asks for (what the data cannot tell) is therefore only in the cap detour, where it is mis-stated (finding 2).
    - Direction: after the check passes, ask what it proved and what it relied on. Do not state the answer in the prompt.

11. **The requirement section: "It could mean three things" is followed by "a narrower reading", a fourth.**
    - The page never says which reading Jo's question needed, as Chapter 2's owner example does ("Who should I ask" needed ...). It never says which reading the record satisfies, either.
    - "The tracker's record" generalises from one MLflow dataset record. MLflow also has params, tags and artifacts, where a user could log a query.
    - The requirement says "the model" and the page says "the forecast". Nothing links the two.

12. **`source` is the word that matters most to the requirement and is never explained.**
    - The record shows `source` (a pointer to the table as it is now, per research 1.7), `schema`, `profile` and `context`. Only `digest` and `profile` get a sentence.
    - `digest` is used in the intro and printed before it is defined.
    - `source` also clashes with the course's own "source" (Chapter 6's lineage source).

13. **The chapter promises "ML and AI" and covers one training run.**
    - The plan lists embeddings, vector indexes, retrieval, generated artefacts and evaluation. The closing says only "The page could not show the evaluation ..., where it was used, or what it predicted".
    - The research on LangChain and LlamaIndex went unused, and nothing says why.
    - Direction: state what the chapter leaves out, in the closing or the note.

14. **The chapter does not connect the run's input record to the learner's own run events (Chapters 7 and 8).**
    - A run's input dataset is the model-to-training-data edge the thesis names. The note says the forecast "can be named as a dataset a run writes" but nothing shows the same run with `daily_sales` as an input.
    - `DatasetVersionDatasetFacet` is in `sources.md`, and it is the nearest standard answer to "which version".

15. **OpenLineage claim: "A dataset's type may be `MODEL`, so the forecast can be named as a dataset a run writes."**
    - The facet's text is "Dataset type, for example: TABLE|VIEW|FILE|TOPIC|STREAM|MODEL|JOB_OUTPUT", a free string given as an example. The specification does not define a model as a dataset; the "so" is an inference.
    - The fact is right as in `sources.md`, but the commit should be named. The sentence should say it is a possible use, not a specified one.

16. **The check's failure line does not tell a reader what to look at.**
    - "Your rows (7) give the digest `6b0727dc`, not the run's `60ba54ee`." The run's row count is not repeated, and the page does not say to compare it with the profile's 5.
    - The page also does not give the nightly run time (02:30), so Saturday 09:00 versus the Saturday-night run is left to inference. The 7-row stub and the profile's 5 let a reader reach Friday.
    - Direction: add the run's row count to the message.

## COULD

17. "The digests differ, so the table has changed since the run." The row counts (5 and 7), shown in the same table, already say this. The digest's added value, confirming a reconstruction, comes only in the next cell.
18. "Changing row 10,001, the last" (prose) against the label "row 10001" (table). "13650 pence" has no separator but "10,000" does.
19. The `today` table has an empty first column header.
20. Message bug: "You can only execute one statement at a time.." has a double full stop (`"{error}."` plus SQLite's own stop). An empty condition prints a raw SQLite error: `near "ORDER": syntax error`.
21. "The next day's revenue" on a Saturday morning with data to Friday means Saturday's, not Sunday's. Check the intent.
22. `source_type` is omitted from "the fields MLflow keeps".
23. The standing map line "as Chapter 7 left them" and the returns-desk caption are irrelevant to this chapter. The figure is a harmless standing reference.
24. The "Time and memory" callout says "9 to 12 seconds"; the chapter's own measurement in the notes is 8.7 to 9.5 s.

Prose otherwise: plain and without slogans. The one exception is "A digest shows a change only within the rows it reads", which is wrong (finding 2) and aphoristic.
