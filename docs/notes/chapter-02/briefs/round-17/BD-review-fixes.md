# Brief BD: Chapter 2's fixes from round 17's review

Round 17's review read Chapter 2 against today's Chapter 1, and a sceptic upheld the findings
below (`docs/notes/chapter-02/review/round-17/verdicts.md`). Each slot gives the current text, what
is wrong, and the facts the new text must carry. Write each slot following `docs/style.md` and
`AGENTS.md`. British English. No em dashes. Do not mention a lab, an engine, a simulator, Jupyter,
JupyterLite or Pyodide. The reader is "you", a data engineer who has done Chapter 1. Keep names in
backticks exactly as written. Change only what a slot asks; keep its other sentences as they are.

Words fixed across the course: the things that run each night are **jobs**; the **export** from the
shop's checkout and catalogue writes the three files; the head of the shop's line is a **message**,
"Thursday's revenue looks wrong.", not a question; "catalogue" means the shop's products only, never
the warehouse's record of its tables; a block of code is a **cell**, never "code cell". Never use
"run" as a noun; "run" as a verb is fine. Do not use the words "lineage", "job" as a technical term,
"event" or "metadata" before the slot that introduces metadata (slot R).

## Facts the slots draw on (checked against the shop's data)

- Thursday 10 September: 7 orders in `orders.jsonl`, all completed, adding up to 20550 pence.
  `daily_sales` says 5150 for Thursday. The difference is 15400 pence, £154.00.
- 3 of Thursday's orders have no customer id: orders 7021, 7023 and 7025. Together they are worth
  15400 pence. `clean_orders` does not have them.
- The raw orders and `daily_sales` agree on Monday, Friday and Sunday, and differ on Tuesday,
  Wednesday, Thursday and Saturday.
- The warehouse records `etl_service` as the owner of all three tables. The name looks like an
  account a program logs in as; the warehouse records nothing more about it.
- In the shop's design (which the learner cannot see, and which the platform does not record), one
  job writes `clean_orders` from `orders.jsonl` with four rules: keep one row of an order the export
  wrote twice, drop orders with no customer id, keep cancelled orders, drop orders with a quantity
  of 0 or less. No order in the week has a quantity of 0 or less.
- A query over `clean_orders` (completed orders, price times quantity, per day) gives every row of
  `daily_sales`. The learner wrote a guess at the end of Chapter 1 for each warehouse table: which
  file or table it is made from, and why.
- The menu's last cell lists every query, from a fixed set of simple ones over the week's assets,
  that gives every row `daily_sales` has, even with a row more. Each row of its result is one query:
  `source` is the asset it reads; `keep` which orders it keeps (all, completed or cancelled);
  `measure` what it adds up (revenue, quantity or rows); `per` what it groups by (day, customer or
  product); `sql` the query itself. As the shop is: one query, over `clean_orders`. With the
  analyst's copy: two, `clean_orders` and the copy. With the edit for refunds: none. With the failed
  night: one, over `clean_orders` (it still has Sunday's row, which `daily_sales` lacks).
- On the failed night `daily_sales` has 6 rows, none for Sunday, and was last altered on Sunday at
  02:30, a day earlier than `clean_orders` (Monday at 02:05) and the dashboard (refreshed Monday at
  03:00). Each record is a normal record; only comparing the times shows the gap.
- Object storage records three things about a file: its key (its full name, such as
  `s3://shop-raw/orders.jsonl`, where `shop-raw` is the bucket, the container the file sits in), its
  size in bytes, and when it was last modified.
- `warehouse.sql(..., files={"raw_orders": "s3://shop-raw/orders.jsonl"})` lets one query read a
  file from object storage as if it were a table, here called `raw_orders`.
- The handover note is now a cell: the learner writes between the triple quotes and presses
  **Save** to keep it. Text typed into a box would be lost on a reload; a cell is kept.

## Slots

A. **message** (Chapter 1, its last section). Current: "[Chapter 2](chapter_02.ipynb) goes back to
the head of the shop's line and starts with Thursday's revenue." Say "message" for "line". Keep the
link exactly.

B. **questions_lead** ("Questions the platform cannot answer", the line before the list). Current:
"Questions like the head of the shop's arrive every week on a platform you did not build:". It calls
the message a question and is clumsy. Say that messages like the head's arrive every week on a
platform you did not build, and each raises questions like these (the list follows).

C. **questions_after** (same section, after the list). Current: "Each is answered by something that
happened, or by a decision somebody made: a job that reads a file, a rule somebody chose, a person
who took responsibility. None of them is answered by the rows a table holds today." Fix: "somebody"
twice; and the rows do answer part of the first question (whether the total differs). Keep the
point: the full answers need what happened or what somebody decided, which the rows do not hold.

D. **thursday_open** ("Thursday", first paragraph). Current: "Start with the arithmetic. `orders.jsonl`
holds every order the shop took, as the checkout sent it. Thursday's orders add up to 20550 pence.
`daily_sales` holds one row per day, with amounts in pence, and its Thursday row says 5150; the
dashboard shows £51.50. Somewhere between the file and the table, 15400 pence, £154.00, went
missing." Fix: drop "Start with the arithmetic." (a signpost); drop the two descriptions Chapter 1
already gave (what `orders.jsonl` holds; what `daily_sales` holds); say the two totals differ by
15400 pence, £154.00, rather than that money "went missing" (the raw total is not known to be right).

E. **thursday_rerun** ("Thursday", before the cell that reads `daily_sales`). Current: "The code cell
below reads the row from `daily_sales` for the day that the code cell above sets. If you change the
day in the code cell above, run the code cell below too. It does not run again by itself. Select the
code cell above and press **Run below**, which runs that cell and every cell below it." Fix: "code
cell" to "cell"; drop the clause defining Run below (Chapter 1's box defines it); keep the
instruction to select the cell above and press **Run below**.

F. **compare_lead** (before the cell that compares every day). Current: "The cell below puts, for
every day, the total of the raw orders in `orders.jsonl` beside that day's row in `daily_sales`. It
shows whether the two are the same." Add the fact about `files=` in one sentence.

G. **thursday_orders_lead** (new, after the comparison cell's text "It is not only Thursday ... or
why."). One or two sentences before a new cell. The new cell lists Thursday's orders in
`orders.jsonl` that have no customer id. Ask the learner to look at what these orders have in
common, and compare their total with the gap. Do not give the total or the count: the cell shows
them.

H. **thursday_orders_after** (new, after that cell). One or two sentences: the 3 orders, 7021, 7023
and 7025, have no customer id; together they are 15400 pence, the whole of Thursday's gap; and
`clean_orders` does not have them. Say that this shows which orders are missing, not why: nothing on
the platform records the rule that left them out.

I. **holds_open** ("What the platform holds", second paragraph). Current: "The cell below reads the
warehouse's record of `daily_sales` from its catalogue, which you query with SQL. ..." Replace "from
its catalogue" so that "catalogue" is not used for the warehouse's record: the warehouse keeps a
record of its own tables, which you query with SQL as `information_schema`. Keep the sentence about
`information_schema.tables` and `information_schema.columns`.

J. **storage_record** (same section). Current: "Object storage records as much about a file: its
location, its size and when it was last modified. The reporting tool records ... The cell below
lists the files in the bucket `shop-raw`. For each file, object storage records its key, its size in
bytes and when it was last modified." Fix: "as much" is vague; "location" should be "key"; say once
what a key and a bucket are (facts above); do not list the three fields twice.

K. **state_not_history** (end of "What the platform holds"). Current: "... The platform has a
complete picture of its own state and no account of its history." Fix: this personifies the
platform and overstates. Say plainly that the platform records the current state of each asset and
none of its history.

L. **fields_for** ("What the fields are for", first paragraph). Current: "... In the shop's platform,
and in most real ones, a system records what its own work needs and nothing more. ..." Restrict the
claim to the shop's platform: drop "and in most real ones" (the chapter's close says real platforms
keep more). Keep the rest.

M. **owner** ("What the fields are for", second paragraph). Current: "The owner field shows how far
that goes. "Who should I ask about `daily_sales`?" wants a person or a team. The warehouse answers
`etl_service`, the account that all four of the shop's jobs log in as. The field is called owner, but
the question it answers is which account controls the table. The requirement that every table has an
owner is met, and your question is not." Fix: state the requirement before saying it is met, as a
requirement might be written: "Every table must have an owner."; do not say the jobs log in as
`etl_service` or how many jobs there are (the learner cannot see them): use the facts above about
what the warehouse records. Keep: the field is called owner, but the question it answers is which
account controls the table; the requirement is met as written, and your question is not.

N. **owner_cell** (same section). Current: "The cell below lists the owner of every table in the
catalogue." Replace "in the catalogue" (say every table in the warehouse).

O. **guess_daily_sales** (new, in "Reconstruction", before its first paragraph's last sentences or
just before the cell). One or two sentences: take out what you wrote at the end of Chapter 1 for
`daily_sales`; compare it with the query below, which the data supports. Do not say whether the
learner's guess is right.

P. **menu_lead** (the line above the menu). Current: "Choose a change to the shop from the menu
below. Then select the first cell below the menu and press **Run below**. The cells below show the
platform on Monday morning, after the week ran with the change you chose. The cells above the menu
keep showing the week as it ran." Add, first, what to look for: for each change, which of the
platform's records show it, and whether a query still gives every row of `daily_sales`. Keep the
instructions.

Q. **queries_lead** (the bold heading line before the last cell under the menu, now a sentence).
Current: "**Queries that give every row of `daily_sales`**". Replace with one or two sentences that
say what the cell lists and what each column means (facts above), including that a query counts if
it gives every row `daily_sales` has, even with a row more.

R. **failed_night** ("Reconstruction", the failed-night paragraph). Current: "... Everything the
platform records looks like a normal morning with one row fewer. Only a record of the failure would
say that a write was due and did not happen." Fix the overclaim: each record is normal on its own;
only comparing the last-altered times shows the gap (facts above). Keep the last sentence.

S. **guess_clean_orders** (new, in "A rule the week never tests", before "The cell below counts").
One sentence: your guess for `clean_orders` from Chapter 1 meets the same limit: the data can
confirm a rule only where some row would have triggered it.

T. **rules_design** ("A rule the week never tests", first paragraph). Current: "... `clean_orders` is
made from `orders.jsonl` by a few rules: ... The last rule is in the job. ..." Fix: mark the rules as
the shop's design, which the platform does not record and the learner could not have seen (the
paragraph then shows the data cannot tell whether the last rule exists); say "four rules", not "a
few". Keep the rest of the paragraph.

U. **made_from** ("Records made at the time", third list item). Current: "what was made from what:
`daily_sales` is built from the completed orders in `clean_orders`, and the dashboard reads
`daily_sales`." Fix: say this is what such a record would say, not a fact the learner has seen
recorded.

V. **handover_cell** ("The handover"). Current paragraph ends: "... Then compare it with what the
warehouse records: two column names, a row count, a size, two times and an account." and the next
text is "You write your handover note in the box above. The cell below shows only what the warehouse
records about `daily_sales`, so you can compare it with your note." The box becomes a cell (facts
above). Rewrite the second text so it says: write your note in the cell above, between the triple
quotes; press **Save** to keep it; the cell below shows only what the warehouse records about
`daily_sales`, to compare with your note.

W. **note_placeholder** (the text that starts inside the note's cell, between the triple quotes, for
the learner to replace). Current: "Write what daily_sales means and who to ask about it. Include what
runs each night, what it reads and what it writes, and what to do when a night fails." Keep its
content; plain text, no backticks; at most two short lines of about 70 characters each.

X. **reflect** ("Before Chapter 3", new, between its first paragraph and the paragraph about Chapter
3). Two or three reflective questions, as a short list, that carry the chapter to new situations: one
on the learner's guess for `clean_customers` (nothing in this chapter tested it: what would?), one on
a table on a platform the learner works on, and one leading into Chapter 3 (what a description of
an asset would have to say to answer "Who should I ask about `daily_sales`?"). Questions only; no
answers.

Y. **warning** (Chapter 2's warning box). Current: "The page runs Python in your browser, and the
first time you open it on its own, your browser downloads about 13 MB. Measured on a computer, the
page downloaded less than 1 MB when opened from Chapter 1's link, in a browser that had opened
Chapter 1. Chapter 1's link opens this page in a new tab, and Chapter 1 stays open in its own tab.
On a computer, running every cell took 10 to 12 seconds, and the page used about 420 MB of memory.
If a phone runs short of memory, the browser may reload the page, and a reload loses anything you
have not saved." Fix: the new-tab sentence states no consequence. Keep every measurement as it is
(13 MB on its own; less than 1 MB from Chapter 1's link in a browser that had opened Chapter 1;
10 to 12 seconds; about 420 MB). Say the consequence of the new tab: Chapter 1 stays open in its own
tab and keeps its own memory, so on a phone closing it leaves more for this page. Keep the last
sentence. Keep the phrases "downloads about 13 MB", "the page downloaded less than 1 MB when opened
from Chapter 1's link", "running every cell took 10 to 12 seconds", "the page used about 420 MB of
memory" and "a reload loses anything you have not saved" word for word.

Z. **close_note** ("How this differs from a real platform", its last paragraph). Current: "A file's
size is its real size in bytes. A table's size is an estimate from its rows. All times are UTC. A
real platform has hundreds or thousands of assets; searching for queries that rebuild one would cost
far more. "No simple query reproduces it" means none that keeps every row, completed orders or
cancelled orders of one asset; a query with a condition on the date would." Fix: the last sentence
is hard to parse and does not match the chapter's words ("no simple query over the week's assets
reproduces it"): say that the simple queries are those the menu's last cell tries (facts above), and
that a query with a condition on the date could still reproduce the edited table. Keep the first
four sentences.

Write the slots under `## A` to `## Z`, each the exact text to place.
