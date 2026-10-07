## inspectorLead

Choose an asset from the list. The figure shows what storage records about it: its record, what storage says about eight questions, its columns and their types, and its rows. The figure asks every asset the same eight questions. Then try one of these:

- Find the rows of `orders.parquet` that make Thursday's total differ from `daily_sales`
- Compare `orders.parquet` with `clean_orders`
- Put the seven assets in the order they were last written, and say what that order suggests and what it cannot prove
- Open `daily_sales` and read what storage says about each question

## construction

Storage does not say where `daily_sales` comes from. The data might.

A query **rebuilds** an asset when it gives every row the asset has, with the same values.

Build one with the query builder below. It writes your choices as SQL and runs the query on Monday morning's data.

If your query rebuilds `daily_sales`, have you found out how `daily_sales` was made?

## changeLead

This experiment tests whether rebuilding `daily_sales` with a query shows how it was made.

It runs your query from the construction section again, so it starts once your query passes its tests.

Each change gives a different week: the lab runs the whole week again from Monday with that change.

Before a change runs, you predict what the data will then say about where `daily_sales` comes from: how many queries in the builder's choices will rebuild it. The builder's choices cover every asset in storage that week.

After it runs, the figure shows those queries, what storage holds on Monday morning, and your query's rows against the new `daily_sales`.

## changeQuestion

After this change, how many queries in the builder's choices will rebuild `daily_sales`?

## changeOptions

- none: none, so the data no longer points to any query
- one: one, so the data still points to a single query
- twoOrMore: two or more, so the data fits more than one query

## refundsLabel

the program that writes daily_sales is edited to keep orders that are not refunded, from Saturday's row on

## afterAll

Rebuilding `daily_sales` suggested how it was made, but did not show it. Each of the three changes altered that evidence.

The copy made it ambiguous: two assets fit equally well. The edit left none of the builder's choices that fits. The failed night left the dashboard looking up to date over a table a day behind. Storage kept some traces: the copy left a new file, and the failed night a stale time. None of the changes left a record of the change itself: what changed, who changed it, or why.
