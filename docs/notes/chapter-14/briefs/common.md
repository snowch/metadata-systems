# What every brief for Chapters 14, 15, 16 and 17 shares

Write for a Jupyter notebook read by a data engineer; the reader is "you". Follow `docs/style.md`
and `AGENTS.md`: British English, short plain sentences, active voice, no em dashes, no filler, no
reassurance, no narration of what the chapter does or will do, no "in this chapter", nothing that
personifies a system, a program, an event, a cell, a check, a trace, a search or a graph (a trace
does not "know", "see", "think", "want" or "tell"; say what it lists, reads, records or finds). Say
the thing; do not build up to it. Keep every name in backticks exactly as written. A block of code
is a "cell". The buttons are **Run all**, **Run below** and **Save**, in bold; name no other control.
Never refer to Jo Marsh or any person as "he" or "she": repeat the name. Do not say a number, a
table or a record "says" anything; say what it shows, holds or lists.

Words the chapters already use, with one meaning each: *asset* (a file, a table or the dashboard);
*dataset* (a file or a table of rows); *job* (one of the four programs that run each night);
*program* (any of the shop's programs: the four jobs, the two functions of the returns desk, the
analyst's script); *function* (one of the returns desk's two programs, or a function in SQL such as
`returned_quantity`, which the brief names); *node*, *edge*, *graph*; *lineage*, *upstream*,
*downstream*; *run* (one time a program did its work), *event*; *OpenLineage*, *namespace*,
*producer*, *facet*; *ingestion*; *schema* (a dataset's columns and their types); *the catalogue*
(the warehouse's record of its tables and columns); *column lineage*; *schema evolution*; *breaking
change*; *environment*; *identity*; *qualified name*; *observation* (a fact recorded about a run
while it ran); *freshness*. Never "walk": say "follows".

The nights: each night's work runs in the early hours of the next day, so the work that read
Thursday's orders ran early on Friday 11 September. Name a night's work by the date it ran on. A
day is written as in the brief: "Thursday 10", "Friday 11". Money: the brief gives pence or pounds;
keep the unit it gives.

The reader has been told to press **Run all** first, so when they reach a cell for their expectation,
the cells below it have already run: ask them to write it "before you read on".

Never write: lab, engine, simulator, Jupyter, notebook (say "page" if needed), alias, index,
partition, retention, delivery, collector, precedence, idempotent, deduplication, event time,
arrival time, entity resolution. Each brief adds the terms its chapter must not use yet.

Never write a number in words where the brief gives it in figures, and never write one the brief
does not give.

Write the file once. Do not change it after you reply. Use only the Read and Write tools. Send no
messages and call no other tool.
