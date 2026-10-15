# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Provenance",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 14](chapter_14.ipynb) · [Next: Chapter 16](chapter_16.ipynb)

    # Chapter 15: Provenance

    **Objectives**

    - Follow Thursday's total on the dashboard back to the lines of the file it came from.
    - Find what a record of a total's sources leaves out.
    - Check whether Sunday's total adds up from the shop's tables, and find what it adds up from.
    - Question the requirement "Show where Thursday's total came from."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 14's link, in a browser that had opened and run Chapter 14 (measured on a computer). Chapter 14's link opens this page in a new tab. Chapter 14 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 14 leaves more memory for this page.

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
    ## Thursday's £51.50

    Chapter 2 began with the head of the shop's message: "Thursday's revenue looks wrong." The dashboard shows £51.50 for Thursday 10.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which orders you expect £51.50 to be made of.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next cell follows Thursday's total back, one step at a time, from the dashboard to the file. At each step it lists the asset, the run that made it, the rows it found, and their total in pence.
    """)
    return


@app.cell
def _(shop):
    week15 = shop.run_week()
    shop.provenance.trace(week15, "2026-09-10")
    return (week15,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Thursday's total goes back through four steps.

    1. The dashboard's value for Thursday, £51.50, drawn by `run-028`, `refresh_dashboard`, early on Monday 14.
    2. The row of `daily_sales` for Thursday, written by `run-015`, `build_daily_sales`, early on Friday 11.
    3. The rows of `clean_orders` for orders 7020, 7022, 7024 and 7026, as the table holds them now. The table was last written by `run-026` early on Monday 14. `run-015` read the table after `run-014` wrote it early on Friday 11. The shop's warehouse keeps no earlier state of a table, so the rows `run-015` read are not kept. The rows now add up to the same total.
    4. Lines 21, 23, 25 and 27 of `orders.jsonl`, in the version the export wrote at 01:00:41 on Friday 11. The shop's object storage keeps every version of a file, with the time it was written. This version is the last one before `run-014` started. `run-014` did not record which version it read. The time is how the version is chosen.

    Each step adds up to 5150 pence.

    Information about where a piece of data came from and how it was made is its **provenance**.

    The total is made from four orders together; none of them alone is where it came from.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What the record leaves out

    Thursday's total is low because three orders were left out (Chapter 2). The four steps list only the rows the total was made from.

    The next cell follows the total back again with `dropped=False`. Change it to `dropped=True`. Before you press **Run below**, decide what reason the steps will give for each of orders 7021, 7023 and 7025. Then select the cell and press **Run below**.
    """)
    return


@app.cell
def _(shop, week15):
    shop.provenance.trace(week15, "2026-09-10", dropped=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `dropped=True`, three more rows list lines 22, 24 and 26 of the same version of `orders.jsonl`: orders 7021, 7023 and 7025, each with `customer_id IS NOT NULL is false`, together 15400 pence. `run-014` read them and left them out.

    They are found by applying `build_clean_orders`'s conditions again to each line of that version.

    A record of what a total was made from lists what was used. Why Thursday's total is low is in what was not used, and that needs the rows each run read and the condition that left each out.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sunday's total

    The next week has the change `corrected`. From Saturday's row on, `build_daily_sales` takes away what was returned, through the SQL function `returned_quantity`, which reads the table `returns` (Chapter 10).

    On Sunday 13 at 18:10 the returns desk records `r-205`: 2 rolls of bar tape back from order 7044. Early on Monday 14, at 02:30, `build_daily_sales` writes Sunday's row. At 08:40 on Monday the desk corrects `r-205` to 1 roll.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide whether you expect Sunday's total to add up from the shop's tables as they are at 09:00 on Monday, and why.
    """), kind="info")
    return


@app.cell
def _(shop):
    week15c = shop.run_week(["corrected"])
    shop.provenance.trace(week15c, "2026-09-13")
    return (week15c,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dashboard and `daily_sales` show 6925 pence for Sunday.

    The five Sunday orders in `clean_orders`, 7043 to 7047, add up to 9775 pence. `returns`, as it is now, holds `r-205` with 1 roll of order 7044, written by `run-036`, `record_return`, after the correction: 1425 pence less. Together, these come to 8350 pence.

    8350 is not 6925. Sunday's total does not add up from the tables as they are now.

    The next cell lists every version of `r-205`'s object.
    """)
    return


@app.cell
def _(shop, week15c):
    shop.provenance.object_versions(week15c, "r-205")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `r-205`'s object has two versions. The first, at 18:10 on Sunday, has quantity 2. The second, at 08:40 on Monday, has quantity 1.

    `run-034`, the run of `build_daily_sales` that wrote Sunday's row, started at 02:30 on Monday, between the two.

    In the next cell, change `as_read=False` to `as_read=True`, select the cell and press **Run below**. With `as_read=True`, the cell rebuilds `returns` as it was when `run-034` started, from the versions of the objects that the runs of `record_return` read.
    """)
    return


@app.cell
def _(shop, week15c):
    shop.provenance.trace(week15c, "2026-09-13", as_read=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The rebuilt `returns`, as at 02:30:00 on Monday, holds `r-205` with 2 rolls, from the first version, which `run-031` read: 2850 pence less. 9775 less 2850 is 6925, Sunday's total.

    The shop does not record that `run-034` read `returns`: the function's read is in no record (Chapter 10). That the rebuilt table gives 6925 is the evidence that `run-034` used what the first version held.

    The shop's warehouse keeps no earlier state of `returns`. It could be rebuilt only because each run of `record_return` recorded which version it read, and the shop's object storage kept that version.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Four meanings of a total's origin
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement is: "Show where Thursday's total came from."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what you would show.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "where it came from"</summary>

    "Where it came from" could mean four things. Each needs something different.

    - The rows: which rows it was made from, found by following it back row by row.
    - The program: which programs made it, from lineage.
    - The run: which runs made it, from the record of each run.
    - The rows as they were when each run read them: a version of each input, kept and recorded.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For Thursday, the first three were met. For the fourth: the file's version was kept by the shop's object storage and chosen by the time `run-014` started, but `run-014` did not record it; the tables were read as they are now, and every step still added up.

    For Sunday, with the correction, the first three were met. The fourth was not met by `returns` as it is now. It was met only by rebuilding the table from the object versions the runs of `record_return` recorded.

    None of the four readings asks for the rows each run read and left out.

    The requirement does not say which reading it means.

    Compare these with what you decided.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 16

    Thursday's £51.50 was followed back through four steps to four lines of one version of `orders.jsonl`. The orders that made it low were not among them. They showed only once the rows each run read and left out were listed.

    Sunday's total did not add up from the tables as they were at 09:00 on Monday. It added up from `returns` as it was when the run started, rebuilt from object versions.

    The record could not show what was made from a return after it changed, or what a change to a column would affect.

    Chapter 16 asks, before a change is made, what it would affect.

    - Which of your platform's tables could be read again as a run read it?
    - How would you find the rows a program read and left out?
    - Which of your totals were made from inputs that have changed since?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    - The returns, the correction and the runs are invented for the course.
    - The W3C's PROV data model (a W3C Recommendation of 30 April 2013) describes provenance with entities (things), activities (which happen over a period of time and use or generate entities) and agents (which bear responsibility). Its relations include an activity using an entity, an entity generated by an activity, and one entity derived from another.
    - PROV calls an entity a thing "with some fixed aspects" (PROV-DM's words). By that, the two versions of `r-205`'s object would be two entities.
    - The shop's way of following a total back is its own: it applies the programs' conditions again to the rows.
    - Some table formats keep a table's earlier states as snapshots (Chapter 2). With them, a table could be read as a run read it.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 14](chapter_14.ipynb) · [Next: Chapter 16](chapter_16.ipynb)

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
