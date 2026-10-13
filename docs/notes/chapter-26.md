# Chapter 26: Build the lineage graph

A working note. Written on 13 October 2026 with Chapters 24, 25, 27 and 28
(`notebook/chapter_26.py`).

## What the chapter does

The reader builds the lineage graph one stored event at a time, from the collector's file (82
events, the week with the returns desk, the `source` change and Part V's faults):

- writes `add(edges, event)`, which keeps each edge's runs and first and last times;
- predicts what the graph shows at 09:00 on Thursday 10 for `build_daily_sales` writing
  `daily_sales`, with `add` taking each arriving event's time as the last; finds Wednesday's, because
  Wednesday's COMPLETE arrived late; takes the earlier and the later of two times; 3 of 3;
- reads the edges of `build_daily_sales`: `clean_orders` in 5 runs, last on Saturday 12; the copy in
  2, Sunday and Monday;
- questions "Lineage must show the platform as it is now."

## What was built for it

`notebook/shop/lineage_graph.py`: `edges_of`, `stored` (the collector's file with the shop's
pieces), `build` with a save and load at the restart, `table`, `check`, `now`.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `late-last-time`

- **Role:** experiment
- **Objective:** the reader discovers that a graph updated in arrival order lets a late event make an
  edge look older, and that keeping the later of two times fixes it.
- **Known before:** Chapter 20's late COMPLETE.
- **Driving question:** at 09:00 on Thursday 10, when does the graph say `daily_sales` was last
  written?
- **The action:** write the prediction; read the check; change `add`; press **Run below**.
- **Why the action:** the reader's own `add` sets the time.
- **Evidence:** Wednesday 9's time as `add` stands; 3 of 3 after.
- **Consequence:** an edge's time must come from the events, compared, not from their order.
- **Predictable:** yes, from Chapter 20.
- **Gives nothing away:** the cell asks for a time.
- **Not knowing:** fair.
- **Next question:** which edges does the platform have now?

### `edges-of-build-daily-sales`

- **Role:** inspect
- **Serves:** what changed on Sunday? The three edges with their runs and times.
- **Why now:** the requirement's readings are read off these times.

### `now`

- **Role:** experiment (completes the requirement): each edge under three readings of "now".

## Requirements

"Lineage must show the platform as it is now." Readings: each program's latest run's edges; every
edge ever seen; edges seen in the last 2 days. `clean_orders` is in "ever" only. Time-stamped edges
answer all three; a graph with no times answers only "ever". The figure that questions it is the
free-text cell after the box.

## Originality

The obvious example is a lineage tool's documentation of a graph that shows the latest version of
each job. This chapter's graph is built one event at a time from the shop's own collector, with the
shop's late event, and the three readings are read from its own times.
