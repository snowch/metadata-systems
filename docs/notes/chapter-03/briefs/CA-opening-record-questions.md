# Brief CA: Chapter 3's opening, the record of `daily_sales`, and the four questions again

Chapter 3, "What is metadata?", is a Jupyter notebook for a data engineer. The reader is "you". It
follows Chapter 2, where you found that `daily_sales` leaves out three of Thursday's orders and that
nothing on the platform records why. In this chapter you write records about the shop's assets and
find what they answer. Write each slot below, following `docs/style.md` and `AGENTS.md` (attached):
British English, short plain sentences, no em dashes, no filler, no reassurance, no "in this chapter
we will", nothing that personifies a system or a record. Keep every name in backticks exactly as
written. A block of code is a "cell". The buttons are **Run all**, **Run below** and **Save**, in
bold, and no other control is named.

Words you must not use anywhere: entity, attribute, identifier, dataset, graph, node, edge, lineage,
upstream, downstream, event, observation, freshness, identity, environment, assertion, namespace,
the noun "run" (say "night", "write" or "time"; "run the cell" is fine), "lab", "engine",
"simulator", "Jupyter", "Pyodide". Do not use "descriptive", "operational" or "schema" in this brief:
a later section introduces them.

Write the file once. Do not change it after you reply.

## Facts (each checked against the shop's data)

- The day is still Monday 14 September 2026; it is the afternoon.
- From Chapter 2: `daily_sales` leaves out Thursday's three orders with no customer id (orders 7021,
  7023 and 7025, worth 15400 pence together), because `clean_orders` does not have them. Nothing on
  the platform records whether they should be left out.
- You asked the head of the shop who decides what `daily_sales` should count. The head's reply
  says three things: Jo Marsh, in finance, built the dashboard and decides what counts as revenue;
  Sam Lund keeps the product catalogue; the two cleaned tables, `clean_customers` and
  `clean_orders`, were the last engineer's and are now yours.
- Jo Marsh's answer, about a day's revenue: the value of every completed order placed that day,
  taking the day from the order's time in UTC, in pence. Never refer to Jo with "he" or "she":
  repeat the name.
- A record, in this chapter, is a set of lines of text you write and keep beside the data. One fact
  per line: the asset's name; then a column's name, if the fact is about a column; then a field; a
  colon; and the value. Example: `daily_sales revenue_pence unit: pence`. A value of dots,
  `........`, is one not yet written.
- You choose the field names. The cells use three: `means` (what the asset or the column means),
  `responsible` (who to ask about it) and `unit`.
- The record cell holds five lines for `daily_sales`, each with `........` for its value: what the
  table means, who is responsible for it, what `day` means, what `revenue_pence` means, and the unit
  of `revenue_pence`. You replace each `........` with what the head of the shop and Jo told you,
  select the cell and press **Run below**. The cell then shows the record as a table, one row per
  line. **Save** keeps what you wrote.
- The check cell lists each column of `daily_sales` that has no description (no `means` line with
  a value), and each line that names a column the warehouse does not have. With every line written,
  it finds no problems.
- Chapter 2 opened with four questions the platform could not answer:
  - Is Thursday's total wrong, and since when?
  - Can we delete `products.csv`? Does anything still read it?
  - If the checkout renames a column in `orders.jsonl`, what stops working?
  - Who should I ask about `daily_sales`?
- Before the cells that answer them, you write in a cell, for each question, whether your record
  answers it, in part or not at all, and why. **Save** keeps it.
- The first query cell asks the record who is responsible for `daily_sales`. It returns Jo Marsh.
- The next cell turns Jo's words into a query over `orders.jsonl`: it keeps each completed order
  once, even an order the export wrote twice, adds up price times quantity for each UTC day, and
  puts that total beside each row of `daily_sales`, marked `same` or `different`.
- Its result: Thursday is the only day that differs, 5150 pence in `daily_sales` against 20550 by
  Jo's meaning. Every other day is the same.
- "Every completed order" does not say what to do with an order the export wrote twice. The query
  had to decide: it counts each order once. A query that counted every line of the file would also
  find Wednesday different, because order 7015 is in the file twice.
- By the meaning Jo gave, Thursday's total is wrong. The record says nothing about since when: it
  holds no time and nothing about what happened each night.
- The next cell compares `daily_sales` with the meaning you could have written from the data
  alone: Chapter 2's query, the completed orders in `clean_orders`, added up per day.
- Its result: every day is the same, Thursday included. A description written from the data agrees
  with the data on every day, so it cannot show that any day is wrong. Jo's description came from
  the person who decides what revenue means, not from the table, so the table can be checked
  against it.
- The last cell of the section lists every line of your record that names `products.csv` or
  `orders.jsonl`. It finds none. The second and third questions ask what reads those files; a record
  of what each asset is does not say what reads it. Chapter 6 records that. (Do not name what
  Chapter 6 calls it.)

## Slots

A. **objectives**: Chapter 3's objectives, a Markdown list of four items, each starting with a verb:
write a record of `daily_sales` from what the shop's people tell you; find which of Chapter 2's
four questions the record answers; tell what a record of an asset holds from what the systems
record about it (without the words "descriptive", "operational" or "schema"); test a requirement
about descriptions, and a check, against changes to the shop.

B. **opening**: the section "## Monday afternoon": one or two short paragraphs. The day; what
Chapter 2 found (one sentence); the question you asked; the head of the shop's reply, quoted as a
message; Jo's answer, quoted. End with one sentence saying what you do next: write what you have
learnt as a record kept beside the data, then ask Chapter 2's four questions again.

C. **record_lead**: before the record cell, the section "## A record of `daily_sales`": the notation
(with the example line), the three field names, and what to do with the dots (replace, select, press
**Run below**), and what the cell then shows.

D. **check_lead**: one or two sentences before the check cell: what it lists, and that with every
line written it finds no problems.

E. **questions_lead**: the section "## The four questions again": that Chapter 2 opened with four
questions (list them as Chapter 2 did, word for word, as a Markdown list), and what to write in the
next cell before running the cells below it.

F. **questions_cell**: the text inside the cell, between triple quotes, for the reader to fill in:
the four questions, shortened to fit about 60 characters each, each followed by `........`. Plain
text; no backticks.

G. **who_lead**: one sentence before the cell that asks who is responsible for `daily_sales`.

H. **meaning_lead**: after the answer, Jo Marsh, one sentence saying the record answers the fourth
question; then what the next cell does with Jo's words (facts above), including that it counts an
order the export wrote twice once.

I. **meaning_after**: after that cell: the result; Thursday wrong by Jo's meaning; the record says
nothing about since when; and the fact about the order written twice and Wednesday.

J. **reconstruction_lead**: one sentence before the cell comparing `daily_sales` with Chapter 2's
query over `clean_orders`.

K. **reconstruction_after**: its result and what it means (facts above).

L. **files_lead_and_after**: one sentence before the cell that lists lines naming the two files,
and one or two after it: none; the two questions ask what reads the files; a record of what each
asset is does not say; Chapter 6 records that.

Write the slots under `## A` to `## L`, each the exact text to place.
