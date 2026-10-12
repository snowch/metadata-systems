[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 7](chapter_07.ipynb) · [Next: Chapter 9](chapter_09.ipynb)

# Chapter 8: OpenLineage

**Objectives**

- Find where each of Chapter 7's fields goes in an open standard's events.
- Find what a program that receives the events knows after each one.
- Write an event by hand, and find why two names for one table do not join.
- Question a requirement about the events the shop's programs must send. 

## A form other programs can read

The head of the shop wants to see the shop's runs in a tool the shop did not write.

Chapter 7's events use field names the shop chose. A tool written elsewhere would have to learn those names, and the names of every other place where it is used.

**OpenLineage** is an open specification for events about runs of jobs. It sets their form, so a program written by one team can send them, and a program written by another team can read them.

The specification's words differ from the shop's in one place. What a run reads are its inputs. What it writes are its outputs.

The requirement from the head of the shop is "Our programs must emit OpenLineage." To emit an event is to send it. The requirement comes back at the end. 

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them. 

[figure] The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table returns. 

<div class="ms-box ms-box-warning">

The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

<details><summary>Time and memory</summary>

The page downloaded less than 1 MB when opened from Chapter 7's link, in a browser that had opened and run Chapter 7 (measured on a computer). Chapter 7's link opens this page in a new tab. Chapter 7 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 7 leaves more memory for this page.

Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

</details>

</div> 

<div class="ms-box ms-box-steps">

**Running and saving the page**

1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser and is shown instead of the chapter, even after the chapter is updated.

</div> 

[hidden code cell]

[hidden code cell]

[hidden code cell]

## One run as OpenLineage events

The next cell runs the week with the returns desk and with the `failed` change. In that change, `build_daily_sales` fails on its last night, as in Chapter 2.

The cell makes every run's events in OpenLineage's form. It prints the two events of `build_clean_orders`'s run on Friday 11, the run that read the orders up to Thursday. 

```python
week8 = shop.run_week(["returns", "failed"])
events = shop.openlineage.run_events(week8)
friday = [e for e in events if e["job"]["name"] == "build_clean_orders" and e["eventTime"].startswith("2026-09-11")]
for event in friday:
    print(shop.openlineage.show(event))
```

[output]
{
  "eventType": "START",
  "eventTime": "2026-09-11T02:05:00Z",
  "run": {
    "runId": "01a08e36-04e0-7f2d-a476-dd470ff68684",
    "facets": {
      "nominalTime": {
        "_producer": "https://example.org/shop/jobs/tree/v1",
        "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/NominalTimeRunFacet.json#/$defs/NominalTimeRunFacet",
        "nominalStartTime": "2026-09-11T02:05:00Z"
      }
    }
  },
  "job": {
    "namespace": "shop",
    "name": "build_clean_orders",
    "facets": {
      "jobType": {
        "_producer": "https://example.org/shop/jobs/tree/v1",
        "_schemaURL": "https://openlineage.io/spec/facets/2-0-4/JobTypeJobFacet.json#/$defs/JobTypeJobFacet",
        "processingType": "BATCH",
        "integration": "SHOP",
        "jobType": "JOB"
      },
      "sourceCodeLocation": {
        "_producer": "https://example.org/shop/jobs/tree/v1",
        "_schemaURL": "https://openlineage.io/spec/facets/1-1-0/SourceCodeLocationJobFacet.json#/$defs/SourceCodeLocationJobFacet",
        "type": "git",
        "url": "https://example.org/shop/repository/blob/b178023/jobs/build_clean_orders.py",
        "version": "b178023"
      }
    }
  },
  "inputs": [
    {
      "namespace": "s3://shop-raw",
      "name": "orders.jsonl"
    }
  ],
  "outputs": [],
  "producer": "https://example.org/shop/jobs/tree/v1",
  "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"
}
{
  "eventType": "COMPLETE",
  "eventTime": "2026-09-11T02:05:52Z",
  "run": {
    "runId": "01a08e36-04e0-7f2d-a476-dd470ff68684",
    "facets": {
      "nominalTime": {
        "_producer": "https://example.org/shop/jobs/tree/v1",
        "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/NominalTimeRunFacet.json#/$defs/NominalTimeRunFacet",
        "nominalStartTime": "2026-09-11T02:05:00Z"
      }
    }
  },
  "job": {
    "namespace": "shop",
    "name": "build_clean_orders",
    "facets": {
      "jobType": {
        "_producer": "https://example.org/shop/jobs/tree/v1",
        "_schemaURL": "https://openlineage.io/spec/facets/2-0-4/JobTypeJobFacet.json#/$defs/JobTypeJobFacet",
        "processingType": "BATCH",
        "integration": "SHOP",
        "jobType": "JOB"
      },
      "sourceCodeLocation": {
        "_producer": "https://example.org/shop/jobs/tree/v1",
        "_schemaURL": "https://openlineage.io/spec/facets/1-1-0/SourceCodeLocationJobFacet.json#/$defs/SourceCodeLocationJobFacet",
        "type": "git",
        "url": "https://example.org/shop/repository/blob/b178023/jobs/build_clean_orders.py",
        "version": "b178023"
      }
    }
  },
  "inputs": [
    {
      "namespace": "s3://shop-raw",
      "name": "orders.jsonl",
      "inputFacets": {
        "inputStatistics": {
          "_producer": "https://example.org/shop/jobs/tree/v1",
          "_schemaURL": "https://openlineage.io/spec/facets/1-0-0/InputStatisticsInputDatasetFacet.json#/$defs/InputStatisticsInputDatasetFacet",
          "rowCount": 27
        }
      }
    }
  ],
  "outputs": [
    {
      "namespace": "warehouse://shop-warehouse",
      "name": "shop.analytics.clean_orders",
      "outputFacets": {
        "outputStatistics": {
          "_producer": "https://example.org/shop/jobs/tree/v1",
          "_schemaURL": "https://openlineage.io/spec/facets/1-0-2/OutputStatisticsOutputDatasetFacet.json#/$defs/OutputStatisticsOutputDatasetFacet",
          "rowCount": 23
        }
      }
    }
  ],
  "producer": "https://example.org/shop/jobs/tree/v1",
  "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"
}


The first event's `eventType` is `START`, and the second's is `COMPLETE`. A run that fails sends `FAIL` in place of `COMPLETE`.

`run.runId` is the run's identifier. The specification requires a UUID, a standard form of identifier. The shop makes UUIDs of version 7, which begin with the run's start time. The specification's documentation recommends that version.

A job is named by a **namespace** and a name inside it. Here the job `build_clean_orders` is named in the namespace `shop`.

A dataset is named the same way. `orders.jsonl` has the name `orders.jsonl` in the namespace `s3://shop-raw`, which is its bucket. `clean_orders` has the name `shop.analytics.clean_orders` in the namespace `warehouse://shop-warehouse`. That name holds the database `shop`, the schema `analytics` and the table `clean_orders`.

The `producer` field is the address of the program that made the event. Here it is `https://example.org/shop/jobs/tree/v1`. That program is the event's **producer**. The functions' events come from a second producer: the library of the platform the functions run on.

Further metadata comes in a **facet**: a named object. It holds `_producer`, then `_schemaURL` (the address of the facet's schema), then its own fields.

In these events, `inputStatistics` holds the rows read, 27. `outputStatistics` holds the rows written, 23. `sourceCodeLocation` holds the code version, `b178023`. `nominalTime` holds the time the run was due to start.

The `START` names the input and no output. The `COMPLETE` names the input again, with its row count, and adds the output.

The next cell lists where each of Chapter 7's fields went. 

```python
shop.openlineage.mapping()
```

[output]
field | in OpenLineage | 
run | run.runId | 
job | job.namespace and job.name | 
type | eventType: START, or COMPLETE or FAIL | 
time | eventTime | 
status | eventType: COMPLETE or FAIL | 
code_version | job.facets.sourceCodeLocation.version | 
reads | inputs | 
writes | outputs | 
rows_read | inputs[].inputFacets.inputStatistics.rowCount | 
rows_written | outputs[].outputFacets.outputStatistics.rowCount | 
object | run.facets.shop_objectChange.object | 
object_version | run.facets.shop_objectChange.version, and inputs[].facets.version.datasetVersion | 
object_change | run.facets.shop_objectChange.change |

## What a consumer knows

A program that receives events is a consumer. The cell after the next one sends the `START` alone to a consumer: the shop's own, a small one. It keeps one row for each run, and it adds to that row what each event says.

Before you read on, write in the next cell what the consumer knows about the run after the `START` alone, and what it knows about `clean_orders`. 

```python
expected = """
After the START alone, what does it know about the run?
........
What does it know about clean_orders?
........
"""
```

```python
consumer = shop.openlineage.Consumer()
consumer.send(friday[0])
consumer.runs()
```

[output]
job | state | started | ended | inputs | outputs | events | 
shop/build_clean_orders | START | 2026-09-11T02:05:00Z |  | s3://shop-raw/orders.jsonl |  | 1 |

The consumer writes each name as its namespace, then `/`, then the name. Its row has the state `START`, the start time, the input `orders.jsonl`, no output and no end time.

It knows that the run began, and what the run reads. It knows nothing about `clean_orders`, because the `START` names no output.

It cannot tell a run that is still working from one that stopped without sending another event.

The next cell sends the `COMPLETE`. 

```python
consumer.send(friday[1])
consumer.runs()
```

[output]
job | state | started | ended | inputs | outputs | events | 
shop/build_clean_orders | COMPLETE | 2026-09-11T02:05:00Z | 2026-09-11T02:05:52Z | s3://shop-raw/orders.jsonl | warehouse://shop-warehouse/shop.analytics.clean_orders | 2 |

The row now has the state `COMPLETE`, the end time `2026-09-11T02:05:52Z`, the output `warehouse://shop-warehouse/shop.analytics.clean_orders`, and 2 events.

The `COMPLETE` named the input again, and the consumer did not list it twice.

The specification says that events about one run add to each other. In its words: "All metadata is additive." A facet sent again under the same name replaces the earlier one.

The next cell sends every event of the week to a new consumer, and lists the runs whose state is `FAIL`. 

```python
everything = shop.openlineage.Consumer().send(*events)
everything.runs(state="FAIL")
```

[output]
job | state | started | ended | inputs | outputs | events | 
shop/build_daily_sales | FAIL | 2026-09-14T02:30:00Z | 2026-09-14T02:30:21Z | warehouse://shop-warehouse/shop.analytics.clean_orders |  | 2 |

The consumer holds 34 runs. One of them has the state `FAIL`: `build_daily_sales` on Monday 14. It has no output. 

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

```python
start = {
    "eventType": "START",
    "eventTime": "2026-09-11T02:15:00Z",
    "run": {"runId": shop.openlineage.uuid7("2026-09-11T02:15:00Z", "copy")},
    "job": {"namespace": "analyst", "name": "copy_clean_orders"},
    "inputs": [{"namespace": "warehouse://shop-warehouse", "name": "analytics.clean_orders"}],
    "outputs": [],
    "producer": "https://example.org/analyst/copy-script/v1",
    "schemaURL": shop.openlineage.SCHEMA_URL,
}
complete = {
    **start,
    "eventType": "COMPLETE",
    "eventTime": "2026-09-11T02:15:17Z",
    "outputs": [{"namespace": "s3://shop-scratch", "name": "clean_orders_copy.csv"}],
}
shop.openlineage.check(start)
```

[output]
The event breaks none of the specification's rules that the check tests.

The check finds no problems in `start`.

The cell after the next one sends the week's events and the analyst's two events to a new consumer, and follows edges upstream from the copy, `s3://shop-scratch/clean_orders_copy.csv`.

Before you read on, write in the next cell whether that traversal will reach `orders.jsonl`. 

```python
expected_join = """
Will the traversal reach orders.jsonl?
........
"""
```

```python
joined = shop.openlineage.Consumer().send(*events, start, complete)
joined.lineage().upstream("s3://shop-scratch/clean_orders_copy.csv")
```

[output]
node | type | steps | path | 
copy_clean_orders | job | 1 | s3://shop-scratch/clean_orders_copy.csv <-writes- copy_clean_orders | 
warehouse://shop-warehouse/analytics.clean_orders | dataset | 2 | s3://shop-scratch/clean_orders_copy.csv <-writes- copy_clean_orders -reads-> warehouse://shop-warehouse/analytics.clean_orders |

The traversal reaches 2 nodes, `copy_clean_orders` and `analytics.clean_orders`, and stops. It does not reach `orders.jsonl`.

The consumer joins two datasets only when their namespace and their name are the same. To the consumer, `analytics.clean_orders` and `shop.analytics.clean_orders` are two datasets.

In the cell that holds `start`, change `"analytics.clean_orders"` to `"shop.analytics.clean_orders"`. Select that cell and press **Run below**.

The traversal then reaches 4 nodes, through `build_clean_orders`, to `orders.jsonl`.

The specification's naming page gives a namespace and a name for each kind of data store it lists. It lists no form for a warehouse like the shop's, so the shop's producers must agree on one.

The page warns of the same failure for one data store it lists. Names made under Snowflake's older form of account name do not connect to names made under the newer form. 

## An event that breaks a rule

The next cell copies `start`, sets its `runId` to `"copy-friday"`, deletes its `producer`, and checks it. 

```python
broken = {**start, "run": {"runId": "copy-friday"}}
del broken["producer"]
shop.openlineage.check(broken)
```

[output]
where | problem | 
producer | Every run event needs this field, and the event does not have it. | 
run.runId | The run's identifier is not a UUID. |

The check lists 2 problems: `producer` is missing, and `run.runId` is not a UUID.

The shop's consumer refuses an event that breaks the rules, and keeps it aside. That is the shop's choice. The specification says what an event must hold. 

## "Our programs must emit OpenLineage."

The head of the shop set this requirement at the start of the chapter.

Before you read on, write in the next cell what you would check to say that the shop meets it. The same cell then counts, job by job, the runs and the events of each type. 

```python
reading = """
What would you check to say the shop meets the requirement?
........
"""
shop.openlineage.summary(events)
```

[output]
job | runs | START | COMPLETE | FAIL | 
shop/build_clean_customers | 7 | 7 | 7 | 0 | 
shop/build_clean_orders | 7 | 7 | 7 | 0 | 
shop/build_daily_sales | 7 | 7 | 6 | 1 | 
shop/refresh_dashboard | 7 | 7 | 7 | 0 | 
shop/record_return | 5 | 5 | 5 | 0 | 
shop/remove_return | 1 | 1 | 1 | 0 |

The counts show 6 programs that sent events: the four jobs and the two functions. Each run sent a `START`, then a `COMPLETE`, except the run of `build_daily_sales` on Monday 14, which sent a `FAIL`.

The requirement could mean several things, each needing something different:

- Which programs: the jobs and the functions send events. The export and the analyst's copy do not.
- Which events: the specification's schema requires one `START`, and one of `COMPLETE`, `ABORT` or `FAIL`, for each run. `RUNNING` and `OTHER` are optional.
- Which facets: the specification requires none. The shop sends some of the standard ones, and one of its own, `shop_objectChange`, for a function's file change. It is named with the shop's prefix, as the specification asks of a facet that is not standard.
- Which namespaces and names: the naming page's form for object storage, and the shop's own for its warehouse and its reporting tool.

As written, the shop meets the requirement for its jobs and its functions. Whether it means every program that touches the shop's data, or particular facets or names, the requirement does not say. 

## Before Chapter 9

The shop's runs now have OpenLineage's form. The consumer knew a run's input after its `START`, and its output only after its `COMPLETE`. A failed run sent a `FAIL`. An event written by hand passed the check, but two names for one table did not join until the analyst changed one. An event that broke two rules was refused.

The experiments could not show how a consumer keeps a week of events and turns them into a graph that answers questions. They could not show what a consumer does with a line it cannot read.

Chapter 9 builds that, one stage at a time, from the events as received to a graph.

- Which programs on a platform you work on would need to send events for its lineage to be whole?
- How should your platform name its warehouse's tables, and who must agree on the names?
- What should a consumer do with a `START` whose run never sends another event? 

### How this differs from a real platform

The shop, its programs, its producers and their addresses are invented for the course. The addresses at `example.org` lead nowhere.

The consumer is the shop's own, not a product. The OpenLineage documentation calls Marquez the reference implementation of its API. Chapter 29 compares real consumers.

The specification's schema and its page on the run cycle disagree on one point. The schema allows `OTHER` events after a run's `COMPLETE`, `ABORT` or `FAIL`. The run cycle page says no event follows those.

The namespaces `warehouse://shop-warehouse` and `reporting://shop-reporting` are the shop's choice.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 7](chapter_07.ipynb) · [Next: Chapter 9](chapter_09.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow 

