# Revision brief Q: Chapter 21, Conflicting metadata

Letter Q. Read `rev-common.md` first. Redraft these slots: B, C, D, E, E2, F, F2, H, Z.
The term **precedence** is introduced in slot E2, in bold there and nowhere before. Do not use the
word "role".

## B

- Keep the heading `## Three sources` and the first draft's opening sentence.
- A list of the three sources:
  - The warehouse: its catalogue, read every night at 03:30. Its owner is the account the
    warehouse records as the table's owner, `etl_service` (Chapter 2). Its columns are the table's
    columns.
  - Your records (Chapters 3 and 4), sent when they change. You last changed them on Monday 14 at
    16:40, and they name `j.marsh` as responsible.
  - The team sheet: keep the first draft's bullet, including "Nobody has edited it since 28 August.
    It is imported every night at 04:00".
- The shop's metadata system files each source's statement of who owns the table under one
  attribute, `owner`, and its statement of the columns under `columns`. That is the shop's choice.
- Keep the definition of a claim and its two times, `sent` and `as of`.
- The next cell lists the claims the shop's metadata system holds at 18:00 on Monday 14.

## C

- Keep: "There are five claims."
- Three are about the owner: `etl_service`, `j.marsh` and `data team`. Two are about the columns:
  `day, revenue_pence` from the warehouse, and `day, revenue` from the team sheet.
- The shop keeps each source's latest sending of each attribute, so each night's import replaces
  the one before.
- The team sheet's claims were sent at 04:00 on Monday 14, and are as of 28 August.
- One rule for choosing: the claim sent most recently wins. The next cell shows the value this rule
  chooses for each attribute.

## D

- At 18:00 on Monday 14, the owner is `j.marsh`, from your records, sent at 16:40. The columns are
  `day, revenue`, from the team sheet: its import at 04:00 is newer than the warehouse's read at
  03:30. `daily_sales` has no column `revenue`.
- On the night of Monday 14, the shop's nightly work runs as on every other night: the night's work
  writes `daily_sales` at 02:30:21, the warehouse's catalogue is read at 03:30, and the team sheet
  is imported at 04:00.
- You do not change your records, and nobody edits the team sheet.
- Before you read on, write in the next cell what this rule will show as the owner at 09:00 on
  Tuesday 15.

## E

- At 09:00 on Tuesday 15, the owner is `data team`, from the team sheet. The columns are still
  `day, revenue`.
- The next cell lists the claims held at 09:00 on Tuesday 15, with the time each was sent.

## E2

- The team sheet's claims were sent at 04:00 on Tuesday 15, the warehouse's at 03:30, and your
  records' at 16:40 on Monday 14. The team sheet's import is the most recent claim.
- The rule took the claim sent last. The team sheet's content is the oldest of the three: 28 August.
- Compare this with what you wrote.
- When sources disagree, the rule for which claim counts is called **precedence**.

## F

- Then this heading: `## Other rules`
- The next cell applies another rule to Tuesday's claims: `as of`. The claim whose source's content
  changed most recently wins.
- The owner is `etl_service` and the columns are `day, revenue_pence`, both from the warehouse.
- Keep: "The warehouse's content changes every night, at 02:30:21, when the night's work writes
  `daily_sales`." The warehouse's owner does not change.

## F2

- Change `"as of"` to `"ranked"` in that cell, select it and press **Run below**.
- `ranked` takes, for each attribute, the claim of the source that comes first in an order the shop
  chose. For the owner: your records, then the team sheet, then the warehouse. For the columns: the
  warehouse first.
- The owner is `j.marsh` and the columns are `day, revenue_pence`.
- The order works only while the first source in it has sent a claim. At 12:00 on Monday 14,
  before your records were sent, `ranked` gave the owner `data team`, from the team sheet.
- Change it to `"all"` and press **Run below**. The cell lists every claim the shop holds, with its
  source and its two times: five rows.

## H

- Keep the opening: "Correct" could mean three things, each needing something different.
- Keep the first draft's list of three readings and what each needs, and keep: "On Tuesday at
  09:00, the three give, in that order: `data team`; `j.marsh`; all three owners."
- "Owner" is Chapter 2's word, and the three owners answer different questions: `j.marsh` names a
  person responsible, `data team` a team, and `etl_service` the account the warehouse records.
- The shop holds all three claims. A rule that shows one claim shows one of these meanings. Keeping
  every claim leaves the meaning to whoever reads them.
- The requirement names neither a rule nor a meaning, so none of the outputs above is shown to be
  the correct owner.

## Z

- Keep the heading `## Before Chapter 22`.
- Summary facts, in order: three sources made five claims about `daily_sales`; choosing the claim
  sent most recently let a nightly import of an unchanged sheet replace the owner and keep a column
  the table does not have; choosing by the time a source last changed gave the warehouse's account
  on Tuesday morning, because the table changes every night; an order of sources for each attribute
  gave `j.marsh` and the warehouse's columns, while your records had been sent; keeping every claim
  with its source left the choice to you.
- Keep: "Chapter 22 asks when references from different systems name the same asset."
- Keep the first draft's three questions as a list, and its heading `### How this differs from a
  real platform` with its two bullets.
