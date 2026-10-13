# Revision brief P26: Chapter 26, Build the lineage graph

Read `rev-common.md` first. Redraft these slots: A, B, C, E, F, H, I, Z. Terms: none new.

## A

A list of four objectives:

- Build the lineage graph one stored event at a time, with each edge's runs and its first and last
  time.
- Find what a late event does to an edge's last time.
- Save the graph and load it after the collector's restart, with its edges and times kept.
- Question the requirement "Lineage must show the platform as it is now."

## B

- Keep the heading `### Edges with their times`.
- Chapter 9 built the edges by job from all the week's events at once. Here the lineage graph is kept
  up to date as each event is stored, one event at a time, from the collector's file.
- The file is Chapter 25's collector's, with the shop's own versions of your three pieces, run over a
  longer week: the returns desk, Part V's faults, and the analyst's job `copy_clean_orders`, which
  copies `clean_orders` every night.
- From Sunday 13, `build_daily_sales` reads the analyst's copy instead of `clean_orders` (Chapter 9).
- The next cell reads the file: 82 events. That is 14 more than Chapter 25's 68: the copy job's 7
  runs, with 2 events each.

## C

- Each edge in the graph is one program reading or writing one dataset. For each edge, the graph
  keeps the runs that had it, and the first and last time an event named it.
- Those times are the events' own times, set by the programs that sent them. The order the events
  arrived in decides only the order in which the graph takes them (Chapter 20).
- `shop.lineage_graph.edges_of(event)` gives the edges that one event names. You write
  `add(edges, event)`, which updates the graph for one event.
- The next cell holds the function `add` as it stands. It creates an edge the first time an event
  names it, adds the event's run to that edge, and sets the edge's last time to the time of each event
  it takes.

## E

- The check runs 3 tests, in this order:
  1. the graph built from the whole file;
  2. the graph as it stands at 09:00 on Thursday 10;
  3. the graph saved and loaded again.
  Write that as a numbered list.
- The third test saves the graph as one line for each edge (its runs, first time and last time) and
  loads it again after Chapter 25's restart, on Saturday 12 at 16:50:20. The graph is held in memory,
  like the collector's keys, so a restart loses it unless it is saved.
- Keep: "As `add` stands, 2 pass."
- The first passes: built from the whole file, the graph has the same edges and run counts as Chapter
  9's way of building edges by job gives for this file. This file has no line cut short, so `daily_sales`
  is written in 7 runs, not Chapter 9's 6.
- The third passes: the loaded graph holds the same edges, runs and times as the one that was never
  saved.
- The second fails: at 09:00 on Thursday 10, the graph shows `build_daily_sales` last wrote
  `daily_sales` at 02:30:21 on Wednesday 9, not on Thursday 10. Wednesday's `COMPLETE` arrived last,
  so `add` took it last and set the edge's last time from it.
- Compare this with what you wrote.
- Change `add` so that an edge's first time is the earlier of its first time and the event's time, and
  its last time is the later of its last time and the event's time. Select the cell with `add` and
  press **Run below**. All 3 tests pass.
- No event in this week names an edge for the first time after a later event has named it, so the
  check cannot tell whether the first time is right. The earlier of the two times is still the rule
  that keeps it right when that happens.
- The next cell builds the graph from the whole file and lists the edges of `build_daily_sales`, to
  show what the graph holds about Sunday's change of input.

## F

- Keep: "`build_daily_sales` reads `clean_orders` in 5 runs, first at 02:30:00 on Tuesday 8 and last at 02:30:21 on Saturday 12."
- `build_daily_sales` reads the analyst's copy, `clean_orders_copy.csv`, in 2 runs, from 02:30:00 on
  Sunday 13 to 02:30:21 on Monday 14.
- `build_daily_sales` writes `daily_sales` in 7 runs.
- A first time of 02:30:00 is a run's `START`: the graph takes every event's time, `START`s included.

## H

- Chapter 9 asked what "current" means of the edges by job, which kept no times. This graph keeps
  each edge's times, which allows one more reading: a window.
- "Now" could mean three things. A list; each item says what it needs:
  - the edges of each program's latest run: each edge's last time and each program's latest run;
  - every edge ever seen: every edge kept, and nothing removed;
  - the edges seen in the last 2 days: each edge's last time, and the length of the window.
- The next cell shows, for each edge of `build_daily_sales` and of `record_return` at 09:00 on
  Monday 14, which of the three readings includes it.

## I

- `build_daily_sales`'s reads of `clean_orders` are in "ever" only. Its reads of the analyst's copy,
  and its writes to `daily_sales`, are in all three readings.
- `record_return` last ran on Friday 11 at 13:15. Its read of `r-204.json` and its write to `returns`
  are in its latest run, but not in the last 2 days. Its reads of the other three return files are in
  "ever" only.
- So the latest run and the window disagree for a program that has not run for 2 days.
- The graph keeps each edge's first and last time, so it answers all three readings. Without times
  on its edges, the graph alone answers only "ever".
- The requirement does not say which reading it means.

## Z

- Keep the heading `### Before Chapter 27`.
- A list:
  - The graph, built one stored event at a time, had the same edges and run counts as Chapter 9's way
    of building them from the same file.
  - Setting an edge's last time from each event as it was taken let Wednesday's late `COMPLETE` make
    Thursday's write look older: Wednesday's 02:30:21.
  - Taking the earlier and the later of two times fixed the edge's last time.
  - Saved as lines and loaded after the restart, the graph kept its edges, runs and times.
  - The graph's times answered three readings of "now".
- The graph could not show whether an edge that has not been seen for a while has stopped or is only
  idle: `record_return` had not run for 2 days.
- Chapter 27 asks questions of this graph.
- Three questions, as a list:
  - Does your lineage graph keep when each edge was last seen?
  - Which of your edges have not been seen for a week?
  - Which reading of "now" do your lineage views show?
- Keep the heading `### How this differs from a real platform`, then a list:
  - The shop's graph is held in memory and saved as a list of lines, one for each of its 17 edges.
    Chapter 23 projected what a platform of 10,000,000 assets holds.
  - The graph takes its times from the events' own times, which is the shop's choice. Those times
    give the order things happened in only while the programs' clocks agree (Chapter 20).
  - The window of 2 days is the shop's choice.
