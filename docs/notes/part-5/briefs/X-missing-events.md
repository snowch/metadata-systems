# Brief X: Chapter 18, "Missing events"

Read `docs/notes/part-5/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms this chapter introduces, in bold, and nowhere before the slot named: **delivery** (slot B),
**at least once** (slot H). Do not write: idempotent, deduplication, event time, arrival time,
precedence, alias, entity resolution, index, partition, retention, compaction.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Send the week's events to the collector, lose one, and build the graph from what arrived.
- Find the runs that started and never ended, and what the events cannot say about them.
- Send an event again until the collector acknowledges it, and see what that costs.
- Question the requirement "Lineage must be complete."

### Slot B: under the heading `## From the programs to the collector`

- In every chapter so far, the collector received every event the shop's programs sent, each once
  and in order.
- Each program sends each event to the collector over the network. In the shop, a program sends an
  event 1 second after the event's time, and the collector receives it 2 seconds later.
- The path an event takes from a program to the collector, and whether the event arrives, is its
  **delivery**.
- The next cell sends the week's events, with the returns desk, and counts what the collector
  received.

### Slot C: after that cell, under the heading `## One COMPLETE lost`

- 68 events sent, 68 received, none lost.
- Now one event is lost: the COMPLETE of the run of `build_daily_sales` early on Thursday 10. Its
  START arrives.
- The graph of Chapter 9 lists, job by job, each edge with how many runs had it. With every event,
  `build_daily_sales` has two edges: it reads `clean_orders` in 7 runs and writes `daily_sales` in 7
  runs. A run's outputs come in its COMPLETE (Chapter 8).
- Before you read on, write in the next cell what the graph will show for `build_daily_sales` when
  that COMPLETE never arrives: which edges, and how many runs each.

### Slot CC: the text inside that cell (between triple quotes)

One question, then `........` on its own line: what will the graph show for build_daily_sales? At
most about 60 characters a line. Plain text.

### Slot D: after the cell that builds the graph from what arrived

- Both edges are still there. `writes` now has 6 runs, not 7; `reads` still has 7.
- The other 6 runs that wrote `daily_sales` carry the edge. The lost event shows only in its own run.
- Compare this with what you wrote.
- The next cell lists the runs the collector has a START for and no COMPLETE, ABORT or FAIL, at
  09:00 on Monday 14: how many seconds since each started, and how long the job's runs that did end
  usually took.

### Slot E: after that cell

- One run: `build_daily_sales`, started at 02:30:00 on Thursday 10, 369000 seconds before Monday
  09:00, more than four days. Its job's runs that ended took 21 seconds.
- The collector's events cannot tell a COMPLETE that was lost from a run that is still running: both
  leave a START and nothing after it.
- Other evidence can. The run early on Thursday 10 writes Wednesday 9's row of `daily_sales`. The
  next cell reads that row from the warehouse.

### Slot F: after that cell, under the heading `## A job that ran once`

- The row is there: 15375 pence for Wednesday 9. The run did its work; only its COMPLETE is missing.
- `remove_return` ran once in the week: on Saturday 12 at 16:50:02, when the returns desk deleted
  `r-203`. Its START names no dataset. Its COMPLETE names what it wrote, `returns`.
- The next cell loses that COMPLETE and builds the graph from what arrived.

### Slot G: after that cell

- `remove_return` has no edge. With every event, it has one: it writes `returns`.
- With its one COMPLETE lost, nothing the collector holds shows that `remove_return` writes
  `returns`. The dependency is real and cannot be shown.
- The next cell lists the open runs again.

### Slot H: after that cell, under the heading `## Sending again`

- The open run of `remove_return` started at 16:50:02 on Saturday 12. Its usual time is empty: the job
  has no other run to compare with.
- So far, each program sends each event once and keeps nothing. A lost event is gone.
- Another way: the collector acknowledges each event it receives. The program keeps each event until
  it is acknowledged, and sends it again if no acknowledgement comes within 30 seconds. Every event
  sent then arrives once or more: delivery **at least once**.
- The next cell loses the same COMPLETE once, sends with `at_least_once=True`, and lists the events
  sent or received more than once.

### Slot I: after that cell

- The COMPLETE was sent twice and received once, at 16:50:37 on Saturday 12, 30 seconds after the first
  sending.
- Now change `lose=` to `lose_ack=` in the cell, select it and press **Run below**. The COMPLETE then
  arrives, and its acknowledgement is lost.
- With `lose_ack`, the COMPLETE is sent twice and received twice: at 16:50:07 and at 16:50:37.
- At least once trades a lost event for an event that can arrive twice. Chapter 19 takes up the
  second.

### Slot RH: the heading of the requirement's section

Exactly `## Complete lineage`. A box holding the requirement comes after this heading.

### Slot J: after the box that holds the requirement

The box quotes the requirement, so do not quote it again.

- Before you read on, write in the next cell what "complete" means to you here.

### Slot JJ: the text inside that cell

One question, then `........` on its own line: what does "complete" mean here? Plain text.

### Slot K: after that cell

- "Complete" could mean three things, each needing something different. Write them as a Markdown
  list, each with what it needs:
  - every event a program sends arrives: delivery at least once, or no loss;
  - every program that touches the data sends events: each program instrumented;
  - every run's end and edges are known: a COMPLETE, ABORT or FAIL for each run.
- Then, as a second list, what the shop's records meet:
  - every event sent arrives: met with at least once, not without; one lost COMPLETE left a run open
    and, for `remove_return`, no edge;
  - every program: not met; the export and the analyst's copy send no events (Chapter 8);
  - every run's end: met with at least once, as long as each program sends its events at all.
- The requirement does not say which it means.

### Slot Z: the closing (a heading `## Before Chapter 19`, a summary, a lead, three questions)

- Summary: a lost COMPLETE left the job graph with every edge, because other runs carried them, and
  left one run open; the events could not tell a lost COMPLETE from a run still going, and the
  warehouse's row could. For a job that ran once, the lost COMPLETE left no edge at all. Sending again
  until acknowledged delivered the event, and a lost acknowledgement delivered it twice.
- Chapter 19 asks what ingestion does with an event it receives twice.
- Three questions, as a list: Which of your platform's programs send no events at all? What does
  your collector do with an event it has already received? How would you tell a slow run from a
  lost event?

Then a heading `### How this differs from a real platform` and a list:

- The shop's faults are invented for the course.
- The shop's path loses only the events the cell names. A real network loses, delays and repeats
  events at random, and a collector can be down.
- The shop's collector is never down, and acknowledges every event it receives at once.
- The OpenLineage specification says nothing about how an event travels, or what a consumer does
  with an event that never arrives (Chapter 8).
