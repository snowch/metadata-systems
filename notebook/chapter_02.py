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

    The head of the shop has sent you one line: "Thursday's revenue looks wrong."

    You investigate it using only what the shop's platform holds, and find where that evidence stops.

    1. [Find the discrepancy](#1.-Find-the-discrepancy): compare the raw orders with what the warehouse reports, and find the orders that are missing.
    2. [What the platform records](#2.-What-the-platform-records): what object storage, the warehouse and the reporting tool record about each asset.
    3. [Test an explanation](#3.-Test-an-explanation): rebuild `daily_sales` from the data, and see what that establishes and what it does not.

    [Records made at the time](#Records-made-at-the-time) says which records would have answered; [a short check](#Check:-evidence-of-what-a-job-read) closes the chapter.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Monday morning

    It is Monday 14 September 2026, your first morning as the shop's data engineer. You have looked round the shop's platform in [Chapter 1](chapter_01.ipynb).
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

    The rows show whether Thursday's total differs from Thursday's orders. Why it differs, which files the jobs read, and who is responsible for a table depend on what the jobs do and what people decided. The rows a table holds record none of these.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Find the discrepancy
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.totals(week, ('Raw orders, `orders.jsonl`', '`daily_sales`', 'Difference')), 'Thursday 10 September, the raw orders against `daily_sales`.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell below sets each day's raw orders beside that day's row in `daily_sales`.
    """)
    return


@app.cell
def _(warehouse):
    # files= reads orders.jsonl from object storage as raw_orders.
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
    On Monday, Friday and Sunday the raw orders add up to the day's row in `daily_sales`. On Tuesday, Wednesday, Thursday and Saturday they do not. The next cell lists every order in `orders.jsonl`, across the whole week, that `clean_orders` does not have.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql(
        """
        SELECT * FROM raw_orders
        WHERE order_id NOT IN (SELECT order_id FROM clean_orders)
        """,
        files={"raw_orders": "s3://shop-raw/orders.jsonl"},
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    <div class="ms-found">

    **Established.** Across the whole week, 3 orders in `orders.jsonl` are missing from `clean_orders`: 7021, 7023 and 7025. All three are Thursday's, and none has a customer id. Together they are worth 15400 pence, the whole of Thursday's gap.

    </div><div class="ms-open">

    **Not established.** Which rule left them out, which job applied it, and since when. Why Tuesday, Wednesday and Saturday differ: no order from those days is missing from `clean_orders`.

    </div>
    """), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. What the platform records

    The cells read each system's own record of its assets: the warehouse's `information_schema` for `daily_sales`, the listing of the bucket `shop-raw`, and the reporting tool's record of `sales_dashboard`.
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


@app.cell
def _(storage):
    storage.ls("s3://shop-raw/")
    return


@app.cell
def _(reporting):
    reporting.dashboard("sales_dashboard")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    <div class="ms-found">

    **Established.** Each record describes an asset as it is this morning. The record for `daily_sales` gives its columns and their types, 7 rows, a size, when it was created, a last-altered time of 02:30 on Monday 14 September, and an owner, `etl_service`. Each file's record gives its key, size and last-modified time. The dashboard's record gives its title, who created it, when it last refreshed and the values it shows.

    </div><div class="ms-open">

    **Not established.** Which job wrote any of these assets, what the job read, which version of its code ran, what the rows were the day before, or who decided the rules that shaped them.

    </div>
    """), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What each system records about assets, and why

    Each of the shop's systems records what its own work needs. The warehouse keeps column names and types so that it can run a query. Object storage keeps a file's key so that it can serve the file. The reporting tool keeps the values so that it can draw the chart. The warehouse and the reporting tool also keep a little more: an owner, created times and who created the dashboard. None of it says what an asset means or how it was made.

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

    The rule is met as written: the warehouse fills in an owner for every table by itself. The owner it found answers only the last reading, which account controls the table, so you still do not know whom to ask about `daily_sales`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Test an explanation

    Nothing on the platform records how `daily_sales` was made. The usual move is to infer it: find a query over another asset that gives the same rows. The hypothesis below comes with the evidence for each part. Compare it with your guess for `daily_sales` at the end of Chapter 1.

    **`daily_sales` is made from `clean_orders`: completed orders only, `price_pence` × `quantity` added up for each day.**

    - `daily_sales` has two columns, `day` and `revenue_pence`: one total in pence per day.
    - `clean_orders` has `price_pence`, `quantity`, `status` and `ordered_at` for each order.
    - On Thursday, `daily_sales` agrees with `clean_orders`, not with `orders.jsonl`: it is short by exactly the three orders that `clean_orders` lacks.
    - Leaving out cancelled orders is an assumption, that a cancelled order brings in no money. Nothing so far shows whether `daily_sales` counts them.
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
    # Prints True if the query gives exactly the rows of daily_sales, in order.
    rebuilt == warehouse.sql("SELECT * FROM daily_sales ORDER BY day")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.

    The query also explains the other three days that differ. The two cells below list the cancelled orders that `clean_orders` holds, and the orders that `orders.jsonl` holds more than once.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
        SELECT order_id, date(ordered_at) AS day, status, price_pence * quantity AS pence
        FROM clean_orders
        WHERE status = 'cancelled'
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql(
        """
        SELECT order_id, date(ordered_at) AS day, COUNT(*) AS copies
        FROM raw_orders
        GROUP BY order_id
        HAVING COUNT(*) > 1
        """,
        files={"raw_orders": "s3://shop-raw/orders.jsonl"},
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `clean_orders` holds 2 cancelled orders, 7009 on Tuesday, worth 2999 pence, and 7037 on Saturday, worth 2400 pence. The query leaves them out, and so does `daily_sales`: they are Tuesday's and Saturday's gaps. `orders.jsonl` holds order 7015, placed on Wednesday, twice, and `clean_orders` holds it once, so Wednesday's gap is its second copy, worth 4500 pence.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.inferred(week, {'from': 'a table, {rows} rows', 'step': 'Query: completed orders, `price_pence` × `quantity`, per day.', 'fit': 'Inferred: gives all {rows} rows', 'to': 'a table, {rows} rows', 'recorded': 'Nothing: no system records this link.'}), 'The hypothesis as a link from `clean_orders` to `daily_sales`, inferred from the data.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    <div class="ms-found">

    **Established.** A query over `clean_orders` that keeps completed orders and adds up `price_pence` × `quantity` per day gives every row of `daily_sales`. It accounts for every day's gap.

    </div><div class="ms-open">

    **Not established.** That the job that writes `daily_sales` runs this query, or reads `clean_orders` at all. That it did the same every night.

    </div>
    """), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Could have been made, or was made

    The query shows how `daily_sales` **could have been** made, not how it **was** made. Three what-ifs test that difference. Each describes one of three small changes to the shop. None of them happened in the week you have read.

    Each cell below runs the week again with one change, and prints Monday morning's records in a table. The column `the week as it ran` holds the record for the week you have read. The column `with the change` holds the record for the week with the change.

    For each change, ask: does a query over the week's assets still give every row of `daily_sales`, and which records show the change?

    <details><summary>How the last row is found</summary>

    The last row comes from a fixed set of simple queries over the week's assets. Each reads one asset, keeps all, completed or cancelled orders, and adds up revenue, quantity or rows, per day, customer or product. A query is listed if it gives every row of `daily_sales`, even if it gives one row more. The listed queries include, for example `clean_orders: completed orders, revenue per day`, which is the query you ran above.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **An analyst copies `clean_orders` every night.** The copy goes to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night, at 02:15, after the job that writes `clean_orders`.
    """)
    return


@app.cell
def _(shop, week):
    with_copy = shop.run_week(["copy"])
    shop.records_beside(week, with_copy)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The copy is a new file in object storage, `s3://shop-scratch/clean_orders_copy.csv`. The last row now lists two queries: the same query over `clean_orders` and over the copy. Every other record is the same as in the week as it ran. None of the records says which of the two the job that writes `daily_sales` reads. A query that fits is evidence for every source it fits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **From Saturday, the `daily_sales` job keeps unrefunded orders.** Someone on the shop's team edits the job that writes `daily_sales`, so that from Saturday's row on, written early on Sunday 13, it keeps every order that has not been refunded, where it kept completed orders.
    """)
    return


@app.cell
def _(shop, week):
    with_refunds = shop.run_week(["refunds"])
    shop.records_beside(week, with_refunds)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The shop has no refunds: every order's `status` is `completed` or `cancelled`. So from Saturday every order counts, cancelled ones included. The dashboard shows £215.49 instead of £191.49 for Saturday, 2026-09-12. The table still has 7 rows and the same last-altered time. The last row says `none`. No query in the set gives the rows of `daily_sales` any more. No record on the platform says the job was edited.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The `daily_sales` job fails on the last night.** Early on Monday 14, the job that writes `daily_sales` fails and writes nothing.
    """)
    return


@app.cell
def _(shop, week):
    with_failure = shop.run_week(["failed"])
    shop.records_beside(week, with_failure)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found. The query over `clean_orders` is still listed: it gives every row of `daily_sales`, and one row more, for Sunday.

    The shortfall is visible: 6 rows where the week as it ran has 7, and six values on a dashboard titled "Sales, last 7 days". No record says that this is a failure. Seeing it takes knowing to expect 7 rows, or comparing the last-altered times.

    Only a record of the failure would say that a write was due and did not happen.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A rule the week never tests

    A reconstruction can be checked only where the data has something to check.

    In the shop's design, `clean_orders` is made from `orders.jsonl` by four rules. No system records them:

    - keep one row of an order the export wrote twice
    - drop orders with no customer id
    - keep cancelled orders
    - drop orders with a quantity of 0 or less

    The first cell counts the orders in `orders.jsonl` with a quantity of 0 or less. The second lists every setting of the four rules that turns the raw orders into `clean_orders` exactly, one setting per row.
    """)
    return


@app.cell
def _(storage):
    sum(1 for o in storage.records("s3://shop-raw/orders.jsonl") if o["quantity"] <= 0)
    return


@app.cell
def _(shop, week):
    shop.cleaning_rules_that_fit(week)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The count is 0. No order in the week has a quantity of 0 or less.

    So the last rule never removes a row. Two settings fit: one with the rule and one without.

    From the data you cannot tell whether the rule exists. The data can confirm a rule only where some row would have triggered it.

    Your guess for `clean_orders` from Chapter 1 meets the same limit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Records made at the time

    Each question the investigation could not settle needs its own kind of record, and the platform keeps none of them. The figure below sets them side by side.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, shop, week):
    mo.Html(figures.figure(figures.three_records(week, shop.run_week(["copy"]), ('The question', 'What the platform holds', 'The record that would answer it'), [('What is `daily_sales`, and whom do I ask?', '{columns} columns, {rows} rows, last altered {time}; owner `{owner}`, an account', 'A description of the asset: what it means, who is responsible for it.'), ('What is it made from?', "Nothing; a query over `clean_orders` fits, and with the analyst's copy, one over the copy fits too", 'A record of what was made from what (Chapter 6 calls this lineage).'), ("What did each night's job do?", 'Nothing; no record of the job. Failed night: a missing row, older last-altered time.', 'A record of each time a job ran: its code version, inputs, output, time, and whether it succeeded (Chapter 7).')]), 'For `daily_sales`, each question beside what the platform holds and the record that would answer it.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A record of what the job read would have answered the analyst's copy. A record of which version of the job's code ran each night would have answered the edit. A record of whether each night's write succeeded would have answered the failed night.

    Information of this kind, about an asset or about the platform, is called **metadata**: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets. Some of it the systems already keep for their own purposes: the names, types, counts and times you read above. They do not keep what an asset means, what it was made from, or what happened to it. Somebody has to record those. What happened, such as which tables a night's job read, has to be recorded when it happens. What a table is made from can also be read later, from the jobs' code (Chapter 6). That shows what the code says, not what the job did on a given night. A note of what a job read, written the next morning from the data, is a reconstruction, with the limits shown above.

    Real platforms keep more history than the shop's: query logs, table snapshots, audit trails. Those are records made at the time too, kept by the system rather than by a person, and later chapters use them where they exist.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check: evidence of what a job read

    A data engineer wants to know which inputs one particular run of a job read.

    Consider three pieces of evidence they could have. Which is the strongest evidence of what that run read?

    Open an answer to see whether it holds; you can open the others after.

    <details class="ms-choice"><summary>A. The current table schema and its last-modified timestamp.</summary>

    Not the strongest. A schema and a last-modified time describe the table as it is now. The time says when the table last changed, not what the job that wrote it read. With the analyst's copy, every one of these records stayed the same, whichever file the job read.

    Try another answer.

    </details>

    <details class="ms-choice"><summary>B. A SQL query that reproduces the dashboard's current totals.</summary>

    Not the strongest. A query that matches supports a hypothesis about how the totals could be produced. Another source can fit as well: with the analyst's copy, the same query over `clean_orders_copy.csv` gives the same rows. It matches today's totals, not what a past run did: after the edit to the job, no simple query fitted, and nothing said why.

    Try another answer.

    </details>

    <details class="ms-choice"><summary>C. A recorded job-run event identifying the run ID, code version, input tables, output table, timestamp and status.</summary>

    The strongest. It was recorded when the run happened, and it names that run, its code version, the tables it read and wrote, when, and whether it succeeded.

    It is evidence of what the run's instrumentation captured. It is only as complete as that instrumentation: a read the instrumentation did not capture would be missing from the record. So it shows which inputs were recorded, not that the job read nothing else.

    <div class="ms-takeaway">

    **Current metadata describes an asset. A matching reconstruction supports a hypothesis. Recorded execution events provide evidence of a particular run.**

    </div>

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 3

    The platform's state answers what exists. It does not answer what happened or why. Inferring the history from the data gave an explanation that fitted. Three ordinary changes then tested it: the copy made it ambiguous, the edit made it wrong, and one failed night was left that no record names as a failure. The records that would have answered had to be made when the work was done.

    Chapter 3 starts making them: a description of each asset, kept beside the data, with what the asset means and who is responsible for it. It then asks the four questions at the start again. Chapter 6 records what was made from what, which is called lineage, and Chapter 7 records each run of a job.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its people and its data are invented for the course.

    Some real systems keep history that the shop's warehouse does not. An Apache Iceberg table keeps snapshots, each the state of the table at some time. A Delta Lake table keeps, for each write, the operation, the user and the time, for 30 days by default. The shop's systems keep only the current rows.

    In some real databases, a table's owner is an account too. In PostgreSQL, for example, a new table's owner is normally the account that created it. At first, only the owner (or a superuser) can do anything with the table; other accounts can use it once they are given the right to. The right to alter or drop the table comes with being its owner. The shop's warehouse records the owning account and no such rights.

    A file's size is its real size in bytes. A table's size is an estimate from its rows. All times are UTC. A real platform has hundreds or thousands of assets; searching for queries that rebuild one would cost far more. The last row of each table above tries only the fixed set of simple queries. So `none`, in the second what-if, means none of those queries; it says nothing about others. A query with a condition on the date could still reproduce the edited table.

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
