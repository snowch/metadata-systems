[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 4](chapter_04.ipynb) · [Next: Chapter 6](chapter_06.ipynb)

# Chapter 5: Metadata as a graph

**Objectives**

- Turn the records into connections between the things they describe.
- Predict where following some connections leads, then check.
- Find what following every connection returns, and why.
- Question the requirement "Show everything related to `daily_sales`." 

## Jo Marsh's question

Jo Marsh, in finance, replies to the list of owners you sent at the end of Chapter 4. Jo wants daily revenue to count orders that have no customer id. Jo's meaning of a day's revenue already says so (Chapter 3). Before anything changes, Jo asks:

> Show me everything related to `daily_sales`. 

The three systems, in the order data moves through them each night. 

[figure] The shop's three systems and what each holds. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 4's link, in a browser that had opened and run Chapter 4 (measured on a computer). Chapter 4's link opens this page in a new tab. Chapter 4 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 4 leaves more memory for this page.

Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

</details>

</div> 

<div class="ms-box ms-box-steps">

**Running and saving the page**

1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.

</div> 

[hidden code cell]

[hidden code cell]

[hidden code cell]

The records cell holds the records as Chapter 4 left them, with the two spellings merged into `j.marsh` and `s.lund`, and the data engineer as a team with the identifier `data_engineering`. Two new lines, under a `#` note, say which dataset each column of `daily_sales` belongs to, with the attribute `of`. 

```python
records = shop.typed_records("""
# The records as Chapter 4 left them: two spellings merged, the data engineer a team
dataset daily_sales means: the value of every completed order placed that day, by its UTC date
dataset daily_sales responsible: j.marsh
column daily_sales.day means: the UTC date the orders were placed
column daily_sales.revenue_pence means: the value of the day's completed orders
column daily_sales.revenue_pence unit: pence
dataset clean_customers responsible: data_engineering
dataset clean_orders responsible: data_engineering
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
```

[output]
line | type | identifier | attribute | value | 
2 | dataset | daily_sales | means | the value of every completed order placed that day, by its UTC date | 
3 | dataset | daily_sales | responsible | j.marsh | 
4 | column | daily_sales.day | means | the UTC date the orders were placed | 
5 | column | daily_sales.revenue_pence | means | the value of the day's completed orders | 
6 | column | daily_sales.revenue_pence | unit | pence | 
7 | dataset | clean_customers | responsible | data_engineering | 
8 | dataset | clean_orders | responsible | data_engineering | 
9 | dataset | s3://shop-raw/products.csv | responsible | s.lund | 
10 | dashboard | sales_dashboard | means | revenue per day, for the last 7 days | 
11 | dashboard | sales_dashboard | responsible | j.marsh | 
12 | person | j.marsh | name | Jo Marsh | 
13 | person | j.marsh | team | finance | 
14 | person | s.lund | name | Sam Lund | 
15 | person | s.lund | team | catalogue | 
16 | team | finance | name | Finance | 
17 | team | catalogue | name | Catalogue | 
18 | team | data_engineering | name | the data engineer | 
20 | column | daily_sales.day | of | daily_sales | 
21 | column | daily_sales.revenue_pence | of | daily_sales |

The model cell adds one line, `column of: dataset`, so that the value of `of` on a column must name a dataset. 

```python
model = shop.model("""
dataset means: text
dataset responsible: person or team
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
```

[output]
line | type | attribute | value | 
1 | dataset | means | text | 
2 | dataset | responsible | person or team | 
3 | column | of | dataset | 
4 | column | means | text | 
5 | column | unit | text | 
6 | dashboard | means | text | 
7 | dashboard | responsible | person or team | 
8 | person | name | text | 
9 | person | team | team | 
10 | team | name | text |

## The records as a graph

Each entity the records describe becomes a **node**, named by its identifier.

Each line whose value is the identifier of another entity becomes an **edge**. The edge goes from the line's entity to the entity its value names, and it carries the line's attribute as its label. For example, `dataset daily_sales responsible: j.marsh` is the edge from `daily_sales` to `j.marsh`, labelled `responsible`. A line whose value is text, such as a `means` line, is no edge.

Nodes and edges together are a **graph**.

The next cell lists the nodes. There are 12: 4 datasets (`daily_sales`, `clean_customers`, `clean_orders`, `products.csv`), 2 columns, the dashboard, 2 people and 3 teams. `orders.jsonl` and `customers.jsonl` are not nodes, because no line describes them. 

```python
graph = shop.graph(records, model)
graph.nodes()
```

[output]
node | type | 
daily_sales.day | column | 
daily_sales.revenue_pence | column | 
sales_dashboard | dashboard | 
clean_customers | dataset | 
clean_orders | dataset | 
daily_sales | dataset | 
s3://shop-raw/products.csv | dataset | 
j.marsh | person | 
s.lund | person | 
catalogue | team | 
data_engineering | team | 
finance | team |

The next cell lists the edges. There are 9, of three kinds: 5 `responsible`, 2 `of` and 2 `team`. 

```python
graph.edges()
```

[output]
from | edge | to | 
daily_sales | responsible | j.marsh | 
clean_customers | responsible | data_engineering | 
clean_orders | responsible | data_engineering | 
s3://shop-raw/products.csv | responsible | s.lund | 
sales_dashboard | responsible | j.marsh | 
j.marsh | team | finance | 
s.lund | team | catalogue | 
daily_sales.day | of | daily_sales | 
daily_sales.revenue_pence | of | daily_sales |

The next cell draws the graph. It draws each part of the graph that edges join on its own. There are 3 parts. Each arrow points from a line's entity to the entity its value names: from a column to its dataset, from an asset to the person or team responsible, and from a person to a team. 

```python
graph.drawing(label="The drawing has 3 parts: daily_sales, its 2 columns and sales_dashboard, joined through j.marsh and finance; clean_customers and clean_orders, joined through data_engineering; and products.csv, s.lund and catalogue.")
```

[output]
[image: The drawing has 3 parts: daily_sales, its 2 columns and sales_dashboard, joined through j.marsh and finance; clean_customers and clean_orders, joined through data_engineering; and products.csv, s.lund and catalogue.]

## Following edges

Walking from one node along its edges, from node to node, is a **traversal**. You choose which kinds of edge it follows, and the direction for each. `"out"` follows an edge the way its arrow points, `"in"` against it, and `"both"` either way. A traversal lists every node it reaches, the number of edges it walked to reach each one, and the path it took.

The first traversal starts at `daily_sales`. It follows `responsible` and `team` edges, each the way its arrow points. Before you read on, write in the next cell which nodes it will reach. 

```python
expected = """
Which nodes will this traversal reach?
........
"""
```

```python
graph.traverse("daily_sales", {"responsible": "out", "team": "out"})
```

[output]
node | type | steps | path | 
j.marsh | person | 1 | daily_sales -responsible-> j.marsh | 
finance | team | 2 | daily_sales -responsible-> j.marsh -team-> finance |

The traversal reaches `j.marsh` by 1 edge and `finance` by 2 edges. `j.marsh` is who is responsible for `daily_sales`, and `finance` is that person's team.

A traversal given no kinds follows every edge both ways. Before you read on, write in the next cell which nodes `graph.traverse("daily_sales")` will reach, and why each. 

```python
expected_everything = """
Which nodes will graph.traverse("daily_sales")
reach, and why is each one reached?
........
"""
```

```python
graph.traverse("daily_sales")
```

[output]
node | type | steps | path | 
j.marsh | person | 1 | daily_sales -responsible-> j.marsh | 
daily_sales.day | column | 1 | daily_sales <-of- daily_sales.day | 
daily_sales.revenue_pence | column | 1 | daily_sales <-of- daily_sales.revenue_pence | 
sales_dashboard | dashboard | 2 | daily_sales -responsible-> j.marsh <-responsible- sales_dashboard | 
finance | team | 2 | daily_sales -responsible-> j.marsh -team-> finance |

The traversal reaches 5 nodes: `j.marsh`, the 2 columns, `sales_dashboard` and `finance`.

The path to `sales_dashboard` is `daily_sales -responsible-> j.marsh <-responsible- sales_dashboard`. The traversal reaches the dashboard because Jo Marsh is responsible for both, not because the dashboard reads `daily_sales`. The dashboard does read `daily_sales`, but no line records that.

The next cell starts at `clean_customers` and follows every edge both ways. 

```python
graph.traverse("clean_customers")
```

[output]
node | type | steps | path | 
data_engineering | team | 1 | clean_customers -responsible-> data_engineering | 
clean_orders | dataset | 2 | clean_customers -responsible-> data_engineering <-responsible- clean_orders |

The cell reaches `data_engineering`, then `clean_orders`, which it reaches through the team responsible for both. `clean_orders` is not made from `clean_customers`: Chapter 2's rules say it is made from `orders.jsonl`.

Following every edge returns what shares an owner with the start, here `clean_customers`. A reader asking for everything related could take that result for what `clean_customers` is made from. Which nodes come back depends on the kinds of edge followed, and on the direction each is followed in. 

## "Show everything related to `daily_sales`."

Jo Marsh's request is a requirement, and it does not say what "related" means. Before you read on, write in the next cell what you would send Jo Marsh, and what "related" means to you. 

```python
reading = """
What would you send Jo Marsh?
........
What does "related" mean to you?
........
"""
```

It could mean four things. Each needs a different kind of edge:

- what `daily_sales` is made from: an edge between datasets, from `daily_sales` to whatever makes it;
- what reads `daily_sales`: the same kind of edge, the other way;
- who is responsible for it: the `responsible` edge;
- where it is kept: the warehouse as an entity, with an edge from `daily_sales` to it. The warehouse is not an entity in these records.

The graph holds the third reading, who is responsible. Its `responsible` edges say who is responsible for a dataset, and its `team` and `of` edges add that person's team and the dataset's columns. No edge says what `daily_sales` is made from or what reads it, and none says where it is kept. Following every edge answers none of the four readings, because it mixes owners, teams and columns. 

## Before Chapter 6

A line whose value names another entity becomes an edge, and the records then form a graph. A traversal answers a question only when it follows the edges that the question means. Following every edge, both ways, returned the assets that share an owner with the start. What `daily_sales` is made from, and what reads it, cannot be read from the graph, because no line records either.

Chapter 6 gives you the jobs' code and records what each job reads and writes, so that the graph holds what is made from what.

- Take a platform you work on. Which of its records name another entity, such as an owner, a table or a team?
- Pick a question you ask about one asset on that platform. Which edges would a traversal have to follow to answer it, and in which direction?
- What would a record have to say for a graph to show that one dataset is made from another? 

### How this differs from a real platform

The shop, its people and its data are invented for the course. The notation, the model and the traversals are the course's own. The graph is made from the records each time the cell runs.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 4](chapter_04.ipynb) · [Next: Chapter 6](chapter_06.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

