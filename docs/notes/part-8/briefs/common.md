# What every brief for Chapter 33 shares

Chapter 33 is the course's last chapter. The reader has done Chapters 1 to 32 on an online shop's
data platform. Here they join the data team of a second platform, an island ferry's, and use what
they built to answer three questions about it.

Write for a Jupyter notebook read by a data engineer; the reader is "you". Follow `docs/style.md`
and `AGENTS.md`: British English, short plain sentences, active voice, no em dashes, no filler, no
reassurance, no narration of what the chapter does or will do, no "in this chapter", nothing that
personifies a system, a function, a job, an event, a cell, a check or a record (a record does not
"know", "see", "say", "tell", "remember" or "decide"; say what it holds, lists or shows). Say the
thing; do not build up to it. Keep every name in backticks exactly as written. A block of code is a
"cell". The buttons are **Run all**, **Run below** and **Save**, in bold; name no other control.
Never refer to any person as "he" or "she".

Words with one meaning each on this page:

- *batch*: one object a ticket gate uploads, holding one sailing's scans from that gate;
- *scan*: one line in a batch, one ticket scanned at a gate;
- *version*: one version of a batch in object storage, named by an identifier such as `15da88b56abc`;
- *function*: `load_scans` or `drop_scans`, which the platform starts when a batch changes;
- *job*: `build_loads` or `send_report`, which the scheduler starts at a set time;
- *run*: one time a function or a job did its work (a noun); "ran" as a verb is fine;
- *sailing*: one departure, written as the day, the side and the time, such as "Tuesday's 17:30 from
  the mainland";
- *the ferry*: the company and its platform; never name a place or a company;
- *event*, *facet*, *namespace*, *collector*, *lineage*, *graph*, *edge*, *dataset*, *producer*,
  *consumer*: as earlier chapters used them.

Never write lab, engine, simulator, Jupyter or notebook (say "page" if needed). No real object
store, function platform or scheduler is named: the ferry's are its own. OpenLineage is named, and a
claim about it is only what the brief gives.

The days: Tuesday 22, Wednesday 23 and Thursday 24 September 2026; the reader starts on Friday 25 at
09:00. Write a day as "Tuesday 22" or "Tuesday", and a time as the brief gives it, such as 07:05.

The reader has pressed **Run all** first, so when they reach a cell for their expectation, the
cells below it have already run: ask them to write it "before you read on".

The reader changes two short cells in this chapter. Say what to change in plain words, and what the
check below shows before and after. Never call the starting cell a stub, and never give the
finished code in the prose.

Use no term the brief does not use. Never write a number in words where the brief gives it in
figures, and never write one the brief does not give. Where the brief says a slot is a list, write a
Markdown list. A slot that is the text of a cell the reader writes in is exactly two lines: the
question, then a line of eight full stops. A heading the brief gives (`### ...`) goes in the slot
where the brief puts it.

Write the file once. Use only the Read and Write tools. Send no messages and call no other tool.
Write the draft as Markdown with one `## key` heading per slot, in the brief's order, and nothing
under each heading but the text itself.
