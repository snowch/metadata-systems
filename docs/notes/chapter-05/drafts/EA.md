## A

- Turn the records into connections between the things they describe.
- Predict where following some connections leads, then check.
- Find what following every connection returns, and why.
- Question the requirement "Show everything related to `daily_sales`."

## B

## Jo Marsh's question

Jo Marsh, in finance, replies to the list of owners you sent at the end of Chapter 4. Jo wants daily revenue to count orders that have no customer id. Jo's meaning of a day's revenue already says so (Chapter 3). Before anything changes, Jo asks:

> Show me everything related to `daily_sales`.

## C

The records cell holds the records as Chapter 4 left them, with the two spellings merged into `j.marsh` and `s.lund`, and the data engineer as a team with the identifier `data_engineering`. Two new lines, under a `#` note, say which dataset each column of `daily_sales` belongs to, with the attribute `of`.

## NOTE_OF

Which dataset each column belongs to

## D

The model cell adds one line, `column of: dataset`, so that the value of `of` on a column must name a dataset.

## E

## The records as a graph

Each entity the records describe becomes a **node**, named by its identifier.

Each line whose value is the identifier of another entity becomes an **edge**. The edge goes from the line's entity to the entity its value names, and it carries the line's attribute as its label. For example, `dataset daily_sales responsible: j.marsh` is the edge from `daily_sales` to `j.marsh`, labelled `responsible`. A line whose value is text, such as a `means` line, is no edge.

Nodes and edges together are a **graph**.

The next cell lists the nodes. There are 12: 4 datasets (`daily_sales`, `clean_customers`, `clean_orders`, `products.csv`), 2 columns, the dashboard, 2 people and 3 teams. `orders.jsonl` and `customers.jsonl` are not nodes, because no line describes them.

## F

The next cell lists the edges. There are 9, of three kinds: 5 `responsible`, 2 `of` and 2 `team`.

## G

The next cell draws the graph. It draws each part of the graph that edges join on its own. There are 3 parts. Each arrow points from a line's entity to the entity its value names: from a column to its dataset, from an asset to the person or team responsible, and from a person to a team.

## ALT

The drawing has 3 parts: `daily_sales`, its 2 columns and `sales_dashboard`, joined through `j.marsh` and `finance`; `clean_customers` and `clean_orders`, joined through `data_engineering`; and `products.csv`, `s.lund` and `catalogue`.

## H

## Following edges

Walking from one node along its edges, from node to node, is a **traversal**. You choose which kinds of edge it follows, and the direction for each. `"out"` follows an edge the way its arrow points, `"in"` against it, and `"both"` either way. A traversal lists every node it reaches, the number of edges it walked to reach each one, and the path it took.

The first traversal starts at `daily_sales`. It follows `responsible` and `team` edges, each the way its arrow points. Before you read on, write in the next cell which nodes it will reach.

## I

"""
Which nodes will this traversal reach?
........
"""

## J

The traversal reaches `j.marsh` by 1 edge and `finance` by 2 edges. `j.marsh` is who is responsible for `daily_sales`, and `finance` is that person's team.

A traversal given no kinds follows every edge both ways. Before you read on, write in the next cell which nodes `graph.traverse("daily_sales")` will reach, and why each.

## K

"""
Which nodes will graph.traverse("daily_sales")
reach, and why is each one reached?
........
"""

## L

The traversal reaches 5 nodes: `j.marsh`, the 2 columns, `sales_dashboard` and `finance`.

The path to `sales_dashboard` is `daily_sales -responsible-> j.marsh <-responsible- sales_dashboard`. The traversal reaches the dashboard because Jo Marsh is responsible for both, not because the dashboard reads `daily_sales`. The dashboard does read `daily_sales`, but no line records that.

The next cell starts at `clean_customers` and follows every edge both ways.

## M

The cell reaches `data_engineering`, then `clean_orders`, which it reaches through the team responsible for both. `clean_orders` is not made from `clean_customers`: Chapter 2's rules say it is made from `orders.jsonl`.

Following every edge returns what shares an owner with the start, here `clean_customers`. A reader asking for everything related could take that result for what `clean_customers` is made from. Which nodes come back depends on the kinds of edge followed, and on the direction each is followed in.

## N

## "Show everything related to `daily_sales`."

Jo Marsh's request is a requirement, and it does not say what "related" means. Before you read on, write in the next cell what you would send Jo Marsh, and what "related" means to you.

## O

"""
What would you send Jo Marsh?
........
What does "related" mean to you?
........
"""

## P

It could mean four things. Each needs a different kind of edge:

- what `daily_sales` is made from: an edge between datasets, from `daily_sales` to whatever makes it;
- what reads `daily_sales`: the same kind of edge, the other way;
- who is responsible for it: the `responsible` edge;
- where it is kept: the warehouse as an entity, with an edge from `daily_sales` to it. The warehouse is not an entity in these records.

The graph holds the third reading, who is responsible. Its `responsible` edges say who is responsible for a dataset, and its `team` and `of` edges add that person's team and the dataset's columns. No edge says what `daily_sales` is made from or what reads it, and none says where it is kept. Following every edge answers none of the four readings, because it mixes owners, teams and columns.

## Q

## Before Chapter 6

A line whose value names another entity becomes an edge, and the records then form a graph. A traversal answers a question only when it follows the edges that the question means. Following every edge, both ways, returned the assets that share an owner with the start. What `daily_sales` is made from, and what reads it, cannot be read from the graph, because no line records either.

Chapter 6 gives you the jobs' code and records what each job reads and writes, so that the graph holds what is made from what.

- Take a platform you work on. Which of its records name another entity, such as an owner, a table or a team?
- Pick a question you ask about one asset on that platform. Which edges would a traversal have to follow to answer it, and in which direction?
- What would a record have to say for a graph to show that one dataset is made from another?

## R

### How this differs from a real platform

The shop, its people and its data are invented for the course. The notation, the model and the traversals are the course's own. The graph is made from the records each time the cell runs.
