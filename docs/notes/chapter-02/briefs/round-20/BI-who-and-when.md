# Brief BI: the three changes, with who makes each and when

The author asked of the passage before Chapter 2's menu: "who made the changes, when? I don't get
what you mean." The passage now reads:

> The query shows how `daily_sales` could have been made. It does not show how it was made. You can
> test that difference with three small changes to the shop. Each changes the shop's week in one way,
> and you apply them one at a time. None of the three happened in the week you have read so far.
>
> - **An analyst copies clean_orders every night**: the analyst copies `clean_orders` to a CSV file,
>   `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night.
> - **From Saturday, the daily_sales job keeps unrefunded orders**: the job that writes `daily_sales` is
>   edited, from Saturday's row on, to keep every order that has not been refunded, where it kept
>   completed orders.
> - **The daily_sales job fails on the last night**: it writes nothing that night.
>
> For each change, the question is the same: does a query over the week's assets still give every row
> of `daily_sales`, and which of the platform's records show the change?

What is missing: that nobody made these changes, because they are what-ifs; who would make each one
in the shop, and when in the week; and what the menu does with the one the reader picks.

Write one slot, BI, to replace the passage. Follow `docs/style.md` and `AGENTS.md`. British English.
No em dashes. The reader is "you", a data engineer who has done Chapter 1. Keep names in backticks
exactly as written. A block of code is a "cell". Never use "run" as a noun. Do not use the words
"lineage", "event" or "metadata". Do not say what any change does to the query, the tables or the
dashboard: the cells below the menu show that.

## Facts, in order

1. The query shows how `daily_sales` could have been made. It does not show how it was made.
2. To see the difference, try three what-ifs. Nobody made these changes: none of them happened in the
   week you have read. Keep the words "three small changes to the shop" in this paragraph.
3. You choose one from the menu below. The page runs the shop's week again as if that change had
   happened, and the cells under the menu show the platform on Monday morning.
4. A list of the three, each item starting with the menu's own label in bold, kept word for word,
   then a colon, then who makes the change and when:
   - **An analyst copies clean_orders every night**: an analyst copies `clean_orders` to a CSV file,
     `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night, at 02:15, after the job that
     writes `clean_orders`. Keep the words "to a CSV file, `clean_orders_copy.csv`, in the bucket
     `shop-scratch`, every night".
   - **From Saturday, the daily_sales job keeps unrefunded orders**: someone on the shop's team edits
     the job that writes `daily_sales`, so that from Saturday's row on, written early on Sunday 13, it
     keeps every order that has not been refunded, where it kept completed orders.
   - **The daily_sales job fails on the last night**: early on Monday 14, the job that writes
     `daily_sales` fails and writes nothing.
5. Keep, word for word: "For each change, the question is the same: does a query over the week's
   assets still give every row of `daily_sales`, and which of the platform's records show the change?"

Write `docs/notes/chapter-02/drafts/round-20/BI.md`: a `## BI` heading, then the slot's text and
nothing else. Write the file once. Use only the Read and Write tools. Send no messages.
