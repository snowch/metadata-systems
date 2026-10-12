# Chapter 23: Metadata at scale

A working note. Written on 12 October 2026 with Chapters 18 to 22 (`notebook/chapter_23.py`).

## What the chapter does

- measures the week: 11 assets, 6 jobs, 34 runs, 68 events, 67 run edges, 14 job edges, 7 days,
  1492 bytes an event; and how much of the job graph a traversal downstream from each dataset
  follows: 43% from `orders.jsonl`;
- predicts which question passes a budget of a million stored records first as the platform grows
  to ten million assets, each with the week's events per asset per day, kept 90 days; runs the
  projection: the questions that read every stored event pass it at 100,000 assets; partitioned by
  day, and downstream to the end, at ten million; with an **index**, or four steps, never; meets
  **index** and **partition**;
- deletes events older than three days on Monday morning (**retention**) and finds `r-201`'s row
  still in `returns` with no lineage; folds runs' edges into job edges first (**compaction**) and
  keeps it;
- questions "Keep lineage for 90 days."

## Figures

### `measured`

- **Role:** inspect

### `first-over`

- **Role:** experiment
- **Objective:** the reader discovers that the question that fails first is a simple one asked
  without the structure that serves it, not the deep traversal.
- **Known before:** the measured week; Chapter 9's graph; Chapter 13's latest run.
- **Driving question:** which question reads more than a million records first?
- **The action:** commit; run the projection.
- **Evidence:** the scans at 100,000.
- **Consequence:** a structure (index, partition, depth limit) is a precondition, not a tuning.
- **Predictable:** yes, with arithmetic.
- **Gives nothing away:** options are questions.
- **Not knowing:** fair.
- **Next question:** what does keeping less cost?

### `retention`

- **Role:** experiment
- **Evidence:** 68 events, 28 kept; r-201's edge gone; kept after compaction; the row in `returns`.

## Requirements

"Keep lineage for 90 days." Readings: 90 days of events; of edges; of whatever assets still in use
depend on. Compaction meets the second; the third needs retention by use, not by age.

## Originality

The obvious examples are a database's indexing tutorial and a time-series store's retention
policies. This chapter's numbers are the shop's own week projected by a model the chapter states;
its budget and depth limit are the shop's assumptions, labelled as such.
