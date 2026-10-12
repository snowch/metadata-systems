# Chapter 12: Identity

A working note. Written on 12 October 2026 with Chapters 10, 11 and 13, as a notebook
(`notebook/chapter_12.py`).

## What the chapter does

On Monday at 10:20 a developer runs `build_daily_sales` in a development copy of the warehouse
(the `dev` change). The reader:

- meets **environment**, writes which programs the graph will show writing production's
  `daily_sales`, and finds two: Chapter 9's rule for names gave the developer's names production's
  database, and the development run is now the last to write production's table;
- meets **identity**, writes for six pairs of names whether each names the same asset, asks each
  store what each name refers to, and meets **qualified name**: case matters to object storage and
  not to the warehouse; an unqualified name means a table only by a connection's defaults;
- tests each pair five ways (text, object, rows, environment, version) and finds them disagree: a
  view has its table's rows and is another object; two versions are one object with different
  rows;
- questions "The same table must have one identity." (below);
- gives ingestion a database for each producer, by removing a `# ` and pressing **Run below**, and
  sees the two runs write two tables.

## What was built for it

- `notebook/shop/identity.py`: `resolve` (by each store's rules: the warehouse ignores case and
  fills in production's defaults; object storage reads keys exactly), `compare` and `references`.
- The `dev` change: a database `shop_dev` in the warehouse, the development run, the developer's
  runner as a producer (`openlineage.dev_events`, names without the database, jobs in the
  namespace `dev`), and the supplier's test export `Orders.jsonl`. The `view` change: Jo Marsh's
  view `sales_by_day`.
- `ingest.normalise(events, databases)`: a database for each producer's names that leave it out.
- `Edges.of` finds a dataset's edges by the end of its name, as well as a job's.
- Object storage keeps each version's text (`version_text`).

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the shop's systems as Chapter 7 left them; the development database comes later, in prose.
- **Why now:** every chapter opens with the map.

### `development-run`

- **Role:** experiment
- **Objective:** the reader learns that a rule that fills in what a name leaves out can join two
  environments' tables, and that the graph then misstates which run last wrote production's table.
- **Known before:** Chapter 9's rule for names, stated there and here; the developer's names.
- **Driving question:** which programs will the graph show writing production's `daily_sales`?
- **The action:** write the expectation; read the edges.
- **Why the action:** a reader who expects the two databases to stay apart commits to that.
- **Evidence:** `shop/build_daily_sales` in 7 runs, `dev/build_daily_sales` in 1, the last.
- **Consequence:** the reader sees a rule from Chapter 9 fail on the case Chapter 9 named as its limit: two databases with tables of the same name.
- **Predictable:** yes, from Chapter 9's rule.
- **Gives nothing away:** the prose says what the runner names, not where ingestion puts it.
- **Not knowing:** a fair answer.
- **Next question:** when are two names the same asset?
- **An experiment:** commit, run, compare.

### `six-pairs`

- **Role:** experiment
- **Objective:** the reader learns that "the same asset" has several tests that disagree, and that a
  name is read by its store's rules.
- **Known before:** where each name is used, listed with the pairs.
- **Driving question:** for each pair, do the two names refer to the same asset?
- **The action:** write yes, no or cannot tell; read what each name refers to; read the five tests.
- **Why the action:** each answer is a belief about what "same" means.
- **Evidence:** the stores' answers; the five tests per pair.
- **Consequence:** a reader who answered by text learns case and defaults; one who answered by rows
  learns the view is another object.
- **Predictable:** in part.
- **Gives nothing away:** the pairs say where each name comes from, not what it names.
- **Not knowing:** the right answer for several pairs until "same" is defined, and the requirement
  section says so.
- **Next question:** which "same" does the requirement mean?
- **An experiment:** commit, run, compare.

### `a-database-for-each-producer`

- **Role:** experiment
- **Objective:** the reader learns that the fix can be made at ingestion, per producer, or at the
  source, with qualified names.
- **Known before:** the development run's edges.
- **Driving question:** does a database for each producer keep the two tables apart?
- **The action:** remove a `# `, press **Run below**, read the edges.
- **Why the action:** the reader changes the rule that failed.
- **Evidence:** `dev/build_daily_sales` writes `shop_dev.analytics.daily_sales`.
- **Consequence:** the rule now has to list every producer.
- **Predictable:** yes.
- **Gives nothing away:** the prose names the line, not the result.
- **Not knowing:** not the right answer.
- **Next question:** whether the dashboard is up to date (Chapter 13).
- **An experiment:** change, run again, compare.

## Requirements

The chapter questions "The same table must have one identity.", the plan's candidate, after the
pairs are tested.

1. **What it says:** one identity for the same table.
2. **What it might mean:** the same name, qualified and read by its store's rules; the same rows;
   the same environment; the same version.
3. **What each needs:** qualified names and each store's case rule; a comparison of contents; which
   environment holds each asset; versions, which the warehouse does not keep for a table.
4. **What the shop records:** ingestion joins on namespace and name after normalising, comparing
   names exactly.
5. **Whether it is met:** the first reading in part: ingestion compares names exactly, so it would
   keep pair 1 apart, and it gave the developer's unqualified name production's database, joining
   two tables no reading joins. The other three are not met: the graph compares no rows, records no
   environment and keeps no versions of a table. The requirement does not say which "same" it
   means.

## Originality

The obvious examples are a catalogue product's "qualified name" scheme with its own separators, a
master-data or record-linkage tutorial matching customers by fuzzy name, and the OpenLineage naming
page's table of data stores. This chapter's pairs are all the shop's own: names in its events, its
code, a person's query, a view, a test file and an object's versions, each resolved by the shop's
stores and tested five ways; its failure is the shop's own Chapter 9 rule meeting a development
database. OpenLineage's naming page and symlinks facet are named in the reality note, from their
documentation.

## What the prose process caught

Brief RA, draft under `drafts/`. Every fact was right. Edits: the objective quoted the requirement,
which would have used "identity" before its section; "the shop's requirement starts with" became
the head of the shop's requirement; the text cell lost its backticks; two "next cell" sentences
pointed at different cells, and their order was swapped so each points at the cell after it. The
brief itself was corrected before it went out: *schema* in this chapter means a group of tables, as
Chapter 8 used it, and nowhere a dataset's columns. The agent reported one stray tool call, which
was rejected and sent nothing.

## The review

A reviewer on another model read the chapter as a learner (`review/findings.md`, 23 findings) and an
independent sceptic attacked each (`review/verdicts.md`). Acted on: the requirement no longer says
ingestion's rule joined pair 3; it says ingestion gave the developer's unqualified name production's
database, pair 2's mechanism with the wrong default (1); every reading has a verdict against what
the graph holds (2); the requirement now comes before the five tests, so their headings do not
prime the reader (3); the environment test is said to come from the database's name (4); pairs 3
and 4 are described by where their names come from (5); after the tests, "same asset?" is said to
depend on the test, with pairs 4 and 6 (6, 16); Chapter 9's rule is restated above the prediction
(7); the reader decides before the last edit (8); only a producer whose names mean another database
needs a line, and a producer is code, not an environment (9); the development tables are not called
copies, and an environment is "a set" (10); *schema* is defined where it appears (11); "same rows"
is defined for an object; the version test is empty across two objects; `@` is explained (19); the
closing is about this chapter (17); the invented list names Jo Marsh's query in capitals (20); the
symlinks sentence follows the source (21); the plan's row matches what is built (22). Rejected:
merging the two tables (13), reordering the commentary (15), defining identity later (18), and
extending the map (12, the notes corrected instead). Brief RB drafted the new paragraphs; every fact
was right.

## Measured

See `docs/notes/notebook-prototype.md`, "Chapters 10 to 13".

12 October 2026, the published page after the review (opened alone, desktop and phone): Run all 10.2 s on a desktop, 10.6 and 10.8 s as a phone; peak memory 402 MB, and 398 and
398 MB.

## Known gaps

- Chapter 22 takes names across systems (a transformation tool's model names, the dashboard's
  datasets) and rules for merging them.
- The warehouse keeps no versions of a table, so the version test is empty for tables.
