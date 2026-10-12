# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Root-cause analysis",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 16](chapter_16.ipynb)

    # Chapter 17: Root-cause analysis

    **Objectives**

    - Follow a wrong total on the dashboard back to the step where it went wrong.
    - Find two causes that each explain a total, and tell them apart.
    - Find where the shop's records end.
    - Question the requirement "Find the cause of the wrong total."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 16's link, in a browser that had opened and run Chapter 16 (measured on a computer). Chapter 16's link opens this page in a new tab. Chapter 16 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 16 leaves more memory for this page.

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
    3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.
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
    ## "Thursday's revenue looks wrong."

    Chapter 2 began with a message from the head of the shop: "Thursday's revenue looks wrong." The dashboard shows £51.50 for Thursday 10.

    The shop now records each run and its code as it was that night (Chapter 7). It also records what each run of `build_clean_orders` counted (Chapter 14). Object storage keeps every version of each file, with the time it was written.

    Before you read on, write in the next cell where you would look first, and what would show you that you had found the cause.
    """)
    return


@app.cell
def _():
    where_to_look = """
Where would you look first,
and what would show you had found the cause?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Back from Thursday's total

    The next cell starts from the dashboard's value for Thursday and steps back through `daily_sales`, then `clean_orders`, then the version of `orders.jsonl` that was current when `build_clean_orders` started.

    At each step, the code in the cell measures Thursday's revenue the way `build_daily_sales` defines it: price times quantity over the day's completed orders, each order once.

    For each step, the output lists whether the total differs from the step's input. It also lists whether the code of the program that made the step changed since the night before.
    """)
    return


@app.cell
def _(shop):
    week17 = shop.run_week()
    shop.cause.search(week17, "2026-09-10")
    return (week17,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dashboard, `daily_sales` and `clean_orders` each hold 5150 pence for Thursday. The version of `orders.jsonl` written at 01:00 on Friday 11 holds 20550 pence.

    The difference first appears in `clean_orders`. It was made by `run-014`, `build_clean_orders`, early on Friday 11, and its code had not changed since the night before.

    The last row is the checkout. The shop records nothing about what the export read, so the steps end at `orders.jsonl`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Two causes

    `run-014` counted 3 rows with no customer id in the file it read (Chapter 14). Those are Thursday's three orders.

    Two things together made Thursday's total low. The checkout sent three orders with no customer id. And `build_clean_orders` drops orders with no customer id, by a rule that was in its code all week. Change either, and the total would have counted the three orders.

    A cause that, if removed, would stop a fault happening again is a **root cause**. Here, each of the two causes meets that definition.

    Of the two causes, the shop's records show that the data changed and the code did not. The checkout is outside the shop's records: no record shows why it sent orders with no customer id.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Saturday that is too high

    The next week has Chapter 2's change `refunds`. From Saturday's row on, `build_daily_sales` keeps every order that is not refunded. Before that, it kept completed orders. The dashboard shows £215.49 for Saturday 12.

    The next cell searches back from Saturday's total. Before you read on, decide at which step you expect the difference to appear, and whether a code change will show.
    """)
    return


@app.cell
def _(shop):
    week17r = shop.run_week(["refunds"])
    day = "2026-09-12"
    shop.cause.search(week17r, day)
    return (week17r,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The difference first appears in `daily_sales`: 21549 pence, where `clean_orders` holds 19149 for Saturday. `daily_sales` was made by `run-023`, `build_daily_sales`, early on Sunday 13. Its code had changed since the night before.

    Two explanations fit. The first is the change to the code. The second is Saturday's cancelled order 7037, 2 sets of brake pads, 2400 pence, which is the difference.

    Tuesday 8 also had a cancelled order, 7009. Change `day = "2026-09-12"` to `day = "2026-09-08"`, select the cell and press **Run below**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For Tuesday, no step differs. Every step holds 16225 pence, and no code had changed.

    A cancelled order alone did not change the total. With the code as it was when Tuesday's row was written, the cancelled order was left out. The change to the code explains Saturday's total.

    The next cell prints the lines of `build_daily_sales`'s code that changed for the work early on Sunday 13.
    """)
    return


@app.cell
def _(shop, week17r):
    print(shop.cause.code_change(week17r, "build_daily_sales", "2026-09-13"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `status = 'completed'` became `status <> 'refunded'`.

    The shop's records show what changed and the first run that used it. They do not show why it was changed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Find the cause of the wrong total."

    The head of the shop's requirement: "Find the cause of the wrong total."

    Before you read on, write in the next cell what you would give as the cause of Thursday's total.
    """)
    return


@app.cell
def _():
    the_cause = """
What is the cause of Thursday's total?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "The cause" could mean three things, each needing something different:
    - where the data first went wrong: each step measured the same way, and the versions of what each run read;
    - the change that did it: each run's code, and what each run counted;
    - the decision behind that change: a record of who decided it and why.

    For Thursday:
    - where: two answers fit. `orders.jsonl` already held the three orders with no customer id; the total first changes in `clean_orders`.
    - the change: none in the shop's records. The code did not change; the checkout's change is outside them.
    - the decision: none recorded.

    For Saturday, with `refunds`:
    - where: `daily_sales`, made by `run-023`.
    - the change: the edit to `build_daily_sales`, shown by the code each run recorded.
    - the decision: none recorded.

    The requirement does not say which of the three it means. Compare these with what you wrote.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 18

    From Thursday's total, the steps back found where the difference first appeared, in a run whose code had not changed. They ended at the checkout, which is outside the shop's records. Two causes explained the total. From Saturday's, they found a code change. A day with the same kind of order and no change ruled out the other explanation.

    The records could not show why either the checkout or the code changed.

    Part IV used the shop's record of every run. Every run's events arrived, each once and in order.

    Chapter 18, the first chapter of Part V, asks what the shop's records hold when an event never arrives.

    - Where does your platform's record end, upstream?
    - How would you tell a change to the data from a change to the code?
    - Where are the reasons for a change to your code kept, if anywhere?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    - The shop's faults are invented for the course.
    - The search measures one thing, a day's revenue, the same way at every step. A fault that does not change that total, such as an order counted against the wrong customer, would not show.
    - The search reads files in the version current when each run started, and tables as they are now (Chapter 15).
    - The shop's repository keeps each program's code. It records no reason for a change.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 16](chapter_16.ipynb)

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
