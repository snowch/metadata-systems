# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="The invisible data system, part 1",
    css_file="notebook.css",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 1, part 1: The shop and its platform

    **Objectives**

    - Name the shop's three systems, and what each one holds: files, tables or a dashboard.
    - Read the shop's products, customers and orders as their files store them.
    - Read the rows of the warehouse's three tables, and the values the dashboard shows.
    - Say what happens on the platform each night, and what you cannot see of it: the programs, when they are due to run, and any notes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md("This page runs Python in your browser. The first time you open it, your browser downloads about 17 MB. On a computer, Python took 9 to 17 seconds to start, and the page used about 0.8 GB of memory. If your phone runs short of memory, the browser may reload the page, and a reload loses what you changed or wrote on the page."), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You start work on Monday 14 September 2026 at 09:00, as the data engineer of an online shop that sells bicycle parts. The shop opened its online store a week ago, on Monday 7 September. Nobody who built its data platform is there to ask, and nothing about it is written down. Before anyone asks you about the shop's numbers, find out what the platform holds and what happens on it each night.

    The platform has three systems: object storage, which holds files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard. Every night, programs read the files, write the tables and refresh the dashboard. You can read everything the three systems hold. You cannot see the programs, when they are due to run, or any note anybody kept.

    The boxes of code with numbered lines are cells you can run. To run a cell, press its run button. The run button is a triangle at the top right of the cell. You can also press Ctrl+Enter (Cmd+Enter on a Mac) while you type in the cell. On a computer, the run button appears when the pointer is over the cell. On a phone, the run button is always there. When you run a cell, the cells that use its results run again. Nothing you change is saved. Reloading the page shows the chapter as it was published.

    In the cells, `storage`, `warehouse` and `reporting` name the shop's three systems: object storage, the warehouse and the reporting tool.
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
    An asset is one thing the platform holds: here, a file, a table or a dashboard.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours of the next day, the three files are written again, then programs write the tables and refresh the dashboard. The last night ends early on Monday 14 September, before you start work.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.week_strip(week), "The shop's first week: order days, a night's work after each, and the morning you start."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The product catalogue

    `products.csv`, in object storage, holds the shop's catalogue: 8 products in 6 categories. Each product has an id (`product_id`), a name, a category, a list price in pence (`list_price_pence`) and the member of staff who last edited it (`updated_by`). `products.csv` names its columns once, in its first line, and has no types: every value is text.

    The cell below prints `products.csv` exactly as it is stored.
    """)
    return


@app.cell
def _(storage):
    print(storage.read_text("s3://shop-raw/products.csv"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The customers

    `customers.jsonl` holds the shop's 10 customers, in 7 countries. A customer's record has five fields: an id (`customer_id`), a name, an email address (`email`), a country as a two-letter code, and the date the customer signed up (`signed_up`). `orders.jsonl` and `customers.jsonl` are JSON Lines, with one record per line, and every record names its fields. A JSON value has one of a few types, such as a string, a number, true or false, or null, and a date or an amount is just a string or a number.

    The cell below prints `customers.jsonl` exactly as it is stored.
    """)
    return


@app.cell
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


@app.cell
def _(storage):
    day = "2026-09-07"
    storage.sql("s3://shop-raw/orders.jsonl", "SELECT * FROM file WHERE date(ordered_at) = :day", day=day)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The warehouse

    The warehouse holds three tables: `clean_customers`, `clean_orders` and `daily_sales`. You read a table by writing SQL in `warehouse.sql`. `daily_sales` has one row per day: the day and that day's revenue in pence (`revenue_pence`).

    The cell below reads every row of `clean_customers`.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("SELECT * FROM clean_customers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below reads the first 7 rows of `clean_orders`, and you can change `LIMIT 7` to read more.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("SELECT * FROM clean_orders LIMIT 7")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below reads every row of `daily_sales`.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("SELECT * FROM daily_sales")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The dashboard

    The reporting tool holds one dashboard, `sales_dashboard`, titled "Sales, last 7 days", and it shows each day's revenue in pounds for 7 to 13 September.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.dashboard_chart(week), "Monday morning's dashboard: revenue per day, 7 to 13 September."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you have finished looking round the platform, the head of the shop sends you one line: "Thursday's revenue looks wrong." [Part 2](part-2.html) starts from that line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its people and its data are invented for the course. All times are UTC.

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
