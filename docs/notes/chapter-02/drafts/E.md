## titles.challenge

Recovering the rules of `clean_orders`

## c2Title

Which rules filter `orders.parquet`?

## c2Task

You need to choose four rules that turn `orders.parquet` into `clean_orders`. The tests check that your rules keep every row `clean_orders` has, and no row it lacks.

## c2Fields

duplicates: copies of the same order
missingCustomer: orders with no customer id
cancelled: cancelled orders
quantity: orders with a quantity of 0 or less

## c2Options

duplicates.keep: keep every copy
duplicates.one: keep one
missingCustomer.keep: keep
missingCustomer.drop: drop
cancelled.keep: keep
cancelled.drop: drop
quantity.keep: keep
quantity.drop: drop

## c2Hints

Compare `orders.parquet` with `clean_orders` row by row. Which rows are missing, and which appear fewer times?

A common mistake: dropping cancelled orders. `clean_orders` keeps them; `daily_sales` leaves them out later.

On Wednesday, order 7015 appears twice in `orders.parquet` and once in `clean_orders`.

Keep one copy of each order, and drop orders with no customer id.

Keep one copy, drop orders with no customer id, keep cancelled orders. Either choice passes for the quantity rule.

## c2Lead

The rules appear as SQL below the choices, with the number of rows they keep.

## c2Caption

Choose which orders to filter out.

## caseLabels2

every row of `clean_orders` is kept
no row that `clean_orders` lacks is kept

## titles.reflection

What you could not find out

## reflection

Storage gave you names, types, row counts, sizes, times and one account. It showed when `daily_sales` was last altered and who owns it. You rebuilt `daily_sales` from `clean_orders` with a query. That query matched the warehouse table — a strong hint that you found the right rule.

But the data cannot tell you everything. Until you added a copy and made an edit, the data suggested one answer. After the copy and the edit, it suggested two answers and then none. The program the shop really runs for `clean_orders` drops orders with a quantity of 0 or less. No order this week had one, so both answers to that rule passed your tests. No rebuild from this week's data could find what the program really does.

What would you write down about `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?

## objectives

Say what the shop's storage records about a file, a table and a dashboard, and what it does not.

Rebuild an asset from another asset with a query, and say what a match does and does not prove.

Show, with three changes to the shop, how evidence from data becomes ambiguous, impossible or misleading.

Sort questions about an asset by what can answer them: storage, the data, or only a record kept at the time.

## modelVsReality

Real storage systems record different things. Some warehouses record no owner and no last-altered time. Some object stores keep every version of a file, and logs of who read it. The lab models none of these.

The lab's sizes are estimates from the rows.

The lab works in UTC and has no time zones.

A real platform has hundreds or thousands of assets. Searching for queries that rebuild one would cost far more.

The lab's search covers only the query builder's choices. "No query rebuilds it" means none of those choices.
