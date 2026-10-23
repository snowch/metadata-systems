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

    - Read six references to `daily_sales`, or to a table or file named like it, and where each comes from.
    - Merge them by the last part of their names, and find what merged that should not.
    - Merge them by qualified names, then by what two systems' configurations declare.
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
    ## Six references

    A reference is the name one system uses for an asset. Chapter 12 tested pairs of references inside the warehouse and object storage. The shop's metadata system takes references from more places than those.

    The shop's developer has started using a transformation tool. The tool names each program's output as a model in a project. The project is `shop_models`, so the output `daily_sales` is `shop_models:daily_sales`.

    The reporting tool names the dataset behind the dashboard `Daily sales`, written with the prefix `dataset:`.

    Jo Marsh exported `daily_sales` to a CSV file in `shop-scratch`.

    The events name a dataset by a namespace and a name (Chapter 8). The development table is Chapter 12's, in `shop_dev`, a second database of the warehouse.

    The next cell lists the six references, and where each came from.
    """)
    return


@app.cell  # reader-id: cell-10
def _(shop):
    shop.aliases.references()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the rule for merging: take the last part of each name, in lower case, with spaces and hyphens read as underscores, and a file's extension left off. References with the same last part become one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which references this rule will merge.
    """), kind="info")
    return


@app.cell  # reader-id: cell-13
def _(shop):
    shop.aliases.merge("last part")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    Under that rule, all six become one entity. Among them are the development table, which holds other rows in another environment (Chapter 12), and Jo Marsh's CSV file, a copy made at one time.

    Compare this with what you decided.

    Deciding which references name one entity is **entity resolution**.

    If it merges too much, the development table's runs show in production's lineage (Chapter 12). If it merges too little, the model, the reporting tool's dataset and the table stay three entities, and what each system records about one is not joined to what the others record.

    </details>

    In the cell, change `"last part"` to `"qualified"`. Select the cell and press **Run below**. The qualified rule reads each warehouse name by the warehouse's rules (Chapter 12), and it takes an event's namespace as the warehouse.

    <details><summary>The printed result, explained</summary>

    The result has five entities. The warehouse's reference and the events' reference merge into one.

    The other four each stay alone: the development table is in another database; the CSV file's name is an object's key in storage, not a warehouse name; the transformation tool's and the reporting tool's names are not warehouse names.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What each system states

    The transformation tool's configuration declares that the model `shop_models:daily_sales` stands for the table `shop.analytics.daily_sales`. The reporting tool's configuration declares that the dataset `Daily sales` stands for the table `daily_sales`.

    Taking those declarations to name the table itself is the shop's choice.

    Another name a system declares for an asset is an **alias**.

    A dataset that filtered the table's rows, or added them up, would not be an alias of the table. A rule that merged it with the table would merge two different assets.

    In the cell, change the rule to `"aliases"`. Select the cell and press **Run below**. The `aliases` rule merges by qualified names first, then by the aliases each system declares.

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
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "the same dataset" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "the same dataset"</summary>

    "The same dataset" could mean four things, and each needs different information.

    - The same name: it needs a rule for reading names. Met for warehouse names, by the qualified rule. The other references' names alone do not merge.
    - The same rows: it needs a comparison of contents (Chapter 12). No rule here compares contents, so this reading is not tested.
    - The same thing to the business: it needs a statement of what each name stands for. Met only as far as the two configurations declare it, which is the shop's choice.
    - The same across environments: it needs to know which environment holds each table. The `aliases` rule keeps the development table apart.

    The requirement does not say which it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 23

    Six references name `daily_sales`, or a table or file named like it. The last part of each name merged all six, the development table and the copy among them. Qualified names merged two. Adding what two configurations declare merged four, and kept the development table and the copy apart.

    The rules decided from names and from what two configurations declare. Nothing compared contents, and nothing checked that the configurations are right.

    Chapter 23 asks what the shop's metadata system costs as the platform grows.

    - Which of your systems name the same table differently?
    - Where does each of your systems declare what a name stands for?
    - Which of your environments share table names?

    ### How this differs from a real platform

    - The transformation tool, its notation, the reporting tool's dataset and Jo Marsh's export are invented for the course.
    - A real catalogue resolves references with rules written for each system. A producer can also state other names for a dataset in its events: OpenLineage defines a `symlinks` dataset facet for these.

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
