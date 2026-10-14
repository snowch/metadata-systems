# Brief BR: the shop's data, and each system's records about its assets

Read `docs/style.md` for the voice: British English, active voice, short plain sentences, no em
dashes, no filler, no reassurance, no "notice", no meta-commentary about the exercise. The reader
is "you", a software or data engineer. Do not use the word "metadata" in BR1: the chapter defines
it much later. Write each string under its own `## BRn` heading, exactly as it will appear on the
page, and nothing else.

The author's note: the section must make it clearer that the platform holds more than the shop's
business data.

## BR1: the paragraph under the heading "## 2. What the platform records about its assets"

It replaces this paragraph:

> The cells read each system's own record of its assets: the warehouse's `information_schema` for
> `daily_sales`, the listing of the bucket `shop-raw`, and the reporting tool's record of
> `sales_dashboard`.

Facts, in this order:

1. Section 1 read the shop's data: the orders in `orders.jsonl`, and the rows of `clean_orders`
   and `daily_sales`.
2. Besides that data, each system keeps records about the assets it holds. A record about an
   asset is not an order or a day's revenue; it describes the file, the table or the dashboard.
3. The cells below read those records: the warehouse's `information_schema` for `daily_sales`
   (two cells: the table, then its columns), the listing of the bucket `shop-raw`, and the
   reporting tool's record of `sales_dashboard`.
4. What to look for as you read them: whether any record says which job made `daily_sales`, or
   what that job read. Do not say whether one does.

At most four sentences. Keep every name in backticks exactly as written.

## BR2: one sentence in the later section "Records made at the time"

The sentence is: "Some of it the systems already keep for their own purposes: the names, types,
counts and times you read above."

Rewrite it with one change only: instead of "above", it points to section 2 by its heading,
"What the platform records about its assets", so that the reader connects the word just defined
with the records they read there. Keep the rest of the sentence as it is.
