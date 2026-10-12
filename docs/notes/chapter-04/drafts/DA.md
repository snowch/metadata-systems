## A

- Count the owners that the records name, and find out why the count is not a count of people.
- Rewrite the records so that each line says what kind of thing it describes.
- Write a model that the records can be checked against, and merge two spellings of one owner.
- Question the requirement "Each asset has one owner."

## B

## Who owns what

It is still Monday 14 September 2026, late in the afternoon. The head of the shop sends you a requirement:

> Each asset has one owner. Send me the list.

You have your records from Chapter 3. Jo Marsh, in finance, has sent the notes Jo keeps about the dashboard and `daily_sales`. The first cell puts both together, in Chapter 3's notation: your records first, then Jo's notes.

## C

Run the next cell to list every line that has `responsible` in it.

## D

The next cell asks how many people are responsible for the shop's assets, according to these records. Fill in its blanks with your answer and how you counted, before you run the cell after it.

## E

```
"""
How many people are responsible for the shop's
assets, according to these records?
........
How I counted:
........
"""
```

## F

The cell counts 4 different values of `responsible`: the data engineer, Jo Marsh, `j.marsh` and Sam Lund.

The count is of spellings, not people. Jo Marsh and `j.marsh` may be one person, and the records do not say whether they are. To the records, each is a piece of text. The head of the shop said in Chapter 3 that Jo Marsh built the dashboard, and the reporting tool records `j.marsh` as the dashboard's creator. That supports one person. It does not prove it, because to the records each name is still a piece of text.

As written, `daily_sales` has two owners: Jo Marsh, from your records, and `j.marsh`, from Jo's notes.

You ask the head of the shop for the staff list. It has two lines: `j.marsh` is Jo Marsh, in finance; `s.lund` is Sam Lund, in catalogue. So `j.marsh` and Jo Marsh are one person.

## G

## What the records describe

To count people, the records must describe people. Each line must also say what kind of thing it describes.

A thing the records describe is an **entity**: a table, a file, a column, a person or a team. Each entity has a type.

A named property that every entity of a type can have is an **attribute**, such as `means` or `name`. Each line gives the value of one attribute of one entity.

A value that names exactly one entity of its type, and that every record uses for it, is an **identifier**. `j.marsh` can serve as one if every record uses it for Jo Marsh, and never sometimes Jo Marsh. The staff logins, `j.marsh` and `s.lund`, are identifiers. So are a table's name in the warehouse and a file's key in object storage.

## H

A file and a table both hold rows under named columns. The same attributes describe both: what they mean, who is responsible for them, and their columns. One type covers both. It is a **dataset**: a file or a table of rows.

The dashboard holds no rows of its own, so it does not fit the dataset type. It has a type of its own, `dashboard`.

## I

Chapter 4 writes each line in one notation. The line starts with the type of the thing, then its identifier, then the attribute, a colon and the value:

`dataset daily_sales responsible: j.marsh`

`person j.marsh name: Jo Marsh`

A column's identifier is its table's name and its own name joined by a dot. For example, `daily_sales.revenue_pence` is the column `revenue_pence` in `daily_sales`.

The next cell holds the same records in this notation, with the staff list added: a person for each login, with a name and a team, and a team for each of the two teams.

## J

## A model of the records

A model says which types there are, which attributes each type has, and what each attribute's value is. The value is either text, or the identifier of an entity of another type.

An attribute whose value is the identifier of an entity of another type links the two entities. `responsible` links a dataset or the dashboard to a person or a team. An attribute of this kind is a relationship type.

The model has one line per attribute: the type, the attribute, a colon, and what the value is. The value is `text`, or one or more type names joined by `or`. For example, `dataset responsible: person or team` says that the value of `responsible` on a dataset names a person or a team.

The model cell defines the types `dataset`, `column`, `dashboard`, `person` and `team`.

## K

The check cell compares the records with the model. It lists every line whose type or attribute the model does not have, and every value that should be the identifier of a person or a team and is not.

## L

The check finds 5 problems. Of these, 4 are lines whose `responsible` value is not the identifier of a person or team in the records:

- `daily_sales` has `responsible` Jo Marsh.
- `products.csv` has `responsible` Sam Lund.
- `clean_customers` has `responsible` the data engineer.
- `clean_orders` has `responsible` the data engineer.

The fifth problem is `drops` on `clean_orders`. The model gives a dataset no attribute called `drops`.

## M

In the records cell, change `responsible: Jo Marsh` to `responsible: j.marsh`, and change `responsible: Sam Lund` to `responsible: s.lund`. Then select the cell and press **Run below**.

The check then lists 3 problems. Both `responsible` lines of `daily_sales` now give `j.marsh`, so `daily_sales` has one owner. The spelling Jo Marsh is kept, as the `name` of the person `j.marsh`.

## N

"The data engineer" is a role: the staff list does not name it, and no record describes it. Whether it should name a person or a team depends on what "one owner" means, and a later section of the chapter returns to this.
