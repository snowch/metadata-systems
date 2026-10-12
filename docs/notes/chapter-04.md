# Chapter 4: Metadata as a model

A working note. The chapter was written on 12 October 2026 with Chapter 3, as a notebook
(`notebook/chapter_04.py`, built into the site as `chapter_04.ipynb`).

## What the chapter does

Late on the Monday, the head of the shop asks for a list: "Each asset has one owner. Send me the
list." The reader's records from Chapter 3 and the notes Jo Marsh keeps are put together in Chapter
3's notation, and the reader:

- lists every `responsible` line, writes down how many people they expect the records to name, and
  counts the different values: 4, because `daily_sales` has Jo Marsh in one record and `j.marsh` in
  the other. The evidence that they are one person (the head said Jo built the dashboard; the
  reporting tool records `j.marsh` as its creator) supports it without proving it; the staff list
  settles it;
- meets **entity**, **attribute**, **identifier** and **dataset**, each from the need: to count
  people the records must describe people, say what kind of thing each line is about, and use one
  value for each person; files and tables share their attributes and become one type;
- reads the same records in Chapter 4's notation (`type identifier attribute: value`), with the
  head's answer about the two logins as person and team lines, and a model of them
  (`type attribute: text`, or a type, a relationship type);
- checks the records against the model: 5 problems (four values that name no person or team, one
  attribute the model lacks); merges the two spellings by editing two values to identifiers; checks
  again: 3; counts the `responsible` values again: 4, then 3, one for each person or role;
- weighs the fact the model has no type for, `clean_orders drops: orders with no customer id`, the
  rule Chapter 2 found behind Thursday: refuse it, or add `dataset drops: text` (2 problems left)
  and accept it as text no check can test;
- questions "Each asset has one owner." (below).

It introduces the plan's four terms in the section "What the records describe", which the term test
holds; it uses none of Chapter 5's (graph, node, edge, traversal) and says "relationship type" and
"reference" for what Chapter 5 will draw.

## What was built for it

- `notebook/shop/records.py`: `typed_records` (Chapter 4's notation), `model` (types, attributes
  and what each value is: `text` or type names joined by `or`), `Model.check(records)` (lines the
  model cannot read; record lines with an unknown type or attribute; values that should name an
  entity of a type and name none the records describe; a model line naming an undefined type), and
  `owners(week, records)`: every asset on the platform with its `responsible` values and three
  readings of "one owner" (exactly one value; one person; one team, directly or through the
  person's team).
- Tests in `notebook/tests/test_engine.py` ("TheRecords") and the chapter's words in
  `notebook/tests/test_words.py` ("TheWordsOfChapter4"), which read the records and the model from
  the chapter's own source.

## Figures

### `platform`

- **Role:** reference
- **Serves:** the seven assets the list must cover, in their systems; the requirement's last cell
  lists exactly those seven.
- **Why now:** "Each asset" needs the assets in view.

### `the-count`

- **Role:** experiment
- **Objective:** the reader discovers that records that name owners as text count spellings, not
  people, and that the records alone cannot say whether two spellings are one person.
- **Known before:** the records cell's lines, the list of `responsible` lines, and Chapter 3's two
  facts about Jo Marsh and `j.marsh`.
- **Driving question:** will the count of different `responsible` values be the number of people
  responsible, more, fewer, or can you not tell yet?
- **The action:** write the expectation and how it was decided, then read the count.
- **Why the action:** a reader who counts people ("three: me, Jo, Sam") commits to the belief the
  query then contradicts.
- **Evidence:** 4 values.
- **Consequence:** a reader who said three learns the query counted text; one who said four has
  already seen the spellings, and is asked whether they are one person. The evidence for "yes" is
  indirect until the staff list.
- **Predictable:** yes, from the list just above.
- **Gives nothing away:** the list shows the values, which is the evidence the reader reasons from;
  nothing above says how many people there are.
- **Not knowing:** "I can't tell whether Jo Marsh and `j.marsh` are one person" is right until the
  staff list, and the prose says so.
- **Next question:** what must the records hold for a count to count people?
- **An experiment:** the reader commits, runs, and the output answers.

### `the-model-check` and the merge

- **Role:** experiment
- **Objective:** the reader finds that a model makes a reference checkable (a value must name a
  known entity), makes the merge a matter of identifiers, and refuses facts it has no attribute for.
- **Known before:** the typed records, the model, and the check's rules, stated above the cell.
- **Driving question:** which lines does the model reject, and why?
- **The action:** run the check; change two values to identifiers in the records cell; press
  **Run below**; read the check again.
- **Why the action:** the merge is the reader's edit, and the change from 5 to 3 problems is its
  evidence.
- **Evidence:** 5 problems, then 3: the data engineer twice, and `drops`; the count of
  `responsible` values, 4, then 3.
- **Consequence:** the reader sees one owner for `daily_sales` because two lines now hold one
  identifier, and the spelling kept as the person's `name`.
- **Predictable:** the first result is, once the rules are read.
- **Gives nothing away:** the check's output is the evidence; the prose after it groups it.
- **Not knowing:** "the data engineer" is left open, honestly, for the requirement.
- **Next question:** what should the model do with `drops`, and what does "one owner" mean?
- **An experiment:** the reader acts and the check answers.

### `owners`

- **Role:** experiment, completing the requirement exercise
- **Objective:** the reader sees which assets meet which reading of "one owner", that `orders.jsonl`
  and `customers.jsonl` meet none, and that a choice of theirs (the data engineer a team or a
  person) moves the counts.
- **Known before:** the reader's own answer, written first; then the three readings, each named by
  its column, and what each needs.
- **Driving question:** which reading would you require, and what does the shop's list meet?
- **The action:** write the choice, then run the cell.
- **Why the action:** the choice is the reader's, as it would be at work; the table answers only
  what the records meet.
- **Evidence:** 7 assets: with the data engineer a team, one owner 5, one person 3, one team 5;
  with the data engineer a person (the reader's choice, one line in the cell), 5, 5 and 3.
- **Consequence:** no reading is marked wrong; the list must say which reading it meets.
- **Predictable:** mostly, from the records above.
- **Gives nothing away:** the readings are stated as needs, not verdicts; the choice comes first.
- **Not knowing:** "the requirement does not say which" is the conclusion.
- **Next question:** the references now lead from one entity to the next: Chapter 5.
- **An experiment:** the reader commits and runs.

The cell applies the two merge edits itself (idempotently), so its output is the same whether or not
the reader made them, and makes "the data engineer" a team or a person, `data_engineering`, by the
line `the_data_engineer = "team"`, which the reader may change.

## Requirements

The chapter questions "Each asset has one owner.", the plan's candidate, with the `owners` cell.

1. **What it says:** each asset has one owner.
2. **What it might mean:** one person to ask; one team that answers for it; one owner however the
   records spell the owner's name.
3. **What each needs:** `responsible` naming a person, one value per asset; a team per asset,
   directly or through the person; identifiers, so two spellings count once.
4. **What the records hold:** after the merge, one value for every asset except `orders.jsonl` and
   `customers.jsonl`, which have no `responsible` line; with the data engineer a team, a person for
   three assets and a team for five; as a person, five and three.
5. **Whether it is met:** for no reading on all 7 assets. As written, 5 of 7; the others depend on
   the reader's choice for the data engineer. The head of the shop did not say which was meant.

The reader writes what they would send and what "one owner" means to them before the readings
appear; the readings name the columns of the table.

The reader writes their choice first; no reading is marked wrong. Chapter 2's owner (an account in
the warehouse) is not among the readings here: the records are the reader's, and Chapter 21
returns to owners that conflict across systems.

## Originality

The obvious examples for a metadata model are an entity-relationship diagram of customers and
orders, as database textbooks draw it, and the entity, aspect or type definitions of metadata
products (DataHub's entities and aspects, Apache Atlas's type definitions, OpenMetadata's JSON
schemas). This chapter has no diagram and copies no product's model: the reader arrives at types,
attributes and identifiers from one person's name spelled two ways in their own records, in two
line notations of the course's own, and the model is checked by a small function the reader runs.
The relationship between a dataset and a person is one attribute line, `dataset responsible:
person or team`. The staff list, the logins and the teams are invented for the course.

## What the prose process caught

Two briefs (`docs/notes/chapter-04/briefs/` DA and DB, drafts under `drafts/`); the check messages
came from brief CC and the warning from CD (Chapter 3's notes).

| Draft | Dropped, restored with the fewest words | Wrong, sent back |
| --- | --- | --- |
| DA | | slot G said the records already use `j.marsh` every time, which is the opposite of the problem the section answers |
| DB | | slot B's first sentence dropped who set the requirement and added a claim; the second draft read as if the requirement had a head; the third was right |

## Measured

12 October 2026, as Chapter 3 (`docs/notes/notebook-prototype.md`, "Chapters 3 and 4"): about 13
MB on its own; 0.32 MB from Chapter 3's link in a new tab after Chapter 3 had run; Run all 8.9 to
10.5 s; peak memory 400 to 406 MB.

## The review, 12 October 2026

A reader on another model read the chapter as built and after the edit, as a learner who had done
Chapters 1 to 3 (`docs/notes/chapter-04/review/`: 17 findings, 8 marked blocking), and an
independent sceptic attacked each (`verdicts.md`): one rejected (the staff list's size), several
trimmed. Code first, then brief DC (Haiku, checked for facts: nothing dropped, nothing wrong), then
the messages and the first cell's notes of brief CF. What changed:

- The first cell says where each of its lines comes from (findings 3, 4): the reader's own record
  of `daily_sales` from Chapter 3, three lines from the head's message, and one line from the
  orders Chapter 2 found missing, `clean_orders drops: orders with no customer id`, which is all
  Chapter 2 showed; the quantity rule, which the week never tests, is gone from it.
- The page says that the head's "owner" is counted as the `responsible` lines, and that the
  warehouse's account answers a different question (6).
- The first expectation asks whether the count of values will be the number of people, more, fewer,
  or not yet known (7); a new count after the merge gives 3 (14). Cells are named by their first
  line, and the prose under the check says "before your change" (11).
- *Records* is the set, a *line* is one line, everywhere, and the check's column is `text` (8).
- The data engineer is the reader's choice, team or person, with both results stated (5); the
  reader is not on the head's list because they started today.
- The requirement: the reader commits first; the readings follow, each named by its column; "no
  reading holds for all 7 assets"; the two files are named, with no claim about the export (1, 2,
  12).
- Smaller: the objectives say what the reader does (9); the reader can add `dataset drops: text`
  and see 2 problems (10); the dashboard's type, the assets as entities, and columns as entities
  (13); the identifier's sentence (15); the forward reference to Chapter 6 for `drops` is gone, and
  the repetitions are cut (16).

## Known gaps

- The warning's run time, "9 to 11 seconds" from the local build, became "9 to 12 seconds" once the
  published page was measured (11.4 to 11.8 s): a number changed to the measurement, not a sentence
  rewritten.

- Chapter 4's notebook ends the course's written chapters for now: its links offer no next chapter.
- The reader's choice of reading is free text, kept by **Save**.
