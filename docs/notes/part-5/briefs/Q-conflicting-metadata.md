# Brief Q: Chapter 21, "Conflicting metadata"

Read `docs/notes/part-5/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms this chapter introduces, in bold, and nowhere before the slot named: **precedence** (slot E).
Terms already introduced, which you may use: delivery, deduplication, idempotent, event time,
arrival time. Do not write: alias, entity resolution, index, partition, retention, compaction.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Read what three sources claim about one table, and when each claim was sent.
- Find why "the newest claim wins" shows a claim nobody has changed for weeks.
- Try three other rules for choosing, and keep where each claim came from.
- Question the requirement "Show the correct owner."

### Slot B: under the heading `## Three sources`

- The shop's metadata system takes what other systems hold about `daily_sales` from three sources.
  Write them as a Markdown list:
  - the warehouse: its catalogue, read every night at 03:30. Its owner is the account that created the
    table, `etl_service` (Chapter 2), and its columns are the table's;
  - your records (Chapters 3 and 4), sent when they change. You last changed them on Monday 14 at
    16:40; they name `j.marsh` as responsible;
  - the team sheet: a spreadsheet of owners and columns that the engineer who built the platform wrote
    before the shop opened. Nobody has edited it since 28 August. It is imported every night at
    04:00, and each import sends every row again.
- Each source's statement about one attribute is a claim. Each claim keeps two times: when it was sent
  (`sent`), and when its source's content last changed (`as of`).
- The next cell lists the claims the shop's metadata system holds at 18:00 on Monday 14.

### Slot C: after that cell

- Five claims: three about the owner (`etl_service`, `j.marsh`, `data team`) and two about the columns
  (`day, revenue_pence` from the warehouse; `day, revenue` from the team sheet).
- The team sheet's claims were sent at 04:00 on Monday 14, and are as of 28 August.
- One rule for choosing: the claim sent most recently wins. The next cell shows its choice.

### Slot D: after that cell

- At 18:00 on Monday 14, the owner is `j.marsh`, from your records, sent at 16:40. The columns are `day,
  revenue`, from the team sheet: its import at 04:00 is newer than the warehouse's read at 03:30.
  `daily_sales` has no column `revenue`.
- Overnight, the warehouse's catalogue is read again at 03:30 and the team sheet imported again at
  04:00. Nobody changes anything.
- Before you read on, write in the next cell what this rule will show as the owner at 09:00 on Tuesday
  15.

### Slot DD: the text inside that cell

One question, then `........` on its own line: what owner will the rule show on Tuesday at 09:00?
Plain text.

### Slot E: after that cell

- At 09:00 on Tuesday 15, the owner is `data team`, from the team sheet. Its import at 04:00 is now the
  most recent claim. The columns are still `day, revenue`.
- The rule took the claim sent last. The team sheet's content is the oldest of the three: 28 August.
- Compare this with what you wrote.
- The rule that decides which claim wins when sources disagree is **precedence**.

### Slot F: under the heading `## Other rules`

- Change `"newest"` to `"as of"` in the cell, select it and press **Run below**. The claim whose
  source changed most recently wins: the owner is `etl_service` and the columns `day, revenue_pence`,
  both from the warehouse. The warehouse's content changes every night, at 02:30:21 when the night's
  work writes `daily_sales`; its owner does not.
- Change it to `"ranked"` and press **Run below**. Each attribute has its own order of sources: for
  the owner, your records first, then the team sheet, then the warehouse; for the columns, the
  warehouse first. The owner is `j.marsh` and the columns `day, revenue_pence`.
- Change it to `"all"` and press **Run below**. Every claim is kept, with its source and its two
  times: five rows.
- `ranked` is the shop's own choice of order. It holds only while the sources keep to the roles it
  gives them.

### Slot RH: the heading of the requirement's section

Exactly `## The correct owner`. A box holding the requirement comes after this heading.

### Slot G: after the box (do not quote the requirement again)

- Before you read on, write in the next cell what "correct" means to you here, and which owner you
  would show.

### Slot GG: the text inside that cell

Two short questions, each followed by `........` on its own line: what does "correct" mean here?
Which owner would you show? Plain text.

### Slot H: after that cell

- "Correct" could mean three things, each needing something different. Write them as a Markdown
  list:
  - the newest claim: the time each claim was sent;
  - the claim from the source trusted most for owners: an order of sources for each attribute;
  - every claim, with where it came from: all of them kept, with their sources and times.
- On Tuesday at 09:00 these give: `data team`; `j.marsh`; all three owners.
- "Owner" is Chapter 2's word, which can mean a person responsible, a team, or the account that
  controls the table. `j.marsh` names a person, `data team` a team, `etl_service` an account. A rule
  that picks one claim also picks one meaning.
- The requirement does not say which it means.

### Slot Z: the closing (a heading `## Before Chapter 22`, a summary, a lead, three questions)

- Summary: three sources made five claims about `daily_sales`. The newest claim was the most recently
  sent, so a nightly import of an unchanged sheet replaced the owner and kept a column the table does
  not have. The time a source last changed picked the warehouse's account, because its content changes
  every night. An order of sources per attribute picked `j.marsh` and the warehouse's columns.
  Keeping every claim with its source left the choice to the reader.
- Chapter 22 asks when references from different systems name the same asset.
- Three questions, as a list: Which of your platform's sources resend everything on a schedule? Which
  source would you trust for an owner, and which for a schema? Where does your metadata system keep
  where each value came from?

Then a heading `### How this differs from a real platform` and a list:

- The shop's sources, their times and the team sheet are invented for the course.
- The shop keeps the latest claim of each source for each attribute. A real system may keep every
  claim it has received, with its history.
