# Brief U: Chapter 15, "Provenance"

Read `docs/notes/chapter-14/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
Chapter 14's terms (*data quality*, *assertion*) may be used.

Term this chapter introduces, in bold in slot C and nowhere before it: **provenance**. Do not write:
impact analysis, root cause.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Follow Thursday's figure on the dashboard back to the lines of the file it came from.
- Find what a record of a figure's sources leaves out.
- Find why Sunday's figure no longer adds up from the shop's tables.
- Question the requirement "Show where Thursday's figure came from."

### Slot B: under the heading `## Thursday's £51.50`

- Chapter 2 began with the head of the shop's message: "Thursday's revenue looks wrong." The
  dashboard shows £51.50 for Thursday 10.
- Before you read on, write in the next cell which orders you expect £51.50 to be made of.

### Slot BB: the text inside that cell (between triple quotes)

One question, then `........` on its own line: which orders is Thursday's £51.50 made of? At most
about 60 characters a line. Plain text.

### Slot BC: before the cell that follows the figure back, after the text cell

- The next cell follows Thursday's figure back, one step at a time, from the dashboard to the file.
  At each step it lists the asset, the run that made it, the rows it found, and their total in pence.

### Slot C: after that cell

- Four steps:
  1. the dashboard's value for Thursday, £51.50, drawn by `run-028`, `refresh_dashboard`, early on
     Monday 14;
  2. the row of `daily_sales` for Thursday, written by `run-015`, `build_daily_sales`, early on
     Friday 11;
  3. the rows of `clean_orders` for orders 7020, 7022, 7024 and 7026, written by `run-014`,
     `build_clean_orders`, early on Friday 11;
  4. lines 21, 23, 25 and 27 of `orders.jsonl`, in the version the export wrote at 01:00 on Friday 11,
     the last before `run-014` started.
- Each step adds up to 5150 pence.
- The record of where a piece of data came from (the rows it was made from, the programs and runs
  that made it, and the inputs as they were when each run read them) is its **provenance**.
- The figure is the sum of four orders. No one of them is its source: change any of the four and the
  figure changes.
- `orders.jsonl` is read in the version that was current when `run-014` started: object storage
  keeps every version of a file, with the time it was written. `clean_orders` is read as it is now:
  the warehouse keeps no earlier state of a table.

Write the four steps as a numbered Markdown list after one lead sentence.

### Slot D: under the heading `## What the record leaves out`

- Thursday's figure is low because three orders were left out (Chapter 2). The four steps list only
  the rows the figure was made from.
- The next cell follows the figure back again with `dropped=False`. Change it to `dropped=True`.
  Before you press **Run below**, decide whether the steps will then list orders 7021, 7023 and 7025.
  Then select the cell and press **Run below**.

### Slot E: after that cell

- With `dropped=True`, a last row lists lines 22, 24 and 26 of the same version of `orders.jsonl`:
  orders 7021, 7023 and 7025, each with `customer_id IS NOT NULL is false`, together 15400 pence.
  `run-014` read them and left them out.
- They are found by applying `build_clean_orders`'s conditions again to each line of that version.
- A record of what a figure was made from lists what was used. Why Thursday's figure is low is in
  what was not used, and that needs the rows each run read and the condition that left each out.

### Slot F: under the heading `## Sunday's figure`

- The next week has the change `corrected`. From Saturday's row on, `build_daily_sales` takes away
  what was returned, through the function `returned_quantity`, which reads the table `returns`
  (Chapter 10).
- On Sunday 13 at 18:10 the returns desk records `r-205`: 2 rolls of bar tape back from order 7044.
  Early on Monday 14 at 02:30, `build_daily_sales` writes Sunday's row. At 08:40 on Monday the desk
  corrects `r-205` to 1 roll.
- Before you read on, write in the next cell whether you expect Sunday's figure to add up from the
  shop's tables as they are at 09:00 on Monday, and why.

### Slot FF: the text inside that cell (between triple quotes)

One question, then `........` on its own line: does Sunday's figure add up from the tables as they are
now? At most about 60 characters a line. Plain text.

### Slot G: after the cell that follows Sunday's figure back

- The dashboard and `daily_sales` show 6925 pence for Sunday.
- The five Sunday orders in `clean_orders`, 7043 to 7047, add up to 9775 pence. `returns`, as it is
  now, holds `r-205` with 1 roll of order 7044: 1425 pence less. Together, 8350 pence.
- 8350 is not 6925. Sunday's figure does not add up from the tables as they are now.
- The next cell lists every version of `r-205`'s object.

### Slot H: after that cell

- Two versions: at 18:10 on Sunday, with quantity 2; at 08:40 on Monday, with quantity 1.
- `run-034`, the run of `build_daily_sales` that wrote Sunday's row, started at 02:30 on Monday,
  between the two.
- In the next cell, change `as_read=False` to `as_read=True`, select the cell and press **Run below**.
  With it, `returns` is rebuilt as it was when `run-034` started, from the versions of the objects
  that the runs of `record_return` read.

### Slot I: after that cell

- `returns`, as it was at 02:30:00, held `r-205` with 2 rolls, from the first version, read by
  `run-031`: 2850 pence less. 9775 less 2850 is 6925, Sunday's figure.
- Each version of the object was a different input. `run-034` used what the first held.
- The warehouse keeps no earlier state of `returns`. It could be rebuilt only because each run of
  `record_return` recorded which version it read, and object storage kept that version.

### Slot J: under the heading `## "Show where Thursday's figure came from."`

- The head of the shop's requirement: "Show where Thursday's figure came from."
- Before you read on, write in the next cell what you would show.

### Slot JJ: the text inside that cell (between triple quotes)

One question, then `........` on its own line: what would you show? At most about 60 characters a
line. Plain text.

### Slot READINGS: after that cell

- "Where it came from" could mean four things, each needing something different:
  - the rows: which rows it was made from, found by following it back row by row;
  - the program: which programs made it, from lineage;
  - the run: which runs made it, from the record of each run;
  - the rows as they were when each run read them: a version of each input, kept and recorded.

Write slot READINGS as one lead sentence and a Markdown list.

### Slot K: after slot READINGS, as its own paragraph group

- For Thursday, the first three were met. The fourth was met for the file, read in the version
  current when `run-014` started; the tables were read as they are now, and every step still added up.
- For Sunday, with the correction, the first three were met. The fourth was not met by `returns` as
  it is now, and was met only by rebuilding the table from the object versions the runs recorded.
- A record of what was used does not show what was left out, which was the question about Thursday.
- The requirement does not say which reading it means.
- Compare these with what you wrote.

### Slot L: under the heading `## Before Chapter 16`

- Thursday's £51.50 was followed back through four steps to four lines of one version of
  `orders.jsonl`. The orders that made it low were not among them; they showed only once the rows each
  run read and left out were listed.
- Sunday's figure did not add up from the tables as they were at 09:00 on Monday. It added up from
  `returns` as it was when the run started, rebuilt from object versions.
- The record could not show what was made from a return after it changed, or what a change to a
  column would affect.
- Chapter 16 asks, before a change is made, what it would affect.
- Then three reflective questions, as a Markdown list:
  - which of your platform's tables could be read again as a run read it;
  - how you would find the rows a program read and left out;
  - which of your figures were made from inputs that have changed since.

### Slot M: under the heading `### How this differs from a real platform`

- The returns, the correction and the runs are invented for the course.
- The W3C's PROV data model (a W3C Recommendation of 30 April 2013) describes provenance with
  entities (things), activities (which happen over a period of time and use or generate entities) and
  agents (which bear responsibility). Its relations include an activity using an entity, an entity
  generated by an activity, and one entity derived from another.
- In PROV an entity has fixed aspects, so the two versions of `r-205`'s object would be two entities.
- The shop's way of following a figure back is its own: it applies the programs' conditions again to
  the rows.
- Some table formats keep a table's earlier states as snapshots (Chapter 2). With them, a table could
  be read as a run read it.

Write slot M as a Markdown list.

## Slots

Write the file `docs/notes/chapter-15/drafts/U.md` with the slots under `## A`, `## B`, `## BB`,
`## BC`, `## C`, `## D`, `## E`, `## F`, `## FF`, `## G`, `## H`, `## I`, `## J`, `## JJ`,
`## READINGS`, `## K`, `## L` and `## M`, each the exact text to place, and nothing else in the file.
Each slot that has a heading starts with that heading.
