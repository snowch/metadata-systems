# Chapter 21: Conflicting metadata

A working note. Written on 12 October 2026 with Chapters 18 to 20, 22 and 23
(`notebook/chapter_21.py`).

## What the chapter does

- reads three sources' claims about `daily_sales`: the warehouse's catalogue (owner `etl_service`,
  columns `day, revenue_pence`), your records (owner `j.marsh`), and the previous engineer's team
  sheet (owner `data team`, columns `day, revenue`), each with when it was sent and when its source
  last changed;
- sees that "newest wins" shows `j.marsh` on Monday at 18:00, and predicts what it shows at 09:00 on
  Tuesday 15, after the nightly sync and import: `data team`, and the stale columns, though nobody
  changed anything;
- tries "as of" (`etl_service`: the warehouse's content changes every night, its owner does not) and
  "ranked" by attribute (`j.marsh` and the warehouse's columns); meets **precedence**;
- keeps every claim with its source, and questions "Show the correct owner.", where Chapter 2's
  owner returns.

## Figures

### `claims`

- **Role:** inspect
- **Serves:** the five claims, their sources and their two times.

### `newest-overnight`

- **Role:** experiment
- **Objective:** the reader discovers that the newest claim is the most recently sent, which can be
  the oldest content.
- **Known before:** Chapter 2's and Chapter 4's owners; Chapter 3's records.
- **Driving question:** what will "newest wins" show on Tuesday morning?
- **The action:** commit; change the time to Tuesday 09:00, press **Run below**.
- **Evidence:** `data team` and `day, revenue`, from the team sheet.
- **Consequence:** the rule chose by when a claim was sent, not by when it was true.
- **Predictable:** yes, from the sent times.
- **Gives nothing away:** the options are values.
- **Not knowing:** fair.
- **Next question:** which rule would choose well?

### `rules`

- **Role:** experiment (completes `newest-overnight`): `as of`, `ranked`, `all`.

## Requirements

"Show the correct owner." Readings: the newest claim; the claim from the most trusted source for
the owner; every claim with where it came from. Each rule's answer on Tuesday: `data team`;
`j.marsh`; all three. "Correct" also carries Chapter 2's question: owner in which sense.

## Originality

The obvious examples are a catalogue product's documentation of ownership types, and a data
fusion paper's source-reliability ranking. This chapter's three sources, two times and four rules
are the shop's own; the stale claim comes from a nightly import of an unchanged sheet.
