## titles.failureExperiment

Three changes storage does not record

## changeCaption

Choose a change to the shop, run the week again, and compare what storage shows.

## changeLead

Each change alters the shop before the week begins. The figure will run the whole week again from Monday, with that change in place.

Before you run each change, make a prediction. Will storage show the change? Will your query still rebuild `daily_sales`?

## changeLabels

- copy: an analyst copies `clean_orders` every night
- refunds: the program that writes `daily_sales` is edited for refunds
- failed: the last night's write of `daily_sales` fails

## outcomeCopy

A new file appears in storage: `clean_orders_copy.parquet` in bucket `shop-scratch`, last modified at 02:15, with the same 44 rows as `clean_orders`. Now two queries rebuild `daily_sales`: from `clean_orders` and from the copy. The data cannot say which one was used. Both fit equally well.

## outcomeRefunds

From Saturday's row on, the program keeps every order whose status is not "refunded", not completed orders. Saturday's row now reads 215.49, not 191.49, because its cancelled order counts. Sunday's row is unchanged at 97.75, because Sunday had no cancelled order. Storage shows nothing else different. No query in the builder's choices rebuilds `daily_sales` any more.

## outcomeFailed

The program fails on the last night and writes nothing. `daily_sales` has 6 rows, with no row for Sunday, and was last altered on Sunday 13 September at 02:30. The dashboard refreshed on Monday at 03:00 as usual and shows 6 values. From storage, a failed night looks like a night with nothing to write. Your query still rebuilds every row `daily_sales` has, and gives one more: Sunday.

## afterAll

The data suggested where `daily_sales` comes from. A copy made the answer ambiguous, an edit made it impossible, and a failure made a missing row look like a quiet night. None of the three changes left anything in storage that says what happened.
