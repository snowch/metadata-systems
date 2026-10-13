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

### `record`

- **Role:** inspect
- **Serves:** what does a tracker keep about a run's training data?
- **Why now:** the prediction is about this record.

### `which-rows`

- **Role:** experiment
- **Objective:** the reader finds that a run's record of its data is a fingerprint, which can test a
  guess about the rows but cannot give them back.
- **Known before:** Chapter 2's note on tables that keep history; Chapter 15's provenance.
- **Driving question:** can the record tell you which rows the forecast was trained on?
- **The action:** write the prediction; read the comparison; change the condition until the digest
  matches.
- **Why the action:** only a tested guess turns the digest into evidence.
- **Evidence:** different digests; then the recorded one for the rows up to Friday 11.
- **Consequence:** a digest shows change and tests a guess; a snapshot or a version is needed to
  give the rows back.
- **Predictable:** partly; the record's fields are on the page.
- **Gives nothing away:** the cell asks whether; the comparison comes after.
- **Not knowing:** fair.
- **Next question:** what does a digest read?

### `cap`

- **Role:** experiment (completes `which-rows`)
- **Evidence:** changing the first row changes the digest; changing row 10,001 does not.

## Requirements

"Record the training data of the model." (the plan's). Readings: the snapshot it read (a version or
time, and a table that keeps history); the query that chose it (text and time); the features (code
and values). The tracker's record meets a narrower reading: which table, and whether it changed. The
figure that questions it is the free-text cell after the box.

## Originality

The obvious examples are an experiment tracker's tutorial: a classifier trained on a public
dataset, its parameters and metrics logged. This chapter trains nothing worth the name: a mean of
3 days of the shop's own revenue, so that the record, not the training, is the subject, and the
digest is tested against the shop's own table as it grows.

## What the prose process caught

Brief P32 (`part-7/briefs/`), draft `part-7/drafts/P32.md`. Fixed with the fewest words, as
placement edits (`place_p7.py`): a "The question:" label at the head of two of the reader's cells in
Chapters 31 and 32; a fragment introducing Chapter 31's list of rules; "sets" for "holds" of a cell in
Chapter 29; and Chapter 30's first mention of the provider, which now names it and Chapter 29. In
Chapter 32 the draft put "the forecast" for "a trained model", following the brief's rule on "model";
kept.

## Measured

Locally, 13 October 2026, before the review (`docs/notes/notebook-prototype.md`, "Chapters 29 to
32"): from Chapter 31's link, 11 files, 0.31 MB, in a new tab; Run all 8.7 to 9.5 s; peak memory 390 to 401 MB alone, 614 MB with Chapter 31 open; no
error output, no console error. The browser test types the reference into the chapter's cell and
reads the check.
