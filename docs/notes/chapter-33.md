# Chapter 33: Build the whole thing

A working note. Written on 13 October 2026 (`notebook/chapter_33.py`), after the author passed plan
checkpoint 5. It is Part VIII, the course's last chapter (`docs/notes/part-8/design.md`).

## What the chapter does

The reader joins the data team of an island ferry, a second platform built on object storage whose
changes start functions, with scheduled jobs and tables over the results. Three of the operations
manager's messages on Friday 25 at 09:00 drive it. The reader:

- reads what the ferry's four systems record, and finds no record that links Tuesday's 17:30 row
  of `sailing_loads` to the batches it counted;
- questions "Record the lineage of every boarding." and writes `inputs(change)`, so that each
  function run names the batch and the version it read, and a delete names the version it removed;
  1 of 3 tests to 3 of 3;
- sends the ferry's events through the shop's collector and graph (Part VI's reference pieces);
- sets Thursday's island loads beside the harbour master's count (31/31, 14/24, 10/17), predicts
  whether any run failed (none did), questions "Alert us when a sailing's data is missing." and
  writes `suspect(run)` from the runs' own counts; 1 of 2 to 2 of 2, past a rule that also flags a
  batch with one aborted scan; reads the fields that show the rename to `scan_time`;
- predicts which of gate 2's two uploads Tuesday's 35 counted, and reads the trace: the first
  version, `15da88b56abc`, loaded before the 01:00 build; `boardings` now holds 38;
- predicts which datasets still count a deleted test batch (`sailing_loads` and the emailed report
  do; `boardings` does not), and questions "A deleted batch must leave no trace."

## What was built for it

`notebook/shop/ferry.py`: the ferry's three days (object storage, functions with their log, a
warehouse, a scheduler), its events, built with the reader's `inputs`, and the questions asked of
them: `check_inputs`, `collect`, `graph`, `edges`, `run_states`, `runs`, `check_suspect`, `fields`,
`trace`, `made_from_test`. `notebook/shop/figures.py`: `ferry_platform`, the ferry's four systems.
Every number the page states is pinned in `notebook/tests/test_words.py` (`test_chapter_33`) and
`test_engine.py` (`TheFerry`).

## Figures

### `ferry-platform`

- **Role:** reference
- **Serves:** what are the ferry's systems, and what does each hold on Friday morning?
- **Why now:** the reader meets a platform they have not seen; the figure carries its four systems
  so the prose need not. It draws no arrow from one asset to another, and its labels say that what
  the functions and jobs write is not recorded: the standing map's rule, for this platform. The
  shop's map does not appear: this chapter's platform is the ferry's.

### `records`

- **Role:** inspect
- **Serves:** which batches, and which versions, was Tuesday's 17:30 row built from? The cells show
  the triggers, the function log for that sailing and the runs of `build_loads`, and the prose asks
  the reader to look for a record that links them.
- **Why now:** it is Chapter 2's finding on a platform built another way, and the reason for what
  the reader builds next.

### `inputs`

- **Role:** experiment
- **Objective:** the reader finds that a function's run can name the version it read, and that a
  delete's run, which reads nothing, must be told to name what it removed, or the removal is lost to
  the lineage.
- **Known before:** Chapters 7 and 8's returns desk, its version facet and `remove_return`'s empty
  inputs.
- **Driving question:** how must each run's inputs be written so that a figure can be traced to the
  versions it counted?
- **The action:** change `inputs(change)`; read the check and the delete's event.
- **Why the action:** the version is on the change, not in the event, until the reader puts it there.
- **Evidence:** 38 of 38 runs without a version, and a delete that names nothing; then 3 of 3.
- **Consequence:** the trace later shows each version, or "not recorded" without this change.
- **Predictable:** yes, from the change record and the requirement's third reading.
- **Gives nothing away:** the prose names the facet's helper, not the code.
- **Not knowing:** not asked; the reader acts on a chosen reading.
- **Next question:** what does the graph built from these events hold?

### `edges`

- **Role:** inspect
- **Serves:** what did each function and job read and write? The answer the first section's records
  could not give.
- **Why now:** every later section reads this graph.

### `counts` and `states`

- **Role:** experiment (a prediction)
- **Objective:** the reader finds that data can go missing with every run finished: a failed run is
  not the only sign of a loss.
- **Known before:** run states from Chapters 7 and 13; the harbour master's count, an independent
  source.
- **Driving question:** did any run fail in the three days?
- **The action:** read the counts against `sailing_loads`; write the prediction; read the states.
- **Why the action:** the discrepancy comes first, from evidence outside the platform; the states
  answer the belief that a loss shows as a failure.
- **Evidence:** 14 against 24 and 10 against 17; every run COMPLETE.
- **Consequence:** the reader needs another signal, which the requirement's third reading names.
- **Predictable:** a reader may expect a failure; that is the belief tested.
- **Gives nothing away:** the cell asks whether; the states print below, by the course's convention.
- **Not knowing:** fair.
- **Next question:** what would show the loss?

### `suspect`

- **Role:** experiment
- **Objective:** the reader writes a quality rule from the runs' own counts, and finds that the
  obvious rule (fewer rows than scans) also flags a batch the function filtered on purpose.
- **Known before:** Chapter 14's assertions; the counts each run records.
- **Driving question:** which runs lost their scans?
- **The action:** change `suspect(run)`, read the check, change it again.
- **Why the action:** the reader chooses the threshold; the check shows what each choice flags.
- **Evidence:** 0 of 2 flagged; then Wednesday's aborted scan flagged too; then 2 and no other.
- **Consequence:** a rule has to tell a scan dropped on purpose from one lost; the batches' fields
  then show the rename.
- **Predictable:** partly.
- **Gives nothing away:** the prose says what to flag, not how.
- **Not knowing:** not asked.
- **Next question:** why did the scans not reach `boardings`? (the fields)

### `fields`

- **Role:** inspect (completes `suspect`)
- **Serves:** what changed in the island's gate 2 batches, and when?
- **Why now:** the check found which runs; this shows the cause the records hold, and the prose
  says what they do not (why the gate changed).

### `trace`

- **Role:** experiment (a prediction)
- **Objective:** the reader explains a figure from the versions its run counted, and finds that a
  correction after the build changed `boardings` and not the row built from it.
- **Known before:** the function log's times; Chapter 15's provenance.
- **Driving question:** which of gate 2's two uploads did the 35 count?
- **The action:** write the prediction from the times; read the trace.
- **Why the action:** the times allow an inference; the trace, from the reader's own instrumented
  events, records it.
- **Evidence:** the build at 01:00 counted versions `4a6121574c55` and `15da88b56abc`; `f0ff6ad37438`
  came at 07:05:02; `boardings` 38.
- **Consequence:** `build_loads` rebuilds only the day before; the row stays wrong.
- **Predictable:** yes, from the times; the trace confirms it from records.
- **Gives nothing away:** the message gives the effect (35 and 38), not which upload.
- **Not knowing:** fair.
- **Next question:** what else did a change after the build leave behind? (the test batch)

### `made-from`

- **Role:** experiment (a prediction)
- **Objective:** the reader finds that a delete reaches only what its own run changes; the figure
  and the emailed copy built from the batch still count it.
- **Known before:** Chapter 16's impact; the lineage graph.
- **Driving question:** which of `boardings`, `sailing_loads` and the report still count the test
  scans?
- **The action:** write the prediction; read the graph's downstream with each dataset's state.
- **Why the action:** the graph finds what was made from the batch; each dataset's own rows say
  whether it still counts it.
- **Evidence:** no, yes, yes; the report 22, the harbour master 17.
- **Consequence:** the requirement "leave no trace" has readings that conflict.
- **Predictable:** yes, from the build times.
- **Gives nothing away:** the cell asks which; the result prints below, by the course's convention.
- **Not knowing:** fair.
- **Next question:** what does "leave no trace" mean?

## Requirements

The plan's row for Chapter 33: the unfamiliar platform's own requirements, each questioned before
building to it. The chapter questions three, each in a box and a free-text cell, then its readings:
"Record the lineage of every boarding." (per scan, per batch, per version; the page builds to the
third), "Alert us when a sailing's data is missing." (no batch, a failed run, scans that did not
reach the table, fewer passengers than usual; it builds to the third), and "A deleted batch must
leave no trace." (no rows, no figure, no copy, no record; the last works against the second and the
third).

## Originality

The obvious examples for an event-driven capstone are a ride-hire or taxi trips dataset, a web
shop's clickstream, and a cloud vendor's tutorial that makes a thumbnail when a picture lands in a
bucket. The ferry, its ticket gates' batches, its timetable, its three days and the three things
that go wrong in them are the course's own; no product, place or company is named.

## What the prose process caught

Briefs `part-8/briefs/common.md` and `P33a.md` to `P33c.md`, drafted by Haiku a part at a time
(`part-8/drafts/`). Facts added with the fewest words: the third message named at the head of "The
test batch"; "With your change to `inputs`" before the graph's counts, which hold only after it; the
first question called "the question about Tuesday's 17:30", since "the first question" read as the
first message; and "`sailing_loads` shows 35 passengers for it", where "It shows" had no clear
subject. The figure's three labels are Haiku's, copied into `figures.FERRY_FLOWS`.
