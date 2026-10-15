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
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 4](chapter_04.ipynb) · [Next: Chapter 6](chapter_06.ipynb)

    # Chapter 5: Metadata as a graph

    **Objectives**

    - Turn the records into connections between the things they describe.
    - Choose which connections to follow and in which direction, predict where they lead, then change one and check.
    - Find what following every connection returns, and what it misses.
    - Question the requirement "Show everything related to `daily_sales`."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Jo Marsh's question

    Jo Marsh, in finance, wants daily revenue to count orders that have no customer id. Jo's meaning of a day's revenue says so (Chapter 3). Chapter 2 found that `clean_orders` leaves out orders with no customer id.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Jo asks you, before asking for any change: "Show me everything related to `daily_sales`."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Jo wants two things from the answer: where those orders are lost, and what a change would touch.
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

    The page downloaded less than 1 MB when opened from Chapter 4's link, in a browser that had opened and run Chapter 4 (measured on a computer). Chapter 4's link opens this page in a new tab. Chapter 4 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 4 leaves more memory for this page.

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
    The records below are Chapter 4's records after both of its changes. The two spellings are merged into `j.marsh` and `s.lund`. Chapter 4's last cell made the data engineer a team, `data_engineering`, by default. Chapter 4's merge left the line `dataset daily_sales responsible: j.marsh` twice. The cell keeps it once. The cell keeps the line `dataset clean_orders drops: orders with no customer id`. The model accepts it as text, which was one of Chapter 4's two choices. Two new lines, under a `#` note, say which dataset each column of `daily_sales` belongs to, with the attribute `of`.
    """)
    return


@app.cell
def _(shop):
    records = shop.typed_records("""
# These are Chapter 4's records after both changes.
dataset daily_sales means: the value of every completed order placed that day, by its UTC date
dataset daily_sales responsible: j.marsh
column daily_sales.day means: the UTC date the orders were placed
column daily_sales.revenue_pence means: the value of the day's completed orders
column daily_sales.revenue_pence unit: pence
dataset clean_customers responsible: data_engineering
dataset clean_orders responsible: data_engineering
dataset clean_orders drops: orders with no customer id
dataset s3://shop-raw/products.csv responsible: s.lund
dashboard sales_dashboard means: revenue per day, for the last 7 days
dashboard sales_dashboard responsible: j.marsh
person j.marsh name: Jo Marsh
person j.marsh team: finance
person s.lund name: Sam Lund
person s.lund team: catalogue
team finance name: Finance
team catalogue name: Catalogue
team data_engineering name: the data engineer
# Which dataset each column belongs to
column daily_sales.day of: daily_sales
column daily_sales.revenue_pence of: daily_sales
""")
    records
    return (records,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The model cell has Chapter 4's lines, with `dataset drops: text`, and one new line, `column of: dataset`. The value of `of` on a column must name a dataset.
    """)
    return


@app.cell
def _(shop):
    model = shop.model("""
dataset means: text
dataset responsible: person or team
dataset drops: text
column of: dataset
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
    ## The records as a graph

    Each entity the records describe becomes a **node**, named by its identifier.

    Each line whose value is the identifier of another entity becomes an **edge**. The edge goes from the line's entity to the entity its value names, and it carries the line's attribute as its label. For example, `dataset daily_sales responsible: j.marsh` is the edge from `daily_sales` to `j.marsh`, labelled `responsible`. A line whose value is text, such as a `means` line, is no edge.

    Nodes and edges together are a **graph**.

    The next cell lists the nodes. There are 12: 4 datasets (`daily_sales`, `clean_customers`, `clean_orders`, `products.csv`), 2 columns, the dashboard, 2 people and 3 teams. `orders.jsonl` and `customers.jsonl` are not nodes, because no line describes them.
    """)
    return


@app.cell
def _(model, records, shop):
    graph = shop.graph(records, model)
    graph.nodes()
    return (graph,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next cell lists the edges. There are 9, of three kinds: 5 `responsible`, 2 `of` and 2 `team`.
    """)
    return


@app.cell
def _(graph):
    graph.edges()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next cell draws the graph. It draws each part of the graph that edges join on its own. There are 3 parts. Each arrow points from a line's entity to the entity its value names: from a column to its dataset, from an asset to the person or team responsible, and from a person to a team.
    """)
    return


@app.cell
def _(graph):
    graph.drawing(label="The drawing has 3 parts: daily_sales, its 2 columns and sales_dashboard, joined through j.marsh and finance; clean_customers and clean_orders, joined through data_engineering; and products.csv, s.lund and catalogue.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Following edges

    Walking from one node along its edges, from node to node, is a **traversal**.

    You choose which kinds of edge it follows, and the direction for each, in braces. For example, `{"responsible": "in"}` follows `responsible` edges against their arrows.

    `"out"` follows an edge the way its arrow points, `"in"` against it, and `"both"` either way.

    A traversal lists every node it reaches, the number of edges it walked to reach it (`steps`), and its `path`. In a path, `-responsible->` is an edge followed the way its arrow points, and `<-responsible-` one followed against it.

    The first traversal finds which assets Jo Marsh is responsible for. It starts at `j.marsh` and follows `responsible` edges `"in"`.

    Before you read on, write in the next cell which nodes it will reach, and which it would reach with `"out"` in place of `"in"`.
    """)
    return


@app.cell
def _():
    expected = """
Which nodes will the traversal reach?
........
Which nodes will it reach with "out" in place of "in"?
........
"""
    return


@app.cell
def _(graph):
    graph.traverse("j.marsh", {"responsible": "in"})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The traversal reaches `daily_sales` and `sales_dashboard`, each by 1 edge and each against a `responsible` arrow.

    Change `"in"` to `"out"` in the cell above, select that cell and press **Run below**. Compare what it lists with what you wrote.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `"out"`, the traversal reaches no node, and the cell shows "No rows." Every `responsible` edge at `j.marsh` points to it, so none leaves it.

    Change `"out"` back to `"in"` and press **Run below** again.

    A traversal given no kinds of edge follows every edge, both ways.

    Before you read on, write in the next cell which nodes `graph.traverse("daily_sales")` will reach, and whether it will reach `clean_orders`, whose `drops` line holds the rule behind the orders Jo asks about.
    """)
    return


@app.cell
def _():
    expected_everything = """
Which nodes will graph.traverse("daily_sales") reach?
........
Will it reach clean_orders?
........
"""
    return


@app.cell
def _(graph):
    graph.traverse("daily_sales")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read the `path` of `sales_dashboard` in the table above: `daily_sales -responsible-> j.marsh <-responsible- sales_dashboard`.

    The traversal reaches the dashboard because Jo Marsh is responsible for both, not because the dashboard reads `daily_sales`. The dashboard does read `daily_sales`, but no line records that.

    The traversal does not reach `clean_orders`. The `drops` line is text, so it is no edge, and no edge joins `clean_orders` to any node the traversal reaches.

    The next cell starts at `clean_customers` and follows every edge both ways.
    """)
    return


@app.cell
def _(graph):
    graph.traverse("clean_customers")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It reaches `data_engineering` by 1 edge, then `clean_orders` by 2, through the team responsible for both.

    `clean_orders` is not made from `clean_customers`: Chapter 2's rules say it is made from `orders.jsonl`.

    Following every edge reaches whatever the lines join to the start: its columns, who is responsible for it and their team, and anything else they are responsible for.

    From `clean_customers`, it reached a dataset that is not made from it. From `daily_sales`, it missed `clean_orders`, which holds the rule Jo asks about.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Show everything related to `daily_sales`."

    Jo Marsh's request is a requirement, and it does not say what "related" means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the block below, which holds four readings of "related", decide two things: what you would send Jo Marsh, and what you take "related" to mean.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Four readings of "related"</summary>

    Set what you decided beside four readings of "related":

    - What `daily_sales` takes its data from: a line that says what produces it, followed back towards the files;
    - What reads `daily_sales`: the same kind of line, followed the other way;
    - Who is responsible for it: the `responsible` edge, and that person's `team`;
    - Where it is kept: the warehouse as an entity, with an edge from `daily_sales` to it.

    The records answer only the third reading. The warehouse is not an entity in these records, so no line gives the fourth. No line says what `daily_sales` takes its data from, or what reads it.

    Jo's purpose, where the orders are lost and what a change would touch, needs the first two readings.

    As written, the request is met by a list of what a traversal along every edge reaches. As Jo meant it, no traversal of these records can meet it, because no line records what is made from what.

    What you can send Jo: who is responsible for `daily_sales` and the dashboard; the `drops` line on `clean_orders`; and that the records do not say what `daily_sales` takes its data from, or what reads it.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Before Chapter 6

    A line whose value names another entity becomes an edge, and the records form a graph. A traversal's answer depends on the kinds of edge it follows and their directions. Changing `"in"` to `"out"` took the traversal from `j.marsh` from 2 nodes to none. Following every edge reached the dashboard through Jo Marsh, reached `clean_orders` from `clean_customers` through a team, and missed `clean_orders` from `daily_sales`.

    The records could not show what `daily_sales` takes its data from, or what reads it, because no line records either.

    In Chapter 6 you read the jobs' code. Lines record what each job reads and writes, so the graph can show what is made from what.

    - Take a platform you work on. Which of its records name another entity, such as a person, a table or a team?
    - Pick a question you ask about one asset on that platform. Which edges would a traversal have to follow to answer it, and in which direction?
    - What would a record have to say for a graph to show that one dataset is made from another?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How this differs from a real platform

    The shop, its people and its data are invented for the course. The notation, the model and the traversals are the course's own. The graph is made from the records each time the cell runs.

    The shop's records are 20 lines. On a platform with thousands of assets and people, joined by `responsible` and `team` edges, a traversal along every edge reaches far more nodes, most of them unrelated to the question.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 4](chapter_04.ipynb) · [Next: Chapter 6](chapter_06.ipynb)

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
