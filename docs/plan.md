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

## The lab

Every figure runs the Metadata Lab (`packages/lab`, described in `docs/lab.md`): a small online
shop's data platform that really runs. Three raw files arrive each night (`customers.parquet`,
`orders.parquet`, `products.parquet`); programs written in the course's SQL subset clean them
(`clean_customers`, `clean_orders`), add them up (`daily_sales`), and refresh a dashboard
(`sales_dashboard`). The course's week is Monday 7 to Sunday 13 September 2026, and the learner
arrives on Monday 14 September. On Thursday something went wrong, and the dashboard shows it.

A small map of the platform stays to hand through a chapter: the systems in the order data moves
through them, the assets each holds, and between them the programs the learner cannot yet see. In
Chapter 1 it shows no link from one asset to another, because that is what the chapter finds
storage cannot tell. As the learner builds records in later chapters, the map gains what those
records hold, and a link appears on it only once something the learner built records it.

The lab starts with deliberately too little information. Chapter 1 gives the learner storage and
nothing else. Each later chapter adds one kind of record, built by the learner, and the lab keeps
what they built: the lab a figure runs is the shop plus the learner's own graded work from every
earlier chapter (`docs/lab.md`, "The learner's state").

## How a chapter runs

Every chapter follows the loop **predict, build, run, inspect, explain, change, run again**, inside
the platform's ten sections: question, motivation, prediction, investigation, construction,
failure experiment, explanation, generalisation, challenge, reflection. Read as the learner meets
it, the loop asks: a real question; what can I believe about it now; predict; act on the lab;
observe; what did that prove; what can the data not tell me; what would a system have to record.
A prediction is built around what the learner should learn, asks for a belief about a result the
learner can observe, and never asks for a cause before its effect has been seen (`CLAUDE.md`).
Every figure says whether it is an experiment, an instrument or a reference, experiments are
preferred, and an instrument always has a question in front of it. A chapter is finished when
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
| 1 | The invisible data system | nothing yet: storage is all there is | an essay, read with four figures: a query over `clean_orders` reproduces `daily_sales` and explains Thursday, and three changes show what that does and does not establish | an analyst's copy makes two sources fit; an edited program leaves nothing that fits and no trace; a failed night leaves the dashboard looking up to date over a table a day behind | asset, metadata |
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

## Questioning the requirement, chapter by chapter

A candidate for each chapter: a requirement that sounds settled in that chapter's material, and
the questions it could be asking. Each chapter confirms or replaces its own when it is written,
and its notes say which (`CLAUDE.md`, "Question the requirement").

| Ch | A requirement that sounds settled | What it could be asking |
| --- | --- | --- |
| 1 | "Every table must have an owner." (questioned in the prose) | who is responsible for it; which team is; which program writes it; which account controls it in the warehouse |
| 2 | "Every column must have a description." | what the column means; its unit; where its values come from; whether it may be empty. A description that repeats the column's name meets it as written |
| 3 | "Each asset has one owner." | one person, one team, or one identifier for an owner two records spell differently |
| 4 | "Show everything related to `daily_sales`." | what it is made from; what reads it; who is responsible for it; where it is kept. Each is a different kind of edge |
| 5 | "Record the lineage of `daily_sales`." | what its program declares it reads, what it was seen to read, or both; between tables or between columns |
| 6 | "Record every run." | to find failures; to know when an asset was last written; to audit who changed what. Each needs a different event |
| 7 | "Our programs must emit OpenLineage." | which events, with which facets, under which namespace and name |
| 8 | "The graph must show the current lineage." | current as of the last event received, the last run, or the last change to a program |
| 9 | "Show which columns `revenue` depends on." | the columns its value is computed from, or also those that decide which rows count, such as `status` |
| 10 | "Warn us of breaking changes." | breaking for which reader: a program that reads by name, the dashboard, somebody's own query |
| 11 | "The same table must have one identity." | the same name, the same rows, the same environment, or the same version |
| 12 | "The dashboard must be fresh." | refreshed lately; built from the latest data; showing the latest day. Chapter 1's failed night met the first and neither of the others |
| 13 | "No order without a customer." | in the raw file, in `clean_orders`, or on the dashboard. An assertion on `clean_orders` passes because the rows were filtered first |
| 14 | "Show where Thursday's figure came from." | the rows; the program; the run; the rows as they were when the run read them |
| 15 | "Tell us what breaks if `customer_id` is renamed." | what fails, or also what keeps running and gives a wrong answer |
| 16 | "Find the cause of the wrong figure." | where the data first went wrong; the change that did it; the decision behind that change |
| 17 | "Lineage must be complete." | complete for the programs that send events, or for every program that touches the data |
| 18 | "Ingestion must ignore duplicates." | the same event twice; the same run reported twice; the same content at another time |
| 19 | "Show the latest state of each run." | latest by when it happened, or by when it arrived |
| 20 | "Show the correct owner." | the newest claim; the claim from the most trusted system; every claim with where it came from. Chapter 1's owner returns |
| 21 | "Merge the same dataset across systems." | the same name, the same rows, or the same thing to the business; across environments or not |
| 22 | "Keep lineage for 90 days." | 90 days of events, of edges, or of whatever assets still in use depend on |
| 23 to 27 | the learner's own query layer must answer "who owns X?" (Chapter 26) | whichever meaning the learner's records keep, and the query layer says which |
| 28 | "Use the reference consumer." | what the specification requires, against what one implementation does |
| 29 | "Capture lineage from Airflow, Spark, dbt and Trino." | each system's own meaning of a task, a run and an input |
| 30 | "Choose a metadata platform that tracks ownership." | each platform's own meaning of an owner, compared from its documentation |
| 31 | "Record the training data of the model." | the snapshot it read; the query that chose it; the features computed from it |
| 32 | the unfamiliar platform's own requirements | the learner questions each before building to it |

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
- **Code** (Part VI, and Chapter 32): Python, run in the browser by Pyodide, decided at
  checkpoint 1 because the learner reads and writes this code and Python is a data engineer's
  language. The lab stays TypeScript; the learner's Python runs in a Web Worker against tests, and
  the two exchange JSON. Pyodide 0.28.3's core is about 5.3 MB to download, compressed, on the
  first visit, and cached after (measured from its CDN on 6 October 2026). The course will serve
  it from its own site, so that no figure fetches from a third party, and its licence, MPL-2.0,
  joins the licence check when it is added.

## OpenLineage, placed

OpenLineage appears in Chapter 7, after the learner has designed an event from the problem in
Chapter 6, and returns in Chapters 8, 17 to 19 and 28. What the course states about it is checked
against the specification (`docs/sources.md`), and the specification's silences are named as
silences. For a batch job it expects a START and one terminal event per run, and events about a
run accumulate; a streaming job or a service may never send a terminal event and instead sends
periodic snapshots of a time window. It does not say what a consumer must do with a duplicate, a
late or a missing event. Part V is about exactly those silences. Its schema and its run-cycle
page also disagree on whether an `OTHER` event may follow a terminal one, and the course says so.

## The checkpoints

The author reviews the course at five checkpoints:

1. After Chapter 1, the plan, the lab's design and the platform move (now).
2. After Chapter 8: the event model and OpenLineage are in place.
3. After Chapter 16: metadata is operational.
4. After Chapter 22: the failure chapters.
5. Before Chapter 32.

## Decisions since the brief

### 10 October 2026: Chapter 1 as an essay

The author restarted Chapter 1 without labs: the figures were getting in the way of the learning.
The chapter is now an essay with four reference and inspect figures (the pipeline, the week, the
asset cards, the dashboard) and no experiment, prediction or challenge: the Thursday prediction,
the rebuild, the change lab, the sort and the rules challenge are gone from the page, and their
figures stay in `packages/views` for later chapters. The author's own essay read as AI-written
and long, so it was rewritten from scratch against the writing standard (`AGENTS.md`): the same
structure, about half the length, every number pinned (`docs/notes/chapter-01.md`, "The chapter
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
from Haiku's draft of brief AJ (`docs/notes/chapter-01/briefs/round-14`), checked for facts only:
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
passages and redrafted two notes (`docs/notes/chapter-01.md`).

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
   Chapter 1's owner and days predictions were rebuilt on this rule (`docs/notes/chapter-01.md`).
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
