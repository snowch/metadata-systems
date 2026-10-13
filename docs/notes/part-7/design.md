# Part VII: design

A working note, 13 October 2026, written before the engine for Chapters 29 to 32. It says what each
chapter shows of a real system, what the learner does, which requirement it questions, and where
each fact comes from. The research notes beside it (`research/chapter-29.md` to `chapter-32.md`)
hold what was read; the facts the chapters state were read again at the commits below and are
recorded in `docs/sources.md` with the chapter that uses them.

## What is the same in every chapter of the part

- **A real system does not run in the page.** None of these systems runs in a browser, and the
  course does not pretend one does. Each chapter takes the shop's own week and applies to it a rule
  that a real system's specification, documentation or code states, read at a named commit: how a
  provider names a job, how a consumer sets a run's state, how a platform types an owner. The cell
  that applies the rule is the shop's code, and the page says whose rule it is and where it was
  read ("Marquez's code, as read, sets a run's state from each event in the order it is taken").
  The model-versus-reality note of each chapter says that the cell applies the rule and is not the
  system, and what the system does that the rule leaves out.
- **Implementation is not specification.** Where a fact is one project's behaviour, the page says
  "Marquez does", never "OpenLineage requires" (`CLAUDE.md`, "Accuracy"). Where the specification
  is silent, the page says so.
- **Products are compared by architecture, never by marketing**, and no chapter says which product
  is better. A product appears where it answers a question the shop raised.
- **The learner changes one small thing per chapter**: an order, a configuration value, a mapping.
  Part VI's code-writing ends with Chapter 28; Part VII's cells are short edits with a check below.
- **No new terms** (the plan has none for Part VII). Product names are names, in plain text; their
  field names are in code font and used as names.
- **Originality.** No example from the projects' documentation is reused: not their sample jobs, DAGs,
  dbt projects, queries or owner examples (the naming page's `orders_etl.count_orders` among them).
  Every name the pages show is the shop's, put through the real rule.

## Chapter 29: OpenLineage in practice

The plan: real producers and the reference consumer, real events and facets, against the learner's
own collector.

- **Producers.** The shop's programs send their events through the OpenLineage Python client
  (`client/python`, 1.55.0): the client fills `producer` with its own default when the program sets
  none, sets `schemaURL` to the 2-0-2 `RunEvent`, gives each facet `_producer` and `_schemaURL`, and
  refuses a run id that is not a UUID. An instrument shows one of the shop's events as the shop sends
  it and as the client would build it, field by field. Both pass Chapter 8's check.
- **The reference consumer.** The OpenLineage project's README calls Marquez "the reference
  implementation of the OpenLineage API". Marquez's code, read at `180f37b`, stores every event it
  takes as a row with no rule that makes it unique (the key was dropped in migration V20), sets a
  run's current state from each event in the order it takes them, without comparing times
  (`RunDao.upsert`, `ON CONFLICT ... current_run_state = EXCLUDED`), maps `START` and any type it
  does not know to `RUNNING`, writes a state row and moves the run's end time on each terminal
  event, and stamps each state with the event's own time.
- **Experiment.** Chapter 25's arrivals, faults and all, go to the learner's collector (the shop's
  pieces) and through Marquez's rules. Prediction: after every arrival, which state does Marquez
  hold for the run early on Friday 11, whose `START` arrived after its `COMPLETE`? Evidence: the
  collector holds `COMPLETE`; Marquez's rules hold `RUNNING`. The same table shows Thursday's retry
  with a new time (the run's end time moves to 02:30:52) and Saturday's repeat (two event rows, two
  state rows).
- **The learner's change:** the order in which events reach the consumer, `"arrival"` to
  `"event time"` (a buffer that sorts before sending, Chapter 20's rule). Friday's run is then
  `COMPLETED` in Marquez's rules; Thursday's end time is still 02:30:52, because ordering does not
  drop a repeat with a new time. Ordering and deduplication are two jobs.
- **Requirement:** "Use the reference consumer." Readings: the consumer the project names as its
  reference implementation (Marquez); a consumer that does what the specification requires (the
  specification says nothing on repeats, late events or order, so it does not separate the
  learner's collector from Marquez); a consumer to check your own against (they disagree about
  Friday, and which is right is a choice about order the specification leaves open).

## Chapter 30: Airflow, Spark, dbt and Trino

The plan: where each system's metadata comes from. The shop's `build_daily_sales` is run four ways
over the week, and each system's own record and its OpenLineage integration's names are computed
from the rules read.

- **Airflow** (tag 3.3.0; provider `providers/openlineage` at `7f0d50c`): a task instance is one
  task in one Dag run, keyed by Dag, task, run and map index, with a `try_number` the scheduler
  raises on each try; the provider names the job `{dag_id}.{task_id}`, takes its namespace from
  `[openlineage] namespace`, else `OPENLINEAGE_NAMESPACE`, else `default`, and makes the run id
  from the namespace, Dag, task, try number and map index with the logical date, so each try is a
  new OpenLineage run.
- **Spark** (v4.0.0; OpenLineage's Spark integration at `60261f0`): Spark's own job is one action;
  the integration names the job from the application's name, the executed plan's top node through
  its normaliser (camel case to lower case with `_`), and the output table, so a job writing
  another table is another job.
- **dbt** (dbt-core v1.11.0 artifacts; `openlineage-dbt` at `60261f0`): the wrapper runs dbt, then
  reads `manifest.json` and `run_results.json` and sends every event at the end; a model's job is
  named `{database}.{schema}.{package}.{model}`, its inputs come from the manifest's parents, its
  times from the result's timing, and each processing of the artifacts makes new run ids.
- **Trino** (`trino-openlineage` at `7a821d4`): the listener sends `START` when a query is created
  and `COMPLETE` or `FAIL` when it ends, with inputs and the output on the second only; the default
  job name is the query's id; by default it sends nothing for a `SELECT`.
- **Experiment.** Prediction, after the four rules are on the page: over the week's 7 nights, how many
  jobs do Trino's events show for building `daily_sales`? Evidence: 7, one for each query. The
  learner's change: the listener's `job.name-format`, from `$QUERY_ID` to `$SOURCE`. Then the four
  nightly jobs' queries, which share one source, become one job: too many runs merged (Chapter 22).
  A source for each program makes one job each.
- **What else the chapter shows:** the analyst's copy, a `SELECT` exported by a client, sends no
  event through Trino by default, so its edge is missing; a dbt run's events all arrive after the
  run, `START` included, and processing the same artifacts twice gives two runs that Chapter 25's key
  cannot match.
- **Requirement:** "Capture lineage from Airflow, Spark, dbt and Trino." Readings: by each system's
  own job (a task, an action and table, a model, a query); by the shop's programs (what Part II
  meant); by the datasets each reads and writes, whatever names the jobs. Each needs a different
  rule for names; none of the four systems' default names is the shop's program.

## Chapter 31: Metadata platforms

The plan: OpenMetadata, DataHub, Apache Atlas and Marquez compared: how metadata arrives, how it is
modelled, stored, indexed and served. Commits: DataHub `40287ac`, OpenMetadata `18294ee`, Atlas
`ec7dc21`, Marquez `180f37b`.

- **Instrument:** the four architectures side by side, each fact sourced: arrival (DataHub and
  OpenMetadata pull with connectors on a schedule and take pushes; Atlas takes hooks' messages and
  REST; Marquez takes OpenLineage events); model (DataHub's schema-first entities and aspects, in
  PDL; OpenMetadata's JSON Schemas; Atlas's type system; Marquez's tables of namespaces, sources,
  datasets, jobs and runs); store and index (a relational store with a search index for the first
  two, a graph store with a search index for Atlas, PostgreSQL for Marquez).
- **Experiment:** the three owners of `daily_sales` (Chapter 27: the account, the person
  responsible, the team) put into each platform's owner field under its rule. DataHub: a list of
  owners, each a user or a group, each with a type (technical owner, business owner, data steward,
  none, or one the organisation defines); OpenMetadata: a list of users or teams of type Group, with
  no type; Atlas: one optional text value on the asset; Marquez: no owner on a dataset, only on a
  namespace, which events create with the owner `anonymous`. Prediction: which platforms keep all
  three owners and which meaning each holds? Evidence: DataHub only, through its types.
- **The learner's change:** the type each owner gets in DataHub's payload; the check holds it to the
  enum and the entity types, and says which meaning the reader can recover.
- **Requirement:** "Choose a metadata platform that tracks ownership." Readings: stores an owner for
  each dataset; stores whom to ask; stores which meaning each owner holds. DataHub can meet all three, OpenMetadata and Atlas the first,
  and Marquez none for a dataset.

## Chapter 32: Metadata for ML and AI

The plan: training data to training run to model to evaluation to deployment to inference. The shop
trains a forecast of the next day's revenue from `daily_sales`, and records it as an experiment
tracker does: a run, its input dataset with a name, a digest, a source and the context `training`,
and a registered version that names the run (MLflow's fields, read at `9d651c2`).

- **The digest.** MLflow's digest for a pandas table is an MD5 over a hash of the first 10,000 rows'
  text and number columns, the row count and the column names, cut to 8 characters. The shop
  computes a digest in that manner from its own rows; it is the shop's, not MLflow's value, and the
  page says so.
- **Experiment.** The forecast is trained on Sunday morning. By Tuesday, `daily_sales` has been
  rebuilt. Prediction: from the run's record, can you tell which rows the forecast was trained on?
  Evidence: the digest differs from today's table's, so the record shows the data changed; it
  cannot give the rows back. With a table that keeps its history (Chapter 2's closing note), the
  record would need the version it read.
- **The word "model".** In this chapter a trained forecast is "the forecast" or "the trained model",
  never the data model of Part I (`CLAUDE.md`, "What no check can catch").
- **Requirement:** "Record the training data of the model." Readings: the snapshot it read (a
  version or a time); the query that chose it (its text and when it ran); the features computed
  from it (the code and the values). The tracker's record meets "which table, and whether it
  changed".

## As built

What the review changed from the design above (each chapter's note, "The review", has the rest):

- **Chapter 29.** The prediction asks for Friday's state once all events have arrived. The
  printed event is the shop's with the provider's names and facets put in, and the facets it lacks
  and loses are named.
- **Chapter 30.** Spark's job name ends in the output's path. The prediction is the shared-source
  case under `$SOURCE`, not the default's count, which the stated default settled; a count of each
  format's jobs follows the change.
- **Chapter 31.** DataHub's ownership type is written as a `typeUrn`, not the deprecated enum; the
  check holds the form and the difference, not that a type exists. DataHub can meet all three
  readings, OpenMetadata and Atlas the first, Marquez none for a dataset.
- **Chapter 32.** The forecast is trained on Saturday 12 and the question asked on Monday 14. The
  prediction asks whether Monday's `daily_sales` gives the recorded digest; the model's version is
  shown; the digest's blind spot is a value changed in place past row 10,000, not any later row.
  This record meets none of the three readings.

## Checkpoint

Plan checkpoint 5, the author's review, comes before Chapter 33. Part VII ends there.
