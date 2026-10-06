# Brief B: investigation and construction

Attach: `common.md`, `../facts.md`, `docs/style.md`. Write to `docs/notes/chapter-01/drafts/B.md`.

## titles.investigation
A heading of three to six words: everything storage holds.

## inspectorCaption
One sentence: browse the seven assets and what storage records about each.

## inspectorLead
Shown above the figure. A short paragraph and a list of things to try. Facts:
1. Choose an asset from the list. The figure shows what its storage system records about it, its
   rows, and what storage says about eight questions.
2. Things to try, as a list of instructions (do not give their results):
   - In `orders.parquet`, find the rows whose `customer_id` is NULL, and their day.
   - Find an `order_id` that appears twice.
   - Find the orders whose `status` is cancelled.
   - Compare the number of rows in `orders.parquet` with the number in `clean_orders`.
   - Open `daily_sales` and read what storage says about each question.

## inspectorAfter
Shown below the figure from the start. Two or three sentences, giving no result of the list above.
Facts:
1. Storage recorded names, types, row counts, sizes, times and an owning account.
2. Nothing it recorded says which program wrote an asset, from what, or why some orders in
   `orders.parquet` are missing from `clean_orders`.

## titles.construction
A heading of three to six words: rebuilding `daily_sales` from the other assets.

## construction
Two short paragraphs. Facts:
1. Storage does not say where `daily_sales` comes from. The data might.
2. If a query over another asset gives exactly the rows of `daily_sales`, that query is a candidate
   for how it was made.
3. Build one with the query builder. It writes your choices as SQL and runs the query on Monday
   morning's storage.

## c1Title
A challenge title of three to six words: rebuild `daily_sales`.

## c1Task
The challenge's task, shown above the builder. Two to four sentences. Facts:
1. Choose an asset to read, which rows to keep, what to add up, and per what.
2. The tests compare your query's result with `daily_sales`, one test per day: your row for that
   day must equal its row.

## c1Fields
The builder's four field labels, one per line, each one to three words, in this order:
- source: which asset to read
- keep: which rows to keep
- measure: what to add up
- per: what to add up per

## c1Options
Option labels, one per line, as `field.value: label`, short lowercase phrases (the asset names
stay as they are and are not listed here):
- keep.all: every row
- keep.completed: completed orders only
- keep.cancelled: cancelled orders only
- measure.revenue: price times quantity
- measure.quantity: quantity
- measure.rows: the number of rows
- per.day: the day the order was placed
- per.customer: customer
- per.product: product

## c1Hints
Five hints, in this order, each one to three sentences. The ladder must not give the answer
before the fifth.
1. The concept: a query that rebuilds `daily_sales` must count exactly the orders it counts and
   add up the same number per day.
2. A common mistake: reading `orders.parquet`. The raw file has rows that revenue leaves out: an
   order written twice, orders with no customer id, cancelled orders.
3. A smaller example: from `orders.parquet`, Monday already matches, because Monday had none of
   those rows. Compare a day that does not match.
4. Part of the answer: read from `clean_orders`.
5. The whole answer: read from `clean_orders`, keep completed orders only, add up price times
   quantity, per the day the order was placed.

## c1Lead
Shown above the challenge, one or two sentences: your query appears below the choices as SQL, with
its result, before you run the tests.

## c1Caption
One sentence caption for the challenge.

## caseLabels
The seven test labels, one per line, in this form: Monday 7 September, Tuesday 8 September, and so
on to Sunday 13 September. (Write them exactly like that.)
