# Brief W: Chapter 17, "Root-cause analysis"

Read `docs/notes/chapter-14/briefs/common.md` first, and `docs/style.md`. Their rules hold here, and
the terms of Chapters 14 to 16 (*data quality*, *assertion*, *provenance*, *impact analysis*) may be
used.

Term this chapter introduces, in bold in slot E and nowhere before it: **root cause**.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Follow a wrong figure on the dashboard back to the step where it went wrong.
- Find two causes that each explain a figure, and tell them apart.
- Find where the shop's records end.
- Question the requirement "Find the cause of the wrong figure."

### Slot B: under the heading `## "Thursday's revenue looks wrong."`

- Chapter 2 began with the head of the shop's message: "Thursday's revenue looks wrong." The dashboard
  shows £51.50 for Thursday 10.
- The shop now records each run and its code as it was that night (Chapter 7), and what each run of
  `build_clean_orders` counted (Chapter 14). Object storage keeps every version of each file, with the
  time it was written.
- Before you read on, write in the next cell where you would look first, and what would show you that
  you had found the cause.

### Slot BB: the text inside that cell (between triple quotes)

One question, then `........` on its own line: where would you look first, and what would show you had
found the cause? At most about 60 characters a line. Plain text.

### Slot C: under the heading `## Back from Thursday's figure`

- The next cell starts at the dashboard's value for Thursday and steps back: `daily_sales`, then
  `clean_orders`, then the version of `orders.jsonl` that was current when `build_clean_orders`
  started.
- At each step it measures Thursday's revenue the way `build_daily_sales` defines it: price times
  quantity over the day's completed orders, each order once.
- For each step it lists whether the total differs from the step's input, and whether the code of the
  program that made the step changed since the night before.

### Slot D: after that cell

- The dashboard, `daily_sales` and `clean_orders` each hold 5150 pence for Thursday. The version of
  `orders.jsonl` written at 01:00 on Friday 11 holds 20550.
- The difference first appears in `clean_orders`, made by `run-014`, `build_clean_orders`, early on
  Friday 11. Its code had not changed since the night before.
- The last row is the checkout. The shop records nothing about what the export read, so the steps end
  at `orders.jsonl`.

### Slot E: under the heading `## Two causes`

- `run-014` counted 3 rows with no customer id in the file it read (Chapter 14): Thursday's three
  orders.
- Two things together made Thursday's figure low: the checkout sent three orders with no customer id;
  and `build_clean_orders` drops orders with no customer id, by a rule that was in its code all week.
  Change either, and the figure would have counted the three orders.
- A cause that, if removed, would stop a fault happening again is a **root cause**. Here two causes
  each meet that.
- Of the two causes, the shop's records show that the data changed and the code did not. The checkout
  is outside them: no record shows why it sent orders with no customer id.

### Slot F: under the heading `## A Saturday that is too high`

- The next week has Chapter 2's change `refunds`: from Saturday's row on, `build_daily_sales` keeps
  every order that is not refunded, where it kept completed orders. The dashboard shows £215.49 for
  Saturday 12.
- The next cell searches back from Saturday's figure. Before you read on, decide at which step you
  expect the difference to appear, and whether a code change will show.

### Slot G: after that cell

- The difference first appears in `daily_sales`: 21549 pence, where `clean_orders` holds 19149 for
  Saturday. `daily_sales` was made by `run-023`, `build_daily_sales`, early on Sunday 13, and its code
  had changed since the night before.
- Two explanations fit: the change to the code, or Saturday's cancelled order 7037, 2 sets of brake
  pads, 2400 pence, the difference.
- Tuesday 8 also had a cancelled order, 7009. Change `day = "2026-09-12"` to `day = "2026-09-08"`,
  select the cell and press **Run below**.

### Slot H: after slot G, as its own paragraph group

- For Tuesday, no step differs: 16225 pence at every step, and no code had changed.
- A cancelled order alone did not change the figure. With the code as it was on Tuesday's night, the
  cancelled order was left out. The change to the code explains Saturday's figure.
- The next cell prints the lines of `build_daily_sales`'s code that changed for Sunday's night.

### Slot I: after that cell

- `status = 'completed'` became `status <> 'refunded'`.
- The shop's records show what changed and the first run that used it. They do not show why it was
  changed.

### Slot J: under the heading `## "Find the cause of the wrong figure."`

- The head of the shop's requirement: "Find the cause of the wrong figure."
- Before you read on, write in the next cell what you would give as the cause of Thursday's figure.

### Slot JJ: the text inside that cell (between triple quotes)

One question, then `........` on its own line: what is the cause of Thursday's figure? At most about
60 characters a line. Plain text.

### Slot READINGS: after that cell

- "The cause" could mean three things, each needing something different:
  - where the data first went wrong: each step measured the same way, and the versions of what each
    run read;
  - the change that did it: each run's code, and what each run counted;
  - the decision behind that change: a record of who decided it and why.
- For Thursday:
  - where: two answers fit. `orders.jsonl` already held the three orders with no customer id; the
    total first changes in `clean_orders`.
  - the change: none in the shop's records. The code did not change; the checkout's change is outside
    them.
  - the decision: none recorded.
- For Saturday, with `refunds`:
  - where: `daily_sales`, made by `run-023`.
  - the change: the edit to `build_daily_sales`, shown by the code each run recorded.
  - the decision: none recorded.
- The requirement does not say which of the three it means.
- Compare these with what you wrote.

Write slot READINGS as one lead sentence, a Markdown list of the three readings, then a lead line
and a Markdown list for each day, then two sentences.

### Slot K: under the heading `## Before Chapter 18`

- From Thursday's figure, the steps back found where the difference first appeared, in a run whose
  code had not changed, and ended at the checkout, outside the shop's records. Two causes explained
  the figure. From Saturday's, they found a code change; a day with the same kind of order and no
  change ruled out the other explanation.
- The records could not show why either the checkout or the code changed.
- Part IV used the shop's record of every run. Every run's events arrived, each once and in
  order.
- Chapter 18, the first chapter of Part V, asks what the shop's records hold when an event never
  arrives.
- Then three reflective questions, as a Markdown list:
  - where your platform's records end, upstream;
  - how you would tell a change to the data from a change to the code;
  - where the reasons for a change to your code are kept, if anywhere.

### Slot L: under the heading `### How this differs from a real platform`

- The shop's faults are invented for the course.
- The search measures one thing, a day's revenue, the same way at every step. A fault that does not
  change that total, such as an order counted against the wrong day, would not show.
- It reads files in the version each run read and tables as they are now (Chapter 15).
- The shop's repository keeps each program's code. It records no reason for a change.

Write slot L as a Markdown list.

## Slots

Write the file `docs/notes/chapter-17/drafts/W.md` with the slots under `## A`, `## B`, `## BB`,
`## C`, `## D`, `## E`, `## F`, `## G`, `## H`, `## I`, `## J`, `## JJ`, `## READINGS`, `## K` and
`## L`, each the exact text to place, and nothing else in the file. Each slot that has a heading
starts with that heading.
