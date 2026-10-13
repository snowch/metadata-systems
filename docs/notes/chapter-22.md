# Chapter 22: Identity across systems

A working note. Written on 12 October 2026 with Chapters 18 to 21 and 23
(`notebook/chapter_22.py`).

## What the chapter does

- reads six references (a reference is the name one system uses for an asset): the warehouse's, the
  events' namespace and name, the development table in `shop_dev`, a transformation tool's model
  `shop_models:daily_sales`, the reporting tool's dataset `Daily sales`, and Jo Marsh's CSV export
  of `daily_sales`;
- predicts which merge when references are merged by the last part of their name, then runs it:
  all six, the development table and Jo's copy among them;
- meets **entity resolution**; runs Chapter 12's qualified names (the warehouse and the events
  merge; the development table is another database, the file's name an object's key, the tools'
  names not warehouse names), then adds the **aliases** two configurations declare (the model and
  the dataset each stand for the table, which is the shop's choice): four merge, the development
  table and the copy stay apart;
- questions "Merge the same dataset across systems."

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `references`

- **Role:** inspect
- **Serves:** which names does the shop's metadata system receive for `daily_sales`, and from
  where?
- **Why now:** the merge rule's prediction needs the six names in view.

### `last-part`

- **Role:** experiment
- **Objective:** the reader discovers that a rule loose enough to join every system's name joins
  different assets too.
- **Known before:** Chapter 12's identity tests and the development database.
- **Driving question:** under "last part", which references become one entity?
- **The action:** write in a free-text cell; read the merge.
- **Why the action:** the rule is stated; applying it by hand to six names is the reasoning.
- **Evidence:** one entity of six.
- **Consequence:** merging too much puts the development table's runs in production's lineage;
  merging too little leaves the model, the dataset and the table apart.
- **Predictable:** yes, from the stated rule.
- **Gives nothing away:** the cell asks which merge, and names none.
- **Not knowing:** fair.
- **Next question:** what evidence would merge the right four?

### `qualified`

- **Role:** experiment (completes `last-part`): change `"last part"` to `"qualified"`, press **Run
  below**.
- **Evidence:** five entities: the warehouse's and the events' references merge.

### `aliases`

- **Role:** experiment (completes `last-part`): change the rule to `"aliases"`, press **Run below**.
- **Evidence:** entities of 4, 1 and 1.

## Requirements

"Merge the same dataset across systems." Readings: the same name; the same rows; the same thing to
the business; across environments. The page gives a verdict for each: met for warehouse names by
the qualified rule; not tested for rows, since no rule compares contents; met for the business only
as far as two configurations declare, the shop's choice; the development table kept apart. The
figure that questions it is the free-text cell after the box. The overlap with Chapter 12's readings
is the plan's decision (`docs/plan.md`, requirements table).

## Originality

The obvious examples are a catalogue's URN scheme and its documentation of platform instances.
This chapter's six references, the transformation tool's notation, the reporting tool's dataset and
Jo Marsh's export are the shop's own, invented; the rules are the shop's.

## What the prose process caught

Brief R, draft `part-5/drafts/R.md`; the review's changes through brief R-rev, draft
`part-5/drafts/R-rev.md`. In the revision, Haiku turned the brief's label "what the experiments
could not show" into a sentence that announced a list; cut, the facts kept. It also restored a lead-in
to the questions that the first placement had cut; cut again.

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 13 findings (`review/verdicts.md`): 4 upheld, 6 partly, 3 rejected. Read whole again after the fixes, with each
cell's output (`review/chapter_22-after-review.md`). Acted on:

- an alias equated a model and a dataset with the table as if building or reading made them the
  same; the page now says the two configurations declare the names stand for the table, that taking
  them so is the shop's choice, and that a filtered or summed dataset is not an alias;
- the requirement section gives a verdict per reading;
- "six systems" was false; the page counts references, and says what a reference is;
- the claim about Jo Marsh's file on the day it was exported is gone; the export is listed as
  invented;
- every reference left alone under `qualified` has its reason; the bullet list that repeated the
  table is gone, its two extra facts folded into the opening;
- the closing says what the rules could not show; the reality note names `symlinks`.

Rejected, with the sceptic: a new requirement candidate (the plan's), a figure of merging, and the
map.

## Measured

Locally, 12 October 2026, before the review's changes (`docs/notes/notebook-prototype.md`,
"Chapters 18 to 23"): from Chapter 21's link, 11 files, 0.31 MB, in a new tab; Run all 7.8 to 8.7 s;
peak memory 388 to 394 MB alone, 608 MB with Chapter 21 open; no error output.
Live, 12 October 2026, published at `b15b63a`, opened alone at desktop and phone widths: Run all
9.2 to 9.4 s; peak memory 389 to 394 MB; no error output, no console error. The warning's 9 to 12 seconds and about 400 MB
hold.

## Known gaps

- No rule compares contents; the rows reading is stated, not tested.
