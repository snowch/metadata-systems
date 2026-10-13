# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Build the metadata interface",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 27](chapter_27.ipynb)

    # Chapter 28: Build the metadata interface

    **Objectives**

    - Build a page for one asset from the store, the collector's file, the lineage graph and the queries that Chapters 24 to 27 built.
    - Write the page's run history, and find which run a first version leaves out.
    - Choose the page's sections, and see what the page leaves out.
    - Question the requirement 'The asset page must show everything about an asset.'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 27's link, in a browser that had opened and run Chapter 27 (measured on a computer). Chapter 27's link opens this page in a new tab. Chapter 27 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 27 leaves more memory for this page.

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
    ## A page for one asset

    The page is made of sections. Each section is drawn from what the earlier chapters of Part VI built, in the shop's own versions: `description` and `owner` from the store and the owners' sources, `runs` from the collector's file, `upstream` and `downstream` from the lineage graph and the queries, `columns` from the warehouse, and `freshness` from Chapter 13's measure.

    The week is Chapter 27's, with Monday's failed run of `build_daily_sales`.

    You write one section's rows, `run_history(asset)`. `shop.interface.runs()` gives every run in the collector's file: its program, state, start, end, and the datasets it wrote. `shop.interface.writers(asset)` gives the programs the lineage graph records writing the asset.

    The next cell lists the programs that write `daily_sales`: one, `build_daily_sales`. The file holds 41 runs in all.
    """)
    return


@app.cell
def _(shop):
    print(shop.interface.writers("daily_sales"))
    print(len(shop.interface.runs()), "runs in the file")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below the one you write in holds `run_history` as it stands: it keeps the runs whose written datasets include the asset.

    Before you read on, write in the next cell whether that run history for `daily_sales` will include Monday's run.
    """)
    return


@app.cell
def _():
    expected_history = """
Will the run history include Monday's run of build_daily_sales?
........
"""
    return


@app.cell
def _(shop):
    def run_history(asset):
        return [r for r in shop.interface.runs() if asset in r["writes"]]
    return (run_history,)


@app.cell
def _(run_history, shop):
    shop.interface.check(run_history)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The check finds 6 runs, and not Monday's. Monday's run failed and wrote nothing, so the datasets it wrote are none. A run history built from what each run wrote leaves it out.

    Compare this with what you wrote.

    Change `run_history` so that it keeps the runs of the programs that write the asset, from `shop.interface.writers(asset)`. Select the cell and press **Run below**. The check finds 7 runs, the `FAIL` among them.

    ## The sections

    The next cell holds the page's sections as a list, `sections`. As it stands, it has `description`, `owner` and `runs`. The cell after it draws the page for `daily_sales`, and ends with the sections the page leaves out: `upstream`, `downstream`, `columns` and `freshness`.

    Add the sections you would want on the page, from the seven names. Select the cell and press **Run below**.
    """)
    return


@app.cell
def _():
    sections = ["description", "owner", "runs"]
    return (sections,)


@app.cell
def _(run_history, sections, shop):
    shop.interface.page("daily_sales", sections, run_history)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Everything about an asset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "The asset page must show everything about an asset."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "everything" means to you here.
    """)
    return


@app.cell
def _():
    what_everything_means = """
What does "everything about an asset" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "Everything" could mean three things, and each needs something different.

    - every section the shop can draw: the seven names, all on one page;
    - everything a person asking about the asset needs: the sections that answer their question. Who to ask about `daily_sales` needs `owner`; why its latest day is Saturday 12 needs `runs` and `freshness`;
    - the asset's whole history: every run and every claim, which grows every night.

    The page draws the sections you chose and names the ones it leaves out, so whoever reads it can tell what it does not show.

    The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 29

    The page took its sections from the store, the collector's file, the lineage graph and the queries of Chapters 24 to 27. A run history built from what each run wrote left out Monday's failed run, which wrote nothing. Built from the programs that write the asset, the run history held all 7 runs. The page named the sections it left out.

    Part VI ends here. Chapter 29 starts Part VII, where real producers and a real consumer of OpenLineage events meet the shop's own collector.

    - Which runs does your catalogue's history of an asset leave out?
    - Which sections of your asset pages does anyone read?
    - What does your asset page not show, and does it say so?

    ### How this differs from a real platform

    - The shop's page is drawn in these cells from the shop's own code, for one asset at a time.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 27](chapter_27.ipynb)

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
