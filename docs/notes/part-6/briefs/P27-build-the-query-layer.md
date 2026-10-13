# Brief P27: Chapter 27, Build the query layer

Read `common.md` in this folder first, and `docs/style.md`. Write
`docs/notes/part-6/drafts/P27.md`, with one `## key` heading per slot below, in this order. A
heading inside a slot that this brief gives as `## ...` must be written as `### ...`. The chapter
introduces no new term. Words from earlier chapters: *downstream*, *upstream*, *traversal* (Chapter
5), *freshness* (Chapter 13), *impact analysis* (Chapter 16).

## A

A list of four objectives:

- Write a traversal that finds everything downstream of an asset in the lineage graph.
- Read the shop's answers to the other questions over the same graph and the same week.
- Find an asset that is recent by when it was written and old by what it shows.
- Question the requirement "The query layer must answer who owns each asset."

## B

- The heading `## Questions over the graph`.
- Since Part III, the shop's pages have answered questions about its assets: what depends on an
  asset (Chapter 14), where it came from (Chapter 15), who owns it (Chapters 2, 4 and 21), how recent
  it is (Chapter 13), which runs failed (Chapter 13), and what a change to a column reaches (Chapter
  16). Here they are asked of the lineage graph Chapter 26 built, the shop's version.
- The week has the returns desk, the analyst's copy as `build_daily_sales`'s input from Sunday 13,
  and Chapter 13's failed night: early on Monday 14, `build_daily_sales` fails and writes nothing.
- `shop.query.next_assets(graph, asset)` gives the assets one step downstream: what each program that
  reads the asset writes. The next cell builds the graph and asks it for `orders.jsonl`.

## C

- One step downstream of `orders.jsonl` is `clean_orders`.
- The next cell holds `downstream(graph, asset)` as it stands: it gives one step. Change it so that
  it follows `next_assets` from each asset it finds, until no new asset turns up, as Chapter 5's
  traversal did. Select the cell and press **Run below**.
- The check below it asks for what is downstream of `orders.jsonl`, `clean_orders` and `returns`. As
  `downstream` stands, it gets 1 of 3 right: `returns`, which nothing reads.

## D

- With the traversal, all 3 are right. Downstream of `orders.jsonl` are `clean_orders`,
  `clean_orders_copy.csv`, `daily_sales` and `sales_dashboard`.
- Then this heading: `## The other questions`
- Monday's run of `build_daily_sales` failed, and `refresh_dashboard` ran after it and redrew the
  dashboard (Chapter 13).
- The shop's query for stale assets lists every asset last written more than 24 hours before 09:00
  on Monday 14.
- Before you read on, write in the next cell whether that query will list `sales_dashboard`.

## DD

Two lines: the question, then a line of eight full stops.

- The question: will the query list `sales_dashboard` as stale?

## E

- The next cell gives the shop's answers to four questions.
- `daily_sales` came from `clean_orders`, `clean_orders_copy.csv` and `orders.jsonl`.
- The stale assets are `daily_sales` and `returns`. `sales_dashboard` is not among them: it was last
  written at 03:00:09 on Monday 14, 6 hours before. Its latest day is Saturday 12, the same as
  `daily_sales`'s, because the dashboard was redrawn from a table that the failed run did not write.
- Compare this with what you wrote.
- The failed run is `build_daily_sales`'s, ended at 02:30:21 on Monday 14.
- A change to `clean_orders.customer_id` reaches `clean_orders_copy.csv.customer_id`.
- A query that asks when an asset was last written cannot see that the dashboard shows old data
  (Chapter 13).

## RH

- The heading `## Who owns it`.

## F

- Before you read on, write in the next cell what "who owns `daily_sales`" means to you here.

## FF

Two lines: the question, then a line of eight full stops.

- The question: what does "who owns daily_sales" mean here?

## G

- The shop holds three answers, each from its own source, and each answers a different question.
  The next cell lists them:
  - `account`: `etl_service`, the account the warehouse records as the table's owner (Chapter 2);
  - `responsible`: `j.marsh`, the person your records name (Chapter 4);
  - `team`: `data team`, from the team sheet (Chapter 21).
- You write `owner(asset)`. It must give an owner and say which meaning it holds: a dictionary with
  `owner` and `meaning`, where `meaning` is `account`, `responsible` or `team`. The cell after the
  list holds it as it stands: it gives the account's owner and no meaning, and the check below it
  fails.
- Change it to give one meaning's owner and that meaning's name. Select the cell and press
  **Run below**.

## H

- The check passes for any of the three meanings, as long as the owner given is that meaning's.
- The requirement as written is met by any of them. The question Chapter 2 started from, "who
  should I ask about `daily_sales`?", needs `responsible`, or a team that still exists.
- A query that names its meaning lets whoever reads the answer tell which question it answered.
- The requirement does not say which meaning it wants.

## Z

- The heading `## Before Chapter 28`.
- Summary facts, in order: a traversal over the graph found 4 assets downstream of `orders.jsonl`;
  the shop's query for stale assets listed `daily_sales` and `returns`, and not the dashboard, which
  was written on Monday and shows Saturday; the owner query passed only when it said which meaning
  it gave.
- Chapter 28 builds a page that shows what these queries find about one asset.
- Three questions, as a list: Which of your metadata system's answers say which question they
  answer? Which of your freshness checks look at when an asset was written, and which at what it
  holds? Which meaning of "owner" does your catalogue show?
- The heading `### How this differs from a real platform`, and two bullets:
  - The shop's queries run over a graph of 17 edges, held in memory. Chapter 23 projected what such
    questions read at 10,000,000 assets.
  - The 24 hours that make an asset stale are the shop's choice.
