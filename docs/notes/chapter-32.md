# Chapter 32: Metadata for ML and AI

A working note. Written on 13 October 2026 with Chapters 29 to 31 (`notebook/chapter_32.py`). It
closes Part VII.

## What the chapter does

On Saturday 12 at 09:00 the shop trains a forecast of the next day's revenue (13650 pence), and
records the run's input as an experiment tracker does. The reader:

- reads the record: name, digest `60ba54ee`, source, schema, profile (5 rows), context `training`;
- predicts whether the record can say which rows the forecast was trained on; reads the record
  beside Monday's table (7 rows, `6b0727dc`);
- changes a condition from `day <= '2026-09-13'` to Friday 11's date, and finds the recorded digest;
- reads a 10,001-row table whose last row changes and whose digest does not;
- questions "Record the training data of the model."

## What was built for it

`notebook/shop/ml.py`: `digest`, `rows_at`, `train`, `record`, `today`, `cap`, `check`, with the
condition as the reader's piece. The digest follows MLflow's rule (`docs/sources.md`, "Read for
Part VII") and is the shop's value.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `record` and `version`

- **Role:** inspect
- **Serves:** what does a tracker keep about a run's training data, and how does the model lead
  back to it (the version's `run_id`)?
- **Why now:** the prediction is about this record.

### `which-rows`

- **Role:** experiment
- **Objective:** the reader finds that a run's record of its data is a fingerprint, which can test a
  guess about the rows but cannot give them back.
- **Known before:** Chapter 2's note on tables that keep history; Chapter 15's provenance.
- **Driving question:** will `daily_sales` on Monday 14 give the digest the run recorded, and what
  would that show? (Redirected by the review: "can the record tell you which rows?" was answered by
  the record printed above it.)
- **The action:** write the prediction; read the comparison; change the condition until the digest
  matches.
- **Why the action:** only a tested guess turns the digest into evidence.
- **Evidence:** different digests; then the recorded one for the rows up to Friday 11.
- **Consequence:** a digest shows change and tests a guess; a snapshot or a version is needed to
  give the rows back.
- **Predictable:** partly; the nightly append is known from earlier chapters.
- **Gives nothing away:** the cell asks whether; the comparison comes after.
- **Not knowing:** fair.
- **Next question:** what does a digest read?

### `cap`

- **Role:** experiment (completes `which-rows`)
- **Evidence:** changing the first row changes the digest; changing row 10,001 in place does not; a
  row added anywhere would, through the count.

## Requirements

"Record the training data of the model." (the plan's). Readings: the snapshot it read (a version or
time, and a table that keeps history); the query that chose it (text and time); the features (code
and values). This record meets none of the three: it names the table, and its digest and count show whether the
rows are as the run read them. The
figure that questions it is the free-text cell after the box.

## Originality

The obvious examples are an experiment tracker's tutorial: a classifier trained on a public
dataset, its parameters and metrics logged. This chapter trains nothing worth the name: a mean of
3 days of the shop's own revenue, so that the record, not the training, is the subject, and the
digest is tested against the shop's own table as it grows.

## What the prose process caught

The review's revision: briefs `part-7/briefs/rev-common.md` and `P32-rev.md`, draft
`part-7/drafts/P32-rev.md`. One fix of mine: the draft kept the brief's "Keep:" label on the sentence it was to keep; cut. "Ask three questions:" became "Three questions:", as in Chapters 29 to 31.

Brief P32 (`part-7/briefs/`), draft `part-7/drafts/P32.md`. Fixed with the fewest words, as
placement edits (`place_p7.py`): a "The question:" label at the head of two of the reader's cells in
Chapters 31 and 32; a fragment introducing Chapter 31's list of rules; "sets" for "holds" of a cell in
Chapter 29; and Chapter 30's first mention of the provider, which now names it and Chapter 29. In
Chapter 32 the draft put "the forecast" for "a trained model", following the brief's rule on "model";
kept.

## The review

A reviewer on another model read the chapter as built (`chapter-32/review/findings.md`); an
independent sceptic attacked each of the 24 findings (`chapter-32/review/verdicts.md`): 6 upheld, 12
partly, 6 rejected. Read whole again after the fixes (`chapter-32/review/chapter_32-after-review.md`).
Acted on:

- "A digest shows a change only within the rows it reads" was wrong: the count and the column names
  are inside it, so only a value changed in place past row 10,000 goes unseen;
- the page says once that each cell applies MLflow's rules as its code states them, in the version
  read; the digest rule is stated for a pandas table, and the shop's record's missing `source_type`
  is named;
- "the record" counts rows and `daily_sales` has them; neither is "the table";
- the model's version is shown, and its `run_id` leads to the run; the forecast's 13650 pence is in
  that list, not the prose;
- the run reads all 5 rows and takes the mean of the last 3; `source` is explained;
- the prediction asks whether Monday's `daily_sales` gives the recorded digest; after the check the
  page says the match relied on the table only gaining rows;
- the readings say what this record meets; embeddings, vector indexes, retrieval and generated
  artefacts are named as not shown; the reality note places the run's input in OpenLineage and
  calls `MODEL` an example, not a defined meaning; the check's failure line names the run's count,
  and SQLite's error loses its doubled stop.

Rejected, with the sceptic: the row counts making the digests redundant, number formats in the cap
table, the empty column header, the forecast's date, the map line and the warning's seconds.

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
29 to 32"): from Chapter 31's link, 11 files, 0.31 MB, in a new tab; Run all 8.5 to 9.1 s; peak memory
392 to 398 MB alone, 617 MB with Chapter 31 open; no error output, no console error. The browser
test (`notebook/jupyterlite/smoke.mjs`) types the reference into the chapter's cell and reads the
check.

## Known gaps

- The answer cells print below each prediction once **Run all** has run, as the course's
  convention has it; raised with the author at checkpoint 5.
