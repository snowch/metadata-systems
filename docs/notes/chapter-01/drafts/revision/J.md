## title

The shop changed three ways

## changeLead

The experiment runs your query from the construction section again, so it starts once your query passes its tests.

Each change alters the shop before the week begins. The lab runs the whole week again from Monday, with that change in place.

Before a change runs, you predict how many queries in the builder's choices will rebuild `daily_sales` afterwards. After it runs, the figure shows those queries, what storage holds on Monday morning, and your query's rows against the new `daily_sales`.

## changeQuestion

How many queries in the builder's choices will rebuild `daily_sales` after this change?

## changeOptions

- none: none
- one: one
- twoOrMore: two or more

## outcomeCopy

A new file appears in storage: `clean_orders_copy.parquet`, in the bucket `shop-scratch`, last modified at 02:15, with the same 44 rows as `clean_orders`.

Now 2 queries rebuild `daily_sales`: the same query over `clean_orders` and over the copy.

The data cannot say which of the two `daily_sales` was built from. Both fit equally well.

Storage shows the new file. Nothing says who made it or why.

## outcomeRefunds

From Saturday's row on, the program that writes `daily_sales` keeps every order whose status is not "refunded", where before it kept completed orders only.

The shop has no refunds: every order is completed or cancelled.

Saturday's row now reads 215.49, because Saturday's cancelled order counts. The dashboard shows the same. In the week as it first ran it read 191.49.

Sunday's row is unchanged, 97.75, because Sunday had no cancelled order.

Storage shows nothing else different: the same 7 rows and the same last-written time.

None of the builder's choices rebuilds `daily_sales` any more. A query with a condition on the date would, and the builder offers none.

Nothing says whether Saturday's figure is a mistake or a decision.

## outcomeFailed

On the last night, the program that writes `daily_sales` fails and writes nothing.

`daily_sales` has 6 rows, with no row for Sunday. It was last altered on Sunday 13 September at 02:30, a day before `clean_orders` (Monday at 02:05) and the dashboard (Monday at 03:00).

The dashboard refreshed on Monday at 03:00 as on every morning, and shows 6 values. Its own record shows that Monday-morning refresh, so it looks up to date.

Storage shows that `daily_sales` is a day behind. It does not show that a write was due on Monday, or that one failed.

Your query still rebuilds `daily_sales`: it gives the 6 rows `daily_sales` has, and a seventh, for Sunday, that `daily_sales` lacks.

## afterAll

The data suggested where `daily_sales` comes from, and each of the three changes altered that evidence.

The copy made it ambiguous: two assets fit equally well.

The edit left none of the builder's choices that fits.

The failed night left the dashboard looking up to date over a table a day behind.

Storage kept some traces: the copy left a new file, and the failed night a stale time.

None of the changes left a record of the change itself: what changed, who changed it, or why.

## changeLegend

change

## firstWeek

the week as it first ran

## firstWeekStatus

This is the week as it first ran, the one you have been reading.

## runWithChange

Run with this change

## ranWith

The lab ran the whole week again with this change: {change}.

## locked

This figure starts once your answer to the challenge called "{title}" passes its tests.

## storageNowHeading

What storage holds on Monday morning

## compareNote

Storage holds only this week's values. Each comparison with the week as it first ran is the lab's, because it ran both weeks.

## newAsset

A new file, `{asset}`, at `{location}`, last modified at `{time}`.

## changedTime

`{asset}` was last written at `{after}`; in the week as it first ran, at `{before}`.

## changedRows

`{asset}` has `{after}` rows; in the week as it first ran, `{before}`.

## changedValue

In `{asset}`, the row for `{day}` reads `{after}`; in the week as it first ran, `{before}`.

## noDiff

Storage holds the same as in the week as it first ran.

## yourQueryHeading

Your query against this week's daily_sales

## fitsHeading

The queries in the builder's choices that rebuild daily_sales

## fitsNone

None of the builder's choices rebuilds it.

## caption

Choose a change to the shop, predict how many queries will rebuild `daily_sales` afterwards, run the week again with it, and read what storage holds.
