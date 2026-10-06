# Brief E: challenge, reflection and the chapter's labels

Attach: `common.md`, `../facts.md`, `docs/style.md`. Write to `docs/notes/chapter-01/drafts/E.md`.

## titles.challenge
A heading of three to six words: recovering the rules of `clean_orders`.

## c2Title
A challenge title of three to six words.

## c2Task
The challenge's task. Two to four sentences. Facts:
1. Choose four rules that turn `orders.parquet` into `clean_orders`.
2. The tests check that your rules keep every row `clean_orders` has, and no row it lacks.

## c2Fields
Four field labels, one per line, in this order:
- duplicates: copies of the same order
- missingCustomer: orders with no customer id
- cancelled: cancelled orders
- quantity: orders with a quantity of 0 or less

## c2Options
Option labels, one per line, as `field.value: label`:
- duplicates.keep: keep every copy
- duplicates.one: keep one
- missingCustomer.keep: keep
- missingCustomer.drop: drop
- cancelled.keep: keep
- cancelled.drop: drop
- quantity.keep: keep
- quantity.drop: drop

## c2Hints
Five hints, in this order, one to three sentences each. Nothing before the fifth gives the whole
answer.
1. The concept: compare `orders.parquet` with `clean_orders` row by row: which rows are missing,
   and which appear fewer times.
2. A common mistake: dropping cancelled orders. `clean_orders` keeps them; `daily_sales` leaves
   them out later.
3. A smaller example: on Wednesday, order 7015 appears twice in `orders.parquet` and once in
   `clean_orders`.
4. Part of the answer: keep one copy of each order, and drop orders with no customer id.
5. The whole answer: keep one copy, drop orders with no customer id, keep cancelled orders. Either
   choice passes for the quantity rule.

## c2Lead
Shown above the challenge, one or two sentences: the rules appear as SQL below the choices, with
the number of rows they keep.

## c2Caption
One sentence caption.

## caseLabels2
Two test labels, one per line:
- every row of `clean_orders` is kept
- no row that `clean_orders` lacks is kept

## titles.reflection
A heading of three to six words: what you could not find out.

## reflection
Two short paragraphs and two questions. Facts:
1. Storage gave you names, types, row counts, sizes, times and one account.
2. The data suggested where `daily_sales` comes from, until a copy, an edit or a failed night.
3. The program the shop really runs for `clean_orders` also drops orders with a quantity of 0 or
   less. No order this week had one, so both answers to that rule passed your tests, and no
   rebuilding from this week's data could find the rule.
4. Close with two questions for the learner to keep: what would you write down about
   `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?

## objectives
Four objectives, one per line, each starting with a verb, each one sentence:
1. Say what the shop's storage records about a file, a table and a dashboard, and what it does not.
2. Rebuild an asset from another asset with a query, and say what a match does and does not prove.
3. Show, with three changes to the shop, how evidence from data becomes ambiguous, impossible or
   misleading.
4. Sort questions about an asset by what can answer them: storage, the data, or only a record kept
   at the time.

## modelVsReality
A note headed elsewhere as "How the lab differs from a real platform". Short paragraphs or a short
list. Facts:
1. Real storage systems record different things. Some warehouses record no owner and no
   last-altered time. Some object stores can keep every version of a file, and logs of who read
   it. The lab models none of these.
2. The lab's sizes are estimates from the rows.
3. The lab works in UTC and has no time zones.
4. A real platform has hundreds or thousands of assets. Searching for queries that rebuild one
   would cost far more.
5. The lab's search covers only the query builder's choices. "No query rebuilds it" means none of
   those choices.
