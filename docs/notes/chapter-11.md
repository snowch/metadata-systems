# Chapter 11: Schema evolution

A working note. Written on 12 October 2026 with Chapters 10, 12 and 13, as a notebook
(`notebook/chapter_11.py`).

## What the chapter does

The checkout's supplier plans one of three changes to `orders.jsonl`: a new field (`added`), a
renamed one (`renamed`, `quantity` to `qty`), or customer ids written as text (`retyped`). The
reader:

- writes, for each change, whether it will change what `daily_sales` holds;
- meets the shop's record of a dataset's schema at every write, and **schema evolution**: 2
  versions of `orders.jsonl` under `renamed`, compared by name, so the rename is a removal and an
  addition; under every change the catalogue's `clean_orders` keeps 1 version, though under
  `retyped` all 44 of its customer ids are text in a column declared `INTEGER`;
- counts what three readers get (the rows of `daily_sales`, the dashboard's days, Jo Marsh's own
  query): `added` 7, 7, 7; `renamed` 5, 5, 0; `retyped` 7, 7, 0; meets **breaking change**;
- lists, by Chapter 10's column lineage, the program that reads `quantity`, changes the cell to
  `customer_id`, presses **Run below**, and finds the same program, which the new type did not
  break; Jo Marsh's query, which it did, is in no record;
- questions "Warn us of breaking changes." (below).

## What was built for it

- `notebook/shop/schemas.py`: `versions`, `schema`, `diff` (by name), `diffs`, `readers` (by column
  lineage), `compare` and `compare_all`, and `JO_QUERY`.
- `Execution.schema`, recorded at every write: a file's fields with the JSON types of their values
  (`platform.file_schema`), a table's declared columns from the catalogue.
- The changes `added`, `renamed` and `retyped` (`week.supplier_changes`), from the export of the
  night that writes Saturday's row.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the assets the supplier's file feeds.
- **Why now:** every chapter opens with the map.

### `three-changes`

- **Role:** experiment (with `what-each-reader-gets`, which answers it)
- **Objective:** the reader learns that whether a change to a file breaks a table depends on how
  each program reads it, and that the change that looks smallest (a new type) is the one that
  breaks a reader no record names.
- **Known before:** `build_clean_orders`'s code (Chapter 6), its filter and `DISTINCT`; Chapter 10's
  column lineage.
- **Driving question:** does each change alter what `daily_sales` holds on Monday?
- **The action:** write a guess for each; read the versions and the counts.
- **Why the action:** each guess is a belief about how the programs read the file.
- **Evidence:** 7, 5, 7 rows; the dashboard's days; Jo Marsh's query at 7, 0, 0.
- **Consequence:** a reader who expected the rename to fail loudly learns that it emptied tables in
  silence; one who expected the new type to break `daily_sales` learns it broke a reader outside
  the shop's records.
- **Predictable:** in part, from the filter `quantity > 0`.
- **Gives nothing away:** the changes are described, not their effects; the versions above the
  counts show names and types, not rows.
- **Not knowing:** a fair answer for the new type before the warehouse's behaviour is known.
- **Next question:** who reads each column?
- **An experiment:** commit, run, compare.

### `versions` and `diff`

- **Role:** inspect
- **Serves:** the record the shop keeps, and why a rename shows as two changes.
- **Why now:** the term is given against the versions.

### `value-types`

- **Role:** inspect
- **Serves:** the catalogue's declared type against the values the warehouse holds.
- **Why now:** it explains why the table's schema record did not change.

### `who-reads-the-column`

- **Role:** experiment
- **Objective:** the reader learns that column lineage names the readers of a column, not whether a
  change breaks them, and names no reader outside the shop's code.
- **Known before:** the counts above.
- **Driving question:** which programs would a warning about each column reach?
- **The action:** change `quantity` to `customer_id`, press **Run below**, compare.
- **Why the action:** the same answer for two columns, one of which broke nothing, is the point.
- **Evidence:** `build_clean_orders`, in the same three ways, for both.
- **Consequence:** a warning by lineage over-warns for one reader and misses another.
- **Predictable:** yes.
- **Gives nothing away:** the prose names the change to make, not the answer.
- **Not knowing:** not the right answer.
- **Next question:** whom should the shop warn?
- **An experiment:** change, run again, compare.

## Requirements

The chapter questions "Warn us of breaking changes.", the plan's candidate, after the counts.

1. **What it says:** warn of breaking changes.
2. **What it might mean:** breaking for a program that reads the dataset; for the dashboard; for
   somebody's own query.
3. **What each needs:** column lineage of the programs and the schema's versions; lineage downstream
   to the dashboard; a record of the queries people run.
4. **What the shop records:** schema versions at every write, column lineage of the code it has,
   lineage to the dashboard; no record of Jo Marsh's query.
5. **Whether it is met:** for programs and the dashboard, a warning can be raised, and over-warns
   for the new type; for somebody's own query, not met. The requirement does not say for whom.

## Originality

The obvious examples are a schema registry's tutorial on which changes are compatible, and a
table format's documentation of adding and renaming a column. This chapter has no registry and no compatibility mode: the shop's own records, compared by
name, against three changes from a supplier, and the readers they reach, one of them a person's
query in a spreadsheet. Iceberg's column ids are named in the model-versus-reality note as one
answer, from its specification.

## What the prose process caught

Brief QA, draft under `drafts/`. Every fact was right. Edits: the fourth objective quoted the
requirement, which would have used "breaking change" before its section, and now names it without
the term; the text cell put its question after the change names, and the question came first and
was wrapped; the draft set sentences as bullet points, which became paragraphs; "the requirement,
as the shop states it" became the head of the shop's; the closing's labels went. The agent reported
one stray tool call, which failed and changed nothing.

## The review

A reviewer on another model read the chapter as a learner (`review/findings.md`) and an
independent sceptic attacked each finding (`review/verdicts.md`). Acted on: the third change breaks
Jo Marsh's query through its new values, `C101`; the shop's warehouse would store `"101"` as a
number, now stated at the value-type cell and pinned by a test (B1); the verdicts are per reading
and per change, "met" is defined, the dashboard's warning for `retyped` is shown to have no break
behind it, and the reader now commits to what the shop would have to record (B2); a breaking change
is a change to a dataset's structure or format (B3); the changes are alternative weeks, from the
export early on Sunday 13 (S1); the reader decides before the `customer_id` run, and the step to
`daily_sales` cites Chapter 10 (S2); object storage keeps the old files, and "schema version" is
used throughout (S3); Chapters 2 and 3's rename question is named (S4); `clean_orders` is said to
be empty, and why (S5); the objective says what the reader does (S7); the closing ties to the
column rename (S10); restatements and "the supplier's notice" went (C3, C4); the schema facet's
type is optional (C1). Rejected: a computed table of warnings, a compatibility sense of
"breaking" with no source, running `qty`, and renaming the reader rows. Brief QB drafted the new
paragraphs; every fact was right. The drafting agent tried one message, which was refused.

## Measured

See `docs/notes/notebook-prototype.md`, "Chapters 10 to 13".

12 October 2026, the published page after the review (opened alone, desktop and phone): Run all 11.6 s on a desktop, 11.4 s as a phone; peak memory 405 MB and 399 MB.

## Known gaps

- Versions are compared by name; the shop keeps no column ids.
- A file's types are JSON's, read from its values; a CSV file's are all text.
