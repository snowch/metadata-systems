# Brief MA: Chapter 8, "OpenLineage", after its review

Read `docs/notes/chapter-07/briefs/common.md` first, and `docs/style.md`. Its rules hold here. Terms
as brief JA: **OpenLineage** in slot B; **namespace**, **producer** and **facet** in slot D, each in
bold once, none before its slot (the objectives in slot A included). Do not say a consumer "knows";
say what it holds or records. No signposting ("comes back at the end"). Quote the specification only
where a quotation is given, marked as one.

A review found that two predictions were answered on the page before the reader committed, a
definition did not hold for every case, a claim was made about a refusal no cell showed, and the
requirement section lacked what each reading needs and a verdict for each. These slots replace
paragraphs of the chapter.

## Facts (each checked against the specification, `docs/sources.md`, or the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Find where each of Chapter 7's fields goes in an open standard's events.
- Find what a program that receives the events holds after each one.
- Check an event written by hand, and find why two names for one table do not join.
- Question a requirement about the events the shop's programs must send.

### Slot B: under the heading `## A form other programs can read`

- The head of the shop wants to see the shop's runs in a tool the shop did not write.
- Chapter 7's events use field names the shop chose. A tool written elsewhere would have to learn
  them, and the field names of every other shop it reads from.
- **OpenLineage** is an open specification for events about data processing, which sets their form
  so that a program written by one team can send them and a program written by another can read
  them. It defines three kinds of event; this chapter uses one, the run event, which describes a run
  of a job. The other two describe a job, or a dataset, on its own.
- The head's requirement: "Our programs must emit OpenLineage." To emit an event is to send it.

### Slot C: under the heading `## One run as OpenLineage events`

- The next cell runs the week with the returns desk and with the `failed` change, in which
  `build_daily_sales` fails on its last night, as in Chapter 2.
- It makes every run's events in OpenLineage's form, and prints the two events of
  `build_clean_orders`'s run on Friday 11, which read the orders up to Thursday: the first in full,
  and of the second only its type, its time, its inputs and its outputs, where it differs from the
  first.

### Slot D: after that cell

- The first event's `eventType` is `START`; the second's is `COMPLETE`. A run that fails sends `FAIL`
  in place of `COMPLETE`. `eventTime` is when the event happened. `schemaURL` is the address of the
  version of the specification's schema the event follows.
- `run.runId` is the run's identifier. The specification requires a UUID, a standard form of
  identifier. The shop makes UUIDs of version 7, which begin with the run's start time; the
  specification's documentation recommends that version.
- A job is named by a **namespace** and a name inside it: here the namespace `shop` and the name
  `build_clean_orders`.
- A dataset is named the same way. `orders.jsonl` is named `orders.jsonl` in the namespace
  `s3://shop-raw`, its bucket. The shop's producers name `clean_orders` as
  `shop.analytics.clean_orders` (the shop's choice: a database `shop`, a schema `analytics`, then
  the table) in the namespace `warehouse://shop-warehouse`.
- `producer` is the address of the code that made the event: here
  `https://example.org/shop/jobs/tree/v1`, which makes the events of all four jobs. That code is the
  event's **producer**.
- Further metadata comes in a **facet**: a named object holding its own fields, with `_producer` (the
  code that made it) and `_schemaURL` (the address of the facet's own schema).
- In these events: `jobType` says the job is a batch job, one that starts and finishes;
  `sourceCodeLocation` holds the code version, `b178023`, which the shop fills with its own hash of
  the code (Chapter 7's `code_version`), not a commit; `nominalTime` holds the time the run was due to
  start; `inputStatistics` holds the rows read, 27; `outputStatistics` holds the rows written, 23.
- The next cell lists where each of Chapter 7's fields went.

### Slot G: after the cell that sends the START alone

- The consumer writes each name as its namespace, then `/`, then the name.
- Its row holds the state `START`, the start time, and the input `orders.jsonl`. It holds no output
  and no end time: the START named the input and no output.
- From this row alone, a run still working and a run that stopped without sending another event look
  the same.
- The next cell sends the COMPLETE.

### Slot H: after the cell that sends the COMPLETE

- The row now holds the state `COMPLETE`, the end time `2026-09-11T02:05:52Z`, the output
  `warehouse://shop-warehouse/shop.analytics.clean_orders`, and 2 events.
- The COMPLETE named the input again, with its row count, and added the output.
- The specification says that events about one run add to each other. Its words: "All metadata is
  additive". A facet sent again under the same name replaces the earlier one.
- That the consumer lists the repeated input once, matching it by its namespace and name, is how the
  shop's consumer is written.
- The next cell sends every event of the week to a new consumer, prints how many runs it holds, and
  lists the runs whose state is `FAIL`.

### Slot J: under the heading `## An event written by hand`

- The analyst's copy sends no events. The analyst writes the two events of Friday 11's copy by hand.
- The next cell holds them as Python dictionaries, `start` and `complete`.
- The `runId` comes from `shop.openlineage.uuid7`, which makes a version 7 UUID from a start time.
- The cell checks `start` against the specification's rules:
  - the fields every run event must have: `eventTime`, `producer`, `schemaURL`, `run` with a `runId`,
    and `job` with a namespace and a name;
  - a `runId` that is a UUID;
  - an `eventType` from the specification's list, where the event has one;
  - a time in the specification's date-time form;
  - addresses that are URIs;
  - in each facet, a `_producer` and a `_schemaURL`.
- (Do not describe how the analyst names any dataset.)

### Slot M: after the traversal upstream from the copy

- The traversal reaches 2 nodes, `analyst/copy_clean_orders` and
  `warehouse://shop-warehouse/analytics.clean_orders`, and stops. It does not reach `orders.jsonl`.
- Compare the analyst's input in the cell above with the name the jobs' events gave `clean_orders`
  earlier: `analytics.clean_orders` against `shop.analytics.clean_orders`. The analyst left out the
  database.
- The consumer joins two datasets only when their namespace and their name are the same. To it, the
  two names are two datasets.
- Change the analyst's input to the jobs' name, `"shop.analytics.clean_orders"`, select that cell and
  press **Run below**. The traversal then reaches 4 nodes, through `shop/build_clean_orders`, to
  `orders.jsonl`.
- The specification's naming page gives a namespace and a name for each kind of data store it lists.
  It lists no form for the store the shop's warehouse runs on, so the shop's producers must agree on
  one.
- The page warns of the same failure for a store it lists: names made under Snowflake's older form of
  account name do not connect to names made under the newer form, so the lineage does not join.

### Slot O: after the check of the broken event, and the cell that sends it to a consumer

- The check lists 2 problems: `producer` is missing, and `run.runId` is not a UUID.
- The next cell sent the event to a new consumer, which set it aside and holds no run from it.
- Setting such an event aside is how the shop's consumer is written. The specification says what an
  event must hold.

### Slot P: under the heading `## "Our programs must emit OpenLineage."`

- The head of the shop's requirement, from the start of the chapter.
- Before you read on, write in the next cell what you would check to say that the shop meets it.

### Slot READINGS: after that cell, before the cell that counts the events

- The requirement could mean four things, each needing something different:
  - which programs: a list of every program that touches the shop's data, and whether each sends
    events;
  - which events: for each run, one START and one COMPLETE, ABORT or FAIL, as the specification
    requires (ABORT is for a run stopped abnormally, FAIL for one that failed); RUNNING and OTHER are
    optional;
  - which facets: a list of the facets each event must carry; the specification requires none;
  - which names: one namespace and name for each dataset, which every producer uses.
- The next cell counts, job by job, the runs, the events of each type, and the events that break the
  specification's rules.

Write slot READINGS as one Markdown list of the four readings, then the sentence about the next cell.

### Slot R: after the counts

- 6 programs sent events: the four jobs and the two functions. Every run sent a START and a COMPLETE,
  except the run of `build_daily_sales` on Monday 14, which sent a FAIL. No event breaks the
  specification's rules.
- By reading:
  - which programs: not met for every program; the export and the analyst's copy send nothing;
  - which events: met, for the jobs and the functions;
  - which facets: the shop sends some of the standard facets and one of its own,
    `shop_objectChange`, for a function's file change, named with the shop's prefix as the
    specification asks of a facet that is not standard. Whether these are the facets meant, the
    requirement does not say;
  - which names: met within the shop's own producers; the analyst's hand-written events used another
    name until you changed it.
- As written, "Our programs" covers every program, so the shop does not meet the requirement until
  the export and the analyst's copy send events too.

Write slot R as a short paragraph, one Markdown list of the four verdicts, then a short paragraph.

### Slot S: under the heading `## Before Chapter 9`

- Showed: the shop's runs in OpenLineage's form. After a START, the consumer held the run's input and
  no output; the output came with the COMPLETE. A failed run sent a FAIL. An event written by hand
  passed the check, but two names for one table did not join until you changed one. An event that
  broke two rules was set aside.
- Could not show: how a consumer keeps a week of events and turns them into a graph that answers
  questions, and what it does with an event that arrives damaged.
- Next: Chapter 9 builds that, one stage at a time, from the events as received to a graph.
- Then the same three reflective questions as now (keep their wording):
  - Which programs on a platform you work on would need to send events for its lineage to be whole?
  - How should your platform name its warehouse's tables, and who must agree on the names?
  - What should a consumer do with a `START` whose run never sends another event?

### Slot T: under the heading `### How this differs from a real platform`

- The shop, its programs, its producers and their addresses are invented for the course. The
  addresses at `example.org` lead nowhere.
- Here the shop's own code makes each event and hands it straight to the consumer. A real producer is
  usually a library inside the program that runs the job, and the specification also defines an HTTP
  interface for sending events to a consumer.
- The consumer is the shop's own, not a product. It takes a run's state from the last event it
  received. The OpenLineage documentation calls Marquez the reference implementation of its API;
  Chapter 29 compares real consumers.
- The specification does not say what a consumer does with a missing, repeated or late event.
  Chapters 18 to 20 take that up.
- The specification's schema and its page on the run cycle disagree on one point: the schema allows
  OTHER events, which carry extra metadata, after a run's COMPLETE, ABORT or FAIL; the run cycle page
  says no event follows those.
- The namespaces `warehouse://shop-warehouse` and `reporting://shop-reporting` are the shop's
  choice.

## Slots

Write the file `docs/notes/chapter-08/drafts/MA.md` with the slots under `## A`, `## B`, `## C`,
`## D`, `## G`, `## H`, `## J`, `## M`, `## O`, `## P`, `## READINGS`, `## R`, `## S` and `## T`, each
the exact text to place, and nothing else in the file. Each slot that has a heading starts with that
heading.
