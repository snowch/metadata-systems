## A

- Find where each of Chapter 7's fields goes in an open standard's events.
- Find what a program that receives the events knows after each one.
- Write an event by hand, and find why two names for one table do not join.
- Question a requirement about the events the shop's programs must send.

## B

## A form other programs can read

The head of the shop wants to see the shop's runs in a tool the shop did not write.

Chapter 7's events use field names the shop chose. A tool written elsewhere would have to learn those names, and the names of every other place where it is used.

**OpenLineage** is an open specification for events about runs of jobs. It sets their form, so a program written by one team can send them, and a program written by another team can read them.

The specification's words differ from the shop's in one place. What a run reads are its inputs. What it writes are its outputs.

The requirement from the head of the shop is "Our programs must emit OpenLineage." To emit an event is to send it. The requirement comes back at the end.

## MAP

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## C

## One run as OpenLineage events

The next cell runs the week with the returns desk and with the `failed` change. In that change, `build_daily_sales` fails on its last night, as in Chapter 2.

The cell makes every run's events in OpenLineage's form. It prints the two events of `build_clean_orders`'s run on Friday 11, the run that read the orders up to Thursday.

## D

The first event's `eventType` is `START`, and the second's is `COMPLETE`. A run that fails sends `FAIL` in place of `COMPLETE`.

`run.runId` is the run's identifier. The specification requires a UUID, a standard form of identifier. The shop makes UUIDs of version 7, which begin with the run's start time. The specification's documentation recommends that version.

A job is named by a **namespace** and a name inside it. Here the job `build_clean_orders` is named in the namespace `shop`.

A dataset is named the same way. `orders.jsonl` has the name `orders.jsonl` in the namespace `s3://shop-raw`, which is its bucket. `clean_orders` has the name `shop.analytics.clean_orders` in the namespace `warehouse://shop-warehouse`. That name holds the database `shop`, the schema `analytics` and the table `clean_orders`.

The `producer` field is the address of the program that made the event. Here it is `https://example.org/shop/jobs/tree/v1`. That program is the event's **producer**. The functions' events come from a second producer: the library of the platform the functions run on.

Further metadata comes in a **facet**: a named object. It holds `_producer`, then `_schemaURL` (the address of the facet's schema), then its own fields.

In these events, `inputStatistics` holds the rows read, 27. `outputStatistics` holds the rows written, 23. `sourceCodeLocation` holds the code version, `b178023`. `nominalTime` holds the time the run was due to start.

The `START` names the input and no output. The `COMPLETE` names the input again, with its row count, and adds the output.

The next cell lists where each of Chapter 7's fields went.

## E

## What a consumer knows

A program that receives events is a consumer. The cell after the next one sends the `START` alone to a consumer: the shop's own, a small one. It keeps one row for each run, and it adds to that row what each event says.

Before you read on, write in the next cell what the consumer knows about the run after the `START` alone, and what it knows about `clean_orders`.

## F

"""
After the START alone, what does it know about the run?
........
What does it know about clean_orders?
........
"""

## G

The consumer's row has the state `START`, the start time, the input `orders.jsonl`, no output and no end time.

It knows that the run began, and what the run reads. It knows nothing about `clean_orders`, because the `START` names no output.

It cannot tell a run that is still working from one that stopped without sending another event.

The next cell sends the `COMPLETE`.

## H

The row now has the state `COMPLETE`, the end time `2026-09-11T02:05:52Z`, the output `warehouse://shop-warehouse/shop.analytics.clean_orders`, and 2 events.

The `COMPLETE` named the input again, and the consumer did not list it twice.

The specification says that events about one run add to each other. In its words: "All metadata is additive." A facet sent again under the same name replaces the earlier one.

The next cell sends every event of the week to a new consumer, and lists the runs whose state is `FAIL`.

## I

The consumer holds 34 runs. One of them has the state `FAIL`: `build_daily_sales` on Monday 14. It has no output.

## J

## An event written by hand

The analyst's copy sends no events. The analyst writes the two events of Friday 11's copy by hand.

The next cell holds them as Python dictionaries, `start` and `complete`.

The `runId` comes from `shop.openlineage.uuid7`, which makes a version 7 UUID from a start time.

The analyst names `clean_orders` as `analytics.clean_orders` in the namespace `warehouse://shop-warehouse`, without the database.

The same cell checks `start` against the specification's rules:

- the fields every run event must have: `eventTime`, `producer`, `schemaURL`, `run` with a `runId`, and `job` with a namespace and a name;
- a `runId` that is a UUID;
- an `eventType` from the specification's list;
- a time in the specification's date-time form;
- addresses that are URIs;
- in each facet, a `_producer` and a `_schemaURL`.

## CHECK

The check prints one row per problem. Each row gives `where`, which is the place of the problem, such as `run.runId`, and one of these kinds:

### missing

Every run event needs this field, and the event does not have it.

### event_type

The event type is not one of `START`, `RUNNING`, `COMPLETE`, `ABORT`, `FAIL` or `OTHER`.

### run_id

The run's identifier is not a UUID.

### time

The time is not a date and time in the form `2026-09-11T02:15:00Z`.

### uri

The value is not an address with a scheme, such as `https:`.

### facet

Every facet needs `_producer` and `_schemaURL`, and this facet lacks this one.

### not_object

This should be an object, with fields inside braces.

### none

This is printed in place of the table when the event breaks no rule. It says that the event breaks none of the specification's rules that the check tests.

## K

The check finds no problems in `start`.

The cell after the next one sends the week's events and the analyst's two events to a new consumer, and follows edges upstream from the copy, `s3://shop-scratch/clean_orders_copy.csv`.

Before you read on, write in the next cell whether that traversal will reach `orders.jsonl`.

## L

"""
Will the traversal reach orders.jsonl?
........
"""

## M

The traversal reaches 2 nodes, `copy_clean_orders` and `analytics.clean_orders`, and stops. It does not reach `orders.jsonl`.

The consumer joins two datasets only when their namespace and their name are the same. To the consumer, `analytics.clean_orders` and `shop.analytics.clean_orders` are two datasets.

In the cell that holds `start`, change `"analytics.clean_orders"` to `"shop.analytics.clean_orders"`. Select that cell and press **Run below**.

The traversal then reaches 4 nodes, through `build_clean_orders`, to `orders.jsonl`.

The specification's naming page gives a namespace and a name for each kind of data store it lists. It lists no form for a warehouse like the shop's, so the shop's producers must agree on one.

The page warns of the same failure for one data store it lists. Names made under Snowflake's older form of account name do not connect to names made under the newer form.

## N

## An event that breaks a rule

The next cell copies `start`, sets its `runId` to `"copy-friday"`, deletes its `producer`, and checks it.

## O

The check lists 2 problems: `producer` is missing, and `run.runId` is not a UUID.

The shop's consumer refuses an event that breaks the rules, and keeps it aside. That is the shop's choice. The specification says what an event must hold.

## P

## "Our programs must emit OpenLineage."

The head of the shop set this requirement at the start of the chapter.

Before you read on, write in the next cell what you would check to say that the shop meets it. The same cell then counts, job by job, the runs and the events of each type.

## Q

"""
What would you check to say the shop meets the requirement?
........
"""

## R

The counts show 6 jobs that sent events: the four jobs and the two functions. Each run sent a `START`, then a `COMPLETE`, except the run of `build_daily_sales` on Monday 14, which sent a `FAIL`.

The requirement could mean several things, each needing something different:

- Which programs: the jobs and the functions send events. The export and the analyst's copy do not.
- Which events: the specification's schema requires one `START`, and one of `COMPLETE`, `ABORT` or `FAIL`, for each run. `RUNNING` and `OTHER` are optional.
- Which facets: the specification requires none. The shop sends some of the standard ones, and one of its own, `shop_objectChange`, for a function's file change. It is named with the shop's prefix, as the specification asks of a facet that is not standard.
- Which namespaces and names: the naming page's form for object storage, and the shop's own for its warehouse and its reporting tool.

As written, the shop meets the requirement for its jobs and its functions. Whether it means every program that touches the shop's data, or particular facets or names, the requirement does not say.

## S

## Before Chapter 9

The shop's runs now have OpenLineage's form. The consumer knew a run's input after its `START`, and its output only after its `COMPLETE`. A failed run sent a `FAIL`. An event written by hand passed the check, but two names for one table did not join until the analyst changed one. An event that broke two rules was refused.

The experiments could not show how a consumer keeps a week of events and turns them into a graph that answers questions. They could not show what a consumer does with a line it cannot read.

Chapter 9 builds that, one stage at a time, from the events as received to a graph.

- Which programs on a platform you work on would need to send events for its lineage to be whole?
- How should your platform name its warehouse's tables, and who must agree on the names?
- What should a consumer do with a `START` whose run never sends another event?

## T

### How this differs from a real platform

The shop, its programs, its producers and their addresses are invented for the course. The addresses at `example.org` lead nowhere.

The consumer is the shop's own, not a product. The OpenLineage documentation calls Marquez the reference implementation of its API. Chapter 29 compares real consumers.

The specification's schema and its page on the run cycle disagree on one point. The schema allows `OTHER` events after a run's `COMPLETE`, `ABORT` or `FAIL`. The run cycle page says no event follows those.

The namespaces `warehouse://shop-warehouse` and `reporting://shop-reporting` are the shop's choice.
