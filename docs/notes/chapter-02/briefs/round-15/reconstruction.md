# Brief: Chapter 2, the start of "Reconstruction"

Read `docs/style.md` first; its rules hold. The author could not follow this section's start. Its
faults: it told the reader to compare "the guess you wrote in Chapter 1's last cell" without
showing it; it described the query and said that it reproduces `daily_sales` before the cell ran;
and "It also explains Thursday" was never explained.

The section now runs: slot R1, a code cell where the reader writes a guess, slot R2, the cell with
the query (it prints `True` or `False`), slot R3. After R3 the chapter goes on with: "The query is
evidence of how the table could have been made, not a record of how it was made, and three small
changes to the shop show the difference."

## What the reader has seen by now in this chapter

Thursday's orders in `orders.jsonl` add up to 20550 pence and `daily_sales` says 5150. Orders 7021,
7023 and 7025, Thursday's orders with no customer id, are not in `clean_orders`, and together they
are worth the whole of Thursday's gap, 15400 pence. Then the sections on what the systems record.

## Slot R1: under the heading "Reconstruction", before the reader's cell

- The platform records nothing about how `daily_sales` was made.
- The usual move is to infer it from the data: find a query over another asset that gives the same
  rows.
- In Chapter 1's last cell you wrote a guess at what `daily_sales` is made from. The cell below has
  the same line. Write your guess in it again, or a new one: which table, which orders, and what is
  added up.
- Do not say what `daily_sales` is made from.

## Slot R2: after the reader's cell, before the query's cell

- The cell below tests one guess: from `clean_orders`, keep the completed orders, and add up price
  times quantity, in pence, for each day.
- It compares the result with the rows of `daily_sales`. `True` means every row is the same.
- Do not say what it prints.

## Slot R3: after the query's cell

- It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.
- Thursday matches because `clean_orders` does not have Thursday's three orders with no customer
  id, as you found above.
- The query keeps only completed orders. `clean_orders` also holds 2 cancelled orders, which
  `daily_sales` does not count.
- Compare the query with your guess: the same table, and the same orders?

## Output

Write the file `docs/notes/chapter-02/drafts/round-15/reconstruction.md` with three sections headed
`## R1`, `## R2` and `## R3`, each holding only the exact text to place, and nothing else.
