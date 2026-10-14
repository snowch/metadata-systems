# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Conflicting metadata",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 20](chapter_20.ipynb) · [Next: Chapter 22](chapter_22.ipynb)

    # Chapter 21: Conflicting metadata

    **Objectives**

    - Read what three sources claim about one table, and when each claim was sent.
    - Find why "the newest claim wins" shows a claim that nobody has changed for weeks.
    - Try three other rules for choosing, and keep track of where each claim came from.
    - Question the requirement "Show the correct owner."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 20's link, in a browser that had opened and run Chapter 20 (measured on a computer). Chapter 20's link opens this page in a new tab. Chapter 20 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 20 leaves more memory for this page.

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
    ## Three sources

    The shop's metadata system takes what other systems hold about `daily_sales` from three sources.

    - The warehouse: its catalogue, read every night at 03:30. Its owner is the account the warehouse records as the table's owner, `etl_service` (Chapter 2). Its columns are the table's columns.
    - Your records (Chapters 3 and 4), sent when they change. You last changed them on Monday 14 at 16:40, and they name `j.marsh` as responsible.
    - The team sheet: a spreadsheet of owners and columns that the engineer who built the platform wrote before the shop opened. Nobody has edited it since 28 August. It is imported every night at 04:00, and each import sends every row again.

    The shop's metadata system files each source's statement of who owns the table under one attribute, `owner`, and its statement of the columns under `columns`. That is the shop's choice.

    Each source's statement about one attribute is a claim. Each claim keeps two times: when it was sent (`sent`), and when its source's content last changed (`as of`).

    The next cell lists the claims the shop's metadata system holds at 18:00 on Monday 14.
    """)
    return


@app.cell
def _(shop):
    held = shop.claims.claims("2026-09-14T18:00:00Z")
    held
    return (held,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are five claims. Three are about the owner: `etl_service`, `j.marsh` and `data team`. Two are about the columns: `day, revenue_pence` from the warehouse, and `day, revenue` from the team sheet.

    The shop keeps each source's latest sending of each attribute, so each night's import replaces the one before.

    The team sheet's claims were sent at 04:00 on Monday 14, and are as of 28 August.

    One rule for choosing: the claim sent most recently wins. The next cell shows the value this rule gives for each attribute.
    """)
    return


@app.cell
def _(held, shop):
    shop.claims.resolve(held, "newest")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At 18:00 on Monday 14, the owner is `j.marsh`, from your records, sent at 16:40. The columns are `day, revenue`, from the team sheet: its import at 04:00 is newer than the warehouse's read at 03:30. `daily_sales` has no column `revenue`.

    On the night of Monday 14, the shop's nightly work runs as on every other night: the night's work writes `daily_sales` at 02:30:21, the warehouse's catalogue is read at 03:30, and the team sheet is imported at 04:00.

    You do not change your records, and nobody edits the team sheet.

    Before you read on, write in the next cell what this rule will show as the owner at 09:00 on Tuesday 15.
    """)
    return


@app.cell
def _():
    expected_tuesday = """
What owner will the rule show on Tuesday at 09:00?
........
"""
    return


@app.cell
def _(shop):
    tuesday = shop.claims.claims("2026-09-15T09:00:00Z")
    shop.claims.resolve(tuesday, "newest")
    return (tuesday,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At 09:00 on Tuesday 15, the owner is `data team`, from the team sheet. The columns are still `day, revenue`.

    The next cell lists the claims held at 09:00 on Tuesday 15, with the time each was sent.
    """)
    return


@app.cell
def _(tuesday):
    tuesday
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The team sheet's claims were sent at 04:00 on Tuesday 15, the warehouse's at 03:30, and your records' at 16:40 on Monday 14. The team sheet's import is the most recent claim.

    The rule took the claim sent last. The team sheet's content is the oldest of the three: 28 August.

    Compare this with what you wrote.

    When sources disagree, the rule for which claim counts is called **precedence**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Other rules

    The next cell applies another rule to Tuesday's claims: `as of`. The claim whose source's content changed most recently wins.

    The owner is `etl_service` and the columns are `day, revenue_pence`, both from the warehouse.

    The warehouse's content changes every night, at 02:30:21, when the night's work writes `daily_sales`. The warehouse's owner does not change.
    """)
    return


@app.cell
def _(shop, tuesday):
    rule = "as of"
    shop.claims.resolve(tuesday, rule)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Change `"as of"` to `"ranked"` in that cell, select it and press **Run below**.

    `ranked` takes, for each attribute, the claim of the source that comes first in an order the shop chose. For the owner: your records, then the team sheet, then the warehouse. For the columns: the warehouse first.

    The owner is `j.marsh` and the columns are `day, revenue_pence`.

    The order works only while the first source in it has sent a claim. At 12:00 on Monday 14, before your records were sent, `ranked` gave the owner `data team`, from the team sheet.

    Change it to `"all"` and press **Run below**. The cell lists every claim the shop holds, with its source and its two times: five rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The correct owner
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Show the correct owner."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "correct" means to you here, and which owner you would show.
    """)
    return


@app.cell
def _():
    what_correct_means = """
What does "correct" mean here?
........

Which owner would you show?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    "Correct" could mean three things, each needing something different.

    - the newest claim: the time each claim was sent;
    - the claim from the source trusted most for owners: an order of sources for each attribute;
    - every claim, with where it came from: all of them kept, with their sources and times.

    On Tuesday at 09:00, the three give, in that order: `data team`; `j.marsh`; all three owners.

    "Owner" is Chapter 2's word, and the three owners answer different questions: `j.marsh` names a person responsible, `data team` a team, and `etl_service` the account the warehouse records.

    The shop holds all three claims. A rule that shows one claim shows one of these meanings. Keeping every claim leaves the meaning to whoever reads them.

    The requirement names neither a rule nor a meaning, so none of the outputs above is shown to be the correct owner.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 22

    Three sources made five claims about `daily_sales`. Choosing the claim sent most recently let a nightly import of an unchanged sheet replace the owner and keep a column the table does not have. Choosing by the time a source last changed gave the warehouse's account on Tuesday morning, because the table changes every night. An order of sources for each attribute gave `j.marsh` and the warehouse's columns, once your records had been sent. Keeping every claim with its source left the choice to you.

    Chapter 22 asks when references from different systems name the same asset.

    - Which of your platform's sources resend everything on a schedule?
    - Which source would you trust for an owner, and which for a schema?
    - Where does your metadata system record where each value came from?

    ### How this differs from a real platform

    - The shop's sources, their times and the team sheet are invented for the course.
    - The shop keeps the latest claim of each source for each attribute. A real system may keep every claim it has received, with its history.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 20](chapter_20.ipynb) · [Next: Chapter 22](chapter_22.ipynb)

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
