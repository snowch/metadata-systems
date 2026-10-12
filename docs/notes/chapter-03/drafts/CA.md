## A

- Write a record of `daily_sales` from what the shop's people tell you.
- Find which of Chapter 2's four questions the record answers.
- Tell what a record of an asset holds, from what the systems record about it.
- Test a requirement about descriptions, and a check, against changes to the shop.

## B

## Monday afternoon

It is still Monday 14 September 2026, in the afternoon. In Chapter 2 you found that `daily_sales` leaves out Thursday's three orders with no customer id (7021, 7023 and 7025, worth 15400 pence together), and nothing on the platform records whether they should be left out. You asked the head of the shop who decides what `daily_sales` should count.

The head of the shop replied:

> Jo Marsh, in finance, built the dashboard and decides what counts as revenue. Sam Lund keeps the product catalogue. The two cleaned tables, `clean_customers` and `clean_orders`, were the last engineer's and are now yours.

Jo Marsh's answer, about a day's revenue:

> The value of every completed order placed that day, taking the day from the order's time in UTC, in pence.

Next, you write what you have learnt as a record kept beside the data, then ask Chapter 2's four questions again.

## C

## A record of `daily_sales`

A record is a set of lines of text that you write and keep beside the data. Each line holds one fact. It starts with the asset's name. If the fact is about a column, the column's name comes next. Then come a field, a colon and the value. For example:

`daily_sales revenue_pence unit: pence`

The cells use three fields:

- `means`: what the asset or the column means.
- `responsible`: who to ask about it.
- `unit`: the unit the values are in.

A value of `........` is one not yet written.

The record cell below holds five lines for `daily_sales`, each with `........` as its value. Replace each `........` with what the head of the shop and Jo Marsh told you. Then select the cell and press **Run below**. The cell shows the record as a table, one row per line. **Save** keeps what you wrote.

## D

The check cell lists each column of `daily_sales` that has no description, meaning no `means` line with a value. It also lists each line that names a column the warehouse does not have. With every line written, it finds no problems.

## E

## The four questions again

Chapter 2 opened with four questions the platform could not answer:

- Is Thursday's total wrong, and since when?
- Can we delete `products.csv`? Does anything still read it?
- If the checkout renames a column in `orders.jsonl`, what stops working?
- Who should I ask about `daily_sales`?

Before you run the cells below, write in the next cell, for each question, whether your record answers it, in part or not at all, and why. **Save** keeps what you wrote.

## F

"""
Is Thursday's total wrong, and since when? ........
Can we delete products.csv? Does anything still read it? ........
If the checkout renames a column, what stops working? ........
Who should I ask about daily_sales? ........
"""

## G

The next cell looks up who the record names as responsible for `daily_sales`.

## H

The record answers the fourth question: it names Jo Marsh as responsible for `daily_sales`. The next cell takes Jo Marsh's words about a day's revenue and turns them into a query over `orders.jsonl`. It keeps each completed order once, even an order the export wrote twice. It adds up price times quantity for each UTC day, and puts that total beside each row of `daily_sales`, marked `same` or `different`.

## I

Thursday is the only day that differs: `daily_sales` shows 5150 pence, and Jo Marsh's meaning gives 20550. Every other day is the same. By that meaning, Thursday's total is wrong.

The record says nothing about since when. It has no time in it, and nothing about what happened each night.

The words "every completed order" do not say what to do with an order the export wrote twice. The query had to decide, and it counts each order once. A query that counted every line of the file would also find Wednesday different, because order 7015 is in the file twice.

## J

The next cell compares `daily_sales` with a meaning you could write from the data alone: the completed orders in `clean_orders`, added up per day, as in Chapter 2.

## K

Every day is the same, Thursday included. A description written from the data agrees with the data on every day, so it cannot show that any day is wrong. Jo Marsh's description came from the person who decides what counts as revenue, not from `daily_sales`, so `daily_sales` can be checked against it.

## L

The last cell lists each line of your record that names `products.csv` or `orders.jsonl`.

It finds none. The second and third questions ask what reads those files. A record of what each asset is does not say what reads it. Chapter 6 records what reads each asset.
