[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 5](chapter_05.ipynb)

# Chapter 6: What is lineage?

**Objectives**

- Record what each job reads and writes, from its code.
- Find what a change to one file affects, and what an asset is made from.
- Test a line written from what a person believes against the code.
- Find what happens to such lines when a job's code changes. 

## The jobs' code

The checkout's developer writes:

> Next week we rename `customer_id` in `orders.jsonl` to `customer_ref`. What does that affect?

That is the third question from Chapter 2.

The head of the shop gives you access to the repository where the last engineer kept the jobs' code. In Chapter 1 you could not see the jobs. Now you can read their code.

The code says what each job does now. It does not say when a job did its work, or what it did on any night.

Two things that write or read the shop's files are not in the repository:

- the export, whose code belongs to the checkout's supplier;
- the analyst's copy of Chapter 2, a script on the analyst's laptop. 

The three systems, in the order data moves through them each night. 

[figure] The shop's three systems and what each holds. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 5's link, in a browser that had opened and run Chapter 5 (measured on a computer). Chapter 5's link opens this page in a new tab. Chapter 5 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 5 leaves more memory for this page.

Running every cell took 9 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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

The next cell prints the code of the four jobs, one file each. In each file, `read("...")` reads a file from object storage, a table after `FROM` is read from the warehouse, and `write("...")` or `refresh("...")` names what the job writes. 

```python
repo = shop.repository(week)
for job in repo:
    print("#", job["file"])
    print(job["code"])
```

[output]
# jobs/build_clean_customers.py
raw_customers = read("s3://shop-raw/customers.jsonl")
write("clean_customers", """
SELECT customer_id, name, LOWER(email), country, signed_up
FROM raw_customers
WHERE email IS NOT NULL
""")

# jobs/build_clean_orders.py
raw_orders = read("s3://shop-raw/orders.jsonl")
write("clean_orders", """
SELECT DISTINCT order_id, customer_id, product_id, quantity, price_pence, status, ordered_at
FROM raw_orders
WHERE customer_id IS NOT NULL AND quantity > 0
""")

# jobs/build_daily_sales.py
write("daily_sales", """
SELECT date(ordered_at), SUM(price_pence * quantity)
FROM clean_orders
WHERE status = 'completed' AND date(ordered_at) = :day
GROUP BY date(ordered_at)
""", append=True, day=yesterday)

# jobs/refresh_dashboard.py
refresh("sales_dashboard", """
SELECT day, revenue_pence FROM daily_sales ORDER BY day
""")



The records cell holds Chapter 5's records, with one line for each of the two files that no line described, so that each is an entity. Under a `#` note, it also has two lines for each job: what the job reads and what it writes, with the attributes `reads` and `writes`, taken from the job's code.

The two lines for `build_daily_sales` have dots. Fill them in from that job's code, select the cell and press **Run below**. Until you do, the cells below show the dots: the check reports the two lines, and the walks stop at `clean_orders`. 

```python
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
```

[output]
line | type | identifier | attribute | value | 
2 | dataset | daily_sales | means | the value of every completed order placed that day, by its UTC date | 
3 | dataset | daily_sales | responsible | j.marsh | 
4 | column | daily_sales.day | of | daily_sales | 
5 | column | daily_sales.revenue_pence | of | daily_sales | 
6 | dataset | clean_customers | responsible | data_engineering | 
7 | dataset | clean_orders | responsible | data_engineering | 
8 | dataset | s3://shop-raw/products.csv | responsible | s.lund | 
9 | dashboard | sales_dashboard | responsible | j.marsh | 
10 | person | j.marsh | team | finance | 
11 | person | s.lund | team | catalogue | 
12 | team | finance | name | Finance | 
13 | team | catalogue | name | Catalogue | 
14 | team | data_engineering | name | the data engineer | 
16 | dataset | s3://shop-raw/orders.jsonl | means | every order the checkout took, as the export writes it | 
17 | dataset | s3://shop-raw/customers.jsonl | means | the shop's customers, as the export writes them | 
19 | job | build_clean_customers | reads | s3://shop-raw/customers.jsonl | 
20 | job | build_clean_customers | writes | clean_customers | 
21 | job | build_clean_orders | reads | s3://shop-raw/orders.jsonl | 
22 | job | build_clean_orders | writes | clean_orders | 
23 | job | build_daily_sales | reads | ........ | 
24 | job | build_daily_sales | writes | ........ | 
25 | job | refresh_dashboard | reads | daily_sales | 
26 | job | refresh_dashboard | writes | sales_dashboard |

The model cell adds a type, `job`, with two attributes:

- `job reads: dataset`: the value of `reads` on a job is a dataset.
- `job writes: dataset or dashboard`: the value of `writes` is a dataset or the dashboard.

Until now, a job has been a plain word. Now it is an entity: a node between the assets it reads and the assets it writes. 

```python
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
```

[output]
line | type | attribute | value | 
1 | dataset | means | text | 
2 | dataset | responsible | person or team | 
3 | column | of | dataset | 
4 | dashboard | responsible | person or team | 
5 | person | team | team | 
6 | team | name | text | 
7 | job | reads | dataset | 
8 | job | writes | dataset or dashboard |

## Lineage

The next cell draws only the `reads` and `writes` edges, between the assets and the jobs. This is the platform from Chapter 1, drawn with arrows at last, because your lines now record what each job reads and writes. An arrow from an asset to a job means the job reads it. An arrow from a job to an asset means the job writes it.

Records of what was made from what, and by which job, are **lineage**.

The drawing has 3 parts:

- `orders.jsonl` to `sales_dashboard` through three jobs;
- `customers.jsonl` to `clean_customers` through one job;
- `products.csv`, which no job reads. 

```python
lineage = shop.graph(records, model).only(["reads", "writes"], ["dataset", "dashboard", "job"])
lineage.drawing(label="The drawing shows the chain from orders.jsonl through three jobs to sales_dashboard, the chain from customers.jsonl through one job to clean_customers, and products.csv with no arrow to a job.")
```

[output]
[image: The drawing shows the chain from orders.jsonl through three jobs to sales_dashboard, the chain from customers.jsonl through one job to clean_customers, and products.csv with no arrow to a job.]

## What a change to `orders.jsonl` affects

Before you read on, write which assets a change to `orders.jsonl` affects, in the next cell. The cell gives no result. Write your answer in its dots. 

```python
expected = """
Which assets does a change to orders.jsonl affect,
and why?
........
"""
```

```python
lineage.downstream("s3://shop-raw/orders.jsonl")
```

[output]
node | type | steps | path | 
build_clean_orders | job | 1 | s3://shop-raw/orders.jsonl <-reads- build_clean_orders | 
clean_orders | dataset | 2 | s3://shop-raw/orders.jsonl <-reads- build_clean_orders -writes-> clean_orders |

The cell above walked from `orders.jsonl` to each job that reads it, then to what that job writes, and on. What is made from an asset in this way is **downstream** of it.

Downstream of `orders.jsonl` there are 6 nodes. The 3 jobs are `build_clean_orders`, `build_daily_sales` and `refresh_dashboard`. The 3 assets are `clean_orders`, `daily_sales` and `sales_dashboard`.

The opposite walk goes from an asset to the job that writes it, then to what that job reads, and on. What an asset is made from in this way is **upstream** of it.

The next cell walks back from `sales_dashboard`. 

```python
lineage.upstream("sales_dashboard")
```

[output]
node | type | steps | path | 
refresh_dashboard | job | 1 | sales_dashboard <-writes- refresh_dashboard | 
daily_sales | dataset | 2 | sales_dashboard <-writes- refresh_dashboard -reads-> daily_sales |

Upstream of `sales_dashboard` there are 6 nodes. The farthest back is `orders.jsonl`. `customers.jsonl` and `clean_customers` are not upstream of the dashboard.

The next cell walks downstream from `products.csv`. 

```python
lineage.downstream("s3://shop-raw/products.csv")
```

[output]
No rows.

Downstream of `products.csv` there is nothing. No job in the repository reads it. Chapter 2 asked "Does anything still read it?" As far as the lines go, the answer is no.

The lines record only the jobs in the repository. The export and the analyst's script are not in the repository, and no line records what they read. So "nothing reads `products.csv`" means only that the lines know of no reader. 

## A line from a belief

Jo Marsh says that the daily sales job leaves out test customers, so it reads `clean_customers`. Jo has not read the code. Written as a line, the belief is:

`job build_daily_sales reads: clean_customers`

The next cell adds that line to your records and walks downstream from `customers.jsonl`. 

```python
jos_line = "job build_daily_sales reads: clean_customers"
with_jo = shop.typed_records(records.text + "\n" + jos_line + "\n")
shop.graph(with_jo, model).downstream("s3://shop-raw/customers.jsonl")
```

[output]
node | type | steps | path | 
build_clean_customers | job | 1 | s3://shop-raw/customers.jsonl <-reads- build_clean_customers | 
clean_customers | dataset | 2 | s3://shop-raw/customers.jsonl <-reads- build_clean_customers -writes-> clean_customers | 
build_daily_sales | job | 3 | s3://shop-raw/customers.jsonl <-reads- build_clean_customers -writes-> clean_customers <-reads- build_daily_sales |

With that line, downstream of `customers.jsonl` reaches 6 nodes, `daily_sales` and `sales_dashboard` among them. A change to `customers.jsonl` now seems to affect the dashboard.

The next cell compares each job's lines with its code. It lists one row for each line the code does not bear out, and one row for each read or write in the code that no line records. 

```python
shop.compare_with_code(with_jo, repo)
```

[output]
line | job | says | code | problem | 
23 | build_daily_sales | reads: ........ |  | The line says the job reads this, but the job's code does not read it. | 
28 | build_daily_sales | reads: clean_customers |  | The line says the job reads this, but the job's code does not read it. | 
24 | build_daily_sales | writes: ........ |  | The line says the job writes this, but the job's code does not write it. | 
 | build_daily_sales |  | reads: clean_orders | The job's code reads this, but no line says so. | 
 | build_daily_sales |  | writes: daily_sales | The job's code writes this, but no line says so. |

The comparison lists one row: Jo's line. The code of `build_daily_sales` does not read `clean_customers`, and nothing in it leaves out test customers.

A line written by hand records what someone believes. The code is evidence of what the job reads now. 

## A line gone stale

Suppose that from Saturday, the daily sales job, `build_daily_sales`, is changed to read the analyst's copy of `clean_orders` instead of `clean_orders`. The copy is Chapter 2's `clean_orders_copy.csv`, in the bucket `shop-scratch`. It holds the same rows.

Your lines were written from the code as it is today.

Before you read on, write in the next cell whether the comparison will report anything after the change, and whether the rows of `daily_sales` will change. 

```python
expected_change = """
Will the comparison report anything after the change?
........
Will the rows of daily_sales change?
........
"""
```

```python
changed = shop.run_week(["source"])
shop.compare_with_code(records, shop.repository(changed))
```

[output]
line | job | says | code | problem | 
23 | build_daily_sales | reads: ........ |  | The line says the job reads this, but the job's code does not read it. | 
24 | build_daily_sales | writes: ........ |  | The line says the job writes this, but the job's code does not write it. | 
 | build_daily_sales |  | reads: s3://shop-scratch/clean_orders_copy.csv | The job's code reads this, but no line says so. | 
 | build_daily_sales |  | writes: daily_sales | The job's code writes this, but no line says so. |

The cell runs the week with the change, and compares your lines with the code as it is after the change. It finds 2 rows. Your line says `build_daily_sales` reads `clean_orders`, and its code no longer does. Its code reads `s3://shop-scratch/clean_orders_copy.csv`, and no line says so.

Your lines went stale when the code changed, and nothing changed them.

The next cell compares the rows of `daily_sales` in the changed week with today's. 

```python
changed.warehouse.sql("SELECT * FROM daily_sales") == warehouse.sql("SELECT * FROM daily_sales")
```

[output]
True

`True`: the rows of `daily_sales` are the same in the changed week as today. The data shows no change. Only the code does.

The code shows what the job does now. It does not say which nights the job read `clean_orders` and which nights it read the copy. A record made each time the job does its work would say so. Chapter 7 makes such records. 

## "Record the lineage of `daily_sales`."

The head of the shop's requirement is "Record the lineage of `daily_sales`." Before you read on, write in the next cell what you would record, and from what. 

```python
reading = """
What would you record?
........
From what?
........
"""
```

The requirement could mean four things:

- **What someone says the job reads.** Needs someone to write it down. A line like Jo's records a belief.
- **What the job's code reads now.** Needs the repository, which is evidence of today.
- **What the job read on each night.** Needs a record made each time the job does its work. Nothing on the platform makes one (Chapter 7).
- **Which tables, or which columns, `daily_sales` is made from.** Needs the input columns of each output column. For example, `revenue_pence` is made from `price_pence` and `quantity` of `clean_orders`. Lines between tables do not say so (Chapter 10).

Your lines meet the requirement as written, and agree with the code today. None of them says what the job read on each night, or which columns `revenue_pence` comes from. 

## Before Chapter 7

The experiments showed three things. Lines of what each job reads and writes let the graph answer what a change to a file affects, and what an asset is made from. A line from a belief made the dashboard seem to depend on `customers.jsonl`, until the code was compared with the line. A line written from today's code went stale when the code changed, and the data did not show it.

The experiments could not show what each job read on each night, or what the export and the analyst's script read.

Chapter 7 records each time a job does its work: when it started and ended, which version of its code it used, what it read and wrote, and whether it succeeded.

- Take a platform you work on. Which of its lineage lines were written by hand, and which came from its code? How would you find out that one of them is stale?
- A job reads its input table's name from a configuration file. Which of your lines could be false while the code still looks the same?
- Which nights did the job read `clean_orders`, and which nights did it read the copy? What would you need in order to find out? 

### How this differs from a real platform

The shop, its people, its jobs and its repository are invented for the course.

The shop's jobs are short, and what each reads is found with a small rule: `read("...")`, and a table after `FROM` or `JOIN`. Real code can hide what it reads in functions, variables or SQL built while the job executes. No small rule finds all of it.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 5](chapter_05.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

