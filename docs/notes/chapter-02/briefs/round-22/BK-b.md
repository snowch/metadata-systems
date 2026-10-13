# Brief BK, part B: the what-ifs, the untested rule, the records, and the check

Read `BK-common.md` first; its rules hold for every slot.

## BK6: the what-ifs (the three what-ifs' own paragraphs stay as they are)

BK6.1. The heading, word for word: `### Could have been made, or was made`

BK6.2. The lead, before the first what-if:
1. The query shows how `daily_sales` **could have been** made, not how it **was** made. Keep both
   bold words.
2. Three what-ifs test the difference: keep the words "three small changes to the shop". None of
   them happened in the week you have read.
3. Each cell below runs the week again with one change, and prints Monday morning's records in a
   table. Keep these two sentences word for word: "The column `the week as it ran` holds the
   record for the week you have read." and "The column `with the change` holds the record for the
   week with the change."
4. For each change, ask: does a query over the week's assets still give every row of
   `daily_sales`, and which records show the change?

BK6.3. A collapsible note for the table's last row. Write it as HTML and Markdown exactly in this
shape, with your words in place of the dots:
```
<details><summary>How the last row is found</summary>

...

</details>
```
Inside, one paragraph:
1. The last row comes from a fixed set of simple queries over the week's assets.
2. Each reads one asset, keeps all, completed or cancelled orders, and adds up revenue, quantity
   or rows, per day, customer or product.
3. A query is listed if it gives every row of `daily_sales`, even if it gives one row more.
4. Keep these words word for word: "for example `clean_orders: completed orders, revenue per
   day`, which is the query you ran above".

## BK7: the rule the week never tests

BK7.1. The heading, word for word: `### A rule the week never tests`

BK7.2. Before two cells:
1. A reconstruction can be checked only where the data has something to check.
2. In the shop's design, which no system records, `clean_orders` is made from `orders.jsonl` by
   four rules: keep one row of an order the export wrote twice; drop orders with no customer id;
   keep cancelled orders; drop orders with a quantity of 0 or less.
3. The first cell counts the orders in `orders.jsonl` with a quantity of 0 or less. The second
   lists every setting of the four rules that turns the raw orders into `clean_orders` exactly,
   one setting per row.

BK7.3. After the two cells:
1. The count is 0. Keep the words "No order in the week has a quantity of 0 or less" word for
   word.
2. So the last rule never removes a row. Two settings fit: one with the rule and one without.
3. From the data you cannot tell whether the rule exists. The data can confirm a rule only where
   some row would have triggered it.
4. Your guess for `clean_orders` from Chapter 1 meets the same limit.

## BK8: records made at the time

BK8.1. The heading, word for word: `## Records made at the time`. Then one or two sentences: each
question the investigation could not settle needs its own kind of record, and the platform keeps
none of them. The figure below sets them side by side.

BK8.2. Words for a figure: a table with three columns and three rows. The engine fills in the
numbers in the middle column; write the words around them exactly as they should appear, and keep
the bracketed slots as they are. Give the caption, the three column headings, and the three rows,
each as `question | holds | record`.
- caption: for `daily_sales`, each question beside what the platform holds and the record that
  would answer it.
- column headings: the question; what the platform holds; the record that would answer it.
- row 1: What is `daily_sales`, and whom do I ask? | [columns] columns, [rows] rows, last altered
  [time]; owner `[owner]`, an account | a description of the asset: what it means, who is
  responsible for it.
- row 2: What is it made from? | nothing; a query over `clean_orders` fits, and with the analyst's
  copy, one over the copy fits too | a record of what was made from what (Chapter 6 calls this
  lineage).
- row 3: What did each night's job do? | nothing; after a failed night, each record looks normal |
  a record of each time a job ran: its code version, inputs, output, time, and whether it
  succeeded (Chapter 7).

BK8.3. After the figure: keep this paragraph word for word, it is already approved: "A record of
what the job read would have answered the analyst's copy. A record of which version of the job's
code ran each night would have answered the edit. A record of whether each night's write
succeeded would have answered the failed night."

## BK9: the check

BK9.1. The heading, word for word: `## Check: evidence of what a job read`

BK9.2. The scenario, before the answers:
1. A data engineer wants to know which inputs one particular run of a job actually read. ("run" is
   a noun here, and that is allowed in this slot only.)
2. They have three pieces of evidence. Which is the strongest evidence of what that run read?
3. Open an answer to see whether it holds; you can open the others after.

BK9.3. Three answers. Write each exactly in this shape, one after another, with the summary line
word for word as given and your feedback in place of the dots:
```
<details class="ms-choice"><summary>A. The current table schema and its last-modified timestamp.</summary>

...

</details>
```
The three summary lines, word for word:
- A. The current table schema and its last-modified timestamp.
- B. A SQL query that reproduces the dashboard's current totals.
- C. A recorded job-run event identifying the run ID, code version, input tables, output table, timestamp and status.

Feedback for A (one paragraph, then "Try another answer."):
1. Not the strongest.
2. A schema and a last-modified time describe the table as it is now.
3. The time says when the table last changed, not what the job that wrote it read.
4. With the analyst's copy, every one of these records stayed the same, whichever file the job
   read.

Feedback for B (one paragraph, then "Try another answer."):
1. Not the strongest.
2. A query that matches supports a hypothesis about how the totals could be produced.
3. Another source can fit as well: with the analyst's copy, the same query over
   `clean_orders_copy.csv` gives the same rows.
4. It matches today's totals, not what a past run did: after the edit to the job, no simple query
   fitted, and nothing said why.

Feedback for C (two paragraphs, then the takeaway):
1. The strongest.
2. It was recorded when the run happened, and it names that run, its code version, the tables it
   read and wrote, when, and whether it succeeded.
3. It is evidence of what the run's instrumentation captured. It is only as complete as that
   instrumentation: a read the instrumentation did not capture would be missing from the record.
   So it shows which inputs were recorded, not that the job read nothing else.
4. Then the takeaway, as its own paragraph, word for word, in bold: **Current metadata describes
   an asset. A matching reconstruction supports a hypothesis. Recorded execution events provide
   evidence of a particular run.**
