# Chapter 17: Root-cause analysis

A working note. Written on 12 October 2026 with Chapters 14, 15 and 16, as a notebook
(`notebook/chapter_17.py`). It ends Part IV.

## What the chapter does

The head of the shop's first message returns: "Thursday's revenue looks wrong." The reader:

- writes where they would look first, and what would show they had found the cause;
- searches back from Thursday's total, each step measured the way `build_daily_sales` defines
  revenue, and finds the difference first in `clean_orders`, made by a run whose code had not
  changed; the search ends at the checkout, outside the records;
- reads two causes, the checkout's orders with no customer id and the rule that drops them, and meets
  **root cause**, which each meets;
- in the week with `refunds`, searches back from Saturday's £215.49, finds the difference at
  `daily_sales` with a code change, and two explanations; changes the day to Tuesday 8, which had a
  cancelled order too, presses **Run below**, and finds no difference: the code change explains it;
- reads the changed line of code, and that no record shows why;
- questions "Find the cause of the wrong total." against three readings.

## What was built for it

- `notebook/shop/cause.py`: `search` and `code_change`.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** where the search steps.
- **Why now:** every chapter opens with the map.

### `thursday-search`

- **Role:** experiment
- **Objective:** the reader learns to find where a total first differs from its input, and that the
  shop's records end before the cause outside them.
- **Known before:** Chapters 2, 14 and 15 on Thursday.
- **Driving question:** where would you look first, and what would show you had found the cause?
- **The action:** write the plan; read the search.
- **Why the action:** the search is the plan, step by step, with each step's evidence.
- **Evidence:** 5150, 5150, 5150, 20550; no code change; the checkout unrecorded.
- **Consequence:** "where it went wrong" and "why" are different questions.
- **Predictable:** yes.
- **Gives nothing away:** the prompt asks for a method.
- **Not knowing:** not the right answer.
- **Next question:** which of two causes is the cause?
- **An experiment:** commit, run, compare.

### `saturday-search`

- **Role:** experiment
- **Objective:** the reader learns to tell two explanations apart by a case that has one and not the
  other: a day with a cancelled order and no code change.
- **Known before:** Chapter 2's `refunds` change.
- **Driving question:** at which step will the difference appear, and will a code change show?
- **The action:** decide; read; change the day to Tuesday 8, press **Run below**.
- **Why the action:** Tuesday holds the cancelled-order explanation without the code change.
- **Evidence:** 21549 against 19149 at `run-023`, code changed; Tuesday 16225 at every step.
- **Consequence:** a cause is shown by a comparison, not by the evidence that fits it.
- **Predictable:** yes, from Chapter 2.
- **Gives nothing away:** the two explanations are given only after the result.
- **Not knowing:** a fair first answer.
- **Next question:** what does the record say about why the code changed?
- **An experiment:** decide, run, change, run again.

### `code-change`

- **Role:** inspect
- **Serves:** the changed line, and the absence of a reason.
- **Why now:** it closes the search.

## Requirements

The chapter questions "Find the cause of the wrong total.", the plan's candidate with "figure" now
"total".

1. **What it says:** find the cause.
2. **What it might mean:** where the data first went wrong; the change that did it; the decision
   behind that change.
3. **What each needs:** each step measured one way, with the versions each run read; each run's code
   and counts; a record of who decided and why.
4. **What the shop records:** runs, their code, the counts of Chapter 14, object versions; no reason
   for a change, nothing from the checkout.
5. **Whether it is met:** for Thursday, the first has two answers, the second none in the records,
   the third none; for Saturday, the first and second are met, the third not. The requirement does
   not say which it means.

## Originality

The obvious examples are the "five whys" told over a factory fault, and an observability product's
incident timeline of a broken table. This chapter searches back through the shop's own steps by the
shop's own measure, separates a data cause from a code cause with a day of the shop's own week that
has one and not the other, and stops where the shop's records stop.

## What the prose process caught

Brief WA, draft `drafts/W.md`. The total of the file's version lacked its unit; "pence" added. My
brief's example of a fault the search misses, an order counted against the wrong day, would change
the day's total; it is now one counted against the wrong customer. "The shop reads files…" named the
wrong subject; it is the search. Two nights named by a day became the date the work ran on.
"Figure" for a number became "total".

## The review

To be done with the review of Part IV.

## Measured

Locally, 12 October 2026 (`docs/notes/notebook-prototype.md`, "Chapters 14 to 17"): from Chapter 16's link, 11 files, 0.32 MB, in a new tab; Run all 7.9 to 8.9 s; peak memory 392 to 397 MB alone, 605 MB with Chapter 16 open; no error output. Live: to be measured once published.

## Known gaps

- The search measures one total; a fault that does not change it does not show.
