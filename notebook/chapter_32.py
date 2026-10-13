# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Metadata for ML and AI",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 31](chapter_31.ipynb)

    # Chapter 32: Metadata for ML and AI

    **Objectives**

    - Record a forecast trained on `daily_sales` with the fields an experiment tracker keeps.
    - Find what the run's record can tell you about the rows the forecast was trained on, and what it cannot.
    - Test a guess about those rows against the record's digest.
    - Question the requirement "Record the training data of the model."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 31's link, in a browser that had opened and run Chapter 31 (measured on a computer). Chapter 31's link opens this page in a new tab. Chapter 31 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 31 leaves more memory for this page.

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
    ## A forecast and its record

    On Saturday 12 at 09:00 the shop trains a forecast of the next day's revenue: the mean of the last 3 days in `daily_sales`. It comes to 13650 pence.

    The run is recorded with the fields MLflow, an experiment tracker, keeps for a run's input: its `name`, `digest`, `source`, `schema` and `profile`, and the context `training`.

    The forecast is registered as version 1 of `next_day_revenue`, and the version names the run that made it.

    The next cell lists the record of the run's input, one field on each row.
    """)
    return


@app.cell
def _(shop):
    week32 = shop.run_week(["returns"])
    shop.ml.record(week32)
    return (week32,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The digest is a short fingerprint of the rows. MLflow computes it from the first 10,000 rows, the number of rows and the column names, through MD5, and keeps 8 characters.

    The shop computes its digest the same way from its own rows. It is the shop's value, not MLflow's, because MLflow reads the rows with a library the shop does not use.

    The profile holds the number of rows: 5.

    On Monday 14 at 09:00, Jo Marsh asks which rows the forecast was trained on.

    Before you read on, write in the next cell whether the run's record can tell you.
    """)
    return


@app.cell
def _():
    expected_rows = """
Can the run's record tell you which rows the forecast was trained on?
........
"""
    return


@app.cell
def _(shop, week32):
    shop.ml.today(week32)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell above sets the run's record beside `daily_sales` on Monday 14 at 09:00. The record has 5 rows and the digest `60ba54ee`. The table has 7 rows and the digest `6b0727dc`.

    The record lists no rows. It holds a name, a digest and a count. The digests differ, so the table has changed since the run.

    Compare this with what you wrote.

    Each night's run of `build_daily_sales` adds one row, for the day before, and leaves the other rows as they are. So the rows the forecast read may still be in the table.

    The record can test that guess: the right rows give the same digest.

    The next cell holds `where`, a condition on the rows of `daily_sales`. As it stands, `day <= '2026-09-13'` keeps all 7.

    Change the date so that the condition keeps the rows the table held on Saturday 12 at 09:00. Select the cell and press **Run below**. The check below it computes the digest of the rows your condition keeps.
    """)
    return


@app.cell
def _():
    where = "day <= '2026-09-13'"
    return (where,)


@app.cell
def _(shop, week32, where):
    shop.ml.check(week32, where)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the date of Friday 11, the check passes: 5 rows give the digest `60ba54ee`, the one the run recorded.

    A match is strong evidence, not proof: with 8 characters, other rows could give the same digest, though the chance is small.

    ## What a digest reads

    The digest reads only the first 10,000 rows, with the row count.

    The next cell takes a table of 10,001 rows made for this cell, and changes one row at a time by 1 penny.
    """)
    return


@app.cell
def _(shop):
    shop.ml.cap()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Changing the first row changes the digest, from `b54985ab` to `ebf8f1e4`. Changing row 10,001, the last, leaves it at `b54985ab`.

    A digest shows a change only within the rows it reads.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The training data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Record the training data of the model."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "record the training data" means to you here.
    """)
    return


@app.cell
def _():
    what_training_data_means = """
What does "record the training data" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It could mean three things. Each item says what it needs:

    - the snapshot the forecast read: a version or a time of the table, and a table that keeps its earlier states, as the table formats in Chapter 2's closing note do;
    - the query that chose the rows: its text and when it ran. The same text run on Monday reads 7 rows, not 5;
    - the features computed from the rows: the code that computed them and the values it gave, here the last 3 days' revenue.

    The tracker's record meets a narrower reading: which table, and whether it has changed since. The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 33

    The run's record held a name, a digest and a count, not the rows. The digest showed the table had changed since the run, and a guess about the rows could be tested against it.

    A digest that reads the first 10,000 rows did not change when a later row did.

    The page could not show the evaluation of the forecast, where it was used, or what it predicted: each would need its own record.

    Part VII ends here. Chapter 33 asks you to build the whole thing on a second platform you have not seen.

    Ask three questions:

    - Which version of the data did your last training run read?
    - Could you rebuild that data from what your tracker recorded?
    - What does your digest, or your checksum, read, and what does it leave out?

    ### How this differs from a real platform

    - The forecast is a mean of 3 numbers, made so that there is a run to record. A real training run reads far more rows, and its record holds more: settings, measures of how well it did, and the version of its code.
    - The shop's digest follows MLflow's rule, but it is not MLflow's value.
    - OpenLineage has no facet for training or evaluation. A dataset's type may be `MODEL`, so the forecast can be named as a dataset a run writes.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 31](chapter_31.ipynb)

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
