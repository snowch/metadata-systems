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
    ## Four platforms

    A metadata platform receives metadata from many systems, keeps it, and answers questions about it, as the shop's store, collector, graph and pages did in Part VI.

    DataHub, OpenMetadata, Apache Atlas and Marquez are four such platforms.

    As in Chapters 29 and 30, none of them runs here. The next cell sets out, from each project's documentation and code in the version read, how metadata arrives in each, how it is modelled, where it is kept and how it is searched.
    """)
    return


@app.cell
def _(shop):
    shop.platforms.architectures()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The owners of `daily_sales`

    Chapter 27 found three owners of `daily_sales`: the account `etlsvc/batch01.corp.internal@CORP.INTERNAL`, the person responsible `j.marsh`, and the team `data team`.

    Each platform has a rule for an owner, as its code states it:

    - DataHub: a list of owners. Each owner is a user or a group, named by a URN, which is DataHub's form of name: `urn:li:corpuser:` and a user's name, or `urn:li:corpGroup:` and a group's name. Each owner has an ownership type, also named by a URN. DataHub defines four, from `urn:li:ownershipType:__system__technical_owner` to `urn:li:ownershipType:__system__none`, each with a name and a description, and an organisation can define more.
    - OpenMetadata: a list of owners. Each is a user, or a team whose team type is `Group`. An owner has no ownership type.
    - Atlas: one text value, `owner`, on each asset, which may be left empty.
    - Marquez: no owner on a dataset. A namespace has one, and a namespace made from an OpenLineage event gets the owner `anonymous`.

    Here the shop gives DataHub and OpenMetadata `etlsvc/batch01.corp.internal@CORP.INTERNAL` and `j.marsh` as users, and `data team` as a group in DataHub and a team of team type `Group` in OpenMetadata.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which platforms keep all three owners of `daily_sales`.
    """), kind="info")
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
    <details><summary>The printed result, explained</summary>

    DataHub and OpenMetadata keep all three. Atlas keeps one, here the first, `etlsvc/batch01.corp.internal@CORP.INTERNAL`. Marquez keeps none.

    Compare this with what you decided.

    The list of stored owners gives DataHub's three owners the same ownership type, `urn:li:ownershipType:__system__technical_owner`, with its description. So the count of owners below it shows none of DataHub's three told apart by ownership type. OpenMetadata's owners carry no ownership type at all.

    </details>

    The next cell holds `types`: the ownership type each of the three owners gets in DataHub. As it stands, each is `urn:li:ownershipType:__system__technical_owner`.

    Change them so that each owner has its own ownership type: one of DataHub's four, or one of your own, written `urn:li:ownershipType:` followed by a name. Select the cell and press **Run below**.

    The check below it tests that each ownership type is written as DataHub names one, and whether the three owners can be told apart by their ownership types.

    The check does not test that an ownership type of your own has been defined in DataHub, as DataHub would need. That is the shop's simplification.
    """)
    return


@app.cell
def _():
    types = {
        "account": "urn:li:ownershipType:__system__technical_owner",
        "responsible": "urn:li:ownershipType:__system__technical_owner",
        "team": "urn:li:ownershipType:__system__technical_owner",
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


@app.cell
def _(shop, types):
    shop.platforms.owners_in(types)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With three different ownership types, both tests pass. The count of owners below the check shows all 3 of DataHub's owners told apart by ownership type.

    The list of stored owners below that shows each owner's ownership type, and the description of each of DataHub's own ownership types.

    An ownership type tells the owners apart. Neither DataHub's names for its four nor their descriptions say which question an owner answers: `__system__business_owner` is described as "Principal stakeholders or domain experts associated with the asset(s).", not as the person to ask.

    An ownership type the organisation defines carries the description the organisation gives it.
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
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "tracks ownership" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "choose a metadata platform that tracks ownership"</summary>

    "Choose a metadata platform that tracks ownership" could mean three things. Each item says what it needs, then which platforms meet it:

    - an owner for each dataset: it needs an owner on a dataset. DataHub, OpenMetadata and Atlas can keep one. Marquez keeps owners only on namespaces, not on datasets;
    - whom to ask about each dataset: it needs a person, and a record that this person is the one to ask. DataHub can, with an ownership type defined to mean it. OpenMetadata and Atlas can hold `j.marsh`, but their rules keep no meaning with an owner, so the record does not show that `j.marsh` is the one to ask;
    - which meaning each owner holds: it needs an ownership type for each owner. Of the four, only DataHub keeps one.

    So DataHub can meet all three readings, OpenMetadata and Atlas the first only, and Marquez none for a dataset.

    The requirement does not say which it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 32

    DataHub and OpenMetadata kept all three owners of `daily_sales`, Atlas one and Marquez none.

    Only DataHub's ownership types let a reader tell the three apart, and only when each had its own ownership type. Their names and descriptions still did not say which question each owner answers.

    Chapter 32 follows the metadata of a forecast trained on the shop's data.

    Three questions:

    - Which meaning of "owner" does your own metadata platform keep?
    - Can a reader of it tell one owner's meaning from another's?
    - Which of your datasets have no owner at all?

    ### How this differs from a real platform

    - The architectures list and the owner rules come from each project's documentation and code in the version read. Each platform keeps much more than an owner.
    - DataHub names an owner's ownership type in the field `typeUrn`. The shop's check takes any name after `urn:li:ownershipType:` and does not check that the ownership type has been defined. DataHub also has an older field, `type`, that its schema marks as no longer to be used.
    - A comment in DataHub's schema says its web front end supports only users as owners. The schema also allows groups.
    - The shop gives OpenMetadata `etlsvc/batch01.corp.internal@CORP.INTERNAL` as a user. OpenMetadata's rule takes any user.
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
