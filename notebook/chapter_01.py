# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="The shop and its platform",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)

    # Chapter 1: The shop and its platform

    **Objectives**

    - Identify what the platform holds: three systems, which hold files, tables and a dashboard.
    - Describe what happens on the platform each night, and what you cannot see of it: the export, the jobs, when they are due to run, and any notes.
    - Write a guess, for each warehouse table, at what it is made from.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You start work on Monday 14 September 2026 at 09:00, as the data engineer of an online shop that sells bicycle parts. The shop opened its online store a week ago, on Monday 7 September. Nobody who built its data platform is there to ask, and nothing about it is written down. Before you have sat down, the head of the shop sends you a message: "Thursday's revenue looks wrong." You cannot yet tell whether it is wrong; to find out, you first need to know what the platform holds and what happens on it each night.

    The platform has three systems: object storage, which holds files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard. Every night, an export from the shop's checkout and catalogue writes three files to object storage. Then jobs read the files, write the tables and refresh the dashboard. You can read everything the three systems hold. You cannot see the export, the jobs, when they are due to run, or any note anybody kept.

    In the code cells, three Python variables stand for the shop's three systems: `storage` is object storage, `warehouse` is the warehouse, and `reporting` is the reporting tool.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The three systems, in the order data moves through them each night.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.pipeline(week), "The shop's three systems and what each holds."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours of the next day, the export writes the three files to object storage again, then jobs write the tables and refresh the dashboard. The last night ends early on Monday 14 September, before you start work.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.week_strip(week), "The shop's first week: order days, the export and jobs after each, and the morning you start."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    On a computer, running every cell took 10 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

    </details>
    """), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    **Running and saving the page**

    1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
    2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
    3. To keep changes to code cells, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser. The answer boxes at the end save separately as you type.

    <details><summary>Your saved copy after a course update</summary>

    When the chapter is updated, the page shows the new version instead. If you changed a cell, your copy is kept under the chapter's name with "(your copy)" added, and [the list of files in this browser](https://snowch.github.io/metadata-systems/jupyterlite/tree/) opens it.

    </details>
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As you read each file, note which fields could tie it to a table in the warehouse. Note also anything in the rows that a job might have to deal with.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The product catalogue

    `products.csv`, in object storage, holds the shop's product catalogue: 8 products in 6 categories. Each product has an id (`product_id`), a name, a category, a list price in pence (`list_price_pence`) and the member of staff who last edited it (`updated_by`). `products.csv` stores every value as text, and it has no types.

    The cell below prints `products.csv` exactly as it is stored.
    """)
    return


@app.cell  # reader-id: products
def _(storage):
    print(storage.read_text("s3://shop-raw/products.csv"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The customers

    `customers.jsonl` holds the shop's 10 customers, in 7 countries. A customer's record has five fields: `customer_id`, a name, `email`, a country as a two-letter code, and `signed_up`. Each record names its fields. A date such as `signed_up` is just a string: the file has no date type.

    The cell below prints `customers.jsonl` exactly as it is stored.
    """)
    return


@app.cell  # reader-id: customers
def _(storage):
    print(storage.read_text("s3://shop-raw/customers.jsonl"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The orders

    `orders.jsonl` holds every order the shop took, as the checkout sent it. Each night, the file is written again, with every order taken since the online store opened. An order's record has seven fields: its id (`order_id`), the customer (`customer_id`), the product (`product_id`), the number of items (`quantity`), the price of one item in pence (`price_pence`), a status (`status`) and the time it was placed (`ordered_at`, in UTC). In this week's file, `status` is `completed` or `cancelled`.

    The cell below shows one day's orders as a table, and the day is set to Monday, `2026-09-07`. You can change it to any day from `2026-09-07` to `2026-09-13` and run the cell again.
    """)
    return


@app.cell  # reader-id: orders
def _(storage):
    day = "2026-09-07"
    storage.sql(
        "s3://shop-raw/orders.jsonl",
        """
    SELECT *
    FROM file
    WHERE date(ordered_at) = :day
        """,
        day=day,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The warehouse

    The warehouse holds three tables: `clean_customers`, `clean_orders` and `daily_sales`. Use `warehouse.sql` to query them with SQL.

    ### `clean_customers`

    The columns are `customer_id`, `name`, `email`, `country` and `signed_up`.

    The query below reads every row of `clean_customers`.
    """)
    return


@app.cell  # reader-id: clean_customers
def _(warehouse):
    warehouse.sql("SELECT * FROM clean_customers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `clean_orders`

    This table has seven columns:

    - **Order, customer and product:** `order_id`, `customer_id` and `product_id`.
    - **Quantity and price:** `quantity` and `price_pence`.
    - **Status and time:** `status` and `ordered_at`.

    The query below reads the first 7 rows of `clean_orders`. Change `LIMIT 7` to read more.
    """)
    return


@app.cell  # reader-id: clean_orders
def _(warehouse):
    warehouse.sql("SELECT * FROM clean_orders LIMIT 7")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `daily_sales`

    This table has one row per day:

    - **Date:** `day`.
    - **Reported revenue:** `revenue_pence`, in pence.

    The query below reads every row of `daily_sales`.
    """)
    return


@app.cell  # reader-id: daily_sales
def _(warehouse):
    warehouse.sql("SELECT * FROM daily_sales")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The dashboard

    The reporting tool holds one dashboard, `sales_dashboard`, titled "Sales, last 7 days", and it shows each day's reported revenue in pounds for 7 to 13 September.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.dashboard_chart(week), "Monday morning's dashboard: revenue per day, 7 to 13 September."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Your guesses about the warehouse tables

    For each of the three tables, write in its answer box which file or table you think it is made from, and what on this page makes you think so. The boxes save as you type; you do not need to run a cell or press **Save**. Chapter 2 shows your guesses for `daily_sales` and `clean_orders` beside the evidence and gives you separate boxes for revised explanations.

    <!-- answer: guesses -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Chapter 2](chapter_02.ipynb) goes back to the head of the shop's message and starts with Thursday's revenue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its people and its data are invented for the course. All times are UTC.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)

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
