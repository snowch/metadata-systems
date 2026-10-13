# Brief BK, part A: the opening and the three stages

Read `BK-common.md` first; its rules hold for every slot.

## BK0: the opening, under the chapter's heading

1. The head of the shop has sent you one line, word for word: "Thursday's revenue looks wrong."
2. You investigate it using only what the shop's platform holds, and find where that evidence
   stops.
3. A numbered list of the three stages. Each stage's name is a link, written exactly as here,
   followed by a colon and what the stage does:
   1. `[Find the discrepancy](#1.-Find-the-discrepancy)`: compare the raw orders with what the
      warehouse reports, and find the orders that are missing.
   2. `[What the platform records](#2.-What-the-platform-records)`: what object storage, the
      warehouse and the reporting tool record about each asset.
   3. `[Test an explanation](#3.-Test-an-explanation)`: rebuild `daily_sales` from the data, and
      see what that establishes and what it does not.
4. One line after the list, with two links written exactly as here:
   `[Records made at the time](#Records-made-at-the-time)` says which records would have answered;
   `[a short check](#Check:-evidence-of-what-a-job-read)` closes the chapter.

## BK2: under the four questions (the questions themselves stay as they are)

1. Keep this sentence word for word: "The rows show whether Thursday's total differs from
   Thursday's orders."
2. Why it differs, which files the jobs read, and who is responsible for a table depend on what
   the jobs do and what people decided. The rows a table holds record none of these.
Two or three sentences in all.

## BK3: stage 1

BK3.1. The heading, word for word: `## 1. Find the discrepancy`

BK3.2. Labels for a figure of three totals for Thursday 10 September. Give the caption and the
three labels, each on its own line, as `caption:`, `label 1:`, `label 2:`, `label 3:`.
- caption: Thursday 10 September, the raw orders against `daily_sales`.
- label 1: the raw orders in `orders.jsonl` (the figure shows £205.50, 20550 pence).
- label 2: `daily_sales` (£51.50, 5150 pence).
- label 3: the difference (£154.00, 15400 pence).
Labels are two to five words. The caption is one short line.

BK3.3. One sentence before a cell: the cell sets each day's raw orders beside that day's row in
`daily_sales`. Do not say what it finds.

BK3.4. One comment line for the top of that cell's code, starting `# `, at most 70 characters: the
argument `files=` makes the query read `orders.jsonl` from object storage as a table called
`raw_orders`.

BK3.5. After that cell, two sentences, then one more:
1. Keep these word for word: "On Monday, Friday and Sunday the raw orders add up to the day's row
   in `daily_sales`. On Tuesday, Wednesday, Thursday and Saturday they do not."
2. The next cell lists every order in `orders.jsonl`, across the whole week, that `clean_orders`
   does not have.

BK3.6. A box of findings in two parts. Write the first part as one paragraph starting
`**Established.**` and the second as one paragraph starting `**Not established.**`.
Established:
1. Across the whole week, 3 orders in `orders.jsonl` are missing from `clean_orders`: 7021, 7023
   and 7025.
2. All three are Thursday's, and none has a customer id.
3. Together they are worth 15400 pence, the whole of Thursday's gap.
Not established:
4. Which rule left them out, which job applied it, and since when.
5. Why Tuesday, Wednesday and Saturday differ: no order from those days is missing from
   `clean_orders`.

## BK4: stage 2

BK4.1. The heading, word for word: `## 2. What the platform records`

BK4.2. One sentence before four cells: the cells read each system's own record of its assets: the
warehouse's `information_schema` for `daily_sales`, the listing of the bucket `shop-raw`, and the
reporting tool's record of `sales_dashboard`.

BK4.3. A box of findings in two parts, as in BK3.6.
Established:
1. Each record describes an asset as it is this morning.
2. For `daily_sales` the warehouse holds two columns, `day` (DATE) and `revenue_pence`
   (INTEGER), 7 rows, a size of 794 bytes, a created time of 10:20 on 1 September, a
   last-altered time of 02:30 on Monday 14 September, and an owner, `etl_service`.
3. Object storage holds each file's key, size in bytes and last-modified time.
4. The reporting tool holds the dashboard's title, who created it (`j.marsh`) and when, when it
   last refreshed (03:00 on Monday 14 September), and the values it shows.
Not established:
5. Which job wrote any of these assets, what the job read, which version of its code ran, what
   the rows were the day before, or who decided the rules that shaped them.
6. None of the three systems records how an asset came to be as it is.

BK4.5. After the table of the owner rule's readings, which ends the requirement exercise. One or
two sentences:
1. The rule is met as written, and you did nothing to meet it.
2. The owner it found answers only the last reading, which account controls the table, so you
   still do not know whom to ask about `daily_sales`. Keep the words "so you still do not know
   whom to ask" word for word.

## BK5: stage 3

BK5.1. The heading, word for word: `## 3. Test an explanation`

BK5.2. The lead, before the hypothesis:
1. Nothing on the platform records how `daily_sales` was made.
2. The usual move is to infer it: find a query over another asset that gives the same rows.
3. The hypothesis below comes with the evidence for each part. Compare it with the guess you wrote
   at the end of Chapter 1.

BK5.3. The hypothesis, word for word, as one bold line:
**`daily_sales` is made from `clean_orders`: completed orders only, `price_pence` × `quantity`
added up for each day.**

BK5.4. A bulleted list of the evidence, one short bullet each:
1. `daily_sales` has two columns, `day` and `revenue_pence`: one total in pence per day.
2. `clean_orders` has `price_pence`, `quantity`, `status` and `ordered_at` for each order.
3. On Thursday, `daily_sales` agrees with `clean_orders`, not with `orders.jsonl`: it is short by
   exactly the three orders that `clean_orders` lacks.
4. Leaving out cancelled orders is an assumption, that a cancelled order brings in no money.
   Nothing so far shows whether `daily_sales` counts them.

BK5.5. One comment line for the top of the cell's code, starting `# `, at most 70 characters: the
last line prints True if the query gives exactly the rows of `daily_sales`, in order.

BK5.6. After the cell:
1. Keep these words word for word: "It prints `True`: the query gives all 7 rows of `daily_sales`,
   Thursday's 5150 pence included."
2. The query also accounts for the other three days' gaps.
3. `clean_orders` holds 2 cancelled orders: 7009, on Tuesday, worth 2999 pence, and 7037, on
   Saturday, worth 2400 pence. Keep the words "`clean_orders` also holds 2 cancelled orders" if
   they fit; otherwise keep "2 cancelled orders".
4. The query leaves them out, and so does `daily_sales`: they are Tuesday's and Saturday's gaps.
5. `orders.jsonl` holds order 7015, placed on Wednesday, twice. `clean_orders` holds it once, so
   Wednesday's gap is its second copy, worth 4500 pence.

BK5.7. Labels for a diagram of the hypothesis. Give each on its own line as `caption:`,
`from:`, `step:`, `fit:`, `to:`, `recorded:`.
- caption: the hypothesis as a link from `clean_orders` to `daily_sales`, inferred from the data.
- from: under the name `clean_orders`: a table, 44 rows.
- step: what the query does: completed orders, `price_pence` × `quantity`, per day.
- fit: that it is inferred and gives all 7 rows.
- to: under the name `daily_sales`: a table, 7 rows.
- recorded: what any system records of this link: nothing.
Each label is at most eight words.

BK5.8. A box of findings in two parts, as in BK3.6.
Established:
1. A query over `clean_orders` that keeps completed orders and adds up `price_pence` × `quantity`
   per day gives every row of `daily_sales`.
2. It accounts for every day's gap.
Not established:
3. That the job that writes `daily_sales` runs this query, or reads `clean_orders` at all.
4. That it did the same every night.
