# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Build the metadata store",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 23](chapter_23.ipynb) · [Next: Chapter 25](chapter_25.ipynb)

    # Chapter 24: Build the metadata store

    **Objectives**

    - Keep the week's metadata as JSON documents, as a table, as a table with an index, and as a graph.
    - Answer the same question for each shape: what reads a dataset.
    - Count the records each shape reads to answer it, and find which questions each shape suits.
    - Question the requirement "The metadata store must be fast."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 23's link, in a browser that had opened and run Chapter 23 (measured on a computer). Chapter 23's link opens this page in a new tab. Chapter 23 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 23 leaves more memory for this page.

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
    ## One question, four shapes

    Since Chapter 9, the shop's metadata system has answered questions from the events it ingested. Part VI builds the parts it used, one chapter each, starting here with the store that keeps the metadata.

    One store can keep the same metadata in different shapes.

    Here the metadata is the 14 edges by job of the week with the returns desk, the week Chapter 23 measured. It also holds the lines Chapter 4 wrote about two datasets: what `daily_sales` means and who is responsible for it, and who is responsible for `sales_dashboard`.

    Each shape answers one question: what reads a dataset? You write the answer for each shape.

    A check below your code runs it for each of the 11 datasets the edges name, compares each answer with the edges, and counts the items your code read.

    The first shape is JSON documents: one for each program that ran (the four jobs and the returns desk's two functions) and one for each dataset. The next cell prints them, one document on each line.
    """)
    return


@app.cell
def _(shop):
    week24 = shop.run_week(["returns"])
    documents = shop.store.documents(week24)
    print(documents)
    return documents, week24


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A program's document holds `job`, its number of runs (`runs`), the datasets it reads (`reads`) and the datasets it writes (`writes`).

    A dataset's document holds `dataset` and the lines Chapter 4 wrote about it, where there are any. It has no `reads`.

    The 11 datasets are the ones the edges name, so the list includes `r-203.json`, which is no longer in storage. It leaves out `products.csv`, which no program reads or writes. That is why it differs from the map's assets.

    The next cell defines `readers_of(documents, dataset)`. Its loop goes through every document and adds nothing to the result.

    As it stands, the check below it finds 3 of 11 datasets right: the 3 that no program reads.

    Change the line inside the loop so that it adds a program's `job` when its `reads` lists the dataset. Then select the cell and press **Run below**.
    """)
    return


@app.cell
def _():
    def readers_of(documents, dataset):
        found = []
        for doc in documents:
            pass  # add doc["job"] when the document's "reads" lists the dataset
        return found
    return (readers_of,)


@app.cell
def _(documents, readers_of, shop, week24):
    shop.store.check(week24, documents, readers_of)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the loop changed, the check finds 11 of 11 datasets right. The loop reads 187 documents: all 17 documents for each of the 11 datasets.

    The loop opens every document because a dataset's readers are named in each program's document, not in the dataset's own.

    ## A table

    The second shape is a table in SQLite, the database the shop's warehouse runs on: `edges`, with one row for each edge by job, and the columns `job`, `edge`, `dataset` and `runs`.

    The table has no index. SQLite does not make one unless a statement creates it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide whether a query for one dataset's readers will read every row of `edges`, or only that dataset's rows.
    """), kind="info")
    return


@app.cell
def _(shop, week24):
    tables = shop.store.tables(week24)
    tables
    return (tables,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next cell holds the query, as text, in `query`.

    As it stands, the query has no `:dataset`, the name the check passes in for each dataset. The check takes that as no readers for any dataset, and finds 3 of 11 right: the 3 that no program reads.

    Add a `WHERE` clause that keeps the rows whose `edge` is `reads` and whose `dataset` is `:dataset`. Select the cell and press **Run below**.

    The check gets SQLite's own plan for the query. The plan shows whether the query reads the whole table or looks its rows up.
    """)
    return


@app.cell
def _():
    query = "SELECT job FROM edges"
    return (query,)


@app.cell
def _(query, shop, tables, week24):
    shop.store.check(week24, tables, query)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    With the `WHERE` clause, the check finds 11 of 11 right. The query reads every row of `edges`: 154 rows, 14 for each of the 11 datasets.

    The plan is a scan: SQLite reads each row and tests it against the `WHERE` clause.

    Compare this with what you decided.

    </details>

    ## An index

    The next cell drops the index `edges_index` if there is one, and creates it on the column `job` of `edges`.

    Change `job` to the column your query looks up. Select the cell and press **Run below**: the check below it runs your query again.
    """)
    return


@app.cell
def _(tables):
    tables.sql("DROP INDEX IF EXISTS edges_index")
    tables.sql("CREATE INDEX edges_index ON edges(job)")
    return


@app.cell
def _(query, shop, tables, week24):
    shop.store.check(week24, tables, query)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the index on `dataset`, the query reads 14 rows in all. That is, for each dataset, only that dataset's rows. The plan looks them up through the index, and the check names the index.

    With the index on `job`, the plan stays a scan, because the query does not look up a job.

    An index on `edge` is used too, but it narrows little: each search reads the 8 rows whose `edge` is `reads`, 88 in all.

    ## A graph

    The fourth shape is a graph, as in Chapter 5: a node for each program and each dataset, and an edge for each edge by job.

    `graph.edges_at(name)` gives the edges at one node, and the check counts each edge it gives.

    The next cell defines `readers_of(graph, dataset)` for the graph. As it stands, it gives the job of every edge at the dataset's node, and the check finds 6 of 11 right.

    Keep only the edges whose `edge` is `reads`. Select the cell and press **Run below**.
    """)
    return


@app.cell
def _():
    def readers_of(graph, dataset):
        return [e["job"] for e in graph.edges_at(dataset)]
    return (readers_of,)


@app.cell
def _(readers_of, shop, week24):
    shop.store.check(week24, shop.store.graph(week24), readers_of)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With that condition, the check finds 11 of 11 right, and reads 14 edges: for each dataset, the edges at its node.

    For this question, over all 11 datasets: the documents read 187, the table with no index 154, the table with the index on `dataset` 14, and the graph 14.

    These counts compare how many items each shape opens, not how big each item is.

    The next cell asks each shape two questions, with the shop's own code: what reads `clean_orders`, and what `build_daily_sales` reads. The table has the index on `dataset`, and no index on `job`.
    """)
    return


@app.cell
def _(shop, week24):
    shop.store.compare(week24, "warehouse://shop-warehouse/shop.analytics.clean_orders", "shop/build_daily_sales")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What reads `clean_orders`: 17 documents, 2 rows of the table, 2 edges of the graph.

    What `build_daily_sales` reads: 1 document, 14 rows of the table, 2 edges of the graph.

    The documents are kept one for each program, so a program's question opens 1 document and a dataset's question opens all 17.

    The table's 14 rows for the program's question are a scan: the table has no index on `job`. The index on `dataset` serves the dataset's question only.

    The graph keeps both ends of every edge, so each question reads only one node's edges: 2 here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A fast store
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "The metadata store must be fast."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "fast" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "fast"</summary>

    "Fast" could mean several things:

    - fast to find one program or dataset by its name: a key for each document, or a lookup by name. Finding `build_daily_sales` took 1 document.
    - fast to find what reads a dataset: an index on `dataset`, or a graph. Each read 2 items for `clean_orders`.
    - fast to follow lineage several steps: one node's edges at each step, as in Chapter 5's traversal. This chapter measured one step.
    - fast to take each event as it arrives: this chapter did not measure writing.
    - fast enough as the store grows: counts at a larger size, which Chapter 23 projected for other questions, and the time each takes, which this chapter did not measure.

    Of the shapes here, the documents and the graph met the first reading. The table, with no index on `job`, did not. The table with the index on `dataset` and the graph met the second. The graph met the third, for one step. None was measured against the fourth or the fifth.

    The requirement does not say which it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 25

    Four shapes answered the same question, and each passed the same check. Where the answer is kept decided how many items it read: in each program's document, every document; in a table with no index, every row; through an index on `dataset` or at a graph's node, only the dataset's own.

    The check could not show the time each shape takes, or what each costs to write.

    Chapter 25 builds the collector that receives the events the store is filled from.

    - Which questions does your metadata store answer most often?
    - Which of them read every item?
    - Which structure would serve them, and which questions would it not?

    ### How this differs from a real platform

    - The shop's store holds 14 edges. Chapter 23 projected other questions at 10,000,000 assets: the latest run of one job, one day's events, and what is downstream of one asset.
    - The check counts items from SQLite's plan and from the shop's own counting, not from the time taken.
    - Finding a document by name, a node, or a place in an index counts as nothing here. Chapter 23 counted about 30 steps down an index at 10,000,000 assets.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 23](chapter_23.ipynb) · [Next: Chapter 25](chapter_25.ipynb)

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
