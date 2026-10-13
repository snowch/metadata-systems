# VERDICTS ON THE CHAPTER 32 FINDINGS

**Count: 6 upheld, 12 partly upheld, 6 rejected (24 findings).**

**What I ran and read.**
- I ran `shop.ml.train`, `record`, `today` and `check` from `/home/user/metadata-systems/notebook`. The numbers match the as-built page: forecast 13650, digests `60ba54ee` and `6b0727dc`, 5 and 7 rows.
- I checked the double full stop and the empty-condition message by running `check` on `day<='2026-09-11';` and on an empty string.
- I read MLflow at `9d651c2` for `digest_utils.py`, `pandas_dataset.py`, `spark_dataset.py`, `dataset.py` and `entities/dataset.py`.
- I read OpenLineage `DatasetTypeDatasetFacet.json` at `60261f0`.
- I read the Chapter 32 notes, `design.md`, `research/chapter-32.md`, `sources.md` "Read for Part VII", the closings of Chapters 29 to 31, and `authoring.md`.
- To fetch the upstream sources I wrote copies of the MLflow files into the scratchpad. I wrote nothing in the repository.

## BLOCKING

**1. No statement that nothing real runs, and no commit named. PARTLY UPHELD.**
- Upheld: Chapters 29 to 31 each say a cell applies a rule as the code states it. Chapter 32 says nothing of the kind. "The run is recorded with the fields MLflow … keeps" reads as if MLflow recorded it. The model-versus-reality bullet "follows MLflow's rule" never says that the cell applies a rule and is not MLflow.
- Fix: one sentence near the first cell, one in the closing, and one in the note. Use the siblings' form: the cell applies the rule as the code states it, in the version read.
- Not upheld: "Name the commit, as chapter 31 does." Chapters 29 to 31 name no commit on the page; I grepped for hashes and found none, only "in the version read". The commit is in `sources.md`. Naming it would break the part's pattern.
- Downgraded from BLOCKING to should-fix. Nothing on the page is false; it is incomplete against the design rule.

**2. "A digest shows a change only within the rows it reads" is wrong. UPHELD.**
- I confirmed it in `compute_pandas_digest`. The digest hashes the first 10,000 rows, `np.int64(len(df))` and every column name. A row appended after row 10,000 changes the count, so it changes the digest. Only an in-place edit beyond the cap goes unseen.
- The shop's own `digest` does the same (`rows[:MAX_ROWS]`, `len(rows)`, column names).
- The closing line "did not change when a later row did" has the same fault, and so does the aphoristic sentence.
- Fix: say exactly what is outside the digest, a value changed in place past row 10,000. Say that the row count and the column names are inside it.
- The type-dropping point is optional. It would help answer the closing question about what a digest leaves out. Chapter 32's shop digest does not drop types, so if it is mentioned, say it is MLflow's rule only.

**3. "The record has 5 rows" and "The record lists no rows"; "the table" used for two things. UPHELD.**
- The page contradicts itself. The record holds a count, and `daily_sales` holds rows. "The table" means both the printed table and `daily_sales`, which `CLAUDE.md` lists as a two-meanings fault.
- Fix: the record "counts 5 rows" or "holds a count of 5", and `daily_sales` "has 7 rows". Use one noun for each.

## SHOULD

**4. MLflow's digest rule is stated of MLflow in general. UPHELD.**
- `sources.md` and the code support it only for a pandas table. In `spark_dataset.py` the digest is `get_normalized_md5_digest([np.int64(semantic_hash)])`, a hash of the query plan that reads no rows.
- Fix: qualify with "for a table held as a pandas table". Say the shop's cell imitates that dataset type.

**5. "Computes its digest the same way." PARTLY UPHELD.**
- The shop hashes JSON text of values plus `str(len)`. MLflow hashes `hash_pandas_object` values, which include the index, an `int64` count and the column names, and it drops columns that are not text or numeric. "The same way" overclaims.
- The next sentence already says the shop's value is not MLflow's, so the harm is small.
- Fix: replace "the same way" with the three-part rule (the first 10,000 rows, the count, the column names). Optionally mention in the note that the row hashing and the column filter differ.
- This merges with finding 4.

**6. The record's fields are the shop's simplified versions. PARTLY UPHELD.**
- Confirmed in `entities/dataset.py`: the entity has `source_type`, and `schema` and `profile` are strings. `PandasDataset.profile` has `num_elements` as well as `num_rows`.
- I did not verify the `{"mlflow_colspec": ...}` shape of the schema string. I did not verify that `warehouse://` is not an MLflow source form. Do not assert either without reading them.
- Fix: one line in the model-versus-reality note. The shop's record keeps fewer fields than MLflow's and shows `schema` and `profile` in its own simpler form.

**7. Forecast 13650 and version 1: no cell shows them, and `sources.md` lacks the registry link. PARTLY UPHELD.**
- Confirmed: `record` prints only the input. Nothing on the page uses the forecast value or the version again.
- Confirmed: "Read for Part VII" has only the digest rule and the dataset and `log_input` facts. It has nothing on the model version's `run_id`, or on the entity's `schema`, `profile` and `source_type`. Research items 1.5 and 1.13 have them.
- Fix, required either way: add those entries to `sources.md`.
- On the page, choose one:
  - Cut "It comes to 13650 pence", since nothing uses it. Show or cut "the version names the run".
  - Prefer showing the version's three fields. The link from the model to the run to the input is what the requirement "training data of the model" needs. It is a small `Rows` from `train()["version"]`, not a new figure.

**8. "Rows the forecast was trained on" is used for 5 rows and 3 rows. PARTLY UPHELD.**
- The finding is right that the page says "mean of the last 3 days" while the record and the check cover all 5 rows the run read. A "last 3 days" condition gives "Your rows (3) … `750e36ed`", which I ran.
- It is partly handled: the instruction says to keep "the rows the table held on Saturday 12 at 09:00", which points to 5.
- "The same text run on Monday reads 7 rows, not 5" assumes an unstated query.
- Fix: one clause saying the run reads all the rows the table holds, 5, and takes the mean of the last 3. That also makes the "same text … 7 rows" line consistent.
- No new figure is needed.

**9. The first prediction is answerable from the page. PARTLY UPHELD.**
- The convention that answer cells print below the prediction is not the fault, and I do not count it against the chapter.
- The finding is partly right. The record is printed above with no rows in it, and the line "The profile holds the number of rows: 5" follows. "Can the record tell you which rows?" is answerable by reading.
- It does not ask about the belief the chapter turns on, which is whether the data is still as it was.
- Fix: redirect the prediction to a result the learner has not seen. For example, whether Monday's `daily_sales` will still match what the run recorded, and what that would show. This is the "effect before cause" order. Put no option text that holds the answer.

**10. The page never says what a passing check does not show. UPHELD.**
- The match depends on `daily_sales` only ever being appended to. Had a row been updated or deleted, no condition would match, and the record could not say why.
- The page says only that the nightly run "leaves the other rows as they are" and that a match is "strong evidence". The surprise the course wants, what the data cannot tell, appears only in the cap section, and is misstated there (finding 2).
- Fix: after the check, state what the match relied on and what a changed or deleted row would leave unanswerable. Do not state which reading of the requirement that favours.

**11. Requirement section. PARTLY UPHELD.**
- Upheld: "three things" followed by "a narrower reading" counts as a fourth. `authoring.md` asks the page to say which readings the record answers, and whether the requirement is met as written. Chapters 30 and 31 do this in one sentence. Chapter 32 does it only half way.
- Fix: say what the record meets and what it does not, in terms of the three readings. Say "this record", not "the tracker's record". MLflow params, tags and artifacts could hold a query.
- Rejected: linking "the model" and "the forecast". The requirement is the plan's wording, and the connection is obvious on the page.

**12. `source` unexplained; `digest` used before it is defined. PARTLY UPHELD.**
- Upheld: `source` is the field that explains why a digest is needed at all. It says where the table is and holds no rows. One sentence after the record table is enough. Do not say it is a pointer to the table "as it is now"; that is an inference from `load()`, per research 1.7. Say it names where the data is kept.
- Rejected: the order of the `digest` definition. The definition follows the record table directly.
- Rejected: the clash with Chapter 6's "source". The field name is a tracker's, in code font, used as a name.

**13. "ML and AI" covers one training run. PARTLY UPHELD.**
- The plan row lists embeddings, vector indexes, retrieval and generated artefacts. `design.md` narrowed the chapter to one forecast run, and that is a recorded decision.
- The closing lists evaluation, use and prediction as left out, but not the rest.
- Fix: add one clause naming embeddings, vector indexes, retrieval and generated artefacts as not shown. Do not add content. The research found no standard record for them in the projects it read.

**14. No link to the learner's run events (Chapters 7 and 8). PARTLY UPHELD.**
- Rejected: a new figure or engine feature. The cost is not justified.
- Accepted: one sentence in the model-versus-reality bullets, merged with finding 15. The run's input would be `daily_sales` as an input dataset, as in Chapter 8. `DatasetVersionDatasetFacet` gives a version as free text with no defined meaning, so it is the nearest standard place for "which version". Both facts are in `sources.md`.

**15. The OpenLineage `MODEL` claim. UPHELD.**
- Confirmed in `DatasetTypeDatasetFacet.json`: `datasetType` is a string with the description "Dataset type, for example: TABLE|VIEW|FILE|TOPIC|STREAM|MODEL|JOB_OUTPUT". `MODEL` is an example in a free string, not a defined meaning.
- Fix: say the facet lists `MODEL` among its examples, so a run could name the forecast as a dataset it writes. That is a possible use, not a specified one. No commit on the page (see finding 1).

**16. The failure line does not say what to look at. PARTLY UPHELD.**
- The mismatch message gives the learner's row count and digest but not the run's row count.
- Fix: add the run's row count to `match_no`, for example "the run read 5". That is evidence already on the page, not the answer. It needs the message changed in `ml.py` and its pin in the tests.
- Rejected: stating the 02:30 run time. The learner has the nightly schedule from earlier chapters, and the inference is the exercise.

## COULD

**17. Digests differ, but the row counts already show the change. REJECTED.** The digest is the general change test, and the chapter is about the digest. The cost of cutting exceeds the gain.

**18. "row 10,001" in the prose, "row 10001" in the table; "13650" against "10,000". REJECTED.** Cosmetic, and the table label comes from the engine. If finding 7 cuts 13650, the point disappears anyway.

**19. The `today` table has an empty first column header. REJECTED.** An unlabelled row-label column is an ordinary table form. It would also need a header change in the engine and its pin.

**20. Message bugs. PARTLY UPHELD.**
- Upheld: I confirmed the double stop, "You can only execute one statement at a time..", for a condition ending in `;`. Strip the trailing stop from SQLite's text, or drop the added one.
- Rejected: the empty-condition message. It mentions `ORDER`, but it still says the condition could not be run, and this is an edge case.

**21. "Next day's revenue" on a Saturday with data to Friday. REJECTED.** It is a fiction detail. The forecast is for the day after the last row, and nothing on the page depends on the date. Changing it would disturb the pinned name `next_day_revenue`.

**22. `source_type` is omitted from "the fields MLflow keeps". UPHELD.** It is an omission in a list the page states as MLflow's. It is fixed together with finding 6: either name the field or say the shop keeps a subset.

**23. The standing map line and caption are irrelevant. REJECTED.** The reviewer calls it harmless. Chapters 29 to 32 carry the same line, and the standing map is a convention of every chapter.

**24. "9 to 12 seconds" against the chapter's own 8.7 to 9.5. REJECTED.** The callout is shared by Chapters 29 to 32. The 12 comes from the published pages' range in `notebook-prototype.md`, and the note's figure is a local measurement. Changing one chapter would make them differ.
