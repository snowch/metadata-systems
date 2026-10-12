# Brief HA: Chapter 5, "Metadata as a graph", after its review

Read `docs/notes/chapter-05/briefs/common.md` first: its rules hold here. Also read `docs/style.md`.

The chapter turns the reader's records into a graph and follows its edges. A review found that the
opening did not say what Jo Marsh wants the answer for, that the records were not quite Chapter 4's,
that the reader never chose a traversal's direction, and that the conclusions said more than the
results showed. These slots replace the chapter's prose in those places.

Terms. Before the slot E, the chapter has introduced **node**, **edge** and **graph**, and slot E
introduces **traversal** (in bold, once). Slots A to D must not use node, edge, graph or traversal:
say "connections" or "following them" there. Words you must not use anywhere: lineage, upstream,
downstream, run (as a noun), event, lab, engine, Jupyter, owner (say "responsible"), "made from"
about `daily_sales` (Chapter 2 showed that a query fitting the data does not show how a table was
made; say "the orders Jo asks about" instead).

## Facts (each checked against the shop's data)

The opening (slot B), under the heading `## Jo Marsh's question`:

- Jo Marsh, in finance, wants daily revenue to count orders that have no customer id. Jo's meaning
  of a day's revenue says so (Chapter 3).
- Chapter 2 found that `clean_orders` leaves out orders with no customer id.
- Jo asks you, before asking for any change: "Show me everything related to `daily_sales`." Quote
  it as a Markdown quotation (a line starting `> `).
- Jo wants two things from the answer: where those orders are lost, and what a change would touch.
  Say this as Jo's purpose, in one sentence, after the quotation.

The records (slot C, a paragraph above the records cell; slot NOTE, a `#` note inside the cell):

- The records cell holds Chapter 4's records after both of Chapter 4's changes: the two spellings
  merged into `j.marsh` and `s.lund`, and the data engineer a team, `data_engineering`, as Chapter
  4's last cell made it by default.
- Chapter 4's merge left the line `dataset daily_sales responsible: j.marsh` twice. The cell keeps
  it once.
- The cell keeps the line `dataset clean_orders drops: orders with no customer id`: the model
  accepts it as text, which was one of Chapter 4's two choices.
- Two new lines, under a `#` note, say which dataset each column of `daily_sales` belongs to, with
  the attribute `of`.
- Slot NOTE is the `#` note at the top of the cell: under about 60 characters, saying these are
  Chapter 4's records after both changes. Plain text, no backticks.

The model (slot D, above the model cell):

- The model cell has Chapter 4's lines, with `dataset drops: text`, and one new line,
  `column of: dataset`: the value of `of` on a column must name a dataset.

Following edges (slot E, under the heading `## Following edges`):

- Walking from one node along its edges, from node to node, is a **traversal**.
- You choose which kinds of edge it follows, and the direction for each, in braces: for example
  `{"responsible": "in"}` follows `responsible` edges against their arrows.
- `"out"` follows an edge the way its arrow points, `"in"` against it, and `"both"` either way.
- A traversal lists every node it reaches, the number of edges it walked to reach it (`steps`), and
  its `path`. In a path, `-responsible->` is an edge followed the way its arrow points, and
  `<-responsible-` one followed against it.
- The first traversal asks which assets Jo Marsh is responsible for. It starts at `j.marsh` and
  follows `responsible` edges `"in"`.
- Before you read on, write in the next cell which nodes it will reach, and which it would reach
  with `"out"` in place of `"in"`.

Slot F, the text inside that cell (between triple quotes): two questions, each followed on its own
line by `........`: which nodes the traversal will reach; which it will reach with "out" in place of
"in". At most about 60 characters a line. Plain text.

After the first traversal (slot G):

- It reaches `daily_sales` and `sales_dashboard`, each by 1 edge, each against a `responsible`
  arrow.
- Change `"in"` to `"out"` in the cell above, select that cell and press **Run below**. Compare what
  it lists with what you wrote.

Slot H, a separate paragraph after slot G:

- With `"out"`, the traversal reaches no node, and the cell shows "No rows." Every `responsible`
  edge points to `j.marsh`; none leaves it.
- Change `"out"` back to `"in"` and press **Run below** again.
- A traversal given no kinds of edge follows every edge, both ways.
- Before you read on, write in the next cell which nodes `graph.traverse("daily_sales")` will
  reach, and whether it will reach `clean_orders`, whose `drops` line holds the rule behind the
  orders Jo asks about.

Slot I, the text inside that cell: two questions, each followed on its own line by `........`:
which nodes `graph.traverse("daily_sales")` will reach; whether it will reach `clean_orders`. At
most about 60 characters a line. Plain text.

After the traversal from `daily_sales` (slot J):

- Read the `path` of `sales_dashboard` in the table above:
  `daily_sales -responsible-> j.marsh <-responsible- sales_dashboard`.
- The traversal reaches the dashboard because Jo Marsh is responsible for both, not because the
  dashboard reads `daily_sales`. The dashboard does read `daily_sales`, but no line records that.
- The traversal does not reach `clean_orders`. The `drops` line is text, so it is no edge, and no
  edge joins `clean_orders` to any node the traversal reaches.
- The next cell starts at `clean_customers` and follows every edge both ways.

After the traversal from `clean_customers` (slot K):

- It reaches `data_engineering` by 1 edge, then `clean_orders` by 2, through the team responsible
  for both.
- `clean_orders` is not made from `clean_customers`: Chapter 2's rules say it is made from
  `orders.jsonl`.
- Following every edge reaches whatever the lines join to the start: its columns, who is
  responsible for it and their team, and anything else they are responsible for.
- From `clean_customers`, it reached a dataset that is not made from it. From `daily_sales`, it
  missed `clean_orders`, which holds the rule Jo asks about.

The readings (slot L, a block after the cell where the reader wrote what they would send Jo and what
"related" means to them):

- "Related" could mean four things, each needing its own lines:
  - what `daily_sales` is made from: a line that says what makes it, followed back towards the
    files;
  - what reads `daily_sales`: the same kind of line, followed the other way;
  - who is responsible for it: the `responsible` edge, and that person's `team`;
  - where it is kept: the warehouse as an entity, with an edge from `daily_sales` to it. The
    warehouse is not an entity in these records.
- The graph holds the third reading only. No line says what `daily_sales` is made from, or what
  reads it, and none says where it is kept.
- Jo's purpose, where the orders are lost and what a change would touch, is the first two readings.
- As written, the request is met by a list of what a traversal along every edge reaches. As Jo
  meant it, no traversal of these records can meet it, because no line records what is made from
  what.
- What you can send Jo: who is responsible for `daily_sales` and the dashboard; the `drops` line on
  `clean_orders`; and that the records do not say what `daily_sales` is made from or what reads it.

Write slot L as one Markdown list of the four readings, then short paragraphs.

The close (slot M), under the heading `## Before Chapter 6`:

- Showed: a line whose value names another entity becomes an edge, and the records form a graph. A
  traversal's answer depends on the kinds of edge it follows and their directions: changing `"in"`
  to `"out"` took the traversal from `j.marsh` from 2 nodes to none. Following every edge reached the
  dashboard through Jo Marsh, reached `clean_orders` from `clean_customers` through a team, and
  missed `clean_orders` from `daily_sales`.
- Could not show: what `daily_sales` is made from, and what reads it, because no line records
  either.
- Next: in Chapter 6 you read the jobs' code, and lines record what each job reads and writes, so
  that the graph holds what is made from what.
- Then these three reflective questions as a Markdown list, none with its answer:
  - Take a platform you work on. Which of its records name another entity, such as a person, a
    table or a team?
  - Pick a question you ask about one asset on that platform. Which edges would a traversal have to
    follow to answer it, and in which direction?
  - What would a record have to say for a graph to show that one dataset is made from another?

The note (slot N), under the heading `### How this differs from a real platform`:

- The shop, its people and its data are invented for the course. The notation, the model and the
  traversals are the course's own. The graph is made from the records each time the cell runs.
- The shop's records are 20 lines. On a platform with thousands of assets and
  people, joined by `responsible` and `team` edges, a traversal along every edge reaches far more
  nodes, most of them unrelated to the question.

## Slots

A. **objectives**: four objectives as a Markdown list (no heading; it sits under **Objectives**):
turn the records into connections between the things they describe; choose which connections to
follow and in which direction, predict where they lead, then change one and check; find what
following every connection returns, and what it misses; question the requirement "Show everything
related to `daily_sales`."

B. **opening**: the heading `## Jo Marsh's question` and the opening.

C. **records_lead**. NOTE. **records_note**. D. **model_lead**. E. **traversal_lead**.
F. **first_cell**. G. **first_after**. H. **first_out**. I. **every_cell**. J. **every_after**.
K. **clean_after**. L. **readings**. M. **close**. N. **reality**.

Write the file `docs/notes/chapter-05/drafts/HA.md` with the slots under `## A`, `## B`, `## C`,
`## NOTE`, `## D` and on to `## N`, each the exact text to place, and nothing else in the file.
