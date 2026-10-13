# What every brief for Chapters 29 to 32 shares

Write for a Jupyter notebook read by a data engineer; the reader is "you". Follow `docs/style.md`
and `AGENTS.md`: British English, short plain sentences, active voice, no em dashes, no filler, no
reassurance, no narration of what the chapter does or will do, no "in this chapter", nothing that
personifies a system, a program, an event, a cell, a check, a rule or a product (a rule does not
"know", "see", "think", "want", "choose" or "decide"; say what it takes, keeps, drops, sets or
lists). Say the thing; do not build up to it. Keep every name in backticks exactly as written. A
block of code is a "cell". The buttons are **Run all**, **Run below** and **Save**, in bold; name no
other control. Never refer to Jo Marsh or any person as "he" or "she": repeat the name. Do not say a
number, a table or a record "says" anything; say what it shows, holds or lists.

Words the chapters already use, with one meaning each: *asset*, *dataset*, *job* (one of the four
programs that run each night, or a job in a named system), *program* (any of the shop's programs),
*function* (one of the returns desk's two programs), *node*, *edge*, *graph*, *lineage*,
*upstream*, *downstream*, *run* (one time a program did its work), *event*, *OpenLineage*,
*namespace*, *producer*, *facet*, *ingestion*, *schema*, *collector* (the program that receives
every event, Chapter 9; the reader built its pieces in Chapter 25), *identity*, *qualified name*,
*alias*, *freshness*, *index*. Never "walk": say "follows".

Real systems appear by name: OpenLineage, Marquez, Airflow, Spark, dbt, Trino, DataHub,
OpenMetadata, Apache Atlas (then "Atlas"), MLflow. Write a product's name in plain text. A field,
setting or value of a product goes in backticks, as the brief writes it. Never call a product
better or worse than another, and never use a product's marketing words.

None of these systems runs on the page. Each cell that shows what a system does applies that
system's rule, as its code or documentation states it, to the shop's own week. Say it that way:
"by Marquez's rules", "the name the provider gives", "as dbt's integration sends them". Never write
that Marquez, Airflow or any system "ran", "received" or "stored" something on the page. Never write
lab, engine, simulator, Jupyter, notebook (say "page" if needed).

Keep what a specification requires apart from what one implementation does: "the OpenLineage
specification requires" and "Marquez does" are different claims, and the brief says which each
fact is.

The days: each night's work runs in the early hours of the next day, so the run of
`build_daily_sales` early on Thursday 10 writes Wednesday 9's row. Name a run by the day it ran on,
as the brief does. A day is written as in the brief: "Friday 11". Times are UTC and written as the
brief gives them.

The reader has pressed **Run all** first, so when they reach a cell for their expectation, the cells
below it have already run: ask them to write it "before you read on".

In Part VII the reader changes one short cell per chapter: a setting, an order or a small mapping,
in a cell that starts with a value that runs and gives a result the check below fails. Say what to
change in plain words, and say what the check shows before and after. Never call the starting cell
a stub, and never give the finished value in the prose unless the brief gives it.

Part VII introduces no new terms. Use no term the brief does not use.

Never write a number in words where the brief gives it in figures, and never write one the brief
does not give. Where the brief says a slot is a list, write a Markdown list. A slot that is the
text of a cell the reader writes in is exactly two lines: the question, then a line of eight full
stops.

Write the file once. Do not change it after you reply. Use only the Read and Write tools. Send no
messages and call no other tool. Write the draft as Markdown with one `## key` heading per slot, in
the brief's order (`## A`, `## B`, ...), and nothing under each heading but the text itself.
