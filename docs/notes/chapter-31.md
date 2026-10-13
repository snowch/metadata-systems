# Chapter 31: Metadata platforms

A working note. Written on 13 October 2026 with Chapters 29, 30 and 32 (`notebook/chapter_31.py`).

## What the chapter does

The reader:

- reads four platforms side by side: how metadata arrives, how it is modelled, where it is kept and
  how it is searched;
- predicts which platforms keep all three owners of `daily_sales` (Chapter 27's account, person and
  team); finds DataHub and OpenMetadata keep 3, Atlas 1, Marquez none;
- changes DataHub's ownership types, written as `typeUrn`s, from three
  `urn:li:ownershipType:__system__technical_owner`s to three different ones; 2 of 2, and all 3 told
  apart by ownership type;
- questions "Choose a metadata platform that tracks ownership."

## What was built for it

`notebook/shop/platforms.py`: `architectures`, `owners_in`, `kept`, `check`, with the types as the
reader's piece. Every rule is cited in `docs/sources.md`, "Read for Part VII".

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `architectures`

- **Role:** inspect
- **Serves:** how do the four platforms receive, model, keep and search metadata?
- **Why now:** the plan's comparison, and the setting for the owner question.

### `owners`

- **Role:** experiment
- **Objective:** the reader finds that the platforms' owner fields hold different things, and that
  only a typed owner lets a reader tell the account, the person and the team apart.
- **Known before:** Chapter 27's three owners.
- **Driving question:** which platforms keep all three?
- **The action:** write the prediction; read the two tables; change `types`.
- **Why the action:** the rules are stated; the reader applies them, then sees what a type adds.
- **Evidence:** 3, 3, 1, 0 kept; 0 told apart until the types differ, then 3 in DataHub.
- **Consequence:** "tracks ownership" is met in different senses by each platform.
- **Predictable:** yes, from the rules listed.
- **Gives nothing away:** the cell asks which; the rules are stated, the count is not.
- **Not knowing:** fair.
- **Next question:** which sense does the requirement want?

## Requirements

"Choose a metadata platform that tracks ownership." (the plan's). Readings: an owner for each
dataset; whom to ask; which meaning each owner holds. DataHub can meet all three, OpenMetadata and
Atlas the first, Marquez none for a dataset. The figure that
questions it is the free-text cell after the box.

## Originality

The obvious examples are vendor comparison tables and each platform's own architecture diagram.
This chapter draws no diagram from any project and ranks nothing: it sets four facts per platform
side by side, each from the project's own documentation or code, and puts the shop's own three
owners to each platform's rule.

## What the prose process caught

The review's revision: briefs `part-7/briefs/rev-common.md` and `P31-rev.md`, draft
`part-7/drafts/P31-rev.md`. Every fact landed; nothing added. Cut by me: the label "The question:" in the reader's cell, and "to ask of your own platform" before the questions, which repeated the first question.

Brief P31 (`part-7/briefs/`), draft `part-7/drafts/P31.md`. Fixed with the fewest words, as
placement edits (`place_p7.py`): a "The question:" label at the head of two of the reader's cells in
Chapters 31 and 32; a fragment introducing Chapter 31's list of rules; "sets" for "holds" of a cell in
Chapter 29; and Chapter 30's first mention of the provider, which now names it and Chapter 29. In
Chapter 32 the draft put "the forecast" for "a trained model", following the brief's rule on "model";
kept.

## The review

A reviewer on another model read the chapter as built (`chapter-31/review/findings.md`); an
independent sceptic attacked each of the 16 findings (`chapter-31/review/verdicts.md`): 4 upheld, 8
partly, 4 rejected. Read whole again after the fixes (`chapter-31/review/chapter_31-after-review.md`).
Acted on:

- "Each platform meets some" was false of Marquez: the readings now say what each needs and which
  platforms meet it, in parallel, and the closing sentence says which meet which;
- the check held DataHub to a rule its schema does not state (it refused `CUSTOM`): the ownership
  type is now written as a `typeUrn`, DataHub's four built-in ones are shown with their
  descriptions, and the check's simplification (it does not test that a type is defined) is said on
  the page and in the reality note; URN, `corpuser` and `corpGroup` are explained;
- `kept` counts only ownership types the check accepts; a bad value names its owner;
- "ownership type" throughout, and OpenMetadata's "team type"; the tables are named;
- the architectures paragraph that restated the table is cut; DataHub's store includes Cassandra;
  Marquez's search is off unless set; `docs/sources.md` records each;
- the OpenLineage facet sentence is cut; "your own metadata platform"; a heading before the owners.

Rejected, with the sceptic: moving the answer cells (the course's convention, raised with the author
at checkpoint 5), a harder prediction, and Atlas's "here the first".

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
29 to 32"): from Chapter 30's link, 11 files, 0.31 MB, in a new tab; Run all 8.4 to 8.5 s; peak memory
398 MB alone, 608 MB with Chapter 30 open; no error output, no console error. The browser
test (`notebook/jupyterlite/smoke.mjs`) types the reference into the chapter's cell and reads the
check.

## Known gaps

- The answer cells print below the prediction once **Run all** has run, as the course's
  convention has it; raised with the author at checkpoint 5.
- OpenMetadata's handling of a service account as an owner: its rule takes any user, which is all
  the page says.
