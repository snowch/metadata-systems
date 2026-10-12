# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Metadata as a graph",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 5](chapter_05.ipynb)

    # Chapter 6: What is lineage?

    **Objectives**

    - Record what each job reads and writes, from its code.
    - Find what a change to one file affects, and what an asset is made from.
    - Test a line written from what a person believes against the code.
    - Find what happens to such lines when a job's code changes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The jobs' code

    The checkout's developer writes:

    > Next week we rename `customer_id` in `orders.jsonl` to `customer_ref`. What does that affect?

    That is the third question from Chapter 2.

    The head of the shop gives you access to the repository where the last engineer kept the jobs' code. In Chapter 1 you could not see the jobs. Now you can read their code.

    The code says what each job does now. It does not say when a job did its work, or what it did on any night.

    Two things that write or read the shop's files are not in the repository:

    - the export, whose code belongs to the checkout's supplier;
    - the analyst's copy of Chapter 2, a script on the analyst's laptop.
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
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 5's link, in a browser that had opened and run Chapter 5 (measured on a computer). Chapter 5's link opens this page in a new tab. Chapter 5 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 5 leaves more memory for this page.

    Running every cell took 9 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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
    The next cell prints the code of the four jobs, one file each. In each file, `read("...")` reads a file from object storage, a table after `FROM` is read from the warehouse, and `write("...")` or `refresh("...")` names what the job writes.
    """)
    return


@app.cell
def _(week, shop):
    repo = shop.repository(week)
    for job in repo:
        print("#", job["file"])
        print(job["code"])
    return (repo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The records cell holds Chapter 5's records, with one line for each of the two files that no line described, so that each is an entity. Under a `#` note, it also has two lines for each job: what the job reads and what it writes, with the attributes `reads` and `writes`, taken from the job's code.

    The two lines for `build_daily_sales` have dots. Fill them in from that job's code, select the cell and press **Run below**. Until you do, the cells below show the dots: the check reports the two lines, and the walks stop at `clean_orders`.
    """)
    return


@app.cell
def _(shop):
    records = shop.typed_records("""
# Chapter 5's records
dataset daily_sales means: the value of every completed order placed that day, by its UTC date
dataset daily_sales responsible: j.marsh
column daily_sales.day of: daily_sales
column daily_sales.revenue_pence of: daily_sales
dataset clean_customers responsible: data_engineering
dataset clean_orders responsible: data_engineering
dataset s3://shop-raw/products.csv responsible: s.lund
dashboard sales_dashboard responsible: j.marsh
person j.marsh team: finance
person s.lund team: catalogue
team finance name: Finance
team catalogue name: Catalogue
team data_engineering name: the data engineer
# The two files no line described
dataset s3://shop-raw/orders.jsonl means: every order the checkout took, as the export writes it
dataset s3://shop-raw/customers.jsonl means: the shop's customers, as the export writes them
# Each job's reads and writes, from its code
job build_clean_customers reads: s3://shop-raw/customers.jsonl
job build_clean_customers writes: clean_customers
job build_clean_orders reads: s3://shop-raw/orders.jsonl
job build_clean_orders writes: clean_orders
job build_daily_sales reads: ........
job build_daily_sales writes: ........
job refresh_dashboard reads: daily_sales
job refresh_dashboard writes: sales_dashboard
""")
    records
    return (records,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The model cell adds a type, `job`, with two attributes:

    - `job reads: dataset`: the value of `reads` on a job is a dataset.
    - `job writes: dataset or dashboard`: the value of `writes` is a dataset or the dashboard.

    Until now, a job has been a plain word. Now it is an entity: a node between the assets it reads and the assets it writes.
    """)
    return


@app.cell
def _(shop):
    model = shop.model("""
dataset means: text
dataset responsible: person or team
column of: dataset
dashboard responsible: person or team
person team: team
team name: text
job reads: dataset
job writes: dataset or dashboard
""")
    model
    return (model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lineage

    The next cell draws only the `reads` and `writes` edges, between the assets and the jobs. This is the platform from Chapter 1, drawn with arrows at last, because your lines now record what each job reads and writes. An arrow from an asset to a job means the job reads it. An arrow from a job to an asset means the job writes it.

    Records of what was made from what, and by which job, are **lineage**.

    The drawing has 3 parts:

    - `orders.jsonl` to `sales_dashboard` through three jobs;
    - `customers.jsonl` to `clean_customers` through one job;
    - `products.csv`, which no job reads.
    """)
    return


@app.cell
def _(model, records, shop):
    lineage = shop.graph(records, model).only(["reads", "writes"], ["dataset", "dashboard", "job"])
    lineage.drawing(label="The drawing shows the chain from orders.jsonl through three jobs to sales_dashboard, the chain from customers.jsonl through one job to clean_customers, and products.csv with no arrow to a job.")
    return (lineage,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What a change to `orders.jsonl` affects

    Before you read on, write which assets a change to `orders.jsonl` affects, in the next cell. The cell gives no result. Write your answer in its dots.
    """)
    return


@app.cell
def _():
    expected = """
Which assets does a change to orders.jsonl affect,
and why?
........
"""
    return


@app.cell
def _(lineage):
    lineage.downstream("s3://shop-raw/orders.jsonl")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell above walked from `orders.jsonl` to each job that reads it, then to what that job writes, and on. What is made from an asset in this way is **downstream** of it.

    Downstream of `orders.jsonl` there are 6 nodes. The 3 jobs are `build_clean_orders`, `build_daily_sales` and `refresh_dashboard`. The 3 assets are `clean_orders`, `daily_sales` and `sales_dashboard`.

    The opposite walk goes from an asset to the job that writes it, then to what that job reads, and on. What an asset is made from in this way is **upstream** of it.

    The next cell walks back from `sales_dashboard`.
    """)
    return


@app.cell
def _(lineage):
    lineage.upstream("sales_dashboard")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Upstream of `sales_dashboard` there are 6 nodes. The farthest back is `orders.jsonl`. `customers.jsonl` and `clean_customers` are not upstream of the dashboard.

    The next cell walks downstream from `products.csv`.
    """)
    return


@app.cell
def _(lineage):
    lineage.downstream("s3://shop-raw/products.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Downstream of `products.csv` there is nothing. No job in the repository reads it. Chapter 2 asked "Does anything still read it?" As far as the lines go, the answer is no.

    The lines record only the jobs in the repository. The export and the analyst's script are not in the repository, and no line records what they read. So "nothing reads `products.csv`" means only that the lines know of no reader.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A line from a belief

    Jo Marsh says that the daily sales job leaves out test customers, so it reads `clean_customers`. Jo has not read the code. Written as a line, the belief is:

    `job build_daily_sales reads: clean_customers`

    The next cell adds that line to your records and walks downstream from `customers.jsonl`.
    """)
    return


@app.cell
def _(model, records, shop):
    jos_line = "job build_daily_sales reads: clean_customers"
    with_jo = shop.typed_records(records.text + "\n" + jos_line + "\n")
    shop.graph(with_jo, model).downstream("s3://shop-raw/customers.jsonl")
    return (with_jo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With that line, downstream of `customers.jsonl` reaches 6 nodes, `daily_sales` and `sales_dashboard` among them. A change to `customers.jsonl` now seems to affect the dashboard.

    The next cell compares each job's lines with its code. It lists one row for each line the code does not bear out, and one row for each read or write in the code that no line records.
    """)
    return


@app.cell
def _(repo, shop, with_jo):
    shop.compare_with_code(with_jo, repo)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The comparison lists one row: Jo's line. The code of `build_daily_sales` does not read `clean_customers`, and nothing in it leaves out test customers.

    A line written by hand records what someone believes. The code is evidence of what the job reads now.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A line gone stale

    Suppose that from Saturday, the daily sales job, `build_daily_sales`, is changed to read the analyst's copy of `clean_orders` instead of `clean_orders`. The copy is Chapter 2's `clean_orders_copy.csv`, in the bucket `shop-scratch`. It holds the same rows.

    Your lines were written from the code as it is today.

    Before you read on, write in the next cell whether the comparison will report anything after the change, and whether the rows of `daily_sales` will change.
    """)
    return


@app.cell
def _():
    expected_change = """
Will the comparison report anything after the change?
........
Will the rows of daily_sales change?
........
"""
    return


@app.cell
def _(records, shop):
    changed = shop.run_week(["source"])
    shop.compare_with_code(records, shop.repository(changed))
    return (changed,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell runs the week with the change, and compares your lines with the code as it is after the change. It finds 2 rows. Your line says `build_daily_sales` reads `clean_orders`, and its code no longer does. Its code reads `s3://shop-scratch/clean_orders_copy.csv`, and no line says so.

    Your lines went stale when the code changed, and nothing changed them.

    The next cell compares the rows of `daily_sales` in the changed week with today's.
    """)
    return


@app.cell
def _(changed, warehouse):
    changed.warehouse.sql("SELECT * FROM daily_sales") == warehouse.sql("SELECT * FROM daily_sales")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `True`: the rows of `daily_sales` are the same in the changed week as today. The data shows no change. Only the code does.

    The code shows what the job does now. It does not say which nights the job read `clean_orders` and which nights it read the copy. A record made each time the job does its work would say so. Chapter 7 makes such records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Record the lineage of `daily_sales`."

    The head of the shop's requirement is "Record the lineage of `daily_sales`." Before you read on, write in the next cell what you would record, and from what.
    """)
    return


@app.cell
def _():
    reading = """
What would you record?
........
From what?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The requirement could mean four things:

    - **What someone says the job reads.** Needs someone to write it down. A line like Jo's records a belief.
    - **What the job's code reads now.** Needs the repository, which is evidence of today.
    - **What the job read on each night.** Needs a record made each time the job does its work. Nothing on the platform makes one (Chapter 7).
    - **Which tables, or which columns, `daily_sales` is made from.** Needs the input columns of each output column. For example, `revenue_pence` is made from `price_pence` and `quantity` of `clean_orders`. Lines between tables do not say so (Chapter 10).

    Your lines meet the requirement as written, and agree with the code today. None of them says what the job read on each night, or which columns `revenue_pence` comes from.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 7

    The experiments showed three things. Lines of what each job reads and writes let the graph answer what a change to a file affects, and what an asset is made from. A line from a belief made the dashboard seem to depend on `customers.jsonl`, until the code was compared with the line. A line written from today's code went stale when the code changed, and the data did not show it.

    The experiments could not show what each job read on each night, or what the export and the analyst's script read.

    Chapter 7 records each time a job does its work: when it started and ended, which version of its code it used, what it read and wrote, and whether it succeeded.

    - Take a platform you work on. Which of its lineage lines were written by hand, and which came from its code? How would you find out that one of them is stale?
    - A job reads its input table's name from a configuration file. Which of your lines could be false while the code still looks the same?
    - Which nights did the job read `clean_orders`, and which nights did it read the copy? What would you need in order to find out?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its people, its jobs and its repository are invented for the course.

    The shop's jobs are short, and what each reads is found with a small rule: `read("...")`, and a table after `FROM` or `JOIN`. Real code can hide what it reads in functions, variables or SQL built while the job executes. No small rule finds all of it.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 5](chapter_05.ipynb)

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
