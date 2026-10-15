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
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 27](chapter_27.ipynb) · [Next: Chapter 29](chapter_29.ipynb)

    # Chapter 28: Build the metadata interface

    **Objectives**

    - Build a page for one asset from the shop's versions of the pieces Chapters 24 to 27 built, and from the shop's other records.
    - Write the page's run history, and find which run a first version leaves out.
    - Choose the page's sections, and see what the page leaves out.
    - Question the requirement "The asset page must show everything about an asset."
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
    ## A page for one asset

    The page is made of sections. Each section takes its rows from:

    - `description`: the store (Chapter 24), which holds Chapter 4's lines;
    - `owner`: the three owners' sources (Chapter 27);
    - `runs`: the collector's file (Chapter 25);
    - `upstream` and `downstream`: the lineage graph and the queries (Chapters 26 and 27);
    - `columns`: the warehouse;
    - `freshness`: Chapter 13's measure.

    The pieces from Chapters 24 to 27 are the shop's own versions, not your code.

    The week is Chapter 27's, with Monday's failed run of `build_daily_sales`.

    You write one section's rows, `run_history(asset)`, and the list of sections.

    `shop.interface.runs()` gives every run in the collector's file: its program, state, start, end, and the datasets it wrote. `shop.interface.writers(asset)` gives the programs the lineage graph records writing the asset.

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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide whether that run history for `daily_sales` will include Monday's run.
    """), kind="info")
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
    <details><summary>The printed result, explained</summary>

    The check finds 6 runs, and not Monday's.

    Monday's run failed and wrote nothing, so a run history built from what each run wrote leaves it out.

    Compare this with what you decided.

    </details>

    Change `run_history` so that it keeps the runs of the programs that write the asset, from `shop.interface.writers(asset)`. Select the cell and press **Run below**.

    <details><summary>The printed result, explained</summary>

    The check finds 7 runs, the `FAIL` among them.

    </details>

    ## The sections

    Jo Marsh opens this page on Monday morning to find out why `daily_sales` ends on Saturday 12.

    The next cell holds the page's sections as a list, `sections`. As it stands, it has `description`, `owner` and `runs`.

    `description` holds Chapter 4's lines, which name the person responsible; `owner` puts that person beside the other two owners.

    The cell after it draws the page for `daily_sales`, and ends with the sections the page leaves out: `upstream`, `downstream`, `columns` and `freshness`. A name that is not one of the seven is listed as one the page cannot draw.

    Add the sections Jo Marsh's question needs, from the seven names. Select the cell and press **Run below**.
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
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "everything" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "everything"</summary>

    "Everything" could mean three things, and each needs something different.

    - every section the shop can draw: all seven names in the list. That meets this reading, and shows nothing more about the asset than the sections themselves hold.
    - everything a person asking about the asset needs: the sections that answer their question. Who to ask about `daily_sales` needs `owner`; why its latest day is Saturday 12 needs `runs` and `freshness`.
    - the asset's whole history: every run and every earlier value, which grows every night. No list of sections meets it: `runs` holds this week's 7 runs, and `description` holds one record for each asset.

    The page's last line names which of the seven sections are not drawn. It cannot show what a drawn section leaves out, such as an earlier value or why a run failed.

    The page meets a reading only through the sections chosen for it.

    The requirement does not say which it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 29

    The page took its sections from the shop's versions of the pieces Chapters 24 to 27 built, and from the warehouse and Chapter 13's measure.

    A run history built from what each run wrote left out Monday's failed run, which wrote nothing. Built from the programs that write the asset, it held all 7 runs.

    That history is complete only for programs the graph records writing the asset. A program whose every run failed would write nothing, so the graph would hold no edge from it to the asset, and `writers` would not list it.

    The page named the sections it left out, but not what a drawn section leaves out.

    Part VI ends here. Chapter 29 starts Part VII, where real producers and a real consumer of OpenLineage events meet the shop's own collector.

    - Which runs does your catalogue's history of an asset leave out?
    - Which sections of your asset pages does anyone read?
    - What does your asset page not show, and does it say so?

    ### How this differs from a real platform

    - The shop's page is drawn in these cells, for one asset at a time, from a file read whole. A real catalogue's page reads a store that changes as events arrive.
    - The shop's failed run sends a `FAIL` with no output (Chapter 8). That is the shop's choice: in the OpenLineage specification, any run event may list outputs, a `FAIL` among them, and none must.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 27](chapter_27.ipynb) · [Next: Chapter 29](chapter_29.ipynb)

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
