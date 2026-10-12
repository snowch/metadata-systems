# Revision brief X: Chapter 18, Missing events

Letter X. Read `rev-common.md` first. Redraft these slots: C, D, E, F, G, H, I, IP, IR, K, Z.
Terms already introduced in this chapter: **collector** (slot B), **delivery** (B), **at least
once** (H). Do not bold them again. Do not use the word "instrumented".

## C

- Keep the first two paragraphs of the first draft's C as they are (68 sent, 68 received, none
  lost; the lost `COMPLETE` of the run of `build_daily_sales` early on Thursday 10; its `START`
  arrives).
- Keep: "The graph from Chapter 9 lists each job's edges, with how many runs had each one."
- With every event, `build_daily_sales` has two edges: `reads` to `clean_orders` in 7 runs, and
  `writes` to `daily_sales` in 7 runs. A run reports its outputs in its `COMPLETE` (Chapter 8).
- In Chapter 9, a `COMPLETE` line was cut short inside the shop's own store of events. Here the
  `COMPLETE` is lost on its way to the collector, before anything stores it.
- Before you read on, write in the next cell what the graph will show for `build_daily_sales`
  when that `COMPLETE` never arrives: which edges, and how many runs each.

## D

- Keep: "Both edges are still there. `writes` now has 6 runs, not 7. `reads` still has 7."
- The other 6 runs that wrote `daily_sales` carry the `writes` edge. The lost `COMPLETE` changes
  only the count of runs, as in Chapter 9.
- Compare this with what you wrote.
- A run with a `START` at the collector and no `COMPLETE`, `ABORT` or `FAIL` is an open run. (Write
  "open run" plainly, not in bold.)
- The next cell lists the open runs at 09:00 on Monday 14. For each one it shows the seconds since
  the run started (`seconds since`), and how many seconds that job's runs that ended usually took
  (`usual seconds`).

## E

- The cell lists one open run: `build_daily_sales`, started at 02:30:00 on Thursday 10.
- Keep: "That is 369000 seconds before Monday 09:00, more than four days. The job's runs that ended
  took 21 seconds."
- That gap suggests the `COMPLETE` was lost. It does not prove it: a run that hangs and never ends
  leaves the same events at the collector, a `START` and nothing after it.
- So the events at the collector cannot settle whether the run ended. Evidence from outside the
  events can: what the run wrote.
- The run early on Thursday 10 writes Wednesday 9's row of `daily_sales`, and each run of
  `build_daily_sales` writes one row. The next cell reads that row from the warehouse.

## F

- Keep: "The row is there: 15375 pence for Wednesday 9."
- The row shows that the run wrote it. It does not show how the run ended: a run can write its row
  and then fail.
- Then this heading, on its own line: `### A function that ran once`
- `remove_return` ran once in the week: on Saturday 12 at 16:50:02, when the returns desk deleted
  `r-203`.
- Its `START` names no dataset. It carries the object it was started for,
  `s3://shop-returns/r-203.json`, in its `shop_objectChange` facet. Its `COMPLETE` names the
  dataset it wrote, `returns`.
- The next cell loses that `COMPLETE` and builds the graph from what arrived.

## G

- `remove_return` has no edge in the graph. With every event, it has one edge: it writes
  `returns`.
- The `START` that arrived names the object `r-203.json`, not the table `returns`.
- The graph now shows `record_return` as the only program that writes `returns`.
- The next cell lists the open runs again.

## H

- The open run of `remove_return` started at 16:50:02 on Saturday 12. Its `usual seconds` is empty:
  the function has no other run that ended.
- Then this heading, on its own line: `### Sending again`
- Keep the first draft's H from "So far, each program sends each event once and keeps nothing."
  to the end, with its facts unchanged: the collector acknowledges each event it receives; the
  program keeps each event until it is acknowledged; it sends the event again if no
  acknowledgement comes within 30 seconds (keep: "It sends the event again if no acknowledgement
  comes within 30 seconds."); every event sent then arrives once or more; this delivery is at least
  once; the next cell loses the same `COMPLETE` once, sends with `at_least_once=True`, and lists
  the events that were sent or received more than once.

## I

- The `COMPLETE`'s event time is 16:50:04 on Saturday 12.
- The program sent it at 16:50:05. No acknowledgement came, so it sent it again at 16:50:35, 30
  seconds later.
- The collector received it once, at 16:50:37.
- Next, the `COMPLETE` arrives and its acknowledgement is lost instead.
- Before you change the cell, write in the next cell how many times the collector will receive
  the `COMPLETE`.

## IP

This slot is the text of a cell the reader writes in. Write exactly two lines: the question, then
a line of eight full stops.

- The question: how many times will the collector receive the `COMPLETE`, with its
  acknowledgement lost?

## IR

- In the cell that ends `again.retried()`, change `lose=` to `lose_ack=`. Select that cell and press
  **Run below**.
- Keep: "the `COMPLETE` is sent twice and received twice: at 16:50:07 and at 16:50:37".
- The first copy arrived, and its acknowledgement was lost, so the program sent it again at
  16:50:35.
- Compare this with what you wrote.
- At least once delivers every event the program sends, and can deliver one twice.

## K

A list of three readings, then a list of three results, then two sentences.

- Keep the opening: "Complete" could mean three things, each needing something different:
- Reading 1: every event a program sends arrives. It needs delivery at least once, or a path that
  loses nothing.
- Reading 2: every program that changes the data sends events. It needs each such program to
  send them.
- Reading 3: every run's end is known, and so its edges. It needs a `COMPLETE`, `ABORT` or `FAIL`
  at the collector for each run that has ended.
- Then: The shop's records meet these as follows:
- Result 1: met with at least once, not without it. One lost `COMPLETE` left a run open, and for
  `remove_return` left no edge.
- Result 2: not met. The export sends no events (Chapter 13).
- Result 3: met with at least once for a run whose program sent its end. Not met for a program that
  stops before it sends its `COMPLETE`, `ABORT` or `FAIL`, or for a run that has not ended: there is
  no end to send again.
- Compare these with what you wrote.
- The requirement does not say which of these it means.

## Z

- Keep the heading `### Before Chapter 19`.
- A summary paragraph with these facts, in order:
  - The lost `COMPLETE` of `build_daily_sales` left both its edges in the graph, because the job's
    other runs carried them. It left one run open.
  - The events at the collector could not tell a lost `COMPLETE` from a run that never ended. The
    time since it started suggested a loss; the warehouse's row showed the run had written it, not
    how the run ended.
  - For `remove_return`, which ran once, the lost `COMPLETE` left no edge.
  - Sending again until acknowledged delivered the event. A lost acknowledgement delivered it twice.
- Keep: "Chapter 19 asks what ingestion does with an event it receives twice."
- Keep the three questions of the first draft's Z as a list.
- Keep the heading `### How this differs from a real platform` and its four bullets, but in the
  second bullet end after "at random" (cut "and a collector can be down"). Add a fifth bullet:
  the OpenLineage documentation's run-cycle page says a streaming job's runs have no expected
  terminal event under normal operation, so there an open run is normal.
