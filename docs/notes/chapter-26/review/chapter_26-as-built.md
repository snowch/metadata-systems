[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 25](chapter_25.ipynb) · [Next: Chapter 27](chapter_27.ipynb)

# Chapter 26: Build the lineage graph

**Objectives**

- Build the lineage graph one stored event at a time, with each edge's runs and its first and last time.
- Find what a late event does to an edge's last time.
- Save the graph and load it again after a restart.
- Question the requirement "Lineage must show the platform as it is now."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## Edges with their times

Chapter 9 built the edges by job from all the week's events at once. Here the lineage graph is kept up to date as each event is stored, one event at a time, from the collector's file.

The file is the one Chapter 25 built. It has the shop's own versions of your three pieces. The week includes the returns desk and the faults from Part V. From Sunday 13, `build_daily_sales` reads the analyst's copy instead of `clean_orders` (Chapter 9).

The next cell reads the file: 82 events.

    >>> week26 = shop.run_week(["returns", "source"])
    >>> stored26 = shop.lineage_graph.stored(week26)
    >>> print(len(stored26), "events in the file")
      82 events in the file

Each edge in the graph is one program reading or writing one dataset. For each edge, the graph keeps the runs that had it, and the first and last time an event named it.

`shop.lineage_graph.edges_of(event)` gives the edges that one event names. You write `add(edges, event)`, which updates the graph for one event.

The next cell holds the function `add` as it stands. It creates an edge the first time an event names it, adds the event's run to that edge, and sets the edge's last time to the time of each event as it arrives.

    >>> def add(edges, event):
    >>>     for key in shop.lineage_graph.edges_of(event):
    >>>         edge = edges.setdefault(key, {"runs": set(), "first": event["eventTime"], "last": event["eventTime"]})
    >>>         edge["runs"].add(event["run"]["runId"])
    >>>         edge["last"] = event["eventTime"]

The events reach the graph in the order they arrived. Wednesday 9's `COMPLETE` of `build_daily_sales` was held up. It arrived at 04:30:24 on Thursday 10, after Thursday 10's `COMPLETE` of `build_daily_sales` (Chapter 20).

Before you read on, write in the next cell when the graph, as it stands at 09:00 on Thursday 10, will show that `build_daily_sales` last wrote `daily_sales`.

    [WRITE] At 09:00 on Thursday 10, when will the graph show that build_daily_sales last wrote daily_sales?
    [WRITE] ........

    >>> shop.lineage_graph.check(week26, add)
      | test | passes
      | Built from the whole file, the graph has Chapter 9's edges, each with the same number of runs. | yes
      | At 09:00 on Thursday 10, `build_daily_sales` last wrote `daily_sales` at 2026-09-09T02:30:21Z, not 2026-09-10T02:30:21Z. | no
      | Saved and loaded again after the restart, the graph goes on from where it was. | yes

The check runs 3 tests. As `add` stands, 2 pass.

Built from the whole file, the graph has Chapter 9's edges, each with the same number of runs.

Saved as lines, one for each edge, and loaded again after the collector's restart, the graph goes on from where it was.

The third fails: at 09:00 on Thursday 10, the graph shows `build_daily_sales` last wrote `daily_sales` at 02:30:21 on Wednesday 9, not on Thursday 10. Wednesday's `COMPLETE` arrived last, so it set the edge's last time.

Compare this with what you wrote.

Change `add` so that an edge's first time is the earlier of its first time and the event's time, and its last time is the later of its last time and the event's time. Select the cell with `add` and press **Run below**. All 3 tests pass.

The next cell builds the graph from the whole file and lists the edges of `build_daily_sales`.

    >>> graph26 = shop.lineage_graph.build(week26, add)
    >>> shop.lineage_graph.table(graph26, "build_daily_sales")
      | job | edge | dataset | runs | first | last
      | shop/build_daily_sales | reads | s3://shop-scratch/clean_orders_copy.csv | 2 | 2026-09-13T02:30:00Z | 2026-09-14T02:30:21Z
      | shop/build_daily_sales | reads | warehouse://shop-warehouse/shop.analytics.clean_orders | 5 | 2026-09-08T02:30:00Z | 2026-09-12T02:30:21Z
      | shop/build_daily_sales | writes | warehouse://shop-warehouse/shop.analytics.daily_sales | 7 | 2026-09-08T02:30:21Z | 2026-09-14T02:30:21Z

`build_daily_sales` reads `clean_orders` in 5 runs, first at 02:30:00 on Tuesday 8 and last at 02:30:21 on Saturday 12.

`build_daily_sales` reads the analyst's copy, `clean_orders_copy.csv`, in 2 runs, from 02:30:00 on Sunday 13 to 02:30:21 on Monday 14.

`build_daily_sales` writes `daily_sales` in 7 runs.

## The platform now

[BOX] The head of the shop's requirement: "Lineage must show the platform as it is now."

Before you read on, write in the next cell what "as it is now" means to you here.

    [WRITE] What does "as it is now" mean here?
    [WRITE] ........

"Now" could mean three things. Each needs something different.

- the edges of each program's latest run, with each edge's last time and each program's latest run;
- every edge ever seen, with every edge kept and nothing removed;
- the edges seen in the last 2 days, with each edge's last time and a window.

The next cell shows, for each edge of `build_daily_sales` at 09:00 on Monday 14, which of the three readings includes it.

    >>> shop.lineage_graph.now(graph26, "2026-09-14T09:00:00Z")
      | edge | dataset | in the latest run | ever | in the last 2 days
      | reads | clean_orders_copy.csv | yes | yes | yes
      | reads | shop.analytics.clean_orders | no | yes | no
      | writes | shop.analytics.daily_sales | yes | yes | yes

`build_daily_sales`'s reads of `clean_orders` are in "ever" only. Its reads of the analyst's copy, and its writes to `daily_sales`, are in all three readings.

The graph keeps each edge's first and last time, so it can answer all three readings. A graph with no times on its edges can answer only "ever".

The requirement does not say which reading it means.

## Before Chapter 27

- The graph, built one stored event at a time, matched Chapter 9's edges and run counts.
- Setting an edge's last time to each arriving event's time let Wednesday's late `COMPLETE` make Thursday's write look a day old.
- Taking the earlier and the later of two times fixed the edge's last time.
- Saved and loaded, the graph went on after the restart.
- The graph's times answered three readings of "now".

Chapter 27 asks questions of this graph.

- Does your lineage graph keep when each edge was last seen?
- Which of your edges have not been seen for a week?
- Which reading of "now" do your lineage views show?

### How this differs from a real platform

- The shop's graph is kept in the course's code and saved as a list of lines. It is never too big to keep in memory.
- The window of 2 days is the shop's choice.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 25](chapter_25.ipynb) · [Next: Chapter 27](chapter_27.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

