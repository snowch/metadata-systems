# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Metadata as a model",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 3](chapter_03.ipynb)

    # Chapter 4: Metadata as a model

    **Objectives**

    - Count the owners that the records name, and find out why the count is not a count of people.
    - Merge two spellings of one person into one, and write a model that the records can be checked against.
    - Decide what to do with a fact the model has no place for.
    - Question the requirement "Each asset has one owner."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Who owns what

    It is still Monday 14 September 2026, late in the afternoon. The head of the shop sends you a requirement:

    > Each asset has one owner. Send me the list.
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

    The page downloaded less than 1 MB when opened from Chapter 3's link, in a browser that had opened and run Chapter 3 (measured on a computer). Chapter 3's link opens this page in a new tab. Chapter 3 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 3 leaves more memory for this page.

    Running every cell took 9 to 12 seconds, and the page used about 410 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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
    You have your records from Chapter 3. Jo Marsh, in finance, has sent the notes Jo keeps about the dashboard and `daily_sales`. The first cell puts both together, in Chapter 3's notation: your records first, then Jo's notes.

    Each group of lines starts with a `#` note that says where the lines come from. Your records hold your record of `daily_sales` from Chapter 3, five lines with Jo Marsh as responsible. They also hold three lines from the head of the shop's message in Chapter 3: the data engineer is responsible for `clean_customers` and `clean_orders`, and Sam Lund is responsible for `products.csv`. The last part of your records is one line from the orders Chapter 2 found missing on Thursday: `clean_orders drops: orders with no customer id`. Jo's notes say what `sales_dashboard` means, and name `j.marsh` as responsible for `sales_dashboard` and for `daily_sales`.

    The head's word is "owner". The lines that the head's list counts are the `responsible` lines: Chapter 3 defined `responsible` as who to ask about an asset. The warehouse's owner, the account `etl_service` that Chapter 2 found, answers a different question: which account controls a table. The head's list does not ask for that.
    """)
    return


@app.cell
def _(shop):
    yours = """
# Your own record of `daily_sales`, written in Chapter 3
daily_sales means: the value of every completed order placed that day, by its UTC date
daily_sales responsible: Jo Marsh
daily_sales day means: the UTC date the orders were placed
daily_sales revenue_pence means: the value of the day's completed orders
daily_sales revenue_pence unit: pence
# Three lines from the head of the shop's message
clean_customers responsible: the data engineer
clean_orders responsible: the data engineer
s3://shop-raw/products.csv responsible: Sam Lund
# One line from the Thursday orders Chapter 2 found missing
clean_orders drops: orders with no customer id
"""
    jos = """
# Jo Marsh's notes; Jo Marsh works in finance
sales_dashboard means: revenue per day, for the last 7 days
sales_dashboard responsible: j.marsh
daily_sales responsible: j.marsh
"""
    together = shop.records(yours + jos)
    together
    return (together,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Run the next cell to list every line whose field is `responsible`.
    """)
    return


@app.cell
def _(together):
    together.sql("SELECT asset, value AS responsible FROM records WHERE field = 'responsible' ORDER BY asset")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write your answer in the next cell. The cell gives no result. Fill in its blanks with your answer and how you decided.
    """)
    return


@app.cell
def _():
    expected = """
Will the count of different values of
responsible in these records be the number of
people responsible for the shop's assets, more
than that, fewer, or can you not tell yet?
........
How I decided:
........
"""
    return


@app.cell
def _(together):
    together.sql("SELECT COUNT(DISTINCT value) AS owners FROM records WHERE field = 'responsible'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell counts 4 different values of `responsible`: the data engineer, Jo Marsh, `j.marsh` and Sam Lund.

    The count is of spellings, not people. Jo Marsh and `j.marsh` may be one person, and the records do not say whether they are. The head of the shop said in Chapter 3 that Jo Marsh built the dashboard, and the reporting tool records `j.marsh` as the dashboard's creator. That supports one person. It does not prove it, because to the records each name is still a piece of text.

    As written, `daily_sales` has two owners: Jo Marsh, from your records, and `j.marsh`, from Jo's notes.

    You ask the head of the shop who `j.marsh` and `s.lund` are. The head answers that `j.marsh` is Jo Marsh, in finance, and `s.lund` is Sam Lund, in catalogue. So `j.marsh` and Jo Marsh are one person. You started today and have no line of your own yet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What the records describe

    To count people, the records must describe people. Each line must also say what kind of thing it describes.

    A thing the records describe is an **entity**: a table, a file, a column, the dashboard, a person or a team. Each entity has a type. An asset, the word Chapter 1 used, is an entity of type `dataset` or `dashboard`.

    A named property that every entity of a type can have is an **attribute**, such as `means` or `name`. Each line gives the value of one attribute of one entity.

    A value that names exactly one entity of its type, and that every line uses for it, is an **identifier**. `j.marsh` can serve as one if every line uses it for Jo Marsh. The staff logins, `j.marsh` and `s.lund`, can serve as identifiers. So are a table's name in the warehouse and a file's key in object storage.

    A file and a table both hold rows under named columns. The same attributes describe both: what they mean and who is responsible for them. One type covers both. It is a **dataset**: a file or a table of rows.

    Each column is an entity of its own, of type `column`. The dashboard shows values but holds no rows of its own and has no columns. So it does not fit the dataset type, and no column belongs to it. It has a type of its own, `dashboard`.

    In this chapter's notation, each line starts with the type of the thing, then its identifier, then the attribute, a colon and the value:

    `dataset daily_sales responsible: j.marsh`

    `person j.marsh name: Jo Marsh`

    A column's identifier is its table's name and its own name joined by a dot. For example, `daily_sales.revenue_pence` is the column `revenue_pence` in `daily_sales`.

    The records cell, the one that starts `records = shop.typed_records`, holds the first cell's lines in this notation. It adds the head's answer about the two logins: two people, each with a name and a team, and the two teams.
    """)
    return


@app.cell
def _(shop):
    records = shop.typed_records("""
dataset daily_sales means: the value of every completed order placed that day, by its UTC date
dataset daily_sales responsible: Jo Marsh
column daily_sales.day means: the UTC date the orders were placed
column daily_sales.revenue_pence means: the value of the day's completed orders
column daily_sales.revenue_pence unit: pence
dataset clean_customers responsible: the data engineer
dataset clean_orders responsible: the data engineer
dataset s3://shop-raw/products.csv responsible: Sam Lund
dataset clean_orders drops: orders with no customer id
dashboard sales_dashboard means: revenue per day, for the last 7 days
dashboard sales_dashboard responsible: j.marsh
dataset daily_sales responsible: j.marsh
person j.marsh name: Jo Marsh
person j.marsh team: finance
person s.lund name: Sam Lund
person s.lund team: catalogue
team finance name: Finance
team catalogue name: Catalogue
""")
    records
    return (records,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A model of the records

    A model says which types there are, which attributes each type has, and what each attribute's value is. The value is either text, or the identifier of an entity of another type.

    An attribute whose value is the identifier of an entity of another type links the two entities. `responsible` links a dataset or the dashboard to a person or a team. An attribute of this kind is a relationship type.

    The model has one line per attribute: the type, the attribute, a colon, and what the value is. The value is `text`, or one or more type names joined by `or`. For example, `dataset responsible: person or team` says that the value of `responsible` on a dataset names a person or a team.

    The model cell defines the types `dataset`, `column`, `dashboard`, `person` and `team`.
    """)
    return


@app.cell
def _(shop):
    model = shop.model("""
dataset means: text
dataset responsible: person or team
column means: text
column unit: text
dashboard means: text
dashboard responsible: person or team
person name: text
person team: team
team name: text
""")
    model
    return (model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The check cell compares the records with the model. It lists every line whose type or attribute the model does not have, and every value that should be the identifier of a person or a team and is not.
    """)
    return


@app.cell
def _(model, records):
    model.check(records)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before your change, the check lists 5 problems. Of these, 4 are lines whose `responsible` value is not the identifier of a person or team in the records:

    - `daily_sales` has `responsible` Jo Marsh.
    - `products.csv` has `responsible` Sam Lund.
    - `clean_customers` has `responsible` the data engineer.
    - `clean_orders` has `responsible` the data engineer.

    The fifth problem is `drops` on `clean_orders`. The model gives a dataset no attribute called `drops`.

    In the records cell, the one that starts `records = shop.typed_records`, change `responsible: Jo Marsh` to `responsible: j.marsh`, and change `responsible: Sam Lund` to `responsible: s.lund`. Then select the cell and press **Run below**.

    The check then lists 3 problems. `daily_sales` now has two identical lines, `dataset daily_sales responsible: j.marsh`. They state one fact twice, so `daily_sales` has one owner. The spelling Jo Marsh is kept, as the `name` of the person `j.marsh`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next cell counts the different `responsible` values in these records. Before your change it counts 4. After your change it counts 3: `j.marsh`, `s.lund` and the data engineer, one value for each person or role.
    """)
    return


@app.cell
def _(records):
    records.sql("SELECT COUNT(DISTINCT value) AS owners FROM records WHERE attribute = 'responsible'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "The data engineer" is a role, not one of the two people on the head's list, and no line describes it. The section on the requirement makes it a person or a team, by your choice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A fact the model has no type for

    After the merge, the check still refuses this line:

    `dataset clean_orders drops: orders with no customer id`

    The model gives a dataset no attribute called `drops`. It is the rule Chapter 2 found behind Thursday's missing orders. The model has no place for it.

    You have two choices.

    - Leave the model as it is. The check keeps refusing the line, and the line is lost from any records kept to the model.
    - Add the line `dataset drops: text` to the model cell, and press **Run below**. The check then lists 2 problems, and the model accepts the line as text. Then any dataset can have any text about what it drops. No check can say whether that text is true, or whether the job that writes the table applies that rule.

    Whoever writes the model decides which facts the records can hold, and which of those a check can test.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Each asset has one owner."

    The head of the shop's requirement is "Each asset has one owner." In the cell below, write what you would send the head, and what you take "one owner" to mean. The readings follow the cell.
    """)
    return


@app.cell
def _():
    reading = """
What list would you send the head?
........
What does "one owner" mean to you?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - As written, `one_owner`: exactly one `responsible` value for the asset.
    - One person to ask, `one_person`: exactly one value, and it names a person.
    - One team that answers for it, `one_team`: exactly one team, named directly or as the team of the person named.

    Each needs identifiers, so that two spellings of one owner count once.

    The next cell applies your two changes to the records if you have not made them. It makes the data engineer either a team or a person, with the identifier `data_engineering`. The line `the_data_engineer = "team"` sets which. To make the data engineer a person, change the line to `the_data_engineer = "person"` and press **Run below**. The cell then lists the 7 assets with their `responsible` values, and a `yes` or `no` for each reading: `one_owner`, `one_person` and `one_team`.
    """)
    return


@app.cell
def _(records, shop, week):
    the_data_engineer = "team"
    after = shop.typed_records(
        records.text.replace("responsible: Jo Marsh", "responsible: j.marsh")
        .replace("responsible: Sam Lund", "responsible: s.lund")
        .replace("responsible: the data engineer", "responsible: data_engineering")
        + f"\n{the_data_engineer} data_engineering name: the data engineer\n"
    )
    shop.owners(week, after)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the data engineer as a team, 5 of the 7 assets have one owner under `one_owner`, 3 have one person under `one_person`, and 5 have one team under `one_team`. With the data engineer as a person, the counts are 5, 5 and 3 (the person `data_engineering` has no team).

    `orders.jsonl` and `customers.jsonl` have no `responsible` line in the records, so they fail every reading.

    No reading holds for all 7 assets. The head did not say which one was meant. A list you send should say which reading it meets, and for which assets.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 5

    With a type on each line and an identifier for each person, the count of `responsible` values went from 4 to 3, one for each person or role. A check can find a value that names nothing the records describe. The check refused the line about what `clean_orders` drops, because the model had no attribute for it, until the model was changed. No reading of the requirement holds for every asset. Neither `orders.jsonl` nor `customers.jsonl` meets any reading.

    The checks could not show whether a line is true. The check tests a value's form, and whether the value names an entity the records describe. It does not test whether Jo Marsh is really responsible.

    The lines now point from one entity to another: a dataset to a person, and a person to a team. Chapter 5 follows them from one entity to the next.

    - Take a platform you work on. Which of the three readings of "Each asset has one owner" does its owner field meet, and what would it need in order to meet the others?
    - Which line on that platform could a check accept while the line is false? What would a check need in order to test it?
    - A person leaves, and their login is given to someone else. Which records would then name the wrong person, and how would you find out?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its people, its staff list and its data are invented for the course.

    The record notation and the model notation are the course's own. Real metadata systems each define their own types and attributes. Chapter 31 compares some of them.

    The shop uses staff logins as identifiers for people. A login can change, or be given to someone else after a person leaves. The shop's staff list does not record when.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 3](chapter_03.ipynb)

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
