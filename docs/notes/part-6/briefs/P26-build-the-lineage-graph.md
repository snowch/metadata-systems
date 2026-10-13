# Brief P26: Chapter 26, Build the lineage graph

Read `common.md` in this folder first, and `docs/style.md`. Write
`docs/notes/part-6/drafts/P26.md`, with one `## key` heading per slot below, in this order. A
heading inside a slot that this brief gives as `## ...` must be written as `### ...`. The chapter
introduces no new term. Words from earlier chapters: *edges by job* (Chapter 9), the *collector*
(Chapter 18), *event time*, *arrival time* (Chapter 20).

## A

A list of four objectives:

- Build the lineage graph one stored event at a time, with each edge's runs and its first and last
  time.
- Find what a late event does to an edge's last time.
- Save the graph and load it again after a restart.
- Question the requirement "Lineage must show the platform as it is now."

## B

- The heading `## Edges with their times`.
- Chapter 9 built the edges by job from all the week's events at once. Here the lineage graph is kept
  up to date as each event is stored, one event at a time, from the collector's file.
- The file is the one Chapter 25 built, with the shop's own versions of your three pieces. The week
  has the returns desk and Part V's faults, and from Sunday 13 `build_daily_sales` reads the
  analyst's copy instead of `clean_orders` (Chapter 9).
- The next cell reads the file: 82 events.

## C

- Each edge in the graph is one program reading or writing one dataset. The graph keeps, for each
  edge, the runs that had it, and the first and last time an event named it.
- `shop.lineage_graph.edges_of(event)` gives the edges one event names. You write
  `add(edges, event)`, which updates the graph for one event.
- The next cell holds `add` as it stands: it creates an edge the first time an event names it, adds
  the event's run to it, and sets the edge's last time to the time of each event as it arrives.

## D

- The events reach the graph in the order they arrived. Wednesday 9's `COMPLETE` of
  `build_daily_sales` was held up and arrived at 04:30:24 on Thursday 10, after Thursday 10's
  (Chapter 20).
- Before you read on, write in the next cell when the graph, as it stands at 09:00 on Thursday 10,
  will say `build_daily_sales` last wrote `daily_sales`.

## DD

Two lines: the question, then a line of eight full stops.

- The question: at 09:00 on Thursday 10, when will the graph say `build_daily_sales` last wrote
  `daily_sales`?

## E

- The check runs 3 tests. As `add` stands, 2 pass. Built from the whole file, the graph has Chapter
  9's edges, each with the same number of runs. Saved as lines, one for each edge, and loaded again
  after the collector's restart, the graph goes on from where it was.
- The third fails: at 09:00 on Thursday 10, the graph says `build_daily_sales` last wrote
  `daily_sales` at 02:30:21 on Wednesday 9, not on Thursday 10. Wednesday's `COMPLETE` arrived last,
  so it set the edge's last time.
- Compare this with what you wrote.
- Change `add` so that an edge's first time is the earlier of its first time and the event's time,
  and its last time the later of the two. Select the cell and press **Run below**. All 3 tests pass.
- The next cell builds the graph from the whole file and lists the edges of `build_daily_sales`.

## F

- `build_daily_sales` reads `clean_orders` in 5 runs, first at 02:30:00 on Tuesday 8 and last at
  02:30:21 on Saturday 12. It reads the analyst's copy, `clean_orders_copy.csv`, in 2 runs, from
  02:30:00 on Sunday 13 to 02:30:21 on Monday 14. It writes `daily_sales` in 7 runs.

## RH

- The heading `## The platform now`.

## G

- Before you read on, write in the next cell what "as it is now" means to you here.

## GG

Two lines: the question, then a line of eight full stops.

- The question: what does "as it is now" mean here?

## H

- "Now" could mean three things, and each needs something different. Then a list:
  - the edges of each program's latest run: each edge's last time, and each program's latest run;
  - every edge ever seen: every edge kept, and nothing removed;
  - the edges seen in the last 2 days: each edge's last time, and a window.
- The next cell shows, for each edge of `build_daily_sales` at 09:00 on Monday 14, which of the three
  includes it.

## I

- Its reads of `clean_orders` are in "ever" only. Its reads of the analyst's copy, and its writes to
  `daily_sales`, are in all three.
- The graph keeps each edge's first and last time, so it answers all three readings. A graph with no
  times on its edges answers only "ever".
- The requirement does not say which it means.

## Z

- The heading `## Before Chapter 27`.
- Summary facts, in order: built one stored event at a time, the graph matched Chapter 9's edges and
  run counts; setting an edge's last time to each arriving event's time let Wednesday's late
  `COMPLETE` make Thursday's write look a day old; taking the earlier and the later of two times
  fixed it; saved and loaded, the graph went on after the restart; its times answered three readings
  of "now".
- Chapter 27 asks questions of this graph.
- Three questions, as a list: Does your lineage graph keep when each edge was last seen? Which of
  your edges have not been seen for a week? Which reading of "now" do your lineage views show?
- The heading `### How this differs from a real platform`, and two bullets:
  - The shop's graph is kept in the course's code and saved as a list of lines. It is never too big
    to keep in memory.
  - The window of 2 days is the shop's choice.
