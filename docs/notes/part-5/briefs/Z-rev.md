# Revision brief Z: Chapter 20, Out-of-order events

Letter Z. Read `rev-common.md` first. Redraft these slots: A, B, C, C2, E, F, H, Z.
Terms introduced in slot B, in bold there: **event time**, **arrival time**. Do not bold them again.
Do not name Chapter 13's clock.

## A

A list of four objectives:

- Tell the time an event happened from the time it arrived.
- Hold an event up, and find when taking the last event to arrive as the latest goes wrong.
- Find a run whose state, and a return whose existence, depend on the order events are read in.
- Question the requirement "Show the latest state of each run."

## B

- Keep the heading `## Two times`.
- Keep the definition of event time: every event has a time, `eventTime`; the OpenLineage
  specification describes it as "the time the event occurred at"; the program that sends the event
  sets it; this is the event's **event time**.
- The collector receives each event at a time of its own: the event's **arrival time**.
- Since Chapter 9, ingestion has taken each run's state from its events in the order of their event
  times. In the same order, it keeps for each dataset the run that last wrote it: the dataset's
  last write. Reading them in the order they arrived is the other way. (Chapter 8's consumer did
  that.)
- Here the `COMPLETE` of the run of `build_daily_sales` early on Wednesday 9 is held up for 26
  hours on its way to the collector. Every other event takes 2 seconds.
- Before you read on, write in the next cell when `daily_sales` was last written, as the
  collector's events show it at 09:00 on Thursday 10, by event time and by arrival. "Last written"
  is when the run that last wrote it ended.

## C

- Keep: "By event time, the run that last wrote `daily_sales` ended at 02:30:21 on Thursday 10."
- Change `order="event"` to `order="arrival"` in the cell, select it and press **Run below**.
- Keep: "By arrival, it ended at 02:30:21 on Wednesday 9: a day earlier."
- The next cell lists when each `COMPLETE` of `build_daily_sales` arrived.

## C2

- Wednesday 9's `COMPLETE` arrived at 04:30:24 on Thursday 10, after Thursday 10's, which arrived
  at 02:30:24.
- Taken in the order they arrived, Wednesday's `COMPLETE` came last, so Wednesday's run became the
  last write.
- Chapter 13's freshness, taken from the collector's last write by arrival, would find
  `daily_sales` a day behind on Thursday morning.
- Compare these with what you wrote.
- In the first cell, keep `order="arrival"` and change `26` to `20`. Select it and press
  **Run below**.
- Wednesday 9's `COMPLETE` now arrives at 22:30:24 on Wednesday 9, before Thursday 10's. By arrival,
  the last write is Thursday's run again, ended at 02:30:21 on Thursday 10.
- A held-up event changes the last write only when it arrives after the next `COMPLETE` of the same
  job.

## E

- The run early on Wednesday 9 shows the state `START` and an end of 02:30:21: a run with an end
  time, whose state is `START`.
- Read by arrival, its `START` came last, so its state is `START`.
- Chapter 9 listed the runs whose latest event is a `START`. That list would now hold this run,
  which has ended.
- By event time, its state is `COMPLETE`.
- Then keep the first draft's E from the heading `## A delete before its create` to the end,
  unchanged.

## F

- Keep: "By arrival, `r-206.json`'s last change is `created`, and it exists."
- Keep: "Change `"arrival"` to `"event"` in the cell, select it and press **Run below**. By event
  time, its last change is `deleted`, at 08:50:02 on Monday 14, and it does not exist."
- Each program sets its events' times by its own clock. A program whose clock runs slow sets event
  times that are early, and its events then sort in the wrong order beside other programs' events.
- Two programs' clocks can disagree in the same way.

## H

- "Latest" could mean at least two things, and each needs something different. Then a list:
- Latest by when it happened: it needs `eventTime` on every event, set by each program's clock, and
  clocks that agree. The shop's ingestion reads events in this order unless told otherwise.
- Latest by when it arrived: it needs only the order in which the collector received the events,
  which the shop keeps. It answers which event the collector received last.
- Both can be computed from what the shop records.
- By event time, the run early on Wednesday 9 is `COMPLETE`, `daily_sales` was last written on
  Thursday 10, and `r-206.json` is deleted. By arrival, the run is `START`, the last write is
  Wednesday's, and `r-206.json` exists.
- The requirement does not say which it means.

## Z

- Keep the heading `## Before Chapter 21`.
- Summary facts, in order: a program sets an event's event time, and the collector sets its arrival
  time; taking the last event to arrive as the latest made `daily_sales` a day behind on Thursday
  morning, gave an ended run the state `START`, and left a withdrawn return existing; a delay changed
  the last write only when the late event arrived after the next one; by event time, each showed the
  order in which things happened, as long as the programs' clocks agree.
- Keep: "Chapter 21 asks what happens when two sources disagree about the same fact."
- Keep the first draft's three questions as a list.
- Keep the heading `### How this differs from a real platform` and these bullets:
  - The shop's faults are invented for the course.
  - Keep the first draft's second bullet (the shop keeps every event and can read them again in any
    order; a real collector that updates its state as each event arrives must decide what to do
    with a late one when it comes).
  - The OpenLineage specification does not say what a consumer does with an event that arrives
    late or out of order (Chapter 8). Its run-cycle page says that after a terminal event, no other
    events about that run will be sent.
