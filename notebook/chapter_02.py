# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="The invisible data system",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb) · [Next: Chapter 3](chapter_03.ipynb)

    # Chapter 2: The invisible data system

    **Objectives**

    - Read what the shop's three systems record about a file, a table and a dashboard.
    - Work out from the data how `daily_sales` could have been made, and see what that does and does not establish.
    - Follow three changes to the shop that leave the data unable to say what happened.
    - Name the records that would have answered the questions the platform could not.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Monday morning

    It is Monday 14 September 2026, your first morning as the shop's data engineer. You have looked round the shop's platform in [Chapter 1](chapter_01.ipynb). The head of the shop has sent you a message: "Thursday's revenue looks wrong."
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
def _(figures, mo, week):
    mo.Html(figures.figure(figures.dashboard_chart(week), "Monday morning's dashboard: revenue per day, 7 to 13 September."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Thursday shows £51.50, against £153.75 on Wednesday and £204.24 on Friday.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 1's link, in a browser that had opened Chapter 1 (measured on a computer). Chapter 1's link opens this page in a new tab. Chapter 1 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 1 leaves more memory for this page.

    Running every cell took 10 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

    </details>
    """), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Questions the platform cannot answer

    Messages like the head's arrive every week on a platform you did not build. Each one raises questions like these:

    - Is Thursday's total wrong, and since when?
    - Can we delete `products.csv`? Does anything still read it?
    - If the checkout renames a column in `orders.jsonl`, what stops working?
    - Who should I ask about `daily_sales`?

    The rows show whether Thursday's total differs from Thursday's orders. Why it differs, and since when, depends on the rules the jobs apply. Whether `products.csv` can be deleted, and what a renamed column in `orders.jsonl` breaks, depends on which files the jobs read. Who is responsible for `daily_sales` depends on what people decided and took on. The rows a table holds today record none of these.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Thursday

    Thursday's orders in `orders.jsonl` add up to 20550 pence. `daily_sales` says 5150 for Thursday, and the dashboard shows £51.50. The two totals differ by 15400 pence, £154.00.

    The cell below reads every order in `orders.jsonl` and adds up `price_pence` times `quantity` for one day. The day is set to Thursday, `2026-09-10`, and you can change it and run the cell again.
    """)
    return


@app.cell
def _(storage):
    orders = storage.records("s3://shop-raw/orders.jsonl")
    day = "2026-09-10"
    sum(o["price_pence"] * o["quantity"] for o in orders if o["ordered_at"].startswith(day))
    return day, orders


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below reads the row from `daily_sales` for the day that the cell above sets. If you change the day in the cell above, run the cell below too. It does not run again by itself. Select the cell above and press **Run below**.
    """)
    return


@app.cell
def _(day, warehouse):
    warehouse.sql(
        """
        SELECT * FROM daily_sales
        WHERE day = :day
        """,
        day=day,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It is not only Thursday. On Monday, Friday and Sunday the raw orders add up to the day's row in `daily_sales`. On Tuesday, Wednesday, Thursday and Saturday they do not. The platform holds both sets of numbers and nothing that connects them: no record of which orders `daily_sales` counts, which job decided that, or why.

    The cell below puts, for every day, the total of the raw orders in `orders.jsonl` beside that day's row in `daily_sales`. It shows whether the two are the same. The `files=` argument of `warehouse.sql` lets the query read `orders.jsonl` from object storage as a table called `raw_orders`.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql(
        """
        SELECT d.day, r.raw_orders_pence, d.revenue_pence,
               CASE WHEN r.raw_orders_pence = d.revenue_pence THEN 'same' ELSE 'different' END AS compared
        FROM daily_sales AS d
        JOIN (
            SELECT date(ordered_at) AS day, SUM(price_pence * quantity) AS raw_orders_pence
            FROM raw_orders
            GROUP BY day
        ) AS r USING (day)
        ORDER BY d.day
        """,
        files={"raw_orders": "s3://shop-raw/orders.jsonl"},
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below lists Thursday's orders in `orders.jsonl` that `clean_orders` does not have. Look at what these orders have in common, then compare their total with Thursday's gap of 15400 pence.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql(
        """
        SELECT * FROM raw_orders
        WHERE date(ordered_at) = '2026-09-10'
          AND order_id NOT IN (SELECT order_id FROM clean_orders)
        """,
        files={"raw_orders": "s3://shop-raw/orders.jsonl"},
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Orders 7021, 7023 and 7025 have no customer id. Together they are worth 15400 pence, the whole of Thursday's gap. `clean_orders` does not have them. Their absence from `clean_orders` shows which orders are missing, not why: nothing on the platform records the rule that left them out.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What the platform holds

    What does the warehouse record about `daily_sales`? The two cells below read `information_schema` with SQL, the warehouse's own record of its tables: `information_schema.tables` has one row per table, and `information_schema.columns` has one row per column, with the column's type.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
        SELECT * FROM information_schema.tables
        WHERE table_name = 'daily_sales'
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'daily_sales'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cells showed the two columns of `daily_sales`, `day` and `revenue_pence`, with their types. They also showed 7 rows, a size in bytes, a created time of 1 September, and a last-altered time of 02:30 on Monday 14 September. The warehouse lists `etl_service` as the owner. It records nothing else about the table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Object storage records three things about a file: its key, its size in bytes and when it was last modified. A key is the file's full name, such as `s3://shop-raw/orders.jsonl`, where `shop-raw` is the bucket: the container the file sits in. The reporting tool records the dashboard's title, who created it and when, when it last refreshed, and the values it shows.

    The cell below lists the files in the bucket `shop-raw`.
    """)
    return


@app.cell
def _(storage):
    storage.ls("s3://shop-raw/")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below shows what the reporting tool records about `sales_dashboard`.
    """)
    return


@app.cell
def _(reporting):
    reporting.dashboard("sales_dashboard")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Everything the three systems showed describes each asset as it is this morning. None of it describes how the asset got that way: which job wrote it, what it read, what its rows were yesterday, or who decided its rules. The platform records the current state of each asset and none of its history.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What each system records about assets, and why

    Each of the shop's systems records the things about an asset that its own work needs. The warehouse keeps column names and types so that it can run a query. Object storage keeps a file's key so that it can serve the file. The reporting tool keeps the values so that it can draw the chart. In the shop's platform, a system records what its own work needs and nothing more. The questions you want answered are not its work.

    The owner the warehouse records shows how far that goes. "Who should I ask about `daily_sales`?" wants a person or a team.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Data teams often adopt a rule so that every table has someone to ask about it: "Every table must have an owner."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You adopt the rule for the shop's platform. The cell below lists the owner the warehouse records for each table.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
        SELECT table_name, table_owner
        FROM information_schema.tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The warehouse records `etl_service` as the owner of all three tables, in the column `table_owner` of `information_schema.tables`. The name looks like an account a program logs in as, and the warehouse records nothing more about it.

    | What the rule could mean | What it needs | Does `etl_service` answer it? |
    | --- | --- | --- |
    | who is responsible for the table | a person | no |
    | which team is responsible for it | a team | no |
    | which job writes it | a program | no: it names an account, not a program |
    | which account controls it in the warehouse | an account | yes |

    Answering "Who should I ask about `daily_sales`?" needs a person or a team responsible for the table. The warehouse already records an owner for every table, so the rule is met, and you did nothing to make it so. That owner is an account, `etl_service`: it says which account controls the table in the warehouse. It does not say who is responsible for `daily_sales`, so you still do not know whom to ask.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reconstruction

    The platform records nothing about how `daily_sales` was made. The usual move is to infer it from the data: find a query over another asset that gives the same rows.

    In Chapter 1's last cell you wrote a guess at what `daily_sales` is made from. The cell below has the same line. Write your guess in it again, or a new one: which table, which orders, and what is added up.
    """)
    return


@app.cell
def _():
    guess = """
daily_sales:     made from ........ because ........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below tests one guess, written in the same form as the line in your cell.

    **`daily_sales`: made from `clean_orders`, completed orders only, `price_pence` × `quantity` added up for each day, because:**

    - `daily_sales` has two columns, `day` and `revenue_pence`: one total in pence for each day.
    - Each order in `clean_orders` has a price in pence, `price_pence`, a quantity, `quantity`, and the time it was placed, `ordered_at`.
    - On Thursday, `daily_sales` is short of the raw orders by exactly the three orders that `clean_orders` does not have, so on Thursday it agrees with `clean_orders`, not with `orders.jsonl`.
    - An order's `status` is `completed` or `cancelled` (Chapter 1). The guess leaves cancelled orders out on the assumption that a cancelled order brings in no money. Nothing above shows whether `daily_sales` counts them: this part of the guess has no evidence yet.

    The cell compares the result with the rows of `daily_sales`: `True` means every row is the same, and `False` means at least one row is not.
    """)
    return


@app.cell
def _(warehouse):
    rebuilt = warehouse.sql("""
        SELECT date(ordered_at) AS day, SUM(price_pence * quantity) AS revenue_pence
        FROM clean_orders
        WHERE status = 'completed'
        GROUP BY day
        ORDER BY day
    """)
    rebuilt == warehouse.sql("SELECT * FROM daily_sales ORDER BY day")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.

    Thursday matches because `clean_orders` does not hold Thursday's three orders with no customer id: orders 7021, 7023 and 7025, which you found above.

    The query keeps only completed orders. `clean_orders` also holds 2 cancelled orders. `daily_sales` does not count them, and neither does the query.

    Compare the query with your guess. Did you name the same table and the same orders?

    The query shows how `daily_sales` could have been made. It does not show how it was made. You can test that difference with three small changes to the shop. Each changes the shop's week in one way, and you apply them one at a time. None of the three happened in the week you have read so far.

    - **An analyst copies clean_orders every night**: the analyst copies `clean_orders` to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night.
    - **From Saturday, the daily_sales job keeps unrefunded orders**: the job that writes `daily_sales` is edited, from Saturday's row on, to keep every order that has not been refunded, where it kept completed orders.
    - **The daily_sales job fails on the last night**: it writes nothing that night.

    For each change, the question is the same: does a query over the week's assets still give every row of `daily_sales`, and which of the platform's records show the change?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    change = mo.ui.dropdown(
        options={
            "The shop stays as it is": [],
            "An analyst copies clean_orders every night": [
                "copy"
            ],
            "From Saturday, the daily_sales job keeps unrefunded orders": [
                "refunds"
            ],
            "The daily_sales job fails on the last night": [
                "failed"
            ]
        },
        value="The shop stays as it is",
        label="Choose a change to the shop",
        full_width=True,
    )
    mo.vstack([mo.md("Choose a change to the shop from the menu below. Then select the first cell below the menu and press **Run below**. The cells below show the platform on Monday morning, after the week ran with the change you chose. The cells above the menu keep showing the week as it ran."), change])
    return (change,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What object storage holds**
    """)
    return


@app.cell
def _(change, shop):
    changed = shop.run_week(change.value)
    changed.storage.ls()
    return (changed,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The warehouse's record of `daily_sales`**
    """)
    return


@app.cell
def _(changed):
    changed.warehouse.sql("""
        SELECT * FROM information_schema.tables
        WHERE table_name = 'daily_sales'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The dashboard**
    """)
    return


@app.cell
def _(changed):
    changed.reporting.dashboard("sales_dashboard")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below lists each query, from a fixed set of simple ones over the week's assets, that gives every row of `daily_sales`, even if it gives a row more. Each row of its result is one query: `source` names the asset it reads; `keep` says which orders it keeps (all, completed or cancelled); `measure` says what it adds up (revenue, quantity or rows); `per` says what it groups by (day, customer or product); and `sql` is the query itself.
    """)
    return


@app.cell
def _(changed, shop):
    shop.queries_that_rebuild(changed, "daily_sales", fit="covers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **An analyst copies `clean_orders` every night.** Now the same query over the copy reproduces `daily_sales` too. None of the platform's records says which of the two the job reads. A query that fits is evidence for every source it fits.

    **From Saturday, the `daily_sales` job keeps unrefunded orders.** The shop has no refunds, so from Saturday every order counts, cancelled ones included. Saturday's row in `daily_sales` becomes 21549 instead of 19149, in pence. The dashboard shows £215.49 instead of £191.49. The table still has 7 rows and the same last-altered time, and no simple query over the week's assets reproduces it any more. The evidence has gone, and the platform records nothing about the edit.

    **The `daily_sales` job fails on the last night.** The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found. Each record is normal on its own. The gap shows only when you compare the last-altered times. Only a record of the failure would say that a write was due and did not happen.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A rule the week never tests

    A reconstruction can be checked against the data, but only where the data has something to check. In the shop's design, which the platform does not record and you cannot see, `clean_orders` is made from `orders.jsonl` by four rules: keep one row of an order the export wrote twice, drop orders with no customer id, keep cancelled orders, and drop orders with a quantity of 0 or less. No order in the week has a quantity of 0 or less, so the rule never removes a row, and a version of the job without it would have produced the same table. From the data, you cannot tell whether the rule exists. The data can confirm a rule only where some row would have triggered it.

    Your guess for `clean_orders` from Chapter 1 meets the same limit.

    The cell below counts the orders in `orders.jsonl` with a quantity of 0 or less.
    """)
    return


@app.cell
def _(orders):
    sum(1 for o in orders if o["quantity"] <= 0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below lists the settings of the four cleaning rules that turn the raw orders into `clean_orders` exactly, with one setting on each row. The rules cover orders written twice, orders with no customer id, cancelled orders, and orders with a quantity of 0 or less.
    """)
    return


@app.cell
def _(shop, week):
    shop.cleaning_rules_that_fit(week)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Records made at the time

    The questions at the start need three kinds of record, none of which the platform keeps:

    - what an asset is: what `daily_sales` means, what it is for, and who is responsible for it;
    - what happened: each night's write of `daily_sales`, when it ran, which version of the job's code ran, what it read, and whether it succeeded;
    - what was made from what: such a record would say that `daily_sales` is built from the completed orders in `clean_orders`, and that the dashboard reads `daily_sales`.

    A record of what the job read would have answered the analyst's copy. A record of which version of the job's code ran each night would have answered the edit. A record of whether each night's write succeeded would have answered the failed night.

    Information of this kind, about an asset or about the platform, is called metadata: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets. Some of it the systems already keep for their own purposes: the names, types, counts and times you read above. The systems do not keep what an asset means, what happened to it or what it was made from; somebody has to record those, and the second and third have to be recorded when the thing happens. A note of what a job read, written the next morning from the data, is a reconstruction, with the limits shown above.

    Real platforms keep more history than the shop's: query logs, table snapshots, audit trails. Those are records made at the time too, kept by the system rather than by a person, and later chapters use them where they exist.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The handover

    Suppose you had been the engineer who built the platform, handing it over on the Friday before you started. Write down, for `daily_sales` alone, what you would leave: what the table means and who to ask about it; what runs each night, reading what and writing what; and what the next engineer should do when a night fails. Then compare it with what the warehouse records: two column names, a row count, a size, two times and an account.
    """)
    return


@app.cell
def _():
    note = """
Write what daily_sales means and who to ask about it. Include what
runs each night, what it reads and writes, and what to do if a night fails.
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You write your handover note in the cell above, between the triple quotes, and press **Save** to keep it. The cell below shows only what the warehouse records about `daily_sales`, to compare with your note.
    """)
    return


@app.cell(hide_code=True)
def _(mo, warehouse):
    mo.vstack([
        warehouse.sql("SELECT * FROM information_schema.tables WHERE table_name = 'daily_sales'"),
        warehouse.sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'daily_sales'"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 3

    The platform's state answers what exists. It does not answer what happened or why. Inferring the history from the data gave an explanation that fitted, and three ordinary changes made it ambiguous, made it wrong, or left a failed night looking like a normal one. The records that would have answered had to be made when the work was done.

    Chapter 3 starts making them: a description of each asset, kept beside the data, with what the asset means and who is responsible for it. It then asks the four questions at the start again, to see which of them that record answers. Chapter 6 records what was made from what, which is called lineage. Chapter 7 records each run of a job: when it started and ended, which version of its code ran, what it read and wrote, and whether it succeeded.

    Nothing in this chapter tested your guess for `clean_customers`. What would test it?

    - Pick a table on a platform you work on. What does its record say about who is responsible for it, and what does it say about what the table is made from?
    - What would a description of `daily_sales` have to hold to answer "Who should I ask about `daily_sales`?"
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its people and its data are invented for the course.

    Some real systems keep history that the shop's warehouse does not. An Apache Iceberg table keeps snapshots, each the state of the table at some time. A Delta Lake table keeps, for each write, the operation, the user and the time, for 30 days by default. The shop's systems keep only the current rows.

    In some real databases, a table's owner is an account too. In PostgreSQL, for example, a new table's owner is normally the account that created it. At first, only the owner (or a superuser) can do anything with the table; other accounts can use it once they are given the right to. The right to alter or drop the table comes with being its owner. The shop's warehouse records the owning account and no such rights.

    A file's size is its real size in bytes. A table's size is an estimate from its rows. All times are UTC. A real platform has hundreds or thousands of assets; searching for queries that rebuild one would cost far more. "No simple query over the week's assets reproduces it" means none of the simple queries the menu's last cell tries. A query with a condition on the date could still reproduce the edited table.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb) · [Next: Chapter 3](chapter_03.ipynb)

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
