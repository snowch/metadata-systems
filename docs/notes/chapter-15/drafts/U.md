## A

- Follow Thursday's figure on the dashboard back to the lines of the file it came from.
- Find what a record of a figure's sources leaves out.
- Find why Sunday's figure no longer adds up from the shop's tables.
- Question the requirement "Show where Thursday's figure came from."

## B

## Thursday's £51.50

Chapter 2 began with the first line of the shop's message: "Thursday's revenue looks wrong." The dashboard shows £51.50 for Thursday 10.

Before you read on, write in the next cell which orders you expect £51.50 to be made of.

## BB

Which orders is Thursday's £51.50 made of?
........

## BC

The next cell follows Thursday's figure back, one step at a time, from the dashboard to the file. At each step it lists the asset, the run that made it, the rows it found, and their total in pence.

## C

Thursday's figure goes back through four steps.

1. The dashboard's value for Thursday, £51.50, drawn by `run-028`, `refresh_dashboard`, early on Monday 14.
2. The row of `daily_sales` for Thursday, written by `run-015`, `build_daily_sales`, early on Friday 11.
3. The rows of `clean_orders` for orders 7020, 7022, 7024 and 7026, written by `run-014`, `build_clean_orders`, early on Friday 11.
4. Lines 21, 23, 25 and 27 of `orders.jsonl`, in the version the export wrote at 01:00 on Friday 11, the last before `run-014` started.

Each step adds up to 5150 pence.

The record of where a piece of data came from (the rows it was made from, the programs and runs that made it, and the inputs as they were when each run read them) is its **provenance**.

The figure is the sum of four orders. No one of them is its source: change any of the four and the figure changes.

`orders.jsonl` is read in the version that was current when `run-014` started. Object storage keeps every version of a file, with the time it was written. `clean_orders` is read as it is now: the warehouse keeps no earlier state of a table.

## D

## What the record leaves out

Thursday's figure is low because three orders were left out (Chapter 2). The four steps list only the rows the figure was made from.

The next cell follows the figure back again with `dropped=False`. Change it to `dropped=True`. Before you press **Run below**, decide whether the steps will then list orders 7021, 7023 and 7025. Then select the cell and press **Run below**.

## E

The last row lists lines 22, 24 and 26 of the same version of `orders.jsonl`: orders 7021, 7023 and 7025, each with `customer_id IS NOT NULL is false`, together 15400 pence. `run-014` read them and left them out.

They are found by applying `build_clean_orders`'s conditions again to each line of that version.

A record of what a figure was made from lists what was used. Why Thursday's figure is low is in what was not used. Finding that needs the rows each run read and the condition that left each out.

## F

## Sunday's figure

The next week has the change `corrected`. From Saturday's row on, `build_daily_sales` takes away what was returned, through the function `returned_quantity`, which reads the table `returns` (Chapter 10).

On Sunday 13 at 18:10 the returns desk records `r-205`: 2 rolls of bar tape back from order 7044. Early on Monday 14, at 02:30, `build_daily_sales` writes Sunday's row. At 08:40 on Monday the desk corrects `r-205` to 1 roll.

Before you read on, write in the next cell whether you expect Sunday's figure to add up from the shop's tables as they are at 09:00 on Monday, and why.

## FF

Does Sunday's figure add up from the tables as they are now?
........

## G

The dashboard and `daily_sales` show 6925 pence for Sunday.

The five Sunday orders in `clean_orders`, 7043 to 7047, add up to 9775 pence. `returns`, as it is now, holds `r-205` with 1 roll of order 7044: 1425 pence less. Together, these come to 8350 pence.

8350 is not 6925. Sunday's figure does not add up from the tables as they are now.

The next cell lists every version of `r-205`'s object.

## H

`r-205`'s object has two versions. The first, at 18:10 on Sunday, has quantity 2. The second, at 08:40 on Monday, has quantity 1.

`run-034`, the run of `build_daily_sales` that wrote Sunday's row, started at 02:30 on Monday, between the two.

In the next cell, change `as_read=False` to `as_read=True`, select the cell and press **Run below**. With `as_read=True`, the cell rebuilds `returns` as it was when `run-034` started, from the versions of the objects that the runs of `record_return` read.

## I

At 02:30:00, `returns` held `r-205` with 2 rolls, from the first version, read by `run-031`: 2850 pence less. 9775 less 2850 is 6925, Sunday's figure.

Each version of the object was a different input. `run-034` used what the first version held.

The warehouse keeps no earlier state of `returns`. It could be rebuilt only because each run of `record_return` recorded which version it read, and object storage kept that version.

## J

## "Show where Thursday's figure came from."

The shop's requirement is: "Show where Thursday's figure came from."

Before you read on, write in the next cell what you would show.

## JJ

What would you show?
........

## READINGS

"Where it came from" could mean four things. Each needs something different.

- The rows: which rows it was made from, found by following it back row by row.
- The program: which programs made it, from lineage.
- The run: which runs made it, from the record of each run.
- The rows as they were when each run read them: a version of each input, kept and recorded.

## K

For Thursday, the first three were met. The fourth was met for the file, read in the version current when `run-014` started. The tables were read as they are now, and every step still added up.

For Sunday, with the correction, the first three were met. The fourth was not met by `returns` as it is now. It was met only by rebuilding the table from the object versions the runs recorded.

A record of what was used does not show what was left out, which was the question about Thursday.

The requirement does not say which reading it means.

Compare these with what you wrote.

## L

## Before Chapter 16

Thursday's £51.50 was followed back through four steps to four lines of one version of `orders.jsonl`. The orders that made it low were not among them. They showed only once the rows each run read and left out were listed.

Sunday's figure did not add up from the tables as they were at 09:00 on Monday. It added up from `returns` as it was when the run started, rebuilt from object versions.

The record could not show what was made from a return after it changed, or what a change to a column would affect.

Chapter 16 asks, before a change is made, what it would affect.

- Which of your platform's tables could be read again as a run read it?
- How would you find the rows a program read and left out?
- Which of your figures were made from inputs that have changed since?

## M

### How this differs from a real platform

- The returns, the correction and the runs are invented for the course.
- The W3C's PROV data model (a W3C Recommendation of 30 April 2013) describes provenance with entities (things), activities (which happen over a period of time and use or generate entities) and agents (which bear responsibility). Its relations include an activity using an entity, an entity generated by an activity, and one entity derived from another.
- In PROV an entity has fixed aspects, so the two versions of `r-205`'s object would be two entities.
- The shop's way of following a figure back is its own: it applies the programs' conditions again to the rows.
- Some table formats keep a table's earlier states as snapshots (Chapter 2). With them, a table could be read as a run read it.
