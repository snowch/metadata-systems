# Chapter 20: Out-of-order events

A working note. Written on 12 October 2026 with Chapters 18, 19 and 21 to 23
(`notebook/chapter_20.py`).

## What the chapter does

- meets **event time**, the time the producer says the event occurred (OpenLineage's `eventTime`),
  and **arrival time**, when the collector received it;
- holds up the COMPLETE of the run early on Wednesday 9 by 26 hours, predicts when `daily_sales`
  was last written as the collector sees it at 09:00 on Thursday 10, and reads it both ways: by
  event time, 02:30 on Thursday 10; by arrival, 02:30 on Wednesday 9, a day stale;
- holds up a START by a minute, past its own COMPLETE: by arrival the run is still started;
- runs the week with `withdrawn` and holds up Sunday evening's `record_return` events for `r-206`
  by 12 hours, past Monday morning's delete: by arrival the return exists; by event time it is gone;
- questions "Show the latest state of each run."

## What was built for it

`send(delay=...)`, `Delivery.until`, `ingest.objects(order=...)` with `written`,
`delivery.object_states`.

## Figures

### `late-complete`

- **Role:** experiment
- **Objective:** the reader discovers that taking the last event to arrive as the latest overwrites
  newer state with older.
- **Known before:** Chapter 13's freshness; Chapter 18's delivery.
- **Driving question:** at 09:00 on Thursday, when does the collector say `daily_sales` was last
  written?
- **The action:** commit; run the cell that reads the collector's events both ways.
- **Evidence:** 2026-09-10T02:30:21Z by event time; 2026-09-09T02:30:21Z by arrival.
- **Consequence:** an order rule is needed, and event time is the producer's clock.
- **Predictable:** yes, once the two times are named.
- **Gives nothing away:** the options are times.
- **Not knowing:** fair.
- **Next question:** what else does arrival order break?

### `start-after-complete` and `delete-before-create`

- **Role:** experiment (completes `late-complete`)
- **Evidence:** the run's state START by arrival, COMPLETE by event time; r-206 exists by arrival,
  not by event time.

## Requirements

"Show the latest state of each run." Latest by when it happened, or by when it arrived. The shop's
ingestion orders by event time (Chapter 9); the chapter shows what arrival order would show. Event
time depends on each producer's clock (Chapter 13's slow clock), which the requirement does not
address.

## Originality

The obvious example is a streaming textbook's event-time and processing-time diagram with
watermarks and late data. This chapter uses one late event of the shop's own week and reads one
table's last write both ways, with no window or watermark; a return deleted before it is created is
the shop's own case.
