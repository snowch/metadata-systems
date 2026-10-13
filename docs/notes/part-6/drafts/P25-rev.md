## A

- Receive the week's events with Part V's faults, all at once.
- Write the key that recognises a repeat, and the rule for which of a run's events holds its state.
- Restart the collector, and find what a restart loses.
- Question the requirement "The collector must reject invalid events."

## B

### The faults, together

Part V broke the path to the collector one fault at a time. Here the shop's collector receives the week, returns desk events included, and the faults arrive together.

Among them is an event from the developer's laptop: a `START` of `try_daily_sales`, in a producer and a namespace the shop does not list, with no `eventTime`.

The next cell lists the 5 arrivals the faults touch. Each row gives when it arrived, its program, its type, its event time and its fault.

## C

The collector does four things with each event that arrives:

1. it refuses an event that breaks the rules of Chapter 8's check;
2. it drops an event whose key it has already seen;
3. it keeps every other event, once, in its file;
4. it keeps, for each run, the event that holds the run's state, and replaces it with an event that arrives when `newer(event, current)` gives `True`. `current` is the event it now holds for that run.

A run's state is its latest event, as in Chapter 9. The collector keeps each run's state so that it can say what state a run is in without reading its file again.

You write the pieces for items 2 and 4: `key(event)` and `newer(event, current)`. A third piece comes later.

An event's run id is `event["run"]["runId"]`; its type is `event["eventType"]`; its time is `event["eventTime"]`. A key must be a value a set can hold, such as a tuple or a piece of text.

The next two cells hold the two pieces as they stand: `key` gives the event's whole content as JSON text, and `newer` always gives `True`, so the last event to arrive holds the state.

The check below them runs the collector over the week and prints 5 tests. As the cells stand, 2 of 5 pass.

The two that pass: the developer's event is refused, and the edges by job built from the file match the week with no faults.

## D

Three tests fail. The file holds 69 events, not 68: the content key dropped `remove_return`'s repeat, which is the same event, and kept Thursday's retry, whose time differs. The run early on Thursday 10 ends at 02:30:52. The run early on Friday 11 is `START`.

The edges-by-job test passes anyway. It compares each edge's run count and its first and last time over the week, so it cannot see that one run ends at the wrong time.

Change `key` so that it gives the event's run id and its event type, as Chapter 19's deduplication by run did. Select the cell and press **Run below**. 4 of 5 pass. The file holds each of the 68 events once, and the run early on Thursday 10 ends at 02:30:21.

The collector normalises each event before it keeps it (Chapter 9's second stage), so every time is written the same way, in UTC with `Z`, and comparing two times as text puts them in order.

Then change `newer` so that it gives whether the event's time is not earlier than the time of `current`: the event time, not the arrival time (Chapter 20). Select the cell and press **Run below**. 5 of 5 pass. The run early on Friday 11 is `COMPLETE`, because its `START`, which arrived later, has the earlier time.

Wednesday 9's `COMPLETE`, held up until 04:30:24 on Thursday 10, needs no piece: it is the first `COMPLETE` of its run, and the collector keeps it whenever it arrives. Chapter 26 uses it.

## E

### A restart

The collector holds two things outside its file: the keys it has seen, and each run's state. Its file survives a restart.

In the next check, the collector restarts on Saturday 12 at 16:50:20. The restart falls between the two arrivals of `remove_return`'s `COMPLETE`, at 16:50:07 and 16:50:37.

After a restart, the collector reads its file and rebuilds each run's state. Its keys are what `start(stored)` gives, from the events in the file. `start` is the function in the cell below the one you write in.

Before you read on, write in the next cell whether the collector drops the `COMPLETE` that arrives again at 16:50:37.

## F

With your `key` and `newer`, the check shows 4 of 6 passing. The `COMPLETE` that arrived again after the restart is kept a second time, and the file holds 69 events.

`start` as it stands gives an empty set. The keys the collector had seen were not in its file, so the restart lost them. After the restart, the collector's set of keys was empty. The event's key was right, and its first copy was in the file, but the set did not hold its key.

Compare this with what you wrote.

Change `start` so that it gives the key of every event in `stored`. Select the cell and press **Run below**. 6 of 6 pass.

## H

"Invalid" could mean several things, and each needs something different:

- an event that breaks the specification's rules: it needs those rules, as many as Chapter 8's check holds. The collector refuses it, as it refused the developer's event with no `eventTime`.
- an event from a producer or a job the shop does not know: it needs a list of the shop's producers and jobs, which the collector does not keep. The developer's event, from `try_daily_sales`, breaks no rule once it has a time, so it would have been kept.
- an event that arrives out of order, such as a `START` after its `COMPLETE`: it needs a rule about order. Friday 11's `START` breaks no rule of the specification, and refusing it would refuse a valid event.

The collector meets the first reading. It keeps no list for the second, and it does not refuse an event for the third.

The requirement does not say which it means.

## Z

### Before Chapter 26

The collector refused the developer's event with no `eventTime`. A key of run id and event type let the collector keep each of the 68 events once, through a repeat and a retry with a new time. Comparing event times kept each run's state right when its events arrived out of order. After a restart, the collector kept a repeated event a second time, until `start` rebuilt its keys from the file. The check could not show what a key of run id and event type does with a run that sends more than one event of a type, because the shop's programs never do.

Chapter 26 builds the lineage graph from the collector's file.

- What does your collector keep only in memory?
- What happens to it when the collector restarts?
- Which events does your collector refuse, and by which rule?

### How this differs from a real platform

- The shop's file is a list in the course's code. It is never full, never slow and never lost.
- The shop's programs send one `START` and one `COMPLETE` for each run. The OpenLineage specification allows a run to send `RUNNING` and `OTHER` events as well, and several of them, so a key of run id and event type would drop real events there (Chapter 19).
- Comparing event times gives the order things happened in only while the programs' clocks agree (Chapter 20).
- The shop's collector keeps every key it has seen, with no time limit.
- The OpenLineage specification says nothing about what a consumer does with a repeat or a late event.
