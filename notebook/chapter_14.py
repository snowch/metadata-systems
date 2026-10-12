# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Data quality as metadata",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 13](chapter_13.ipynb) · [Next: Chapter 15](chapter_15.ipynb)

    # Chapter 14: Data quality as metadata

    **Objectives**

    - Read what each run of `build_clean_orders` counted in the file it read.
    - Test one expectation about the orders on every run, against the table and against the file.
    - Set the rows each run read against the rows it wrote.
    - Question the requirement "No order without a customer."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 13's link, in a browser that had opened and run Chapter 13 (measured on a computer). Chapter 13's link opens this page in a new tab. Chapter 13 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 13 leaves more memory for this page.

    Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

    </details>
    """), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    **Running and saving the page**

    1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
    2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
    3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, shop):
    mo.Html(figures.figure(figures.pipeline(shop.run_week(["returns"]), "jobs nightly; functions at any hour"), "The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table `returns`."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What each run counted

    Chapter 13's observations recorded how many rows each run read and wrote. They did not show what those rows held.

    Each run of `build_clean_orders` now also counts four things as it runs, in the file it read (`orders.jsonl`) and in the table it wrote (`clean_orders`):

    - `rows`: the rows.
    - `no customer_id`: the rows with no customer id.
    - `order_id twice`: the rows beyond the first with the same order id.
    - `quantity 0 or less`: the rows with a quantity of 0 or less.

    The next cell lists the counts for `orders.jsonl`, run by run. `orders up to` is the last day of orders the night's file holds.
    """)
    return


@app.cell
def _(shop):
    week14 = shop.run_week()
    shop.quality.measurements(week14, "orders.jsonl")
    return (week14,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The file grows each night, because each export holds every order so far: 6 rows on Tuesday 8, 48 on Monday 14.

    From Thursday 10, `order_id twice` is 1: one order appears twice in the file, and stays twice.

    From Friday 11, `no customer_id` is 3: Thursday's three orders with no customer id (Chapter 2). They stay in every later file.

    `quantity 0 or less` is 0 on every run: no order in the week has one (Chapter 2).

    Whether data is fit for the use made of it is its **data quality**. These counts are observations (Chapter 13) of the data each run read and wrote, and they measure its data quality.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "No order without a customer."

    The head of the shop's requirement is: "No order without a customer."

    Before you read on, write in the next cell what you take it to mean: where must there be no order without a customer, and what should happen to one?
    """)
    return


@app.cell
def _():
    what_it_means = """
Where must there be no order without a customer,
and what should happen to one?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A test on every run

    The shop's developer writes the requirement as a test on every run of `build_clean_orders`: in `clean_orders`, `no customer_id` must be at most 0.

    A stated expectation about data, with a record of whether it held in each run, is an **assertion**.

    Before you read on, write in the next cell which runs you expect to fail the assertion, and why.
    """)
    return


@app.cell
def _():
    expected_failures = """
Which runs do you expect to fail the assertion, and why?
........
"""
    return


@app.cell
def _(shop, week14):
    dataset = "clean_orders"
    shop.quality.check(week14, dataset, "no customer_id")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It passed on all 7 runs.

    `build_clean_orders` drops every order with no customer id before it writes the table. Its rule is `customer_id IS NOT NULL` (Chapter 6, where you read its code). The assertion tests the table after that rule, so it finds no such order on any night. While the rule stays, this assertion cannot fail.

    Change `dataset = "clean_orders"` to `dataset = "orders.jsonl"`, select the cell and press **Run below**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On `orders.jsonl`, 4 runs fail: Friday 11, Saturday 12, Sunday 13 and Monday 14, each with a count of 3. Tuesday 8 to Thursday 10 pass: their files hold no order of Thursday's.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rows read and rows written

    Could a run's own counts show that it left rows out, whatever left them out?

    The next cell lists, for each run, the rows it read and wrote, the rows that repeat an order, and the rows it left out beyond those. Another assertion: `left out` is 0.
    """)
    return


@app.cell
def _(shop, week14):
    shop.quality.reconcile(week14)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tuesday 8 to Thursday 10 pass. On Thursday 10 the run read 20 rows and wrote 19: 1 row repeated an order, and none was left out.

    From Friday 11, every run left 3 rows out. On Friday 11: 27 read, 23 written, 1 repeat, 3 left out.

    This test reads both datasets of one run. It shows that the run left rows out. It does not show which rule left them out, or whether it should have.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Three readings

    "No order without a customer" could mean three things, each needing a different measurement:

    - In the file the checkout sends: `no customer_id` in `orders.jsonl`, on every run.
    - In `clean_orders`: `no customer_id` in the table, on every run.
    - On the dashboard: every completed order the shop took is counted in a day's revenue. This needs the file's orders set against the dashboard's totals. No run records it, so the next cell leaves its `runs failed` empty.

    The next cell tests each reading.
    """)
    return


@app.cell
def _(shop, week14):
    shop.quality.readings(week14)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - In the file: not met; 4 runs failed.
    - In `clean_orders`: met on every run, because the rule removes the orders before the table is written.
    - On the dashboard: not met. Thursday's total leaves out 3 completed orders, worth 15400 pence (Chapter 2).

    Compare these with what you wrote at the start. The requirement does not say which reading it means. Nor does it say what should happen to an order without a customer: dropped, kept without a customer, or the night's work stopped.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The counts as OpenLineage facets

    OpenLineage defines two facets for this: `dataQualityMetrics`, counts for a dataset and for each of its columns; and `dataQualityAssertions`, each assertion and whether it succeeded.

    The shop's events do not carry them. The next cell builds them for the input `orders.jsonl` of `run-014`, the run on Friday 11, as the shop's producer would send it.
    """)
    return


@app.cell
def _(shop, week14):
    import json

    print(json.dumps(shop.quality.facets(week14, "run-014"), indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `rowCount` is 27. For the column `customer_id`, `nullCount` is 3: the rows with no customer id. For `order_id`, `distinctCount` is 26: the 27 rows less the 1 repeat. No field holds `quantity 0 or less`.

    The assertion is `not_null` on `customer_id`, with `success` false, `expected` 0 and `actual` 3.

    Both facets go with the dataset the run read.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 15

    Each run of `build_clean_orders` counted four things in the file it read and the table it wrote. The assertion on `clean_orders` passed on every run, because the rule had removed the orders it was meant to find. On the file, it failed from Friday 11. Comparing the rows each run read with the rows it wrote showed 3 rows left out on every run from Friday 11.

    "No order without a customer" was met in `clean_orders`, not in the file and not on the dashboard, and the requirement does not say which it means.

    The counts could not show which orders were left out, or where a total on the dashboard came from.

    Chapter 15 follows one total on the dashboard back to the rows it was made from.

    - Where do your platform's checks run: on what a program reads, or on what it writes?
    - Which of your checks could not fail, because a program removes the rows first?
    - What does your platform do when a check fails: stop the work, or warn?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    - The shop's counts, its developer's assertion and its runs are invented for the course.
    - OpenLineage's `dataQualityMetrics` facet holds a row count, a size, and for each column counts such as how many values are empty and how many are distinct. Its `dataQualityAssertions` facet holds each assertion's kind, whether it succeeded and, optionally, its column, its severity and the expected and actual values.
    - An assertion's severity in that facet shows whether a failure stops the work (`error`) or only warns (`warn`). The shop's assertion stops nothing: the runs that failed it still wrote their tables.
    - The shop counts only what `build_clean_orders` reads and writes. A real platform counts what someone has set up a check for.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 13](chapter_13.ipynb) · [Next: Chapter 15](chapter_15.ipynb)

    ---

    Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow
    """)
    return


@app.cell(hide_code=True)
def _(shop):
    week = shop.run_week()
    storage, warehouse, reporting = week.storage, week.warehouse, week.reporting
    return reporting, storage, warehouse, week


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import shop
    from shop import figures
    return figures, mo, shop


if __name__ == "__main__":
    app.run()
