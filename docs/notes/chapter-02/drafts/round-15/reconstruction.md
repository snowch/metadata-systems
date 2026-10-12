## R1

The platform records nothing about how `daily_sales` was made. The usual move is to infer it from the data: find a query over another asset that gives the same rows.

In Chapter 1's last cell you wrote a guess at what `daily_sales` is made from. The cell below has the same line. Write your guess in it again, or a new one: which table, which orders, and what is added up.

## R2

The cell below tests one guess. It takes `clean_orders`, keeps the completed orders, and adds up price times quantity, in pence, for each day. It compares the result with the rows of `daily_sales`: `True` means every row is the same, and `False` means at least one row is not.

## R3

It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.

Thursday matches because `clean_orders` does not hold Thursday's three orders with no customer id: orders 7021, 7023 and 7025, which you found above.

The query keeps only completed orders. `clean_orders` also holds 2 cancelled orders. `daily_sales` does not count them, and neither does the query.

Compare the query with your guess. Did you name the same table and the same orders?
