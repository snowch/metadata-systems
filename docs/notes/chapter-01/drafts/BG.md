## A

The page runs Python in your browser, and the first time you open it your browser downloads about 13 MB.

## B

Time and memory

## C

On a computer, running every cell took 10 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

## D

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

## E

The page downloaded less than 1 MB when opened from Chapter 1's link, in a browser that had opened Chapter 1 (measured on a computer). Chapter 1's link opens this page in a new tab. Chapter 1 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 1 leaves more memory for this page.

Running every cell took 10 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

## F

- Identify what the platform holds: three systems, which are files, tables and a dashboard.
- Describe what happens on the platform each night, and what you cannot see of it: the export, the jobs, when they are due to run, and any notes.
- Write a guess, for each warehouse table, at what it is made from.

## G

As you read each file, note which fields could tie it to a table in the warehouse. Note also anything in the rows that a job might have to deal with.

## H

`products.csv`, in object storage, holds the shop's product catalogue: 8 products in 6 categories. Each product has an id (`product_id`), a name, a category, a list price in pence (`list_price_pence`) and the member of staff who last edited it (`updated_by`). `products.csv` stores every value as text, and it has no types.

## I

`customers.jsonl` holds the shop's 10 customers, in 7 countries. A customer's record has five fields: `customer_id`, a name, `email`, a country as a two-letter code, and `signed_up`. Each record names its fields. A date such as `signed_up` is just a string: the file has no date type.

## J

For each of the three tables, write in the cell below which file or table you think it is made from, and what on this page makes you think so. Write one line per table, then press **Save** to keep it. Chapter 2 asks what evidence like this can establish.

## K

```
clean_customers: made from ........ because ........
clean_orders:    made from ........ because ........
daily_sales:     made from ........ because ........
```

## L

Compare the guess you wrote for `daily_sales` in Chapter 1's last cell with the query in the cell below, which the data supports.

## M

What does the warehouse record about `daily_sales`? The two cells below read `information_schema` with SQL, the warehouse's own record of its tables: `information_schema.tables` has one row per table, and `information_schema.columns` has one row per column, with the column's type.

## N

The cells showed the two columns of `daily_sales`, `day` and `revenue_pence`, with their types. They also showed 7 rows, a size in bytes, a created time of 1 September, and a last-altered time of 02:30 on Monday 14 September. The warehouse lists `etl_service` as the owner. It records nothing else about the table.

## O

A record of what the job read would have answered the analyst's copy. A record of which version of the job's code ran each night would have answered the edit. A record of whether each night's write succeeded would have answered the failed night.

- what happened: each night's write of `daily_sales`, when it ran, which version of the job's code ran, what it read, and whether it succeeded

## P

Chapter 3 starts making them: a description of each asset, kept beside the data, with what the asset means and who is responsible for it. It then asks the four questions at the start again, to see which of them that record answers. Chapter 6 records what was made from what, which is called lineage. Chapter 7 records each run of a job: when it started and ended, which version of its code ran, what it read and wrote, and whether it succeeded.
