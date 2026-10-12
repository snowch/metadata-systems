# Brief CE: Chapter 3, revised after its review

Chapter 3, "What is metadata?", was reviewed by a reader on another model, and a sceptic checked
each finding (`docs/notes/chapter-03/review/findings.md`, `verdicts.md`). Revise the slots below.
For each slot you get the text now on the page and what must change. Keep every sentence that the
notes do not touch, word for word; change only what the notes ask, in the same plain style. Follow
`docs/style.md` and `AGENTS.md` (attached): British English, short plain sentences, no em dashes, no
filler, nothing that personifies a system, a record or a check, no narration of what the chapter
does next. Keep every name in backticks exactly as written. The buttons are **Run all**, **Run
below** and **Save**.

Words you must not use: entity, attribute, identifier, identity, dataset, graph, node, edge,
lineage, upstream, downstream, event, observation, freshness, environment, assertion, namespace,
the noun "run", "lab", "engine", "Jupyter". Never refer to Jo Marsh or Sam Lund as "he" or "she".

**One word, one meaning.** On this page, *record* means only the reader's set of lines (the
variable `records`, "your record of `daily_sales`"). What a system keeps is its *information* or
its *fields*. One line of the record is a *line*. *Meaning* is what Jo said revenue is; a
*description* is a `means` line.

Write the file once. Do not change it after you reply.

## Facts that changed (checked against the shop's data)

- The head of the shop's reply, quoted, now says: for `daily_sales` and the dashboard, ask Jo Marsh
  in finance, who built the dashboard and decides what counts as revenue; Sam Lund keeps the
  product catalogue; the two cleaned tables, `clean_customers` and `clean_orders`, were the last
  engineer's and are now yours. Jo Marsh's answer is unchanged.
- The steps box tells the reader to press **Run all** first, and **Run below** from the record
  cell runs every cell below it. So when the reader reaches a cell for their expectation, the cells
  below it have already run. Each expectation must be written "before you read on" (or "before you
  look at the cells below"), never "before you run".
- After **Run all** and before the reader fills in the record, the cells below the record show the
  dots, and the checks list them as problems. The reader should be told this at the record cell.
- The check's problem messages now distinguish a column with no `means` line from one whose
  `means` value is still dots. The record's lines are numbered from 1.
- The example line must not be one of the five the reader fills in: use
  `clean_orders price_pence unit: pence`.
- Tuesday, Wednesday and Saturday differed from the raw totals in Chapter 2 but agree with Jo's
  meaning, because the query leaves out cancelled orders and counts the order the export wrote
  twice once. Thursday differs because its three orders with no customer id are completed orders,
  which Jo's meaning counts.
- The description written from the data is Chapter 2's query, which was chosen because it
  reproduces `daily_sales`; it agrees with the table on every day for that reason.
- Every line of the reader's record is about `daily_sales`. None can say what reads a file.
- Chapter 2's definition, which this chapter keeps: metadata is information about an asset or about
  the platform.
- `updated_by` describes products in the shop's catalogue, and an edit made in the catalogue, which
  is not one of the platform's assets; the export copies it into the file. It is the shop's data.
  A field that said who last wrote `products.csv` would be metadata about the file.
- What the warehouse keeps about a table: columns and types and its owner (an account) say what
  the table is and who controls it now. The last-altered time records when the last write happened;
  the row count and the size measure the table as that write left it; the created time records when
  it was created. The warehouse keeps the last of each, not a history: Chapter 2 found it records
  no history. For `clean_customers`, which each night replaces with the same 9 rows, only the
  last-altered time changes from night to night.
- Object storage: a file's key gives its name and where it is; its size and last-modified time
  come from its last write. The reporting tool: the dashboard's title says what it is; who created
  it and when, and when it last refreshed, record things done to it.
- The criterion: information about what an asset is, or who controls it now, is **descriptive**;
  information about work done on the platform (who did something, when, and what it left) is
  **operational**.
- The word *schema* is also used for something else: in `information_schema` and its column
  `table_schema` (Chapter 2 showed `analytics` there), it names a group of tables in a database.
- The requirement exercise asks about one column: does the line `daily_sales revenue_pence means:
  the revenue in pence` describe the column `revenue_pence` as the requirement asks? The readings
  are five: as written, a `means` line with a value (the check's rule); what the column means
  (which orders it counts); its unit; where its values come from; whether it may be empty. The line
  already says "in pence"; under the reading about meaning it says nothing the name `revenue_pence`
  did not.
- The stale-record section: two comparisons, which detect different things.
  - The check compares the record's columns with the warehouse's. It reports `order_count`: the
    record is now incomplete.
  - Jo's query compares the values with Jo's meaning. After the edit, Saturday differs (21549
    against 19149 pence): the table no longer matches the meaning the record holds. The record has
    not changed and Jo's meaning has not changed.
  - Neither says what changed in the job, when, or who changed it. A record made at the time, of
    which version of the job's code ran each night (Chapter 2's words), would say. Chapter 7 makes
    such records.
- The check never meets a line about a column the warehouse lacks in this chapter: do not mention
  that it lists such lines.
- The close must state the requirement's result too: met as written by four lines of code, and by
  no description that says more than the column's name.
- Chapter 4 begins from two values: the reader's record names Jo Marsh as responsible for
  `daily_sales`; the reporting tool records `j.marsh` as the dashboard's creator. No record says
  that the two name one person.
- PostgreSQL's documentation: comments "can be viewed using psql's \d family of commands".

## Slots: current text, then what must change

A. **objectives** (now: "Write a record of `daily_sales` from what the shop's people tell you." /
"Find which of Chapter 2's four questions the record answers." / "Tell what a record of an asset
holds, from what the systems record about it." / "Test a requirement about descriptions, and a
check, against changes to the shop."). Keep the first two. Replace the third with: tell the
information that says what an asset is from the information about what happened to it (no
rationed words). Split the fourth into: question the requirement "Every column must have a
description."; find what a check against the warehouse catches when the shop changes.

B. **opening**: now three paragraphs and two quotes, ending "Next, you write what you have learnt as
a record kept beside the data, then ask Chapter 2's four questions again." Change: the first
paragraph says you sent the head of the shop what Chapter 2 found (keep its facts), not that you
asked who decides; the head's reply is the new quote above; Jo's answer stays; replace the last
sentence with the problem, not a roadmap: none of this is on the platform, and the next engineer to
look at `daily_sales` would have to ask again.

C. **record_lead**: keep, but the example line becomes `clean_orders price_pence unit: pence`, and
add, at the end, that until the dots are filled in and **Run below** is pressed, the cells below
show the dots, and the checks list them as problems.

D. **check_lead** (now: "The check cell lists each column of `daily_sales` that has no description,
meaning no `means` line with a value. It also lists each line that names a column the warehouse
does not have. With every line written, it finds no problems."). Drop the second sentence.

E. **questions_lead**: keep, but "Before you run the cells below" becomes "Before you read on".

F. **questions_cell**: keep as it is.

G. **who_lead**: keep.

H. **meaning_lead** (now begins "The record answers the fourth question: it names Jo Marsh as
responsible for `daily_sales`."). Change the first sentence: the record answers the fourth
question with Jo Marsh, the name you wrote from the head's reply, now kept where the next engineer
can query it. Keep the rest, but it says only once that the query counts an order the export wrote
twice once (see I).

I. **meaning_after**: keep the first two paragraphs; add one sentence after "Every other day is the
same." on why Tuesday, Wednesday and Saturday agree now and Thursday does not (facts above).
Replace the third paragraph (on "every completed order" and Wednesday) with: the file holds order
7015 on two lines; the words "every completed order" do not say whether a line or an order is
counted; the query counts orders; a query that counted every line would find Wednesday different
too.

J. **reconstruction_lead**: keep.

K. **reconstruction_after**: say that Chapter 2's query was chosen because it reproduces
`daily_sales`, so a description written from it agrees with the table on every day and cannot show
any day wrong. Keep the sentence on Jo's description.

L. **files_lead_and_after** (now: "The last cell lists each line of your record that names
`products.csv` or `orders.jsonl`." / "It finds none. The second and third questions ask what reads
those files. A record of what each asset is does not say what reads it. Chapter 6 records what
reads each asset."). Drop "last"; after the cell: every line of the record is about `daily_sales`,
so none could say what reads a file; keep the rest.

M. **kinds**: the section "## What the platform records already", now five paragraphs. Replace with
one short sentence, then a Markdown list of the three systems, each with what its fields say (from
the facts), then the criterion with the two terms in bold, then one sentence that the warehouse
keeps the last of each, not a history, and one that your record is descriptive.

N. **schema_lead**: keep, but add one sentence on the second use of the word (facts above), and
change "Each line names its fields" to "Each line of the file names its fields".

O. **person_lead**: the section "## A column that names a person". Put the question first: does the
column `updated_by`, whose values include `s.lund`, say who to ask about `products.csv`? Then what
the next cell counts. Keep Sam Lund.

P. **person_after**: drop the sentence that restates the counts; keep "Three people last edited the
8 products." Then say what `updated_by` describes (facts above), that it is the shop's data, and
what kind of field would be metadata about the file. Keep the paragraph on the first line. Replace
the last paragraph with Chapter 2's definition (information about an asset or about the platform),
and that where the information is kept does not decide it, with the two examples.

Q. **requirement_lead**: the requirement stays; the question becomes whether the line describes
the column `revenue_pence` as the requirement asks; "Before you read on" stays.

R. **verdict_cell** (now three lines). Make the question: "Does this line meet the requirement for
revenue_pence? Why?" Keep the rest.

S. **readings**: the five readings as a Markdown list, the first being the requirement as written
(the check's rule), each with what it needs; then that the line already says "in pence", and under
the reading about meaning says nothing the name did not.

T. **full_check_lead**: keep.

U. **by_name_after** (now: "With a description for each of the 14 columns, the check finds no
problems: the requirement is met as written."): say that the check's rule, the requirement as
written, is met. Keep the next sentence.

V. **by_name_meaning**: replace "Under the other readings" with words that name them; keep the
rest.

W. **stale_lead**: the heading becomes "## When the platform changes"; keep the two changes;
"Before you run the cells below" becomes "Before you read on".

X. **stale_after_and_meaning**: rewrite the text after the two check cells and after Jo's query on
the edited week (now "For change 1, ..." to "Chapter 7 makes such records.") from the facts on the
two comparisons: what each compares, what each found, what neither can say, and Chapter 7.

Y. **close**: the first paragraph: what the experiments showed (who to ask; Thursday wrong by its
stated meaning; a description written from the data could not show it; the requirement met as
written by four lines of code, and by no description that says more than the name; the check
caught the new column, and Jo's meaning caught the edit's effect, but not its cause) and could not
show (since when Thursday is wrong; what reads the two files). The second paragraph: Chapter 4
begins from the two values (facts above); say that no record says they name one person, not
"whether those are one person". Then three reflective questions: the first about a platform the
reader works on; the second asks what a description of a column would have to say for a reader to
learn something its name does not; the third leads to Chapter 4: how a set of records could say
that two names refer to one person.

Z. **reality**: keep, but "`psql`'s `\d` commands show it" becomes "the `\d` family of `psql`
commands shows it".

Write the slots under `## A` to `## Z`, each the exact text to place.
