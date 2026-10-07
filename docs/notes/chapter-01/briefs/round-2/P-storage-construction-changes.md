# Brief P: Sections 4, 5 and 6, where the reconstruction becomes the question

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-2/P.md`.

The central question of the chapter is this: if a query rebuilds an asset, has it shown how the
asset was made? Section 5 asks it and does not answer it. Section 6's experiment answers it.

## inspectorLead

Shown above the storage inspector. It replaces the old text, which said: "Choose an asset from
the list. The figure shows what storage records about it: its record, what storage says about
eight questions, its columns and their types, and its rows. The figure asks every asset the same
eight questions. Then try one of these: pick one of the days whose totals differed in the
prediction, and find the rows of `orders.parquet` that make the difference; compare
`orders.parquet` with `clean_orders`; put the seven assets in the order they were last written,
and say what that order suggests and what it cannot prove; open `daily_sales` and read what
storage says about each question." Keep all of it but the first task, which changes. Facts for
the first task:

- Find the rows of `orders.parquet` that make Thursday's total differ from `daily_sales`.

Keep the tasks as a Markdown list.

## construction

Section 5's prose, above the query builder. It replaces: "Storage does not say where
`daily_sales` comes from. The data might. A query **rebuilds** an asset when it gives every row
the asset has, with the same values. A query that rebuilds `daily_sales` is a candidate for how it
was made, not proof. Build one with the query builder below. It writes your choices as SQL and
runs the query on Monday morning's data." Facts, in this order:

- Storage does not say where `daily_sales` comes from. The data might.
- Define the word: a query **rebuilds** an asset when it gives every row the asset has, with the
  same values. Keep "rebuilds" in bold.
- Build one with the query builder below. It writes your choices as SQL and runs the query on
  Monday morning's data.
- End by asking the question, and do not answer it: if your query rebuilds `daily_sales`, have you
  found out how `daily_sales` was made?

## changeLead

Shown above the failure experiment's figure, before anything runs. It replaces the old text.
Facts, in this order:

- Your query rebuilds `daily_sales`. This experiment tests whether that shows how `daily_sales`
  was made.
- It runs your query from the construction section again, so it starts once your query passes its
  tests.
- Each change gives a different week: the lab runs the whole week again from Monday with that
  change.
- Before a change runs, you predict what the data will then say about where `daily_sales` comes
  from: how many queries in the builder's choices will rebuild it. The builder's choices cover
  every asset in storage that week.
- After it runs, the figure shows those queries, what storage holds on Monday morning, and your
  query's rows against the new `daily_sales`.

Say nothing about what any change does to storage or to the queries.

## changeQuestion

The prediction's prompt, shown before the learner commits, once per change. One sentence. Facts:
after this change, how many queries in the builder's choices will rebuild `daily_sales`?

## changeOptions

Three option labels, each saying what the data would then say about where `daily_sales` comes
from, parallel in form and length. Begin each with its count, as written here:

- none: none, so the data no longer points to any query;
- one: one, so the data still points to a single query;
- twoOrMore: two or more, so the data fits more than one query.

## refundsLabel

The label of one of the three changes, shown before it runs, plain text, no full stop. It
replaces "the program that writes daily_sales is edited for refunds", which did not say what the
edit does, so nobody could reason about it. Facts:

- The program that writes daily_sales is edited.
- From Saturday's row on, it keeps every order that is not refunded.
- Do not say when the edit was made, and do not say what the program kept before: the learner's
  own query tells them that.

## afterAll

Shown once all three changes have run. It replaces the old text's first sentence, "The data
suggested where `daily_sales` comes from, and each of the three changes altered that evidence."
and keeps the rest. Facts for the new start:

- It answers the construction's question: rebuilding `daily_sales` suggested how it was made, but
  did not show it.
- Each of the three changes altered that evidence.

The rest stays as it was: "The copy made it ambiguous: two assets fit equally well. The edit left
none of the builder's choices that fits. The failed night left the dashboard looking up to date
over a table a day behind. Storage kept some traces: the copy left a new file, and the failed
night a stale time. None of the changes left a record of the change itself: what changed, who
changed it, or why."
