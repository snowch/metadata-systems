# Brief BJ: the three what-ifs as plain cells, in a section of their own

The author found the Reconstruction section too long, and the menu of changes awkward: choosing a
change showed nothing until the reader selected the next cell and pressed Run below, and the result
was spread over four cells with nothing to compare it with. The menu goes. Reconstruction now ends
at "Compare the query with your guess. Did you name the same table and the same orders?" A new
section follows it. In it, each what-if has one cell that runs the shop's week again with that
change and prints one table: Monday morning's records for the week as it ran, beside the same
records with the change.

Write five slots, BJ1 to BJ5, each under its own `## BJn` heading in your file. Follow
`docs/style.md` and `AGENTS.md`. British English. No em dashes. The reader is "you", a data engineer
who has done Chapter 1. Keep names in backticks exactly as written. A block of code is a "cell".
Never use "run" as a noun. Do not use the words "lineage", "event", "metadata", "menu" or "lab". Do
not say what a change does to the records before its cell: the result paragraph after the cell says
it. Short sentences. Say each thing once.

## BJ1: the section's heading and its opening, before the first cell

1. A heading starting `## ` that names the section's subject: the difference between how
   `daily_sales` could have been made and how it was made. Not a question, not a slogan.
2. The query shows how `daily_sales` **could have been** made. It does not show how it **was**
   made. Keep both bold words exactly as written here.
3. To see the difference, try three what-ifs: three small changes to the shop. Keep the words
   "three small changes to the shop". Nobody made these changes: none of them happened in the week
   you have read so far.
4. Each of the three cells below runs the shop's week again with one change. It prints a table with
   one row for each of the platform's records on Monday morning: the column `the week as it ran`
   holds the record for the week you have read, and the column `with the change` holds it for the
   week with the change.
5. The records, one per row: the files in object storage; when `clean_orders` was last altered;
   how many rows `daily_sales` has, and when it was last altered; when the dashboard last
   refreshed, and the values it shows; and the queries that give every row of `daily_sales`.
6. The last row comes from a fixed set of simple queries over the week's assets. Each reads one
   asset, keeps all, completed or cancelled orders, and adds up revenue, quantity or rows, per
   day, customer or product. A query is listed if it gives every row of `daily_sales`, even if it
   gives a row more. Each is written as the asset it reads, then the rest, for example
   `clean_orders: completed orders, revenue per day`, which is the query you ran above.
7. For each change, ask the same question: does a query over the week's assets still give every
   row of `daily_sales`, and which records show the change? Compare the two columns row by row.

## BJ2: the first what-if, one paragraph before its cell, one after

Before the cell:
1. Start with the bold words **An analyst copies `clean_orders` every night.**
2. An analyst copies `clean_orders` to a CSV file, `clean_orders_copy.csv`, in the bucket
   `shop-scratch`, every night, at 02:15, after the job that writes `clean_orders`. Keep the words
   "to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night" exactly.

After the cell:
3. The copy is a new file in object storage, `s3://shop-scratch/clean_orders_copy.csv`.
4. The last row now lists two queries: the same query over `clean_orders` and over the copy.
5. Every other record is the same as in the week as it ran.
6. None of the records says which of the two the job that writes `daily_sales` reads.
7. A query that fits is evidence for every source it fits.

## BJ3: the second what-if, one paragraph before its cell, one after

Before the cell:
1. Start with the bold words **From Saturday, the `daily_sales` job keeps unrefunded orders.**
2. Someone on the shop's team edits the job that writes `daily_sales`, so that from Saturday's row
   on, written early on Sunday 13, it keeps every order that has not been refunded, where it kept
   completed orders.

After the cell:
3. The shop has no refunds, so from Saturday every order counts, cancelled ones included.
4. The dashboard shows £215.49 for Saturday, 2026-09-12, where it showed £191.49. Keep the words
   "£215.49 instead of £191.49" exactly.
5. The table still has 7 rows and the same last-altered time. Keep these words exactly: "The table
   still has 7 rows and the same last-altered time".
6. The last row says `none`: no query in the set gives the rows of `daily_sales` any more.
7. No record on the platform says the job was edited.

## BJ4: the third what-if, one paragraph before its cell, one after

Before the cell:
1. Start with the bold words **The `daily_sales` job fails on the last night.**
2. Early on Monday 14, the job that writes `daily_sales` fails and writes nothing.

After the cell. Keep the sentences of facts 3 and 4 word for word: a test holds them.
3. "The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier
   than `clean_orders` and the dashboard."
4. "The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found."
5. The query over `clean_orders` is still listed: it gives every row of `daily_sales`, and one row
   more, for Sunday.
6. Keep these two sentences word for word: "Each record is normal on its own. The gap shows only
   when you compare the last-altered times."
7. Only a record of the failure would say that a write was due and did not happen.

## BJ5: one sentence for the chapter's note on how the shop differs from a real platform

It replaces this sentence, which names a menu that is gone: '"No simple query over the week's
assets reproduces it" means none of the simple queries the menu's last cell tries.' The sentence
after it stays: "A query with a condition on the date could still reproduce the edited table."
1. The last row of each table above tries only the fixed set of simple queries.
2. So `none`, in the second what-if, means none of those queries; it says nothing about others.
Write one or two sentences, and nothing else.
