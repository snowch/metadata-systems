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
- **Objective:** the reader finds that the key decides which repeats are dropped, and that taking the
  last event to arrive as the newest breaks a run whose START arrived late.
- **Known before:** Chapter 19's keys; Chapter 20's orders.
- **Driving question:** what must the collector compare to keep each event once and each run's state
  right?
- **The action:** change `key`, press **Run below**; change `newer`, press **Run below**.
- **Why the action:** each change moves its own tests.
- **Evidence:** 2 of 5, 4 of 5, 5 of 5.
- **Consequence:** the reader sees each fault met by one piece.
- **Predictable:** yes, from Part V.
- **Gives nothing away:** the page names what each piece must compare, from Chapters 19 and 20.
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
- **Gives nothing away:** the cell asks whether, not why.
- **Not knowing:** fair.
- **Next question:** what does "invalid" ask the collector to refuse?

## Requirements

"The collector must reject invalid events." Readings: breaks the OpenLineage specification (Chapter
8's check; refused); from a producer or job the shop does not know (needs a list the collector does
not keep; the developer's event with a time passes the check: tested); out of order (Friday's START
breaks no rule; refusing it refuses a valid event). The figure that questions it is the free-text
cell after the box.

## Originality

The obvious example is a message broker's tutorial on idempotent consumers, with a deduplication
table keyed by message id. This chapter's collector, its five faults, its restart between two
arrivals of one event, and its three pieces are the shop's own, built on Part V's week.
