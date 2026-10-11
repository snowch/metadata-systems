## A

[Chapter 2](chapter_02.ipynb) goes back to the head of the shop's message and starts with Thursday's revenue.

## B

Messages like the head's arrive every week on a platform you did not build. Each one raises questions like these:

## C

The rows answer part of the first question: whether the total differs. The full answers come from what happened, or from a decision that someone made: a job that reads a file, a rule that a person chose, a person who took responsibility. The rows a table holds today hold neither.

## D

Thursday's orders in `orders.jsonl` add up to 20550 pence. `daily_sales` says 5150 for Thursday, and the dashboard shows £51.50. The two totals differ by 15400 pence, £154.00.

## E

The cell below reads the row from `daily_sales` for the day that the cell above sets. If you change the day in the cell above, run the cell below too. It does not run again by itself. Select the cell above and press **Run below**.

## F

The cell below puts, for every day, the total of the raw orders in `orders.jsonl` beside that day's row in `daily_sales`. It shows whether the two are the same. The `files=` argument of `warehouse.sql` lets the query read `orders.jsonl` from object storage as a table called `raw_orders`.

## G

The cell below lists Thursday's orders in `orders.jsonl` that `clean_orders` does not have. Look at what these orders have in common, then compare their total with Thursday's gap of 15400 pence.

## H

Orders 7021, 7023 and 7025 have no customer id. Together they are worth 15400 pence, the whole of Thursday's gap. `clean_orders` does not have them. Their absence from `clean_orders` shows which orders are missing, not why: nothing on the platform records the rule that left them out.

## I

The cell below reads the warehouse's record of `daily_sales`. The warehouse keeps a record of its own tables, which you query with SQL as `information_schema`.

## J

Object storage records three things about a file: its key, its size in bytes and when it was last modified. A key is the file's full name, such as `s3://shop-raw/orders.jsonl`, where `shop-raw` is the bucket: the container the file sits in.

## K

The platform records the current state of each asset and none of its history.

## L

In the shop's platform, a system records what its own work needs and nothing more.

## M

The owner field shows how far that goes. "Who should I ask about `daily_sales`?" wants a person or a team. The requirement is: "Every table must have an owner." The warehouse records `etl_service` as the owner of all three tables. The name looks like an account a program logs in as, and the warehouse records nothing more about it. The field is called owner, but the question it answers is which account controls the table. The requirement is met as written, and your question is not.

## N

The cell below lists the owner of every table in the warehouse.

## O

Take out the guess you wrote for `daily_sales` at the end of Chapter 1. Compare it with the query in the cell below, which the data supports.

## P

For each change, find which of the platform's records show it, and whether a query still gives every row of `daily_sales`. Choose a change to the shop from the menu below. Then select the first cell below the menu and press **Run below**. The cells below show the platform on Monday morning, after the week ran with the change you chose. The cells above the menu keep showing the week as it ran.

## Q

The cell below lists each query, from a fixed set of simple ones over the week's assets, that gives every row of `daily_sales`, even if it gives a row more. Each row of its result is one query: `source` names the asset it reads; `keep` says which orders it keeps (all, completed or cancelled); `measure` says what it adds up (revenue, quantity or rows); `per` says what it groups by (day, customer or product); and `sql` is the query itself.

## R

Each record is normal on its own. `daily_sales` has six rows, none for Sunday. The gap shows only when you compare the last-altered times: `daily_sales` was last altered on Sunday at 02:30. `clean_orders` was last altered on Monday at 02:05, and the dashboard was refreshed on Monday at 03:00. Only a record of the failure would say that a write was due and did not happen.

## S

Your guess for `clean_orders` from Chapter 1 meets the same limit: the data can confirm a rule only where some row would have triggered it.

## T

In the shop's design, which the platform does not record and you cannot see, `clean_orders` is made from `orders.jsonl` by four rules:

## U

what was made from what: such a record would say that `daily_sales` is built from the completed orders in `clean_orders`, and that the dashboard reads `daily_sales`.

## V

You write your handover note in the cell above, between the triple quotes, and press **Save** to keep it. The cell below shows only what the warehouse records about `daily_sales`, to compare with your note.

## W

Write what daily_sales means and who to ask about it. Include what
runs each night, what it reads and writes, and what to do if a night fails.

## X

Nothing in this chapter tested your guess for `clean_customers`. What would test it?

- Pick a table on a platform you work on. What does its record say about who is responsible for it, and what does it say about what the table is made from?
- What would a description of `daily_sales` have to hold to answer "Who should I ask about `daily_sales`?"

## Y

The page runs Python in your browser, and the first time you open it on its own, your browser downloads about 13 MB. Measured on a computer, the page downloaded less than 1 MB when opened from Chapter 1's link, in a browser that had opened Chapter 1. Chapter 1's link opens this page in a new tab. Chapter 1 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 1 leaves more memory for this page. On a computer, running every cell took 10 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

## Z

A file's size is its real size in bytes. A table's size is an estimate from its rows. All times are UTC. A real platform has hundreds or thousands of assets; searching for queries that rebuild one would cost far more. "No simple query over the week's assets reproduces it" means none of the simple queries the menu's last cell tries. A query with a condition on the date could still reproduce the edited table.
