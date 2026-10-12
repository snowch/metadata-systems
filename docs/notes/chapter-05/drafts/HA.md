## A

- Turn the records into connections between the things they describe.
- Choose which connections to follow and in which direction, predict where they lead, then change one and check.
- Find what following every connection returns, and what it misses.
- Question the requirement "Show everything related to `daily_sales`."

## B

## Jo Marsh's question

Jo Marsh, in finance, wants daily revenue to count orders that have no customer id. Jo's meaning of a day's revenue says so (Chapter 3). Chapter 2 found that `clean_orders` leaves out orders with no customer id.

Jo asks you, before asking for any change:

> Show me everything related to `daily_sales`.

Jo wants two things from the answer: where those orders are lost, and what a change would touch.

## C

The records below are Chapter 4's records after both of its changes. The two spellings are merged into `j.marsh` and `s.lund`. Chapter 4's last cell made the data engineer a team, `data_engineering`, by default. Chapter 4's merge left the line `dataset daily_sales responsible: j.marsh` twice. The cell keeps it once. The cell keeps the line `dataset clean_orders drops: orders with no customer id`. The model accepts it as text, which was one of Chapter 4's two choices. Two new lines, under a `#` note, say which dataset each column of `daily_sales` belongs to, with the attribute `of`.

## NOTE

These are Chapter 4's records after both changes.

## D

The model cell has Chapter 4's lines, with `dataset drops: text`, and one new line, `column of: dataset`. The value of `of` on a column must name a dataset.

## E

## Following edges

Walking from one node along its edges, from node to node, is a **traversal**.

You choose which kinds of edge it follows, and the direction for each, in braces. For example, `{"responsible": "in"}` follows `responsible` edges against their arrows.

`"out"` follows an edge the way its arrow points, `"in"` against it, and `"both"` either way.

A traversal lists every node it reaches, the number of edges it walked to reach it (`steps`), and its `path`. In a path, `-responsible->` is an edge followed the way its arrow points, and `<-responsible-` one followed against it.

The first traversal finds which assets Jo Marsh is responsible for. It starts at `j.marsh` and follows `responsible` edges `"in"`.

Before you read on, write in the next cell which nodes it will reach, and which it would reach with `"out"` in place of `"in"`.

## F

Which nodes will the traversal reach?
........
Which nodes will it reach with "out" in place of "in"?
........

## G

The traversal reaches `daily_sales` and `sales_dashboard`, each by 1 edge and each against a `responsible` arrow.

Change `"in"` to `"out"` in the cell above, select that cell and press **Run below**. Compare what it lists with what you wrote.

## H

With `"out"`, the traversal reaches no node, and the cell shows "No rows." Every `responsible` edge at `j.marsh` points to it, so none leaves it.

Change `"out"` back to `"in"` and press **Run below** again.

A traversal given no kinds of edge follows every edge, both ways.

Before you read on, write in the next cell which nodes `graph.traverse("daily_sales")` will reach, and whether it will reach `clean_orders`, whose `drops` line holds the rule behind the orders Jo asks about.

## I

Which nodes will graph.traverse("daily_sales") reach?
........
Will it reach clean_orders?
........

## J

Read the `path` of `sales_dashboard` in the table above: `daily_sales -responsible-> j.marsh <-responsible- sales_dashboard`.

The traversal reaches the dashboard because Jo Marsh is responsible for both, not because the dashboard reads `daily_sales`. The dashboard does read `daily_sales`, but no line records that.

The traversal does not reach `clean_orders`. The `drops` line is text, so it is no edge, and no edge joins `clean_orders` to any node the traversal reaches.

The next cell starts at `clean_customers` and follows every edge both ways.

## K

It reaches `data_engineering` by 1 edge, then `clean_orders` by 2, through the team responsible for both.

`clean_orders` is not made from `clean_customers`: Chapter 2's rules say it is made from `orders.jsonl`.

Following every edge reaches whatever the lines join to the start: its columns, who is responsible for it and their team, and anything else they are responsible for.

From `clean_customers`, it reached a dataset that is not made from it. From `daily_sales`, it missed `clean_orders`, which holds the rule Jo asks about.

## L

Set what you wrote in the cell above beside four readings of "related":

- What `daily_sales` takes its data from: a line that says what produces it, followed back towards the files;
- What reads `daily_sales`: the same kind of line, followed the other way;
- Who is responsible for it: the `responsible` edge, and that person's `team`;
- Where it is kept: the warehouse as an entity, with an edge from `daily_sales` to it.

The records answer only the third reading. The warehouse is not an entity in these records, so no line gives the fourth. No line says what `daily_sales` takes its data from, or what reads it.

Jo's purpose, where the orders are lost and what a change would touch, needs the first two readings.

As written, the request is met by a list of what a traversal along every edge reaches. As Jo meant it, no traversal of these records can meet it, because no line records what is made from what.

What you can send Jo: who is responsible for `daily_sales` and the dashboard; the `drops` line on `clean_orders`; and that the records do not say what `daily_sales` takes its data from, or what reads it.

## M

## Before Chapter 6

A line whose value names another entity becomes an edge, and the records form a graph. A traversal's answer depends on the kinds of edge it follows and their directions. Changing `"in"` to `"out"` took the traversal from `j.marsh` from 2 nodes to none. Following every edge reached the dashboard through Jo Marsh, reached `clean_orders` from `clean_customers` through a team, and missed `clean_orders` from `daily_sales`.

The records could not show what `daily_sales` takes its data from, or what reads it, because no line records either.

In Chapter 6 you read the jobs' code. Lines record what each job reads and writes, so the graph can show what is made from what.

- Take a platform you work on. Which of its records name another entity, such as a person, a table or a team?
- Pick a question you ask about one asset on that platform. Which edges would a traversal have to follow to answer it, and in which direction?
- What would a record have to say for a graph to show that one dataset is made from another?

## N

### How this differs from a real platform

The shop, its people and its data are invented for the course. The notation, the model and the traversals are the course's own. The graph is made from the records each time the cell runs.

The shop's records are 20 lines. On a platform with thousands of assets and people, joined by `responsible` and `team` edges, a traversal along every edge reaches far more nodes, most of them unrelated to the question.
