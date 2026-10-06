# Brief I: Sections 4 and 5, and the inspector's answers

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/revision/I.md`.

## inspectorLead

Section 4's prose, above the inspector. Facts:

- Choose an asset from the list. The figure shows what its system records about it: its record,
  what storage says about eight questions, its columns and their types, and its rows.
- The figure asks every asset the same eight questions.
- Then a short list of things to try, as a Markdown list, each an open task that does not say
  what the learner will find:
  - pick one of the days whose totals differed in the prediction, and find the rows of
    `orders.parquet` that make the difference;
  - compare `orders.parquet` with `clean_orders`;
  - put the seven assets in the order they were last written, and say what that order suggests
    and what it cannot prove;
  - open `daily_sales` and read what storage says about each question.

Do not name a NULL, a repeated order or a cancelled order: the learner finds them.

## inspectorAfter

Shown under the inspector from the moment the page loads. One or two sentences. Facts: keep the
questions storage could not answer about `daily_sales`; the next section tries the data on them.
Do not summarise what storage records or why rows differ.

## construction

Section 5's prose, above the query builder. Facts:

- Storage does not say where `daily_sales` comes from. The data might.
- A query **rebuilds** an asset when it gives every row the asset has, with the same values. Put
  "rebuilds" in bold here, once: this is where the word is defined.
- A query that rebuilds `daily_sales` is a candidate for how it was made, not proof.
- Build one with the query builder below. The builder writes your choices as SQL and runs the
  query on Monday morning's data.

Do not list the builder's four choices: the task below the prose does.

## c1Task

The challenge's task, directly under the prose. Facts: build a query over another asset that
rebuilds `daily_sales`; choose an asset to read, which rows to keep, what to add up, and per what;
the tests compare your result with `daily_sales` one day at a time, and each day's row must be the
same as its row. Do not say which choices work.

## captions

Two captions, as a Markdown list with the key before a colon, plain text, one sentence each,
ending with a full stop:

- inspector: browse the seven assets and what storage records about each.
- c1: build a query that rebuilds daily_sales from another asset (no backticks in a caption).

## figure strings

The inspector's answers, one per kind of answer, as a Markdown list with the key before a colon.
Each is one sentence, plain text, ending with a full stop, saying what storage records and,
where the key says so, what it does not. Keep every `{slot}`:

- answered: storage records the last write, at `{time}`.
- columns (for a file or a table, under "How are its numbers worked out?"): storage records the
  column names and their types, not how the values were worked out.
- title (for the dashboard, under the same question): the reporting tool records the title,
  `{title}`, not how the values were worked out.
- owner-role (for a table, under "Who is responsible for it?"): the warehouse records the name
  `{role}` as the owner, which does not say who is responsible for the table.
- creator (for the dashboard, under the same question): the reporting tool records who created
  it, `{person}`, not who is responsible for it now.
- types (under "In what units are its numbers?"): storage records `{column}` as `{type}`, a number
  with no unit.
- time-only (under "Did last night's write work?"): storage records the last write, at `{time}`,
  not whether a write was due.
- nothing: storage records nothing that answers this.
- scrollCue (above a table wider than its box): tell the reader to scroll sideways to see every
  column.

Write the slots as `{time}`, `{title}`, `{role}`, `{person}`, `{column}` and `{type}`, without
backticks.
