# Brief JA: Chapter 8, "OpenLineage"

Read `docs/notes/chapter-07/briefs/common.md` first, and `docs/style.md`. Its rules hold here.

Terms. The reader knows Chapter 7's **run** (one time a program does its work) and **event** (a
message a program sends about a run), and that a **function** is a program started by a change to a
file. This chapter introduces **OpenLineage** (slot B), **namespace**, **producer** and **facet**
(slot D), each in bold once, and none of the four before its slot. Words you must not use
anywhere: ingestion, normalise, impact analysis, provenance. Quote the specification only where
the brief gives a quotation, and mark it as one.

## Facts (each checked against the specification, `docs/sources.md`, or the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Find where each of Chapter 7's fields goes in an open standard's events.
- Find what a program that receives the events knows after each one.
- Write an event by hand, and find why two names for one table do not join.
- Question the requirement "Our programs must emit OpenLineage."

### Slot B: under the heading `## A form other programs can read`

- The head of the shop wants to see the shop's runs in a tool the shop did not write.
- Chapter 7's events use field names the shop chose. A tool written elsewhere would have to learn
  them, and those of every other place it is used.
- **OpenLineage** is an open specification for events about runs of jobs: it sets their form, so a
  program written by one team can send them and a program written by another can read them.
- Its words differ from the shop's in one place: what a run reads are its inputs, and what it writes
  its outputs.
- The head's requirement is "Our programs must emit OpenLineage." To emit an event is to send it.
  The chapter comes back to the requirement at the end.

### Slot MAP: one sentence above the figure

The shop's three systems with the returns desk, as Chapter 7 left them.

### Slot C: under the heading `## One run as OpenLineage events`

- The next cell runs the week with the returns desk and with the `failed` change, in which
  `build_daily_sales` fails on its last night, as in Chapter 2.
- It makes every run's events in OpenLineage's form, and prints the two events of
  `build_clean_orders`'s run on Friday 11.

### Slot D: after that cell

- The first event's `eventType` is `START`, the second's `COMPLETE`. A run that fails sends `FAIL`
  in place of `COMPLETE`.
- `run.runId` is the run's identifier. The specification requires a UUID. The shop makes UUIDs of
  version 7, which begin with the run's start time; the specification's documentation recommends
  that version.
- A job is named by a **namespace** and a name inside it: here `shop` and `build_clean_orders`.
- A dataset is named the same way. `orders.jsonl` is the name `orders.jsonl` in the namespace
  `s3://shop-raw`, its bucket. `clean_orders` is the name `shop.analytics.clean_orders` in the
  namespace `warehouse://shop-warehouse`: the database `shop`, the schema `analytics`, the table.
- `producer` is the address of the program that made the event: here
  `https://example.org/shop/jobs/tree/v1`. That program is the event's **producer**. The functions'
  events come from a second producer, the library of the platform the functions run on.
- Further metadata comes in a **facet**: a named object holding `_producer`, `_schemaURL` (the
  address of the facet's schema), then its own fields.
- In these events, `inputStatistics` holds the rows read, 27; `outputStatistics` holds the rows
  written, 23; `sourceCodeLocation` holds the code version, `b178023`; and `nominalTime` holds the
  time the run was due to start.
- The START names the input and no output. The COMPLETE names the input again, with its row count,
  and adds the output.
- The next cell lists where each of Chapter 7's fields went.

### Slot E: under the heading `## What a consumer knows`

- A program that receives events is a consumer.
- The next cell sends the START alone to a consumer: the shop's own, a small one. It keeps one row
  for each run and adds to it what each event says.
- Before you read on, write in the next cell what the consumer knows about the run after the START
  alone, and what it knows about `clean_orders`.

### Slot F: the text inside that cell (between triple quotes)

Two questions, each followed by `........` on its own line: what the consumer knows about the run
after the START alone; what it knows about clean_orders. At most about 60 characters a line. Plain
text.

### Slot G: after that cell

- The consumer's row: state `START`, the start time, the input `orders.jsonl`, no output and no end
  time.
- It knows that the run began, and what it reads.
- It knows nothing about `clean_orders`: the START names no output.
- It cannot tell a run still working from one that stopped without sending another event.
- The next cell sends the COMPLETE.

### Slot H: after that cell

- The row now has state `COMPLETE`, the end time `2026-09-11T02:05:52Z`, the output
  `warehouse://shop-warehouse/shop.analytics.clean_orders`, and 2 events.
- The COMPLETE named the input again, and the consumer did not list it twice.
- The specification says that events about one run add to each other. Its words: "All metadata is
  additive". A facet sent again under the same name replaces the earlier one.
- The next cell sends every event of the week to a new consumer, and lists the runs whose state is
  `FAIL`.

### Slot I: after that cell

- The consumer holds 34 runs. One is `FAIL`: `build_daily_sales` on Monday 14, with no output.

### Slot J: under the heading `## An event written by hand`

- The analyst's copy sends no events. The analyst writes the two events of Friday 11's copy by hand.
- The next cell holds them as Python dictionaries, `start` and `complete`.
- The `runId` comes from `shop.openlineage.uuid7`, which makes a version 7 UUID from a start time.
- The analyst names `clean_orders` as `analytics.clean_orders` in the namespace
  `warehouse://shop-warehouse`, without the database.
- The cell checks `start` against the specification's rules: the fields every run event must have
  (`eventTime`, `producer`, `schemaURL`, `run` with a `runId`, and `job` with a namespace and a
  name), a `runId` that is a UUID, an `eventType` from the specification's list, a time in the
  specification's date-time form, addresses that are URIs, and in each facet a `_producer` and a
  `_schemaURL`.

### Slot CHECK: what the check prints, one sentence each

Write each under its own sub-heading (`### missing`, `### event_type` and so on), the exact text
only. The check prints one row per problem, with where it is (`where`, such as `run.runId`) and one
of these:

- `missing`: every run event needs this field, and the event does not have it
- `event_type`: the event type is not one of `START`, `RUNNING`, `COMPLETE`, `ABORT`, `FAIL` or
  `OTHER`
- `run_id`: the run's identifier is not a UUID
- `time`: the time is not a date and time in the form `2026-09-11T02:15:00Z`
- `uri`: the value is not an address with a scheme, such as `https:`
- `facet`: every facet needs `_producer` and `_schemaURL`, and this facet lacks this one
- `not_object`: this should be an object, with fields inside braces
- `none`: printed in place of the table when the event breaks no rule: say that the event breaks
  none of the specification's rules that the check tests

### Slot K: after the check

- The check finds no problems in `start`.
- The next cell sends the week's events and the analyst's two to a new consumer, and follows edges
  upstream from the copy, `s3://shop-scratch/clean_orders_copy.csv`.
- Before you read on, write in the next cell whether that traversal will reach `orders.jsonl`.

### Slot L: the text inside that cell

One question, then `........`: whether the traversal will reach orders.jsonl. At most about 60
characters a line. Plain text.

### Slot M: after the traversal

- The traversal reaches 2 nodes, `copy_clean_orders` and `analytics.clean_orders`, and stops. It
  does not reach `orders.jsonl`.
- The consumer joins two datasets only when their namespace and their name are the same. To it,
  `analytics.clean_orders` and `shop.analytics.clean_orders` are two datasets.
- In the cell that holds `start`, change `"analytics.clean_orders"` to
  `"shop.analytics.clean_orders"`, select that cell and press **Run below**.
- The traversal then reaches 4 nodes, through `build_clean_orders`, to `orders.jsonl`.
- The specification's naming page gives a namespace and a name for each kind of data store it lists.
  It lists no form for a warehouse like the shop's, so the shop's producers must agree on one.
- The page warns of the same failure for one store it lists: names made under Snowflake's older form
  of account name do not connect to names made under the newer form.

### Slot N: under the heading `## An event that breaks a rule`

- The next cell copies `start`, sets its `runId` to `"copy-friday"`, deletes its `producer`, and
  checks it.

### Slot O: after that cell

- The check lists 2 problems: `producer` is missing, and `run.runId` is not a UUID.
- The shop's consumer refuses an event that breaks the rules, and keeps it aside. That is the shop's
  choice. The specification says what an event must hold.

### Slot P: under the heading `## "Our programs must emit OpenLineage."`

- The head's requirement, from the start of the chapter.
- Before you read on, write in the next cell what you would check to say that the shop meets it.
- The cell then counts, job by job, the runs and the events of each type.

### Slot Q: the text inside that cell

One question, then `........`: what you would check to say the shop meets the requirement. At most
about 60 characters a line. Plain text.

### Slot R: after the counts

- 6 jobs sent events (the four jobs and the two functions). Each run sent a START, then a COMPLETE,
  except the run of `build_daily_sales` on Monday 14, which sent a FAIL.
- The requirement could mean several things, each needing something different:
  - which programs: the jobs and the functions send events; the export and the analyst's copy do
    not;
  - which events: the specification's schema requires one START and one of COMPLETE, ABORT or FAIL
    for each run; RUNNING and OTHER are optional;
  - which facets: the specification requires none. The shop sends some of the standard ones, and
    one of its own, `shop_objectChange`, for a function's file change, named with the shop's prefix
    as the specification asks of a facet that is not standard;
  - which namespaces and names: the naming page's form for object storage, and the shop's own for
    its warehouse and its reporting tool.
- As written, the shop meets the requirement for its jobs and its functions. Whether it means every
  program that touches the shop's data, or particular facets or names, the requirement does not
  say.

Write slot R as a short paragraph, one Markdown list of the four readings, then a short paragraph.

### Slot S: under the heading `## Before Chapter 9`

- Showed: the shop's runs in OpenLineage's form. The consumer knew a run's input after its START,
  and its output only after its COMPLETE. A failed run sent a FAIL. An event written by hand passed
  the check, but two names for one table did not join until the analyst changed one. An event that
  broke two rules was refused.
- Could not show: how a consumer keeps a week of events and turns them into a graph that answers
  questions, and what it does with a line it cannot read.
- Next: Chapter 9 builds that, one stage at a time, from the events as received to a graph.
- Then three reflective questions as a Markdown list, none with its answer: the first asks which
  programs on a platform the reader works on would need to send events for its lineage to be whole;
  the second asks how the reader's platform should name its warehouse's tables, and who must agree;
  the third asks what a consumer should do with a START whose run never sends another event.

### Slot T: under the heading `### How this differs from a real platform`

- The shop, its programs, its producers and their addresses are invented for the course. The
  addresses at `example.org` lead nowhere.
- The consumer is the shop's own, not a product. The OpenLineage documentation calls Marquez the
  reference implementation of its API; Chapter 29 compares real consumers.
- The specification's schema and its page on the run cycle disagree on one point. The schema allows
  OTHER events after a run's COMPLETE, ABORT or FAIL. The run cycle page says no event follows
  those.
- The namespaces `warehouse://shop-warehouse` and `reporting://shop-reporting` are the shop's
  choice.

## Slots

Write the file `docs/notes/chapter-08/drafts/JA.md` with the slots under `## A`, `## B`, `## MAP`,
`## C`, `## D`, `## E`, `## F`, `## G`, `## H`, `## I`, `## J`, `## CHECK` (with its eight `###`
sub-headings), `## K`, `## L`, `## M`, `## N`, `## O`, `## P`, `## Q`, `## R`, `## S` and `## T`,
each the exact text to place, and nothing else in the file. Each slot that has a heading starts with
that heading.
