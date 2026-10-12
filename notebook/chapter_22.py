# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Identity across systems",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 21](chapter_21.ipynb) · [Next: Chapter 23](chapter_23.ipynb)

    # Chapter 22: Identity across systems

    **Objectives**

    - Read the six references that six systems make to `daily_sales`, or to a thing named like it.
    - Merge them by the last part of their names, and find what merged that should not.
    - Merge them by qualified names, then by what each system's own configuration states.
    - Question the requirement "Merge the same dataset across systems."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 21's link, in a browser that had opened and run Chapter 21 (measured on a computer). Chapter 21's link opens this page in a new tab. Chapter 21 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 21 leaves more memory for this page.

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
    ## Six references

    Chapter 12 tested pairs of references inside the warehouse and object storage. The shop's metadata system takes references from more systems than those.

    The shop's developer has started using a transformation tool. The tool names each program's output as a model in a project. The output `daily_sales` is `shop_models:daily_sales`. The reporting tool names the dataset behind the dashboard `Daily sales`. Jo Marsh exported `daily_sales` to a CSV file in `shop-scratch`.

    The next cell lists the six references, and the system each came from.
    """)
    return


@app.cell
def _(shop):
    shop.aliases.references()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    These are the six references, with the system each came from:

    - the warehouse: `shop.analytics.daily_sales`
    - the events' namespace and name: `warehouse://shop-warehouse/shop.analytics.daily_sales`
    - the development warehouse: `shop_dev.analytics.daily_sales` (Chapter 12)
    - the transformation tool: `shop_models:daily_sales`
    - the reporting tool: `dataset:Daily sales`
    - object storage: `s3://shop-scratch/daily_sales.csv`

    This is the rule for merging. Take the last part of each name, in lower case, with spaces and hyphens read as underscores, and a file's extension left off. References with the same last part become one.

    Before you read on, write in the next cell which references this rule will merge.
    """)
    return


@app.cell
def _():
    expected_merge = """
Which of the six references will this rule merge?
........
"""
    return


@app.cell
def _(shop):
    shop.aliases.merge("last part")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Under that rule, all six become one entity. Among them are the development table, which holds other rows in another environment, and Jo Marsh's CSV file, a copy made at one time.

    Deciding which references name one entity is **entity resolution**. Merging too much is as much a fault as merging too little: the development table's runs would show in production's lineage.

    In the cell, change `"last part"` to `"qualified"`. Select the cell and press **Run below**. The qualified rule reads each warehouse name by the warehouse's rules (Chapter 12), and it takes an event's namespace as the warehouse.

    The result has five entities. The warehouse's reference and the events' reference merge into one. The other four references each stay alone. The transformation tool's name and the reporting tool's name are not warehouse names.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What each system states

    The transformation tool's configuration states which table each model builds. The model `shop_models:daily_sales` builds `shop.analytics.daily_sales`. The reporting tool's configuration states which table each dataset reads. `Daily sales` reads `daily_sales`.

    Another name a system uses for an asset, stated by that system, is an **alias**.

    In the cell, change the rule to `"aliases"`. Select the cell and press **Run below**. The `aliases` rule merges by qualified names first, then by the aliases each system states.

    The result has three entities. One of them holds four references: the warehouse's, the events', the transformation tool's and the reporting tool's. The development table is alone. Jo Marsh's CSV file is alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The same dataset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Merge the same dataset across systems."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "the same dataset" means to you here.
    """)
    return


@app.cell
def _():
    what_same_means = """
What does "the same dataset" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "The same dataset" could mean four things, and each needs different information:

    - the same name: a rule for reading names, such as `last part` or `qualified`;
    - the same rows: a way to compare contents (Chapter 12);
    - the same thing to the business: someone's statement, or each system's own;
    - across environments or not: which environment holds each asset.

    The `aliases` rule merges by what each system states it reads or builds, and it keeps the environments apart. A reading of "the same thing to the business" might merge the development table too. A reading of "the same rows" might merge Jo Marsh's file on the day it was exported.

    The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 23

    Six systems name `daily_sales`, or something named like it, in six ways. The last part of each name merged all six, the development table and the copy among them. Qualified names merged two references. Adding what each system's configuration states merged four, and kept the development table and the copy apart.

    Chapter 23 asks what the shop's metadata system costs as the platform grows.

    - Which of your systems name the same table differently?
    - Where does each of your systems state what it reads or builds?
    - Which of your environments share table names?

    ### How this differs from a real platform

    - The transformation tool, its notation and the reporting tool's dataset are invented for the course.
    - The shop's rules work on six references.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 21](chapter_21.ipynb) · [Next: Chapter 23](chapter_23.ipynb)

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
