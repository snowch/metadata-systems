# Chapter 1: The shop and its platform

A working note. The chapter began on 10 October 2026 as the first of two notebooks the author asked
for when Chapter 2, then Chapter 1, was split into a tour of the shop and an investigation; on 11
October the author made it a chapter of its own, since "part" had come to name both the course's
eight parts and half a chapter (`docs/plan.md`, "11 October 2026: two chapters where there was
one").

## What the chapter does

The chapter is a notebook (`notebook/chapter_01.py`, built into the site as `chapter_01.ipynb`),
which the front page's title for the chapter and its start button open. It opens with the head of
the shop's one line, "Thursday's revenue looks wrong", and says why you look round first; then the
three systems, the files, the warehouse's three tables, the dashboard and the nights, and what the
tour could not show. Its last section, "Your guesses about the warehouse tables", asks the learner
to write down, for each table, which asset they think it is made from and why, with nothing to
grade: Chapter 2 asks what such evidence can establish. Like Chapter 2, it has no prediction,
experiment or challenge: the author's decision of 10 October 2026 (`docs/plan.md`, "Chapter 1 as an
essay") holds for the tour it came from. It introduces *asset*; Chapter 2 introduces *metadata*.

From 11 October 2026 until the same evening the chapter was also a page of the course
(`content/lessons/shop-and-platform.ts`), whose opening, map lead and sentence giving the word
"asset" had moved from Chapter 2's page; its other words were Haiku's drafts of brief AV
(`docs/notes/chapter-01/briefs/`; the files' and the task's titles went back once, for taking the
titles of other sections), with its first section's title from brief AW. When the notebooks became
the only version, the page's last section, the written guesses, moved into the notebook with its
words unchanged. The notebook's other words were drafted from briefs AO to AT in
`docs/notes/chapter-02/briefs/round-16/`, written when the two chapters were one. Its facts come
from the Python engine (`notebook/shop`), whose files are JSON Lines and CSV and whose amounts are
in pence, and `notebook/tests/` pins them.

## Figures

Every figure of the chapter, in its order. Each is a diagram or a figure of the shop's data, with a
caption and nothing else (`CLAUDE.md`, "No lab on the page"); none takes a commitment. The blocks
were written for the page's figures. In the notebook, `platform`, `week` and `dashboard` are drawn
when the site is built, into Markdown cells (`notebook/shop/figures.py`), and show before anything
runs; `products`, `customers`, `orders` and `tables` are
cells whose code the learner can read and run, and which print the files' first lines and the
tables' rows: the same questions, served by output the learner produces.

### `platform`

- **Kind:** a diagram
- **Serves:** every question in the tour that needs to know which systems hold which assets, in
  the order data moves through them. It draws no asset made from another, since the chapter's
  task asks the learner to guess which, and it counts what it shows (3 files + 3 tables + 1
  dashboard = 7 assets); the sentence under it gives the word "asset".
- **Why now:** the head of the shop's line needs the platform under it, and the rest of the tour
  goes through the systems in this order.

### `products`

- **Kind:** a figure of the shop's data
- **Serves:** the learner reads the catalogue as the file holds it: its columns and its 8 rows.
- **Why now:** the files are where the night's work starts, and the catalogue is the smallest.

### `customers`

- **Kind:** a figure of the shop's data
- **Serves:** the learner reads the customers as the file holds them: their columns and the first
  8 of 10 rows.
- **Why now:** the orders that follow name customers by `customer_id`.

### `orders`

- **Kind:** a figure of the shop's data
- **Serves:** the learner reads the orders as the checkout sent them: their columns, `status` among
  them, and the first 8 of 48 rows.
- **Why now:** Thursday's revenue is a sum of orders, and Chapter 2 starts from this file.

### `tables`

- **Kind:** a figure of the shop's data
- **Serves:** the learner reads the warehouse's three tables, and sees two that share their columns
  with a file, which the task then asks about.
- **Why now:** after the files, in the order data moves.

### `dashboard`

- **Kind:** a figure of the shop's data
- **Serves:** the learner sees the dashboard the head of the shop read: revenue per day, 7 to 13
  September.
- **Why now:** the last system, and the place the line came from.

### `week`

- **Kind:** a diagram
- **Serves:** the nights: when each night's work happened after each day of orders, and where the
  learner's morning falls; the prose gives the last night's times.
- **Why now:** the opening said you need to know what happens on the platform each night.

## Requirements

None. The chapter tours what the platform holds and questions no requirement; Chapter 2 questions
its first, "Every table must have an owner".

## Originality

The obvious example for a first look at a data platform is a ready-made sample project, such as
dbt's jaffle shop, browsed through its generated documentation. Here the learner is handed an
undocumented platform of an invented bicycle-parts shop, with one line from its head in front of
the tour, and reads the shop's own files and tables with code they run; the shop, its data and its
programs are invented for the course.

## Boxes for the page, and printed lines kept whole, 11 October 2026

The author asked whether boxes should break up the text, and whether printed output should wrap.
The paragraph on running and saving the page left the opening story for a box of its own under
the warning, as three steps: Haiku's draft of brief AZ (`docs/notes/chapter-01/briefs/`), which
carried all seven facts and the wording the tests hold, and needed no correction. Chapter 2's
one line on Run all moved, unchanged, into the same kind of box. The warning is a box too, in the
warning's colour; the hidden setup cells follow both boxes. What a cell prints now keeps its own
lines: JupyterLab wrapped `customers.jsonl` inside words and dates (`"countr` / `y"`, `"2` /
`026-05-19"`), so the file no longer showed one record per line. A long line now scrolls inside its
box, with a shadow at the edge it continues past. The smoke test checks both boxes and that the
printed file draws ten lines for its ten records, with the page never scrolling sideways.

