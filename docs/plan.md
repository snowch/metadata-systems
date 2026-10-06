# The course plan

What the course teaches, part by part and chapter by chapter, what the learner's lab holds after
each chapter, and what has been decided since the brief. It says what is planned, not what is
built: the list of chapters on the site shows which chapters exist, worked out from the lessons
themselves.

## What the learner can do at the end

Explain, and build in small, the machinery of a metadata platform:

- what metadata is, and why it is naturally a graph;
- what makes lineage different from other relationships, and why it needs jobs, runs and events;
- what an OpenLineage event tells a consumer, and how events become a lineage graph;
- why identity is hard, why lineage is incomplete, and what column lineage and schema evolution
  add;
- how metadata supports data quality, provenance, impact analysis and root-cause analysis;
- what breaks when events are missing, repeated, late or contradictory, and at scale;
- how real systems (OpenLineage producers, Marquez, OpenMetadata, DataHub, Atlas) are built;
- and how to build a simplified metadata platform themselves, because they have built one.

The course's last chapter asks for almost everything at once: model a small platform's metadata,
instrument its programs, capture lineage, ingest events, build the graph, track schema changes,
record quality observations, diagnose a failure, analyse an impact, and explain where a result
came from.

## The thesis

> Metadata describes what exists. Lineage describes how things become related through
> computation and change.

Three kinds of record, one model:

| Kind | Answers | Examples |
| --- | --- | --- |
| Descriptive | what an asset is | name, type, schema, owner, location, tags, meaning, classification |
| Operational | what happened | jobs, runs, times, status, inputs, outputs, row counts, freshness, quality observations |
| Lineage | what was made from what, by which computation, when | asset to asset, job to asset, run to asset, column to column, model to training data, dashboard to data |

Lineage is the time-and-process dimension of the same model. An edge in the lineage graph is a
claim that a computation read one thing and wrote another, and the claim carries the run that made
it and that run's time. The learner sees this by building it: the descriptive records of Part I
gain jobs and runs in Part II, and the graph that answers "who owns this?" is the graph that
answers "what does this depend on?".

## The lab

Every figure runs the Metadata Lab (`packages/lab`, described in `docs/lab.md`): a small online
shop's data platform that really runs. Three raw files arrive each night (`customers.parquet`,
`orders.parquet`, `products.parquet`); programs written in the course's SQL subset clean them
(`clean_customers`, `clean_orders`), add them up (`daily_sales`), and refresh a dashboard
(`sales_dashboard`). The course's week is Monday 7 to Sunday 13 September 2026, and the learner
arrives on Monday 14 September. On Thursday something went wrong, and the dashboard shows it.

The lab starts with deliberately too little information. Chapter 1 gives the learner storage and
nothing else. Each later chapter adds one kind of record, built by the learner, and the lab keeps
what they built: the lab a figure runs is the shop plus the learner's own graded work from every
earlier chapter (`docs/lab.md`, "The learner's state").

## How a chapter runs

Every chapter follows the loop **predict, build, run, inspect, explain, change, run again**, inside
the platform's ten sections: question, motivation, prediction, investigation, construction,
failure experiment, explanation, generalisation, challenge, reflection. A chapter is finished when
the learner can do something they could not reliably do before, and every major idea in it has an
explanation, a concrete example, an experiment, a prediction, an observable result, a reflection
and an application.

## The parts

Each table gives, per chapter: what the learner builds into the lab; the central experiment; what
the chapter deliberately breaks; and the terms it introduces, which no earlier chapter may use
(the term gate). Terms in plain English (owner, file, table, program) are not rationed.

### Part I: Why metadata exists

The learner meets a platform that keeps its data and almost nothing about it, and builds the first
records about it.

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 1 | The invisible data system | nothing yet: storage is all there is | reproduce `daily_sales` from the other assets with a query, and recover the rules that make `clean_orders` from `orders` | an analyst's copy makes two sources fit; a changed program makes some days stop matching with no trace; a failed night looks like a quiet one | asset, metadata |
| 2 | What is metadata? | descriptive records for the shop's assets: meaning, owner, columns with their meaning and unit | ask Chapter 1's questions again of storage plus the records, and see which become answerable | a column in `products` that names a person is data about the business, not a record about the file; a record nobody updates goes stale while storage moves on | descriptive, operational, schema |
| 3 | Metadata as a model | entity types, attributes, identifiers and relationship types; the records checked against them | merge two records that spell the same owner differently | a reference to an entity that does not exist; a fact the model has no type for | entity, attribute, identifier, dataset |
| 4 | Metadata as a graph | the model as nodes and edges; traversals | predict what a traversal returns, then run it | a traversal that follows the wrong kind of edge and returns half the shop | graph, node, edge, traversal |

### Part II: Lineage

The learner records what was made from what, discovers that a declared dependency is not an
observed one, and designs the event a computation should emit before meeting OpenLineage.

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 5 | What is lineage? | "made from" edges through jobs: A to job to B, then a chain of two jobs; dependency and impact queries | predict everything affected if `orders.parquet` changes | a hand-written dependency that the program does not have; a declared edge that went stale when the program changed | lineage, job, upstream, downstream |
| 6 | Jobs, runs and events | a run per execution, with its times, status, inputs, outputs and code version; the learner designs the event a run emits | predict what the job's record alone cannot say about Thursday, then read the runs | an event with no run identifier merges two nights; an event with no inputs proves nothing | run, event |
| 7 | OpenLineage | the learner's events as OpenLineage run events: START, COMPLETE and FAIL, a run's UUID, a job's namespace and name, inputs, outputs, facets; create, edit and replay | predict what a consumer knows after a START with no outputs and a COMPLETE with outputs | two producers name the same table differently and the lineage does not join | OpenLineage, facet, namespace, producer |
| 8 | From events to graphs | the ingestion pipeline: parse, normalise, metadata objects, graph edges, each stage built and run over the week's events | predict how many nodes and edges the week produces | a malformed event; a facet the parser does not know | ingestion, normalise |

### Part III: Deeper lineage

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 9 | Column-level lineage | the course's SQL parsed into column derivations; `revenue` from `price` and `quantity` | predict which source columns `revenue` depends on, including through the filter on `status` | `SELECT *`; an alias chain; a function the parser cannot see into | column lineage |
| 10 | Schema evolution | schema versions; added, removed, renamed and retyped columns, followed downstream | predict which changes break `daily_sales` | a rename that looks like a drop and an add; a type change that truncates | schema evolution, breaking change |
| 11 | Identity | the identity laboratory: rules over namespace, name, environment and version | predict whether two references are the same asset | case, a path through a link, production and development collapsing into one | identity, qualified name, environment |
| 12 | Runtime metadata | observations from execution: duration, status, rows, bytes, errors, freshness | predict which asset is stale on Monday morning after a failed night | a run that succeeded and wrote no rows; two clocks that disagree | observation, freshness |

### Part IV: Metadata becomes operational

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 13 | Data quality as metadata | quality observations per run (rows, missing customer ids, duplicate orders) and assertions over them | predict which night fails "no order without a customer" | an assertion that passes because the rows it should catch were filtered first | data quality, assertion |
| 14 | Provenance | a query from a figure on the dashboard back to the rows, the program and the run behind it | predict which orders make up Thursday's revenue | provenance through a sum is a set; a source overwritten since the run | provenance |
| 15 | Impact analysis | impact queries over dataset and column lineage | rename `orders.customer_id`: predict what breaks, then ask the graph | a reader the graph never heard of: the analysis is only as complete as the lineage | impact analysis |
| 16 | Root-cause analysis | a backwards search over lineage, runs, observations and changes | start from "the dashboard is wrong" and find where Thursday's fault entered | two plausible causes; a cause outside the recorded system | root cause |

### Part V: When the simple model breaks

The learner runs the lab's events through a delivery path that loses, repeats, delays and
contradicts them, and makes their metadata system survive it.

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 17 | Missing events | a delivery path between producers and the collector, with loss | predict the graph when one COMPLETE never arrives | a run that is running for ever; a dependency nobody can prove | delivery, at least once |
| 18 | Duplicate events | idempotent ingestion | replay an event: predict whether the lineage doubles | a retry whose event differs in time only | idempotent, deduplication |
| 19 | Out-of-order events | event time against arrival time, and an ordering rule | deliver Tuesday's run after Wednesday's | last-writer-wins by arrival overwrites newer state | event time, arrival time |
| 20 | Conflicting metadata | precedence rules that keep where each claim came from | two systems disagree about an owner and a schema: predict which the lab shows | "newest wins" chooses a stale claim | precedence |
| 21 | Identity across systems | aliases and resolution rules across the warehouse, a file path, a transformation tool's model name and the dashboard's dataset | predict which references merge | over-merging two environments' tables of one name | alias, entity resolution |
| 22 | Metadata at scale | a cost model from ten assets to ten million and billions of events: indexes, partitions, retention, compaction, ingestion rate, traversal depth | predict which query fails first as the platform grows | an unbounded traversal; retention that deletes the lineage of an asset still in use | index, partition, retention, compaction |

### Part VI: Building a metadata platform

The learner implements the parts their lab has been using, against tests, in the order data flows
through them.

| Ch | Title | The learner builds |
| --- | --- | --- |
| 23 | Build the metadata store | JSON documents, then tables, then an indexed store, then a graph representation, each passing the same tests |
| 24 | Build the event collector | validation, deduplication, ordering and persistence, run against the week's events with Part V's faults |
| 25 | Build the lineage graph | persistent, time-stamped edges from stored events |
| 26 | Build the query layer | what depends on X, where did X come from, who owns X, which assets are stale, which jobs failed, what a schema change affects |
| 27 | Build the metadata interface | an asset browser, a graph explorer, a lineage view, run history, schema history, quality observations and impact analysis, as views of the learner's own store |

Chapter 24 introduces *collector*. Part VI introduces no other new terms, because it builds what
Parts I to V named.

### Part VII: Real systems

| Ch | Title | What it connects |
| --- | --- | --- |
| 28 | OpenLineage in practice | real producers and the reference consumer, real events and facets, against the learner's own collector |
| 29 | Airflow, Spark, dbt and Trino | where each system's metadata comes from: a scheduler's task instances, an engine's query plan, a transformation tool's manifest and run results, a query engine's events |
| 30 | Metadata platforms | the architectures of OpenMetadata, DataHub, Apache Atlas and Marquez compared: how metadata arrives (pushed or pulled), how it is modelled, stored, indexed and served |
| 31 | Metadata for ML and AI | training data to training run to model to evaluation to deployment to inference; features, experiments, embeddings, vector indexes, retrieval systems and generated artefacts |

### Part VIII: The complete system

| Ch | Title | The learner does |
| --- | --- | --- |
| 32 | Build the whole thing | receive a second, unfamiliar platform and model it, instrument it, capture and ingest its lineage, track its schemas and quality, diagnose a failure, analyse an impact and explain a result's provenance |

## What the learner writes

- **Choices in a figure** (Chapter 1 on): a query built from choices, a rule set, a change to
  apply. The lab shows the SQL a choice means.
- **Records** (Chapter 2 on): descriptive records in a small, line-based notation the lab parses
  and checks; JSON from Chapter 6.
- **The course's SQL subset** (Chapter 9 on, read from Chapter 1): `SELECT` with expressions,
  `DISTINCT`, `WHERE`, `GROUP BY`, `ORDER BY`, `CAST`, a few functions, and named parameters. The
  lab's programs are written in it, the lab runs it, and Chapter 9 derives column lineage from
  its parse.
- **Events** (Chapters 6 to 8): JSON, first in the learner's own design, then as OpenLineage run
  events.
- **Code** (Part VI): to be decided at checkpoint 2. Recommendation: JavaScript run in a Web
  Worker against tests, because it runs in every browser with no download; Python under Pyodide is
  the alternative a data engineer might prefer, at about ten megabytes per visit.

## OpenLineage, placed

OpenLineage appears in Chapter 7, after the learner has designed an event from the problem in
Chapter 6, and returns in Chapters 8, 17 to 19 and 28. What the course states about it is checked
against the specification (`docs/sources.md`), and the specification's silences are named as
silences: it requires a START and one terminal event per run and says events about a run
accumulate, but it does not say what a consumer must do with a duplicate, a late or a missing
event. Part V is about exactly those silences.

## The checkpoints

The author reviews the course at five checkpoints:

1. After Chapter 1, the plan, the lab's design and the platform move (now).
2. After Chapter 8: the event model and OpenLineage are in place, and the language of Part VI is
   decided.
3. After Chapter 16: metadata is operational.
4. After Chapter 22: the failure chapters.
5. Before Chapter 32.

## Decisions since the brief

### 6 October 2026: the course's frame

1. **Title.** *Metadata Systems: From Raw Files to a Working Metadata Platform*, in the pattern of
   the author's digital-design course.
2. **The shop.** An online shop that sells bicycle parts, invented for the course. It is not dbt's
   jaffle shop (a café with customers, orders and payments, laid out as staging and marts); this
   shop has no payments table, has a dashboard, keeps its raw files in object storage and its
   cleaned tables in a warehouse, and its programs are the lab's own SQL.
3. **The week.** Monday 7 to Sunday 13 September 2026; the learner arrives on Monday 14
   September. On Thursday the shop's checkout sent orders with no customer id, and the rule in
   `clean_orders` that drops such orders made Thursday's revenue low. Chapter 1 shows the symptom,
   Chapter 13 measures it, Chapter 14 traces it and Chapter 16 finds it.
4. **The platform moved.** The lesson schema, the runtime and the primitives moved from
   `snowch/digital-design` to `snowch/learning-platform` when this course became their second
   consumer, as the digital-design inventory's section 5.7 planned. `docs/platform.md` says what
   moved, what was generalised and how this course takes the code.
5. **The lab's state is derived, not stored.** What the learner built in earlier chapters reaches
   later chapters by grading their stored work again, never through a separate store a learner
   could edit into a pass (`docs/lab.md`).
6. **The lab has its own SQL subset.** One notation for the programs the learner reads in Chapter
   1, the column lineage of Chapter 9 and the queries of Part VI, as the digital-design course has
   one hardware description subset.
