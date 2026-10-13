# What every brief for Chapters 24 to 28 shares

Write for a Jupyter notebook read by a data engineer; the reader is "you". Follow `docs/style.md`
and `AGENTS.md`: British English, short plain sentences, active voice, no em dashes, no filler, no
reassurance, no narration of what the chapter does or will do, no "in this chapter", nothing that
personifies a system, a program, an event, a cell, a check, a path, a rule or a graph (a rule does
not "know", "see", "think", "want", "choose" or "decide"; say what it takes, keeps, drops or lists).
Say the thing; do not build up to it. Keep every name in backticks exactly as written. A block of
code is a "cell". The buttons are **Run all**, **Run below** and **Save**, in bold; name no other
control. Never refer to Jo Marsh or any person as "he" or "she": repeat the name. Do not say a
number, a table or a record "says" anything; say what it shows, holds or lists.

Words the chapters already use, with one meaning each: *asset*, *dataset*, *job* (one of the four
programs that run each night), *program* (any of the shop's programs), *function* (one of the
returns desk's two programs: `record_return`, `remove_return`), *node*, *edge*, *graph*, *lineage*,
*upstream*, *downstream*, *run* (one time a program did its work), *event*, *OpenLineage*,
*namespace*, *producer*, *facet*, *ingestion*, *schema*, *the catalogue* (the warehouse's record of
its tables), *column lineage*, *environment*, *identity*, *qualified name*, *observation*,
*freshness*, *data quality*, *provenance*, *impact analysis*, *root cause*. The shop's **collector**
is the program that receives every event (Chapter 9). Never "walk": say "follows".

The nights: each night's work runs in the early hours of the next day, so the run of
`build_daily_sales` early on Thursday 10 writes Wednesday 9's row. Name a run by the day it ran on,
as the brief does. A day is written as in the brief: "Thursday 10". Times are UTC and written as the
brief gives them.

The reader has pressed **Run all** first, so when they reach a cell for their expectation, the cells
below it have already run: ask them to write it "before you read on".

Never write: lab, engine, simulator, Jupyter, notebook (say "page" if needed). Each brief lists the
terms its chapter introduces, in bold in the slot named and nowhere before it, and the terms it must
not use at all.

In the shop's metadata, the four jobs and the returns desk's two functions are each a job in
OpenLineage's sense, and the engine's `job` columns name all six. Where a sentence means all six,
say "program"; say "job" only for a column's name or for one of the four nightly jobs.

In Part VI the reader writes code: a short function, query or statement in a cell that starts with
a version that runs and gives a wrong answer. Call that cell's code what it is ("the loop", "the
query", "the function"), say what to change in plain words, and say what the check below it shows
before and after. Never call the starting code a stub, a skeleton or a template, and never give the
finished code in the prose: say what it must do. A "check" is the shop's cell that tests the
reader's code and prints one line per test.

Never write a number in words where the brief gives it in figures, and never write one the brief
does not give. Where the brief says a slot is a list, write a Markdown list.

Write the file once. Do not change it after you reply. Use only the Read and Write tools. Send no
messages and call no other tool. Write the draft as Markdown with one `## key` heading per slot, in
the brief's order (`## A`, `## B`, ...), and nothing under each heading but the text itself.
