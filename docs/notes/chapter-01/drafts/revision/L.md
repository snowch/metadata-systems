## c2Lead

`clean_orders` is made from `orders.parquet` by rules you cannot read. Recover them from the two files by choosing, for each kind of row that differs between them, whether the rules keep it. The tests compare the rows your rules keep with `clean_orders`. Your rules appear as SQL below the choices, with the number of rows they keep.

## c2Task

Choose four rules that turn `orders.parquet` into `clean_orders`. The tests check that your rules keep every row `clean_orders` has, and no row it lacks.

## c2Fields.duplicates

Orders that appear twice

## c2Options.duplicates

- keep: keep both rows
- one: keep one row

## c2Hints

- Compare `orders.parquet` with `clean_orders` row by row. Which rows are missing, and which appear fewer times?
- A common mistake: dropping cancelled orders. `clean_orders` keeps them; `daily_sales` leaves them out later.
- On Wednesday, order 7015 appears twice in `orders.parquet` and once in `clean_orders`.
- Keep one row of an order that appears twice. Drop orders with no customer id.
- Keep one row of an order that appears twice. Drop orders with no customer id. Keep cancelled orders. Either choice passes for the quantity rule.

## caption

Choose which orders the rules keep.

## p3Question

Your rules pass. How many settings of the four rules give `clean_orders` exactly, yours included?

## p3Options

- one: one, only yours
- two: two
- threeOrMore: three or more

## p3Explain

Two settings pass. They differ only in the rule for orders with a quantity of 0 or less. No order this week had a quantity of 0 or less, so either choice keeps the same rows. The shop's program drops such orders. This week's data cannot show that rule, however you rebuild it.

## p3Caption

Predict how many settings of the four rules pass.

## reflection

Back to Thursday. Three orders on Thursday have no customer id. They are in `orders.parquet` and not in `clean_orders`. Together they are worth 154.00, which makes up the difference between Thursday's raw total (205.50) and `daily_sales` (51.50).

Nothing you could read says whether leaving them out is a fault in the checkout or a rule somebody chose. The course comes back to Thursday later.

The four questions from the start each needed a record nobody kept:

- Can we delete `products.parquet`? It needs a record of what reads it. No program in the lab reads it, but storage could not show you that.
- What stops working if the checkout renames a column in `orders.parquet`? It needs a record of what reads that file and what is made from it.
- Is Thursday's figure wrong, and since when? It needs a record of what happened, and of the rule somebody chose.
- Who should I ask about `daily_sales`? It needs a record of what the asset is, including who is responsible for it.

What would you write down about `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?

## modelVsReality

Real systems keep different things. Some keep history that the lab's warehouse does not. An Apache Iceberg table keeps snapshots, each the state of the table at some time. A Delta Lake table keeps, for each write, the operation, the user and the time, for 30 days by default. The lab's storage keeps only the current rows.

The lab's sizes are estimates from the rows.

The lab works in UTC and has no time zones.

A real platform has hundreds or thousands of assets. Searching for queries that rebuild one would cost far more.

The lab's search covers only the query builder's choices. "None of the builder's choices rebuilds it" means none of those choices; a query outside them might.

## labNote

Every figure in this chapter runs the Metadata Lab, a small data platform in your browser. The lab holds the shop's files and tables for the week of 7 to 13 September 2026. Its programs run in SQL over the rows you see. What a figure shows is worked out from those rows each time. The lab's clock is the week's own, not real time. Nothing leaves your browser.

## lead

You build a small metadata system inside a data platform that runs in your browser. For each idea you predict, build, run, inspect, break and repair it. Your work stays in your browser.
