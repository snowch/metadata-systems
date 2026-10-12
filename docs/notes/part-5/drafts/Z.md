## A

- Tell the time an event happened from the time it arrived.
- Hold an event up, and find what taking the last one to arrive as the latest shows.
- Find a run and a return whose state depends on the order events are read in.
- Question the requirement "Show the latest state of each run."

## B

## Two times

Every event has a time, `eventTime`. The OpenLineage specification describes it as "the time the event occurred at". The program that sends the event sets it. This is the event's **event time**.

The collector receives each event at a time of its own. This is the event's **arrival time**.

Ingestion so far took a run's state and each dataset's last write from the events in the order of their event times (Chapter 9). Taking them in the order they arrived is the other way.

Here the `COMPLETE` of the run of `build_daily_sales` early on Wednesday 9 is held up for 26 hours on its way. It arrives at 04:30:24 on Thursday 10, after the `COMPLETE` of the run early on Thursday 10, which arrived at 02:30:24.

Before you read on, write in the next cell when `daily_sales` was last written, as the collector's events show it at 09:00 on Thursday 10: by event time, and by arrival.

## BB

When was `daily_sales` last written, by event time?
........
By arrival?
........

## C

By event time, the run that last wrote `daily_sales` ended at 02:30:21 on Thursday 10.

Change `order="event"` to `order="arrival"` in the cell, select it and press **Run below**.

By arrival, it ended at 02:30:21 on Wednesday 9: a day earlier. The late `COMPLETE` arrived last, so it was taken as the latest, and older state replaced newer.

Chapter 13's freshness, read from this, would find `daily_sales` a day behind on Thursday morning.

Compare these with what you wrote.

## D

## A START after its COMPLETE

Here the `START` of the run early on Wednesday 9 is held up by 60 seconds. It arrives at 02:31:03, after its own `COMPLETE`, which arrived at 02:30:24.

The next cell lists the runs of `build_daily_sales` in the order their events arrived.

## E

The run early on Wednesday 9 shows the state `START`, with an end of 02:30:21. Read by arrival, the `START` came last, so the run seems to have started again after it ended.

By event time, its state is `COMPLETE`.

## A delete before its create

The returns desk recorded a return, `r-206`, on Sunday 13 at 21:15, and withdrew it on Monday 14 at 08:50 (Chapter 16).

Here the events of the `record_return` run on Sunday evening are held up for 12 hours. They arrive at 09:15 on Monday 14, after the events of the `remove_return` run at 08:50.

The next cell lists each return's object as the functions' events leave it, read in the order they arrived.

## F

By arrival, `r-206.json`'s last change is `created`, and it exists.

Change `"arrival"` to `"event"` in the cell, select it and press **Run below**. By event time, its last change is `deleted`, at 08:50:02 on Monday 14, and it does not exist.

Event time depends on the clock of the program that sets it. A program whose clock runs slow, as the reporting tool's did in Chapter 13, sets event times that are early. Its events then sort in the wrong order beside other programs' events.

## RH

## The latest state

## G

Before you read on, write in the next cell what "latest" means to you here.

## GG

What does "latest" mean here?
........

## H

"Latest" could mean two things, and each needs something different.

- latest by when it happened: each event's event time, and clocks that agree;
- latest by when it arrived: each event's arrival time, which the collector sets itself.

By when it happened, the shop's ingestion meets that meaning. By when it arrived, the run early on Wednesday 9 shows `START`, and `daily_sales` is a day old.

The requirement does not say which it means.

## Z

## Before Chapter 21

An event's event time is set by the program that sends it. Its arrival time is set by the collector. Taking the last event to arrive as the latest made `daily_sales` a day old on Thursday morning. It put a run back to `START` after it ended, and it left a withdrawn return existing. By event time, each of these is right, as long as the programs' clocks agree.

Chapter 21 asks what happens when two sources disagree about the same fact.

- Which of your platform's views show the last event to arrive?
- Whose clock sets your events' times?
- What would you show for a run whose `START` arrives after its end?

### How this differs from a real platform

- The shop's faults are invented for the course.
- The shop's ingestion keeps every event and can read them again in any order. A real collector that updates its state as each event arrives must decide what to do with a late one when it comes.
- The OpenLineage specification says nothing about events that arrive late or out of order (Chapter 8).
