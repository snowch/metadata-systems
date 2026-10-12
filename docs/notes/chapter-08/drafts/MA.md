## A

- Find where each of Chapter 7's fields goes in an open standard's events.
- Find what a program that receives the events holds after each one.
- Check an event written by hand, and find why two names for one table do not join.
- Question a requirement about the events the shop's programs must send.

## B
## A form other programs can read

The head of the shop wants to see the shop's runs in a tool the shop did not write.

Chapter 7's events use field names the shop chose. A tool written elsewhere would have to learn them, and the field names of every other shop it reads from.

**OpenLineage** is an open specification for events about data processing. It sets their form, so that a program written by one team can send them and a program written by another can read them. It defines three kinds of event. This chapter uses one, the run event, which describes a run of a job. The other two describe a job, or a dataset, on its own.

The head's requirement reads "Our programs must emit OpenLineage." To emit an event is to send it.

## C
## One run as OpenLineage events

The next cell runs the week with the returns desk and with the `failed` change, in which `build_daily_sales` fails on its last night, as in Chapter 2.

It makes every run's events in OpenLineage's form. It prints the two events of `build_clean_orders`'s run on Friday 11, which read the orders up to Thursday. It prints the first event in full. Of the second, it prints only the fields that differ from the first: its type, its time, its inputs and its outputs.

## D

The first event's `eventType` is `START`. The second's is `COMPLETE`. A run that fails sends `FAIL` in place of `COMPLETE`. `eventTime` is when the event happened. `schemaURL` is the address of the version of the specification's schema that the event follows.

`run.runId` is the run's identifier. The specification requires a UUID, a standard form of identifier. The shop makes UUIDs of version 7, which begin with the run's start time. The specification's documentation recommends that version.

A job is named by a **namespace** and a name inside it. Here the namespace is `shop` and the name is `build_clean_orders`.

A dataset is named the same way. `orders.jsonl` is named `orders.jsonl` in the namespace `s3://shop-raw`, its bucket. The shop's producers name `clean_orders` as `shop.analytics.clean_orders` in the namespace `warehouse://shop-warehouse`. That name is the shop's choice: a database `shop`, a schema `analytics`, then the table.

`producer` is the address of the code that made the event. Here it is `https://example.org/shop/jobs/tree/v1`, which makes the events of all four jobs. That code is the event's **producer**.

Further metadata comes in a **facet**. A facet is a named object that holds its own fields. Each facet has `_producer`, the code that made it, and `_schemaURL`, the address of the facet's own schema.

In these events, `jobType` says the job is a batch job, one that starts and finishes. `sourceCodeLocation` holds the code version, `b178023`. The shop fills it with its own hash of the code, which is Chapter 7's `code_version`, not a commit. `nominalTime` holds the time the run was due to start. `inputStatistics` holds the rows read, 27. `outputStatistics` holds the rows written, 23.

The next cell lists where each of Chapter 7's fields went.

## G

The consumer writes each name as its namespace, then `/`, then the name.

Its row holds the state `START`, the start time, and the input `orders.jsonl`. It holds no output and no end time. The START named the input and no output.

From this row alone, a run still working and a run that stopped without sending another event look the same.

The next cell sends the COMPLETE.

## H

The row now holds the state `COMPLETE`, the end time `2026-09-11T02:05:52Z`, the output `warehouse://shop-warehouse/shop.analytics.clean_orders`, and 2 events.

The COMPLETE named the input again, with its row count, and added the output.

The specification says that events about one run add to each other. Its words: "All metadata is additive". A facet sent again under the same name replaces the earlier one.

The consumer lists the repeated input once, matching it by its namespace and name. The shop's consumer is written that way.

The next cell sends every event of the week to a new consumer, prints how many runs it holds, and lists the runs whose state is `FAIL`.

## J

## An event written by hand

The analyst's copy sends no events. The analyst writes the two events of Friday 11's copy by hand.

The next cell holds them as Python dictionaries, `start` and `complete`.

The `runId` comes from `shop.openlineage.uuid7`, which makes a version 7 UUID from a start time.

The cell checks `start` against the specification's rules:

- the fields every run event must have: `eventTime`, `producer`, `schemaURL`, `run` with a `runId`, and `job` with a namespace and a name;
- a `runId` that is a UUID;
- an `eventType` from the specification's list, where the event has one;
- a time in the specification's date-time form;
- addresses that are URIs;
- in each facet, a `_producer` and a `_schemaURL`.

## M

The traversal reaches 2 nodes, `analyst/copy_clean_orders` and `warehouse://shop-warehouse/analytics.clean_orders`, and stops. It does not reach `orders.jsonl`.

Compare the analyst's input in the cell above with the name the jobs' events gave `clean_orders` earlier: `analytics.clean_orders` against `shop.analytics.clean_orders`. The analyst left out the database.

The consumer joins two datasets only when their namespace and their name are the same. To the consumer, the two names are two datasets.

Change the analyst's input to the jobs' name, `"shop.analytics.clean_orders"`, select that cell and press **Run below**. The traversal then reaches 4 nodes, through `shop/build_clean_orders`, to `orders.jsonl`.

The specification's naming page gives a namespace and a name for each kind of data store it lists. It lists no form for the store the shop's warehouse runs on, so the shop's producers must agree on one.

The page warns of the same failure for a store it lists: names made under Snowflake's older form of account name do not connect to names made under the newer form, so the lineage does not join.

## O

The check lists 2 problems: `producer` is missing, and `run.runId` is not a UUID.

The cell above sent the event to a new consumer. The consumer set it aside and holds no run from it.

Setting such an event aside is how the shop's consumer is written. The specification says what an event must hold.

## P

## "Our programs must emit OpenLineage."

The head of the shop set this requirement at the start of the chapter.

Before you read on, write in the next cell what you would check to say that the shop meets it.

## READINGS

The requirement could mean four things:

- which programs: a list of every program that touches the shop's data, and whether each sends events;
- which events: for each run, one START and one COMPLETE, ABORT or FAIL, as the specification requires (ABORT is for a run stopped abnormally, FAIL for one that failed); RUNNING and OTHER are optional;
- which facets: a list of the facets each event must carry; the specification requires none;
- which names: one namespace and name for each dataset, which every producer uses.

Each reading needs something different. The next cell counts, job by job, the runs, the events of each type, and the events that break the specification's rules.

## R

In all, 6 programs sent events: the four jobs and the two functions. Every run sent a START and a COMPLETE, except the run of `build_daily_sales` on Monday 14, which sent a FAIL. No event breaks the specification's rules.

Taken one reading at a time:

- which programs: not met for every program; the export and the analyst's copy send nothing;
- which events: met, for the jobs and the functions;
- which facets: the shop sends some of the standard facets and one of its own, `shop_objectChange`, for a function's file change, named with the shop's prefix as the specification asks of a facet that is not standard. Whether these are the facets meant, the requirement does not say;
- which names: met within the shop's own producers; the analyst's hand-written events used another name until you changed it.

As written, "Our programs" covers every program, so the shop does not meet the requirement until the export and the analyst's copy send events too.

## S

## Before Chapter 9

The shop's runs, in OpenLineage's form, showed the following. After a START, the consumer held the run's input and no output. The output came with the COMPLETE. A failed run sent a FAIL. An event written by hand passed the check, but two names for one table did not join until you changed one. An event that broke two rules was set aside.

The experiments could not show how a consumer keeps a week of events and turns them into a graph that answers questions. They could not show what a consumer does with an event that arrives damaged.

Chapter 9 builds that consumer, one stage at a time, from the events as received to a graph.

- Which programs on a platform you work on would need to send events for its lineage to be whole?
- How should your platform name its warehouse's tables, and who must agree on the names?
- What should a consumer do with a `START` whose run never sends another event?

## T

### How this differs from a real platform

The shop, its programs, its producers and their addresses are invented for the course. The addresses at `example.org` lead nowhere.

Here the shop's own code makes each event and hands it straight to the consumer. A real producer is usually a library inside the program that runs the job. The specification also defines an HTTP interface for sending events to a consumer.

The consumer is the shop's own, not a product. It takes a run's state from the last event it received. The OpenLineage documentation calls Marquez the reference implementation of its API. Chapter 29 compares real consumers.

The specification does not say what a consumer does with a missing, repeated or late event. Chapters 18 to 20 take that up.

The specification's schema and its page on the run cycle disagree on one point. The schema allows OTHER events, which carry extra metadata, after a run's COMPLETE, ABORT or FAIL. The run cycle page says no event follows those.

The namespaces `warehouse://shop-warehouse` and `reporting://shop-reporting` are the shop's choice.
