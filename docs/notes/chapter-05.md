# Chapter 5: Metadata as a graph

A working note. Written on 12 October 2026, at the author's request to "author chapter 5 and 6", as
a notebook (`notebook/chapter_05.py`) in the form of Chapters 3 and 4.

## What the chapter does

Jo Marsh replies to Chapter 4's list of owners: before revenue counts orders with no customer id,
"Show me everything related to `daily_sales`." The reader takes the records as Chapter 4 left them
(two spellings merged, the data engineer a team), adds a line per column saying which dataset it
belongs to (`of`, so the dot in a column's identifier is no longer the only tie), and:

- makes the records a **graph**: each entity a **node**, each line whose value names another entity
  an **edge** labelled with its attribute: 12 nodes, 9 edges of three kinds, drawn in 3 parts;
- writes what a **traversal** from `daily_sales` along `responsible` and `team` will reach, then
  runs it: `j.marsh`, then `finance`;
- writes what a traversal along every edge, both ways, will reach, then runs it: 5 nodes, the
  dashboard among them, reached because Jo Marsh is responsible for both, not because it reads
  `daily_sales`; from `clean_customers` the same walk reaches `clean_orders` through the team
  responsible for both, and `clean_orders` is not made from it;
- questions "Show everything related to `daily_sales`." (below).

It introduces the plan's four terms, the first three in "The records as a graph" and *traversal* in
"Following edges", which the term test holds.

## What was built for it

- `notebook/shop/graph.py`: `graph(records, model)`, with `nodes`, `edges`, `traverse(start,
  follow)` (a breadth-first walk over the edges `follow` names, each `out`, `in` or `both`, listing
  each node reached, its steps and its path) and `drawing`: an SVG image in the course's phone-width
  form (340 units, 14-unit text, its own light and dark colours), each connected part drawn on its
  own, in layers by type (columns, assets, people, teams) when the graph has no jobs.
- The drawing is a cell's output, not a figure drawn into Markdown, because it is drawn from the
  reader's records, which the reader may change.

## Figures

### `platform`

- **Role:** reference
- **Serves:** the assets in their systems; Jo's question is about one of them.
- **Why now:** the map appears in every chapter; it gains no arrow here, because no line yet records
  what is made from what.

### `nodes-and-edges` and `drawing`

- **Role:** inspect
- **Serves:** what the graph holds: 12 nodes, 9 edges, three kinds, and its 3 parts, which the
  traversals then walk.
- **Why now:** the terms have just been given; the reader sees them applied to their own records
  before predicting a walk over them.

### `first-traversal`

- **Role:** experiment
- **Objective:** the reader learns that a traversal's answer is fixed by the edges and directions it
  is told to follow.
- **Known before:** the graph, drawn and listed; the meaning of `out`.
- **Driving question:** which nodes does a walk from `daily_sales` along `responsible` and `team`
  reach?
- **The action:** write the expectation, then read the walk's rows.
- **Why the action:** committing first makes the reader trace the edges in the drawing.
- **Evidence:** `j.marsh` (1 step), `finance` (2), with paths.
- **Consequence:** a reader who expected the dashboard learns that `out` does not walk back along an
  arrow.
- **Predictable:** yes, from the drawing.
- **Gives nothing away:** the prose above names the edges followed, not the nodes reached.
- **Not knowing:** not the right answer: the drawing settles it.
- **Next question:** what does a walk along every edge return?
- **An experiment:** commit, run, compare.

### `every-edge`

- **Role:** experiment
- **Objective:** the reader discovers that following every edge returns what shares an owner with
  the start, which can pass for what is related by data.
- **Known before:** the graph; the first walk.
- **Driving question:** which nodes does a walk along every edge, both ways, reach, and why each?
- **The action:** write the expectation and the reason for each node, then read the rows and their
  paths; then the same walk from `clean_customers`.
- **Why the action:** the reasons are the point: the path column shows each one.
- **Evidence:** 5 nodes from `daily_sales`, the dashboard by way of Jo Marsh; `clean_orders` from
  `clean_customers` by way of the team.
- **Consequence:** a reader who said "the dashboard, because it reads `daily_sales`" was right about
  the node and wrong about the reason the walk found it.
- **Predictable:** the nodes, yes; the reason is what the path teaches.
- **Gives nothing away:** the cell above asks for reasons; nothing names them.
- **Not knowing:** a reasonable answer about whether the dashboard is "related", and the
  requirement takes it up.
- **Next question:** what does "related" mean?
- **An experiment:** commit, run, compare the reasons.

## Requirements

The chapter questions "Show everything related to `daily_sales`.", the plan's candidate, with the
reading cell and the readings after it.

1. **What it says:** everything related to `daily_sales`.
2. **What it might mean:** what it is made from; what reads it; who is responsible for it; where it
   is kept.
3. **What each needs:** an edge between datasets through what makes them, one way or the other; the
   `responsible` edge; the warehouse as an entity with an edge to it.
4. **What the records hold:** `responsible`, `team` and `of` edges.
5. **Whether it is met:** for "who is responsible" (with that person's team, and the columns), and
   for no other reading; a walk along every edge answers none of them, because it mixes kinds.

The reader writes what they would send Jo and what "related" means to them before the readings.

## Originality

The obvious examples are a knowledge-graph tutorial's people-and-films graph, a graph database's
sample social network, or a metadata product's entity graph browsed in its screens. This chapter's
graph is the reader's own records from Chapters 3 and 4, in the course's notation; its point is not
how to store a graph but that a walk's answer is fixed by the kinds of edge it follows, shown by a
walk that reaches the right dashboard for the wrong reason. The shop, its people and its records are
invented for the course.

## What the prose process caught

Brief EA (`docs/notes/chapter-05/briefs/`, with `common.md`), draft under `drafts/`: every fact
present and right; nothing sent back. The warning is brief GA's (Chapter 6's notes). Each drafting
agent was told to use only Read and Write; three of the five agents of this round made one stray
call each (a session listing, a message that failed), reported it, and changed nothing.

## Measured

12 October 2026, local build (`docs/notes/notebook-prototype.md`, "Chapters 5 and 6"): Run all 8.3
to 8.7 s; peak memory 397 to 403 MB; 0.32 MB from Chapter 4's link.

## Known gaps

- The published page's run time is to be measured after the deploy, as Chapters 3 and 4's were.
- The reader's expectations are free text, kept by **Save**.
