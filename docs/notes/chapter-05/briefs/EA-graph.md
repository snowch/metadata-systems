# Brief EA: Chapter 5, "Metadata as a graph"

Read `docs/notes/chapter-05/briefs/common.md` first: its rules hold here.

This chapter introduces four terms, each where its slot says: **node**, **edge**, **graph** and
**traversal**. Give the plain idea first, then the term in bold. Do not use any of the four before
its slot, objectives included. Words you must not use anywhere: lineage, upstream, downstream,
event, the noun "run", identity, provenance, impact, freshness, observation, namespace, facet, lab,
engine, Jupyter.

## Facts (each checked against the shop's data)

The opening:

- Jo Marsh, in finance, replies to the list of owners you sent at the end of Chapter 4. Jo wants
  daily revenue to count orders that have no customer id, as Jo's meaning of a day's revenue
  already says (Chapter 3), and asks, before anything changes: "Show me everything related to
  `daily_sales`."

The records and the model:

- The records cell holds the records as Chapter 4 left them: the two spellings merged into
  `j.marsh` and `s.lund`, the data engineer a team with the identifier `data_engineering`.
- It adds two lines, under a `#` note: each column of `daily_sales` now says which dataset it
  belongs to, with the attribute `of`: `column daily_sales.day of: daily_sales`. In Chapter 4 only
  the dot in a column's identifier said so, and no check could test it.
- The model cell adds one line, `column of: dataset`.

The graph:

- Each entity the records describe becomes a **node**, named by its identifier.
- Each line whose value is the identifier of another entity becomes an **edge**: it goes from the
  line's entity to the entity its value names, and it carries the line's attribute as its label.
  `dataset daily_sales responsible: j.marsh` is the edge from `daily_sales` to `j.marsh`, labelled
  `responsible`. A line whose value is text, such as a `means` line, is no edge.
- Nodes and edges together are a **graph**.
- The cell that makes the graph lists its nodes: 12. They are 4 datasets (`daily_sales`,
  `clean_customers`, `clean_orders`, `products.csv`), 2 columns, the dashboard, 2 people and 3
  teams.
- `orders.jsonl` and `customers.jsonl` are not nodes: no line describes them.
- The next cell lists the edges: 9, of three kinds: 5 `responsible`, 2 `of`, 2 `team`.
- The cell after it draws the graph. Each part of the graph that edges join is drawn on its own:
  there are 3 parts. Each arrow points from a line's entity to the entity its value names: a column
  to its dataset, an asset to the person or team responsible, a person to a team.
- The 3 parts: `daily_sales`, its 2 columns and `sales_dashboard`, joined through `j.marsh` and
  `finance`; `clean_customers` and `clean_orders`, joined through `data_engineering`;
  `products.csv`, `s.lund` and `catalogue`.

Following edges:

- A **traversal** starts at one node and follows the edges of the kinds it is given, each in the
  direction it is given: `"out"` follows an edge the way its arrow points, `"in"` against it, and
  `"both"` either way. It lists every node it reaches, the number of edges it walked to reach it,
  and the path it took.
- The first traversal cell starts at `daily_sales` and follows `responsible` and `team` the way
  their arrows point. Before you read on, you write what it will reach.
- It reaches `j.marsh` in 1 step and `finance` in 2: who is responsible for `daily_sales`, and that
  person's team.
- A traversal given no kinds follows every edge both ways. Before you read on, you write which
  nodes `graph.traverse("daily_sales")` will reach, and why each.
- It reaches 5 nodes: `j.marsh`, the 2 columns, `sales_dashboard` and `finance`.
- The path to `sales_dashboard` is `daily_sales -responsible-> j.marsh <-responsible-
  sales_dashboard`. The traversal reached the dashboard because Jo Marsh is responsible for both,
  not because the dashboard reads `daily_sales`. The dashboard does read `daily_sales`, but no line
  records that.
- The next cell starts at `clean_customers` and follows every edge both ways. It reaches
  `data_engineering`, then `clean_orders`, through the team responsible for both. `clean_orders`
  is not made from `clean_customers` (Chapter 2's rules: it is made from `orders.jsonl`).
- Following every edge returns what shares an owner with the start. A reader asking for
  "everything related" could take that for what is made from it. Which nodes come back depends on
  which kinds of edge are followed, and which way.

The requirement:

- Jo's request as a requirement: "Show everything related to `daily_sales`."
- You commit first: write in a cell what you would send Jo, and what "related" means to you.
- It could mean four things, each a different kind of edge:
  - what `daily_sales` is made from: an edge between datasets, through whatever makes it;
  - what reads `daily_sales`: the same kind of edge, the other way;
  - who is responsible for it: the `responsible` edge;
  - where it is kept: the warehouse as an entity, with an edge to it; the warehouse is not an
    entity in these records.
- The graph has edges of three kinds: `responsible`, `team` and `of`. It answers "who is
  responsible" (and that person's team, and the dataset's columns). No edge says what
  `daily_sales` is made from or what reads it, and none says where it is kept.
- Following every edge answers none of the four readings: it mixes owners, teams and columns.

The close:

- Showed: records become a graph when a value names another entity; a traversal answers a question
  only when it follows the edges the question means; every edge, both ways, returned assets that
  share an owner.
- Could not show: what `daily_sales` is made from or what reads it: no line records either.
- Next: Chapter 6 gives the reader the jobs' code and records what each job reads and writes, so
  that the graph holds what is made from what. (Do not name what Chapter 6 calls it.)

The note "### How this differs from a real platform":

- The shop, its people and its data are invented for the course. The notation, the model and the
  traversals are the course's own; the graph is made from the records each time the cell runs.

## Slots

A. **objectives**: four items, each starting with a verb, using none of the four new terms: turn the
records into connections between the things they describe; predict where following some
connections leads, then check; find what following every connection returns, and why; question the
requirement "Show everything related to `daily_sales`."

B. **opening**: the section "## Jo Marsh's question": Jo's reply and the request, quoted.

C. **records_lead**: one or two sentences before the records cell: what it holds, and the two new
lines.

NOTE_OF. **note_of**: the `#` note above the two new lines inside the cell: a short phrase, under 60
characters, no backticks.

D. **model_lead**: one sentence before the model cell: the line it adds.

E. **graph**: the section "## The records as a graph": node, edge, graph (in that order), then that
the next cell lists the nodes, with the count and what they are, and which assets are missing and
why.

F. **edges**: one or two sentences before the edges cell, or after it: 9 edges, of three kinds, with
the counts.

G. **drawing_lead**: before the drawing cell: what it draws, the 3 parts, and the direction of the
arrows.

ALT. **alt**: the drawing's text for a reader who cannot see it: one sentence naming the 3 parts.

H. **traversal**: the section "## Following edges": traversal, the three directions, what it lists;
then the first traversal (what it starts at and follows), and what to write before you read on.

I. **traversal_cell**: the text inside the expectation cell, between triple quotes: a question
asking which nodes the traversal will reach, then `........`. At most about 60 characters a line.
Plain text.

J. **traversal_after**: its result; then that a traversal given no kinds follows every edge both
ways, and what to write before you read on.

K. **everything_cell**: the text inside that cell: a question asking which nodes it will reach, and
why each, then `........`. At most about 60 characters a line.

L. **everything_after**: the 5 nodes; the path to `sales_dashboard` and what it means; one sentence
before the next cell, which starts at `clean_customers`.

M. **shared_owner**: after that cell: what it reached and through what; why `clean_orders` is not
made from `clean_customers`; what following every edge returns, and that the result depends on the
kinds and directions followed.

N. **requirement_lead**: the section `## "Show everything related to daily_sales."` (with
`daily_sales` in backticks in the heading): the requirement, and what to write in the next cell
first.

O. **requirement_cell**: the text inside that cell: what you would send Jo, then `........`; what
"related" means to you, then `........`. At most about 60 characters a line.

P. **readings**: the four readings as a Markdown list, each with the edge it needs; then which the
graph holds, and that following every edge answers none of them.

Q. **close**: the section "## Before Chapter 6": what the experiments showed and could not show; one
paragraph on Chapter 6; then two or three reflective questions as a Markdown list, the first about
a platform the reader works on, none with its answer.

R. **reality**: the note "### How this differs from a real platform".

Write the slots under `## A` to `## R` (and `## NOTE_OF`, `## ALT`), each the exact text to place.
