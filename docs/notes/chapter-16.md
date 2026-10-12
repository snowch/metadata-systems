# Chapter 16: Impact analysis

A working note. Written on 12 October 2026 with Chapters 14, 15 and 17, as a notebook
(`notebook/chapter_16.py`).

## What the chapter does

The shop's developer wants to rename `customer_id` in `clean_orders` to `customer`, and the head of
the shop asks what breaks. The reader:

- writes which of four readers they expect to break, and how;
- follows the graph the events make downstream of `clean_orders` (two programs at step 1, the
  dashboard at step 2) and meets **impact analysis**; then column lineage, which lists one column, the
  copy's; changes the column to `status` and sees the filter reach `daily_sales`;
- reads what each reader got, without the rename and with it: `daily_sales` and the dashboard
  unchanged, the copy's header renamed with no error, Jo Marsh's query failing;
- in the week with `withdrawn`, follows the graph from a deleted return's object (one step, to
  `returns`), then reads what the shop made from it: Sunday's row, still 1200 pence less, and the
  dashboard's £85.75;
- questions "Tell us what breaks if `customer_id` is renamed." against two readings: fails, or keeps
  running with a different answer.

## What was built for it

- `notebook/shop/impact.py`: `downstream` (the events' graph), `downstream_columns` (column lineage
  forward), `readers` (four readers in two weeks) and `made_from`.
- The `customer` and `withdrawn` changes; `Warehouse.rename_column`.

## A decision

The plan's experiment renames `orders.customer_id`. The chapter renames the column in `clean_orders`
instead: renaming the file's field is Chapter 11's `renamed` change over again, where a missing
field empties every reader. A renamed table column instead leaves the shop's own programs untouched,
changes the copy silently and makes Jo Marsh's query fail, so the lineage by datasets lists too
much, the lineage by columns lists the copy, and neither lists the one reader that failed.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** where `clean_orders` and the returns sit.
- **Why now:** every chapter opens with the map.

### `rename`

- **Role:** experiment (with the two lineage cells and `readers`, which answer it)
- **Objective:** the reader discovers that an impact analysis lists only what its lineage holds: by
  datasets too much, by columns the shop's own readers, and never a reader outside the records.
- **Known before:** the three readers of `clean_orders`, from Chapters 6, 9 and 11; Chapter 10's
  columns of `build_daily_sales`.
- **Driving question:** which readers break, and how?
- **The action:** write the expectation; read the two lineages; change the column to `status`;
  read what each reader got.
- **Why the action:** setting the lineages' answers beside what happened tells them apart.
- **Evidence:** two programs and the dashboard downstream; one column; unchanged, unchanged, renamed,
  failed.
- **Consequence:** a reader who trusted the graph learns what it missed and what it overstated.
- **Predictable:** partly; the failure of Jo Marsh's query follows from Chapter 11.
- **Gives nothing away:** the prompt lists the readers without results.
- **Not knowing:** reasonable for the copy, whose readers are unknown.
- **Next question:** what does impact analysis miss when the change is to data, not to a schema?
- **An experiment:** commit, ask the graph, change, compare.

### `withdrawn`

- **Role:** experiment
- **Objective:** the reader discovers that a deleted record leaves a wrong total that nothing reports,
  and that the graph of events follows it only as far as the events name.
- **Known before:** Chapter 10's hidden read through `returned_quantity`; Chapter 15's rebuilt
  `returns`.
- **Driving question:** what did the shop make from `r-206`?
- **The action:** decide what the graph will list; read it; read what was made from the return.
- **Why the action:** the two answers differ, and the second explains the dashboard.
- **Evidence:** one step to `returns`; Sunday's row of 8575 pence and £85.75, still there.
- **Consequence:** "remove everything made from it" needs lineage the events do not carry.
- **Predictable:** yes, from Chapter 10.
- **Gives nothing away:** the question is asked before either cell.
- **Not knowing:** a fair answer before the graph is read.
- **Next question:** how would you find where a wrong total went wrong?
- **An experiment:** decide, run, compare.

## Requirements

The chapter questions "Tell us what breaks if `customer_id` is renamed.", the plan's candidate.

1. **What it says:** tell us what breaks.
2. **What it might mean:** what fails with an error; what keeps running and gives a different answer.
3. **What each needs:** every reader, in the records or not; each column's readers and what each does
   with it.
4. **What the shop records:** the events' graph by datasets; column lineage of the code it has.
5. **Whether it is met:** "fails", not: Jo Marsh's query is in no record. "Different answer", for the
   copy only, with two readers listed that did not change. The requirement does not say which.

The plan's second candidate, "When a return is deleted, remove everything made from it", is not
questioned on the page: the withdrawn return is evidence for the closing, and a second requirement
would widen the chapter.

## Originality

The obvious examples are a metadata catalogue's impact view of a dropped column on an orders table,
and a transformation tool's selector for every model downstream of a changed one. This chapter
renames a column of the shop's own table, sets two lineages' answers beside what four of the shop's
readers got, and follows a withdrawn return through a read that no event names.

## What the prose process caught

Brief VA, draft `drafts/V.md`. "From Sunday's night" named a night by a day, against the course's
rule; now "the night's work early on Sunday 13". The requirement's heading gained the backticks of
its name. "Neither the lineage nor the graph of events", which are one thing, became "Neither kind
of lineage". "Figure" for a number became "total".

## The review

A reviewer on another model read the chapter as built (`review/findings.md`); an independent
sceptic attacked each of the 20 findings (`review/verdicts.md`). Every number was right. Acted on,
through brief VB and draft `drafts/VB.md`:

- the requirement section no longer ends on the withdrawn return, a different change;
- "reader" is kept for programs and queries; the table compares what each produced (its column is
  now `output`, with `changed` second so a phone shows it);
- the cell is said to run the week again, not twice; the slogan "An impact analysis can list only
  what the lineage it follows holds" and the closing's untested claim are gone;
- "lineage by datasets" and "column lineage" throughout; "step" is defined;
- the last reality bullet says that `daily_sales` being appended to is the shop's design.

The notes' claim that the requirement section names the plan's second candidate was wrong, and is
corrected below. Rejected, with the sceptic: asking for the meaning of "breaks" earlier (the first
prediction commits the reader), moving "sends no events" (a Chapter 11 fact), a cell for the
withdrawn-return prediction (the course's decide-then-run pattern), and the map. Read whole again
after the fixes (`review/chapter_16-after-review.md`).

## Measured

Locally, 12 October 2026 (`docs/notes/notebook-prototype.md`, "Chapters 14 to 17"): from Chapter 15's link, 11 files, 0.32 MB, in a new tab; Run all 8.2 to 9.5 s; peak memory 394 to 402 MB alone, 612 MB with Chapter 15 open; no error output. Live: to be measured once published.

## Known gaps

- `made_from` finds the runs of `build_daily_sales` by their code calling `returned_quantity`: the
  engine's knowledge, which the page states.
