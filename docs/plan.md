# The course plan

What the course teaches, part by part and chapter by chapter, what the learner's metadata system holds after
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
- and how to build a simplified metadata platform themselves, because they have built one;
- and, at the end, how to build the metadata and lineage process for a platform of a common
  kind: data that lands in object storage, functions that run when objects are created,
  overwritten or deleted, scheduled jobs beside them, and results queried as tables. Chapter 33
  asks them to do it for one they have not seen.

Beside all of this, the learner leaves with a habit: when a requirement sounds obvious, ask what it
actually means. They can say what a requirement literally asks, what it might mean, what each
meaning needs, what a platform actually records, and whether that record meets it (`CLAUDE.md`,
"Question the requirement").

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

## The engine

Every chapter is a Jupyter notebook that runs in the browser, and every figure in it is computed
by the engine (`notebook/shop`, in Python, described in `docs/lab.md`): a small online shop's
data platform that really runs. The page never names it: a figure is a diagram or a figure of the
shop's data, with a caption and no badge, mark or note (`CLAUDE.md`, "No lab on the page"). Three
raw files arrive each night (`orders.jsonl`, `customers.jsonl`, `products.csv`); programs in SQL
clean them (`clean_customers`, `clean_orders`), add them up (`daily_sales`), and refresh a
dashboard (`sales_dashboard`). The course's week is Monday 7 to Sunday 13 September 2026, and the learner
arrives on Monday 14 September. On Thursday something went wrong, and the dashboard shows it.

A diagram of the platform opens each chapter: the systems in the order data moves through them,
the assets each holds, and between them the programs the learner cannot yet see. In Chapter 2 it
shows no link from one asset to another, because that is what the chapter finds
storage cannot tell. As the learner builds records in later chapters, the map gains what those
records hold, and a link appears on it only once something the learner built records it.

The shop's platform starts with deliberately too little information. Chapter 2 gives the learner
storage and nothing else. Each later chapter adds one kind of record, built by the learner; how
a later notebook gets what the learner built earlier is for the first chapter that needs it to
decide (`docs/lab.md`, "The learner's state").

## How a chapter runs

Every chapter follows the loop **predict, build, run, inspect, explain, change, run again**, in
sections that follow its material, each headed by its subject. Read as the learner meets
it, the loop asks: a real question; what can I believe about it now; predict; act on the figure;
observe; what did that prove; what can the data not tell me; what would a system have to record.
A prediction is built around what the learner should learn, asks for a belief about a result the
learner can observe, and never asks for a cause before its effect has been seen (`CLAUDE.md`).
Every figure's notes say whether it is a diagram, a figure of the shop's data or an experiment;
an experiment is preferred where the learner must act, and a figure of the shop's data always has
a question in front of it. A chapter is finished when
the learner can do something they could not reliably do before, and every major idea in it has an
explanation, a concrete example, an experiment, a prediction, an observable result, a reflection
and an application.

## The parts

Each table gives, per chapter: what the learner builds; the central experiment; what
the chapter deliberately breaks; and the terms it introduces, which no earlier chapter may use
(the term gate). Terms in plain English (owner, file, table, job) are not rationed: *job* is the everyday word for
what runs each night from Chapter 1, and Chapter 6 makes it precise as a node in the lineage graph.

### Part I: Why metadata exists

The learner meets a platform that keeps its data and almost nothing about it, and builds the first
records about it.

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 1 | The shop and its platform | nothing yet: storage is all there is | a tour, in a notebook: the shop's files, the warehouse's tables, the dashboard and the nights, with the head of the shop's one line in front of it, and a guess, written down, at which asset each table is made from | nothing: the chapter shows what the platform holds, and what it does not show: the programs, when they are due to run, and any notes | asset |
| 2 | The invisible data system | nothing yet: storage is all there is | an essay in a notebook: a query over `clean_orders` reproduces `daily_sales` and explains Thursday, and three changes show what that does and does not establish | an analyst's copy makes two sources fit; an edited program leaves nothing that fits and no trace; a failed night leaves the dashboard looking up to date over a table a day behind | metadata |
| 3 | What is metadata? | descriptive records for the shop's assets: meaning, owner, columns with their meaning and unit | ask Chapter 2's questions again of storage plus the records, and see which become answerable | a column in `products` that names a person is data about the business, not a record about the file; a record nobody updates goes stale while storage moves on | descriptive, operational, schema |
| 4 | Metadata as a model | entity types, attributes, identifiers and relationship types; the records checked against them | merge two records that spell the same owner differently | a reference to an entity that does not exist; a fact the model has no type for | entity, attribute, identifier, dataset |
| 5 | Metadata as a graph | the model as nodes and edges; traversals | predict what a traversal returns, then run it | a traversal that follows the wrong kind of edge and returns half the shop | graph, node, edge, traversal |

### Part II: Lineage

The learner records what was made from what, discovers that a declared dependency is not an
observed one, and designs the event a computation should emit before meeting OpenLineage.

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 6 | What is lineage? | "made from" edges through jobs: A to job to B, then a chain of two jobs; dependency and impact queries | predict everything affected if `orders.jsonl` changes | a hand-written dependency that the job does not have; a declared edge that went stale when the job changed | lineage, upstream, downstream |
| 7 | Jobs, runs and events | a run per execution, with its times, status, inputs, outputs and code version, and for a run started by an object, the object, its version and what happened to it (created, overwritten, deleted); the learner designs the event a run emits | predict what the job's record alone cannot say about Thursday, then read the runs | grouping events without a run identifier merges two runs of a function on one day; an event with no inputs proves nothing | run, event |
| 8 | OpenLineage | the learner's events as OpenLineage run events: START, COMPLETE and FAIL, a run's UUID, a job's namespace and name, inputs, outputs, facets; create, edit and replay | predict what a consumer knows after a START with no outputs and a COMPLETE with outputs | two producers name the same table differently and the lineage does not join | OpenLineage, facet, namespace, producer |
| 9 | From events to graphs | the ingestion pipeline: parse, normalise, metadata objects, graph edges, each stage built and run over the week's events | predict how many nodes and edges the week produces | a malformed event; a facet the parser does not know | ingestion, normalise |

### Part III: Deeper lineage

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 10 | Column-level lineage | the course's SQL parsed into column derivations; `revenue` from `price` and `quantity` | predict which source columns `revenue` depends on, including through the filter on `status` | `SELECT *`; an alias chain; a function the parser cannot see into | column lineage |
| 11 | Schema evolution | schema versions; added, removed, renamed and retyped columns, followed downstream | predict which changes break `daily_sales` | a rename that looks like a drop and an add; a type change that truncates | schema evolution, breaking change |
| 12 | Identity | the identity laboratory: rules over namespace, name, environment and version | predict whether two references are the same asset | case, a path through a link, production and development collapsing into one | identity, qualified name, environment |
| 13 | Runtime metadata | observations from execution: duration, status, rows, bytes, errors, freshness | predict which asset is stale on Monday morning after a failed night | a run that succeeded and wrote no rows; two clocks that disagree; a table the returns function writes at any hour, which no nightly time describes | observation, freshness |

### Part IV: Metadata becomes operational

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 14 | Data quality as metadata | quality observations per run (rows, missing customer ids, duplicate orders) and assertions over them | predict which night fails "no order without a customer" | an assertion that passes because the rows it should catch were filtered first | data quality, assertion |
| 15 | Provenance | a query from a figure on the dashboard back to the rows, the program and the run behind it | predict which orders make up Thursday's revenue | provenance through a sum is a set; a source overwritten since the run, as a return corrected after the function read it | provenance |
| 16 | Impact analysis | impact queries over dataset and column lineage | rename `orders.customer_id`: predict what breaks, then ask the graph | a reader the graph never heard of: the analysis is only as complete as the lineage; a deleted return, and what was made from it | impact analysis |
| 17 | Root-cause analysis | a backwards search over lineage, runs, observations and changes | start from "the dashboard is wrong" and find where Thursday's fault entered | two plausible causes; a cause outside the recorded system | root cause |

### Part V: When the simple model breaks

The learner runs the shop's events through a delivery path that loses, repeats, delays and
contradicts them, and makes their metadata system survive it.

| Ch | Title | The learner builds | Central experiment | What breaks | Introduces |
| --- | --- | --- | --- | --- | --- |
| 18 | Missing events | a delivery path between producers and the collector, with loss | predict the graph when one COMPLETE never arrives | a run that is running for ever; a dependency nobody can prove | delivery, at least once |
| 19 | Duplicate events | idempotent ingestion | replay an event: predict whether the lineage doubles | a retry whose event differs in time only; an object's trigger delivered twice, which runs the returns function twice | idempotent, deduplication |
| 20 | Out-of-order events | event time against arrival time, and an ordering rule | deliver Tuesday's run after Wednesday's | last-writer-wins by arrival overwrites newer state; a return's delete delivered before its create | event time, arrival time |
| 21 | Conflicting metadata | precedence rules that keep where each claim came from | two systems disagree about an owner and a schema: predict which the figure shows | "newest wins" chooses a stale claim | precedence |
| 22 | Identity across systems | aliases and resolution rules across the warehouse, a file path, a transformation tool's model name and the dashboard's dataset | predict which references merge | over-merging two environments' tables of one name | alias, entity resolution |
| 23 | Metadata at scale | a cost model from ten assets to ten million and billions of events, one run per object among them: indexes, partitions, retention, compaction, ingestion rate, traversal depth | predict which query fails first as the platform grows | an unbounded traversal; retention that deletes the lineage of an asset still in use | index, partition, retention, compaction |

### Part VI: Building a metadata platform

The learner implements the parts the engine has been using, against tests, in the order data flows
through them.

| Ch | Title | The learner builds |
| --- | --- | --- |
| 24 | Build the metadata store | JSON documents, then tables, then an indexed store, then a graph representation, each passing the same tests |
| 25 | Build the event collector | validation, deduplication, ordering and persistence, run against the week's events with Part V's faults |
| 26 | Build the lineage graph | persistent, time-stamped edges from stored events |
| 27 | Build the query layer | what depends on X, where did X come from, who owns X, which assets are stale, which jobs failed, what a schema change affects |
| 28 | Build the metadata interface | an asset browser, a graph explorer, a lineage view, run history, schema history, quality observations and impact analysis, as views of the learner's own store |

Chapter 25 introduces *collector*. Part VI introduces no other new terms, because it builds what
Parts I to V named.

### Part VII: Real systems

| Ch | Title | What it connects |
| --- | --- | --- |
| 29 | OpenLineage in practice | real producers and the reference consumer, real events and facets, against the learner's own collector |
| 30 | Airflow, Spark, dbt and Trino | where each system's metadata comes from: a scheduler's task instances, an engine's query plan, a transformation tool's manifest and run results, a query engine's events |
| 31 | Metadata platforms | the architectures of OpenMetadata, DataHub, Apache Atlas and Marquez compared: how metadata arrives (pushed or pulled), how it is modelled, stored, indexed and served |
| 32 | Metadata for ML and AI | training data to training run to model to evaluation to deployment to inference; features, experiments, embeddings, vector indexes, retrieval systems and generated artefacts |

### Part VIII: The complete system

| Ch | Title | The learner does |
| --- | --- | --- |
| 33 | Build the whole thing | receive a second, unfamiliar platform, built not on a nightly batch but on object storage whose changes start functions, with scheduled jobs beside them and tables over the results, and model it, instrument its functions and jobs, capture and ingest its lineage (per object and per version, deletions included), track its schemas and quality, diagnose a failure, analyse an impact and explain a result's provenance |

## Questioning the requirement, chapter by chapter

A candidate for each chapter: a requirement that sounds settled in that chapter's material, and
the questions it could be asking. Each chapter confirms or replaces its own when it is written,
and its notes say which (`CLAUDE.md`, "Question the requirement").

| Ch | A requirement that sounds settled | What it could be asking |
| --- | --- | --- |
| 1 | none: the chapter tours what the platform holds, and leaves its first requirement to Chapter 2 | |
| 2 | "Every table must have an owner." (questioned in the prose) | who is responsible for it; which team is; which job writes it; which account controls it in the warehouse |
| 3 | "Every column must have a description." | what the column means; its unit; where its values come from; whether it may be empty. A description that repeats the column's name meets it as written |
| 4 | "Each asset has one owner." | one person, one team, or one identifier for an owner two records spell differently |
| 5 | "Show everything related to `daily_sales`." | what it is made from; what reads it; who is responsible for it; where it is kept. Each is a different kind of edge |
| 6 | "Record the lineage of `daily_sales`." | what its job declares it reads, what it was seen to read, or both; between tables or between columns |
| 7 | "Record every run." | to find failures; to know when an asset was last written; to audit who changed what; to know which object started it. Each needs a different event |
| 8 | "Our programs must emit OpenLineage." | which events, with which facets, under which namespace and name |
| 9 | "The graph must show the current lineage." | current as of the last event received, the last run, or the last change to a program |
| 10 | "Show which columns `revenue` depends on." | the columns its value is computed from, or also those that decide which rows count, such as `status` |
| 11 | "Warn us of breaking changes." | breaking for which reader: a program that reads by name, the dashboard, somebody's own query |
| 12 | "The same table must have one identity." | the same name, the same rows, the same environment, or the same version |
| 13 | "The dashboard must be fresh." | refreshed lately; built from the latest data; showing the latest day. Chapter 2's failed night met the first and neither of the others |
| 14 | "No order without a customer." | in the raw file, in `clean_orders`, or on the dashboard. An assertion on `clean_orders` passes because the rows were filtered first |
| 15 | "Show where Thursday's figure came from." | the rows; the program; the run; the rows as they were when the run read them |
| 16 | "Tell us what breaks if `customer_id` is renamed." | what fails, or also what keeps running and gives a wrong answer. A second candidate, from the returns: "When a return is deleted, remove everything made from it": its row, the totals that counted it, copies, or also what was already reported |
| 17 | "Find the cause of the wrong figure." | where the data first went wrong; the change that did it; the decision behind that change |
| 18 | "Lineage must be complete." | complete for the programs that send events, or for every program that touches the data |
| 19 | "Ingestion must ignore duplicates." | the same event twice; the same run reported twice; the same content at another time |
| 20 | "Show the latest state of each run." | latest by when it happened, or by when it arrived |
| 21 | "Show the correct owner." | the newest claim; the claim from the most trusted system; every claim with where it came from. Chapter 2's owner returns |
| 22 | "Merge the same dataset across systems." | the same name, the same rows, or the same thing to the business; across environments or not |
| 23 | "Keep lineage for 90 days." | 90 days of events, of edges, or of whatever assets still in use depend on |
| 24 to 28 | the learner's own query layer must answer "who owns X?" (Chapter 27) | whichever meaning the learner's records keep, and the query layer says which |
| 29 | "Use the reference consumer." | what the specification requires, against what one implementation does |
| 30 | "Capture lineage from Airflow, Spark, dbt and Trino." | each system's own meaning of a task, a run and an input |
| 31 | "Choose a metadata platform that tracks ownership." | each platform's own meaning of an owner, compared from its documentation |
| 32 | "Record the training data of the model." | the snapshot it read; the query that chose it; the features computed from it |
| 33 | the unfamiliar platform's own requirements | the learner questions each before building to it |

## What the learner writes

- **Changes to a cell** (Chapter 2 on): a query to edit, a change to the week to choose from a
  menu, a note to write. The cell shows what it ran and what it found.
- **Records** (Chapter 3 on): descriptive records in a small, line-based notation the engine parses
  and checks; JSON from Chapter 7.
- **SQL** (read from Chapter 1, written from Chapter 2): SQLite's, which the shop's programs are
  written in and the engine runs. Chapter 10 derives column lineage from a parse of the programs'
  SQL; which subset it parses is that chapter's decision.
- **Events** (Chapters 7 to 9): JSON, first in the learner's own design, then as OpenLineage run
  events.
- **Code** (every chapter's cells, and Part VI's own programs): Python, run in the browser by
  Pyodide, decided at checkpoint 1 because the learner reads and writes this code and Python is a
  data engineer's language. The engine is Python too, in the same kernel. The site serves Pyodide
  and every package a notebook loads from its own address, so nothing is fetched from a third
  party, and each package's licence is checked in the build (`notebook/licences.py`).

## OpenLineage, placed

OpenLineage appears in Chapter 8, after the learner has designed an event from the problem in
Chapter 7, and returns in Chapters 9, 18 to 20 and 29. What the course states about it is checked
against the specification (`docs/sources.md`), and the specification's silences are named as
silences. For a batch job it expects a START and one terminal event per run, and events about a
run accumulate; a streaming job or a service may never send a terminal event and instead sends
periodic snapshots of a time window. It does not say what a consumer must do with a duplicate, a
late or a missing event. Part V is about exactly those silences. Its schema and its run-cycle
page also disagree on whether an `OTHER` event may follow a terminal one, and the course says so.

## The checkpoints

The author reviews the course at five checkpoints:

1. After Chapter 2, the plan, the engine's design and the platform move (now).
2. After Chapter 9: the event model and OpenLineage are in place.
3. After Chapter 17: metadata is operational.
4. After Chapter 23: the failure chapters.
5. Before Chapter 33.

## Decisions since the brief

### 12 October 2026: Chapters 5 and 6 written

The author asked for Chapters 5 and 6. Both keep their rows. Chapter 5's reader turns Chapter 4's
records into a graph (each entity a node, each line naming another entity an edge), predicts
traversals before running them, changes a traversal's direction and runs it again, and finds that a
traversal along every edge reaches the dashboard for the wrong reason (a shared person responsible)
and misses `clean_orders`, whose `drops` line Jo Marsh's question is about; the requirement is "Show
everything related to `daily_sales`.". Chapter 6's reader gets the jobs' code in a repository, to
answer the developer's rename, and sees the platform's map gain arrows, drawn from lines of what
each job reads and writes; finds that the traversal downstream is the most a rename could affect,
and the code which job names the column; adds Jo's belief as a line and refutes it against the code,
which also answers Jo; and sees a line written from today's code go stale when the code changes,
while the rows of `daily_sales` show nothing; the requirement is "Record the lineage of
`daily_sales`.". Both were revised after an outside review (their notes, "The review"). Decisions
the plan did not make:

- **The jobs' code becomes visible in Chapter 6**, in a repository the head of the shop opens. It is
  the course's small notation around the SQL the week runs (`docs/lab.md`, "The repository"), so the
  code cannot drift from what runs. The export and anything done by hand stay outside it, which is
  how the chapter shows lineage to be only as complete as its lines.
- **Lineage by hand, then against code; what ran is Chapter 7's.** The chapter's stale line is
  found by comparing the lines with the code as it is now; which nights read which source is left
  for the records Chapter 7 makes, as the plan's order requires.
- **A fifth change**, `source`, for the stale line: from Saturday the daily sales job reads the
  analyst's copy, with the same rows.

### 12 October 2026: the end goal, a metadata and lineage process for an event-driven platform

The author asked that the course leave the reader able to build an end-to-end metadata and lineage
process on top of a platform of the kind that reacts to object storage, without naming a product
and without setting out what one platform supports less well than another. The course's end goals
("What the learner can do at the end") gain it, and Chapter 33's unfamiliar platform is now of that
kind: data landing in object storage, functions started when objects are created, overwritten or
deleted, scheduled jobs beside them, and tables over the results. The returns desk (the decision
below) is the small case the reader meets from Chapter 7 on.

No product is named for it, so the course makes no claim about one, favourable or not. Part VII is
unchanged: Chapter 30's systems are a scheduler and three engines, Chapter 31's are metadata
platforms, and neither compares a storage platform with another. The course's premise treats every
platform alike: each system records what its own work needs (Chapter 2), and what it does not
record is what the reader builds on top. Any claim the course does make about a real system is
still checked against that system's own documentation (`CLAUDE.md`, "Accuracy").

### 12 October 2026: processing started by objects, as a use case of the shop's

The author asked whether the course covers metadata for processing that reacts to object storage:
a function that runs when an object is created, overwritten or deleted, and the lineage and
metadata such processing needs. It did not: every job in the shop runs on the nightly schedule.
The author asked for it as a use case, not as a product, so no product is named; the shop gains it.

- **The use case.** The shop's returns desk records each return as one small object in a bucket of
  its own, `shop-returns`, at the time of the return, any hour of the day. Creating an object starts
  a function that writes the return into a warehouse table, `returns`; overwriting it (a corrected
  return) starts the function again; deleting it (a return withdrawn) starts a function that removes
  the row. Nothing about these runs is on a schedule. It is a change to the shop (`returns`, in
  `docs/lab.md`), run by the chapters that need it, so Chapters 1 to 4 are unchanged.
- **What it gives the planned chapters**, each in its row above: Chapter 7's run started by an
  object, which must record the object, its version and what happened to it; Chapter 13's
  freshness when writes happen at any hour; Chapter 15's provenance through a return corrected
  after the function read it; Chapter 16's impact of a deletion, with a second candidate
  requirement ("When a return is deleted, remove everything made from it"); Chapters 19 and 20's
  duplicated and reordered delivery one layer down, where a trigger delivered twice runs the
  function twice and a delete can arrive before its create; Chapter 23's one run per object.
- **What the engine must gain first** (`docs/lab.md`, "Planned: the returns desk"): writes at any
  time, not only at night; an object's versions; the platform's own notifications of object
  changes, which start the functions and which the platform does not show; and a delivery of
  those notifications that the chapters can make lose, repeat or reorder. It is built with
  Chapter 7, the first chapter that uses it, with tests, not before.
- **Accuracy.** How real object stores deliver such notifications (whether at least once, whether
  in order, what they carry) is a claim about a system, checked in its own documentation and
  recorded in `docs/sources.md` by the chapter that states it. Until then the shop's delivery is
  the shop's own choice, and the chapters' model-versus-reality notes say so.

### 12 October 2026: Chapters 3 and 4 written

The author asked for Chapters 3 and 4. Both are notebooks in Chapter 2's form, prose with cells,
and each keeps the plan's row: Chapter 3's reader writes a record of `daily_sales` from what the
shop's people say, asks Chapter 2's four questions of it, meets `updated_by` (a column that names
people and is data, not a record about the file), questions "Every column must have a
description.", and watches a record go stale; Chapter 4's reader counts owners and finds spellings,
writes a model of types, attributes and identifiers, merges the two spellings of Jo Marsh, meets a
value that names nothing and a fact the model has no type for, and questions "Each asset has one
owner." Where Chapters 1 and 2 ask for nothing to be predicted, these ask the reader to write an
expectation in a cell before the cells that answer it, which **Save** keeps, as Chapter 1's
guesses are kept; nothing grades it. Two decisions the plan did not make:

- **Records are lines of text in notations of the course's own**, `asset [column] field: value` in
  Chapter 3 and `type identifier attribute: value` in Chapter 4, with a model of
  `type attribute: text | type or type` lines. Line notations keep a record readable and editable
  on a phone, avoid any product's format (dbt's YAML, a catalogue's JSON), and let Chapter 4 grow
  out of Chapter 3's by one word at the start of each line (`docs/lab.md`, "What a notebook can ask
  of the engine").
- **A fourth change**, `column`: from Saturday's row, `daily_sales` gains `order_count`. With
  Chapter 2's edited job it is Chapter 3's stale-record experiment: the check sees the column, not
  the changed meaning.

The people the chapters add (Jo Marsh, in finance, who built the dashboard and is the reporting
tool's `j.marsh`; Sam Lund, who keeps the catalogue and is `s.lund` in `updated_by`; the staff list)
are invented for the course. `docs/notes/chapter-03.md` and `chapter-04.md` have the figures'
blocks, the requirements, the originality notes and what the prose process caught.

### 12 October 2026: two outside reviews of Chapters 1 and 2

Two reviewers read both chapters; the author accepted their findings, and Haiku drafted the
changed text from brief BG (`docs/notes/chapter-01/briefs/BG-two-reviews.md`).

- **The warning comes after the opening.** Each chapter opens with the situation, the platform and
  the week; the warning follows, with one line always shown (about 13 MB, the first time) and its
  time and memory folded into a `details` section the reader opens.
- **Chapter 1 is pitched at a data engineer.** It no longer explains how a CSV file names its
  columns or what JSON's types are; it keeps the two facts the chapters use (`products.csv` stores
  every value as text, a JSON Lines date is a string). Its objectives are framed around what you
  must establish before you can look into the reported discrepancy, and a line before the tour
  says what to note in each file.
- **The guesses have a place.** Chapter 1 ends with a code cell holding the learner's three guesses
  in a string, kept by Save as the handover note is; a widget's text is not.
- **The record before its description.** Chapter 2's "What the platform holds" shows the two cells
  that read `information_schema` first and states what they showed after.
- **Each change mapped to its record.** Chapter 2 says which record would have answered each of its
  three changes: what the job read (the analyst's copy), which version of the job's code ran (the
  edit), whether each night's write succeeded (the failed night).
- **The course's arc is named once.** The reviewers found a reader could not see where the course
  goes. Chapter 2's closing paragraph names Chapter 6's record of what was made from what, "which is
  called lineage", and Chapter 7's record of "each run of a job". Both are rationed terms of later
  chapters; the term gate exempts that one paragraph, and a test holds each word to one use there.
  Chapter 2 keeps both figures the second reviewer thought repeated Chapter 1's: the platform and
  the dashboard are what its questions are asked of.

### 11 October 2026: figures drawn into the page, not by code cells

Each figure was a hidden code cell, so it showed only after Run all, behind a stub such as
`HTML(figures.figure(…)) •••`. The author asked why the figures were not embedded instead. The
build now draws them from the shop's week into Markdown cells, so they show before Python loads,
and they are still computed by the engine, never drawn by hand. Tested on the built site, a
Markdown cell drops inline `<svg>` and `<style>`, keeps an SVG image in a base64 data URI, and
showed a cell attachment as a broken image. So the platform and the dashboard are HTML styled by
the course's stylesheet, which restacks on a phone, and the week is an SVG image, redrawn at a
phone's width with each day's label on two lines, with its own light and dark colours: its words
show at about 12 pixels on a 360-pixel phone, where the old drawing's were under 5.

### 11 October 2026: the notebooks follow the reader's light or dark setting

The notebooks were always in JupyterLab's light theme, and with the menus hidden a reader had no
way to change it. The site now turns on JupyterLab's own setting to follow the browser
(`notebook/jupyterlite/overrides.json`, `adaptive-theme`), so a phone or computer set to dark gets
JupyterLab's dark theme. The boxes, figures, tables and printed files were read in both themes on
a phone-sized screen; the figures draw in the text's own colour, with a teal and an orange that
show on either background. The front page keeps its own picker, which the notebooks do not read.

### 11 October 2026: jobs, not programs

The author found "programs" is not what a data engineer calls the things that run on a platform
each night. Chapters 1 and 2 now say *jobs* (Haiku's draft of brief BA, which changed only the word
and its articles), and the platform diagram's label between systems reads "unseen jobs move data
each night". *Job* leaves Chapter 6's rationed terms and joins the plain words (owner, file,
table): a reader meets it as the everyday word from Chapter 1, and Chapter 6 makes it precise, a
node in the lineage graph between the assets it reads and writes. *Run*, the noun, stays Chapter
7's. The engine's code keeps its names (`PROGRAM_ACCOUNT`, `executions`): no learner reads them.

### 11 October 2026: only the notebooks

The author decided that the course has only the notebook version of each chapter. The chapters'
pages are gone, and with them the TypeScript engine (`packages/lab`), the figures and the book
(`packages/views`), the chapters as lesson data (`content/lessons`), the copy of the learning
platform (`platform/`) and their tests; the Python engine (`notebook/shop`) is the only engine.
Asked how, the author chose to keep the front page as the hub, at the same address and with the
same look: the band with the shop's dashboard (now written by the Python engine,
`notebook/front_dashboard.py`, and checked against it), the eight parts, and the contents by part,
where a written chapter's title opens its notebook and an unwritten one is listed. A former
chapter address (`#/chapter/shop-and-platform`, `#/chapter/invisible-data-system`) leads to the
chapter's notebook. Each chapter's originality note moved from its lesson data to its notes, under
"Originality", where a test now looks for it. `CLAUDE.md`, `docs/lab.md` and `docs/authoring.md`
were rewritten around the notebooks; `docs/platform.md` went. The learning platform itself is
unchanged: the digital-design course still uses it. Dated entries below keep the pages, figures
and paths they were written with.

### 11 October 2026: Chapter 1's page

Chapter 1 was a notebook only, and the author asked for the right thing, not the easiest. It now
has a page (`content/lessons/shop-and-platform.ts`), built like Chapter 2's: an essay with figures
the engine computes (the map, a card for each file, the tables' cards, the dashboard, the week),
no prediction or challenge to grade, and a written guess at which asset each table is made from,
which Chapter 2 takes up. Chapter 2's opening, the map's lead about its button, the sentence that
gives the word "asset" and the week's sentence about the nights moved to it, so each is said once;
Chapter 2 opens with its notebook's recap. The front page lists both pages, each with its notebook
under it, and starts at Chapter 1's page; the notebooks' old addresses lead to their chapters.

### 11 October 2026: two chapters where there was one

The author asked whether calling the two notebooks "Chapter 1, part 1" and "part 2" had been a way
to avoid renumbering, and it had: "part" then named both the course's eight parts and half a
chapter. The author's answer was to do the right thing, so the tour is now Chapter 1, "The shop and
its platform" (a notebook, introducing *asset*), and the investigation Chapter 2, "The invisible
data system" (the chapter's page, and a notebook, introducing *metadata*). Every later chapter
moves up one, to 33. The live documents, the code and the tests use the new numbers; dated
entries below this one keep the numbers they were written with, in which Chapter 1 is today's
Chapter 2. The essay's notes moved from `docs/notes/chapter-01` to `chapter-02`, and
`docs/notes/chapter-01.md` is the new chapter's. Chapter 1 has no page on the course yet: the front
page links its notebook, and its start button opens it. Like Chapter 2, it has no prediction or
experiment, under the decision of 10 October that made Chapter 1 an essay.

### 11 October 2026: the front page links the notebooks

The front page is the hub: under Chapter 1's line it links the two notebooks by title, and each
notebook opens and ends with a line back to the contents and to the other part (brief AT). Whether
the notebooks replace the chapter's page stays open (`docs/notes/notebook-prototype.md`, "Links
between the course and the notebooks").

### 10 October 2026: a row of large buttons above the notebook

Asked for custom buttons, the site gains its own JupyterLab extension (`notebook/buttons/`): Run
all, Run below and Save, 44 pixels tall, above every notebook's cells, in place of the two small
labelled toolbar buttons. Its Run all and Run below keep the reader's place, where JupyterLab's
scroll to the last cell. The texts name the row (brief AS), and a browser check presses it in the
notebook workflow. The notebook still runs only when the reader runs it
(`docs/notes/notebook-prototype.md`, "A row of large buttons"). After it was published, the author
reported that the buttons did not seem to work and asked for the menu bar and the toolbar to be
hidden: the extension now hides both, and the row shows a spinner while a run is under way, the
only sign left that Python is busy (the same note, "The menu bar and the toolbar hidden").

### 10 October 2026: marimo ruled out; the notebook is JupyterLite's

The author ruled marimo out as too big for a phone: its pages peaked at 0.79 to 1.09 GB of memory on
a computer, against JupyterLite's 391 to 429 MB for the same two parts. The marimo export, its
workflow job and its deploy step are gone; its two addresses send a browser to the same parts in
JupyterLite. The author also found menus that do not run on a phone: in Chromium's phone emulation,
JupyterLite's menus open when tapped but their items do nothing, while the toolbar's buttons
respond. The notebook's toolbar gains "Run all" and "Run below", set in JupyterLite's settings
overrides (replaced the same day by a row of large buttons, above), and the texts that said how
to run a cell use the toolbar instead of the menus (brief AR). The chapter's two source files keep marimo's file format, as the notation the build turns into
Jupyter notebooks (`docs/notes/notebook-prototype.md`, "marimo ruled out").

### 10 October 2026: the notebook chapter in two parts

Reading the notebooks, the author asked for the chapter in two parts: the first to get the reader
used to the shop and its processes, the second to start on the issues. Both notebook versions are
now two pages (`notebook/chapter_01_part_1.py` and `_part_2.py`, and two Jupyter notebooks). Part 1,
"The shop and its platform", opens with the situation and the head of the shop's message, as the
chapter always has, so the tour serves the question; then the systems, the assets and the week, and
a cell for each thing the shop keeps: its catalogue, its customers, a day's orders, the warehouse's
tables and the dashboard; it ends with a link to part 2. (The message closed part 1 at first; the
author asked for the story to be introduced at the start.) Part 2, "Thursday's
revenue and what the platform cannot say", is the essay from its questions to the handover. Part 1
says what each asset holds and never which is made from which, reads the data but not what the
systems record about it, and counts nothing that shows Thursday's gap, so part 2's investigation is
unchanged. The two marimo pages share one copy of Python in one site: part 2, opened from part 1's
link, downloaded less than 1 MB, and part 1 needs about 0.8 GB of memory against the single
notebook's 1 GB. The course's essay page is unchanged: the same split there needs either 33
chapters, renumbered from Chapter 2 on, or a platform change that gives one chapter two pages, and
that is the author's choice (`docs/notes/notebook-prototype.md`, "The chapter in two parts").

### 10 October 2026: Chapter 1 as a notebook, a prototype beside the course

The author asked whether notebooks that run Python in the browser should deliver the course, for
readers who are data engineers, and for a prototype of Chapter 1 with a warning for phones. The
prototype is `notebook/`: the chapter's essay as a marimo notebook, with the shop's platform in
Python (SQLite for the warehouse, JSON Lines and CSV files, integer pence) and fifteen cells the
reader can change and run. It is exported as a static site with Python and every package bundled,
so the page fetches nothing from another site, and published beside the course under `/notebook/`;
the course is unchanged. Measured in a desktop browser, one visit transfers about 17 MB from GitHub
Pages, Python is ready after 10 to 17 seconds and the page uses about 1 GB of memory; marimo's read-only export would
use about 0.39 GB but shows no code. The warning at the top of the notebook says what was measured
and that a phone short of memory may reload the page, which loses the reader's changes.
`docs/notes/notebook-prototype.md` has the build, the measurements and the questions left for the
author: whether notebooks replace the essay pages, edit mode or run mode, marimo's own chrome, and
whether "no lab on the page" should hold for the code a notebook shows. At the author's request the
same chapter is also built in JupyterLite (`notebook/jupyterlite/`, published at `/jupyterlite/`)
to compare: built from the marimo notebook, so the prose is the same; about 0.44 GB of memory in a
desktop browser against marimo's 1 GB; nothing runs until the reader runs it, and a cell does not
run again when a cell it uses changes; saved edits survive a reload, and are shown in place of the
chapter even after it is updated.

### 10 October 2026: no lab on the page

The author asked for the lab concept to go entirely: the page uses diagrams and figures. The
opening no longer names the Metadata Lab or explains how it runs; the control "How the lab is
built" is gone; the lab's mark above every figure's caption is gone; the role badges and their
notes are gone, since every figure declares no role and names no model (`timeModel: "none"`), so
the platform draws nothing; and the word "lab" is out of every string a learner can read, on the
page and in the figures later chapters may use. The model-versus-reality note opens by saying the
shop, its people and its data are invented, and speaks of the shop's warehouse and systems. What
computes a figure is the engine (`packages/lab`), an implementation detail the engineering
documents name and the page never does. The experiment rubric stays for later chapters' figures,
as a lens in the notes, never as labels on the page; the prose check fails "the lab" and
"Metadata Lab" in anything a learner reads (`CLAUDE.md`, "No lab on the page").

### 10 October 2026: Chapter 1 as an essay

The author restarted Chapter 1 without labs: the figures were getting in the way of the learning.
The chapter is now an essay with four reference and inspect figures (the pipeline, the week, the
asset cards, the dashboard) and no experiment, prediction or challenge: the Thursday prediction,
the rebuild, the change lab, the sort and the rules challenge are gone from the page, and their
figures stay in `packages/views` for later chapters. The author's own essay read as AI-written
and long, so it was rewritten from scratch against the writing standard (`AGENTS.md`): the same
structure, about half the length, every number pinned (`docs/notes/chapter-02.md`, "The chapter
rewritten as an essay"). The chapter's rules in `CLAUDE.md` still hold for the course; where the
essay states a conclusion the lab could have shown, the author's addition to "What this is"
allows it: the experience is a means, not the law. The owner requirement is questioned in the
prose, which states what the field holds and which question that answers.

### 8 October 2026: the front page shows the course's question

The author set the digital-design course's front page beside this one, which was a title, a
paragraph, a button and thirty-one lines of "still to be written", and asked whether this course
should have an intro and a graphic. It now has both, under the course's own rules: the graphic
is a view of the lab, not decoration. A band at the top holds the title, one line that says what
you do, the way in, what the course assumes of you (a short SQL query; files, tables and a
dashboard; nothing about metadata or lineage), and Chapter 1's dashboard live from the lab, with
the lab's mark and its badge, showing the question the course starts from and nothing of what the
chapter finds. Under the band, the eight parts in reading order, one line each, with the parts
not yet written marked; then the contents by part, each part one line until it is pressed, with
how many of its chapters are written, the part of the chapter the button names open. No
animation, no background art: a tinted band, and the dashboard is the graphic. The words came
from Haiku's draft of brief AJ (`docs/notes/chapter-02/briefs/round-14`), checked for facts only:
two dropped facts restored with the fewest words (Part VI builds the lineage graph, not "the graph
of relations"; Part VII includes metadata for ML and AI), "the lab" named as the Metadata Lab
where the page first says it, and a count for a part of one chapter added. A "before you start"
page, as the digital-design course has, is a candidate for later; the line on what the course
assumes is its first form.

### 8 October 2026: "figure" names a box, and the six actions stay internal

An agent's rule for the interactions proposed calling them labs, naming each by its object
(diagram, table, timeline, data browser) and sorting them by six actions (show, inspect, predict,
test, investigate, experiment). The author, reading this session's check of it, kept "the lab" as
the Metadata Lab alone, kept the three badges, and took the six actions as a lens for designing
and reviewing a figure, in the notes and never on the page (`CLAUDE.md`, "Experiments,
instruments and explanations"). The one fault the check found on the page is fixed: "figure"
named an interactive box and, five times, a number; a number is now a total. Every notes block's
objective was read against the author's test, what the learner understands or discovers rather
than what the figure displays, and holds; a content test backstops both rules.

### 7 October 2026: the lab, from the learner's side first

A second agent's guide the author passed on found the Metadata Lab still explained in technical
terms ("a small data platform written for this course", its programs in SQL) before the learner
was told what they do with it. Chapter 1's opening now says what the figures are for and what
happens when you use one (you ask, the lab checks the shop's data, it shows you what it found, you
work out what it means), and keeps how the lab is built, its SQL, its query engine and its run in
memory, in the section's details. `CLAUDE.md` binds the rule for the book: explain a mechanism from
the learner's side first, and the plain model above is the words every chapter uses for a figure.
Two of the guide's words were not taken: "inspect the shop's data or metadata", because the
chapter introduces metadata at its end, from the questions the learner could not answer; and "the
figures on this page are interactive", because the map and the week's figure are only read.

The author then read "You ask the lab a question by using a figure." and asked how, since the
first figure asks nothing. Both points held: the map, the shop's week and the dashboard have no
control, and the page never said how one asks in the others. The paragraph now says which figures
you only read and how you ask in the others (you choose an answer, an asset or the parts of a
query, and press a button), read off the built page's controls, and the rule in `CLAUDE.md` says
the plain model is for a figure the learner uses, with the actions that ask.

### 7 October 2026: the opening in short steps, around two figures

An agent's guide the author passed on found Chapter 1's opening right in what it said and wrong in
how: a long block of prose before the learner did anything, holding the date, the shop, three
systems, what an asset is, seven assets, the nights, the programs, the lab, how the lab runs and
what the browser keeps. The opening now reaches the first question in short steps: the situation
and the lab in two short paragraphs; how the lab runs behind a control the reader opens (a
section's `details`, the platform at 8c2f186); the map, with a count under it the lab computes
(3 files + 3 tables + 1 dashboard = 7 assets) and what an asset is under that; a new figure of
the shop's first week (`week-timeline`), the days, the night of work after each and the morning
the learner starts, computed from the lab's own run; then the dashboard's question. `CLAUDE.md`
binds the rule for every chapter: a diagram carries what prose would make the learner hold in
mind, and each has one job.

Two of the guide's sketches were adapted. Its architecture diagram drew an arrow along one row of
assets, from `orders.parquet` to `clean_orders` to the dashboard, which reads as one asset made
from another: the map keeps its arrows between systems. Its fourth diagram, the lab as an
instrument (a question, the lab, then storage, programs and metadata, then evidence), was not
built: it names metadata before the chapter has earned the word, shows the programs as evidence
in the chapter whose point is that you cannot see them, calls every figure an instrument, the
name of one role, and is not a view of anything the lab computes. The lab's paragraph says in
one sentence what it was for: each figure asks the lab something, and the lab works out its
answer.

### 7 October 2026: the lab's mark

The author asked whether the lab should sit in a coloured box or carry an icon, so that a reader
can tell what the lab is. Every figure runs it, and since the badges name roles, none said so. A
tinted box was tried on the page and set aside: the notes, the outcomes and the marked rows inside
the figures already use the accent's tint, a faded button nearly vanished on it, and a colour
says nothing in words. Every figure that runs the lab now carries a mark above its badge: a flask
drawn for the course, in the accent, and the name "Metadata Lab", the name the opening explains.
Screen readers skip the mark, because the opening tells them every figure runs the lab.

### 7 October 2026: the lab, explained once, where it is first named

The author found the lab named in Chapter 1's opening without an explanation, and its long note
repeated behind every figure's badge and at the foot of the page. The opening now explains it
where the chapter first names it; a badge opens only its role's line (the platform, at 3af8a81),
and the course gives no model note, so the foot states none.

### 7 October 2026: silence is preferable to filler

The author found a badge's note that told the learner nothing ("You have what you were told about
the platform, kept to hand. It asks nothing of you.") and gave a style rule, which `CLAUDE.md`
and `docs/style.md` bind: every sentence tells the learner something concrete, changes what they
should do, explains why something matters, or sets up a prediction or a decision; prose is
written for the learner's next action, not for narrative flow; and a sentence the learner would not
miss is removed, with nothing in its place unless an action belongs there. A content test fails
the commonest forms of filler. An independent review of Chapter 1 against the rule cut twelve
passages and redrafted two notes (`docs/notes/chapter-02.md`).

### 7 October 2026: the author's fifth round: experiments, instruments and explanations

The author gave a guide to designing effective labs, and `CLAUDE.md` binds it ("Experiments,
instruments and explanations"). A figure is an explanation (`reference`), an instrument the learner
examines for evidence (`inspect`), or an experiment, in which the learner has a question, a
hypothesis or a decision and uses the system to answer it; experiments are preferred. Every figure
declares which, and its badge says so, where every badge said "Lab" before, so a map, an asset
browser and an experiment looked alike. The page calls the guide's "lab" an experiment, because
"the lab" is the Metadata Lab. An experiment's notes answer twelve questions, which replace the
eight a prediction's answered; an instrument's or a reference's answer two; and a content test
fails a figure without its role or its answers. The platform gained the role for it.

Chapter 1's audit against it. The inspector was presented as the activity ("Browse the seven
assets and what storage records about each."), the guide's own example of an instrument passed off
as an experiment. The investigation now opens with a decision: where to look first for Thursday's
difference, and what to look for there. A line after the choice says what that asset can show,
from its shape, and the inspector opens on it, as the instrument for that question. The choice of
an explanation to test moved after the inspector, so the investigation runs in the guide's order:
is there a discrepancy, where is it, what could explain it, which explanation fits. The map is a
reference and the dashboard an instrument; every other figure is an experiment.

### 7 October 2026: Thursday's cause, tested by the learner

Asked to do what is best for the learning, the Thursday difference now gets the second half of an
investigation. Once the prediction has shown it, the investigation opens with a choice of which
explanation to test (orders left out, counted at lower values, or counted on another day); the
learner tests it with the inspector and the query builder; and once their query rebuilds
`daily_sales`, a check reads Thursday's orders against the rows the query keeps and marks which
explanations they support. The check waits for the rebuild, so it names no source before the
construction is solved, and it never says why the orders were left out, which the rules challenge
asks. The reflection no longer repeats the numbers; it names what the left-out orders have in
common, after the challenge has found it.

### 7 October 2026: the author's fourth round: predictions around learnable questions

The author gave a quality test for every interactive question, and `CLAUDE.md` binds it
("Interaction is the explanation"). A prediction starts from what the learner should learn. Its
options are results the learner could expect and the beliefs they reflect, never the explanation
the result is about to give. A cause is never asked for before its effect has been seen, evidence
is independent wherever it can be, and "I can't tell yet" is an option where nothing seen settles
the question, never marked wrong. Each prediction's notes answer eight questions, and a content
test fails one that misses any.

Chapter 1's audit against it. The Thursday prediction asked whether the raw orders would add up
to 51.50, and its "no" already said that something on the way to `daily_sales` had left orders
out. It now asks what Thursday's orders add up to, offers 51.50, a different total, or "I can't
tell yet", and only once the lab shows 205.50 asks what explains the difference, which the
investigation then finds. The rules prediction's options named a rule that decides no row, the
very explanation its result gives; they now say only whether another setting can match every
row. The owner requirement, the change lab and the sort passed.

### 7 October 2026: the author's third round: question the requirement

The author asked for a goal of the whole course, beside metadata: the habit of questioning a
requirement before building to it. `CLAUDE.md` binds it ("Question the requirement"): some
exercises carry a requirement that is deliberately underspecified, and keep apart what it says,
what it might mean, what each meaning needs, what the platform records and whether that record
meets it; "not enough information to choose yet" is an option the learner can take. Chapter 1's
owner question became the standing example, on a new figure, `requirement`: the learner chooses
what to store for "Every table must have an owner", sees the four questions the requirement could
be asking and what each needs stored, then sees the warehouse's account and which of the four it
answers. "Questioning the requirement, chapter by chapter", above, lists a candidate for every
later chapter, and each chapter's notes say which requirement it questions, or why none.

### 7 October 2026: the course's icon

The course has an icon for a browser's tab and for installing it on a phone's home screen or a
computer: a white label tag on the accent, drawn in `scripts/icons.mjs`, with a web app manifest
(`docs/sources.md`). The manifest names no `id`, because an id resolves against the origin, which
the author's courses share; each course's start URL is its identity. The browser's own bar takes
the header's colour in the theme the learner picks. There is no service worker, so an installed
course does not promise to work offline; that would be a decision of its own, with the question
of how a learner gets a changed chapter.

### 7 October 2026: the author's second round on Chapter 1

1. **A prediction asks for a belief the learner can already hold**, course-wide. Each option is an
   explanation of how the platform works; a count is offered as what it means (none, one, more
   than one); the chapter's notes say, for each prediction, what the learner has seen and how the
   lab tells the explanations apart, and a content test checks the notes have a row for it.
   Chapter 1's owner and days predictions were rebuilt on this rule (`docs/notes/chapter-02.md`).
2. **A map of the platform, to hand through the chapter**, computed by the lab. The author's sketch
   drew arrows from asset to asset; the map does not, because in Chapter 1 those arrows would
   state what the chapter shows storage cannot tell, and would answer the construction's first
   choice. It draws systems, assets and the unseen programs between systems, and gains links in
   later chapters only from records the learner builds.
3. **"Asset" and "metadata" defined precisely.** An asset is something in the platform that can be
   stored, described, changed, related to other assets, or depended on. Metadata is information
   about an asset or the platform, and can live inside a system, inside a file beside the data, or
   in a system of its own; the course never says it is kept apart from the data.
4. **A chapter ends with a short summary** of what it found, said once, before its reflective
   questions, which lead into the next chapter.

### 6 October 2026: the author's answers at checkpoint 1

1. **Part VI is written in Python**, under Pyodide ("What the learner writes", above).
2. **A prediction, once committed, stays.** Its value is the commitment before the lab answers; a
   re-answer after the reveal teaches nothing and erases the record of the surprise. The
   platform's prediction control now offers "Predict again" only to a figure that asks for it:
   this course does not, and the digital-design course keeps it. The learner's way back is a
   "start this chapter again" at the foot of every chapter, which clears everything the chapter
   keeps, after a second press.
3. **The platform repository is public**, made so by the author: its code was already public
   through this course's copy. The copy stays (`docs/platform.md`).
4. **The digital-design course switches to the moved packages now**, as proposed and agreed: two
   copies of one runtime drift with every fix, and the cross-book overlay job already shows that
   course passing on the moved packages. The switch is a change to `snowch/digital-design`, made
   there.

### 6 October 2026: the course's frame

1. **Title.** *Metadata Systems: From Raw Files to a Working Metadata Platform*, in the pattern of
   the author's digital-design course.
2. **The shop.** An online shop that sells bicycle parts, invented for the course. It is not dbt's
   jaffle shop, the café dbt's guides use, whose quickstart data is customers, orders and
   payments and whose structure guide builds staging, intermediate and marts models
   (`docs/sources.md`). This shop has no payments table and no layers named for dbt's, has a
   dashboard, keeps its raw files in object storage and its cleaned tables in a warehouse, and its
   programs are the lab's own SQL.
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

### 12 October 2026: Chapters 7, 8 and 9 written; Part II complete

The author asked to "complete part 2". The three chapters keep their rows, with one change of
wording in Chapter 7's (below), and checkpoint 2 falls after them. Chapter 7's reader designs the
fields of the events each program sends, groups them into runs to answer Jo Marsh (3 orders left
out, from the run on Friday 11), finds that a program and a day do not identify a run of a function,
answers Chapter 6's question about the analyst's copy from what each run read, and questions "Record
every run."; Chapter 8's reader meets OpenLineage as a mapping from their own fields, sees a
consumer's knowledge grow event by event, writes an event by hand, and finds two names for one
table do not join; Chapter 9's reader runs four stages of ingestion over the week's events, a line
cut short and a facet not known included, and questions "The graph must show the current lineage."
Decisions the plan did not make:

- **The returns desk is built**, as `docs/lab.md` describes, and enters at Chapter 7. Chapters 1 to
  6 run without it; Chapters 7 to 9 run with it.
- **Chapter 7's failure is a function, not a night.** Grouping a nightly job's events by job and day
  works; it merges two runs of `record_return` on one day. The row's wording follows.
- **The reader's state is restated, not carried.** Chapter 8 starts from a mapping of Chapter 7's
  fields, not from the reader's own design (`docs/lab.md`, "The learner's state").
- **What Chapter 8 states about the specification was read again** at a recorded commit, and the
  shop's events were validated against the published schemas outside the repository
  (`docs/sources.md`). The specification's naming page has no form for the shop's warehouse, so its
  namespace is the shop's own, and the page says so.
- **The analyst's script sends events from Chapter 9**, as a third producer, so that normalising has
  two producers' names for one table to join.

