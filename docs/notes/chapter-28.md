# Chapter 28: Build the metadata interface

A working note. Written on 13 October 2026 with Chapters 24 to 27 (`notebook/chapter_28.py`). It
closes Part VI.

## What the chapter does

The reader draws a page for `daily_sales` from the pieces Chapters 24 to 27 built (the shop's
versions), for Chapter 27's week:

- reads the program that writes `daily_sales` and the 41 runs in the file;
- predicts whether a run history built from what each run wrote includes Monday's failed run; finds
  6 runs, without it; builds it from the programs that write the asset; 7 runs, the FAIL among them;
- chooses the page's sections from seven, and sees the page name the ones it leaves out;
- questions "The asset page must show everything about an asset."

## What was built for it

`notebook/shop/interface.py`: `SECTIONS`, `runs`, `writers`, each section's rows, `Page`, `page`,
`check`.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `writers-and-runs`

- **Role:** inspect
- **Serves:** what can a run history be built from? The writers of `daily_sales`, and the number of
  runs in the file.
- **Why now:** the two ways of building it use these.

### `run-history`

- **Role:** experiment
- **Objective:** the reader discovers that a run that failed wrote nothing, so a history built from
  what runs wrote hides it.
- **Known before:** Chapter 13's failed night; Chapter 27's week.
- **Driving question:** will the history include Monday's run?
- **The action:** write the prediction; read the check; change `run_history`; press **Run below**.
- **Evidence:** 6 runs as it stands; 7, the FAIL among them, after.
- **Consequence:** a view must be built from the record that holds what it shows.
- **Predictable:** partly.
- **Gives nothing away:** the cell asks yes or no.
- **Not knowing:** fair.
- **Next question:** what should the page show?

### `page`

- **Role:** experiment (the reader's choice of sections), and the figure the requirement then reads.

## Requirements

"The asset page must show everything about an asset." Readings: every section the shop can draw;
what a person asking about the asset needs; the whole history. The page names what it leaves out.
The figure that questions it is the free-text cell after the box.

## Originality

The obvious examples are a catalogue product's asset page and its screenshots. This page is drawn
from the shop's own pieces, its sections are named in a list the reader edits, and the failed run is
the shop's.
