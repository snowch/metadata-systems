## BL1

The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found. The query over `clean_orders` is still listed: it gives every row of `daily_sales`, and one row more, for Sunday.

The shortfall is visible: 6 rows where the week as it ran has 7, and six values on a dashboard titled "Sales, last 7 days". No record says that this is a failure. Seeing it takes knowing to expect 7 rows, or comparing the last-altered times.

Only a record of the failure would say that a write was due and did not happen.

## BL2

Nothing; no record of the job. Failed night: a missing row, older last-altered time.

## BL3

The platform's state answers what exists. It does not answer what happened or why. Inferring the history from the data gave an explanation that fitted. Three ordinary changes then tested it: the copy made it ambiguous, the edit made it wrong, and one failed night was left that no record names as a failure. The records that would have answered had to be made when the work was done.

Chapter 3 starts making them: a description of each asset, kept beside the data, with what the asset means and who is responsible for it. It then asks the four questions at the start again. Chapter 6 records what was made from what, which is called lineage, and Chapter 7 records each run of a job.

## BL4

Information of this kind, about an asset or about the platform, is called **metadata**: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets. Some of it the systems already keep for their own purposes: the names, types, counts and times you read above. They do not keep what an asset means, what it was made from, or what happened to it. Somebody has to record those. What happened, such as which tables a night's job read, has to be recorded when it happens. What a table is made from can also be read later, from the jobs' code (Chapter 6). That shows what the code says, not what the job did on a given night. A note of what a job read, written the next morning from the data, is a reconstruction, with the limits shown above.

## BL5

Each of the shop's systems records what its own work needs. The warehouse keeps column names and types so that it can run a query. Object storage keeps a file's key so that it can serve the file. The reporting tool keeps the values so that it can draw the chart. Each also keeps a little more: an owner, created times and who created the dashboard. None of it says what an asset means or how it was made.

## BL6

The rule is met as written: the warehouse fills in an owner for every table by itself. The owner it found answers only the last reading, which account controls the table, so you still do not know whom to ask about `daily_sales`.

## BL7

### before

It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.

The query also explains the other three days that differ. The two cells below list the cancelled orders that `clean_orders` holds, and the orders that `orders.jsonl` holds more than once.

### after

`clean_orders` holds 2 cancelled orders, 7009 on Tuesday, worth 2999 pence, and 7037 on Saturday, worth 2400 pence. The query leaves them out, and so does `daily_sales`: they are Tuesday's and Saturday's gaps. `orders.jsonl` holds order 7015, placed on Wednesday, twice, and `clean_orders` holds it once, so Wednesday's gap is its second copy, worth 4500 pence.

## BL8

A data engineer wants to know which inputs one particular run of a job read.

Consider three pieces of evidence they could have. Which is the strongest evidence of what that run read?

## BL9

**Established.** Each record describes an asset as it is this morning. The record for `daily_sales` gives its columns and their types, 7 rows, a size, when it was created, a last-altered time of 02:30 on Monday 14 September, and an owner, `etl_service`. Each file's record gives its key, size and last-modified time. The dashboard's record gives its title, who created it, when it last refreshed and the values it shows.

**Not established.** Which job wrote any of these assets, what the job read, which version of its code ran, what the rows were the day before, or who decided the rules that shaped them.
