# Chapter 22: Identity across systems

A working note. Written on 12 October 2026 with Chapters 18 to 21 and 23
(`notebook/chapter_22.py`).

## What the chapter does

- reads six references from six systems: the warehouse, the events, the development warehouse, a
  transformation tool the developer has started to use, the reporting tool's dataset, and Jo
  Marsh's CSV export of `daily_sales`;
- predicts which merge when references are merged by the last part of their name, then runs it:
  all six, the development table and Jo's copy among them;
- runs Chapter 12's qualified names (the warehouse and the events merge; nothing else), then adds
  the **aliases** each system's own configuration states (the model's table, the dataset's table):
  four merge, the development table and the copy stay apart; meets **entity resolution**;
- questions "Merge the same dataset across systems."

## Figures

### `references`

- **Role:** inspect

### `last-part`

- **Role:** experiment
- **Objective:** the reader discovers that a rule loose enough to join every system's name joins
  different assets too.
- **Known before:** Chapter 12's identity tests and the development database.
- **Driving question:** under "last part", which references become one entity?
- **The action:** commit; run.
- **Evidence:** one entity of six.
- **Consequence:** over-merging is as real a fault as not merging.
- **Predictable:** yes.
- **Gives nothing away:** options are groupings.
- **Not knowing:** fair.
- **Next question:** what evidence would merge the right four?

### `aliases`

- **Role:** experiment (completes `last-part`)
- **Evidence:** entities of 4, 1 and 1.

## Requirements

"Merge the same dataset across systems." Readings: the same name; the same rows; the same thing to
the business; across environments or not. The alias rule merges by what each system's
configuration says it reads or builds; it keeps the development table apart, which a reading "the
same thing to the business" might merge.

## Originality

The obvious examples are a catalogue's URN scheme and its documentation of platform instances.
This chapter's six references, the transformation tool's notation and the reporting tool's dataset
are the shop's own, invented; the rules are the shop's.
