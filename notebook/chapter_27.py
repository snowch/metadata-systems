# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Build the query layer",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 26](chapter_26.ipynb) · [Next: Chapter 28](chapter_28.ipynb)

    # Chapter 27: Build the query layer

    **Objectives**

    - Write a traversal that finds everything downstream of an asset in the lineage graph.
    - Read the shop's answers to four other questions: one from the graph, three from the week's other records.
    - Find an asset that is recent by when it was written and old by what it shows.
    - Question the requirement "The query layer must answer who owns each asset."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 26's link, in a browser that had opened and run Chapter 26 (measured on a computer). Chapter 26's link opens this page in a new tab. Chapter 26 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 26 leaves more memory for this page.

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
    ## Questions over the graph

    Earlier chapters answered questions about the shop's assets: what is downstream of an asset (Chapters 6 and 16), where it came from (Chapter 15), who owns it (Chapters 2, 4 and 21), how recent it is (Chapter 13), which runs failed (Chapter 13), and what a change to a column reaches (Chapter 16).

    Here some of them are asked of the lineage graph Chapter 26 built, and the rest of the week's other records. This page builds the graph with the shop's own version of Chapter 26's `add`. Your cells there are not used.

    The week includes the returns desk. From Sunday 13, the analyst's copy is an input to `build_daily_sales`. Early on Monday 14, Chapter 13's failed night happens: `build_daily_sales` fails and writes nothing.

    `shop.query.next_assets(graph, asset)` gives the assets one step downstream of `asset`: what each program that reads `asset` writes. The next cell builds the graph and queries it for `orders.jsonl`.
    """)
    return


@app.cell
def _(shop):
    week27 = shop.run_week(["returns", "source", "failed"])
    graph27 = shop.query.graph(week27)
    shop.query.next_assets(graph27, "orders.jsonl")
    return graph27, week27


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One step downstream of `orders.jsonl` is `clean_orders`.

    `downstream(graph, asset)` must give the names of every asset downstream of `asset`, each once, without `asset` itself.

    The next cell holds `downstream` as it stands, and it gives one step. Change it so that it follows `next_assets` from each asset it finds, until no new asset turns up, as Chapter 6's `downstream` did. Select the cell and press **Run below**.

    The check below it tests the downstream assets of `orders.jsonl`, `clean_orders` and `returns`. As `downstream` stands, 1 of 3 answers is right: the one for `returns`, which nothing reads.
    """)
    return


@app.cell
def _(shop):
    def downstream(graph, asset):
        return shop.query.next_assets(graph, asset)
    return (downstream,)


@app.cell
def _(downstream, shop, week27):
    shop.query.check_downstream(week27, downstream)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the traversal, all 3 answers are right.

    Downstream of `orders.jsonl` are `clean_orders`, `clean_orders_copy.csv`, `daily_sales` and `sales_dashboard`.

    ## Stale assets, failed runs and column reach

    Monday's run of `build_daily_sales` failed (Chapter 13).

    The shop's query for stale assets reads Chapter 13's freshness measure. It lists each asset the shop measures (`orders.jsonl`, `clean_orders`, `daily_sales`, `sales_dashboard` and `returns`) that was last written more than 24 hours before 09:00 on Monday 14.

    Before you read on, write in the next cell whether that query will list `sales_dashboard`.
    """)
    return


@app.cell
def _():
    expected_stale = """
Will the query list sales_dashboard as stale?
........
"""
    return


@app.cell
def _(shop, week27):
    shop.query.answers(week27)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell above gives the shop's answers to four questions. Only the first, where `daily_sales` came from, follows the graph. The stale assets come from the freshness measure, the failed runs from the week's events, and the columns a change reaches from Chapter 16's column lineage.

    The stale assets are `daily_sales` and `returns`. `sales_dashboard` is not among them.

    Compare this with what you wrote.

    The next cell shows the freshness measure the query read, for each asset it measures: when it was last written, how many hours that was before 09:00 on Monday 14, and the latest day it holds.
    """)
    return


@app.cell
def _(shop, week27):
    shop.observe.freshness(week27)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `sales_dashboard` was last written at 03:00:09 on Monday 14, 6 hours before 09:00. Its latest day is Saturday 12.

    `refresh_dashboard` ran at 03:00, after the failed run, and redrew the dashboard from `daily_sales`, which the failed run did not write. So the dashboard's latest day is the same as `daily_sales`'s.

    A query that asks when an asset was last written does not read the latest day the asset holds (Chapter 13).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Who owns it
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "The query layer must answer who owns each asset."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "who owns `daily_sales`" means to you here.
    """)
    return


@app.cell
def _():
    what_owner_means = """
What does "who owns daily_sales" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The shop holds three owners for `daily_sales`, each from its own source, and each answers a different question. The next cell lists them:

    - `account`: which account controls the table in the warehouse? `svc_nightly_etl` (Chapter 2).
    - `responsible`: whom should you ask about it? `j.marsh`, from your records (Chapter 4).
    - `team`: which team looks after it? `data team`, from the team sheet (Chapter 21).

    You write `owner(asset)`. It must give an owner and say which meaning it holds: a dictionary with `owner` and `meaning`, where `meaning` is `account`, `responsible` or `team`.

    The cell after the list's cell holds `owner` as it stands: it gives the account's owner and no meaning, and the check below it fails.

    Change it to give one meaning's owner and that meaning's name. Select the cell and press **Run below**.
    """)
    return


@app.cell
def _(shop):
    shop.query.owners("daily_sales")
    return


@app.cell
def _(shop):
    def owner(asset):
        return {"owner": shop.query.owners(asset)["account"]}
    return (owner,)


@app.cell
def _(owner, shop):
    shop.query.check_owner(owner)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The check passes for any of the three meanings, as long as the owner given is that meaning's. It tests `daily_sales` only.

    The requirement asks about each asset. The next cell lists every asset on the platform, with the owner each meaning's source holds for it, and a blank where it holds none.
    """)
    return


@app.cell
def _(shop, week27):
    shop.query.coverage(week27)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The platform has 12 assets. The warehouse's `account` has an owner for 4 of them: its tables. `responsible` has an owner for 5: `daily_sales`, `sales_dashboard`, `clean_orders`, `clean_customers` and `products.csv`. `team` has an owner for 1, `daily_sales`.

    6 assets have no owner in any of the three sources: `orders.jsonl`, `customers.jsonl`, the three return files and `clean_orders_copy.csv`.

    So no single meaning gives an owner for each asset, and a query layer can answer the requirement for every asset only from a source that names an owner for each asset.

    The question Chapter 2 started from, "who should I ask about `daily_sales`?", needs `responsible`, or a team.

    A query that names its meaning lets whoever reads the answer tell which question it answered.

    The requirement does not say which meaning it wants.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 28

    A traversal over the graph found 4 assets downstream of `orders.jsonl`.

    The shop's query for stale assets listed `daily_sales` and `returns`, and not the dashboard, which was written on Monday and shows Saturday.

    Your `owner` passed the check for whichever meaning it named. No meaning's source held an owner for every asset.

    The queries could not show whom to ask about the 6 assets no source names.

    Chapter 28 builds a page that shows what these queries find about one asset.

    Take three questions to your own metadata system:

    - Which of your metadata system's answers say which question they answer?
    - Which of your freshness checks look at when an asset was written, and which at what it holds?
    - Which meaning of "owner" does your catalogue show?

    ### How this differs from a real platform

    - The shop's queries run over a graph of 17 edges, held in memory. In Chapter 23, a traversal followed to the end passed the limit of 1,000,000 records at 10,000,000 assets, and a traversal followed 4 steps never did. Your `downstream` follows to the end.
    - `downstream` does not look at the edges' times, so it answers for the whole week: the path through the analyst's copy is there whatever day you ask about.
    - The 24 hours that make an asset stale are the shop's choice.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 26](chapter_26.ipynb) · [Next: Chapter 28](chapter_28.ipynb)

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
