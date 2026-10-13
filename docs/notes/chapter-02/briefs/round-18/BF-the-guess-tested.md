# Brief BF: say which guess the reconstruction tests, and why

The author asked whether the page should say "we are testing a guess that `daily_sales` is made from
… because …". It should. The paragraph before the reconstruction's query says what the query does,
step by step, but not which guess it is, or what makes that guess worth testing, so the reader
cannot set it beside the guess they wrote in the cell above it, whose line has the form
`daily_sales:     made from ........ because ........`.

Write one slot, BF, to replace this paragraph:

> The cell below tests one guess. It takes `clean_orders`, keeps the completed orders, and adds up
> price times quantity, in pence, for each day. It compares the result with the rows of
> `daily_sales`: `True` means every row is the same, and `False` means at least one row is not.

Follow `docs/style.md` and `AGENTS.md`. British English. No em dashes. The reader is "you", a data
engineer who has done Chapter 1 and read Chapter 2 down to this point. Keep names in backticks
exactly as written. A block of code is a "cell". Never use "run" as a noun. Do not use the words
"lineage", "event" or "metadata". Do not say what the cell will print, and do not say whether the
guess is right.

## Facts, in order

1. The cell below tests one guess, written in the same form as the line in your cell.
2. Then the guess itself, as a block of code of its own (three backticks above and below), exactly
   this line, kept word for word:

   daily_sales:     made from clean_orders, completed orders only, price_pence × quantity added up for each day, because

3. Then the reasons, as a Markdown list, one item each, each one something this page or Chapter 1
   showed:
   - `daily_sales` has two columns, `day` and `revenue_pence`: one total in pence for each day.
   - Each order in `clean_orders` has a price in pence, `price_pence`, a quantity, `quantity`, and
     the time it was placed, `ordered_at`.
   - On Thursday, `daily_sales` is short of the raw orders by exactly the three orders that
     `clean_orders` does not have, so on Thursday it agrees with `clean_orders`, not with
     `orders.jsonl`.
   - An order's `status` is `completed` or `cancelled` (Chapter 1). The guess leaves cancelled
     orders out on the assumption that a cancelled order brings in no money. Nothing above shows
     whether `daily_sales` counts them: this part of the guess has no evidence yet.
4. Keep this sentence word for word, after the list: "It compares the result with the rows of
   `daily_sales`: `True` means every row is the same, and `False` means at least one row is not."
   Begin it with "The cell" in place of "It" if the sentence before it is the list.

Write `docs/notes/chapter-02/drafts/round-18/BF.md`: a `## BF` heading, then the slot's text and
nothing else. Write the file once. Use only the Read and Write tools. Send no messages.
