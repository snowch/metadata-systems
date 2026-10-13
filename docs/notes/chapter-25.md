# Chapter 25: Build the event collector

A working note. Written on 13 October 2026 with Chapters 24 and 26 to 28
(`notebook/chapter_25.py`).

## What the chapter does

The collector Chapter 18 named receives the week with the returns desk and Part V's faults at once:
Thursday's retry with a new time, Wednesday's late COMPLETE, Friday's START after its COMPLETE, the
developer's event with no `eventTime`, and Saturday's exact repeat. The reader:

- reads the five faulted arrivals;
- writes `key(event)` (run id and event type) and `newer(event, current)` (event times compared),
  moving the check from 2 of 5 to 4 and then 5: each event kept once, Thursday's run ending at
  02:30:21, Friday's run `COMPLETE`;
- predicts whether, after a restart between Saturday's two arrivals, the repeat is dropped; finds it
  kept, because the collector's keys were in memory; writes `start(stored)` to rebuild them from the
  file; 6 of 6;
- questions "The collector must reject invalid events."

## What was built for it

`notebook/shop/collector.py`: the arrivals with the faults, `faults`, the `Collector` with its file
and memory, `run`, `check` (with a restart only when `start` is given); `delivery.send`'s `restamp`
for chosen events.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `faults`

- **Role:** inspect
- **Serves:** which arrivals will the collector have to handle? The five, with their faults.
- **Why now:** each test below is about one of them.

### `key-and-newer`

- **Role:** experiment
- **Objective:** the reader builds the two pieces Chapters 19 and 20 described, and sees each fault
  met by one of them: the key decides which repeats are dropped, and taking the last event to arrive
  as the newest breaks a run whose START arrived late.
- **Known before:** Chapter 19's keys; Chapter 20's orders.
- **Driving question:** what must the collector compare to keep each event once and each run's state
  right?
- **The action:** change `key`, press **Run below**; change `newer`, press **Run below**.
- **Why the action:** each change moves its own tests.
- **Evidence:** 2 of 5, 4 of 5, 5 of 5.
- **Consequence:** the reader sees each fault met by one piece.
- **Predictable:** yes, from Part V.
- **Gives nothing away:** the page names the fields and what each piece must compare, from Chapters
  19 and 20; the chapter's decision is at the restart, not here.
- **Not knowing:** fair.
- **Next question:** what does the collector lose when it restarts?

### `restart`

- **Role:** experiment
- **Objective:** the reader discovers that a collector's memory of what it has seen does not survive
  a restart unless it is rebuilt from what it stored.
- **Known before:** the key from above.
- **Driving question:** after the restart, is the repeat dropped?
- **The action:** write the prediction; read the check; change `start`; press **Run below**.
- **Why the action:** only the restarted run shows what memory held.
- **Evidence:** 4 of 6, the repeat kept a second time; 6 of 6 after.
- **Consequence:** a reader who trusted the right key learns that the key is not enough.
- **Predictable:** partly; the surprise is the point.
- **Gives nothing away:** before the prediction the page says only that the file survives, that the
  run states are rebuilt from it, and that the keys come from `start`; what `start` gives, and that
  the keys are lost, come after.
- **Not knowing:** fair.
- **Next question:** what does "invalid" ask the collector to refuse?

## Requirements

"The collector must reject invalid events." Readings: breaks the OpenLineage specification (Chapter
8's check; refused); from a producer or job the shop does not know (needs a list the collector does
not keep; the developer's event with a time passes the check: tested in `test_engine.py`); out of order (Friday's START
breaks no rule; refusing it refuses a valid event). The figure that questions it is the free-text
cell after the box.

## Originality

The obvious example is a message broker's tutorial on idempotent consumers, with a deduplication
table keyed by message id. This chapter's collector, its five faults, its restart between two
arrivals of one event, and its three pieces are the shop's own, built on Part V's week.

## What the prose process caught

First draft from brief P25 (`part-6/drafts/P25.md`); the review's changes through brief P25-rev
(`part-6/briefs/P25-rev.md`, draft `part-6/drafts/P25-rev.md`). The first drafts' slips across Part
VI were labels where a statement belonged ("The question:", "Result 1"), single quotes round a
requirement, two joins that left "the next cell" pointing at the wrong cell, *job* where the six
programs were meant, and a total whose scope was missing; each was fixed with the fewest words.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 19 findings (`review/verdicts.md`): 8 upheld, 9 partly, 2 rejected.
Read whole again after the fixes (`review/chapter_25-after-review.md`). Acted on:

- "Chapter 9's first stage" is its second (normalise);
- the graph test compares edges by job (run counts, first and last times), so it cannot see a run
  that ends at the wrong time; its line and the page say so;
- the restart prediction was answered above it; the loss now comes after;
- the reality note carries Chapter 19's `RUNNING` and `OTHER` caveat, Chapter 20's clocks, and the
  keys kept with no time limit;
- a run held as its `START` is said so, not "ends at START"; the page names the fields and says a
  key must be a value a set can hold;
- a run's state is defined, and why the collector keeps it; `newer` points to Chapter 20;
- the held-up Wednesday `COMPLETE` is explained (it needs no piece; Chapter 26 uses it);
- the developer's event is introduced with its row, and its check line names it; the claim that it
  would pass with a time is tested;
- the closing says what the check could not show, and no longer gives the key the collector's
  action.

Rejected, with the sceptic: catching the learner's exceptions in the check, predictions for `key`
and `newer` (Part VI's convention), and a shorter name for the Thursday run.

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
24 to 28"): from Chapter 24's link, 11 files, 0.32 MB, in a new tab; Run all 8.0 to 8.8 s; peak memory 389 to 402 MB alone, 612 MB with Chapter 24
open; no error output, no console error. The browser test (`notebook/jupyterlite/smoke.mjs`) types the
references into each cell and reads the checks' lines.

## Known gaps

- The shop's programs send one event of each type a run; a key of run id and event type is tested
  only against that.
