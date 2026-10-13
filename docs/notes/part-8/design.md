# Part VIII: design

A working note, 13 October 2026, written before the engine for Chapter 33, after the author passed
plan checkpoint 5 ("Pls go"). It says what the chapter's second platform is, what the learner does
with it, which requirements it questions, and where each fact comes from.

## The plan's chapter

"Build the whole thing": receive a second, unfamiliar platform, built not on a nightly batch but on
object storage whose changes start functions, with scheduled jobs beside them and tables over the
results; model it, instrument its functions and jobs, capture and ingest its lineage (per object and
per version, deletions included), track its schemas and quality, diagnose a failure, analyse an
impact and explain a result's provenance. The plan's requirement row: "the unfamiliar platform's own
requirements: the learner questions each before building to it".

## The second platform: the ferry

An island ferry, invented for the course: one vessel's crossings between "the mainland" and "the
island", no place or company named. Its data team is new, and so is the learner on it.

- **Sailings.** Three days, Tuesday 22 to Thursday 24 September 2026; three departures a day from
  each side: the mainland at 07:30, 12:30 and 17:30, the island at 09:30, 14:30 and 19:30. The
  timetable is a warehouse table, `sailings`, typed in by hand before the week: no job writes it and
  nothing sends an event about it.
- **Object storage.** At each harbour, two ticket gates. A minute after each departure, each gate
  uploads the sailing's scans as one object, `s3://ferry-gates/{harbour}/{date}/{HHMM}/gate-{n}.jsonl`,
  one scan per line: `ticket`, `fare`, `scanned_at`. Storage keeps every version and a delete
  marker (the shop's `ObjectStorage`).
- **Functions.** The platform starts a function two seconds after each object change in
  `ferry-gates`: `load_scans` for a create or an overwrite (it replaces the batch's rows in
  `boardings`, keeping only scans that have a `scanned_at`, since the gates' firmware wrote an
  aborted scan with no time), `drop_scans` for a delete (it removes the batch's rows; it reads
  nothing). The function platform records its triggers and a log of its invocations: when, which
  function, which object and version, and whether it finished.
- **Scheduled jobs.** `build_loads` at 01:00 each night rebuilds the day before's rows of
  `sailing_loads` (passengers per sailing, and the share of the vessel's capacity) from
  `boardings` and `sailings`; `send_report` at 06:00 writes the day before's loads as a CSV to
  `s3://ferry-reports/` and the harbour masters get it by email. The scheduler records each job's
  schedule and each run's start, end and status.
- **Investigation time:** Friday 25 September at 09:00.

## What goes wrong in the three days

Each is a fixed part of the week, deterministic, and each gives one of the operations manager's
three messages on Friday morning:

1. **An overwrite after the build.** Tuesday's 17:30 from the mainland: gate 2 loses its connection
   and uploads 3 scans short; it uploads the whole batch again at 07:05 on Wednesday. `build_loads`
   ran at 01:00, so Tuesday's row of `sailing_loads` counts the short batch, and no later run
   rebuilds Tuesday. (Provenance: why does the load report say fewer than `boardings` now holds?)
2. **A test batch, deleted.** At 23:40 on Wednesday an engineer uploads a test batch of 5 scans
   under Wednesday's 19:30 from the island; `load_scans` adds them; `build_loads` counts them at 01:00
   on Thursday; `send_report` sends them at 06:00; the engineer deletes the object at 08:30, and
   `drop_scans` removes the rows. (Impact: what still counts them?)
3. **A silent loss.** From noon on Thursday the island's gate 2 runs new firmware, which writes
   `scan_time` where the old wrote `scanned_at`. `load_scans` keeps no scan from its two batches
   and finishes as usual. Friday's 01:00 build shows the island's afternoon sailings nearly empty;
   the island's harbour master's own count says otherwise. (Diagnosis: no run failed; what shows
   it?) One earlier batch, Wednesday's 12:30 from the mainland, gate 1, holds one aborted scan with
   no time, which `load_scans` rightly leaves out: a rule that flags any run writing fewer rows than
   it read also flags that one.

## The chapter's sections

Each section starts from one message, questions the ferry's requirement for it before building to
it (the plan's row), and ends with what the evidence proved and what it could not.

- **The ferry's platform.** The learner meets the platform through what its systems record: object
  storage's keys and versions, the function platform's triggers and invocation log, the
  warehouse's tables, the scheduler's runs. Instrument (question first): from these records, which
  batches was Tuesday's 17:30 row of `sailing_loads` built from? None of them says (Chapter 2's
  finding, on a platform built another way).
- **What to record.** Requirement: "Record the lineage of every boarding." Readings: per scan, per
  batch, per batch as it was when a run read it. The chapter's model: a dataset per object key, with
  each run's version of it on that run's input (OpenLineage's `version` dataset facet,
  `datasetVersion`), and the change that started a function in the run's own facet, as the shop's
  returns desk did (Chapters 7 and 8). The other choice, a dataset per version, is named with what it
  costs; neither is called right.
- **Instrumenting the functions.** The learner writes `inputs(change)`: the input datasets of a
  function's run event, from the object change that started it. It starts as the shop's
  `remove_return` did: the object without its version for a create or an overwrite, and nothing for
  a delete. The check: every create and overwrite names its version; the delete names the object and
  the version it removed; every event passes Chapter 8's check. OpenLineage's `lifecycleStateChange`
  dataset facet (`CREATE`, `OVERWRITE`, `DROP`, ...) is mentioned for what it is: a change a run makes
  to a dataset, which is not the change the gate made, so the ferry keeps its own facet. The jobs'
  events are the ferry's own and are given.
- **Capture and ingest.** The ferry's events go through the learner's Part VI pieces (the shop's
  reference collector and graph), and the graph answers the first section's question.
- **Thursday afternoon (diagnose; schemas and quality).** Effect first: `sailing_loads` against the
  island's harbour master's count. Prediction: did any function run fail on Thursday? (No: every run
  finished.) Requirement: "Alert us when a sailing's data is missing." Readings: no batch arrived;
  a batch arrived and its run failed; a run kept fewer scans than its batch held; a sailing with
  fewer passengers than usual. The learner writes `suspect(run)` over each `load_scans` run's
  measurements (scans read, rows written, the batch's fields); it starts as `run["state"] == "FAIL"`.
  The check: both of Thursday's island gate-2 runs, and not Wednesday's run that left out one aborted
  scan. Then the batches' fields by version show the rename.
- **Tuesday's 17:30 (provenance).** Prediction: does `sailing_loads` still differ from `boardings`
  for Tuesday's 17:30, now that `build_loads` has run twice since the corrected batch? A trace: the
  row, the run that wrote it, the batches as that run read them (version by version), and the batch's
  later version.
- **The test batch (impact).** Requirement: "A deleted batch must leave no trace." Readings: no rows
  made from it; no figure that counted it; no copy of such a figure; no record that it ever existed,
  which would leave the figures it changed unexplained. Prediction: after the delete, which of
  `boardings`, `sailing_loads` and the morning report still count the test scans? The graph's
  downstream of the batch, with whether each still holds them.

## The learner's code

Two pieces, each with a check: `inputs(change)` and `suspect(run)`. Everything else is the ferry's
or the shop's reference pieces from Part VI. No new terms (the plan has none for Part VIII).

## Accuracy

- OpenLineage's `version` (`DatasetVersionDatasetFacet`, `datasetVersion`) and
  `lifecycleStateChange` (`LifecycleStateChangeDatasetFacet`, the enum `ALTER`, `CREATE`, `DROP`,
  `OVERWRITE`, `RENAME`, `TRUNCATE`) facets, read at the OpenLineage commit `60261f0`; recorded in
  `docs/sources.md` under "Read for Part VIII".
- No real object store, function platform or scheduler is named or described. Every delivery rule,
  time and record of the ferry's platform is the course's own, and the model-versus-reality note
  says so.

## Originality

The obvious examples for an event-driven capstone are a ride-hire or taxi trips dataset, a web shop's
clickstream, and the cloud vendors' "thumbnail a picture when it lands in a bucket" tutorial. The
ferry's ticket-gate batches, its timetable and its three days are the course's own.
