[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 19](chapter_19.ipynb) · [Next: Chapter 21](chapter_21.ipynb)

# Chapter 20: Out-of-order events

**Objectives**

- Tell the time an event happened from the time it arrived.
- Hold an event up, and find when taking the last event to arrive as the latest goes wrong.
- Find a run whose state, and a return whose existence, depend on the order events are read in.
- Question the requirement "Show the latest state of each run."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## Two times

Every event has a time, `eventTime`. The OpenLineage specification describes it as "the time the event occurred at". The program that sends the event sets it. This is the event's **event time**.

The collector receives each event at a time of its own. This is the event's **arrival time**.

Since Chapter 9, ingestion has taken each run's state from its events in the order of their event times. In the same order, it keeps, for each dataset, the run that last wrote it: the dataset's last write. Reading them in the order they arrived is the other way. (Chapter 8's consumer did that.)

Here the `COMPLETE` of the run of `build_daily_sales` early on Wednesday 9 is held up for 26 hours on its way to the collector. Every other event takes 2 seconds.

Before you read on, write in the next cell when `daily_sales` was last written, as the collector's events show it at 09:00 on Thursday 10: by event time, and by arrival. "Last written" is when the run that last wrote it ended.

    [WRITE] When was daily_sales last written, by event time?
    [WRITE] ........
    [WRITE] By arrival?
    [WRITE] ........

    >>> week20 = shop.run_week(["returns"])
    >>> late = shop.delivery.send(week20, delay={"build_daily_sales COMPLETE 2026-09-09": 26 * 3600})
    >>> seen = shop.ingest.normalise(late.until("2026-09-10T09:00:00Z"))
    >>> shop.ingest.objects(seen, order="event").last_write("daily_sales")
      | dataset | job | run ended
      | warehouse://shop-warehouse/shop.analytics.daily_sales | shop/build_daily_sales | 2026-09-10T02:30:21Z

By event time, the run that last wrote `daily_sales` ended at 02:30:21 on Thursday 10.

Change `order="event"` to `order="arrival"` in the cell, select it and press **Run below**.

By arrival, it ended at 02:30:21 on Wednesday 9: a day earlier.

The next cell lists when each `COMPLETE` of `build_daily_sales` arrived.

    >>> late.received(job="build_daily_sales", type="COMPLETE")
      | arrived | job | type | event time
      | 2026-09-08T02:30:24Z | build_daily_sales | COMPLETE | 2026-09-08T02:30:21Z
      | 2026-09-10T02:30:24Z | build_daily_sales | COMPLETE | 2026-09-10T02:30:21Z
      | 2026-09-10T04:30:24Z | build_daily_sales | COMPLETE | 2026-09-09T02:30:21Z
      | 2026-09-11T02:30:24Z | build_daily_sales | COMPLETE | 2026-09-11T02:30:21Z
      | 2026-09-12T02:30:24Z | build_daily_sales | COMPLETE | 2026-09-12T02:30:21Z
      | 2026-09-13T02:30:24Z | build_daily_sales | COMPLETE | 2026-09-13T02:30:21Z
      | 2026-09-14T02:30:24Z | build_daily_sales | COMPLETE | 2026-09-14T02:30:21Z

Wednesday 9's `COMPLETE` arrived at 04:30:24 on Thursday 10, after Thursday 10's, which arrived at 02:30:24.

Taken in the order they arrived, Wednesday's `COMPLETE` came last, so Wednesday's run became the last write.

Chapter 13's freshness, taken from the collector's last write by arrival, would find `daily_sales` a day behind on Thursday morning.

Compare these with what you wrote.

In the cell that starts `week20 =`, keep `order="arrival"` and change `26` to `20`. Select it and press **Run below**.

Wednesday 9's `COMPLETE` now arrives at 22:30:24 on Wednesday 9, before Thursday 10's. By arrival, the last write is Thursday's run again, ended at 02:30:21 on Thursday 10.

A held-up event changes the last write only when it arrives after the next `COMPLETE` of the same job.

## A START after its COMPLETE

Here the `START` of the run early on Wednesday 9 is held up by 60 seconds. It arrives at 02:31:03, after its own `COMPLETE`, which arrived at 02:30:24.

The next cell lists the runs of `build_daily_sales` in the order their events arrived.

    >>> early = shop.delivery.send(week20, delay={"build_daily_sales START 2026-09-09": 60})
    >>> shop.ingest.objects(shop.ingest.normalise(early.events), order="arrival").runs_of(job="shop/build_daily_sales", columns=["started", "ended", "state"])
      | state | started | ended
      | COMPLETE | 2026-09-08T02:30:00Z | 2026-09-08T02:30:21Z
      | START | 2026-09-09T02:30:00Z | 2026-09-09T02:30:21Z
      | COMPLETE | 2026-09-10T02:30:00Z | 2026-09-10T02:30:21Z
      | COMPLETE | 2026-09-11T02:30:00Z | 2026-09-11T02:30:21Z
      | COMPLETE | 2026-09-12T02:30:00Z | 2026-09-12T02:30:21Z
      | COMPLETE | 2026-09-13T02:30:00Z | 2026-09-13T02:30:21Z
      | COMPLETE | 2026-09-14T02:30:00Z | 2026-09-14T02:30:21Z

The run early on Wednesday 9 has an end time of 02:30:21, and its state is `START`.

Read by arrival, its `START` came last, so its state is `START`.

Chapter 9 listed the runs whose latest event is a `START`. That list would now hold this run, which has ended.

By event time, its state is `COMPLETE`.

## A delete before its create

The returns desk recorded a return, `r-206`, on Sunday 13 at 21:15, and withdrew it on Monday 14 at 08:50 (Chapter 16).

Here the events of the `record_return` run on Sunday evening are held up for 12 hours. They arrive at 09:15 on Monday 14, after the events of the `remove_return` run at 08:50.

The next cell lists each return's object as the functions' events leave it, read in the order they arrived.

    >>> week20w = shop.run_week(["returns", "withdrawn"])
    >>> held = shop.delivery.send(week20w, delay={"record_return START 2026-09-13": 12 * 3600, "record_return COMPLETE 2026-09-13": 12 * 3600})
    >>> shop.delivery.object_states(held.events, "arrival")
      | object | last change | at | exists
      | s3://shop-returns/r-201.json | created | 2026-09-08T14:20:02Z | yes
      | s3://shop-returns/r-202.json | overwritten | 2026-09-10T09:30:02Z | yes
      | s3://shop-returns/r-203.json | deleted | 2026-09-12T16:50:02Z | no
      | s3://shop-returns/r-204.json | created | 2026-09-11T13:15:02Z | yes
      | s3://shop-returns/r-206.json | created | 2026-09-13T21:15:02Z | yes

By arrival, `r-206.json`'s last change is `created`, and it exists.

Change `"arrival"` to `"event"` in the cell, select it and press **Run below**. By event time, its last change is `deleted`, at 08:50:02 on Monday 14, and it does not exist.

Each program sets its events' times by its own clock. A program whose clock runs slow sets event times that are early, and its events then sort in the wrong order beside other programs' events.

## The latest state

[BOX] The head of the shop's requirement: "Show the latest state of each run."

Before you read on, write in the next cell what "latest" means to you here.

    [WRITE] What does "latest" mean here?
    [WRITE] ........

"Latest" could mean at least two things, and each needs something different.

- Latest by when it happened: it needs `eventTime` on every event, set by each program's clock, and clocks that agree. The shop's ingestion reads events in this order unless told otherwise.
- Latest by when it arrived: it needs only the order in which the collector received the events, which the shop keeps. It answers which event the collector received last.

Both can be computed from what the shop records.

By event time, the run early on Wednesday 9 is `COMPLETE`, `daily_sales` was last written on Thursday 10, and `r-206.json` is deleted. By arrival, the run is `START`, the last write is Wednesday's, and `r-206.json` exists.

The requirement does not say which it means.

## Before Chapter 21

A program sets an event's event time, and the collector sets its arrival time. Taking the last event to arrive as the latest made `daily_sales` a day behind on Thursday morning. The same rule also gave an ended run the state `START`, and left a withdrawn return existing. A delay changed the last write only when the late event arrived after the next one. By event time, each of these showed the order in which things happened, as long as the programs' clocks agree.

Chapter 21 asks what happens when two sources disagree about the same fact.

- Which of your platform's views show the last event to arrive?
- Whose clock sets your events' times?
- What would you show for a run whose `START` arrives after its end?

### How this differs from a real platform

- The shop's faults are invented for the course.
- The shop's ingestion keeps every event and can read them again in any order. A real collector that updates its state as each event arrives must decide what to do with a late one when it comes.
- The OpenLineage specification does not say what a consumer does with an event that arrives late or out of order (Chapter 8). Its run-cycle page says that after a terminal event, no other events about that run will be sent.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 19](chapter_19.ipynb) · [Next: Chapter 21](chapter_21.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

