## A

- Follow a wrong total on the dashboard back to the step where it went wrong.
- Tell a change in the data from a change in the code.
- Find where the shop's records end.
- Question the requirement "Find the cause of the wrong total."

## C

## Back from Thursday's total

The next cell starts at the dashboard's value for Thursday and steps back: `daily_sales`, then `clean_orders`, then the version of `orders.jsonl` that was current when `build_clean_orders` started. The search's output labels step 3 "clean_orders, as it is now" and gives the version's full time.

Steps 1 and 2 show the values the dashboard and `daily_sales` hold. Steps 3 and 4 add up Thursday's revenue from the rows of `clean_orders`, as the table is now, and from the file: price times quantity over the day's completed orders, each order once. That is revenue as `build_daily_sales` counted it before the `refunds` change.

For each step, the cell lists whether its total differs from its input's. It also lists whether the code of the program that made the step had changed since its run the night before.

## D

The dashboard, `daily_sales` and `clean_orders` each hold 5150 pence for Thursday. The version of `orders.jsonl` written at 01:00:41 on Friday 11 holds 20550 pence.

The difference first appears in `clean_orders`. It was made by `run-014`, `build_clean_orders`, early on Friday 11. Its code had not changed since the night before.

The last row is the checkout. It has no step and no figures, because the shop records nothing about it or about what the export read.

Compare this with where you said you would look first.

Before you read on, write in the next cell what you would report to the head of the shop as the cause of Thursday's total, in one sentence.

## DD

What would you report as the cause of Thursday's total?
........

## E

## Two causes

`run-014` counted 3 rows with no customer id in the file it read (Chapter 14). Those are Thursday's three orders.

Two causes together made Thursday's total low. The first is that the checkout sent three orders with no customer id. The second is that `build_clean_orders` drops orders with no customer id. That rule was in its code on Friday 11 and the night before. Remove either, and the total would have counted the three orders.

In this course, a cause that, if removed, would stop a fault happening again is a **root cause**. Both causes meet that.

The shop's records show that the file held the three orders and that the code had not changed. Nothing the checkout does is recorded.

## F

## Saturday with the `refunds` change

The next week has Chapter 2's change `refunds`. From Saturday's row on, `build_daily_sales` keeps every order that is not refunded, where it kept completed orders. The dashboard shows £215.49 for Saturday 12.

The next cell searches back from Saturday's total. Before you read on, decide at which step you expect the difference to appear, and whether a code change will show.

## G

The difference first appears in `daily_sales`: 21549 pence, where `clean_orders` holds 19149 for Saturday. `daily_sales` was made by `run-023`, `build_daily_sales`, early on Sunday 13, and its code had changed since the night before.

Two causes fit together: the change to the code, and Saturday's cancelled order 7037, 2 pairs of brake pads, 2400 pence, which is the difference.

Tuesday 8 also had a cancelled order, 7009. Change `day = "2026-09-12"` to `day = "2026-09-08"`, select the cell and press **Run below**.

## H

For Tuesday, no step differs: 16225 pence at every step, and no code had changed.

With the code as it was when Tuesday's row was written, the cancelled order was left out. A cancelled order alone does not raise the total. What differs between Tuesday and Saturday is the recorded change to the code.

The next cell prints the lines of `build_daily_sales`'s code that changed for the work early on Sunday 13.

## J

## "Find the cause of the wrong total."

The head of the shop's requirement: "Find the cause of the wrong total."

## READINGS

"The cause" could mean three things, each needing something different:

- where the data first went wrong: the values each step holds or adds up to, and the versions of what each run read;
- the change that did it: each run's code, and what each run counted;
- the decision behind that change: a record of who decided it and why.

For Thursday:

- where: two answers fit. `orders.jsonl` already held the three orders with no customer id. The total first changes in `clean_orders`.
- the change: the records show that the code did not change, and that `run-014` counted 3 rows with no customer id. They hold nothing about the checkout.
- the decision: none recorded.

For Saturday, with `refunds`:

- where: `daily_sales`, made by `run-023`.
- the change: the edit to `build_daily_sales`, shown by the code each run recorded.
- the decision: none recorded.

The shop's records meet the first reading for Thursday, the first two for Saturday, and the third for neither. The requirement does not say which of the three it means.

Compare these with what you wrote.

## K

## Before Chapter 18

From Thursday's total, the steps back found where the difference first appeared, in a run whose code had not changed. They ended at `orders.jsonl`. The checkout, the last row, is outside the shop's records. Two causes made the total. From Saturday's, they found a code change. A day with a cancelled order and no code change showed that the order alone does not raise the total.

The records could not show why the code was changed for Saturday, or why the checkout sent the three orders.

Part IV used the shop's record of every run. Every run's events arrived, each once and in order.

Chapter 18, the first chapter of Part V, asks what the shop's records hold when an event never arrives.

- Where does your platform's record end, upstream?
- How would you tell a change to the data from a change to the code?
- Where are the reasons for a change to your code kept, if anywhere?

## L

### How this differs from a real platform

- The shop's faults are invented for the course.
- The search sets the stored values against one measure, a day's revenue as `build_daily_sales` counted it before the `refunds` change. A fault that does not change that total, such as an order counted against the wrong customer, would not show.
- The search reads files in the version current when each run started, and tables as they are now (Chapter 15).
- The shop's repository keeps each program's code. It records no reason for a change.
