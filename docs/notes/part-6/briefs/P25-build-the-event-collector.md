# Brief P25: Chapter 25, Build the event collector

Read `common.md` in this folder first, and `docs/style.md`. Write
`docs/notes/part-6/drafts/P25.md`, with one `## key` heading per slot below, in this order. The
chapter introduces no new term. Words it uses from earlier chapters, with their meanings: the
shop's *collector* (Chapter 18), *delivery*, *at least once* (Chapter 18), *deduplication* (Chapter
19), *event time*, *arrival time* (Chapter 20).

## A

A list of four objectives:

- Receive the week's events with Part V's faults, all at once.
- Write the key that recognises a repeat, and the rule for which of a run's events holds its state.
- Restart the collector, and find what it forgets.
- Question the requirement "The collector must reject invalid events."

## B

- The heading `## The faults, together`.
- Part V broke the path to the collector one fault at a time. Here the shop's collector receives the
  week with the returns desk, and the faults arrive together.
- The next cell lists the 5 arrivals the faults touch, each with its fault.

## C

- The collector does four things with each event that arrives:
  1. it refuses an event that breaks the OpenLineage specification, by Chapter 8's check;
  2. it drops an event whose key it has already seen;
  3. it keeps every other event, once, in its file;
  4. for each run, it keeps the event that holds the run's state, and replaces it when an event
     arrives that `newer` says is newer.
  (Write these four as a numbered list.)
- You write two of these pieces, `key(event)` and `newer(event, current)`. The next two cells hold
  them as they stand: `key` gives the event's whole content as JSON text, and `newer` always gives
  `True`, so the last event to arrive holds the state.
- The check below them runs the collector over the week and prints 5 tests. As the cells stand, 2
  of 5 pass: the broken event is refused, and the graph built from the file is the graph of the week
  with no faults.

## D

- Three tests fail. The file holds 69 events, not 68: the content key dropped `remove_return`'s
  repeat, which is the same event, and kept Thursday's retry, whose time differs. The run early on
  Thursday 10 ends at 02:30:52. The run early on Friday 11 is `START`.
- The graph test passes all the same, because ingestion merges events into runs by run id
  (Chapter 19).
- Change `key` so that it gives the event's run id and its event type, as Chapter 19's deduplication
  by run did. Select the cell and press **Run below**. 4 of 5 pass: the file holds each of the 68
  events once, and the run early on Thursday 10 ends at 02:30:21.
- Then change `newer` so that it gives whether the event's time is not earlier than the time of the
  event it would replace. Select the cell and press **Run below**. 5 of 5 pass: the run early on
  Friday 11 is `COMPLETE`, because its `START`, which arrived later, has the earlier time.
- The collector normalises each event before it keeps it (Chapter 9's first stage), so every time
  is written the same way, in UTC with `Z`, and comparing two times as text puts them in order.

## E

- The heading `## A restart`.
- The collector holds two things in memory: the keys it has seen, and each run's state. Its file
  survives a restart. Its memory does not.
- In the next check, the collector restarts on Saturday 12 at 16:50:20, between the two arrivals of
  `remove_return`'s `COMPLETE`, at 16:50:07 and 16:50:37. When it starts, it reads its file and
  rebuilds each run's state. The keys it remembers are what `start(stored)` gives, from the events
  in the file.
- The next cell holds `start` as it stands: it gives an empty set.
- Before you read on, write in the next cell whether the collector drops the `COMPLETE` that arrives
  again at 16:50:37.

## EE

Two lines: the question, then a line of eight full stops.

- The question: will the collector drop the `COMPLETE` that arrives again after the restart?

## F

- The check shows 4 of 6 passing. The `COMPLETE` that arrived again after the restart is kept a
  second time, and the file holds 69 events.
- After the restart, the collector's set of keys was empty. The event's key was right, and the
  first copy was in the file, but the keys the collector remembered did not include it.
- Compare this with what you wrote.
- Change `start` so that it gives the key of every event in `stored`. Select the cell and press
  **Run below**. 6 of 6 pass.

## RH

- The heading `## Invalid events`.

## G

- Before you read on, write in the next cell what "invalid" means to you here.

## GG

Two lines: the question, then a line of eight full stops.

- The question: what does "invalid" mean here?

## H

- "Invalid" could mean several things, and each needs something different. Then a list:
  - an event that breaks the OpenLineage specification: it needs the specification's rules, which
    Chapter 8's check holds; the collector refuses it, as it refused the event with no `eventTime`;
  - an event from a producer or a job the shop does not know: it needs a list of the shop's
    producers and jobs, which the collector does not keep; the developer's event, had it carried a
    time, would have been kept;
  - an event that arrives out of order, such as a `START` after its `COMPLETE`: it needs a rule
    about order; Friday 11's `START` breaks no rule of the specification, and refusing it would
    refuse a valid event.
- The collector meets the first reading. It keeps no list for the second, and it does not refuse an
  event for the third.
- The requirement does not say which it means.

## Z

- The heading `## Before Chapter 26`.
- Summary facts, in order: the collector refused the event with no `eventTime`; a key of run id and
  event type kept each of the 68 events once, through a repeat and a retry with a new time;
  comparing event times kept each run's state right when its events arrived out of order; after a
  restart, a key it had seen was kept again until `start` rebuilt the keys from the file.
- Chapter 26 builds the lineage graph from the collector's file.
- Three questions, as a list: What does your collector keep only in memory? What happens to it when
  the collector restarts? Which events does your collector refuse, and by which rule?
- The heading `### How this differs from a real platform`, and two bullets:
  - The shop's file is a list in the course's code. It is never full, never slow and never lost.
  - The OpenLineage specification says nothing about what a consumer does with a repeat, a late
    event or a restart (Chapter 8).
