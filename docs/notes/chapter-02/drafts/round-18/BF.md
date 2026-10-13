## BF

The cell below tests one guess, written in the same form as the line in your cell.

**`daily_sales`: made from `clean_orders`, completed orders only, `price_pence` × `quantity` added up for each day, because:**

- `daily_sales` has two columns, `day` and `revenue_pence`: one total in pence for each day.
- Each order in `clean_orders` has a price in pence, `price_pence`, a quantity, `quantity`, and the time it was placed, `ordered_at`.
- On Thursday, `daily_sales` is short of the raw orders by exactly the three orders that `clean_orders` does not have, so on Thursday it agrees with `clean_orders`, not with `orders.jsonl`.
- An order's `status` is `completed` or `cancelled` (Chapter 1). The guess leaves cancelled orders out on the assumption that a cancelled order brings in no money. Nothing above shows whether `daily_sales` counts them: this part of the guess has no evidence yet.

The cell compares the result with the rows of `daily_sales`: `True` means every row is the same, and `False` means at least one row is not.
