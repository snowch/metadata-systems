# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Column-level lineage",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 9](chapter_09.ipynb) · [Next: Chapter 11](chapter_11.ipynb)

    # Chapter 10: Column-level lineage

    **Objectives**

    - Find which columns of the raw orders `revenue_pence` in `daily_sales` depends on, by parsing the programs' SQL.
    - Find what the SQL alone does not name.
    - See what a SQL function in a query leaves out of the answer.
    - Question the requirement "Show which columns `revenue_pence` depends on."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 9's link, in a browser that had opened and run Chapter 9 (measured on a computer). Chapter 9's link opens this page in a new tab. Chapter 9 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 9 leaves more memory for this page.

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
    ## Which columns

    Chapter 9's graph connects datasets: `build_daily_sales` reads `clean_orders` and writes `daily_sales`. It does not say which columns of `clean_orders` are behind which column of `daily_sales`.

    Jo Marsh is checking the checkout's data and asks which fields of `orders.jsonl` matter to the revenue the dashboard shows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Show which columns `revenue_pence` depends on."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lineage between columns, which columns each column is made from or depends on, is **column lineage**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which columns of `orders.jsonl` you expect `revenue_pence` to depend on, and why.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The program's SQL

    The next cell prints the code of `build_daily_sales`, from the shop's repository (Chapter 6).
    """)
    return


@app.cell
def _(shop):
    week10 = shop.run_week()
    code = [
        p["code"]
        for p in shop.columns.programs(week10)
        if p["job"] == "build_daily_sales"
    ][0]
    print(code)
    return code, week10


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    "Depends on" could mean two things, each needing something different:

    - the columns its value is made from: these are in the expressions the SELECT lists;
    - also the columns that decide which rows count: these are in the WHERE and GROUP BY clauses, and in DISTINCT.

    Either reading can stop at the program that writes `daily_sales`, or go back through every program to `orders.jsonl`.

    </details>

    The next cell gives the code to the shop's SQL parser, a program that reads the course's SQL. For each column the program writes, it lists each column it reads, with `kind` and `how`.
    """)
    return


@app.cell
def _(code, shop, warehouse):
    catalogue = None
    # catalogue = warehouse
    shop.columns.lineage(code, catalogue)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The parser lists `column 1` and `column 2`. The SELECT names no column of `daily_sales`.

    The warehouse puts the SELECT's first value in the table's first column, and the second in the second. To name them, the parser needs the columns of `daily_sales` from the catalogue: the warehouse's record of each table's columns, `information_schema` (Chapter 2).

    In the cell above, delete the `# ` at the start of the line `# catalogue = warehouse`, select the cell and press **Run below**, and read the column names.

    The parser uses two fields. These names are the shop's own:

    - **`kind`:** `value` for a column the value is made from, and `rows` for a column that decides which rows count.
    - **`how`:** says the way. For `value`, it is `copied`, `computed` (by an expression or a function, row by row) or `aggregated` (by SUM, COUNT and the like, over many rows). For `rows`, it is `filter` (WHERE), `grouping` (GROUP BY) or `distinct`.

    For `revenue_pence`, the parser lists:

    - `price_pence` and `quantity`: `value`, `aggregated`;
    - `status`: `rows`, `filter`;
    - `ordered_at`: `rows`, `filter` and `grouping`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Back to the raw orders

    The next cell prints the code of `build_clean_orders`, which writes `clean_orders`.

    The cell after it follows `revenue_pence` back through every program whose code the shop has, to `orders.jsonl`. The export that writes `orders.jsonl` is not in the repository, so the parser stops there.

    In its answer, `value` says whether `revenue_pence` is made from the column, through every step. `rows` says where the column decides which rows count.
    """)
    return


@app.cell
def _(shop, week10):
    print(
        [
            p["code"]
            for p in shop.columns.programs(week10)
            if p["job"] == "build_clean_orders"
        ][0]
    )
    return


@app.cell
def _(shop, week10):
    shop.columns.upstream(
        week10, "daily_sales", "revenue_pence", week10.warehouse
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    11 columns: 4 of `clean_orders` and 7 of `orders.jsonl`. The value of `revenue_pence` is made from 2 columns of `orders.jsonl`: `price_pence` and `quantity`.

    All 7 decide which rows count: `build_clean_orders` keeps one row of each set of equal rows (`distinct`), so every column takes part; its filter reads `customer_id` and `quantity`. The filter of `build_daily_sales` reads `status` and `ordered_at`.

    Three things in the week changed the revenue through columns that decide which rows count: `distinct` removed Wednesday's second copy of order 7015; the filter of `build_clean_orders` removed Thursday's 3 orders with no `customer_id`; the filter on `status` left out the cancelled orders of Tuesday and Saturday.

    Under the two readings:

    - the columns its value is made from: `price_pence` and `quantity`;
    - also the columns that decide which rows count: all 7.

    The parser lists both kinds, so its answer serves either reading. The requirement does not say which. The first reading leaves out `customer_id`, the column behind Thursday's low revenue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `SELECT *`

    In Chapter 6's `source` change, from Saturday's row on, `build_daily_sales` reads the analyst's copy, `clean_orders_copy.csv`.

    The analyst's script is not in the repository. The analyst sends its code: it writes the result of `SELECT * FROM clean_orders` to the copy.

    Which columns of `clean_orders` can the parser say the copy holds, from this code alone? The next cell gives the code to the parser without the catalogue; the cell after it, with it.
    """)
    return


@app.cell
def _(shop):
    week10s = shop.run_week(["source"])
    print(shop.columns.ANALYST_COPY)
    shop.columns.lineage(shop.columns.ANALYST_COPY)
    return (week10s,)


@app.cell
def _(shop, week10s):
    shop.columns.lineage(shop.columns.ANALYST_COPY, week10s.warehouse)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Without the catalogue, the parser gives one row: `clean_orders_copy.csv.*` from `clean_orders.*`. `*` names no column, and the parser lists no column it cannot read.

    With the catalogue, it gives 7 rows, one for each column of `clean_orders`, each `copied`.

    The next cell follows `revenue_pence` back in the week with the `source` change: 15 columns in all, through the copy (4), then `clean_orders` (4), to `orders.jsonl` (7).
    """)
    return


@app.cell
def _(shop, week10s):
    shop.columns.upstream(
        week10s, "daily_sales", "revenue_pence", week10s.warehouse
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The answer is for the code as it stands on Monday. The rows of `daily_sales` for Monday 7 to Friday 11 were written by code that read `clean_orders` directly, as Chapter 9's edges showed.

    The catalogue gives the columns of `clean_orders` as they are on Monday. `SELECT *` copies whatever columns its source has when it runs, so a record made from Monday's catalogue would be wrong for a run made when the columns were different. The columns of `clean_orders` did not change this week.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A SQL function

    In the week with the `net` change, the shop's developer edits `build_daily_sales`, from Saturday's row on, to take away what was returned.

    The developer added a SQL function to the warehouse, `returned_quantity(order_id, product_id)`. It reads the table `returns` and gives how many of one product of an order came back. It is not one of the returns desk's programs.

    The query also gains a `WITH` clause, which names a SELECT `lines` that the query then reads from.

    No order of Saturday or Sunday was returned, so the rows of `daily_sales` are the same.

    The next cell prints the edited code. The cell after it asks the SQL function about two returned orders and one that was not returned.
    """)
    return


@app.cell
def _(shop):
    week10n = shop.run_week(["net"])
    print(
        [
            p["code"]
            for p in shop.columns.programs(week10n)
            if p["job"] == "build_daily_sales"
        ][0]
    )
    return (week10n,)


@app.cell
def _(week10n):
    week10n.warehouse.sql("""
    SELECT
        returned_quantity(7004, 2) AS order_7004,
        returned_quantity(7008, 1) AS order_7008,
        returned_quantity(7001, 1) AS order_7001
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `returned_quantity(7004, 2)` and `returned_quantity(7008, 1)` give 1: one of each came back (`r-201` and `r-202`). `returned_quantity(7001, 1)` gives 0. A row's value depends on what is in `returns`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide whether the parser's answer for `revenue_pence` will include the table `returns`, and why.
    """), kind="info")
    return


@app.cell
def _(shop, week10n):
    shop.columns.upstream(
        week10n, "daily_sales", "revenue_pence", week10n.warehouse
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    13 columns. None is in `returns`.

    The parser followed `lines` back to `clean_orders`. The value of `line_pence` is made from `price_pence`, `quantity`, `order_id` and `product_id`: the last two are the function's arguments.

    The SQL holds the function's name and its arguments, not what the function reads. The parser takes the function's value to depend on its arguments and nothing else.

    The run's events also name `clean_orders` as the only input.

    In the shop, the function is code registered with the warehouse, and nothing records what it reads. A record that it reads `returns` has to come from whoever wrote it, or from the warehouse while the query runs.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## In an event

    The parser's answer is in a cell on this page. A program that receives the shop's events has no parser and no code. It has only what the events carry.

    OpenLineage defines a facet for column lineage, `columnLineage`, on an output dataset.

    Under `fields`, it lists each output column with the input columns its value is made from. Under `dataset`, it lists input columns that affect the whole dataset, such as a filter's.

    An input can carry `transformations`, each with a `type`: `DIRECT` where the output's value is derived from the input, `INDIRECT` where the input affects the output without the value coming from it. A `subtype` says how: among them `TRANSFORMATION`, `AGGREGATION`, `FILTER` and `GROUP_BY`.

    The shop writes `value` as `DIRECT` and `rows` as `INDIRECT`.

    The next cell makes the facet the shop's producer would add to `daily_sales` in a run's `COMPLETE`, and prints it.
    """)
    return


@app.cell
def _(shop, week10):
    print(shop.columns.show(shop.columns.facet(week10, "daily_sales")))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Under `fields`: `day`, from `ordered_at` (`TRANSFORMATION`); `revenue_pence`, from `price_pence` and `quantity` (`AGGREGATION`).

    Under `dataset`: `ordered_at` (`FILTER` and `GROUP_BY`) and `status` (`FILTER`).

    The facet keeps both kinds, so a program that receives it can answer either reading for this one program. Going back to `orders.jsonl` needs the facet of `build_clean_orders`'s output as well.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 11

    The shop's parser read the programs' SQL and listed, for each column, the columns its value is made from and the columns that decide which rows count. The value of `revenue_pence` is made from 2 columns of `orders.jsonl`, and all 7 decide which rows count, `customer_id` among them. The SQL did not name the columns of `daily_sales` or what `*` stands for; the catalogue did. The SQL held the SQL function's name and arguments, not the table it reads.

    The parser could not show what happens to the programs downstream when a dataset's columns change.

    Chapter 11 changes the fields of `orders.jsonl` and follows what each change does.

    - Which of your platform's queries use `SELECT *`, and what would their column lineage need?
    - Which functions in your warehouse read a table their callers do not name?
    - When someone asks what a column depends on, which of the two readings do they need?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    - The shop's parser is the course's own, and reads only the course's small SQL: one source per SELECT, and no joins.
    - OpenLineage's project has its own SQL parser, a library written in Rust that reads several dialects, SQLite's among them.
    - The facet's documentation lists no subtype for `DISTINCT`. In the facet of `clean_orders`, the shop writes it as `INDIRECT`, with the description `SELECT DISTINCT` and no subtype: the shop's choice.
    - The shop's warehouse keeps no record of which columns a query read while it ran.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 9](chapter_09.ipynb) · [Next: Chapter 11](chapter_11.ipynb)

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
