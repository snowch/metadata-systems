# Brief BH: the three changes, said as changes the reader makes

The author found this passage confusing:

> The query is evidence of how the table could have been made, not a record of how it was made, and
> three small changes to the shop show the difference.
>
> - An analyst copies `clean_orders` to a CSV file, `clean_orders_copy.csv`, in the bucket
>   `shop-scratch`, every night.
> - The job that writes `daily_sales` is edited, from Saturday's row on, to keep every order that has
>   not been refunded.
> - On the last night the job that writes `daily_sales` fails and writes nothing.

What is wrong with it: "show the difference" does not say what the reader will look at; the three
items read as things that happened in the week the reader has just studied, when they are changes the
reader applies, one at a time, from a menu further down; and nothing ties each item to that menu.

Write one slot, BH, to replace the passage. Follow `docs/style.md` and `AGENTS.md`. British English.
No em dashes. The reader is "you", a data engineer who has done Chapter 1. Keep names in backticks
exactly as written. A block of code is a "cell". Never use "run" as a noun. Do not use the words
"lineage", "event" or "metadata". Do not say what any change does to the query, the tables or the
dashboard: the cells below the menu show that, and the page explains it after them.

## Facts, in order

1. The query shows how `daily_sales` could have been made. It does not show how it was made.
2. You can test that difference by changing the shop's week in three ways, one at a time. None of
   the three happened in the week you have read so far.
3. A list of the three, each item starting with the menu's own label for it in bold, kept word for
   word, then a colon and the detail:
   - **An analyst copies clean_orders every night**: the copy is a CSV file, `clean_orders_copy.csv`,
     in the bucket `shop-scratch`. Keep the words "to a CSV file, `clean_orders_copy.csv`, in the bucket
     `shop-scratch`, every night" in this item.
   - **From Saturday, the daily_sales job keeps unrefunded orders**: the job that writes `daily_sales`
     is edited, from Saturday's row on, to keep every order that has not been refunded, where it kept
     completed orders.
   - **The daily_sales job fails on the last night**: it writes nothing that night.
4. For each change, the question is the same: does a query over the week's assets still give every
   row of `daily_sales`, and which of the platform's records show the change?
5. The menu below applies one change at a time.

Keep the words "three small changes to the shop" somewhere in the slot: a test reads them.

Write `docs/notes/chapter-02/drafts/round-19/BH.md`: a `## BH` heading, then the slot's text and
nothing else. Write the file once. Use only the Read and Write tools. Send no messages.
