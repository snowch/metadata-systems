# Chapter 27: Build the query layer

A working note. Written on 13 October 2026 with Chapters 24 to 26 and 28
(`notebook/chapter_27.py`).

## What the chapter does

Over Chapter 26's graph (the shop's version) for the week with the returns desk, `source` and
Chapter 13's failed night, the reader:

- writes `downstream(graph, asset)` as a traversal over `next_assets`; 1 of 3 as it stands, 3 of 3
  after; downstream of `orders.jsonl` are `clean_orders`, the copy, `daily_sales` and
  `sales_dashboard`;
- predicts whether the shop's query for stale assets (last written more than 24 hours before Monday
  09:00) lists `sales_dashboard`; it does not: written at 03:00:09 on Monday, showing Saturday 12;
- reads the shop's answers to upstream, failed runs and a column's reach;
- writes `owner(asset)`, which must say which of three meanings it gives, and questions "The query
  layer must answer who owns each asset."

## What was built for it

`notebook/shop/query.py`: `graph`, `next_assets`, `previous_assets`, `upstream`, `owners` (each
meaning from its own source), `check_downstream`, `check_owner`, `answers`. `week.py`: the failed
night reads the copy when `source` applies.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `one-step`

- **Role:** inspect
- **Serves:** what does `next_assets` give? One step from `orders.jsonl`.
- **Why now:** the traversal is built on it.

### `downstream-check`

- **Role:** experiment
- **Objective:** the reader builds a traversal and sees one step answer too little.
- **Known before:** Chapter 5's traversal; Chapter 14's impact.
- **Driving question:** what is downstream of each of three assets?
- **The action:** change `downstream`; press **Run below**.
- **Evidence:** 1 of 3, then 3 of 3.
- **Consequence:** the reader owns the traversal the shop's pages used.
- **Predictable:** yes.
- **Gives nothing away:** the page describes the loop, not the code.
- **Not knowing:** fair.
- **Next question:** what do the other questions find in the same week?

### `answers`

- **Role:** experiment (its prediction: is the dashboard stale?)
- **Objective:** the reader finds that a query by write time calls the dashboard recent while it
  shows Saturday.
- **Known before:** Chapter 13's two freshnesses and its failed night.
- **Driving question:** will the query list `sales_dashboard`?
- **The action:** write the prediction; read the four answers.
- **Evidence:** `daily_sales` and `returns`, not the dashboard.
- **Consequence:** a query answers the question it was written for.
- **Predictable:** yes, from Chapter 13.
- **Gives nothing away:** the cell asks yes or no.
- **Not knowing:** fair.
- **Next question:** whose owner does the query give?

### `owners` and `owner-check`

- **Role:** inspect, then experiment: the three meanings, and the reader's `owner`, which fails until
  it names its meaning.

## Requirements

The plan's: the query layer must answer who owns each asset (`docs/plan.md`, requirements table).
Readings: the account (Chapter 2), the person responsible (Chapter 4), the team (Chapter 21). The
check passes any, as long as the query names its meaning. The figure that questions it is the
free-text cell after the box.

## Originality

The obvious examples are a catalogue's search page and its API for lineage. This chapter's queries
are written over the shop's own graph, its failed night and its three sources of an owner, and the
check is the shop's.
