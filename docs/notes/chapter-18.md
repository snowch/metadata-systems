# Chapter 18: Missing events

A working note. Written on 12 October 2026 with Chapters 19 to 23, as a notebook
(`notebook/chapter_18.py`). It opens Part V.

## What the chapter does

Every chapter so far gave the collector every event the programs sent. The reader:

- sends the week's events down the path to the collector and reads what arrived: 68 sent, 68
  received; and meets **delivery**, the path an event takes and whether it arrives;
- predicts what the job graph shows for `build_daily_sales` when the COMPLETE of its run early on
  Thursday 10 is lost, then builds it: the same two edges, `writes` now with 6 runs, not 7;
- finds that run open: started at 02:30 on Thursday, 369000 seconds before Monday 09:00, where the
  job's runs that ended took 21 seconds; and that nothing the collector holds tells a lost
  COMPLETE from a run that is still going;
- loses the COMPLETE of `remove_return`'s only run, and finds the job with no edge at all: the
  graph cannot show that `remove_return` writes `returns`, and the open run has no usual time;
- sends again until acknowledged and meets **at least once**: the lost COMPLETE arrives 30 seconds
  later, and a lost acknowledgement makes one event arrive twice, which Chapter 19 takes up;
- questions "Lineage must be complete."

## What was built for it

`notebook/shop/delivery.py`: `send`, `open_runs`; `ingest.objects` and `edges` as Chapter 9 built
them.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** where the programs and the collector sit.
- **Why now:** every chapter opens with the map.

### `sent-and-received`

- **Role:** inspect
- **Serves:** what arrived when nothing is lost: the baseline the experiments change.
- **Why now:** the reader needs the count before one event goes missing.

### `lost-complete`

- **Role:** experiment
- **Objective:** the reader discovers that a job's graph, built from all its runs, hides a lost
  event, which shows only in the run it belonged to.
- **Known before:** Chapter 9's graph, job by job, with how many runs had each edge; Chapter 8's
  START and COMPLETE, and that outputs come in the COMPLETE.
- **Driving question:** what will the graph show for `build_daily_sales` when one COMPLETE never
  arrives?
- **The action:** write a prediction in a cell; run the cell that loses it and builds the graph.
- **Why the action:** the graph is built from the events received; only building it shows which
  edges survive.
- **Evidence:** both edges kept; `writes` with 6 runs; one run left START.
- **Consequence:** a reader who expected the edge to vanish learns that other runs carry it; one
  who expected nothing to change finds the run left open.
- **Predictable:** yes, from Chapter 9's runs per edge.
- **Gives nothing away:** the options are results: the same edges, an edge gone, no job.
- **Not knowing:** a fair first answer.
- **Next question:** is that run lost, or still running?

### `open-runs`

- **Role:** inspect
- **Serves:** the runs with a START and no end, and how long the job's ended runs took.
- **Why now:** it answers the question above as far as the events can: they cannot.

### `only-run`

- **Role:** experiment (completes `lost-complete`)
- **Objective:** the reader finds that a job that ran once leaves no edge when its one COMPLETE is
  lost: a dependency the graph cannot show.
- **Evidence:** `remove_return` with no edge; its open run with no usual time.

### `at-least-once`

- **Role:** experiment
- **Objective:** the reader sees what sending again until acknowledged buys (the event arrives)
  and costs (an event can arrive twice).
- **Known before:** the lost COMPLETE above.
- **Driving question:** if the program keeps the event until the collector acknowledges it, does
  the COMPLETE arrive, and how many times?
- **The action:** change `at_least_once` and `lose_ack`, press **Run below**.
- **Why the action:** the two settings answer the two halves.
- **Evidence:** sent twice, received once; with the acknowledgement lost, received twice.
- **Consequence:** the reader trades a loss for a repeat, which Chapter 19 takes up.
- **Predictable:** partly; the repeat is the surprise.
- **Gives nothing away:** the prompt asks how many times.
- **Not knowing:** fair.
- **Next question:** what does ingestion do with an event it has seen?

## Requirements

The chapter questions "Lineage must be complete.", the plan's candidate.

1. **What it says:** lineage must be complete.
2. **What it might mean:** every event each program sends arrives; every program that touches the
   data sends events; every run's edges are known.
3. **What each needs:** delivery that does not lose (or that sends again); every program
   instrumented (Chapter 8 found the export and the analyst's copy send nothing); an end for every
   run.
4. **What the shop records:** what arrived, and runs left open.
5. **Whether it is met:** with at least once, every event sent arrives; the export and the
   analyst's copy still send nothing, so not for every program; a run lost before it sends anything
   leaves nothing to find. The requirement does not say which it means.

## Originality

The obvious examples are a message queue's tutorial on at-least-once delivery with producer acks,
and a lineage tool's documentation of a job stuck in a running state. This chapter loses one named
event of the shop's own week, builds the shop's own graph from what arrived, and contrasts a job
with seven runs against one with a single run. The path's timings and the open-run listing are the
shop's own.
