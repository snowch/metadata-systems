[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 3](chapter_03.ipynb)

# Chapter 4: Metadata as a model

**Objectives**

- Count the owners that the records name, and find out why the count is not a count of people.
- Rewrite the records so that each line says what kind of thing it describes.
- Write a model that the records can be checked against, and merge two spellings of one owner.
- Question the requirement "Each asset has one owner." 

## Who owns what

It is still Monday 14 September 2026, late in the afternoon. The head of the shop sends you a requirement:

> Each asset has one owner. Send me the list. 

The three systems, in the order data moves through them each night. 

[figure] The shop's three systems and what each holds. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 3's link, in a browser that had opened and run Chapter 3 (measured on a computer). Chapter 3's link opens this page in a new tab. Chapter 3 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 3 leaves more memory for this page.

Running every cell took 9 to 11 seconds, and the page used about 410 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

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

You have your records from Chapter 3. Jo Marsh, in finance, has sent the notes Jo keeps about the dashboard and `daily_sales`. The first cell puts both together, in Chapter 3's notation: your records first, then Jo's notes. 

```python
yours = """
daily_sales means: the value of every completed order placed that day, by its UTC date
daily_sales responsible: Jo Marsh
daily_sales revenue_pence unit: pence
clean_customers responsible: the data engineer
clean_orders responsible: the data engineer
clean_orders drops: orders with no customer id, and orders with a quantity of 0 or less
s3://shop-raw/products.csv responsible: Sam Lund
"""
jos = """
sales_dashboard means: revenue per day, for the last 7 days
sales_dashboard responsible: j.marsh
daily_sales responsible: j.marsh
"""
together = shop.records(yours + jos)
together
```

[output]
line | asset | column | field | value | 
2 | daily_sales |  | means | the value of every completed order placed that day, by its UTC date | 
3 | daily_sales |  | responsible | Jo Marsh | 
4 | daily_sales | revenue_pence | unit | pence | 
5 | clean_customers |  | responsible | the data engineer | 
6 | clean_orders |  | responsible | the data engineer | 
7 | clean_orders |  | drops | orders with no customer id, and orders with a quantity of 0 or less | 
8 | s3://shop-raw/products.csv |  | responsible | Sam Lund | 
10 | sales_dashboard |  | means | revenue per day, for the last 7 days | 
11 | sales_dashboard |  | responsible | j.marsh | 
12 | daily_sales |  | responsible | j.marsh |

Run the next cell to list every line that has `responsible` in it. 

```python
together.sql("SELECT asset, value AS responsible FROM records WHERE field = 'responsible' ORDER BY asset")
```

[output]
asset | responsible | 
clean_customers | the data engineer | 
clean_orders | the data engineer | 
daily_sales | Jo Marsh | 
daily_sales | j.marsh | 
s3://shop-raw/products.csv | Sam Lund | 
sales_dashboard | j.marsh |

The next cell asks how many people are responsible for the shop's assets, according to these records. Fill in its blanks with your answer and how you counted, before you run the cell after it. 

```python
expected = """
How many people are responsible for the shop's
assets, according to these records?
........
How I counted:
........
"""
```

```python
together.sql("SELECT COUNT(DISTINCT value) AS owners FROM records WHERE field = 'responsible'")
```

[output]
owners | 
4 |

The cell counts 4 different values of `responsible`: the data engineer, Jo Marsh, `j.marsh` and Sam Lund.

The count is of spellings, not people. Jo Marsh and `j.marsh` may be one person, and the records do not say whether they are. To the records, each is a piece of text. The head of the shop said in Chapter 3 that Jo Marsh built the dashboard, and the reporting tool records `j.marsh` as the dashboard's creator. That supports one person. It does not prove it, because to the records each name is still a piece of text.

As written, `daily_sales` has two owners: Jo Marsh, from your records, and `j.marsh`, from Jo's notes.

You ask the head of the shop for the staff list. It has two lines: `j.marsh` is Jo Marsh, in finance; `s.lund` is Sam Lund, in catalogue. So `j.marsh` and Jo Marsh are one person. 

## What the records describe

To count people, the records must describe people. Each line must also say what kind of thing it describes.

A thing the records describe is an **entity**: a table, a file, a column, a person or a team. Each entity has a type.

A named property that every entity of a type can have is an **attribute**, such as `means` or `name`. Each line gives the value of one attribute of one entity.

A value that names exactly one entity of its type, and that every record uses for it, is an **identifier**. `j.marsh` can serve as one if every record uses it for Jo Marsh, and never sometimes Jo Marsh. The staff logins, `j.marsh` and `s.lund`, are identifiers. So are a table's name in the warehouse and a file's key in object storage.

A file and a table both hold rows under named columns. The same attributes describe both: what they mean, who is responsible for them, and their columns. One type covers both. It is a **dataset**: a file or a table of rows.

The dashboard holds no rows of its own, so it does not fit the dataset type. It has a type of its own, `dashboard`.

Chapter 4 writes each line in one notation. The line starts with the type of the thing, then its identifier, then the attribute, a colon and the value:

`dataset daily_sales responsible: j.marsh`

`person j.marsh name: Jo Marsh`

A column's identifier is its table's name and its own name joined by a dot. For example, `daily_sales.revenue_pence` is the column `revenue_pence` in `daily_sales`.

The next cell holds the same records in this notation, with the staff list added: a person for each login, with a name and a team, and a team for each of the two teams. 

```python
records = shop.typed_records("""
dataset daily_sales means: the value of every completed order placed that day, by its UTC date
dataset daily_sales responsible: j.marsh
column daily_sales.revenue_pence unit: pence
dataset clean_customers responsible: the data engineer
dataset clean_orders responsible: the data engineer
dataset clean_orders drops: orders with no customer id, and orders with a quantity of 0 or less
dataset s3://shop-raw/products.csv responsible: s.lund
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
```

[output]
line | type | identifier | attribute | value | 
2 | dataset | daily_sales | means | the value of every completed order placed that day, by its UTC date | 
3 | dataset | daily_sales | responsible | j.marsh | 
4 | column | daily_sales.revenue_pence | unit | pence | 
5 | dataset | clean_customers | responsible | the data engineer | 
6 | dataset | clean_orders | responsible | the data engineer | 
7 | dataset | clean_orders | drops | orders with no customer id, and orders with a quantity of 0 or less | 
8 | dataset | s3://shop-raw/products.csv | responsible | s.lund | 
9 | dashboard | sales_dashboard | means | revenue per day, for the last 7 days | 
10 | dashboard | sales_dashboard | responsible | j.marsh | 
11 | dataset | daily_sales | responsible | j.marsh | 
12 | person | j.marsh | name | Jo Marsh | 
13 | person | j.marsh | team | finance | 
14 | person | s.lund | name | Sam Lund | 
15 | person | s.lund | team | catalogue | 
16 | team | finance | name | Finance | 
17 | team | catalogue | name | Catalogue |

## A model of the records

A model says which types there are, which attributes each type has, and what each attribute's value is. The value is either text, or the identifier of an entity of another type.

An attribute whose value is the identifier of an entity of another type links the two entities. `responsible` links a dataset or the dashboard to a person or a team. An attribute of this kind is a relationship type.

The model has one line per attribute: the type, the attribute, a colon, and what the value is. The value is `text`, or one or more type names joined by `or`. For example, `dataset responsible: person or team` says that the value of `responsible` on a dataset names a person or a team.

The model cell defines the types `dataset`, `column`, `dashboard`, `person` and `team`. 

```python
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
```

[output]
line | type | attribute | value | 
2 | dataset | means | text | 
3 | dataset | responsible | person or team | 
4 | column | means | text | 
5 | column | unit | text | 
6 | dashboard | means | text | 
7 | dashboard | responsible | person or team | 
8 | person | name | text | 
9 | person | team | team | 
10 | team | name | text |

The check cell compares the records with the model. It lists every line whose type or attribute the model does not have, and every value that should be the identifier of a person or a team and is not. 

```python
model.check(records)
```

[output]
line | record | problem | 
5 | dataset clean_customers responsible: the data engineer | This value should be the identifier of something of type person or team, and no record describes such a thing with that identifier. | 
6 | dataset clean_orders responsible: the data engineer | This value should be the identifier of something of type person or team, and no record describes such a thing with that identifier. | 
7 | dataset clean_orders drops: orders with no customer id, and orders with a quantity of 0 or less | The model does not give this type this attribute. |

The check finds 5 problems. Of these, 4 are lines whose `responsible` value is not the identifier of a person or team in the records:

- `daily_sales` has `responsible` Jo Marsh.
- `products.csv` has `responsible` Sam Lund.
- `clean_customers` has `responsible` the data engineer.
- `clean_orders` has `responsible` the data engineer.

The fifth problem is `drops` on `clean_orders`. The model gives a dataset no attribute called `drops`.

In the records cell, change `responsible: Jo Marsh` to `responsible: j.marsh`, and change `responsible: Sam Lund` to `responsible: s.lund`. Then select the cell and press **Run below**.

The check then lists 3 problems. Both `responsible` lines of `daily_sales` now give `j.marsh`, so `daily_sales` has one owner. The spelling Jo Marsh is kept, as the `name` of the person `j.marsh`.

"The data engineer" is a role: the staff list does not name it, and no record describes it. Whether it should name a person or a team depends on what "one owner" means, and a later section of the chapter returns to this. 

## A fact the model has no type for

After the merge, the check still refuses this line:

`dataset clean_orders drops: orders with no customer id, and orders with a quantity of 0 or less`

The model gives a dataset no attribute called `drops`. The line is the rule that explains Thursday's low revenue in Chapter 2. The model has no place for it.

You have two choices.

- Leave the model as it is. The check keeps refusing the fact. Anyone who keeps the records to the model loses it.
- Add the line `dataset drops: text` to the model. The check accepts it, as text. Then any dataset can have any text about what it drops. No check can say whether that text is true, or whether the job that writes the table applies that rule.

A model decides which facts the records can hold, and which of those a check can test.

A fact about how an asset is made, such as this one, gets a place of its own in Chapter 6. 

## "Each asset has one owner."

The head of the shop's requirement, "Each asset has one owner.", could mean three things, each needing something different in the records:

- **One person to ask about each asset.** The records need `responsible`, a line that names a person, with one value per asset.
- **One team that answers for each asset.** The records need a team for each asset, named directly or as the team of the person named.
- **One owner, however the records spell the owner's name.** The records need identifiers, so that two spellings of one person count once.

In the cell below, write which reading you would require in the shop's place, and why. No reading is marked right or wrong. 

```python
reading = """
Which reading would you require in the shop's place?
........
Why would you require that reading?
........
"""
```

The next cell reads the records after your two changes and makes the data engineer a team with the identifier `data_engineering`. Then it lists every asset, the values of its `responsible` lines, and a `yes` or `no` for each reading: `one_owner`, `one_person` and `one_team`. 

```python
after = shop.typed_records(
    records.text.replace("responsible: Jo Marsh", "responsible: j.marsh")
    .replace("responsible: Sam Lund", "responsible: s.lund")
    .replace("responsible: the data engineer", "responsible: data_engineering")
    + "\nteam data_engineering name: Data engineering\n"
)
shop.owners(week, after)
```

[output]
asset | responsible | one_owner | one_person | one_team | 
s3://shop-raw/customers.jsonl |  | no | no | no | 
s3://shop-raw/orders.jsonl |  | no | no | no | 
s3://shop-raw/products.csv | s.lund | yes | yes | yes | 
clean_customers | data_engineering | yes | no | yes | 
clean_orders | data_engineering | yes | no | yes | 
daily_sales | j.marsh | yes | yes | yes | 
sales_dashboard | j.marsh | yes | yes | yes |

Of the 7 assets, 5 have one owner under `one_owner`: every asset except `orders.jsonl` and `customers.jsonl`. Those two are the files the export writes, and the records do not say who is responsible for them.

Three assets have one person under `one_person`: `products.csv`, with `s.lund`, and `daily_sales` and `sales_dashboard`, both with `j.marsh`. The two cleaned tables name a team.

Five assets have one team under `one_team`: every asset with an owner.

No reading is wrong. The requirement does not say which one it means. Any list meets some readings and not others, so the list should say which ones it meets. 

## Before Chapter 5

With a type on each line and an identifier for each person, the records can count people instead of spellings. A check can also find a value that names nothing the records describe. The check rejected the line about what `clean_orders` drops, because the model had no attribute for it. The requirement is met under some readings and not others, and the two files the export writes have no owner under any reading.

The checks could not show whether a record is true. The model checks the form of a value, and whether the value names a known entity. It does not check whether Jo Marsh is really responsible.

The records now point from one entity to another: a dataset to a person, and a person to a team. Chapter 5 follows those references from one entity to the next.

- Take a platform you work on. Which of the three readings of "Each asset has one owner" does its owner field meet, and what would it need in order to meet the others?
- Which record on that platform could a check accept while the record is false? What would a check need in order to test it?
- A person leaves, and their login is given to someone else. Which records would then name the wrong person, and how would you find out? 

### How this differs from a real platform

The shop, its people, its staff list and its data are invented for the course.

The record notation and the model notation are the course's own. Real metadata systems each define their own types and attributes. Chapter 31 compares some of them.

The shop uses staff logins as identifiers for people. A login can change, or be given to someone else after a person leaves. The shop's staff list does not record when.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 3](chapter_03.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

