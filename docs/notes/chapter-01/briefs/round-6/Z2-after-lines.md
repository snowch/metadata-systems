# Brief Z2: two of the decision's lines, sent back

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief. Write your draft to `docs/notes/chapter-01/drafts/round-6/Z2.md`.

Your draft of brief Z said "`orders.parquet` keeps one row per order". The fault was the brief's:
it is not true. Each row of `orders.parquet` is an order, but one order appears twice, which the
learner finds in the chapter's last challenge. So neither line may say how many rows an order
has. The corrected facts are in `docs/notes/chapter-01/facts.md`, under "Where to look first".

## wAfter

Two of the lines shown after the decision about where to look first, in Markdown, names in
backticks. Each says what that asset can show: a fact about the asset's shape, never what it shows
for Thursday. Write them as a list, `orders:` then `clean:`. Facts, in this order:

- orders: each row of `orders.parquet` is an order, with its price, quantity and status. It shows
  what Thursday's 205.50 is made of. It does not say which orders `daily_sales` counts.
- clean: each row of `clean_orders` is an order too, with the same columns as `orders.parquet`.
  Set beside it, it shows which orders the two hold differently.
