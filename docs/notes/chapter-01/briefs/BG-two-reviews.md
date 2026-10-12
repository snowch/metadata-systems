# Brief BG: changes from two outside reviews of Chapters 1 and 2

Two reviewers read both chapters. The author accepted these changes: the warning moves below the
opening and folds its measurements away; Chapter 1 drops explanations a data engineer already has
and says what to look for in the tour; Chapter 1 gets a cell for the learner's guesses; Chapter 2
shows the warehouse's record before saying what it holds; Chapter 2 says which record would have
answered each of its three changes; and Chapter 2's close names the records later chapters build,
using the words "lineage" and "run" once each, as names of what is coming.

Write each slot following `docs/style.md` and `AGENTS.md`. British English. No em dashes. Do not
mention a lab, an engine, a simulator, Jupyter, JupyterLite or Pyodide. The reader is "you", a data
engineer. Keep names in backticks exactly as written. Change only what a slot asks. Do not use
"run" as a noun, "lineage", "event" or "catalogue" except where a slot says so. A block of code is a
"cell".

## Facts (checked against the shop's data and the measurements on record)

- Chapter 1's page: the first time you open it, your browser downloads about 13 MB. On a computer,
  running every cell took 10 to 12 seconds, and the page used about 400 MB of memory. If a phone runs
  short of memory, the browser may reload the page, and a reload loses anything you have not saved.
- Chapter 2's page: the first time you open it on its own, about 13 MB; opened from Chapter 1's link,
  in a browser that had opened Chapter 1, it downloaded less than 1 MB (measured on a computer).
  Chapter 1's link opens it in a new tab; Chapter 1 stays open in its own tab and keeps its own
  memory, so on a phone closing Chapter 1 leaves more memory for this page. Running every cell took
  10 to 12 seconds, and the page used about 420 MB of memory. The same reload sentence applies.
- `products.csv` holds 8 products in 6 categories. Its columns: `product_id`, a name, a category,
  `list_price_pence`, and `updated_by` (the member of staff who last edited the product). A CSV file
  names its columns and stores every value as text: it has no types.
- `customers.jsonl` holds 10 customers in 7 countries. Fields: `customer_id`, a name, `email`, a
  country as a two-letter code, `signed_up`. A JSON Lines record names its fields, but a date such as
  `signed_up` is just a string: the file has no date type.
- Each night the export writes every file again; `orders.jsonl` holds every order since the store
  opened.
- In Chapter 2, the warehouse's record of `daily_sales` (the cell shows it): two columns, `day` and
  `revenue_pence`, with their types; 7 rows and a size in bytes; a created time, 1 September; a
  last-altered time, 02:30 on Monday 14 September; an owner, `etl_service`. Nothing else.
- Chapter 2's three changes, and the record that would have answered each: the analyst's copy (which
  source the job read) needs a record of what the job read; the edited job (from Saturday it keeps
  every order not refunded) needs a record of which version of the job's code ran each night; the
  failed night needs a record of whether each night's write succeeded.
- Later chapters: Chapter 3 makes a description of each asset (what it means, who is responsible
  for it). Chapter 6 records what was made from what, which is called lineage. Chapter 7 records each
  run of a job: when it started and ended, which version of its code ran, what it read and wrote, and
  whether it succeeded.

## Slots

A. **ch1_warning_line**: one sentence, always visible, for Chapter 1's warning box: the page runs
Python in your browser, and the first time you open it your browser downloads about 13 MB.

B. **warning_more**: a short label (two to four words) for the part of each warning box the reader
opens for the details, about time and memory. Not a sentence.

C. **ch1_warning_details**: Chapter 1's details, from the facts: the 10 to 12 seconds, about 400 MB,
and the reload sentence. Keep these phrases word for word: "running every cell took 10 to 12
seconds", "the page used about 400 MB of memory", "a reload loses anything you have not saved".

D. **ch2_warning_line**: one sentence, always visible, for Chapter 2's box: the page runs Python in
your browser, and the first time you open it on its own your browser downloads about 13 MB. Keep
"downloads about 13 MB".

E. **ch2_warning_details**: Chapter 2's details, from the facts, in this order: less than 1 MB from
Chapter 1's link; the new tab and its memory; 10 to 12 seconds and about 420 MB; the reload sentence.
Keep word for word: "the page downloaded less than 1 MB when opened from Chapter 1's link", "running
every cell took 10 to 12 seconds", "the page used about 420 MB of memory", "a reload loses anything
you have not saved".

F. **ch1_objectives**: Chapter 1's objectives, as a short Markdown list of three items, framed around
the opening question: what you need to establish about the platform before you can look into a
reported discrepancy. The items: what the platform holds (three systems; files, tables, a dashboard);
what happens on it each night, and what you cannot see of it (the export, the jobs, when they are due
to run, any notes); and a written guess, for each warehouse table, at what it is made from. Start
each item with a verb.

G. **ch1_look_for**: one or two sentences, placed before the tour of the three files: as you read each
file, note which fields could tie it to a table in the warehouse, and anything in the rows that a job
might have to deal with. Do not say what the learner will find.

H. **ch1_products**: replaces "`products.csv`, in object storage, holds the shop's product catalogue:
8 products in 6 categories. Each product has an id (`product_id`), a name, a category, a list price in
pence (`list_price_pence`) and the member of staff who last edited it (`updated_by`). `products.csv`
names its columns once, in its first line, and has no types: every value is text." Keep "holds the
shop's product catalogue: 8 products in 6 categories" word for word. Drop the explanation of how CSV
names its columns; keep the fact that it stores every value as text, with no types.

I. **ch1_customers**: replaces "`customers.jsonl` holds the shop's 10 customers, in 7 countries. A
customer's record has five fields: ... `orders.jsonl` and `customers.jsonl` are JSON Lines, with one
record per line, and every record names its fields. A JSON value has one of a few types, such as a
string, a number, true or false, or null, and a date or an amount is just a string or a number."
Keep "holds the shop's 10 customers, in 7 countries" word for word and the five fields. Drop the
explanation of JSON Lines and of JSON's types; keep that a record names its fields and that a date is
just a string, with no date type.

J. **ch1_guesses**: replaces Chapter 1's last section's text, "For each of the three tables, write down
which file or table you think it is made from, and what on this page makes you think so. Keep what
you wrote. Chapter 2 asks what evidence like this can establish." The learner now writes in the cell
below, one line per table, and presses **Save** to keep it. Keep: which file or table each is made
from, and what on this page makes you think so; Chapter 2 asks what evidence like this can establish.

K. **ch1_guesses_cell**: the text that starts inside the guesses cell, between triple quotes, for the
learner to fill in: one line per table (`clean_customers`, `clean_orders`, `daily_sales`), each with
room for the source and the reason. Plain text; no backticks; each line at most about 60 characters.

L. **ch2_guess_daily_sales**: replaces "Take out the guess you wrote for `daily_sales` at the end of
Chapter 1. Compare it with the query in the cell below, which the data supports." The guesses are now
in Chapter 1's last cell. Keep the comparison with the query below.

M. **ch2_holds_lead**: Chapter 2, "What the platform holds" now opens with the cells, and the
paragraph that states the record moves after them. Write one or two sentences that open the section:
a question (what does the warehouse record about `daily_sales`?) and what the two cells below read
(the warehouse's record of its own tables, which you query with SQL as `information_schema`:
`information_schema.tables` has one row per table, and `information_schema.columns` one row per
column, with the column's type). Do not state what the record contains: the cells show it.

N. **ch2_holds_after**: after the two cells, replaces "Take `daily_sales`. The warehouse records two
columns, ... and an owner, `etl_service`. It records nothing else about the table." Say what the
cells showed, from the facts, and keep "It records nothing else about the table." Do not open with
"Take `daily_sales`."

O. **ch2_which_record**: a new paragraph in "Records made at the time", after its list: which record
would have answered each of the three changes (facts above), one clause each, in the order the
changes came (the copy, the edit, the failed night). Also: the list's second item, "what happened:
each night's write of `daily_sales`, when it ran, what it read, and whether it succeeded", gains
"which version of the job's code ran"; write that item again with it.

P. **ch2_close**: replaces Chapter 2's closing paragraph, "Chapter 3 starts making them: a description
of each asset, kept beside the data, with what the asset means and who is responsible for it. It
then asks the four questions at the start again, to see which of them that record answers." Keep both
sentences, then name the records later chapters build (facts above), so a reader sees where the
course goes: Chapter 6, a record of what was made from what, which is called lineage; Chapter 7, a
record of each run of a job. Use "lineage" once and "run" as a noun once, here only.

Write the slots under `## A` to `## P`, each the exact text to place.
