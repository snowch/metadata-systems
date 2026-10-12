# Chapter 3: What is metadata?

A working note. The chapter was written on 12 October 2026, at the author's request to "author
chapter 3 and 4", as a notebook (`notebook/chapter_03.py`, built into the site as
`chapter_03.ipynb`) in the form Chapter 2 set: prose, with cells the reader runs and changes.

## What the chapter does

Chapter 2 ended by promising a description of each asset, kept beside the data, with what it means
and who is responsible for it, and then the four questions asked again. The chapter keeps that
promise. It is the Monday afternoon: the head of the shop names Jo Marsh as the person who decides
what counts as revenue, Sam Lund as the keeper of the catalogue, and the cleaned tables as yours;
Jo gives a day's revenue a meaning. The reader writes a record of `daily_sales` from those two
messages, in a line notation of the course's own (`asset [column] field: value`), and then:

- asks Chapter 2's four questions of the record, after writing down which it answers: who to ask
  (yes), whether Thursday is wrong (yes, against Jo's meaning; not since when), what reads
  `products.csv` or `orders.jsonl` (no);
- compares `daily_sales` with Jo's meaning turned into a query over the raw orders (Thursday
  differs) and with the meaning Chapter 2's reconstruction would have given (no day differs): a
  description written from the data cannot show the data wrong;
- sorts what the platform already records into what an asset is (**descriptive**) and what
  happened to it (**operational**), and names a table's columns and types its **schema**;
- meets `updated_by`, a column that names people and is data about products, not a record about
  the file, and the file's first line, which describes the file from inside it: metadata is defined
  by what it describes, not where it is kept;
- questions "Every column must have a description." (below);
- sees what two comparisons catch when the platform changes: the check against the warehouse's
  columns catches a new column (the record is incomplete); Jo's meaning as a query catches the
  effect of Chapter 2's edited job (the table no longer matches the meaning the record holds); and
  neither says what changed in the job, when, or who changed it.

It introduces *descriptive*, *operational* and *schema* (the plan's terms for the chapter), each
in the section "What the platform keeps", which the term test holds.

## What was built for it

- `notebook/shop/records.py`: Chapter 3's records (`shop.records`), a parser of the line notation,
  `sql` over the lines as a table, `about`, and `check(warehouse, asset=None)`: every warehouse
  column needs a `means` line with a value (dots are a value not yet written), and every line must
  name a table or file that exists and a column the table has. It cannot test what a description
  says. The messages it prints are Haiku's drafts of brief CC.
- A fourth change, `column` (`notebook/shop/week.py`): from Saturday's row, the job that writes
  `daily_sales` also writes `order_count`, a column the warehouse's catalogue records at once
  (`Warehouse.add_column`); the rows before have none. `Warehouse.write` now takes a table's types
  from its catalogue, not from the fixed list, so a table can gain a column.
- `Rows` takes the text it prints when empty (`No problems found.` for a check), and sets a name in
  backticks inside a printed table in the code font.

## Figures

The platform's diagram is the chapter's only drawn figure; the rest are cells the reader runs.

### `platform`

- **Role:** reference
- **Serves:** where the assets the chapter describes live, in the order data moves; it draws no
  asset made from another, since nothing the reader has built records that.
- **Why now:** the map appears in every chapter, and the record the reader writes is about one of
  its assets.

### `the-record`

- **Role:** experiment (the reader builds; the check completes it)
- **Objective:** the reader finds that the facts Chapter 2 could not find on the platform can be
  written down in a few lines, once someone with the answers is asked.
- **Known before:** the two messages, quoted just above the cell.
- **Driving question:** what would you write down about `daily_sales` so the next person need not
  reconstruct it?
- **The action:** replace five lines of dots with what the messages say, and press **Run below**.
- **Why the action:** the four questions are asked of the reader's own record; a record the page
  supplied would answer them by fiat.
- **Evidence:** the record as a table, and the check of `daily_sales`, which finds no problems once
  every line is written.
- **Consequence:** the reader holds a record of their own making, and sees what the check holds it
  to (a description per column) and what it does not (whether the description is true).
- **Predictable:** yes; the check's rule is stated before it runs.
- **Gives nothing away:** the cell asks for no prediction.
- **Not knowing:** not applicable: the reader writes what they were told.
- **Next question:** which of Chapter 2's questions does this record answer?
- **An experiment:** the reader builds, and the check is the evidence; with nothing to predict it
  is closer to a construction than to an experiment, and the next figure is the experiment.

### `the-four-questions`

- **Role:** experiment
- **Objective:** the reader discovers that a descriptive record answers who to ask and whether a
  number matches its stated meaning, and nothing about when or about what reads what.
- **Known before:** the four questions (repeated word for word), their record, and Jo's meaning.
- **Driving question:** which of the four questions does the record answer, and how far?
- **The action:** write a verdict per question in a cell (Save keeps it), then run the cells that
  ask the record: who is responsible; `daily_sales` against Jo's meaning as a query; against the
  reconstruction's meaning; every line that names either file.
- **Why the action:** the reader commits before seeing; the queries are the record's answers, not
  the page's.
- **Evidence:** Jo Marsh; Thursday alone differs (5150 against 20550 pence); no day differs from the
  reconstruction's meaning; no line names either file.
- **Consequence:** a reader who expected the record to answer "since when" finds it holds no time;
  one who expected the reconstruction's description to catch Thursday finds that a description
  read off the data agrees with it everywhere. Both are the chapter's point.
- **Predictable:** yes, from Chapter 2's three orders and the statuses its cell printed.
- **Gives nothing away:** the verdict cell sits above every answering cell; the prose above it
  restates the questions and asks for the verdict, nothing more.
- **Not knowing:** "in part" is an answer the cell invites, and is right for the first question.
- **Next question:** what else does the platform record, and is that the same kind of record?
- **An experiment:** the reader commits, runs, and the outputs answer.

The note under Jo's query, that "every completed order" does not say what to do with an order the
export wrote twice, is the requirement habit at small scale: the words left a decision to whoever
turned them into a query, and the query made it (`DISTINCT`). Counting every line would mark
Wednesday different too; the test pins both.

### `the-schema`

- **Role:** inspect
- **Serves:** "schema", named in the sentence above it, and the 14 columns the requirement later
  covers.
- **Why now:** the paragraph has just sorted the warehouse's fields into what a table is and what
  happened to it; its columns and types are the first kind.

### `updated-by`

- **Role:** inspect, with the question put before it in the prose
- **Serves:** whether a column that names people says who is responsible for the file it is in.
  The counts (three logins over 8 products) make it plain that the column is about products.
- **Why now:** the head of the shop has just named Sam Lund for the catalogue, so `s.lund` in the
  column invites the wrong reading, and the chapter's title asks what metadata is.

### `requirement-verdict` and `by-name`

The requirement exercise (below): the verdict cell, the full check (12 columns undescribed), the
cell that writes a description from each column's name and passes the check, and the two lines it
wrote for `daily_sales`.

- **Role:** experiment
- **Objective:** the reader learns that a requirement met as written can say nothing, and that a
  check can count descriptions but cannot judge them.
- **Known before:** the requirement, the line `the revenue in pence`, and the four readings, which
  come after the verdict cell.
- **Driving question:** does the line meet the requirement?
- **The action:** write a verdict; run the full check; run the cell that meets the requirement
  mechanically.
- **Why the action:** the mechanical pass takes four lines of code; doing it is the argument.
- **Evidence:** 12 columns undescribed; then none; `day means: day`, `revenue_pence means:
  revenue pence`.
- **Consequence:** "yes, as written" and "no, as meant" are both right, and the reader sees why.
- **Predictable:** yes.
- **Gives nothing away:** the verdict cell comes before the readings and before either check.
- **Not knowing:** "it depends what the requirement means" is the answer the section arrives at.
- **Next question:** what happens to a record when the platform changes and nobody updates it?
- **An experiment:** the reader commits and runs.

### `stale-record`

- **Role:** experiment
- **Objective:** the reader discovers that a check against the warehouse catches a change the
  warehouse records (a column) and not one it does not (a job's rule), and that only an
  operational record made at the time would show the second.
- **Known before:** both changes, described in full; the check's rule; Jo's query.
- **Driving question:** will the check of `daily_sales` report a problem after each change?
- **The action:** write a verdict per change, then run the week with each change and check the
  record.
- **Why the action:** the reader must reason from what the check compares; the outputs settle it.
- **Evidence:** `order_count` with no description; nothing for the edit; then Jo's query on the
  edited week: Saturday differs (21549 against 19149 pence).
- **Consequence:** a reader who expected the check to guard the record's meaning learns what it
  compares; Chapter 7's records are motivated.
- **Predictable:** yes: the check compares columns, and only one change adds one.
- **Gives nothing away:** the verdict cell is above both checks; the prose describes the changes
  and not their effect.
- **Not knowing:** not the right answer here: the check's rule settles it.
- **Next question:** Chapter 4's: is Jo Marsh `j.marsh`, and how would a record say so?
- **An experiment:** the reader commits and runs.

The changes are run as counterfactual weeks ("the shop could make two changes"), as Chapter 2's
menu does: the record describes the plain week, and each change is applied to a week run again.

## Requirements

The chapter questions "Every column must have a description.", the plan's candidate, with the
`requirement-verdict` and `by-name` cells.

1. **What it says:** every column has a description.
2. **What it might mean:** what the column means (which orders it counts); its unit; where its
   values come from; whether it may be empty.
3. **What each needs:** a statement of the rule (completed orders, each once, by UTC day); a `unit`
   line; a record of the asset and columns it is computed from; a line saying whether it may be
   empty, which a check could test against the rows.
4. **What the platform records:** nothing; the shop's check counts `means` lines with a value.
5. **Whether it is met:** as written, yes, by four lines of code that turn each column's name into
   its description; under every other reading, no.

The reader commits before the readings; no reading is marked wrong.

## Originality

The obvious example for "what is metadata?" is the library catalogue card or a photograph's EXIF
fields, with "data about data" as the definition, and, for a data platform, adding descriptions and
owners in a catalogue's screens or a dbt project's YAML file of model and column descriptions. This
chapter writes its definition from a case: a column inside a file that names people and is data,
beside the same file's first line, which is metadata; it uses its own line notation, not YAML or a
product's screens; and its experiments (a description read off the data that cannot fail, a
requirement met by four lines of code, a check that catches a new column and not a new meaning)
are built on the shop's invented week. The shop, Jo Marsh, Sam Lund and the messages are invented
for the course.

## Accuracy

- PostgreSQL's `COMMENT ON` (the closing note): read from the documentation's source in
  `postgres/postgres` (`doc/src/sgml/ref/comment.sgml`, branch `master`, commit `a241bc4`), because
  postgresql.org refused the build environment; recorded in `docs/sources.md`.
- The definition the chapter states, that information is metadata by what it describes (an asset,
  or the work done on the platform) and not by where it is kept or who wrote it, holds for the
  cases the course has met: a CSV header, a warehouse's catalogue, a person's record, a Parquet
  footer (`docs/sources.md`). It does not claim that a value is metadata in every context: the
  chapter says `updated_by` is data about the business on this platform.
- The sorting into descriptive and operational is the course's (`CLAUDE.md`, "The thesis"); the
  created time is put with what happened, as a time something happened once.

## What the prose process caught

Five briefs went to Haiku drafting agents (`docs/notes/chapter-03/briefs/`, drafts under
`drafts/`): CA (opening, record, the four questions), CB (the two kinds, the person, the
requirement, the stale record, the close), CC (the check messages, for both chapters) and CD (the
warning boxes, both chapters), after the measurement below. The fact check found:

| Draft | Dropped, restored with the fewest words | Wrong, sent back |
| --- | --- | --- |
| CA | the questions cell dropped "in orders.jsonl" from the third question | |
| CB | | the close said a description written from the data could have answered neither question; the fact is only that it could not have shown Thursday wrong |
| CC | the model message's form omitted a value of one type | |
| CD | | |

Each agent was told to write its file once and not change it after replying, and the checked
drafts were frozen before placing. The agent drafting brief DA reported one stray `send_message`
call to a session it did not have; it failed and delivered nothing.

## The read as built

Both chapters were built, run in CPython and read start to finish as text. Two faults found and
fixed in code: the table printed by a check showed a name's backticks literally (now the code
font); and Chapter 4's owner table depended on whether the reader had made the merge's two edits
(the cell now applies them itself, which changes nothing when they are made).

The chapter's outputs after **Run all**, before the reader fills in the record, show the dots and
the check's two problems; the prose after the record cell describes the record as written. The
record cell's text says to fill it in and press **Run below** before reading on.

## Measured

Measured 12 October 2026 on the built site, served locally, in Chromium with a profile on disk
(`docs/notes/notebook-prototype.md`, "Chapters 3 and 4"): about 13 MB the first time on its own;
0.32 MB from Chapter 2's link in a new tab after Chapter 2 had run; Run all 8.9 to 9.6 s; peak
memory 400 to 418 MB.

## The review, 12 October 2026

A reader on another model read the chapter as built and after the reader's edit, as a learner who
had done Chapters 1 and 2 (`docs/notes/chapter-03/review/`: the brief, the pages read, 22 findings,
8 marked blocking), and an independent sceptic attacked each finding (`verdicts.md`): none was
rejected outright, several were trimmed, and one piece of evidence was wrong (`daily_sales` gains a
row every night; the claim about row counts still failed for `clean_customers`, which each night
replaces with the same 9 rows). Code first, then brief CE (Haiku, checked for facts: nothing
dropped, nothing wrong; the close's heading, which the draft left out, was put back), then the
messages of brief CF. What changed:

- The expectation cells say "before you read on": after **Run all**, and after **Run below** from
  the record, the cells below have already run (findings 1, 6). The record cell says that until it
  is filled in the cells below show the dots.
- The head of the shop's reply now names Jo Marsh for `daily_sales` (2); the answer to "who should I
  ask" is said to be what the reader wrote, now kept where it can be queried.
- The stale-record section is now "When the platform changes", and says what each comparison
  compares and catches, and what neither can say (3); the close and its questions follow.
- The two kinds of information: what the warehouse keeps is the last of each, not a history,
  reconciled with Chapter 2; the criterion is stated; only the last-altered time changes with every
  write (4, 5). The section is a list, not five paragraphs (19).
- The definition is Chapter 2's ("information about an asset or about the platform"), and
  `updated_by` is said to describe products and edits made in the catalogue, not an asset (7).
- *Record* is the reader's set of lines only; what a system keeps is information; one line is a
  line (8). The check's messages tell a missing `means` line from one still dots (14), and lines are
  numbered from 1 (15).
- Smaller: the example line is not one the reader fills in (9); the files' lookup says why it finds
  nothing (10); the order written twice is said once (11); why Tuesday, Wednesday and Saturday agree
  with Jo's meaning, and that the reconstruction agrees by construction (12); the requirement's five
  readings, the first as written (13); the check's unused capability is not mentioned (16); the
  opening ends on the problem, not a roadmap (17); the question comes before the `updated_by` count
  (18); the second use of "schema" (20); the closing questions lead to Chapter 4 (21); the
  objectives and the close cover the requirement (22).

## Known gaps

- The run time and memory were measured on the local build, not yet on the published page.
- The reader's verdicts are free text, kept by **Save**; nothing compares them with the outputs.
