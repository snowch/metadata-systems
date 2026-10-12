## A

## What the platform records already

Your record says what `daily_sales` is: what it means, who is responsible for it, and what its columns mean and their unit. The warehouse, object storage and the reporting tool record other things.

The warehouse records each table's columns and their types, its owner (an account) and its created time. It also records the table's row count, size and last-altered time. The row count, the size and the last-altered time change with every write to the table. Together with the created time, they record what happened to the table. The columns, their types and the owner say what the table is.

Object storage records a file's key, which says what the file is and where it is. Its size and last-modified time record the file's last write.

The reporting tool records a dashboard's title, which says what the dashboard is. It also records who created the dashboard and when, and when it last refreshed. The creator, the creation time and the last refresh record what happened to the dashboard.

Records of the first kind say what an asset is. Records of the second kind say what happened to it. The first kind is **descriptive**. The second is **operational**. Your record of `daily_sales` is descriptive.

## B

A table's columns and their types make up its structure. That list is the table's **schema**. The next cell lists the schema of the warehouse's three tables: 14 columns in all, 5 in `clean_customers`, 7 in `clean_orders` and 2 in `daily_sales`.

`orders.jsonl` declares no schema. Each line names its fields, and a reader works out their types. `products.csv`'s first line names its columns and gives no types.

## C

## A column that names a person

The head of the shop said Sam Lund keeps the product catalogue. `products.csv` has a column, `updated_by`, that holds a member of staff's login for each product. The next cell counts the products each login last edited.

## D

The cell counts `k.adeyemi` 3, `r.novak` 2 and `s.lund` 3. Three people last edited the 8 products.

`updated_by` says who last changed each product. It is a fact about each product: the shop's catalogue keeps it, and the export copies it into the file. It says nothing about who is responsible for `products.csv`. The column would hold the same logins whoever that was. It is data about the shop's business.

The file's first line, `product_id,name,category,list_price_pence,updated_by`, names the file's columns. That line describes the file, so it is metadata, kept inside the same file as the data.

So what makes information metadata is what it describes: an asset, or the work done on the platform. Where the information is kept, and who wrote it, does not decide that. The warehouse keeps its tables' schemas inside itself. You keep your record beside the data.

## E

## "Every column must have a description."

Suppose the shop sets the requirement: "Every column must have a description." Before you read on, write in the next cell whether the line `daily_sales revenue_pence means: the revenue in pence` meets it, and why.

## F

daily_sales revenue_pence means: the revenue in pence
Does this line meet the requirement? Why?
........

## G

The requirement could ask four different things. Each needs a different line:

- The column's meaning: which orders it counts. It needs a line saying which orders, such as completed orders, each once, by UTC day.
- The unit. It needs a `unit` line that says pence.
- Where its values come from: which asset and which columns. It needs a line naming them. Your record holds nothing of this.
- Whether it may be empty. It needs a line saying so, which a check could test against the rows.

The words `the revenue in pence` repeat the column's name: `revenue_pence` already said "revenue" and "pence".

## H

The next cell runs the check over all three tables. Your record describes only the columns of `daily_sales`, so the check lists the 12 columns of `clean_customers` and `clean_orders` that have no description.

## I

The next cell meets the requirement the quick way. It writes a description for each of the 14 columns from the column's name, with underscores changed to spaces, and then runs the same check.

## J

With a description for each of the 14 columns, the check finds no problems: the requirement is met as written.

The next cell shows the two lines it wrote for `daily_sales`.

## K

Under the other readings, these descriptions say nothing the names did not. They do not say which orders a column counts, where its values come from, or whether it may be empty. A check can count descriptions. It cannot tell whether a description says more than the column's name.

## L

## A record nobody updates

Your record describes `daily_sales` as it is this Monday. The shop could make two changes. Each applies from Saturday's row of `daily_sales` on.

1. The job that writes `daily_sales` also writes each day's number of completed orders, in a new column, `order_count`. The rows before Saturday have no value in `order_count`.
2. The job is edited to keep every order that has not been refunded, as in Chapter 2. The shop has no refunds, so from Saturday a cancelled order counts too.

Before you run the cells below, write in the next cell, for each change, whether the check of `daily_sales` will report a problem.

## M

Change 1, new column: a problem? ........
Change 2, edited job: a problem? ........

## N

For change 1, the check reports the new column, `order_count`, with no description. The warehouse records its columns, so the check can compare them with your record, and your record has no line for `order_count`.

For change 2, the check reports nothing: the edit changed no column.

## O

The next cell compares the edited week's `daily_sales` with Jo's meaning, using the query from above.

## P

Saturday now differs too: 21549 pence in `daily_sales`, against 19149 by Jo's meaning. Thursday still differs.

Your record still says what Jo means by revenue. From Saturday the table counts a cancelled order. Nothing on the platform recorded the edit. So nothing prompted a change to your record, and the check could not see the edit. A record written by hand stays as written while the platform changes. An operational record, made when the job changed and saying which version of the job's code wrote each row, would have shown the edit. Chapter 7 makes such records.

## Q

## Before Chapter 4

The experiments showed that your record answered who to ask about `daily_sales`: Jo Marsh. It answered whether Thursday is wrong by its stated meaning. A description written from the data could not have shown Thursday wrong, because it agrees with the data on every day. The check caught a new column, but not a changed meaning. The experiments could not show since when Thursday is wrong, or what reads `products.csv` or `orders.jsonl`.

Your record names Jo Marsh as responsible for `daily_sales`. The reporting tool records `j.marsh` as the dashboard's creator. Whether those are one person, and how a record could say so, is where Chapter 4 starts. Chapter 4 asks what each record is about, and how one record can point to what another describes.

- Pick a platform you work on. Which of its records say what a table is, and which say what happened to it?
- Which question does a column's description need to answer before a check can tell it apart from the column's name?
- If a job changed and nothing recorded the change, how would you find out when a table's meaning changed?

## R

### How this differs from a real platform

The shop, its people and its data are invented for the course. All times are UTC.

Some real databases keep a description with a table or column. In PostgreSQL, the command `COMMENT ON` stores one comment for a table or a column, and a new one replaces the old. The comment is kept inside the database. `psql`'s `\d` commands show it. For most objects, only the owner can set it. The shop's warehouse keeps no descriptions.

The record notation is the course's own.
