# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Metadata platforms",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 30](chapter_30.ipynb) · [Next: Chapter 32](chapter_32.ipynb)

    # Chapter 31: Metadata platforms

    **Objectives**

    - Compare four metadata platforms: how metadata arrives, how it is modelled, where it is kept and how it is searched.
    - Put the three owners of `daily_sales` into each platform, under its rule for an owner.
    - Choose DataHub's ownership types for the three owners, and find what a reader can tell from them.
    - Question the requirement "Choose a metadata platform that tracks ownership."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 30's link, in a browser that had opened and run Chapter 30 (measured on a computer). Chapter 30's link opens this page in a new tab. Chapter 30 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 30 leaves more memory for this page.

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
    ## Four platforms

    A metadata platform receives metadata from many systems, keeps it, and answers questions about it, as the shop's store, collector, graph and pages did in Part VI.

    DataHub, OpenMetadata, Apache Atlas and Marquez are four such platforms.

    As in Chapters 29 and 30, none of them runs here. The next cell sets out, from each project's documentation and code, how metadata arrives, how it is modelled, where it is kept and how it is searched.
    """)
    return


@app.cell
def _(shop):
    shop.platforms.architectures()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    DataHub and OpenMetadata take metadata both ways: connectors pull it on a schedule, and other systems push it. Atlas takes it pushed, from hooks inside other systems or through its API. Marquez takes OpenLineage events, as in Chapter 29.

    Each keeps its metadata in a database and searches it through an index. Atlas keeps it as a graph.

    Chapter 27 found three owners of `daily_sales`: the account `etl_service`, the person responsible `j.marsh`, and the team `data team`.

    Each platform has a rule for an owner, as its code states it:

    - DataHub: a list of owners. Each is a user or a group, and has an ownership type: `TECHNICAL_OWNER`, `BUSINESS_OWNER`, `DATA_STEWARD`, `NONE`, or a type the organisation defines.
    - OpenMetadata: a list of owners. Each is a user, or a team whose type is `Group`. An owner has no ownership type.
    - Atlas: one text value, `owner`, on each asset, which may be left empty.
    - Marquez: no owner on a dataset. A namespace has one, and a namespace made from an OpenLineage event gets the owner `anonymous`.

    Before you read on, write in the next cell which platforms keep all three owners of `daily_sales`.
    """)
    return


@app.cell
def _():
    expected_owners = """
Which platforms will keep all three owners of daily_sales?
........
"""
    return


@app.cell
def _(shop):
    shop.platforms.owners_in()
    return


@app.cell
def _(shop):
    shop.platforms.kept()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    DataHub and OpenMetadata keep all three. Atlas keeps one, here the first, `etl_service`. Marquez keeps none.

    Compare this with what you wrote.

    The first table gives DataHub's three owners the same ownership type, `TECHNICAL_OWNER`, so the second table shows that none of them can be told from the others by its type. OpenMetadata's owners carry no type at all.

    The next cell holds `types`: the ownership type each of the three owners gets in DataHub. As it stands, each is `TECHNICAL_OWNER`.

    Change them so that each owner has its own type. A type of your own is written `urn:li:ownershipType:` followed by a name. Select the cell and press **Run below**.

    The check below it holds each type to DataHub's rule, and asks whether the three owners can be told apart.
    """)
    return


@app.cell
def _():
    types = {
        "account": "TECHNICAL_OWNER",
        "responsible": "TECHNICAL_OWNER",
        "team": "TECHNICAL_OWNER",
    }
    return (types,)


@app.cell
def _(shop, types):
    shop.platforms.check(types)
    return


@app.cell
def _(shop, types):
    shop.platforms.kept(types)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With three different types, both tests pass, and the table below the check shows all 3 of DataHub's owners told apart by type.

    A type tells the owners apart, but DataHub's own names do not say which question each owner answers: `BUSINESS_OWNER` does not say "whom to ask". A type the organisation defines can carry its own description.

    OpenLineage has a facet for a dataset's owners too: each owner has a name and an optional type, both as text.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A platform that tracks ownership
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The head of the shop's requirement: "Choose a metadata platform that tracks ownership."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before you read on, write in the next cell what "tracks ownership" means to you here.
    """)
    return


@app.cell
def _():
    what_tracks_means = """
What does "tracks ownership" mean here?
........
"""
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It could mean three things. Each item below says what it needs and which platforms meet it:

    - keeps an owner for each dataset: DataHub, OpenMetadata and Atlas do; Marquez keeps none on a dataset.
    - keeps whom to ask: it needs a person. DataHub and OpenMetadata can hold `j.marsh` as a user, and Atlas can hold one name as text.
    - keeps which meaning each owner holds: it needs a type for each owner. Of the four, only DataHub keeps one.

    Each platform meets some of these readings. The requirement does not say which it means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 32

    DataHub and OpenMetadata kept all three owners of `daily_sales`, Atlas one and Marquez none.

    Only DataHub's ownership types let a reader tell the three apart, and only when each had its own type.

    The page could not show the platforms themselves: each result is a platform's rule, as its code states it, applied here.

    Chapter 32 follows the metadata of a forecast trained on the shop's data.

    - Which meaning of "owner" does your platform keep?
    - Can a reader of your platform tell one owner's meaning from another's?
    - Which of your datasets have no owner at all?

    ### How this differs from a real platform

    - The table and the rules come from each project's documentation and code in the version read. Each platform keeps much more than an owner.
    - DataHub's list of ownership types here leaves out six that its schema marks as no longer to be used.
    - Atlas has room for one owner; which of the three it holds depends on what writes it.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 30](chapter_30.ipynb) · [Next: Chapter 32](chapter_32.ipynb)

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
