# Brief L: Sections 9 and 10, the closing note, the lab's note and the front page

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/revision/L.md`. No text here may state the settings that pass the
challenge, except `p3Explain`, which is shown only after the learner's own rules pass.

## c2Lead

Shown above the challenge. Give the section a purpose. Facts:

- `clean_orders` is made from `orders.parquet` by rules you cannot read.
- Recover them from the two files: for each kind of row the two files differ in, choose whether
  the rules keep it.
- The tests compare the rows your rules keep with `clean_orders`.
- Your rules appear as SQL below the choices, with the number of rows they keep.

## c2Task

The challenge's task. Facts: choose four rules that turn `orders.parquet` into `clean_orders`;
the tests check that your rules keep every row `clean_orders` has, and no row it lacks.

## c2Fields.duplicates

The label of the first rule, plain text: orders that appear twice. (The other three labels stay:
"Orders with no customer id", "Cancelled orders", "Orders with a quantity of 0 or less".)

## c2Options.duplicates

Two option labels as a Markdown list with the key before a colon: keep: keep both rows; one: keep
one row.

## c2Hints

Five hints, a Markdown list, in this order. Keep hints 1 to 3 as they are, word for word; redraft
4 and 5 so they say "row" or "appears twice" where they said "copy" ("copy" is the analyst's
file):

1. Compare `orders.parquet` with `clean_orders` row by row. Which rows are missing, and which
   appear fewer times?
2. A common mistake: dropping cancelled orders. `clean_orders` keeps them; `daily_sales` leaves
   them out later.
3. On Wednesday, order 7015 appears twice in `orders.parquet` and once in `clean_orders`.
4. (Redraft.) Facts: keep one row of an order that appears twice, and drop orders with no
   customer id.
5. (Redraft; this hint gives the answer.) Facts: keep one row of an order that appears twice,
   drop orders with no customer id, keep cancelled orders; either choice passes for the quantity
   rule.

## caption

The challenge's caption, plain text, one sentence ending with a full stop: choose which orders
the rules keep.

## p3Question

Shown after the learner's rules pass, before they commit. It must not hint at the answer. Facts:
your rules pass; how many settings of the four rules give `clean_orders` exactly, yours included?

## p3Options

Three option labels, a Markdown list with the key before a colon: one: one, only yours; two:
two; threeOrMore: three or more.

## p3Explain

Shown after the learner commits. Facts:

- Two settings pass.
- They differ only in the rule for orders with a quantity of 0 or less.
- No order this week had a quantity of 0 or less, so either choice keeps the same rows.
- The shop's program drops such orders. This week's data cannot show that rule, however you
  rebuild it.

## p3Caption

The prediction's caption, plain text, one sentence ending with a full stop: predict how many
settings of the four rules pass.

## reflection

Section 10's prose, the end of the chapter. Do not restate the failure experiment's summary or
list what storage records: add what the chapter has not said. Facts, in this order:

- Back to Thursday. Three orders on Thursday have no customer id. They are in `orders.parquet`
  and not in `clean_orders`, and they make up the 154.00 between Thursday's raw total (205.50) and
  `daily_sales` (51.50).
- Nothing you could read says whether leaving them out is a fault in the checkout or a rule
  somebody chose. The course comes back to Thursday later.
- The four questions from the start each needed a record nobody kept (a Markdown list, one line
  each):
  - Can we delete `products.parquet`? It needs a record of what reads it. No program in the lab
    reads it, but storage could not show you that.
  - What stops working if the checkout renames a column in `orders.parquet`? It needs a record of
    what reads that file and what is made from it.
  - Is Thursday's figure wrong, and since when? It needs a record of what happened, and of the
    rule somebody chose.
  - Who should I ask about `daily_sales`? It needs a record of what the asset is, including who is
    responsible for it.
- End with two questions for the learner: what would you write down about `daily_sales` so that
  the next person need not rebuild it? Who should write it down, and when?

No "really". No promise about "the next chapter".

## modelVsReality

The note at the foot of the chapter: how the lab differs from a real platform. Short
paragraphs. Facts, from the fact sheet's closing section only:

- Real systems keep different things. Some keep history the lab's warehouse does not: an Apache
  Iceberg table keeps snapshots, each the state of the table at some time; a Delta Lake table
  keeps, for each write, the operation, the user and the time, for 30 days by default. The lab's
  storage keeps only the current rows.
- The lab's sizes are estimates from the rows.
- The lab works in UTC and has no time zones.
- A real platform has hundreds or thousands of assets; searching for queries that rebuild one
  would cost far more.
- The lab's search covers only the query builder's choices. "None of the builder's choices
  rebuilds it" means none of those; a query outside them might.

## labNote

The note behind every figure's "Lab" badge, and at the foot of the page under "How the figures
run". Facts: every figure in this chapter runs the Metadata Lab, a small data platform in your
browser; the lab holds the shop's files and tables for the week of 7 to 13 September 2026; its
programs run in SQL over the rows you see; what a figure shows is worked out from those rows each
time; the lab's clock is the week's own, not real time; nothing leaves your browser.

## lead

The front page's opening line, under the course's title, before any chapter. Facts: you build a
small metadata system inside a data platform that runs in your browser; for each idea you
predict, build, run, inspect, break and repair it; your work stays in your browser. Say "small"
once at most. No "really".
