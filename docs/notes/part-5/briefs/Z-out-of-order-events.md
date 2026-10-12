# Brief Z: Chapter 20, "Out-of-order events"

Read `docs/notes/part-5/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms this chapter introduces, in bold, and nowhere before the slot named: **event time** and
**arrival time** (both in slot B). Terms already introduced, which you may use: delivery, at least
once, deduplication, idempotent. Do not write: precedence, alias, entity resolution, index,
partition, retention, compaction.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Tell the time an event happened from the time it arrived.
- Hold an event up, and find what taking the last one to arrive as the latest shows.
- Find a run and a return whose state depends on the order events are read in.
- Question the requirement "Show the latest state of each run."

### Slot B: under the heading `## Two times`

- Every event has a time, `eventTime`. The OpenLineage specification describes it as "the time the
  event occurred at". The program that sends the event sets it. This is the event's **event time**.
- The collector receives each event at a time of its own: the event's **arrival time**.
- Ingestion so far took a run's state and each dataset's last write from the events in the order of
  their event times (Chapter 9). Taking them in the order they arrived is the other way.
- Here the COMPLETE of the run of `build_daily_sales` early on Wednesday 9 is held up for 26 hours on
  its way. It arrives at 04:30:24 on Thursday 10, after the COMPLETE of the run early on Thursday 10,
  which arrived at 02:30:24.
- Before you read on, write in the next cell when `daily_sales` was last written, as the collector's
  events show it at 09:00 on Thursday 10: by event time, and by arrival.

### Slot BB: the text inside that cell

Two short questions, each followed by `........` on its own line: when was daily_sales last written,
by event time? By arrival? Plain text.

### Slot C: after the cell (it lists the run that last wrote each dataset, by event time)

- By event time, the run that last wrote `daily_sales` ended at 02:30:21 on Thursday 10.
- Change `order="event"` to `order="arrival"` in the cell, select it and press **Run below**.
- By arrival, it ended at 02:30:21 on Wednesday 9: a day earlier. The late COMPLETE arrived last, so
  it was taken as the latest, and older state replaced newer.
- Chapter 13's freshness, read from this, would find `daily_sales` a day behind on Thursday morning.
- Compare these with what you wrote.

### Slot D: under the heading `## A START after its COMPLETE`

- Here the START of the run early on Wednesday 9 is held up by 60 seconds. It arrives at 02:31:03,
  after its own COMPLETE, which arrived at 02:30:24.
- The next cell reads the runs of `build_daily_sales` in the order their events arrived.

### Slot E: after that cell

- The run early on Wednesday 9 shows the state START, with an end of 02:30:21. Read by arrival, the
  START came last, so the run seems to have started again after it ended.
- By event time, its state is COMPLETE.
- Under the heading `## A delete before its create`: the returns desk recorded a return, `r-206`, on
  Sunday 13 at 21:15 and withdrew it on Monday 14 at 08:50 (Chapter 16). Here the events of the
  `record_return` run on Sunday evening are held up for 12 hours and arrive at 09:15 on Monday 14,
  after the events of the `remove_return` run at 08:50. The next cell lists each return's object as
  the functions' events leave it, read in the order they arrived.

Write the heading `## A delete before its create` where the third fact starts.

### Slot F: after that cell

- By arrival, `r-206.json`'s last change is `created`, and it exists.
- Change `"arrival"` to `"event"` in the cell, select it and press **Run below**. By event time, its
  last change is `deleted`, at 08:50:02 on Monday 14, and it does not exist.
- Event time depends on the clock of the program that sets it. A program whose clock runs slow, as
  the reporting tool's did in Chapter 13, sets event times that are early, and its events then sort
  in the wrong order beside other programs' events.

### Slot RH: the heading of the requirement's section

Exactly `## The latest state`. A box holding the requirement comes after this heading.

### Slot G: after the box (do not quote the requirement again)

- Before you read on, write in the next cell what "latest" means to you here.

### Slot GG: the text inside that cell

One question, then `........` on its own line: what does "latest" mean here? Plain text.

### Slot H: after that cell

- "Latest" could mean two things, each needing something different. Write them as a Markdown list:
  - latest by when it happened: each event's event time, and clocks that agree;
  - latest by when it arrived: each event's arrival time, which the collector sets itself.
- By when it happened, the shop's ingestion meets it. By when it arrived, the run early on Wednesday 9
  shows START and `daily_sales` a day old.
- The requirement does not say which it means.

### Slot Z: the closing (a heading `## Before Chapter 21`, a summary, a lead, three questions)

- Summary: an event's event time is set by the program that sends it; its arrival time by the
  collector. Taking the last event to arrive as the latest made `daily_sales` a day old on Thursday
  morning, put a run back to START after it ended, and left a withdrawn return existing. By event
  time, each was right, as long as the programs' clocks agree.
- Chapter 21 asks what happens when two sources disagree about the same fact.
- Three questions, as a list: Which of your platform's views show the last event to arrive? Whose
  clock sets your events' times? What would you show for a run whose START arrives after its end?

Then a heading `### How this differs from a real platform` and a list:

- The shop's faults are invented for the course.
- The shop's ingestion keeps every event and can read them again in any order. A real collector that
  updates its state as each event arrives must decide what to do with a late one when it comes.
- The OpenLineage specification says nothing about events that arrive late or out of order (Chapter
  8).
