# Brief UB: Chapter 15, after its review

Read `docs/notes/chapter-14/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
brief UA's terms. A review found: step 3 credited to a run that did not write the table as it is now;
a rebuilt table described as observed; a file's version said to be recorded when it is chosen by
time; a definition of provenance that already held the four readings; an objective that gave away a
result; a near-trivial prediction; repeats. The trace now lists the table as it is now with the run
that last wrote it, gives full timestamps, and lists each left-out line on its own row. These slots
replace paragraphs.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Follow Thursday's total on the dashboard back to the lines of the file it came from.
- Find what a record of a total's sources leaves out.
- Check whether Sunday's total adds up from the shop's tables, and find what it adds up from.
- Question the requirement "Show where Thursday's total came from."

### Slot C: after the cell that follows Thursday's total back

- Thursday's total goes back through four steps:
  1. the dashboard's value for Thursday, £51.50, drawn by `run-028`, `refresh_dashboard`, early on
     Monday 14;
  2. the row of `daily_sales` for Thursday, written by `run-015`, `build_daily_sales`, early on
     Friday 11;
  3. the rows of `clean_orders` for orders 7020, 7022, 7024 and 7026, as the table holds them now. The
     table was last written by `run-026` early on Monday 14. `run-015` read it after `run-014` wrote
     it early on Friday 11; the shop's warehouse keeps no earlier state of a table, so the rows
     `run-015` read are not kept. The rows now add up to the same total;
  4. lines 21, 23, 25 and 27 of `orders.jsonl`, in the version the export wrote at 01:00:41 on
     Friday 11. The shop's object storage keeps every version of a file, with the time it was
     written; this one is the last before `run-014` started. `run-014` did not record which version
     it read: the time chooses it.
- Each step adds up to 5150 pence.
- Information about where a piece of data came from and how it was made is its **provenance**.
- The total is made from four orders together; none of them alone is where it came from.

Write the four steps as a numbered Markdown list after one lead sentence, then the three sentences.

### Slot D: under the heading `## What the record leaves out`

- Thursday's total is low because three orders were left out (Chapter 2). The four steps list only the
  rows the total was made from.
- The next cell follows the total back again with `dropped=False`. Change it to `dropped=True`.
  Before you press **Run below**, decide what reason the steps will give for each of orders 7021,
  7023 and 7025. Then select the cell and press **Run below**.

### Slot E: after that cell

- With `dropped=True`, three more rows list lines 22, 24 and 26 of the same version of
  `orders.jsonl`: orders 7021, 7023 and 7025, each with `customer_id IS NOT NULL is false`, together
  15400 pence. `run-014` read them and left them out.
- They are found by applying `build_clean_orders`'s conditions again to each line of that version.
- A record of what a total was made from lists what was used. Why Thursday's total is low is in what
  was not used, and that needs the rows each run read and the condition that left each out.

### Slot F: under the heading `## Sunday's total`

- The next week has the change `corrected`. From Saturday's row on, `build_daily_sales` takes away what
  was returned, through the SQL function `returned_quantity`, which reads the table `returns`
  (Chapter 10).
- On Sunday 13 at 18:10 the returns desk records `r-205`: 2 rolls of bar tape back from order 7044.
  Early on Monday 14 at 02:30, `build_daily_sales` writes Sunday's row. At 08:40 on Monday the desk
  corrects `r-205` to 1 roll.
- Before you read on, write in the next cell whether you expect Sunday's total to add up from the
  shop's tables as they are at 09:00 on Monday, and why.

### Slot G: after the cell that follows Sunday's total back

- The dashboard and `daily_sales` show 6925 pence for Sunday.
- The five Sunday orders in `clean_orders`, 7043 to 7047, add up to 9775 pence. `returns`, as it is
  now, holds `r-205` with 1 roll of order 7044, written by `run-036`, `record_return`, after the
  correction: 1425 pence less. Together, 8350 pence.
- 8350 is not 6925. Sunday's total does not add up from the tables as they are now.
- The next cell lists every version of `r-205`'s object.

### Slot I: after the cell with `as_read`

- The rebuilt `returns`, as at 02:30:00 on Monday, holds `r-205` with 2 rolls, from the first
  version, which `run-031` read: 2850 pence less. 9775 less 2850 is 6925, Sunday's total.
- The shop does not record that `run-034` read `returns`: the function's read is in no record
  (Chapter 10). That the rebuilt table gives 6925 is the evidence that `run-034` used what the first
  version held.
- The shop's warehouse keeps no earlier state of `returns`. It could be rebuilt only because each run
  of `record_return` recorded which version it read, and the shop's object storage kept that version.

### Slot K: after slot READINGS, as its own paragraph group

- For Thursday, the first three were met. For the fourth: the file's version was kept by the shop's
  object storage and chosen by the time `run-014` started, but `run-014` did not record it; the
  tables were read as they are now, and every step still added up.
- For Sunday, with the correction, the first three were met. The fourth was not met by `returns` as it
  is now. It was met only by rebuilding the table from the object versions the runs of
  `record_return` recorded.
- None of the four readings asks for the rows each run read and left out.
- The requirement does not say which reading it means.
- Compare these with what you wrote.

### Slot M: under the heading `### How this differs from a real platform`

- The returns, the correction and the runs are invented for the course.
- The W3C's PROV data model (a W3C Recommendation of 30 April 2013) describes provenance with entities
  (things), activities (which happen over a period of time and use or generate entities) and agents
  (which bear responsibility). Its relations include an activity using an entity, an entity generated
  by an activity, and one entity derived from another.
- PROV calls an entity a thing "with some fixed aspects" (PROV-DM's words). By that, the two versions
  of `r-205`'s object would be two entities.
- The shop's way of following a total back is its own: it applies the programs' conditions again to
  the rows.
- Some table formats keep a table's earlier states as snapshots (Chapter 2). With them, a table could
  be read as a run read it.

Write slot M as a Markdown list.

## Slots

Write the file `docs/notes/chapter-15/drafts/UB.md` with the slots under `## A`, `## C`, `## D`,
`## E`, `## F`, `## G`, `## I`, `## K` and `## M`, each the exact text to place, and nothing else in
the file. Each slot that has a heading starts with that heading.
