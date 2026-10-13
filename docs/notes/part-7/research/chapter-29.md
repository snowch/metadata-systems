# Sources for Chapter 29 (research)

A research note, gathered on 13 October 2026 from each project's own repository. Facts the chapter states are re-checked and recorded in `docs/sources.md` before they land.

SOURCES FOR CHAPTER 29

Method and versions. I read shallow git clones of each project's main branch. Nothing was executed, so every statement about behaviour is from reading code, SQL or docs. Each is marked "code reading" where it is an inference from SQL or Java rather than a documented claim.
- MarquezProject/marquez, branch main, commit 180f37b22387146187af1ef0279e3ee1d1ccd789 (12 Apr 2026). Its spec/openapi.yml says version 0.51.2-SNAPSHOT. `build.gradle` line 60 pins `openlineageVersion = '1.23.0'`.
- OpenLineage/OpenLineage, branch main, commit 60261f0b57fb1370c2c6c3cadc9f1721b6c3c3b5 (12 Oct 2026). `client/python/pyproject.toml` and `constants.py` say openlineage-python 1.55.0. The core spec `$id` is https://openlineage.io/spec/2-0-2/OpenLineage.json.
- apache/airflow, branch main, commit 7f0d50cffc61a48650590078f6832b349860322b (12 Oct 2026), sparse checkout of providers/openlineage. `__init__.py` says provider version 2.20.3.
- The GitHub REST API was blocked in this session, so I used git clones and raw.githubusercontent.com. Marquez paths below are relative to `api/src/main/java/marquez/` unless they start with `spec/`, `docs/` or `api/src/main/resources/`.

====================================================================
1. MARQUEZ
====================================================================

1.1 Receiving events
- Claim: Marquez accepts a run event as an HTTP POST of JSON to `/api/v1/lineage`. The resource class is mounted at `/api/v1`, and `create` is `@POST @Consumes(APPLICATION_JSON) @Path("/lineage")`.
  Source: `api/OpenLineageResource.java` lines 49, 61-68 (main).
- Claim: The same endpoint accepts three OpenLineage event kinds: run events (`LineageEvent`), dataset events (`DatasetEvent`) and job events (`JobEvent`). Any other type is logged as a warning, skipped without error, and echoed back with HTTP 200.
  Source: `api/OpenLineageResource.java` lines 70-90.
- Claim: Marquez picks the event kind from the last path segment of `schemaURL` (`/RunEvent`, `/DatasetEvent` or `/JobEvent`). A missing `schemaURL`, or one with no slash, means a run event.
  Source: `service/models/BaseEvent.java` (`@JsonTypeInfo ... property = "schemaURL"`, `defaultImpl = LineageEvent.class`); `service/models/EventTypeResolver.java` lines 22-33 and `typeFromId`.
- Claim: A successful POST returns 201 with no body. An `IllegalArgumentException` gives 400. Any other error gives 500.
  Source: `api/OpenLineageResource.java` lines 93-109.
  DISAGREEMENT: `spec/openapi.yml` lines 575-591 (operationId `recordLineage`, "Record a single lineage event") documents only `'200': OK`. The code returns 201.
- Claim: A run event must have `eventTime`, `run` (with `run.runId`), `job` (with `job.namespace` and `job.name`) and `producer`. `eventType`, `inputs`, `outputs` and `schemaURL` are optional. Facet base fields `_producer` and `_schemaURL` are `@NotNull`.
  Source: `service/models/LineageEvent.java` lines 43-53, 75-78, 122-123, 209-210.
- Claim: In Marquez, the client's `eventType` is a free string. `getRunState` maps `complete` to COMPLETED, `abort` to ABORTED, `fail` to FAILED and `start` to RUNNING. Anything else, including `RUNNING`, `OTHER` and a missing type, becomes RUNNING.
  Source: `db/OpenLineageDao.java` lines 1103-1119.
- Port: README says the Docker setup listens on 5000 (admin 5001) and the non-Docker build on 8080 (admin 8081). `marquez.example.yml` defaults `MARQUEZ_PORT` to 8080. `docker/up.sh` line 70 sets `API_PORT=5000`.
  Source: README.md lines 81 and 171.

1.2 Processing: what a run event creates or updates (code reading)
Service entry: `service/OpenLineageService.java`, `createAsync(LineageEvent)`, lines 122-158. It runs two tasks concurrently on an executor and waits for both:
(a) it stores the raw event;
(b) it updates the Marquez model (`updateMarquezModel`).
The two tasks have no ordering between them.

- Raw event store. Every run event is inserted into the `lineage_events` table with event_type, event_time (taken from the event, not the receive time), run_uuid, job_name, job_namespace, the whole JSON, and producer. This is a plain INSERT with no ON CONFLICT.
  Source: `db/OpenLineageDao.java` lines 90-108.
  Migration `V17.2__open_lineage.sql` created `lineage_events` with a primary key on (event_time, event). `V20__drop_lineage_pk.sql` dropped it. No later migration that mentions `lineage_events` adds a unique constraint, so repeated events are kept as extra rows (V33, V36, V47, V54, V66.2 and V71 are index or column changes). Both files are in `api/src/main/resources/marquez/db/migration/`.
- Namespace. `upsertNamespaceRow(... formatNamespaceName(job.namespace), "anonymous")`. The job namespace is sanitised so that characters outside `[a-zA-Z0-9:/\-_.@+]` become `_`. A conflict on name just updates `updated_at`. The default owner is the literal "anonymous".
  Source: `db/OpenLineageDao.java` lines 81-82, 293-300, 833-835; `db/NamespaceDao.java` line 151 (ON CONFLICT(name) DO UPDATE).
  Dataset namespaces also get a row. The first dataset-namespace upsert at line 840 uses the raw `ds.getNamespace()`, and the second at lines 865-871 uses the sanitised name.
- Job. `buildJobFromEvent` upserts a row in `jobs` (through `jobs_view`) with type, description (from `DocumentationJobFacet`), location (from `SourceCodeLocationJobFacet.url`), the input dataset ids and the current run. A trigger does `ON CONFLICT (namespace_uuid, name) DO UPDATE`, so a repeated event updates the same job row.
  Source: `db/OpenLineageDao.java` lines 505-594; `api/src/main/resources/marquez/db/migration/R__Jobs_view_and_rewrite_function.sql` lines 41-77.
- Job hierarchy from ParentRunFacet. If the run has a parent run facet, Marquez also creates or finds a parent job and a parent run record. The child job name has the `<parent>.` prefix stripped, and the stored full name is `parent.name || '.' || name`. The code comments on a workaround for conflicting parent run UUIDs, quoted: "Addresses an Airflow integration bug that generated conflicting run UUIDs".
  Source: `db/OpenLineageDao.java` lines 305-307, 531-558, 596-744 (comment at line 625); the trigger SQL above, lines 36-40.
- Run args. A row is upserted from nominal start and end times and the parent run's id, name and namespace, keyed by a checksum.
  Source: `db/OpenLineageDao.java` lines 328-333 and 1121-1141.
- Run. One row per run in `runs`. The run id is `UUID.fromString(runId)`, and a non-UUID id is hashed to a name-based UUID. The original string is kept as `external_id`.
  Source: `db/OpenLineageDao.java` lines 335-352 and 1143-1150 (`runToUuid`); `service/OpenLineageService.java` lines 167-175.
  The run upsert is `INSERT ... ON CONFLICT(uuid) DO UPDATE SET external_id, updated_at, current_run_state = EXCLUDED.current_run_state, transitioned_at = EXCLUDED.transitioned_at, nominal_start_time = COALESCE(EXCLUDED..., runs.nominal_start_time), nominal_end_time = COALESCE(...), location`.
  Source: `db/RunDao.java` lines 225-270 (the ON CONFLICT clause is at 258-266). A variant without a state is at about lines 271-320 and omits `current_run_state`.
- Run state. When `eventType` is present, each event INSERTs a new row in `run_states` (uuid, transitioned_at = event time, run_uuid, state). `run_states` has no unique constraint.
  Source: `db/RunStateDao.java` lines 23-26; `db/OpenLineageDao.java` lines 356-367 (when `eventType` is null no `run_states` row is written); `V1__initial_schema.sql` lines 100-105.
  The `runs` row records only one start pointer and one end pointer: `started_at` and `start_run_state_uuid` for RUNNING, `ended_at` and `end_run_state_uuid` for COMPLETED, ABORTED or FAILED. Both pointers are overwritten each time a matching event arrives.
  Source: `db/OpenLineageDao.java` lines 362-366; `db/RunDao.java` lines 53-75; `common/models/RunState.java` lines 12-33 (enum NEW, RUNNING, COMPLETED, ABORTED, FAILED, OTHER; `isStarting()` is only RUNNING; `isDone()` is COMPLETED, ABORTED or FAILED).
- Run facets, job facets, dataset facets. They are stored in separate facet tables (`insertRunFacetsFor`, `insertJobFacetsFor`, `insertDatasetFacetsFor`, and the input and output variants). Marquez gives special treatment to `nominalTime` and `parent` on runs; `documentation`, `sourceCodeLocation`, `sql` and `jobType` on jobs; and `documentation`, `schema`, `lifecycleStateChange`, `dataSource`, `columnLineage` and `symlinks` on datasets. Every other facet goes through a `@JsonAnySetter` map and is stored as raw JSON.
  Source: `db/OpenLineageDao.java` lines 353, 369, 378-379, 394-395, 422-503; `service/models/LineageEvent.java` lines 86-103 (RunFacet), 255-259 (JobFacet), 411-420 (DatasetFacets), 654-690 (input and output facet maps).
- Source (a `sources` row). For each input or output dataset, the source is taken from `DatasourceDatasetFacet` (`name`, `uri`). Without that facet it is the row named "default". `getSourceType` always returns POSTGRESQL and `getDatasetType` always returns DB_TABLE, whatever the event says.
  Source: `db/OpenLineageDao.java` lines 81, 844-858, 1095-1101; `db/SourceDao.java` lines 50 and 111 (ON CONFLICT(name) DO UPDATE).
- Dataset. A `datasets` row is upserted using a "symlink" row for the name and the facet `symlinks`. Schema fields from `SchemaDatasetFacet` become `dataset_fields` rows plus a schema version.
  Source: `db/OpenLineageDao.java` lines 837-1012 (symlink at 873-903, dataset upsert at 910-923, fields at 925-944).
- Dataset version.
  - For an output, a new version is created. The version UUID is a name-based UUID of namespace, source name, dataset name, physical name, schema location, fields, lifecycle state and the run id.
  - For an input, the dataset's current version is reused.
  - `INSERT ... ON CONFLICT(version) DO UPDATE SET run_uuid`.
  Source: `db/OpenLineageDao.java` lines 946-984; `common/Utils.java` lines 298-355 (`newDatasetVersionFor`); `db/DatasetVersionDao.java` lines 335-340.
  The dataset's current-version pointer for an output moves only when a COMPLETE event is processed, or the job is a streaming job. Source: `service/OpenLineageService.java` lines 149-150 and 204-213. For an input it is set only if the dataset has none yet (`OpenLineageDao.java` lines 993-1002).
- Job version.
  - Created only when the run reaches a done state (COMPLETE, ABORT or FAIL; code reading).
  - The version UUID is a name-based UUID of job namespace, job name, the sorted input dataset ids, the sorted output dataset ids and the job location.
  - It is upserted with `ON CONFLICT(version) DO UPDATE SET updated_at`. The run is linked to it, the job's current version is updated, and the job facets are linked.
  - A START event creates no job version for a batch job.
  Source: `db/OpenLineageDao.java` lines 167-178 and 759-774; `db/JobVersionDao.java` lines 180-182, 464-526, 543-575; `common/Utils.java` lines 250-280.
  Streaming jobs follow a different rule: a version is created at job start, keyed by the datasets. `OpenLineageDao.java` lines 776-815; CHANGELOG.md line 159.
- Column lineage. Marquez reads `columnLineage` facet `fields.<col>.inputFields` plus the deprecated `transformationDescription` and `transformationType`. Its model class has no `transformations` array. Only output datasets are handled.
  Source: `db/OpenLineageDao.java` lines 1014-1089; `service/models/LineageEvent.java` lines 626-631. The spec marks those two fields as deprecated in `spec/facets/ColumnLineageDatasetFacet.json` (OpenLineage repo).
- Listener notifications. After the model update, Marquez notifies run-transition listeners: job output on COMPLETE (or streaming), job input, and a run transition with old state `null` for RUNNING or old state RUNNING otherwise.
  Source: `service/OpenLineageService.java` lines 139-155 and 286-295.
- Marquez's own description of its model: the data model is "centralized" with "built-in metadata versioning support". Run-level metadata is tracked by calls to `/lineage`. Dataset versions are immutable and mapped to the run id that changed the dataset. A job version links to a code reference, the latest run id and versioned input and output datasets.
  Source: `docs/docs/quickstart/index.mdx` lines 71-85.

1.3 Repeated, late, out-of-order, after-terminal events
What I found:
- No documentation. A search of README.md, CHANGELOG.md, `docs/docs/**` and `spec/openapi.yml` for out of order, late, duplicate, idempotent, replay, retry and terminal found no statement about how Marquez treats repeated, late or out-of-order events. The only hit for "out of order" is a comment in `common/models/DatasetId.java` line 19 about job inputs and outputs.
- One test touches ordering. `OpenLineageIntegrationTest.java` line 583, `testOpenLineageJobHierarchyAirflowHandlesParentForEventsOutOfOrder`: it sends a COMPLETE with no parent facet first, then a START with the parent facet. It asserts one run, the right job and parent job, and `parentJobName`. It does not assert the final run state.
  Source: `api/src/test/java/marquez/OpenLineageIntegrationTest.java` lines 583-633.
- The spec side is in section 3 of the Spec notes below. The spec's own docs are not fully consistent.

What the code does (code reading, all `db/` and `service/` paths above). I found no guard on event time or terminal state in the run upsert; anything beyond that is my reading of the SQL:
- Duplicate event (same run id, same eventType).
  - Raw: another `lineage_events` row.
  - `runs` row: updated in place.
  - `run_states`: another row.
  - `ended_at` and `end_run_state_uuid` (or the start pair): overwritten with the later duplicate's values.
  - Dataset version: same hash, because the run id is part of it, so it is the same row (`run_uuid` rewritten).
  - Job version: same hash, so the same row (`updated_at` changed).
  - Namespace, source, job: same rows.
  - So versions are stable, but history rows (`lineage_events`, `run_states`) are not deduplicated.
- Late or out-of-order event (a START arriving after a COMPLETE). The `runs` upsert sets `current_run_state = EXCLUDED.current_run_state` and `transitioned_at = EXCLUDED.transitioned_at` without comparing event times or checking whether the existing state is terminal (`RunDao.java` lines 258-266).
  - So the arrival order decides `current_run_state`: a late START would set it back to RUNNING.
  - The late START also overwrites `started_at` and `start_run_state_uuid`.
  - `ended_at` and `end_run_state_uuid` from the earlier COMPLETE stay.
  - `run_states` keeps both rows, ordered by their event times.
- After-terminal events:
  - A second terminal event of a different kind (FAIL after COMPLETE) replaces `current_run_state` and the end pointers the same way.
  - An OTHER or RUNNING event after COMPLETE is mapped to RUNNING (`getRunState`), so it also sets the state back to RUNNING.
  - Marquez never rejects any of these. All return 201.
- Missing eventType. `getRunState(null)` is RUNNING, but no `run_states` row is written and `runs.current_run_state` is not updated, because the state-less upsert variant is used (`OpenLineageDao.java` lines 349-367; `RunDao.java` `upsert(RunUpsert)`, lines about 335-360).

====================================================================
2. OPENLINEAGE PYTHON CLIENT (client/python, package openlineage-python 1.55.0)
====================================================================
All paths under `client/python/src/openlineage/client/` in OpenLineage/OpenLineage, main.

2.1 Sending
- Claim: A producer builds an event object and calls `OpenLineageClient.emit(event)`. `emit` accepts the v1 classes (`openlineage.client.run`: RunEvent, DatasetEvent, JobEvent) or the v2 classes (`openlineage.client.event_v2`). Any other type raises `ValueError`. Before sending it runs the environment-variable, tags, source-code-location, dataset-reducer and filter steps, then calls `transport.emit`.
  Source: `client.py` lines 185-216.
- The old `openlineage.client.run` module warns that it is deprecated in favour of `event_v2`. Its schema URL is `.../spec/1-0-5/OpenLineage.json#/definitions/RunEvent`. Source: `run.py` lines 20-24.
- Transports registered in the default factory, by their `kind` name: `composite`, `http`, `async_http`, `kafka`, `msk-iam`, `console`, `noop`, `file`, `transform`, `amazon_datazone_api`, `datadog`, `gcplineage`.
  Source: `transport/__init__.py` lines 23-35; each class's `kind =` line (for example `http.py` line 524, `console.py` line 21, `msk_iam.py` line 72, `amazon_datazone.py` line 40).
- How the client chooses a transport (first match wins): `OPENLINEAGE_DISABLED=true` gives noop; a transport object passed in; the config `transport.type` from the constructor, an `openlineage.yml` (found via `OPENLINEAGE_CONFIG`, the working directory, or `~/.openlineage`) or `OPENLINEAGE__...` env vars; the deprecated `url` argument; the `OPENLINEAGE_URL` env var (http); otherwise the console transport with a warning.
  Source: `client.py` lines 260-303, 320-340, 374-400.
- The http transport POSTs the serialised event to `urljoin(url, endpoint)`. `HttpConfig.endpoint` defaults to `"api/v1/lineage"` and the timeout to 5.0 seconds. Source: `transport/http.py` lines 459-466 (config) and 575-586 (post).
- The console transport writes with `log.info(Serde.to_json(event))`. It uses the logging module, not `print`, although the factory's warning says "will print events to console". Source: `transport/console.py` line 30 and `transport/factory.py` line 43.
- `constants.py` also defines `DEFAULT_OPENLINEAGE_URL = "http://localhost:5000"`. A search of `src/` found no other use of it.

2.2 Defaults the client fills in
- `producer` defaults to `DEFAULT_PRODUCER = f"https://github.com/OpenLineage/OpenLineage/tree/{__version__}/client/python"`, which is `.../tree/1.55.0/client/python`. Source: `constants.py` line 11; `generated/base.py` lines 12-24, 31-34 (`BaseEvent.__attrs_post_init__` sets `producer` from module-level `PRODUCER` when empty). `set_producer()` changes it (the Airflow provider calls it at `plugins/adapter.py` line 73).
- `schemaURL` is not a constructor argument (`init=False`). It is set from `_get_schema()`. For a v2 run event this gives `https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent`. Source: `generated/base.py` lines 31-34, 315-317.
- Facet `_producer` defaults to the same `PRODUCER`, and `_schemaURL` is set per facet class. Example: `.../spec/facets/1-2-0/ParentRunFacet.json#/$defs/ParentRunFacet`. Source: `generated/base.py` lines 59-72; the facet classes in `generated/` (the versions match section 3).
- `eventType` has no default in effect (default `None`), though its docstring repeats the spec text "required to issue 1 START event and 1 of [ COMPLETE, ABORT, FAIL ] event per run". Source: `generated/base.py` lines 296-306.
- `run.runId` is validated with `UUID(value)`. A non-UUID run id raises `ValueError` in the v2 client. Source: `generated/base.py` lines 288-292. Marquez, by contrast, accepts non-UUID run ids and hashes them (section 1.2).
- `eventTime` must parse as ISO 8601 and contain a time part. Source: `generated/base.py` lines 36-42.

====================================================================
3. FACETS (spec/facets/ in OpenLineage/OpenLineage, main)
====================================================================
Core spec: spec/OpenLineage.json, `$id` https://openlineage.io/spec/2-0-2/OpenLineage.json. Required fields there: BaseEvent has eventTime, producer, schemaURL. RunEvent adds run and job. Run has runId. Job has namespace and name. Dataset has namespace and name. BaseFacet has _producer and _schemaURL. `eventType` is not in the required list, although its description says one START and one terminal event are required per run.

Every facet below also carries the BaseFacet fields `_producer` and `_schemaURL`, which are always required.

| Facet (file) | Version in `$id` | Facet-specific required fields |
|---|---|---|
| ParentRunFacet (`spec/facets/ParentRunFacet.json`) | 1-2-0 | `run`, `job`. Inside `run`: `runId` (uuid). Inside `job`: `namespace`, `name`. Optional `root` (if given, needs `run` and `job`; RootRun needs `runId`, RootJob needs `namespace` and `name`). |
| NominalTimeRunFacet (`NominalTimeRunFacet.json`) | 1-0-1 | `nominalStartTime`. Optional `nominalEndTime`. |
| ErrorMessageRunFacet (`ErrorMessageRunFacet.json`) | 1-0-1 | `message`, `programmingLanguage`. Optional `stackTrace`. |
| ProcessingEngineRunFacet (`ProcessingEngineRunFacet.json`) | 1-1-1 | `version`. Optional `name`, `openlineageAdapterVersion`. |
| JobTypeJobFacet (`JobTypeJobFacet.json`) | 2-0-4 | `processingType`, `integration`. Optional `jobType`, `emissionPattern`. |
| SQLJobFacet (`SQLJobFacet.json`) | 1-1-0 | `query`. Optional `dialect`. |
| SourceCodeLocationJobFacet (`SourceCodeLocationJobFacet.json`) | 1-1-0 | `type`, `url`. Optional `repoUrl`, `path`, `version`, `tag`, `branch`, `pullRequestNumber`. |
| SchemaDatasetFacet (`SchemaDatasetFacet.json`) | 1-2-0 | None at the facet level (`fields` is an optional array). Each field item requires `name`; optional `type`, `description`, `ordinal_position`, nested `fields`. |
| DatasourceDatasetFacet (`DatasourceDatasetFacet.json`). The file and class are "Datasource", not "DataSource". | 1-0-1 | None. Optional `name`, `uri`. |
| ColumnLineageDatasetFacet (`ColumnLineageDatasetFacet.json`) | 1-2-0 | `fields`. Each entry in `fields` requires `inputFields` (array). Each input field requires `namespace`, `name`, `field`; optional `transformations`, each of which requires `type` (optional `subtype`, `description`, `masking`). Also optional `dataset` (array of the same input-field object). `transformationDescription` and `transformationType` are marked deprecated. |
| OutputStatisticsOutputDatasetFacet (`OutputStatisticsOutputDatasetFacet.json`) | 1-0-2 | None. Optional `rowCount`, `size`, `fileCount` (all integers). |
| DataQualityMetricsInputDatasetFacet (`DataQualityMetricsInputDatasetFacet.json`) | 1-0-3 | `columnMetrics`. Optional `rowCount`, `bytes`, `fileCount`, `lastUpdated`. Each column's metrics are all optional (`nullCount`, `distinctCount`, `sum`, `count`, `min`, `max`, `quantiles`). |

Notes:
- The facet type classes (input facet, output facet, run facet and so on) are chosen by position: input facets sit under an input dataset's `inputFacets`, output facets under `outputFacets`, as the `InputDataset` and `OutputDataset` classes show (`generated/base.py` lines 190-198 and the matching output class).
- The Python client's generated classes use the same versions (checked with grep over `client/python/src/openlineage/client/generated/`).

Spec notes on run lifecycle (relevant to 1.3):
- `website/docs/spec/run-cycle.md` lines 29-36 says events for one run are "accumulative"; COMPLETE, ABORT and FAIL are terminal. Quote: "no other events related to this run will be emitted" (lines 30-31). OTHER may be sent "anytime before the terminal states, also before START".
- DISAGREEMENT within the spec: `spec/OpenLineage.json` line 35 says "Additional events with OTHER eventType can be added to the same run" and gives the example of sending metadata "after the run is complete". `run-cycle.md` says nothing is emitted after a terminal event. Both texts are in the same repository.
- Streaming and service jobs: `run-cycle.md` lines 53-72 says START or terminal events "should not be relied upon" for them, and that a service may start again after a terminal event (line 111).
- Silence: I searched `website/docs/spec`, `guides`, `faq.md` and `client` for out of order, duplicate and idempotent, and found no consumer rule for duplicate events, late events or events after a terminal event. The spec is silent on what a consumer does with them.
- `spec/OpenLineage.md` line 12-13 says "Sending at least a START event and a COMPLETE/FAIL/ABORT event is required" (not quoted exactly) and that a run id "must be a UUID" (lines 30-32).

====================================================================
4. AIRFLOW OPENLINEAGE PROVIDER (providers/openlineage, version 2.20.3)
====================================================================
All paths under `providers/openlineage/src/airflow/providers/openlineage/` in apache/airflow, main.

- Task job name: `{dag_id}.{task_id}`. Source: `utils/utils.py` lines 177-178 (`get_job_name` returns `f"{task.dag_id}.{task.task_id}"`). The DAG itself is a job named `dag_id` (`plugins/adapter.py`, `dag_started` uses `job_name=dag_id`, about lines 409-460). The job type is carried in `JobTypeJobFacet.jobType` as "DAG" or "TASK" (`adapter.py` lines 75-76, 651-653).
  This matches the naming table in `website/docs/spec/naming.md` line 76: "Airflow task | `{dag_id}.{task_id}` | `orders_etl.count_orders`".
- Job namespace: `conf.namespace()` reads `[openlineage] namespace`. If empty it uses the `OPENLINEAGE_NAMESPACE` environment variable, and if that is unset the string "default". Source: `conf.py` lines 118-125; used in `adapter.py` line 659 (`Job(namespace=conf.namespace(), ...)`).
  NOTE: `provider.yaml` lines 246-253 documents the option with `default: ~` and the example "my_airflow_instance_1". The code default of "default" is only in `conf.py`.
- Parent job namespace in the parent facet also defaults to `conf.namespace()` (`utils/utils.py` lines 368-369, 392-393).
- Other configuration (names only):
  - Transport: `[openlineage] transport` is a JSON string (`conf.py` lines 127-133; `provider.yaml` lines 280-287, example `{"type": "http", "url": "http://localhost:5000", "endpoint": "api/v1/lineage"}`).
  - Config file: `config_path` (`provider.yaml` lines 124-131).
  - Other: `disabled`, `disabled_for_operators`, `custom_extractors`, `custom_run_facets`, `selective_enable` (deprecated, replaced by `emission_policy`), `spark_inject_parent_job_info`, `spark_inject_transport_info`, `include_full_task_info`, `debug_mode`.
  - Source: `conf.py` function list; `provider.yaml` `openlineage:` section starting line 110.
  - The provider hands events to `OpenLineageClient` (`plugins/adapter.py` lines 89-137, 164-225), so transports are the client's.
- Provider's own producer string: `https://github.com/apache/airflow/tree/providers-openlineage/{OPENLINEAGE_PROVIDER_VERSION}` (`utils/utils.py` line 137). It calls `set_producer(_PRODUCER)` (`adapter.py` line 73).
- Run ids are deterministic UUIDs. Task: `generate_static_uuid(instant=logical_date, data=f"{namespace}.{dag_id}.{task_id}.{try_number}.{map_index}")` (`utils/utils.py` lines 1589-1614). DAG run: `data=f"{namespace}.{dag_id}.{clear_number}"` (lines 1630-1647).
- Run facets attached to task events (names only; keys as in the dictionaries):
  - `parent` (ParentRunFacet) pointing to the DAG run (see next bullet)
  - `airflow` (AirflowRunFacet) and `airflow_mappedTask` (AirflowMappedTaskRunFacet, only for mapped tasks)
  - `nominalTime` (NominalTimeRunFacet, built from the DAG run's data interval, when a start is known)
  - `processing_engine` (ProcessingEngineRunFacet, name "Airflow")
  - `errorMessage` (ErrorMessageRunFacet, FAIL events only, with `programmingLanguage="python"` and the stack trace if available)
  - `debug` (only when `debug_mode` is on)
  - any facets from user-provided/custom facets and from the operator's extractor
  - `unknownSourceAttribute` (older, marked deprecated in the log text)
  Source: `plugins/listener.py` lines 329-346 (START), 493-509 (success), 671-687 (fail); `utils/utils.py` lines 252-300, 674-688, 1376-1396, 1399-1422, 2095-2110; `plugins/adapter.py` lines 580-601 (`_build_run`: `nominalTime`, `processing_engine`), 380-382 (`errorMessage`).
- Job facets attached to task events: `jobType` (JobTypeJobFacet, `integration="AIRFLOW"`, `processingType="BATCH"`), plus `documentation`, `ownership` and `tags` when present, and whatever the operator's extractor returns (for SQL operators this includes `sql` (SQLJobFacet), `api/sql.py` line 177 and `sqlparser.py` line 319).
  Source: `plugins/adapter.py` lines 604-659.
- Does a task event send a ParentRunFacet pointing at the DAG run? Yes. The listener computes `parent_run_id = self.adapter.build_dag_run_id(dag_id, logical_date, clear_number)` and passes `get_task_parent_run_facet(parent_run_id=..., parent_job_name=dag.dag_id, ...)`. `_get_parent_run_facet` fills the facet's `run.runId` with the DAG run id, `job` with the provider namespace and `dag_id`, and `root` with the same values unless the DAG run conf supplies a different root.
  Source: `plugins/listener.py` lines 260-264, 331-336; `utils/utils.py` lines 362-433.
- The DAG run's own events: they carry the parent facet only if the DAG run conf has complete parent (and optionally root) identifiers, for example for a DAG triggered by another task. `get_dag_parent_run_facet` returns an empty dict otherwise. DAG-run events carry `airflowDagRun`, and success and fail events carry `airflowState`.
  Source: `utils/utils.py` lines 543-575; `plugins/listener.py` lines 1198-1203, 1304-1307; `plugins/adapter.py` lines 409-460, 540-566. `docs/macros.rst` lines 37-51 and 169 also say a triggering relationship produces a ParentRunFacet on the triggered run, while a consuming DAG run gets a `JobDependenciesRunFacet` instead.

====================================================================
5. NAMING CONVENTIONS
====================================================================
- `spec/Naming.md` in OpenLineage/OpenLineage main is now a stub: "This document is obsolete, please look at the OpenLineage Naming Conventions" (line 1), pointing to https://openlineage.io/docs/spec/naming. The current text is `website/docs/spec/naming.md`. That file's "Additional Resources" still links to `spec/Naming.md` (line 102), a small inconsistency.
- General rule: job namespaces come from schedulers and dataset namespaces from datasources (naming.md lines 10-11). The job namespace is "usually set in OpenLineage client config" and the job name is unique within its namespace (lines 71-72).

Dataset forms, from the table at `website/docs/spec/naming.md` lines 17-55:

| Store | Namespace | Name |
|---|---|---|
| Postgres (line 35) | `postgres://{host}:{port}` | `{database}.{schema}.{table}` |
| BigQuery (line 24) | `bigquery` | `{project id}.{dataset name}.{table name}` |
| Snowflake (line 38) | `snowflake://{organization name}-{account name}` (legacy: `snowflake://{account-locator}(.{compliance})(.{cloud_region_id})(.{cloud})`) | `{database}.{schema}.{table}` |
| S3 (line 52) | `s3://{bucket name}` | `{object key}` |
| GCS (line 45), for comparison | `gs://{bucket name}` | `{object key}` |
| Local file system (line 48) | `file` | `{path}` |

- Snowflake caveat (lines 60-64): the legacy account-locator form is supported but yields dataset ids that will not match ids from the orgname-accountname form, and "existing lineage nodes won't connect to new ones" (paraphrase of lines 62-64).

Job forms (lines 66-79):

| Job type | Name | Example |
|---|---|---|
| Airflow task | `{dag_id}.{task_id}` | `orders_etl.count_orders` |
| Spark job | `{appName}.{command}.{table}` | `my_awesome_app.execute_insert_into_hive_table.mydb_mytable` |
| SQL | `{schema}.{table}` | `gx.validate_datasets` |
| Debezium | `{topic.prefix}.{taskId}` | `inventory.0` |

- Run naming (lines 81-91): runs are named with client-generated UUIDs; the client keeps the same id for the whole run cycle. This agrees with `spec/OpenLineage.md` lines 30-32 (a run id "must be a UUID").
- The doc's examples (for instance `orders_etl.count_orders`, `gx.validate_datasets`) are written by the project. Do not reuse them as course examples. This is relevant to the course's originality rule.

====================================================================
WHAT I COULD NOT FIND, AND DISAGREEMENTS TO CARRY INTO docs/sources.md
====================================================================
1. No Marquez documentation says what happens with repeated, late, out-of-order or after-terminal events. Everything in 1.3 is my reading of the SQL and Java at commit 180f37b. State it as "Marquez's code does X", not "Marquez documents X". If the chapter wants to show the behaviour, it should be tested against a running Marquez, which I did not do.
2. The OpenLineage spec is silent on what a consumer should do with duplicates or late events. It also contradicts itself on events after a terminal event (`spec/OpenLineage.json` line 35 vs `website/docs/spec/run-cycle.md` lines 29-36).
3. Marquez's `spec/openapi.yml` documents 200 for POST `/lineage`, while the code returns 201.
4. The Marquez `eventType` mapping has no case for RUNNING or OTHER; both fall through to the default RUNNING.
5. Marquez forces `source type = POSTGRESQL` and `dataset type = DB_TABLE` for every dataset arriving by OpenLineage.
6. `spec/Naming.md` is obsolete. The authoritative text is the website page in the same repository.
7. The Python client's `run.runId` validator rejects non-UUIDs, but Marquez accepts and hashes them.
8. I did not check the OpenLineage Java client, the website's client docs for the Python client, or OpenLineage's own doc pages for each facet beyond the JSON schemas. The facet tables above come from the JSON files in `spec/facets/`.
