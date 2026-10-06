# Brief C: the failure experiment

Attach: `common.md`, `../facts.md`, `docs/style.md`. Write to `docs/notes/chapter-01/drafts/C.md`.

## titles.failureExperiment
A heading of three to six words: three changes storage does not record.

## changeCaption
One sentence: choose a change to the shop, run the week again, and compare what storage shows.

## changeLead
Shown above the figure from the start, so it must not say what any change does to storage or to
the query. Two short paragraphs. Facts:
1. Each change below alters the shop before its week. The figure runs the whole week again with
   the change, then shows what storage shows differently, your query's rows against the new
   `daily_sales`, and every query in the builder's choices that rebuilds it.
2. The figure uses your query from the construction section if it passes its tests, and the
   course's query if it does not.
3. Before you run each change, say what you expect: will storage show the change, and will your
   query still rebuild `daily_sales`?

## changeLabels
Three option labels, one per line, each a short phrase, in this order:
- copy: an analyst copies `clean_orders` every night
- refunds: the program that writes `daily_sales` is edited for refunds
- failed: the last night's write of `daily_sales` fails

## outcomeCopy
Shown only after the learner runs this change. Two to four sentences. Facts (fact sheet, change 1):
1. A new file appears in storage: `clean_orders_copy.parquet`, in a second bucket, `shop-scratch`,
   last modified at 02:15, with the same 44 rows as `clean_orders`.
2. Now two queries rebuild `daily_sales`: the same choices, from `clean_orders` and from the copy.
3. The data cannot say which one `daily_sales` was built from. Both fit equally well.

## outcomeRefunds
Shown only after the learner runs this change. Two to five sentences. Facts (fact sheet, change 2):
1. From Saturday's row on, the program keeps every order whose status is not "refunded". It used
   to keep completed orders. The shop has no refunds.
2. Saturday's row now reads 215.49, not 191.49: Saturday's cancelled order now counts.
3. Sunday's row is unchanged, 97.75, because Sunday had no cancelled order.
4. Storage shows nothing else different: the same 7 rows and the same last-written time.
5. No query in the builder's choices rebuilds `daily_sales` any more. Nothing says whether
   Saturday is a mistake or a decision.

## outcomeFailed
Shown only after the learner runs this change. Two to five sentences. Facts (fact sheet, change 3):
1. The program fails on the last night and writes nothing.
2. `daily_sales` has 6 rows, none for Sunday, and was last altered on Sunday 13 September at
   02:30.
3. The dashboard refreshed on Monday at 03:00 as usual and shows 6 values.
4. From storage, a failed night looks like a night with nothing to write.
5. Your query still rebuilds every row `daily_sales` has, and gives one more, for Sunday.

## afterAll
Shown only once all three changes have run. Two or three sentences. Facts:
1. The data suggested where `daily_sales` comes from, until a copy made the answer ambiguous, an
   edit made it impossible, and a failure made a missing row look like a quiet night.
2. None of the three changes left anything in storage that says what happened.
