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

    - Compare each day's raw orders in `orders.jsonl` with `daily_sales`, and find which orders Thursday's total leaves out.
    - Read what each of the shop's systems records about an asset, and find what those records do not say: which job wrote the asset, and what it read.
    - Question the requirement "Every table must have an owner."
    - Test an explanation of how `daily_sales` is made, and find what a query that rebuilds `daily_sales` cannot show.

    The head of the shop has sent you one line: "Thursday's revenue looks wrong."

    You investigate it using only what the shop's platform holds, and find where that evidence stops.

    1. [Find the discrepancy](#1.-Find-the-discrepancy)
    2. [What the platform records about its assets](#2.-What-the-platform-records-about-its-assets)
    3. [Test an explanation](#3.-Test-an-explanation)

    [Records made at the time](#Records-made-at-the-time) says which records would have answered; [a short check](#Check:-evidence-of-what-a-job-read) compares evidence of what a job read.
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
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB. On a slow phone, running every cell the first time can take a minute or more. Python starts loading as soon as the page opens, so the wait is shorter if you read the opening before you run anything.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 1's link, in a browser that had opened Chapter 1 (measured on a computer). Chapter 1's link opens this page in a new tab. Chapter 1 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 1 leaves more memory for this page.

    Running every cell took 10 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

    Measured on 13 October 2026, on a computer set to run like a slow phone, with the browser held to a third of one processor core, running every cell as soon as the page showed took 52 seconds on a fast mobile network (9 Mbps) and 101 seconds on a slow one (1.6 Mbps). Running every cell after 45 seconds of reading took 4.5 seconds on the fast network and 55 seconds on the slow one. After a reload, running every cell again at once took 39 to 40 seconds.

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
    SELECT
        d.day,
        r.raw_orders_pence,
        d.revenue_pence,
        CASE
            WHEN r.raw_orders_pence = d.revenue_pence THEN 'same'
            ELSE 'different'
        END AS compared
    FROM daily_sales AS d
    JOIN (
        SELECT
            date(ordered_at) AS day,
            SUM(price_pence * quantity) AS raw_orders_pence
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
    SELECT *
    FROM raw_orders
    WHERE order_id NOT IN (
        SELECT order_id
        FROM clean_orders
    )
        """,
        files={"raw_orders": "s3://shop-raw/orders.jsonl"},
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    <div class="ms-found">

    **Established**

    - Across the whole week, 3 orders in `orders.jsonl` are missing from `clean_orders`: 7021, 7023 and 7025.
    - All three are Thursday's, and none has a customer id.
    - Together they are worth 15400 pence, the whole of Thursday's gap.

    </div><div class="ms-open">

    **Not established**

    - Which rule left them out, which job applied it, and since when.
    - Why Tuesday, Wednesday and Saturday differ: no order from those days is missing from `clean_orders`.

    </div>
    """), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. What the platform records about its assets

    Section 1 read the shop's data: the orders in `orders.jsonl`, and the rows of `clean_orders` and `daily_sales`. Besides that data, each system keeps records about the assets it holds: a record describes the file, the table or the dashboard, and is not an order or a day's revenue.

    The cells below read three of these records:

    - The warehouse's `information_schema` for `daily_sales` (the table, then its columns).
    - The listing of the bucket `shop-raw`.
    - The reporting tool's record of `sales_dashboard`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    As you read them, look for whether any record says which job made `daily_sales`, or what that job read.
    """), kind="info")
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
    SELECT *
    FROM information_schema.tables
    WHERE table_name = 'daily_sales'
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
    SELECT
        column_name,
        data_type
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

    **Established**

    Each record describes an asset as it is this morning.

    - The record for `daily_sales` gives its columns and their types, 7 rows, a size, when it was created, a last-altered time of 02:30 on Monday 14 September, and an owner, `etlsvc/batch01.corp.internal@CORP.INTERNAL`.
    - Each file's record gives its key, size and last-modified time.
    - The dashboard's record gives its title, who created it, when it last refreshed and the values it shows.

    </div><div class="ms-open">

    **Not established**

    - Which job wrote any of these assets.
    - What the job read.
    - Which version of its code ran.
    - What the rows were the day before.
    - Who decided the rules that shaped them.

    </div>
    """), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Every table must have an owner."

    The head of the shop sends a second message: "When a number on the dashboard looks wrong, as Thursday's did, I need to know whom to ask about it."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    A proposed rule for the shop’s platform is: "Every table must have an owner."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The warehouse has a column that looks like the answer. The cell below reads it.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
    SELECT
        table_name,
        table_owner
    FROM information_schema.tables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The warehouse records `etlsvc/batch01.corp.internal@CORP.INTERNAL` in `table_owner` for all three tables. The shop’s four nightly programs use this account.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Does the `table_owner` value tell you whom to ask about Thursday’s revenue? What would you report to the head, and what information is still missing?
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>What does "owner" mean?</summary>

    In real systems, "owner" can have different meanings:

    - **Database owner:** an account recorded as owning the table.
    - **Responsible person:** a named person to contact about the data.
    - **Responsible team:** a team accountable for the data.

    The catalogue does not identify the **producing job**, the program that writes the table. Recording that program would be useful, but would not by itself identify a responsible person or team.

    <div class="ms-box ms-box-requirement">

    For this request, each table needs a named person or team to contact. The shared account in `table_owner` does not provide that information.

    </div>

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Test an explanation

    The usual move is to infer how `daily_sales` was made: find a query over another asset that gives the same rows. The hypothesis below comes with the evidence for each part.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`daily_sales` is made from `clean_orders`: completed orders only, `price_pence` × `quantity` added up for each day.**
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, week):
    mo.Html(figures.figure(figures.hypothesis(week, {'keep': 'Keeps rows where `status` is `completed` (assumed).', 'per': 'The date part of `ordered_at` becomes `day`.', 'measure': '`price_pence` × `quantity` for each order, added up for each day.', 'unused': 'Not used from `clean_orders`: {columns}.'}), 'How `daily_sales` could be made from `clean_orders`, column by column.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - On Thursday, `daily_sales` agrees with `clean_orders`, not with `orders.jsonl`: it is short by exactly the three orders that `clean_orders` lacks.
    - Leaving out cancelled orders is an assumption, that a cancelled order brings in no money. Nothing so far shows whether `daily_sales` counts them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare the hypothesis above with your saved Chapter 1 guess for `daily_sales`. After checking the query below, write what the evidence supports and what remains unknown in the separate explanation box.

    <!-- answer: daily_sales -->
    """)
    return


@app.cell
def _(warehouse):
    rebuilt = warehouse.sql("""
    SELECT
        date(ordered_at) AS day,
        SUM(price_pence * quantity) AS revenue_pence
    FROM clean_orders
    WHERE status = 'completed'
    GROUP BY day
    ORDER BY day
    """)
    # Prints True if the query gives exactly the rows of daily_sales,
    # in order.
    rebuilt == warehouse.sql("SELECT * FROM daily_sales ORDER BY day")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.

    </details>

    The query also explains the other three days that differ. The two cells below list the cancelled orders that `clean_orders` holds, and the orders that `orders.jsonl` holds more than once.
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql("""
    SELECT
        order_id,
        date(ordered_at) AS day,
        status,
        price_pence * quantity AS pence
    FROM clean_orders
    WHERE status = 'cancelled'
    """)
    return


@app.cell
def _(warehouse):
    warehouse.sql(
        """
    SELECT
        order_id,
        date(ordered_at) AS day,
        COUNT(*) AS copies
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

    **Established**

    - A query over `clean_orders` that keeps completed orders and adds up `price_pence` × `quantity` per day gives every row of `daily_sales`.
    - It accounts for every day's gap.

    </div><div class="ms-open">

    **Not established**

    - That the job that writes `daily_sales` runs this query, or reads `clean_orders` at all.
    - That it did the same every night.

    </div>
    """), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Could have been made, or was made

    The query shows how `daily_sales` **could have been** made, not how it **was** made.

    The difference is tested by three small changes to the shop. None of them happened in the week you have read.

    Each cell below runs the week again with one change. It prints Monday morning's records in three columns: `the week as it ran`, `with the change`, and `changed`, which says `yes` where the two differ.

    The equality check above required the query to reproduce `daily_sales` exactly. The last row of these comparisons uses a weaker test: it lists queries that match every existing row of `daily_sales`, even if they return additional rows. Here, "fits" means matching the existing rows; it does not mean reproducing the whole table exactly.

    <details><summary>How the last row is found</summary>

    The last row comes from a fixed set of simple queries over the week's assets. Each reads one asset, keeps all, completed or cancelled orders, and adds up revenue, quantity or rows, per day, customer or product. The listed queries include, for example `clean_orders: completed orders, revenue per day`, which is the query you ran above.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Change 1: an analyst copies `clean_orders` every night

    The copy goes to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night, at 02:15, after the job that writes `clean_orders`.

    Can a query that fits tell two possible sources apart?
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
    <details><summary>The printed result, explained</summary>

    Two records change: object storage has a new file, `s3://shop-scratch/clean_orders_copy.csv`, and the last row lists a second query that fits, over the copy. No record says which of the two the job that writes `daily_sales` reads, and a query that fits is evidence for every source it fits. Only a record of what the job read would settle it.

    <!-- figure: figures.figure(figures.two_sources(shop.run_week(["copy"]), {'table': 'A table with {rows} rows.', 'file': 'A CSV file with {rows} rows.', 'to': 'A table with {rows} rows.', 'fit': 'Inferred: gives all {rows} rows'}), "After Change 1, the same query fits two sources: `clean_orders` and the analyst's copy, each linked to `daily_sales`.") -->

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Change 2: from Saturday, the `daily_sales` job keeps unrefunded orders

    Someone on the shop's team edits the job that writes `daily_sales`. From Saturday's row onwards, it keeps every order that has not been refunded, where it previously kept completed orders. The job writes Saturday's row early on Sunday 13.

    Does an edit to a job leave a trace in the platform's records?
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
    <details><summary>The printed result, explained</summary>

    Two records change: the dashboard shows £215.49 instead of £191.49 for Saturday 12 September, and no query in the set fits any more (the last row says `none`). Saturday changes because the shop has no refunds: every order's `status` is `completed` or `cancelled`, so from Saturday cancelled orders count too. The row count, 7, and the last-altered time do not change, and no record says the job was edited. Only a record of which version of the job's code ran each night would show it.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Change 3: the `daily_sales` job fails on the last night

    Early on Monday 14, the job that writes `daily_sales` fails and writes nothing.

    Does a job that fails show up as a failure?
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
    <details><summary>The printed result, explained</summary>

    Three records change: `daily_sales` has 6 rows, none for Sunday; it was last altered on Sunday at 02:30, a day earlier than `clean_orders`; and the dashboard shows 6 values. The dashboard still refreshed at 03:00 on Monday. The query over `clean_orders` matches every existing row, but also returns Sunday's row. It passes the weaker test used here; it would fail the exact equality check above. The shortfall is there to see if you expect 7 rows or compare the last-altered times, but no record says a write was due and did not happen. Only a record of whether each night's write succeeded would.

    </details>
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

    From the data you cannot tell whether the rule exists. Testing it requires an input that would produce different results with and without the rule.

    Compare this limit with your saved Chapter 1 guess for `clean_orders`. In the separate explanation box, say which parts you can test against these rows and which remain uncertain.

    <!-- answer: clean_orders -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Records made at the time

    Each question the investigation could not settle needs its own kind of record, and the platform keeps none of them.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, shop, week):
    mo.Html(figures.figure(figures.three_records(week, shop.run_week(["copy"]), ('The question', 'What the platform holds', 'The record that would answer it'), [('What is `daily_sales`, and whom do I ask?', '{columns} columns, {rows} rows, last altered {time}; owner `{owner}`, an account', 'A description of the asset: what it means, who is responsible for it.'), ('What is it made from?', "Nothing; a query over `clean_orders` fits, and with the analyst's copy, one over the copy fits too", 'A record of what was made from what (Chapter 6 calls this lineage).'), ("What did each night's job do?", 'Nothing; no record of the job. Failed night: a missing row, older last-altered time.', 'A record of each time a job ran: its code version, inputs, output, time, and whether it succeeded (Chapter 7).')]), 'For `daily_sales`, each question beside what the platform holds and the record that would answer it.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Information of this kind, about an asset or about the platform, is called **metadata**: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets.

    Some of it the systems already keep for their own purposes: the names, types, counts and times you read in section 2, [What the platform records about its assets](#2.-What-the-platform-records-about-its-assets). They do not keep what an asset means, what it was made from, or what happened to it. Somebody has to record those.

    What happened, such as which tables a night's job read, has to be recorded when it happens. What a table is made from can also be read later, from the jobs' code (Chapter 6). That shows what the code says, not what the job did on a given night. A note of what a job read, written the next morning from the data, is a reconstruction, with the limits shown above.

    Real platforms keep more history than the shop's: query logs, table snapshots, audit trails. Those are records made at the time too, kept by the system rather than by a person, and later chapters use them where they exist.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check: evidence of what a job read

    A data engineer wants to know which inputs one particular run of a job read.

    Consider three pieces of evidence they could have. Which is the strongest evidence of what that run read?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Open an answer to see whether it holds; you can open the others after.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details class="ms-choice"><summary>A. The current table schema and its last-modified timestamp.</summary>

    Not the strongest. A schema and a last-modified time describe the table as it is now. The time says when the table last changed, not what the job that wrote it read. With the analyst's copy, every one of these records stayed the same, whichever file the job read.

    Try another answer.

    </details>

    <details class="ms-choice"><summary>B. A SQL query that reproduces the dashboard's current totals.</summary>

    Not the strongest. A query that matches supports a hypothesis about how the totals could be produced. Another source can fit as well: with the analyst's copy, the same query over `clean_orders_copy.csv` gives the same rows. It matches today's totals, not what a past run did: after the edit to the job, none of the queries we tried fitted, and no record explained why.

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
    ## Is Thursday's revenue wrong?

    Write a short reply to the head of the shop. Say what the evidence establishes about Thursday's discrepancy, whether it establishes an error, and what you need to find out before recommending a change.

    <!-- answer: report -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>A possible reply</summary>

    Thursday's gap is accounted for by the orders with no customer id: they appear in `orders.jsonl` but are absent from `clean_orders`. A query over completed orders in `clean_orders` reproduces `daily_sales`. That supports an explanation of the reported total, but does not establish which job or rule produced it.

    We cannot yet say whether the reported revenue is wrong. The available records do not say whether orders with no customer id should count towards revenue. We need an agreed definition of revenue and a person or team responsible for it. We also need the job's rules and records of what it did each night to establish how the total was produced before deciding what to change.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 3

    The platform's state answers what exists. It does not answer what happened or why. Inferring the history from the data gave an explanation that fitted. Three ordinary changes then tested it: the copy made it ambiguous, the edit made it wrong, and one failed night was left that no record names as a failure.

    Chapter 3 starts recording descriptions of assets: what each asset means and who is responsible for it, kept beside the data. It then asks the four questions at the start again. Chapter 6 records what was made from what, which is called lineage, and Chapter 7 records each run of a job.
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
