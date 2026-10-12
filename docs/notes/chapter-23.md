# Chapter 23: Metadata at scale

A working note. Written on 12 October 2026 with Chapters 18 to 22 (`notebook/chapter_23.py`).

## What the chapter does

- measures the week: 11 assets, 6 jobs, 34 runs, 68 events, 67 edges by run, 14 edges by job,
  7 days, 1492 bytes an event; and how much of the job graph a traversal downstream from each
  dataset follows: 0.43 from `orders.jsonl`;
- predicts which ways of answering three questions pass a limit of a million records read first, as
  the platform grows in powers of ten to ten million assets at the week's rates, every event kept
  90 days, and a traversal limited to 4 steps of at most 3 edges each; runs the projection: the two
  ways that read every stored event pass it at 100,000 assets (somewhere above 10,000); stored by
  day, and downstream to the end, at ten million; sorted by job and time (31 records read: about 30
  steps down the index and one record), or four steps (81 edges), never; meets **index** and
  **partition**;
- deletes events older than three days on Monday morning (**retention**), as a stand-in for 90 days,
  which would delete the same run after 14:20 on Monday 7 December; finds `r-201`'s row still in
  `returns`, read by Chapter 10's `returned_quantity(7004, 2)`, with the run that wrote it gone;
  folds runs' edges into job edges first (**compaction**) and keeps that `record_return` read the
  file;
- questions "Keep lineage for 90 days."

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `measured`

- **Role:** inspect
- **Serves:** what does one week of the shop's metadata amount to? The counts and the reach that
  the projection scales.
- **Why now:** the projection's rates come from these rows, and the page says which.

### `first-over`

- **Role:** experiment
- **Objective:** the reader discovers that the question that fails first is a simple one asked
  without the structure that serves it, not the deep traversal.
- **Known before:** the measured week; Chapter 9's graph; Chapter 13's latest run.
- **Driving question:** which question reads more than a million records first?
- **The action:** write in a free-text cell; read the first size each way passes the limit, then the
  projection's numbers at every size.
- **Why the action:** the counts are arithmetic on rates the page states; doing it before reading
  is the reasoning.
- **Evidence:** the two ways that read every stored event at 100,000; the others at ten million or
  "not within 10,000,000".
- **Consequence:** a structure (index, partition, depth limit) is a precondition, not a tuning.
- **Predictable:** yes, with arithmetic.
- **Gives nothing away:** the cell asks which ways, and the table's labels are plain ("sorted by job
  and time", "stored by day") until the terms arrive after it.
- **Not knowing:** fair.
- **Next question:** what does keeping less cost?

### `retention`

- **Role:** a demonstration, completing `first-over`'s question of what keeping less costs; it takes
  no prediction.
- **Objective:** the reader finds that deleting events by age deletes the record of how a row still
  in use was made, and that folding edges by job first keeps that the file was read, not by which
  run.
- **The action:** read the cell that keeps three days of events, the row in `returns`, and the
  compacted edges.
- **Evidence:** 68 events, 28 kept; no edge by run names `r-201.json`; the row is in `returns`; one
  edge by job after compaction, 1 run, 14:20:05 on Tuesday 8.
- **Next question:** what does "keep lineage for 90 days" ask for?

## Requirements

"Keep lineage for 90 days." Readings, as questions: can I see the last 90 days' events (retention by
age); can I see which jobs read and wrote which assets in 90 days (compaction first; jobs, not
runs); can I see how every asset still in use was made, however old (a record of use, which the
shop does not keep). With 90 days' retention, the run that wrote `r-201`'s row would go on 7
December while the row stays. The figure that questions it is the free-text cell after the box.

## Originality

The obvious examples are a database's indexing tutorial and a time-series store's retention
policies. This chapter's numbers are the shop's own week projected by a model the chapter states;
its limit, depth limit and edges a step are the shop's assumptions, labelled as such. *Compaction*
here is the shop's fold of runs into job edges, not Kafka's log compaction, which the reality note
names (`docs/sources.md`).

## What the prose process caught

Brief S, draft `part-5/drafts/S.md`; the review's changes through brief S-rev, draft
`part-5/drafts/S-rev.md`. In the revision, two sentences in a row began "The next cell"; joined.
"The shop records which assets are in use nowhere" put its adverb last; reordered.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 21 findings (`review/verdicts.md`): 6 upheld, 10 partly, 5 rejected. Read whole again after the fixes, with each
cell's output (`review/chapter_23-after-review.md`). Acted on:

- 3 days stood in for 90 without saying so; the page says it, and when 90 days would delete the
  same run;
- the readings are questions with what each needs;
- "never" showed as NULL; `first_over` labels it "not within 10,000,000", and the ways' labels are
  plain words, so no term appears before its definition;
- the sizes are powers of ten, so "first size", not the exact crossing (about 12,600 assets);
- the fan-out of 3 and the constant 0.43 are stated, and in the reality note; 31 is records read,
  about 30 steps and one record;
- `r-201`'s row is shown, and "in use" means Chapter 10's function reads it; keeping the folded edge
  is the shop's rule, the cell deleted nothing;
- *traversal*, *edges by run* and *edges by job*, as Chapters 5 and 9 named them, in the prose and
  in `measure`'s columns; Chapter 24 named by what it builds; writes and index upkeep not counted;
  compaction's other meaning noted, with its source.

Rejected, with the sceptic: projecting storage size, rounding the engine's numbers, a note on the
week's variant, and a more literal heading.

## Measured

Locally, 12 October 2026, before the review's changes (`docs/notes/notebook-prototype.md`,
"Chapters 18 to 23"): from Chapter 22's link, 11 files, 0.31 MB, in a new tab; Run all 8.1 to 8.3 s;
peak memory 395 to 398 MB alone, 608 MB with Chapter 22 open; no error output.

## Known gaps

- The projection counts records read; it is a model of growth, not a measurement of one.
