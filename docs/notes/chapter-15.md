# Chapter 15: Provenance

A working note. Written on 12 October 2026 with Chapters 14, 16 and 17, as a notebook
(`notebook/chapter_15.py`).

## What the chapter does

Chapter 2's question returns: where did Thursday's £51.50 come from? The reader:

- writes which orders they expect it to be made of, then follows it back four steps, from the
  dashboard to four lines of the version of `orders.jsonl` that `run-014` read, each step 5150 pence,
  and meets **provenance**: the total is a set of four orders, not one source;
- changes `dropped=False` to `dropped=True` and finds the three orders that made the total low only
  among the rows the run read and left out, with the condition that left each out;
- in the week with the `corrected` change, writes whether Sunday's total adds up from the tables as
  they are, finds it does not (8350 against 6925), reads the two versions of `r-205`'s object, and
  changes `as_read=False` to `as_read=True` to rebuild `returns` as it was when `run-034` started;
- questions "Show where Thursday's total came from." against four readings.

## What was built for it

- `notebook/shop/provenance.py`: `trace` (with `dropped` and `as_read`), `returns_as_of`,
  `figure_adds_up` and `object_versions`.
- The `corrected` change (Part IV's changes are in `docs/lab.md`), and the returns desk's changes of a
  day applied before that night's work.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the assets the total passes through.
- **Why now:** every chapter opens with the map.

### `thursday-back`

- **Role:** experiment
- **Objective:** the reader learns that a total's provenance is the set of rows it was made from,
  with the runs and the input versions, and that no one row is its source.
- **Known before:** Chapter 2's four orders with a customer id and three without.
- **Driving question:** which orders is £51.50 made of?
- **The action:** write the expectation; read the four steps.
- **Why the action:** the steps are the evidence for the reader's belief, step by step.
- **Evidence:** 7020, 7022, 7024, 7026; lines 21, 23, 25, 27; 5150 at every step.
- **Consequence:** the reader's belief from Chapter 2 now rests on a record, not a reconstruction.
- **Predictable:** yes, from Chapter 2.
- **Gives nothing away:** the prompt names the total only.
- **Not knowing:** reasonable for a reader who has forgotten Chapter 2; the steps settle it.
- **Next question:** do the steps show the orders that made it low?
- **An experiment:** commit, read, compare.

### `what-was-left-out`

- **Role:** experiment
- **Objective:** the reader discovers that a record of what made a total omits what was left out,
  which was the question about Thursday.
- **Known before:** the four steps; Chapter 2's three orders.
- **Driving question:** what reason will the steps give for each of orders 7021, 7023 and 7025?
- **The action:** change `dropped=False` to `dropped=True`, press **Run below**.
- **Why the action:** the same trace, with what the run read and did not use.
- **Evidence:** lines 22, 24 and 26, `customer_id IS NOT NULL is false`, 15400 pence.
- **Consequence:** answering "why is it low" needs the rows each run read and the condition.
- **Predictable:** partly; the reader knows from Chapter 2 why they were left out, and must say it as the program's condition.
- **Gives nothing away:** the question is asked before the change.
- **Not knowing:** not the right answer.
- **Next question:** do the inputs the total came from still hold what they held?
- **An experiment:** change, run again, compare.

### `sunday-as-it-is` and `r-205-versions`

- **Role:** experiment, with the versions as its instrument
- **Objective:** the reader discovers that a total can stop adding up from its inputs as they are now,
  and that only a kept version of what a run read explains it.
- **Known before:** the `net` change of Chapter 10; the correction, told before the cell.
- **Driving question:** does Sunday's total add up from the tables as they are now?
- **The action:** write the expectation; read the steps; read the versions; change `as_read`, press
  **Run below**.
- **Why the action:** the same steps with `returns` as it was at 02:30 settle the difference.
- **Evidence:** 9775 less 1425 is 8350, not 6925; versions of 2 and 1 rolls; with the first, 6925.
- **Consequence:** provenance needs the inputs as they were, and a table without versions can be
  rebuilt only where its writers recorded what they read.
- **Predictable:** yes, once the correction is told.
- **Gives nothing away:** the result is not stated before the cell.
- **Not knowing:** a fair answer until the times are compared.
- **Next question:** what would a requirement for provenance ask for?
- **An experiment:** commit, run, change, run again.

## Requirements

The chapter questions "Show where Thursday's total came from.", the plan's candidate, with
"figure" in it now "total" (the course keeps "figure" for an interactive box).

1. **What it says:** show where Thursday's total came from.
2. **What it might mean:** the rows; the program; the run; the rows as each run read them.
3. **What each needs:** a row-by-row trace; lineage; the record of each run; a kept version of each
   input.
4. **What the shop records:** runs and their code; every version of every object; tables as they are
   now only; the object version each function's run read.
5. **Whether it is met:** for Thursday, the first three, and the fourth for the file; for Sunday with
   the correction, the fourth only through object versions. The requirement does not say which it
   means, and none shows what was left out.

## Originality

The obvious examples are the textbook why-provenance of a query result over a small relation of
people or employees, and a lineage product's column-level "data journey" view. This chapter follows
the shop's own dashboard total through the shop's own runs, with the shop's own rows left out by its
own rule, and a return corrected after the run that read it. PROV is described in the course's own
words and only in the reality note.

## What the prose process caught

Brief UA, draft `drafts/U.md`. One fact wrong: "the first line of the shop's message" for "the
head of the shop's message", and the requirement given as the shop's, not the head of the shop's;
both corrected. "Figure" for a number became "total" throughout, my brief's fault.

## Sources

W3C PROV-DM (W3C Recommendation, 30 April 2013), read 12 October 2026 (`docs/sources.md`).

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 19 findings (`review/verdicts.md`). Every number was right. Acted on,
through brief UB and draft `drafts/UB.md`:

- the trace credited the rows of `clean_orders` to `run-014`, though the table as it is now was
  written by `run-026`: the engine now names the run that wrote the table as it is now, and the page
  says `run-015` read the table after `run-014` wrote it, and that those rows are not kept;
- the file's version is said to be chosen by time, since `run-014` recorded no version;
- the rebuilt `returns` is called rebuilt, and its giving 6925 the evidence, not an observation;
- provenance is defined plainly, without the four readings the requirement section separates;
- the objective no longer states the Sunday result; the Thursday prediction asks for the reason the
  steps will give, which a reader can get wrong;
- "the shop's object storage" and "the shop's warehouse"; "the SQL function"; PROV-DM's "with some
  fixed aspects" quoted and attributed; full timestamps; one row per left-out line.

Rejected, with the sceptic: "the next week" (the course's idiom), the map, saying which of 6925 and
8350 to believe (left open, as Chapters 16 and 17 take it up), and the closing's bridge to Chapter
16. Read whole again after the fixes (`review/chapter_15-after-review.md`).

## Measured

Locally, 12 October 2026 (`docs/notes/notebook-prototype.md`, "Chapters 14 to 17"): from Chapter 14's link, 12 files, 0.32 MB, in a new tab; Run all 8.4 to 9.0 s; peak memory 394 to 400 MB alone, 614 MB with Chapter 14 open; no error output. Live: to be measured once published.

## Known gaps

- The trace applies the programs' conditions again; it does not run the programs' SQL row by row.
- Tables are read as they are now: a table rewritten with different rows since a run would break the
  trace silently where it is not rebuilt from object versions.
