# Chapter 8: OpenLineage

A working note. Written on 12 October 2026 with Chapters 7 and 9, as a notebook
(`notebook/chapter_08.py`).

## What the chapter does

The head of the shop wants the runs in a tool the shop did not write, and sets the requirement
"Our programs must emit OpenLineage." The reader meets **OpenLineage** as one answer to a problem
Chapter 7 left: the shop's field names are its own. The reader:

- reads the two OpenLineage run events of `build_clean_orders`'s run on Friday 11, with the
  **namespace**, the **producer** and the **facet** each named where they first appear, and a table
  of where each of Chapter 7's fields went;
- writes what a consumer knows after the START alone, sends it, then the COMPLETE: the input first,
  the output only at the end; the week's 34 runs, one of them a FAIL;
- reads two events the analyst wrote by hand, checked against the specification's rules; writes
  whether the traversal upstream from the copy reaches `orders.jsonl`, finds it stops at
  `analytics.clean_orders`, renames it to the jobs' form, and sees the graph join;
- sees an event that breaks two rules refused, by the shop's choice;
- questions "Our programs must emit OpenLineage." (below).

## What was built for it

- `notebook/shop/openlineage.py`: `run_events` (each run's START and COMPLETE or FAIL, with run
  facets `nominalTime` and the shop's custom `shop_objectChange`, job facets `jobType` and
  `sourceCodeLocation`, input facets `inputStatistics` and `version`, output facet
  `outputStatistics`); `uuid7` (a version 7 UUID from the start time, with hash bits in place of
  random ones); `check` and `problems` (the specification's rules as `docs/sources.md` records them,
  in the course's own code); `Consumer` (accumulates events by `runId`, inputs and outputs added, a
  facet replaced by name, state from the latest event; refuses an event that breaks the rules);
  `mapping`, `summary`, `analyst_events` (Chapter 9's third producer); the check's messages are
  Haiku's drafts of brief JA.
- The functions' events come from a second producer that writes times with `+00:00`.
- Every event the shop produces was validated against the published schema (`$id`
  `https://openlineage.io/spec/2-0-2/OpenLineage.json`) and each standard facet's schema with
  `jsonschema` 4.26 (68 events, no error), and the same check failed on a broken event; the schemas
  were read, not copied (`docs/sources.md`). `notebook/tests` holds every event to the course's own
  check.

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the assets the events name, as Chapter 7 left the platform.
- **Why now:** the chapter opens on the runs of those assets' programs.

### `one-run`

- **Role:** inspect
- **Serves:** what an OpenLineage run event holds, from a run the reader has already met in Chapter
  7 (the run on Friday 11: 27 rows read, 23 written).
- **Why now:** the terms are given against it, and the mapping table follows it.

### `consumer-after-start`

- **Role:** experiment
- **Objective:** the reader learns that a consumer's knowledge of a run grows event by event: after
  a START it knows the input and nothing of the output, and cannot tell a run still working from
  one that stopped.
- **Known before:** the two events, printed above; that a START names no output.
- **Driving question:** what does the consumer know after the START alone, about the run and about
  `clean_orders`?
- **The action:** write the expectation; send the START; send the COMPLETE; read each state.
- **Why the action:** the reader commits before seeing the consumer's row.
- **Evidence:** state START, the input, no output; then COMPLETE, the output, 2 events; then the
  week's 34 runs and one FAIL.
- **Consequence:** a reader who expected the consumer to know of `clean_orders` learns that it
  waits on the terminal event.
- **Predictable:** yes, from the printed events.
- **Gives nothing away:** the question names `clean_orders`, not what the consumer holds.
- **Not knowing:** right about whether the run is still working, and the prose says so.
- **Next question:** what if two producers name a table differently?
- **An experiment:** commit, send, compare.

### `two-names`

- **Role:** experiment
- **Objective:** the reader discovers that lineage from events joins only where producers name a
  dataset identically, and that the specification's naming page gives no form for a warehouse
  like the shop's.
- **Known before:** the analyst's events, with `analytics.clean_orders`; the jobs' name
  `shop.analytics.clean_orders`.
- **Driving question:** will the traversal upstream from the copy reach `orders.jsonl`?
- **The action:** write the expectation; read the traversal; change the name; press **Run below**.
- **Why the action:** the change is the fix a team would make, and the reader makes it.
- **Evidence:** 2 nodes, stopping at `analytics.clean_orders`; 4 after the change, to
  `orders.jsonl`.
- **Consequence:** the reader sees that a consumer joins by namespace and name, not by meaning.
- **Predictable:** yes, if the reader noticed the two names.
- **Gives nothing away:** the prose above gives the analyst's name, not the result.
- **Not knowing:** not the right answer.
- **Next question:** what does a consumer do with a broken event?
- **An experiment:** commit, run, change, run again.

### `broken-event`

- **Role:** inspect
- **Serves:** the check's two problems, and the shop's consumer refusing the event.
- **Why now:** the rules were listed above; this shows them catch something.

## Requirements

The chapter questions "Our programs must emit OpenLineage.", the plan's candidate, with the reader's
expectation and a count of each job's runs and events.

1. **What it says:** the programs must emit OpenLineage.
2. **What it might mean:** which programs; which events; which facets; under which namespace and
   name.
3. **What each needs:** a decision on the export and the analyst's copy; a START and a terminal
   event per run (the schema's requirement); a list of facets; a naming convention.
4. **What the platform records:** START and COMPLETE or FAIL for every run of the jobs and the
   functions; standard facets and one custom; the naming page's form for object storage, the shop's
   own for its warehouse and reporting tool.
5. **Whether it is met:** as written, for the jobs and the functions; the requirement does not say
   which programs, facets or names it means.

## Originality

The obvious examples are the specification's own sample event, a Marquez quickstart's seeded
lineage, or an integration's events from a sample warehouse job. Here the event is the reader's
Chapter 7 run on Friday 11 rewritten field by field, the consumer is a small one of the shop's, the
hand-written event is the invented analyst's copy, and the join failure is the shop's own two names
for one table. Field names, event types and facet names are the specification's, used as names; the
schema is not copied, and the course's check is its own code.

## What the prose process caught

Brief JA, draft under `drafts/`. The brief put the expectation cell after the cell that sends the
START, where the page has it before, in two places; the draft followed the brief, and the fewest
words fixed both ("the cell after the next one sends", "write in the next cell"), and a third
("the same cell then counts"). The check's message for no problems came back as a description of
itself, and its second sentence was kept. The objective that quoted the requirement used the term
OpenLineage before the section that introduces it, and now names the requirement without it.

## Measured

12 October 2026, local build (`docs/notes/notebook-prototype.md`, "Chapters 7, 8 and 9"): Run all 8.9 to 9.3 s; peak memory 396 to 405 MB;
0.29 MB from Chapter 7's link. The published page is measured after the deploy.

## Known gaps

- The consumer is the shop's; what a real one (Marquez, the reference implementation) does with each
  event is Chapter 29's, read in its source first.
- The custom facet's schema address is the shop's and serves nothing.
