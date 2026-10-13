# Sources for Chapter 30 (research)

A research note, gathered on 13 October 2026 from each project's own repository. Facts the chapter states are re-checked and recorded in `docs/sources.md` before they land.

SOURCES FOR CHAPTER 30

Nothing was written to the repository. Scratch copies are under /tmp/claude-0/-home-user/8fe2150f-cb84-52b9-b63b-9e8644068234/scratchpad/ (src/, ch30/, olclone/). Quotations are 15 words or fewer. Line numbers are for the pinned refs.

PINS (for docs/sources.md)
- apache/airflow: tag 3.3.0 (the main branch has since diverged, see A5). Airflow 2 facts are from tag 2.10.5. I confirmed that tag 3.3.0 exists. I did not check that it is the newest release.
- apache/spark: tag v4.0.0. The master branch has the same QueryExecutionListener interface.
- OpenLineage/OpenLineage: main at commit 60261f0b57fb1370c2c6c3cadc9f1721b6c3c3b5 (12 Oct 2026). The dbt wrapper is openlineage-dbt 1.55.0.
- dbt: dbt-labs/dbt-core tag v1.11.0 (code and JSON schemas), plus dbt-labs/docs.getdbt.com branch `current`. dbt-core `main` is now the v2.0 Rust rewrite and no longer holds the v1 Python code or schemas (see D6).
- trinodb/trino: main at commit 7a821d4a8678721f4e739dac49961fef7d67a039 (12 Oct 2026).
- schemas.getdbt.com is blocked by the proxy. I read the same schemas from dbt-core v1.11.0 at schemas/dbt/manifest/v12.json and schemas/dbt/run-results/v6.json.

A. AIRFLOW

A1. A Dag run is one instantiation of a Dag in time. A task instance is one task for one Dag run, and it carries a state.
- Dag run: airflow-core/docs/core-concepts/dag-run.rst (3.3.0), lines 18-22. Quote: "an instantiation of the Dag in time".
- Task instance: airflow-core/docs/core-concepts/tasks.rst, section "Task Instances" (lines 63-70). Quote: "a specific run of that task for a given Dag".
- The 3.x docs write "Dag", not "DAG".
- The class docstring for DagRun says it is created by the scheduler or by an external trigger. Source: airflow-core/src/airflow/models/dagrun.py, class DagRun (line 179).

A2. Task instance states (3.3.0), from `TaskInstanceState` in airflow-core/src/airflow/utils/state.py (line 65, members to about line 91).
- There are 14 members: removed, scheduled, queued, running, success, restarting, failed, up_for_retry, up_for_reschedule, upstream_failed, skipped, deferred, awaiting_input.
- That is 13 names. A 14th is not in the enum: None, meaning created but not yet scheduled. The file comment says "we don't list it here since TaskInstance is a string enum".
- The enum is split into `TerminalTIState` (line 37): success, failed, skipped, upstream_failed, removed. The rest are in `IntermediateTIState` (line 50), plus "running".
- The docs list the same states plus "none" (tasks.rst lines 72-86), and add "Ideally, a task should flow from none, to scheduled, to queued, to running, and finally to success."
- Release differences:
  - Airflow 2.10.5 (airflow/utils/state.py lines 36-70) has the same states except `awaiting_input`. It also has a deprecated `shutdown`, marked "Not used anymore, kept for compatibility."
  - Tag 3.2.0 also lacks `awaiting_input` (diff against main).
  - Tag 3.3.0 has `awaiting_input` (human-in-the-loop).
- Dag run states are only four: `DagRunState` queued, running, success, failed (state.py line 97).
- A Dag run's status comes from its leaf tasks. Source: dag-run.rst lines 29-41. Quote: "success if all of the leaf nodes states are either success or skipped".

A3. `try_number` counts attempts. It is 0 at creation, and the scheduler adds 1 when it moves the task instance to `scheduled`. A `reschedule` sensor keeps the same number.
- Column: airflow-core/src/airflow/models/taskinstance.py (3.3.0) line 574, `try_number ... default=0`. Line 575 is `max_tries` with `server_default="-1"`.
- Reset to 0 at line 715.
- Incrementing: airflow-core/src/airflow/models/dagrun.py (3.3.0), lines 2119-2138. `next_try_number` is `TI.try_number + 1`, except for `up_for_reschedule` ids, which keep `TI.try_number`. The update sets state to SCHEDULED and `try_number=next_try_number`.
- A second increment sits at taskinstance.py line 1808. It applies when a task is deferred, unless the prior state was `up_for_reschedule`.
- Log line at line 1405: `"Starting attempt %s of %s", ti.try_number, ti.max_tries + 1`.
- `max_tries` is a cumulative value (comment near line 1552 in main). It is set to `ti.try_number + task.retries` (line 392). A retry is allowed when `try_number <= max_tries`, and not when `max_tries == 0`. Source: airflow-core/src/airflow/api_fastapi/execution_api/routes/task_instances.py, `_is_eligible_to_retry` (about line 1282).
- In 2.10.5, `try_number` is a column (airflow/models/taskinstance.py line 1829), and `next_try_number` is `try_number + 1` (line 2069).
- I found no docs sentence defining `try_number`. This is read from code.

A4. What the metadata database stores about a task instance. Table `task_instance`, class `TaskInstance` (taskinstance.py 3.3.0, lines 539-640).
- Class docstring: "the authority and single source of truth around what tasks have run".
- Columns (lines 559-619):
  - Key and identity: id (UUID primary key), task_id, dag_id, run_id, map_index.
  - Time and outcome: start_date, end_date, duration, state, try_number, max_tries.
  - Placement: hostname, unixname, pool, pool_slots, queue, priority_weight.
  - Operator and queueing: operator, custom_operator_name, queued_dttm, scheduled_dttm, queued_by_job_id.
  - Execution: last_heartbeat_at, pid, executor, executor_config, external_executor_id.
  - Deferral and display: trigger_id, trigger_timeout, next_method, next_kwargs, rendered_map_index, task_display_name.
  - Versioning and tracing: updated_at, span_status, dag_version_id (foreign key to dag_version), context_carrier.
- Unique constraint "task_instance_composite_key" on (dag_id, task_id, run_id, map_index) at line 641.
- `DagRun` table `dag_run` (dagrun.py lines 179-345): dag_id, run_id, run_type, logical_date, data_interval_start/end, queued_at, start_date, end_date, state, triggered_by, conf, run_after, bundle_version, created_dag_version_id, and others.
- Earlier tries are kept in table `task_instance_history`. Source: airflow-core/src/airflow/models/taskinstancehistory.py (read at tag 3.2.0). Its docstring is "Store old tries of TaskInstances", with a primary key `task_instance_id` and its own try_number, state, start/end dates and so on. I did not re-fetch this file at 3.3.0.
- In 2.10.5 the key was (task_id, dag_id, run_id, map_index) (airflow/models/taskinstance.py lines 1819-1822).
- Bearing on the chapter: the row is mutable, so the latest try overwrites the live row.

A5. SOURCES DISAGREE across versions. On the unreleased `main` branch, taskinstance.py has a docstring saying "Every try of a task is its own row with its own UUID." Only the latest try is "live" (`working_set` true). Earlier tries are archived rows, not the history table. Tag 3.3.0 has no `working_set`. Cite 3.3.0 and say the model is version-dependent.

A6. Datasets and assets.
- Airflow 2: `Dataset` has `uri` and `extra` only. Source: airflow/datasets/__init__.py (2.10.5), class Dataset line 246, fields lines 249-253. `DatasetAlias` is at line 210.
- Airflow 3: `Asset` has `name`, `uri`, `group`, `extra`, `watchers`, `access_control`. Source: task-sdk/src/airflow/sdk/definitions/asset/__init__.py (3.3.0), class Asset lines 262-286. `Dataset(Asset)` (line 444) and `Model(Asset)` (line 450) only change `asset_type` to "dataset" and "model". The default `group` is the asset type, so "asset".
- `AssetAlias` is at line 457.
- Declaring: a task takes `inlets` and `outlets` arguments. Source: task-sdk/src/airflow/sdk/bases/operator.py (3.3.0), lines 1075-1076 and 1220-1221, and `add_inlets`/`add_outlets` at 1336-1342.
- The docs example (authoring-and-scheduling/asset-scheduling.rst lines 26-45) is `MyOperator(outlets=[Asset("s3://asset-bucket/example.csv")])`, and a Dag declares `schedule=[Asset(...)]`.
- "Updated" only on success. Quote: "Airflow marks an asset as `updated` only if the task completes successfully". Same file, lines 57-60.
- The asset docs say nothing on `inlets`. Inlets and outlets are generic lists of objects on the operator.
- Airflow's own lineage page is airflow-core/docs/administration-and-deployment/lineage.rst. It says "Lineage support is very experimental and subject to change". It describes `HookLineageCollector.add_input_asset`/`add_output_asset`.
- I did not check how the Airflow OpenLineage provider consumes inlets and outlets.

B. SPARK

B1. Spark's own vocabulary. Source: docs/cluster-overview.md (v4.0.0), glossary lines 128-146.
- Task: "A unit of work that will be sent to one executor".
- Job: spawned "in response to a Spark action", for example save or collect. A job is divided into stages of tasks.
- So Spark's "job" is one action, not a scheduled pipeline. Nothing in Spark's own model carries input or output dataset names.

B2. Where inputs and outputs can be read from.
- `QueryExecutionListener` (sql/core/src/main/scala/org/apache/spark/sql/util/QueryExecutionListener.scala, lines 33-60) has two callbacks:
  - `onSuccess(funcName, qe, durationNs)`
  - `onFailure(funcName, qe, exception)`
- `qe` is a `QueryExecution`. Its doc says it "carries detail information like logical plan, physical plan". It is `@DeveloperApi`.
- `QueryExecution` (sql/core/.../execution/QueryExecution.scala, v4.0.0) exposes:
  - `logical` (line 63)
  - `analyzed` (line 121)
  - `optimizedPlan` (line 212)
  - `sparkPlan` (line 227)
  - `executedPlan` (line 248)
  - `id`
- Its class comment says it is "not a public class" and exists "to allow easy access to the intermediate phases of query execution".
- `SparkListener` (core/src/main/scala/org/apache/spark/scheduler/SparkListener.scala) offers `onJobStart` (SparkListenerJobStart, jobId, stageInfos, properties), `onJobEnd`, `onStageCompleted`, `onTaskEnd`, `onApplicationStart/End`, and `onOtherEvent`. These are scheduler-level events and carry no dataset names.
- The OpenLineage code states the limit itself. Source: integration/spark/shared/src/main/java/io/openlineage/spark/agent/lifecycle/OpenLineageRunEventBuilder.java (class comment lines ~100-110). The `OutputDataset` "is constructed by reading the LogicalPlan". Input row and byte metrics come from the StageInfo and RDD tree. There is no direct way to tie the metrics to a dataset "except by inference".
- Conclusion: inputs and outputs are not a field of Spark. They are derived by walking the logical plan (and RDD dependencies).

B3. Which listener the OpenLineage Spark integration uses.
- Class `io.openlineage.spark.agent.OpenLineageSparkListener extends org.apache.spark.scheduler.SparkListener`. Source: integration/spark/app/src/main/java/io/openlineage/spark/agent/OpenLineageSparkListener.java line 66.
- It is not a `QueryExecutionListener`.
- It handles `SparkListenerSQLExecutionStart` and `SparkListenerSQLExecutionEnd` in `onOtherEvent` (lines 144-155). It also handles `onJobStart/End`, `onTaskEnd` and `onApplicationStart/End`.
- It gets the plan with `SQLExecution.getQueryExecution(executionId)`. Source: lifecycle/ContextFactory.java line 98. For end events it calls `qe` reflectively on the end event (ContextFactory.java lines 161-168).
- A code comment at SparkSQLExecutionContext.java line ~125 says "Maybe use QueryExecutionListener?".
- Non-SQL (RDD) jobs go through `RddExecutionContext`.
- Registration: `.config('spark.extraListeners', 'io.openlineage.spark.agent.OpenLineageSparkListener')`. Source: website/docs/integrations/spark/quickstart/quickstart_local.md line 46.
- README: integration/spark/README.md says "uses jvm instrumentation to emit OpenLineage metadata".
- Dataset visitors: input and output datasets come from `QueryPlanVisitor`s over `LogicalPlan` (OpenLineageRunEventBuilder.java lines 126-134).

B4. Job names. The form is `{appName}.{command}.{table}`.
- Specification: website/docs/spec/naming.md, "Job Naming" table (line 77). Example `my_awesome_app.execute_insert_into_hive_table.mydb_mytable`. The same table gives the Airflow task form `{dag_id}.{task_id}`, example `orders_etl.count_orders`. The old spec/Naming.md says it is obsolete.
- Java client: client/java/.../io/openlineage/client/job/Naming.java, `Naming.Spark` (line 37).
- Implementation: integration/spark/shared/src/main/java/io/openlineage/spark/api/naming/JobNameBuilder.java, `build(...)` lines 36-70.
  - appName comes from `ApplicationJobNameResolver`. The providers are, in order: the OpenLineage app-name config, the AWS Glue provider, then `spark.app.name`.
  - command is `executedPlan().nodeName()`, with `WholeStageCodegenExec` unwrapped (lines 109-122).
  - table is a suffix from the output dataset builders and visitors, with "." replaced by "_" (lines 56-62).
  - A config flag can turn off appending the output dataset name.
  - Everything is passed through `NameNormalizer.normalize`: camelCase becomes lower snake_case, and non-alphanumerics become "_".
- RDD jobs: `build(context, rddSuffix)` returns `appName + "." + normalised suffix` (line 72).
- So a Spark job name depends on the plan's top node and the output table. It is not a stable pipeline identity.

C. dbt

C1. `manifest.json`, the project as parsed. Sources: docs.getdbt.com `reference/artifacts/manifest-json.md`, dbt-core v1.11.0 schemas/dbt/manifest/v12.json, and core/dbt/artifacts/resources.
- Produced by any command that parses the project, except deps, clean, debug and init. It contains all resources even when only some are run. Quote: "full representation of your dbt project's resources".
- Top-level keys: metadata, nodes, sources, metrics, exposures, groups, macros, docs, parent_map, child_map, group_map, selectors, disabled. In v12 the schema also lists saved_queries, semantic_models, unit_tests and functions.
- Manifest version for dbt 1.8 through 1.11 is v12 (snippets/_manifest-versions.md).
- Common resource fields from the docs: name, unique_id (`<resource_type>.<package>.<resource_name>`), package_name, path, original_file_path.
- Node fields, verified in schema v12 for the Model node type. The required ones are database, schema, name, resource_type, package_name, path, original_file_path, unique_id, fqn, alias, checksum.
  - Also present: config, tags, description, columns, meta, relation_name, raw_code, refs, sources, depends_on, compiled_code, contract, access, version, primary_key and others.
  - `depends_on` is `{macros: [...], nodes: [...]}` (DependsOn, core/dbt/artifacts/resources/v1/components.py lines 44-45).
  - `config` is a `NodeConfig`. `database` and `schema` come from `HasRelationMetadata` (components.py lines 161-163). `alias` is in `ParsedResourceMandatory` (lines 202-205).
  - `resource_type` values include model, test, snapshot, seed, analysis, operation, source, macro, exposure, metric, unit_test (types.py).
- Nodes that have `depends_on`, `alias`, `database`, `schema` and `config` in the schema: seed, analysis, singular and generic test, hook, model, sql_operation, snapshot, function. I computed this by script.
- Docs caveat: some properties such as `compiled_sql` appear only "for executed nodes".
- The docs page does not list `depends_on`, `config` or `database`. Those come from the code and schema.
- `parent_map` and `child_map` hold first-order parents and children.

C2. `run_results.json`, one invocation. Sources: docs reference/artifacts/run-results-json.md; core/dbt/artifacts/schemas/results.py and run/v5/run.py (v1.11.0); schemas/dbt/run-results/v6.json.
- Docs: it records "a completed invocation of dbt, including timing and status info for each node".
- Docs: "only executed nodes appear in the run results".
- It is produced by build, clone, compile, docs generate, retry, run, seed, show, snapshot, test and run-operation.
- Top-level keys: metadata, results, elapsed_time, args.
- Per result (schema v6 required): status, timing, thread_id, execution_time, adapter_response, message, failures, unique_id, compiled, compiled_code, relation_name. `batch_results` is optional.
- `unique_id` maps the result to a manifest node. The full node is not repeated.
- `timing` is a list of {name, started_at, completed_at}. The name is "compile", "execute" or other.
- `execution_time` is a float in seconds.
- `adapter_response` is a dict that varies by adapter. Docs: it holds success code, `rows_affected`, `bytes_processed`, and is "Not applicable for data tests". `rows_affected` is -1 when it is not applicable, for example for a view.
- `status` is one of three enums (NodeStatus in results.py lines 55-64):
  - RunStatus: success, error, skipped, partial success, no-op.
  - TestStatus: pass, error, fail, warn, skipped.
  - FreshnessStatus: pass, warn, error, runtime error.
- Sources disagree on where a `failures` field is documented. The docs page says nothing, but the schema has it.
- The per-run, per-attempt record is not versioned with the manifest. Each artifact is versioned separately. Run results v6 is current.
- metadata (docs dbt-artifacts.md) has dbt_version, dbt_schema_version, generated_at, adapter_type, env, invocation_id. The manifest adds project_name and more.

C3. How the OpenLineage dbt integration works. Source: integration/dbt/src/openlineage/dbt/__init__.py and integration/common/src/openlineage/common/provider/dbt/{local.py,processor.py,structured_logs.py}.
- Default mode: `dbt-ol run` replaces `dbt run`. It runs dbt as a subprocess (`subprocess.Popen(["dbt"] + args)`, __init__.py line 343). Afterwards it reads the artifacts and emits events. The log line in `consume_local_artifacts` says "will send OpenLineage events at the end of dbt execution".
- It emits no events if `run_results.json` is missing or was not modified by this run (lines 352-361).
- `dbt-ol send-events` emits events for the last run without running dbt (README; __init__.py line ~340).
- Artifact paths: `target/manifest.json`, `run_results.json`, `catalog.json` (local.py lines 103-105). The catalog is optional. The README says that without `catalog.json` there is less table and column metadata.
- It accepts manifest schema versions 2-12 and run-results versions 2-6 (local.py lines 257-259).
- Alternative mode: `--consume-structured-logs` emits events while models execute, reading dbt's structured log file. Source: __init__.py lines 194-259. The README does not mention it.
- Events per node (processor.py `parse_execution`, line 299 onward):
  - It loops over run results. It keeps only unique_ids starting with "model.", "source." or "snapshot.", and skips status "skipped".
  - Inputs are the node's parents from `manifest["parent_map"]` that are models or sources (lines 318-340).
  - The output is the node's own dataset.
  - Start and end times come from the result's `timing` (`get_timings`).
  - The SQL facet comes from `compiled_code`.
  - Output row count comes from `adapter_response["rows_affected"]` (lines 797-799).
  - Status "success" gives START plus COMPLETE. Status "error" gives START plus FAIL. Other statuses raise (lines 710-737).
- Job names:
  - A wrapper run job named `dbt-run-{project_name}` is emitted around the whole invocation (local.py lines 136-175). It can be overridden by --openlineage-dbt-job-name or OPENLINEAGE_DBT_JOB_NAME. With OPENLINEAGE_DBT_USE_EXTENDED_JOB_NAME it becomes `dbt-run-{project}-{profile}-{models/selector}`.
  - Per-model job name (processor.py lines 342-358): `{database}.{schema}.{unique_id without "model." prefix}`, joined by "." (`_format_dataset_name`, line 815), plus ".build.run" if the command is `build`.
  - Because `unique_id` is `model.<package>.<name>`, the last part is `<package>.<name>`. This is my inference from the code. I did not run it.
  - Snapshots get ".snapshot" or ".build.snapshot".
  - Tests get the job name = the test's unique_id (line 565).
- Default job namespace is "dbt", from env OPENLINEAGE_NAMESPACE (__init__.py line 274).
- So the integration produces events only from what dbt wrote after it finished. There is no dbt hook.

D. NOT FOUND / CAVEATS (dbt)

D6. `dbt-labs/dbt-core` main is now the v2.0 Rust rewrite, and its README says v1 development moved to the `1.latest` branch (of what appears to be the renamed repo dbt-labs/dbt). The paths `core/dbt/artifacts/...` and `schemas/dbt/...` exist only at tags such as v1.10.0 and v1.11.0. v2.0 also writes Parquet artifacts and still writes JSON. The docs site mentions this, with a `freshness.json` artifact in 2.0.

E. TRINO

E1. The event listener SPI. Source: core/trino-spi/src/main/java/io/trino/spi/eventlistener/EventListener.java.
- It has default methods `queryCreated(QueryCreatedEvent)`, `queryCompleted(QueryCompletedEvent)`, `requiresAnonymizedPlan()` and `shutdown()`.
- `QueryCreatedEvent` holds createTime, `QueryContext`, `QueryMetadata` (QueryCreatedEvent.java lines 37-57).
- `QueryCompletedEvent` holds metadata, statistics, context, `QueryIOMetadata`, optional selectColumnsLineageInfo (`List<ColumnLineageInfo>`), optional failureInfo, warnings, createTime, executionStartTime, endTime (QueryCompletedEvent.java lines 47-130).
- `QueryMetadata` holds queryId, transactionId, query (text), updateType, preparedQuery, queryState, uri, `List<TableInfo> tables`, routines, plan, jsonPlan, payload. `TableInfo` has `isDirectlyReferenced()`.
- `QueryContext` holds user, originalUser, principal, groups, source, clientInfo, clientTags, remoteClientAddress, userAgent, catalog, schema, resourceGroupId, sessionProperties, serverAddress, serverVersion, environment, queryType, retryPolicy and others.
- `QueryIOMetadata` (QueryIOMetadata.java lines 35-48) is `List<QueryInputMetadata> inputs` plus `Optional<QueryOutputMetadata> output`. So there is at most one output.
- `QueryInputMetadata` (lines 46-130) has connectorName, catalogName, catalogVersion, schema, table, `List<Column(name, type)>`, connectorInfo, connectorMetrics, physicalInputBytes, physicalInputRows.
- `QueryOutputMetadata` (lines 42-90) has catalogName, catalogVersion, schema, table, optional `List<OutputColumnMetadata>`, connectorOutputMetadata, jsonLengthLimitExceeded. `OutputColumnMetadata` has column name, type and source columns.
- `QueryFailureInfo` has errorCode, failureType, failureMessage, failureTask, failureHost, failuresJson.
- Where the class doc says so, the event classes are JSON serialisable with compatibility "not guaranteed across versions" (QueryMetadata.java class comment).

E2. Trino ships an OpenLineage listener plugin: plugin/trino-openlineage/ (class `OpenLineageListener implements EventListener`, OpenLineageListener.java line 68). Docs: docs/src/main/sphinx/admin/event-listeners-openlineage.md.
- Run id: a UUIDv7 built from the query create time and a hash of the query id (`getRunId`, lines 134-137). The docs say the same.
- Events: START from `queryCreated` and COMPLETE or FAIL from `queryCompleted`. FAIL is chosen when `queryState` equals "FAILED". The error message is added as a run facet (lines 215-285).
- Job name: from the config `openlineage-event-listener.job.name-format`. The default is `$QUERY_ID`. The variables are $QUERY_ID, $USER, $SOURCE, $CLIENT_IP (OpenLineageListenerConfig.java line 36; job/OpenLineageJobInterpolatedValues.java lines 17-20).
- Job namespace: the config `openlineage-event-listener.namespace`, defaulting to the dataset namespace (listener lines 87-89).
- Dataset namespace: `trino://host:port`, from `trino.uri` with its scheme replaced (`defaultNamespace`, line 401).
- Dataset name: `catalog.schema.table` (`getDatasetName`, listener lines 396-399, `format("%s.%s.%s", ...)`).
- Job facets: jobType (processingType BATCH, integration TRINO, jobType QUERY) and an SQL facet with the query text and dialect "trino" (listener lines 287-300).
- Run facets: processing_engine (name "trino", server version), and Trino-specific facets `trino_metadata`, `trino_query_context`, `trino_query_statistics`. Any of these can be disabled in config.
- Inputs come from `QueryMetadata.getTables()` filtered to `isDirectlyReferenced` (lines 302-322), not from `QueryIOMetadata`. Schema facet fields carry the column names.
- Outputs come from `QueryIOMetadata.getOutput()` (lines 337-386), with schema (name and type) and a column-lineage facet built from `OutputColumnMetadata.getSourceColumns()`.
- Input and output datasets are attached only to the COMPLETE or FAIL event, not to START (lines 215-235 show START without inputs and outputs).
- Query types: the code default is ALTER_TABLE_EXECUTE, DELETE, INSERT, MERGE, UPDATE, DATA_DEFINITION (OpenLineageListenerConfig.java lines 38-45). SELECT is not included by default, so a plain SELECT emits no event unless configured. The docs state "every query that creates or modifies Trino tables".

F. WHERE SOURCES DISAGREE OR ARE SILENT
1. Trino docs vs code, default query types. The docs table says the default is `DELETE,INSERT,MERGE,UPDATE,ALTER_TABLE_EXECUTE` (event-listeners-openlineage.md, near line 143). The code adds DATA_DEFINITION.
2. Trino docs vs code, dataset name. The docs mapping says `{schema}.{table}`. The code emits `catalog.schema.table`. Prefer the code.
3. Trino docs for `name-format` start "Custom namespace to use for the job name attribute". That reads as a copy error. The code uses it as the job name.
4. The OpenLineage naming table has no Trino or dbt job row. Only Airflow, Spark, SQL and Debezium are listed. The dbt and Trino forms above are from the code, not the specification.
5. Airflow: no documentation defines `try_number` precisely. It is read from code. Airflow `main` and 3.3.0 differ on how earlier tries are stored (A5).
6. Spark: I found no Spark documentation stating that inputs and outputs are available from the plan. The `QueryExecution` fields are public API in practice but the class is documented as "not a public class", and the interface is `@DeveloperApi`.
7. Not checked: the Airflow OpenLineage provider; Spark's non-SQL RDD path in detail; dbt `sources.json` and `freshness.json`.
