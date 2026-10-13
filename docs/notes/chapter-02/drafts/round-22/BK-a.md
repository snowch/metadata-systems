## BK0

The head of the shop has sent you one line: "Thursday's revenue looks wrong."

You investigate it using only what the shop's platform holds, and find where that evidence stops.

1. [Find the discrepancy](#1.-Find-the-discrepancy): compare the raw orders with what the warehouse reports, and find the orders that are missing.
2. [What the platform records](#2.-What-the-platform-records): what object storage, the warehouse and the reporting tool record about each asset.
3. [Test an explanation](#3.-Test-an-explanation): rebuild `daily_sales` from the data, and see what that establishes and what it does not.

[Records made at the time](#Records-made-at-the-time) says which records would have answered; [a short check](#Check:-evidence-of-what-a-job-read) closes the chapter.

## BK2

The rows show whether Thursday's total differs from Thursday's orders. Why it differs, which files the jobs read, and who is responsible for a table depend on what the jobs do and what people decided. The rows a table holds record none of these.

## BK3.1

## 1. Find the discrepancy

## BK3.2

caption: Thursday 10 September, the raw orders against `daily_sales`.
label 1: `orders.jsonl`: £205.50 (20550 pence)
label 2: `daily_sales`: £51.50 (5150 pence)
label 3: Difference: £154.00 (15400 pence)

## BK3.3

This cell sets each day's raw orders beside that day's row in `daily_sales`.

## BK3.4

# `files=` reads `orders.jsonl` from object storage as `raw_orders`.

## BK3.5

On Monday, Friday and Sunday the raw orders add up to the day's row in `daily_sales`. On Tuesday, Wednesday, Thursday and Saturday they do not. The next cell lists every order in `orders.jsonl`, across the whole week, that `clean_orders` does not have.

## BK3.6

**Established.** Across the whole week, 3 orders in `orders.jsonl` are missing from `clean_orders`: 7021, 7023 and 7025. All three are Thursday's, and none has a customer id. Together they are worth 15400 pence, the whole of Thursday's gap.

**Not established.** Which rule left them out, which job applied it, and since when. Why Tuesday, Wednesday and Saturday differ: no order from those days is missing from `clean_orders`.

## BK4.1

## 2. What the platform records

## BK4.2

The cells read each system's own record of its assets: the warehouse's `information_schema` for `daily_sales`, the listing of the bucket `shop-raw`, and the reporting tool's record of `sales_dashboard`.

## BK4.3

**Established.** Each record describes an asset as it is this morning. For `daily_sales`, the warehouse holds two columns, `day` (DATE) and `revenue_pence` (INTEGER), 7 rows, a size of 794 bytes, a created time of 10:20 on 1 September, a last-altered time of 02:30 on Monday 14 September, and an owner, `etl_service`. Object storage holds each file's key, size in bytes and last-modified time. The reporting tool holds the dashboard's title, who created it (`j.marsh`) and when, when it last refreshed (03:00 on Monday 14 September), and the values it shows.

**Not established.** Which job wrote any of these assets, what the job read, which version of its code ran, what the rows were the day before, or who decided the rules that shaped them. None of the three systems records how an asset came to be as it is.

## BK4.5

The rule is met as written, and you did nothing to meet it. The owner it found answers only the last reading, which account controls the table, so you still do not know whom to ask about `daily_sales`.

## BK5.1

## 3. Test an explanation

## BK5.2

Nothing on the platform records how `daily_sales` was made. The usual move is to infer it: find a query over another asset that gives the same rows. The hypothesis below comes with the evidence for each part. Compare it with the guess you wrote at the end of Chapter 1.

## BK5.3

**`daily_sales` is made from `clean_orders`: completed orders only, `price_pence` × `quantity` added up for each day.**

## BK5.4

- `daily_sales` has two columns, `day` and `revenue_pence`: one total in pence per day.
- `clean_orders` has `price_pence`, `quantity`, `status` and `ordered_at` for each order.
- On Thursday, `daily_sales` agrees with `clean_orders`, not with `orders.jsonl`: it is short by exactly the three orders that `clean_orders` lacks.
- Leaving out cancelled orders is an assumption, that a cancelled order brings in no money. Nothing so far shows whether `daily_sales` counts them.

## BK5.5

# Prints True if the query gives exactly the rows of `daily_sales`, in order.

## BK5.6

It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.

The query also accounts for the other three days' gaps.

`clean_orders` also holds 2 cancelled orders: 7009, on Tuesday, worth 2999 pence, and 7037, on Saturday, worth 2400 pence.

The query leaves them out, and so does `daily_sales`: they are Tuesday's and Saturday's gaps.

`orders.jsonl` holds order 7015, placed on Wednesday, twice. `clean_orders` holds it once, so Wednesday's gap is its second copy, worth 4500 pence.

## BK5.7

caption: The hypothesis as a link from `clean_orders` to `daily_sales`, inferred from the data.
from: a table, 44 rows.
step: Query: completed orders, `price_pence` × `quantity`, per day.
fit: It is inferred and gives all 7 rows.
to: a table, 7 rows.
recorded: Nothing: no system records this link.

## BK5.8

**Established.** A query over `clean_orders` that keeps completed orders and adds up `price_pence` × `quantity` per day gives every row of `daily_sales`. It accounts for every day's gap.

**Not established.** That the job that writes `daily_sales` runs this query, or reads `clean_orders` at all. That it did the same every night.
