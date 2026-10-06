## inspectorLead

Choose an asset from the list. The figure shows what storage records about it: its record, what storage says about eight questions, its columns and their types, and its rows.

The figure asks every asset the same eight questions.

Then try one of these:

- pick one of the days whose totals differed in the prediction, and find the rows of `orders.parquet` that make the difference;
- compare `orders.parquet` with `clean_orders`;
- put the seven assets in the order they were last written, and say what that order suggests and what it cannot prove;
- open `daily_sales` and read what storage says about each question.

## inspectorAfter

Storage cannot answer some of the questions about `daily_sales`. The next section tries the data on them.

## construction

Storage does not say where `daily_sales` comes from. The data might.

A query **rebuilds** an asset when it gives every row the asset has, with the same values. A query that rebuilds `daily_sales` is a candidate for how it was made, not proof.

Build one with the query builder below.

## c1Task

Build a query over another asset that rebuilds `daily_sales`. Choose an asset to read, which rows to keep, what to add up, and per what. The tests compare your result with `daily_sales` one day at a time, and each day's row must match its row.

## captions

- inspector: browse the seven assets and what storage records about each.
- c1: build a query that rebuilds daily_sales from another asset.

## figure strings

- answered: storage records the last write, at {time}.
- columns: storage records the column names and their types, not how the values were worked out.
- title: the reporting tool records the title, {title}, not how the values were worked out.
- owner-role: the warehouse records the name {role} as the owner, which does not say who is responsible for the table.
- creator: the reporting tool records who created it, {person}, not who is responsible for it now.
- types: storage records {column} as {type}, a number with no unit.
- time-only: storage records the last write, at {time}, not whether a write was due.
- nothing: storage records nothing that answers this.
- scrollCue: scroll sideways to see every column.
