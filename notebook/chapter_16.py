# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Impact analysis",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 15](chapter_15.ipynb) · [Next: Chapter 17](chapter_17.ipynb)

    # Chapter 16: Impact analysis

    **Objectives**

    - Ask the shop's lineage what renaming a column would affect, by dataset and by column.
    - Compare its answers with what each reader produced after the rename.
    - Find what the shop made from a return that was withdrawn.
    - Question the requirement "Tell us what breaks if `customer_id` is renamed."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 15's link, in a browser that had opened and run Chapter 15 (measured on a computer). Chapter 15's link opens this page in a new tab. Chapter 15 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 15 leaves more memory for this page.

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
    3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser. When the chapter is updated, the page shows the new version instead. If you changed a cell, your copy is kept under the chapter's name with "(your copy)" added, and [the list of files in this browser](https://snowch.github.io/metadata-systems/jupyterlite/tree/) opens it.
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
    ## A column to rename

    The shop's developer wants to rename the column `customer_id` of `clean_orders` to `customer`. The change would take effect from the night's work early on Sunday 13. `build_clean_orders` would write the column as `customer`, and the warehouse would rename it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop asks: "Tell us what breaks if `customer_id` is renamed."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three readers of `clean_orders` are known from earlier chapters:

    - `build_daily_sales`, which writes `daily_sales`, which the dashboard shows;
    - the analyst's script, `copy_clean_orders`, which copies `clean_orders` every night to `clean_orders_copy.csv` in the bucket `shop-scratch` and sends events (Chapters 6 and 9);
    - Jo Marsh's query, which joins `clean_orders` to `clean_customers` on `customer_id` in a spreadsheet and sends no events (Chapter 11).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which of `daily_sales`, the dashboard, the analyst's copy and Jo Marsh's query you expect to break, and how.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What the lineage lists

    The next cell follows lineage by datasets, the graph that the week's events make (Chapter 9), downstream from `clean_orders`, in a week with the analyst's script.
    """)
    return


@app.cell
def _(shop):
    week16 = shop.run_week(["copy"])
    shop.impact.downstream(week16, "clean_orders")
    return (week16,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 1 is the programs that read `clean_orders`: `copy_clean_orders` writes `clean_orders_copy.csv`, and `build_daily_sales` writes `daily_sales`. Step 2 is the programs that read what step 1 wrote: `refresh_dashboard` writes `sales_dashboard`.

    Following lineage from a change to find what the change may affect is **impact analysis**. By datasets, everything downstream of `clean_orders` may be affected.

    The next cell follows column lineage (Chapter 10) downstream from one column, `customer_id` of `clean_orders`.
    """)
    return


@app.cell
def _(shop, week16):
    shop.impact.downstream_columns(week16, "clean_orders", "customer_id")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell lists one column: `customer_id` of `clean_orders_copy.csv`, which `copy_clean_orders` copies.

    `build_daily_sales` does not read `customer_id`. It reads `ordered_at`, `price_pence`, `quantity` and `status` (Chapter 10).

    Change `"customer_id"` to `"status"`, select the cell and press **Run below**: the cell lists every column downstream of `status`. Then change it back.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `"status"`, the cell lists `day` and `revenue_pence` of `daily_sales`. `status` decides which rows count there: it is the filter in `build_daily_sales`. The cell also lists `status` of the copy, and `day` and `revenue_pence` of `sales_dashboard`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## After the rename

    The next cell runs the week again with the rename, and sets what each reader produced on Monday morning beside the week above.
    """)
    return


@app.cell
def _(shop, week16):
    shop.impact.readers(week16, shop.run_week(["copy", "customer"]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `daily_sales` and the dashboard are unchanged: 7 rows, 100798 pence, and the same seven values.
    - The analyst's copy: its first line, the names of its columns, now names the column `customer`. The script ran and succeeded.
    - Jo Marsh's query: before, 7 rows, one for each country, 41 orders; after, the error `no such column: o.customer_id`.

    Compare these with what you decided.

    By datasets, the lineage listed `daily_sales` and the dashboard, which did not change. Column lineage listed the copy's column, which now has another name, with no error. Neither listed Jo Marsh's query, which failed: it sends no events, and the shop does not have its code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A return withdrawn

    The next week has the change `withdrawn`. On Sunday 13 at 21:15 the returns desk records `r-206`, the return of the brake pads from order 7047. Early on Monday 14 at 02:30, `build_daily_sales` writes Sunday's row, less what was returned. At 08:50 on Monday the desk withdraws `r-206` and deletes its object, and `remove_return` removes its row from `returns`.

    What did the shop make from `r-206`? Before you run the next cell, decide what the graph will list downstream of its object.
    """)
    return


@app.cell
def _(shop):
    week16w = shop.run_week(["withdrawn"])
    shop.impact.downstream(week16w, "s3://shop-returns/r-206.json")
    return (week16w,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lineage by datasets lists one step: `record_return` writes `returns`.

    According to the events, no program reads `returns`. `build_daily_sales` reads it only through the SQL function `returned_quantity`, and its events do not name the table (Chapter 10).

    The next cell checks every run of `build_daily_sales` whose code calls `returned_quantity` against what `returns` held when that run started (Chapter 15).
    """)
    return


@app.cell
def _(shop, week16w):
    shop.impact.made_from(week16w, "r-206")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The row for `r-206` in `returns`, written by `run-031` (`record_return`), is no longer there.

    The row for Sunday 13 in `daily_sales`, written by `run-034`, is still there. It is still 1200 pence less than Sunday's orders. It holds 8575 pence, and Sunday's five orders add up to 9775 pence.

    The dashboard still shows £85.75 for Sunday 13.

    Nothing failed. Every run succeeded, and Sunday's total counts a return the desk withdrew.

    `daily_sales` is appended to. No run writes Sunday's row again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Tell us what breaks if `customer_id` is renamed."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what you take "breaks" to mean.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "breaks"</summary>

    "Breaks" could mean two things, each needing something different:

    - fails: a program or a query stops with an error. This needs every reader that names the column, whether or not it is in the shop's records.
    - keeps running and gives a different answer: a reader gets other rows, other values or another column name, with no error. This needs the readers of the column, and what each does with it.

    By reading, for the rename:

    - fails: not met. Jo Marsh's query failed, and no record names it.
    - keeps running with a different answer: met for the copy, whose column lineage the shop has. Lineage by datasets also listed `daily_sales` and the dashboard, which did not change.

    The requirement does not say which meaning of "breaks" it wants.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 17

    Lineage by datasets listed everything downstream of `clean_orders`, and two of the datasets it listed did not change. Column lineage listed the copy's column. Neither kind of lineage listed Jo Marsh's query, which failed.

    A withdrawn return left Sunday's row of `daily_sales` and the dashboard 1200 pence low, and lineage by datasets followed it no further than `returns`.

    Chapter 17 starts from a wrong total and follows it back to where it went wrong.

    - Which readers of your most-used table are in no record?
    - Which of your tables are appended to, so that a change to an input never reaches rows already written?
    - What would your platform list if you asked what a deleted record was used for?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    - The rename, the withdrawn return, the analyst's script and Jo Marsh's query are invented for the course.
    - The shop's lineage by datasets holds only what its producers send, and its column lineage only what its parser reads in the code the shop has (Chapters 9 and 10).
    - OpenLineage's column lineage facet (Chapter 10) is what would carry, in events, the column lineage that the shop follows here.
    - That `daily_sales` is appended to, not rebuilt, is the shop's own design.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 15](chapter_15.ipynb) · [Next: Chapter 17](chapter_17.ipynb)

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
