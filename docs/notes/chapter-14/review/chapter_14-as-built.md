[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 13](chapter_13.ipynb) · [Next: Chapter 15](chapter_15.ipynb)

# Chapter 14: Data quality as metadata

**Objectives**

- Read what each run of `build_clean_orders` counted in the file it read.
- Test a rule against every run, and find why it passed on every night.
- Set the rows each run read against the rows it wrote.
- Question the requirement "No order without a customer."

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 13's link, in a browser that had opened and run Chapter 13 (measured on a computer). Chapter 13's link opens this page in a new tab. Chapter 13 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 13 leaves more memory for this page.

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

## What each run counted

Chapter 13's observations recorded how many rows each run read and wrote. They did not show what those rows held.

Each run of `build_clean_orders` now also counts four things as it runs, in the file it read (`orders.jsonl`) and in the table it wrote (`clean_orders`):

- `rows`: the rows.
- `no customer_id`: the rows with no customer id.
- `order_id twice`: the rows beyond the first with the same order id.
- `quantity 0 or less`: the rows with a quantity of 0 or less.

The next cell lists the counts for `orders.jsonl`, run by run. `orders up to` is the last day of orders the night's file holds.

```
week14 = shop.run_week()
shop.quality.measurements(week14, "orders.jsonl")
```

OUTPUT:
run	night	orders up to	dataset	rows	no customer_id	order_id twice	quantity 0 or less
run-002	2026-09-08	2026-09-07	orders.jsonl	6	0	0	0
run-006	2026-09-09	2026-09-08	orders.jsonl	13	0	0	0
run-010	2026-09-10	2026-09-09	orders.jsonl	20	0	1	0
run-014	2026-09-11	2026-09-10	orders.jsonl	27	3	1	0
run-018	2026-09-12	2026-09-11	orders.jsonl	35	3	1	0
run-022	2026-09-13	2026-09-12	orders.jsonl	43	3	1	0
run-026	2026-09-14	2026-09-13	orders.jsonl	48	3	1	0

The file grows each night, because each export holds every order so far: 6 rows on Tuesday 8, 48 on Monday 14.

From Thursday 10, `order_id twice` is 1. One order appears twice in the file, and it stays twice.

From Friday 11, `no customer_id` is 3. These are Thursday's three orders with no customer id (Chapter 2). They stay in every later file.

`quantity 0 or less` is 0 on every run.

Whether data is fit for the use made of it is its **data quality**. Counts like these, recorded by each run, are measurements of it.

## A rule tested on every run

The head of the shop's requirement is: "No order without a customer."

The shop's developer writes it as a rule tested on every run of `build_clean_orders`: in `clean_orders`, `no customer_id` must be at most 0.

A rule that a measurement must meet on every run, with whether it held recorded, is an **assertion**.

Before you read on, write in the next cell which runs you expect to fail the assertion, and why.

```
expected_failures = """
Which runs do you expect to fail the assertion, and why?
........
"""
```

```
dataset = "clean_orders"
shop.quality.check(week14, dataset, "no customer_id")
```

OUTPUT:
run	night	dataset	no customer_id	at most	passed
run-002	2026-09-08	clean_orders	0	0	yes
run-006	2026-09-09	clean_orders	0	0	yes
run-010	2026-09-10	clean_orders	0	0	yes
run-014	2026-09-11	clean_orders	0	0	yes
run-018	2026-09-12	clean_orders	0	0	yes
run-022	2026-09-13	clean_orders	0	0	yes
run-026	2026-09-14	clean_orders	0	0	yes

It passed on all 7 runs.

`build_clean_orders` drops every order with no customer id before it writes the table. Its rule is `customer_id IS NOT NULL` (Chapter 2). The assertion tests the table after that rule, so it finds no such order on any night. While the rule stays, this assertion cannot fail.

Change `dataset = "clean_orders"` to `dataset = "orders.jsonl"`. Before you press **Run below**, decide which runs will fail. Then select the cell and press **Run below**.

On `orders.jsonl`, 4 runs fail: Friday 11, Saturday 12, Sunday 13 and Monday 14, each with a count of 3. Tuesday 8 to Thursday 10 pass: their files hold no order of Thursday's.

Each of the four runs counts 3. The count does not show whether they are the same 3 orders.

## Rows read and rows written

A third test sets what each run read against what it wrote.

The next cell lists, for each run, the rows it read and wrote, the rows that repeat an order, and the rows it left out beyond those. The assertion here: `left out` is 0.

```
shop.quality.reconcile(week14)
```

OUTPUT:
run	night	rows read	rows written	repeats	left out	passed
run-002	2026-09-08	6	6	0	0	yes
run-006	2026-09-09	13	13	0	0	yes
run-010	2026-09-10	20	19	1	0	yes
run-014	2026-09-11	27	23	1	3	no
run-018	2026-09-12	35	31	1	3	no
run-022	2026-09-13	43	39	1	3	no
run-026	2026-09-14	48	44	1	3	no

Tuesday 8 to Thursday 10 pass. On Thursday 10 the run read 20 rows and wrote 19: 1 row repeated an order, and none was left out.

From Friday 11, every run left 3 rows out. On Friday 11: 27 read, 23 written, 1 repeat, 3 left out.

This test reads both datasets of one run. It shows that the run left rows out. It does not show which rule left them out, or whether it should have.

## "No order without a customer."

Before you read on, write in the next cell what you take the requirement to mean: where must there be no order without a customer, and what should happen to one?

```
what_it_means = """
Where must there be no order without a customer,
and what should happen to one?
........
"""
```

"No order without a customer" could mean three things, each needing a different measurement:

- In the file the checkout sends: `no customer_id` in `orders.jsonl`, on every run.
- In `clean_orders`: `no customer_id` in the table, on every run.
- On the dashboard: every completed order the shop took is counted in a day's revenue, against its customer. This needs the file's orders set against the dashboard's totals.

The next cell tests each reading.

```
shop.quality.readings(week14)
```

OUTPUT:
reading	test	runs failed	met
in the file the checkout sends	no customer_id in orders.jsonl is 0	4	no
in clean_orders	no customer_id in clean_orders is 0	0	yes
on the dashboard	every completed order is counted in a day's revenue		no

- In the file: not met; 4 runs failed.
- In `clean_orders`: met on every run, because the rule removes the orders before the table is written.
- On the dashboard: not met. Thursday's total leaves out 3 completed orders, worth 15400 pence (Chapter 2).

Compare these with what you wrote. The requirement does not say which reading it means. Nor does it say what should happen to an order without a customer: dropped, kept without a customer, or the night's work stopped.

## The counts in the shop's events

OpenLineage defines two facets for this. `dataQualityMetrics` holds counts for a dataset and for each of its columns. `dataQualityAssertions` holds each assertion and whether it succeeded.

The next cell prints the input `orders.jsonl` of `run-014`, the run on Friday 11, as the shop's producer would send it with both facets.

```
import json

print(json.dumps(shop.quality.facets(week14, "run-014"), indent=2))
```

OUTPUT:
{
  "namespace": "s3://shop-raw",
  "name": "orders.jsonl",
  "facets": {
    "dataQualityMetrics": {
      "_producer": "https://example.org/shop/jobs/tree/v1",
      "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/DataQualityMetricsDatasetFacet.json#/$defs/DataQualityMetricsDatasetFacet",
      "rowCount": 27,
      "captureDate": "2026-09-11T02:05:00Z",
      "columnMetrics": {
        "customer_id": {
          "nullCount": 3
        },
        "order_id": {
          "distinctCount": 26
        }
      }
    }
  },
  "inputFacets": {
    "dataQualityAssertions": {
      "_producer": "https://example.org/shop/jobs/tree/v1",
      "_schemaURL": "https://openlineage.io/spec/facets/1-1-0/DataQualityAssertionsDatasetFacet.json#/$defs/DataQualityAssertionsDatasetFacet",
      "assertions": [
        {
          "assertion": "not_null",
          "column": "customer_id",
          "success": false,
          "expected": "0",
          "actual": "3"
        }
      ]
    }
  }
}

`rowCount` is 27. For the column `customer_id`, `nullCount` is 3: rows where it is empty. For `order_id`, `distinctCount` is 26.

The assertion is `not_null` on `customer_id`, with `success` false, `expected` 0 and `actual` 3.

Both facets go with the dataset the run read.

## Before Chapter 15

Each run of `build_clean_orders` counted four things in the file it read and the table it wrote. The assertion on `clean_orders` passed on every run, because the rule had removed the orders it was meant to find. On the file, it failed from Friday 11. Comparing the rows each run read with the rows it wrote showed 3 rows left out on every run from Friday 11.

The counts could not show which orders were left out, or where a total on the dashboard came from.

Chapter 15 follows one total on the dashboard back to the rows it was made from.

- Where do your platform's checks run: on what a program reads, or on what it writes?
- Which of your checks could not fail, because a program removes the rows first?
- What does your platform do when a check fails: stop the work, or warn?

### How this differs from a real platform

- The shop's counts, its developer's assertion and its runs are invented for the course.
- OpenLineage's `dataQualityMetrics` facet holds a row count, a size, and for each column counts such as how many values are empty and how many are distinct. Its `dataQualityAssertions` facet holds each assertion's kind, whether it succeeded and, optionally, its column, its severity and the expected and actual values.
- An assertion's severity in that facet shows whether a failure stops the work (`error`) or only warns (`warn`). The shop's assertion stops nothing: the runs that failed it still wrote their tables.
- The shop counts only what `build_clean_orders` reads and writes. A real platform counts what someone has set up a check for.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 13](chapter_13.ipynb) · [Next: Chapter 15](chapter_15.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow