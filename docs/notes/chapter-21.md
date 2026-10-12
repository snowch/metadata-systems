# Chapter 21: Conflicting metadata

A working note. Written on 12 October 2026 with Chapters 18 to 20, 22 and 23
(`notebook/chapter_21.py`).

## What the chapter does

- reads three sources' claims about `daily_sales`: the warehouse's catalogue (owner `etl_service`,
  columns `day, revenue_pence`), your records (owner `j.marsh`), and the previous engineer's team
  sheet (owner `data team`, columns `day, revenue`), each with when it was sent and when its source
  last changed;
- sees that "newest wins" shows `j.marsh` on Monday at 18:00, and predicts what it shows at 09:00 on
  Tuesday 15, after the nightly sync and import: `data team`, and the stale columns, though neither
  the records nor the sheet changed; then reads Tuesday's claims with their sent times; meets
  **precedence**;
- in a cell of its own, on Tuesday's claims, tries "as of" (`etl_service`: the warehouse's content
  changes every night, its owner does not) and "ranked" by attribute (`j.marsh` and the warehouse's
  columns, while the records have been sent: at 12:00 on Monday it gave `data team`);
- keeps every claim with its source, and questions "Show the correct owner.", where Chapter 2's
  owner returns.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `claims`

- **Role:** inspect
- **Serves:** what does the shop hold about `daily_sales`, and from whom? The five claims, their
  sources and their two times; the shop keeps each source's latest sending of each attribute.
- **Why now:** every rule below chooses among these rows.

### `newest-overnight`

- **Role:** experiment
- **Objective:** the reader discovers that the newest claim is the most recently sent, which can be
  the oldest content.
- **Known before:** Chapter 2's and Chapter 4's owners; Chapter 3's records.
- **Driving question:** what will "newest wins" show on Tuesday morning?
- **The action:** write in a free-text cell; read the rule's choice at Tuesday 09:00, then the
  claims with their sent times.
- **Evidence:** `data team` and `day, revenue`, from the team sheet, sent at 04:00 on Tuesday.
- **Consequence:** the rule chose by when a claim was sent, not by when it was true.
- **Predictable:** yes, from the sent times.
- **Gives nothing away:** the cell asks for an owner and names none; Tuesday's claims are shown
  only after it.
- **Not knowing:** fair.
- **Next question:** which rule would choose well?

### `rules`

- **Role:** experiment (completes `newest-overnight`): one cell, fixed at Tuesday 09:00, starting
  at `rule = "as of"`; the reader changes it to `"ranked"`, then `"all"`, pressing **Run below**.
- **Evidence:** `etl_service` and `day, revenue_pence`; `j.marsh` and `day, revenue_pence`; five
  rows.

## Requirements

"Show the correct owner." Readings: the newest claim; the claim from the most trusted source for
the owner; every claim with where it came from. Each rule's answer on Tuesday: `data team`;
`j.marsh`; all three. "Correct" also carries Chapter 2's question: owner in which sense, and the
three claims answer three: a person, a team, an account. The record holds all three; only keeping
every claim leaves the meaning open; the requirement names neither, so no output is shown to be
correct. The figure that questions it is the free-text cell after the box.

## Originality

The obvious examples are a catalogue product's documentation of ownership types, and a data
fusion paper's source-reliability ranking. This chapter's three sources, two times and four rules
are the shop's own; the stale claim comes from a nightly import of an unchanged sheet.

## What the prose process caught

Brief Q, draft `part-5/drafts/Q.md`; the review's changes through brief Q-rev, draft
`part-5/drafts/Q-rev.md`. In the revision, Haiku dropped the quotation marks round "Owner" as a
word; restored. My brief's "while your records had been sent" read as time, not condition; "once".

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each finding (`review/verdicts.md`): 3 upheld, 4 partly, 2 rejected of the 9
numbered findings. Read whole again after the fixes, with each cell's output
(`review/chapter_21-after-review.md`). Acted on:

- "Change `newest`... in the cell" could mean the Monday cell, where `as of` gives `j.marsh`; the
  rules now have their own cell, fixed at Tuesday 09:00;
- "Nobody changes anything" was false: the table is written every night; the page says what does
  not change;
- Tuesday's claims are shown after the prediction, so the explanation can be checked;
- "every claim is kept" against the shop's latest sending per source: the page says the shop keeps
  the latest, and "every claim the shop holds";
- `ranked`'s order is the shop's, and it fails when the first source has sent nothing (Monday
  12:00, `data team`); "role" gone;
- the requirement section says which meaning each claim carries and that no output is shown
  correct; the owner is the account the warehouse records, not the one that created the table; the
  records' `responsible` filed under `owner` is the shop's choice.

Rejected, with the sceptic: a fourth reading for `as of`, a new figure of time, and renaming the
house wording.

## Measured

Locally, 12 October 2026, before the review's changes (`docs/notes/notebook-prototype.md`,
"Chapters 18 to 23"): from Chapter 20's link, 11 files, 0.31 MB, in a new tab; Run all 7.8 to 8.0 s;
peak memory 390 to 397 MB alone, 608 MB with Chapter 20 open; no error output.

## Known gaps

- The week ends on the night of Monday 14; Tuesday's claims follow the same nightly schedule, which
  the page says.
