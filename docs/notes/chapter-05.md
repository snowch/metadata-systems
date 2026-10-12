# Chapter 5: Metadata as a graph

A working note. Written on 12 October 2026, at the author's request to "author chapter 5 and 6", as
a notebook (`notebook/chapter_05.py`) in the form of Chapters 3 and 4.

## What the chapter does

Jo Marsh, in finance, wants daily revenue to count orders with no customer id, which Chapter 2 found
`clean_orders` leaves out, and asks: "Show me everything related to `daily_sales`." Jo wants to know
where those orders are lost and what a change would touch. The reader takes Chapter 4's records after
both of its changes (two spellings merged, the data engineer a team, the `drops` line kept as text),
adds a line per column saying which dataset it belongs to (`of`), and:

- makes the records a **graph**: each entity a **node**, each line whose value names another entity
  an **edge** labelled with its attribute: 12 nodes, 9 edges of three kinds, drawn in 3 parts;
- writes which nodes a **traversal** from `j.marsh` against the `responsible` arrows will reach, and
  which it would reach along them; runs it (`daily_sales`, `sales_dashboard`), changes `"in"` to
  `"out"`, presses **Run below**, and sees no row;
- writes which nodes a traversal along every edge, both ways, from `daily_sales` will reach, and
  whether it reaches `clean_orders`, which holds the `drops` line: it reaches the dashboard through
  Jo Marsh, not because the dashboard reads `daily_sales`, and misses `clean_orders`; from
  `clean_customers` the same traversal reaches `clean_orders` through the team responsible for both;
- questions "Show everything related to `daily_sales`." (below), and is told what can be sent to Jo.

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
- **Objective:** the reader learns that a traversal's answer is fixed by the direction it follows
  each kind of edge in, by changing one direction and seeing the answer empty.
- **Known before:** the graph, drawn and listed; what `in`, `out` and a path mean.
- **Driving question:** which assets is Jo Marsh responsible for, and what does the same traversal
  return along the arrows instead?
- **The action:** write both expectations; read the rows; change `"in"` to `"out"` and press **Run
  below**; compare.
- **Why the action:** the change is the reader's own; the empty answer comes from their edit.
- **Evidence:** `daily_sales` and `sales_dashboard`, 1 step each; then "No rows."
- **Consequence:** a reader who expected the same assets either way learns that a direction is part
  of the question.
- **Predictable:** yes, from the drawing's arrows.
- **Gives nothing away:** the prose above names the start, the kind of edge and the direction, not
  the nodes.
- **Not knowing:** not the right answer: the drawing settles it.
- **Next question:** what does a traversal along every edge return?
- **An experiment:** commit, run, change, run again, compare.

### `every-edge`

- **Role:** experiment
- **Objective:** the reader discovers that following every edge reaches what the lines join to the
  start, which can include what is unrelated by data and miss what Jo's question needs.
- **Known before:** the graph; the first traversal; Jo's purpose; the `drops` line on
  `clean_orders`.
- **Driving question:** which nodes does a traversal along every edge reach from `daily_sales`, and
  does it reach `clean_orders`?
- **The action:** write the expectation; read the rows and the dashboard's path; then the same
  traversal from `clean_customers`.
- **Why the action:** the effect (which nodes) is asked first; the path is the evidence for why.
- **Evidence:** 5 nodes from `daily_sales`, the dashboard by way of Jo Marsh, no `clean_orders`;
  `clean_orders` from `clean_customers` by way of the team.
- **Consequence:** a reader who expected `clean_orders` learns that a text line is no edge, and that
  nothing joins `clean_orders` to `daily_sales` in these records.
- **Predictable:** yes, from the drawing's parts.
- **Gives nothing away:** the question names `clean_orders` and why it matters to Jo, not whether it
  is reached.
- **Not knowing:** a reasonable answer about what "related" means, which the requirement takes up.
- **Next question:** what does "related" mean?
- **An experiment:** commit, run, compare.

## Requirements

The chapter questions "Show everything related to `daily_sales`.", the plan's candidate, with the
reading cell and the readings after it.

1. **What it says:** everything related to `daily_sales`.
2. **What it might mean:** what it is made from; what reads it; who is responsible for it; where it
   is kept.
3. **What each needs:** an edge between datasets through what makes them, one way or the other; the
   `responsible` edge; the warehouse as an entity with an edge to it.
4. **What the records hold:** `responsible`, `team` and `of` edges, and the `drops` line as text.
5. **Whether it is met:** as written, by a list of what a traversal along every edge reaches; as Jo
   meant it (where the orders are lost, what a change would touch: the first two readings), by no
   traversal of these records. The page says what can be sent: who is responsible, the `drops` line,
   and that the records do not say what `daily_sales` is made from or what reads it.

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

Brief HA, after the review: two of the brief's own facts were wrong, and the fewest words fixed them
in the draft: "every `responsible` edge points to `j.marsh`" (only those at `j.marsh` do), and a word
rule that forbade "made from" about `daily_sales` while a reading needed it, which the draft met
with "takes its data from". "Under a comment" became "under a `#` note", the course's word; the
close lost a lead-in ("Three questions to take with you") and a claim that the traversals showed
what the definitions said. The agent made one stray session listing, reported it, and used nothing.

## The review

A reviewer on another model read the chapter as a learner (`review/findings.md`, 18 findings) and
an independent sceptic attacked each finding (`review/verdicts.md`). Acted on: Jo's purpose returned
to and what to send Jo said (2); the `drops` line kept, so the records are Chapter 4's (3); the
readings' contradictions (4, 8); the narrowed conclusion (5); a traversal the reader changes and runs
again (7); a reality note that says how a real platform differs (14); the close's actor (18); and the
small parts of 1, 6, 10 and 11. Rejected by the sceptic: 13 (the engine builds a graph where one name
has two types) and 15 (the platform figure is the course's convention).

## Measured

12 October 2026, local build (`docs/notes/notebook-prototype.md`, "Chapters 5 and 6"): Run all 8.3
to 8.7 s; peak memory 397 to 403 MB; 0.32 MB from Chapter 4's link.

## Known gaps

- The published page's run time is to be measured after the deploy, as Chapters 3 and 4's were.
- The reader's expectations are free text, kept by **Save**.
