[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 14](chapter_14.ipynb) · [Next: Chapter 16](chapter_16.ipynb)

# Chapter 15: Provenance

**Objectives**

- Follow Thursday's total on the dashboard back to the lines of the file it came from.
- Find what a record of a total's sources leaves out.
- Find why Sunday's total no longer adds up from the shop's tables.
- Question the requirement "Show where Thursday's total came from."

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 14's link, in a browser that had opened and run Chapter 14 (measured on a computer). Chapter 14's link opens this page in a new tab. Chapter 14 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 14 leaves more memory for this page.

Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

</details>

</div>

<div class="ms-box ms-box-steps">

**Running and saving the page**

1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.

</div>

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

<figure class="ms-figure"><figcaption>The shop&#x27;s three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table <code>returns</code>.</figcaption><div class="ms-fig"><div class="ms-systems"><div class="ms-system"><h4>Object storage</h4><ul><li><code>customers.jsonl</code><span class="ms-kind">file</span></li><li><code>orders.jsonl</code><span class="ms-kind">file</span></li><li><code>products.csv</code><span class="ms-kind">file</span></li><li><code>r-201.json</code><span class="ms-kind">file</span></li><li><code>r-202.json</code><span class="ms-kind">file</span></li><li><code>r-204.json</code><span class="ms-kind">file</span></li></ul></div><div class="ms-flow">jobs nightly; functions at any hour<span class="ms-right">&nbsp;&rarr;</span></div><div class="ms-system"><h4>Warehouse</h4><ul><li><code>clean_customers</code><span class="ms-kind">table</span></li><li><code>clean_orders</code><span class="ms-kind">table</span></li><li><code>daily_sales</code><span class="ms-kind">table</span></li><li><code>returns</code><span class="ms-kind">table</span></li></ul></div><div class="ms-flow">jobs nightly; functions at any hour<span class="ms-right">&nbsp;&rarr;</span></div><div class="ms-system"><h4>Reporting tool</h4><ul><li><code>sales_dashboard</code><span class="ms-kind">dashboard</span></li></ul></div></div><div class="ms-tally">6 files + 4 tables + 1 dashboard = 11 assets</div></div></figure>

## Thursday's £51.50

Chapter 2 began with the head of the shop's message: "Thursday's revenue looks wrong." The dashboard shows £51.50 for Thursday 10.

Before you read on, write in the next cell which orders you expect £51.50 to be made of.

```
expected_orders = """
Which orders is Thursday's £51.50 made of?
........
"""
```

The next cell follows Thursday's total back, one step at a time, from the dashboard to the file. At each step it lists the asset, the run that made it, the rows it found, and their total in pence.

```
week15 = shop.run_week()
shop.provenance.trace(week15, "2026-09-10")
```

OUTPUT:
step	asset	made by	rows	pence
1	sales_dashboard	run-028, refresh_dashboard	the value for 2026-09-10, shown as £51.50	5150
2	daily_sales	run-015, build_daily_sales	the row for 2026-09-10	5150
3	clean_orders	run-014, build_clean_orders	7020, 7022, 7024, 7026	5150
4	orders.jsonl, version of 09-11 01:00	the export	lines 21, 23, 25, 27	5150

Thursday's total goes back through four steps.

1. The dashboard's value for Thursday, £51.50, drawn by `run-028`, `refresh_dashboard`, early on Monday 14.
2. The row of `daily_sales` for Thursday, written by `run-015`, `build_daily_sales`, early on Friday 11.
3. The rows of `clean_orders` for orders 7020, 7022, 7024 and 7026, written by `run-014`, `build_clean_orders`, early on Friday 11.
4. Lines 21, 23, 25 and 27 of `orders.jsonl`, in the version the export wrote at 01:00 on Friday 11, the last before `run-014` started.

Each step adds up to 5150 pence.

The record of where a piece of data came from (the rows it was made from, the programs and runs that made it, and the inputs as they were when each run read them) is its **provenance**.

The total is the sum of four orders. No one of them is its source: change any of the four and the total changes.

`orders.jsonl` is read in the version that was current when `run-014` started. Object storage keeps every version of a file, with the time it was written. `clean_orders` is read as it is now: the warehouse keeps no earlier state of a table.

## What the record leaves out

Thursday's total is low because three orders were left out (Chapter 2). The four steps list only the rows the total was made from.

The next cell follows the total back again with `dropped=False`. Change it to `dropped=True`. Before you press **Run below**, decide whether the steps will then list orders 7021, 7023 and 7025. Then select the cell and press **Run below**.

```
shop.provenance.trace(week15, "2026-09-10", dropped=False)
```

OUTPUT:
step	asset	made by	rows	pence
1	sales_dashboard	run-028, refresh_dashboard	the value for 2026-09-10, shown as £51.50	5150
2	daily_sales	run-015, build_daily_sales	the row for 2026-09-10	5150
3	clean_orders	run-014, build_clean_orders	7020, 7022, 7024, 7026	5150
4	orders.jsonl, version of 09-11 01:00	the export	lines 21, 23, 25, 27	5150

The last row lists lines 22, 24 and 26 of the same version of `orders.jsonl`: orders 7021, 7023 and 7025, each with `customer_id IS NOT NULL is false`, together 15400 pence. `run-014` read them and left them out.

They are found by applying `build_clean_orders`'s conditions again to each line of that version.

A record of what a total was made from lists what was used. Why Thursday's total is low is in what was not used. Finding that needs the rows each run read and the condition that left each out.

## Sunday's total

The next week has the change `corrected`. From Saturday's row on, `build_daily_sales` takes away what was returned, through the function `returned_quantity`, which reads the table `returns` (Chapter 10).

On Sunday 13 at 18:10 the returns desk records `r-205`: 2 rolls of bar tape back from order 7044. Early on Monday 14, at 02:30, `build_daily_sales` writes Sunday's row. At 08:40 on Monday the desk corrects `r-205` to 1 roll.

Before you read on, write in the next cell whether you expect Sunday's total to add up from the shop's tables as they are at 09:00 on Monday, and why.

```
expected_sunday = """
Does Sunday's total add up from the tables as they are now?
........
"""
```

```
week15c = shop.run_week(["corrected"])
shop.provenance.trace(week15c, "2026-09-13")
```

OUTPUT:
step	asset	made by	rows	pence
1	sales_dashboard	run-035, refresh_dashboard	the value for 2026-09-13, shown as £69.25	6925
2	daily_sales	run-034, build_daily_sales	the row for 2026-09-13	6925
3	clean_orders	run-033, build_clean_orders	7043, 7044, 7045, 7046, 7047	9775
3	returns, as it is now	record_return	r-205: 1 of order 7044	-1425
4	orders.jsonl, version of 09-14 01:00	the export	lines 44, 45, 46, 47, 48	9775

The dashboard and `daily_sales` show 6925 pence for Sunday.

The five Sunday orders in `clean_orders`, 7043 to 7047, add up to 9775 pence. `returns`, as it is now, holds `r-205` with 1 roll of order 7044: 1425 pence less. Together, these come to 8350 pence.

8350 is not 6925. Sunday's total does not add up from the tables as they are now.

The next cell lists every version of `r-205`'s object.

```
shop.provenance.object_versions(week15c, "r-205")
```

OUTPUT:
version	at	order	quantity	deleted
6f6625e102be	2026-09-13T18:10:00Z	7044	2	
06033bcf57d8	2026-09-14T08:40:00Z	7044	1

`r-205`'s object has two versions. The first, at 18:10 on Sunday, has quantity 2. The second, at 08:40 on Monday, has quantity 1.

`run-034`, the run of `build_daily_sales` that wrote Sunday's row, started at 02:30 on Monday, between the two.

In the next cell, change `as_read=False` to `as_read=True`, select the cell and press **Run below**. With `as_read=True`, the cell rebuilds `returns` as it was when `run-034` started, from the versions of the objects that the runs of `record_return` read.

```
shop.provenance.trace(week15c, "2026-09-13", as_read=False)
```

OUTPUT:
step	asset	made by	rows	pence
1	sales_dashboard	run-035, refresh_dashboard	the value for 2026-09-13, shown as £69.25	6925
2	daily_sales	run-034, build_daily_sales	the row for 2026-09-13	6925
3	clean_orders	run-033, build_clean_orders	7043, 7044, 7045, 7046, 7047	9775
3	returns, as it is now	record_return	r-205: 1 of order 7044	-1425
4	orders.jsonl, version of 09-14 01:00	the export	lines 44, 45, 46, 47, 48	9775

At 02:30:00, `returns` held `r-205` with 2 rolls, from the first version, read by `run-031`: 2850 pence less. 9775 less 2850 is 6925, Sunday's total.

Each version of the object was a different input. `run-034` used what the first version held.

The warehouse keeps no earlier state of `returns`. It could be rebuilt only because each run of `record_return` recorded which version it read, and object storage kept that version.

## "Show where Thursday's total came from."

The head of the shop's requirement is: "Show where Thursday's total came from."

Before you read on, write in the next cell what you would show.

```
what_to_show = """
What would you show?
........
"""
```

"Where it came from" could mean four things. Each needs something different.

- The rows: which rows it was made from, found by following it back row by row.
- The program: which programs made it, from lineage.
- The run: which runs made it, from the record of each run.
- The rows as they were when each run read them: a version of each input, kept and recorded.

For Thursday, the first three were met. The fourth was met for the file, read in the version current when `run-014` started. The tables were read as they are now, and every step still added up.

For Sunday, with the correction, the first three were met. The fourth was not met by `returns` as it is now. It was met only by rebuilding the table from the object versions the runs recorded.

A record of what was used does not show what was left out, which was the question about Thursday.

The requirement does not say which reading it means.

Compare these with what you wrote.

## Before Chapter 16

Thursday's £51.50 was followed back through four steps to four lines of one version of `orders.jsonl`. The orders that made it low were not among them. They showed only once the rows each run read and left out were listed.

Sunday's total did not add up from the tables as they were at 09:00 on Monday. It added up from `returns` as it was when the run started, rebuilt from object versions.

The record could not show what was made from a return after it changed, or what a change to a column would affect.

Chapter 16 asks, before a change is made, what it would affect.

- Which of your platform's tables could be read again as a run read it?
- How would you find the rows a program read and left out?
- Which of your totals were made from inputs that have changed since?

### How this differs from a real platform

- The returns, the correction and the runs are invented for the course.
- The W3C's PROV data model (a W3C Recommendation of 30 April 2013) describes provenance with entities (things), activities (which happen over a period of time and use or generate entities) and agents (which bear responsibility). Its relations include an activity using an entity, an entity generated by an activity, and one entity derived from another.
- In PROV an entity has fixed aspects, so the two versions of `r-205`'s object would be two entities.
- The shop's way of following a total back is its own: it applies the programs' conditions again to the rows.
- Some table formats keep a table's earlier states as snapshots (Chapter 2). With them, a table could be read as a run read it.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 14](chapter_14.ipynb) · [Next: Chapter 16](chapter_16.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow