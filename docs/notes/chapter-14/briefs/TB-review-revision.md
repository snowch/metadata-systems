# Brief TB: Chapter 14, after its review

Read `docs/notes/chapter-14/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
brief TA's terms. A review found: a cross-reference to the wrong chapter; an objective that gave away
a result; "rule" meaning both the developer's test and the job's filter; a definition of assertion
too narrow; the reader asked what the requirement means only after the page had supplied a reading;
a section with no question in front of it; a heading that implied the shop's events carry the
counts; a repeated sentence; a closing that left out the requirement's verdicts. These slots replace
paragraphs. Keep "rule" for the job's filter only; the developer's check is a "test" until it is
named an assertion.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Read what each run of `build_clean_orders` counted in the file it read.
- Test one expectation about the orders on every run, against the table and against the file.
- Set the rows each run read against the rows it wrote.
- Question the requirement "No order without a customer."

### Slot C: after the cell that lists the counts (replaces the old slot C)

- The file grows each night, because each export holds every order so far: 6 rows on Tuesday 8, 48
  on Monday 14.
- From Thursday 10, `order_id twice` is 1: one order appears twice in the file, and stays twice.
- From Friday 11, `no customer_id` is 3: Thursday's three orders with no customer id (Chapter 2). They
  stay in every later file.
- `quantity 0 or less` is 0 on every run: no order in the week has one (Chapter 2).
- Whether data is fit for the use made of it is its **data quality**. These counts are observations
  (Chapter 13) of the data each run read and wrote, and they measure its data quality.

### Slot D: under the heading `## "No order without a customer."`

- The head of the shop's requirement: "No order without a customer."
- Before you read on, write in the next cell what you take it to mean: where must there be no order
  without a customer, and what should happen to one?

### Slot D2: under the heading `## A test on every run`

- The shop's developer writes the requirement as a test on every run of `build_clean_orders`: in
  `clean_orders`, `no customer_id` must be at most 0.
- A stated expectation about data, with a record of whether it held in each run, is an
  **assertion**.
- Before you read on, write in the next cell which runs you expect to fail the assertion, and why.

### Slot E: after the cell that tests the assertion

- It passed on all 7 runs.
- `build_clean_orders` drops every order with no customer id before it writes the table: its rule
  `customer_id IS NOT NULL` (Chapter 6, where you read its code). The assertion tests the table after
  that rule, so it finds no such order on any night. While the rule stays, this assertion cannot fail.
- Change `dataset = "clean_orders"` to `dataset = "orders.jsonl"`, select the cell and press
  **Run below**.

### Slot F: after slot E, as its own paragraph group

- On `orders.jsonl`, 4 runs fail: Friday 11, Saturday 12, Sunday 13 and Monday 14, each with a count of
  3. Tuesday 8 to Thursday 10 pass: their files hold no order of Thursday's.

### Slot G: under the heading `## Rows read and rows written`

- Could a run's own counts show that it left rows out, whatever left them out?
- The next cell lists, for each run, the rows it read and wrote, the rows that repeat an order, and the
  rows it left out beyond those. Another assertion: `left out` is 0.

### Slot I: under the heading `## Three readings`

- "No order without a customer" could mean three things, each needing a different measurement:
  - in the file the checkout sends: `no customer_id` in `orders.jsonl`, on every run;
  - in `clean_orders`: `no customer_id` in the table, on every run;
  - on the dashboard: every completed order the shop took is counted in a day's revenue. This needs
    the file's orders set against the dashboard's totals. No run records it, so the next cell leaves
    its `runs failed` empty.
- The next cell tests each reading.

Write slot I as one lead sentence, a Markdown list of the three readings, then one sentence.

### Slot K: after the cell that tests the readings

- In the file: not met; 4 runs failed.
- In `clean_orders`: met on every run, because the rule removes the orders before the table is
  written.
- On the dashboard: not met. Thursday's total leaves out 3 completed orders, worth 15400 pence
  (Chapter 2).
- Compare these with what you wrote at the start.
- The requirement does not say which reading it means. Nor does it say what should happen to an order
  without a customer: dropped, kept without a customer, or the night's work stopped.

Write slot K as a Markdown list of the three verdicts, then a short paragraph.

### Slot L: under the heading `## The counts as OpenLineage facets`

- OpenLineage defines two facets for this: `dataQualityMetrics`, counts for a dataset and for each of
  its columns; and `dataQualityAssertions`, each assertion and whether it succeeded.
- The shop's events do not carry them. The next cell builds them for the input `orders.jsonl` of
  `run-014`, the run on Friday 11, as the shop's producer would send it.

### Slot M: after that cell

- `rowCount` is 27. For the column `customer_id`, `nullCount` is 3: the rows with no customer id. For
  `order_id`, `distinctCount` is 26: the 27 rows less the 1 repeat. No field holds
  `quantity 0 or less`.
- The assertion is `not_null` on `customer_id`, with `success` false, `expected` 0 and `actual` 3.
- Both facets go with the dataset the run read.

### Slot N: under the heading `## Before Chapter 15`

- Each run of `build_clean_orders` counted four things in the file it read and the table it wrote. The
  assertion on `clean_orders` passed on every run, because the rule had removed the orders it was
  meant to find. On the file, it failed from Friday 11. Comparing the rows each run read with the rows
  it wrote showed 3 rows left out on every run from Friday 11.
- "No order without a customer" was met in `clean_orders`, not in the file and not on the dashboard,
  and the requirement does not say which it means.
- The counts could not show which orders were left out, or where a total on the dashboard came from.
- Chapter 15 follows one total on the dashboard back to the rows it was made from.
- Then the same three reflective questions as now, as a Markdown list (keep their wording):
  - Where do your platform's checks run: on what a program reads, or on what it writes?
  - Which of your checks could not fail, because a program removes the rows first?
  - What does your platform do when a check fails: stop the work, or warn?

## Slots

Write the file `docs/notes/chapter-14/drafts/TB.md` with the slots under `## A`, `## C`, `## D`,
`## D2`, `## E`, `## F`, `## G`, `## I`, `## K`, `## L`, `## M` and `## N`, each the exact text to
place, and nothing else in the file. Each slot that has a heading starts with that heading.
