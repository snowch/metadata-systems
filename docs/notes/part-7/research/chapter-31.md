# Sources for Chapter 31 (research)

A research note, gathered on 13 October 2026 from each project's own repository. Facts the chapter states are re-checked and recorded in `docs/sources.md` before they land.

SOURCES FOR CHAPTER 31

Method: shallow, sparse git clones of each project's own repository (read-only, via the proxy), then reading the files. I did not use the GitHub API (it is blocked in this session), a mirror, a blog or a vendor site. Every path is relative to the repository root.

Commits read:
- DataHub: datahub-project/datahub, branch master, commit 2f2dcd4a0a91c2e356605adc8fb9a5291eeb0c6f (12 Oct 2026).
- OpenMetadata: open-metadata/OpenMetadata, branch main, commit 18294ee884c9b10d04071c9bebdc1d00a746157a (12 Oct 2026).
- Atlas: apache/atlas, branch master, commit ec7dc21d49f5d2f07258c4205c948a65194a0aad (7 Oct 2026).
- Marquez: MarquezProject/marquez, branch main, commit 180f37b22387146187af1ef0279e3ee1d1ccd789 (12 Apr 2026).

Quotations are marked and are 15 words or fewer. Line numbers refer to those commits. Everything else is in my own words.

====================================================================
1. DATAHUB (datahub-project/datahub, master)
====================================================================

HOW METADATA ARRIVES: both pull and push.

1.1 DataHub's own architecture page says its ingestion supports push, pull, asynchronous and synchronous models.
- Source: docs/architecture/metadata-ingestion.md, line 7.
- Quote: "can support push, pull, asynchronous and synchronous models."

1.2 The central unit of ingestion is the Metadata Change Proposal (MCP), a request to change one aspect. An MCP can go over Kafka (asynchronous) or straight to an HTTP endpoint on the service tier (synchronous success or failure).
- Source: docs/architecture/metadata-ingestion.md, lines 14-17. Also docs/what/mxe.md, lines 14-26.
- The default Kafka topic for MCPs is MetadataChangeProposal_v1 (docs/what/mxe.md, line 26).
- MCP fields: entityUrn, entityType, changeType, aspectName, aspect (JSON-serialised value) and systemMetadata (docs/what/mxe.md, lines 35-44).
- Change types: "CREATE, UPSERT and DELETE are currently supported. PATCH has limited support" (mxe.md, line 40; the same sentence also sits in the schema table).

1.3 Pull: a Python ingestion system connects to a source and pulls metadata. The source is then pushed to DataHub's storage tier via Kafka or HTTP. Pipelines can be integrated with Airflow for scheduled ingestion.
- Source: docs/architecture/metadata-ingestion.md, lines 19-21.
- The current README of the ingestion framework is metadata-ingestion/README.md (fetched from raw.githubusercontent.com, master). Lines 5-16 say pull-based integrations "crawl your data systems on a schedule" and push-based integrations emit metadata from code (Python SDK, Java SDK, Spark and others). Line 52 shows the pull command `datahub ingest -c snowflake_recipe.yml`, where the recipe is a YAML file.
- Scheduling in the UI: docs/ui-ingestion.md, lines 185-193 (a "Sync Schedule" step, with scheduling optional). A cron schedule from the CLI is at line 320: `datahub ingest deploy ... --schedule "5 * * * *"`.

1.4 Push: any system that can emit an MCP to Kafka or call REST over HTTP can integrate. Python emitters are provided.
- Source: docs/architecture/metadata-ingestion.md, lines 23-25.

1.5 Consumption: a Spring job, mce-consumer-job, reads MCPs from Kafka and writes them to the metadata service (GMS) via its /ingest endpoint.
- Source: docs/architecture/metadata-ingestion.md, lines 29-31.

MODELLING

1.6 The model is schema-first. It is written in Pegasus PDL (LinkedIn's rest.li schema language) extended with custom annotations. The storage, serving, indexing and ingestion layers all work on top of it.
- Source: docs/modeling/metadata-model.md, line 10.
- Quote: "takes a schema-first approach to modeling metadata."

1.7 Entities are the primary node and are identified by a URN. Aspects are groups of attributes attached to an entity. They are "the smallest atomic unit of write", so different aspects of one entity can be updated independently. Aspects can be shared across entity types, and "Ownership" is the example given. Relationships are named edges declared in aspects with a @Relationship annotation, and can be walked both ways.
- Source: docs/modeling/metadata-model.md, lines 12-25.
- Aspects are immutable, so each change makes a new version; optional retention applies (docs/what/aspect.md, lines 3-11).

1.8 Entities and their aspects are tied together in a YAML entity registry.
- Source: docs/modeling/metadata-model.md, lines 48-67. The file is metadata-models/src/main/resources/entity-registry.yml. The `dataset` entity starts at line 15 and its aspect list includes `ownership` at line 46.
- Snapshot models are deprecated as a way to add entities, "as of January 2022" (same doc, line 63).

STORAGE AND INDEXING

1.9 Primary storage is a document store: an RDBMS such as MySQL, Postgres or Cassandra. Primary-key reads go there. Secondary-index and full-text queries go to the search index. Graph queries such as lineage go to the graph index.
- Source: docs/architecture/metadata-serving.md, lines 17-19 and 36-38. docs/components.md, lines 13-18 says "MySQL, Elasticsearch, & Kafka for primary storage & indexing."

1.10 After a commit, the service emits a Metadata Change Log (MCL) event on Kafka. A second Spring job, mae-consumer-job, applies MCLs to the graph and search indexes. MCLs are keyed by entity URN so that changes to one entity are processed in order.
- Source: docs/architecture/metadata-serving.md, lines 21-34.
- Duplicate changes are ignored, so not every MCP produces an MCL (same doc, line 26). This is a documented DataHub behaviour, not an OpenLineage one.

1.11 The quickstart deployment uses MySQL 8.2, OpenSearch 2.19.3 and Kafka (Confluent cp-kafka image). The graph is stored in the search engine.
- Source: docker/quickstart/docker-compose.quickstart-profile.yml. mysql image at line 341 (`mysql:8.2`), opensearch image at line 398 (`opensearchproject/opensearch:2.19.3`), `GRAPH_SERVICE_IMPL: elasticsearch` at line 90.
- The default graph implementation is the search engine: metadata-service/configuration/src/main/resources/application.yaml, lines 434-435, `graphService: type: ${GRAPH_SERVICE_IMPL:elasticsearch}`. Neo4j is an alternative (docker/profiles/docker-compose.gms.yml, lines 28-31).

1.12 SOURCES DISAGREE: docs/what/graph.md, line 3, says "stored in a graph database, Neo4j." That is an old GMA-era page. The current code default and the quickstart use the search engine (1.11). Cite application.yaml and the compose file, not graph.md.

OWNERSHIP

1.13 Ownership is an aspect named "ownership". The `owners` field is a list of Owner records. There is also `ownerTypes` (a map from ownership-type to owner URNs, filled by a mutation hook) and `lastModified` (an audit stamp).
- Source: metadata-models/src/main/pegasus/com/linkedin/common/Ownership.pdl, lines 6-30. Quote: "List of owners of the entity."

1.14 An Owner record has these fields:
- `owner: Urn`, with `@Relationship` name "OwnedBy" and entityTypes [corpuser, corpGroup]. The field comment says "only corpuser is currently supported in the frontend."
- `type: OwnershipType`, which is deprecated.
- `typeUrn: optional Urn`, with relationship "ownershipType" pointing to an `ownershipType` entity.
- `source: optional OwnershipSource`.
- `attribution: optional MetadataAttribution`, which records who, why and how.
- Source: metadata-models/src/main/pegasus/com/linkedin/common/Owner.pdl. The Urn is at line 25, `type` at line 31, `typeUrn` at line 41, `source` at line 46, and the relationship annotation at lines 12-15.

1.15 An owner is therefore a reference to a user or group entity, and the kind of ownership is separate. The enum OwnershipType has these values:
- CUSTOM (set when a type has no enum value).
- TECHNICAL_OWNER: "person or group who is responsible for technical aspects of the asset."
- BUSINESS_OWNER: "responsible for logical, or business related, aspects of the asset."
- DATA_STEWARD: a steward, expert or delegate responsible for the asset.
- NONE.
- Deprecated values: DEVELOPER, DATAOWNER, DELEGATE, PRODUCER, CONSUMER, STAKEHOLDER.
- Source: metadata-models/src/main/pegasus/com/linkedin/common/OwnershipType.pdl, lines 12-32 for the live values.
- The deprecated DATAOWNER is still the type used in the MCP example at docs/what/mxe.md, around lines 51-60.

1.16 Custom ownership types are a separate `ownershipType` entity, so an organisation can use its own terms. The built-in system ones are listed with descriptions in metadata-service/configuration/src/main/resources/bootstrap_mcps/ownership-types.yaml. Examples:
- Technical Owner: "Involved in the production, maintenance, or distribution of the asset(s)."
- Business Owner: principal stakeholders or domain experts.
- Data Steward: "Involved in governance of the asset(s)."
- None.
- Source also: docs/ownership/ownership-types.md, lines 15-32.

1.17 OwnershipSource.type values: AUDIT, DATABASE ("e.g. GRANTS table"), FILE_SYSTEM, ISSUE_TRACKING_SYSTEM, MANUAL, SERVICE, SOURCE_CONTROL, OTHER. The record also has an optional `url`.
- Source: metadata-models/src/main/pegasus/com/linkedin/common/OwnershipSource.pdl.

Not found for DataHub: no document states a single meaning of "owner" beyond the enum and bootstrap-type descriptions above. That is useful for the chapter: the platform's own text splits "technical" from "business" from "steward".

====================================================================
2. OPENMETADATA (open-metadata/OpenMetadata, main)
====================================================================

I did not consult docs.open-metadata.org. The user docs live outside this repository and a fetch returned a redirect. All of the following is from the main repository.

HOW METADATA ARRIVES: both, through one REST API.

2.1 The repository's own ARCHITECTURE.md says there is one Java backend (Dropwizard) in front of a MySQL/Postgres catalog and an Elasticsearch/OpenSearch index. A Python ingestion framework feeds the catalog "through the same REST API".
- Source: ARCHITECTURE.md, lines 14-20. Quote: "feeds the catalog *through the same REST API*".

2.2 Pull path (ARCHITECTURE.md "Path B", lines 30-37):
- An ingestion run starts in the Python tree `ingestion/`, triggered by Airflow or the `metadata` CLI.
- A connector's Source class yields entities.
- A sink (`ingestion/.../sink/metadata_rest.py`) POSTs them to the backend REST API.
- Quote: "**POSTs them to the backend REST API**".
- The tree has 120+ connectors, and about 97 carry a `service_spec.py` plugin contract (ARCHITECTURE.md, line 68 and invariant I2, lines 116-125).

2.3 The ingestion pipeline entity has a cron schedule field: `airflowConfig.scheduleInterval` ("Scheduler Interval for the pipeline in cron format.").
- Source: openmetadata-spec/src/main/resources/json/schema/entity/services/ingestionPipelines/ingestionPipeline.json, lines 62 and 105-107.

2.4 Push: any client can call the same REST API directly. Path A in ARCHITECTURE.md (lines 22-28) uses `POST /v1/tables`. A non-GET request also fans out to change events and a search-index update.

MODELLING

2.5 Everything is typed by JSON Schema. The repository says there are 904 JSON Schemas in `openmetadata-spec`, from which Java, Python and TypeScript models are generated (jsonschema2pojo, datamodel-code-generator, quicktype). The direction is schema to code.
- Source: ARCHITECTURE.md, lines 16-18 and invariant I4, lines 138-147.
- The count (904) is as of this commit and rots. Do not print it in the chapter without a test.

2.6 Relations between entities use a shared EntityReference type: id, type, name, fullyQualifiedName, description, displayName, deleted, inherited, href. Only `id` and `type` are required. The `inherited` flag is described as "the relationship ... is inherited from the parent entity."
- Source: openmetadata-spec/src/main/resources/json/schema/type/entityReference.json, lines 8-46 (required at line 46).
- openmetadata-spec/.../type/entityReferenceList.json is an array of entityReference.

STORAGE AND INDEXING

2.7 The catalog is stored in MySQL or Postgres through JDBI DAOs (CollectionDAO, EntityDAO). The default driver is MySQL.
- Source: ARCHITECTURE.md, lines 22-27. conf/openmetadata.yaml, lines 335-337 (`driverClass: ${DB_DRIVER_CLASS:-com.mysql.cj.jdbc.Driver}`).

2.8 Search is Elasticsearch or OpenSearch, chosen by `searchType`, with default "elasticsearch".
- Source: conf/openmetadata.yaml, lines 626-627.
- Indexes are rebuilt on entity writes by `service/search/indexes/*Index.java`, or by a reindex app (ARCHITECTURE.md, lines 39-44).

2.9 The docker-compose deployment image tag is `docker.getcollate.io/openmetadata/server:2.0.0-SNAPSHOT`.
- Source: docker/docker-compose-openmetadata/docker-compose-openmetadata.yml, lines 17 and 244. Do not use this as a claim about a version.

OWNERSHIP

2.10 The field is `owners`, a list of entity references. For a table:
- On the entity, "Owners of this table." with `$ref ../../type/entityReferenceList.json` (openmetadata-spec/.../json/schema/entity/data/table.json, line 1140). A second `owners` property, "Owners of this Table.", sits at line 1008.
- On the create request, "Owners of this entity" (openmetadata-spec/.../api/data/createTable.json, line 62).

2.11 Code accepts only a user or a team of type Group as an owner. In `EntityRepository.validateOwners`:
- A null owner type is rejected ("Owner type must be specified ...").
- An owner of type team must be a team whose `teamType` is GROUP, otherwise `invalidTeamOwner` is thrown.
- Any other owner type that is not USER is rejected with `invalidOwnerType`.
- Source: openmetadata-service/src/main/java/org/openmetadata/service/jdbi3/EntityRepository.java, lines 9153-9178.
- Team types are Group, Department, Division, BusinessUnit and Organization. Default is Group. The schema says "A Group has only Users" (openmetadata-spec/.../entity/teams/team.json, lines 14-25).
- So OpenMetadata's owner is a person or a group of people, never a service account or a job. This is a code behaviour, not something the schema says.

2.12 Owners are stored as relationships, not as a column. They are read back with `findFrom(entity.getId(), entityType, Relationship.OWNS, ...)`.
- Source: EntityRepository.java, lines 8456-8457; `storeOwners` is at line 8826.

2.13 OpenMetadata's `owners` carries no type of ownership. It has no technical, business or steward distinction in the field. The `inherited` flag on the reference is the only qualifier. I found no ownership-type enum in the schema I read. I did not search other entity types (domains, data products) for owner-like fields.

====================================================================
3. APACHE ATLAS (apache/atlas, master)
====================================================================

HOW METADATA ARRIVES: push, by hooks and Kafka, plus REST.

3.1 Atlas has two integration routes. REST ("All functionality of Atlas is exposed ... via a REST API"). Messaging, based on Kafka, "particularly useful if one wishes to use a more loosely coupled integration".
- Source: docs/src/documents/HighLevelArchitecture.md, lines 42-53.
- Hooks write to Kafka topics.

3.2 Notifications to Atlas go on the Kafka topic ATLAS_HOOK. The hooks for Hive, HBase, Storm and Sqoop use it. Operations include ENTITY_CREATE, ENTITY_FULL_UPDATE, ENTITY_PARTIAL_UPDATE, ENTITY_DELETE and V2 variants. Notifications from Atlas go on ATLAS_ENTITIES: ENTITY_CREATE, ENTITY_UPDATE, ENTITY_DELETE, CLASSIFICATION_ADD, CLASSIFICATION_UPDATE and CLASSIFICATION_DELETE.
- Source: docs/src/documents/Notifications.md, lines 15-29 and 70-80.
- Quote: "Apache Atlas sends notifications about metadata changes to Kafka topic named ATLAS_ENTITIES".

3.3 The Hive hook runs inside Hive and listens to create, update and delete operations. It updates Atlas "via Kafka notifications". It is asynchronous by default (`atlas.hook.hive.synchronous=false`).
- Source: docs/src/documents/Hook/HookHive.md, line 62 (hook), line 83 (synchronous default).
- Batch: a command-line utility, import-hive.sh, imports existing Hive databases and tables to initialise Atlas (same file, lines 143-145). Atlas does not run it on a schedule. This is the nearest thing to pull. I did not find a scheduled connector framework like DataHub's or OpenMetadata's.

MODELLING

3.4 The model is a type system. Types are like classes or table schemas. Metatypes are primitives, enums, collections (array, map) and composites (Entity, Struct, Classification, Relationship). Entity and Classification types can have supertypes (including more than one). Instances of entity types are "entities" and have a GUID the server generates.
- Source: docs/src/documents/TypeSystem.md, lines 16-23, 53-63, 106-108.
- Entities have identity. Structs are embedded inside the entity and have none (line 113).

3.5 Attribute properties documented include name, typeName, isOptional, isIndexable, isUnique and cardinality (TypeSystem.md, lines 120-140).

3.6 Classifications can be created dynamically, can carry attributes, and can propagate via lineage. Examples are PII and EXPIRES_ON.
- Source: docs/src/documents/Overview.md, "Classification" section (read at lines 20-30).

3.7 Predefined types: `Referenceable` (unique `qualifiedName`), `Asset` (extends Referenceable, adds name, displayName, description, userDescription and owner), `DataSet`, `Infrastructure`, `Process` (inputs and outputs, both `array<DataSet>`).
- Source: addons/models/0000-Area0/0010-base_model.json. Asset's attribute definitions are the block that ends at line 58.
- docs/src/documents/TypeSystem.md, lines 184-200 describe them.

3.8 SOURCES DISAGREE (minor): TypeSystem.md says of DataSet "This type extends Referenceable". The model file addons/models/0000-Area0/0010-base_model.json defines DataSet with `"superTypes": ["Asset"]`. Cite the JSON as the actual model, and do not say DataSet "has no owner".

STORAGE AND INDEXING

3.9 Atlas persists metadata as a graph via JanusGraph. The "graph engine" also creates indexes for search.
- Source: docs/src/documents/HighLevelArchitecture.md, lines 31-35.
- Quote: "Atlas uses the JanusGraph to store the metadata objects."

3.10 Storage backend shown in the configuration docs is HBase (`atlas.graph.storage.backend=hbase`). A separate index search engine is required: Solr (cloud mode) or Elasticsearch (labelled "Tech Preview"). The doc says "Only two search engines are currently supported."
- Source: docs/src/documents/Setup/Configuration.md, lines 18-24, 32-36, 53-59.
- That page documents only HBase as a storage backend. I did not check whether other JanusGraph backends such as Cassandra are supported in the shipped configuration.

3.11 Kafka is the notification server (HighLevelArchitecture.md, lines 51-53; Configuration.md, lines 74-94).

OWNERSHIP

3.12 `owner` is an attribute of the `Asset` supertype. Its type is `string`, cardinality SINGLE, `isOptional: true`, `isIndexable: true`, `indexType: STRING`. It is one free-text string. It is not a reference to a user, group or team entity.
- Source: addons/models/0000-Area0/0010-base_model.json, the Asset definition, lines about 47-58.
- Quote from docs/src/documents/TypeSystem.md, line 186: "adds attributes like name, description and owner."
- The same doc says that for Asset, "Name is a required attribute (isOptional=false), the others are optional." So Atlas does not require an owner.

3.13 What fills the string is whatever the source system says. In the Hive hook code:
- The table's owner is set as `table.getOwner()` (addons/hive-bridge/src/main/java/org/apache/atlas/hive/hook/events/BaseHiveEvent.java, line 408).
- A database's owner is `db.getOwnerName()` (line 324).
- The bridge does the same (addons/hive-bridge/src/main/java/org/apache/atlas/hive/bridge/HiveMetaStoreBridge.java, lines 676 and 727).
- Columns copy the table's owner (BaseHiveEvent.java, line 555; HiveMetaStoreBridge.java, line 835).
- So, for Hive assets, Atlas's owner is the Hive metastore's owner, which is a Hive principal.

3.14 `hive_db` adds `ownerType` of enum `hive_principal_type`, with values USER, ROLE and GROUP.
- Source: addons/models/1000-Hadoop/1030-hive_model.json, lines 92-101 (ownerType at line 100). The enum appears in the Hive docs: docs/src/documents/Hook/HookHive.md, lines 37-40.
- Hive docs list `ownerName` for `hive_db` (HookHive.md, line 21). I saw no `ownerName` attribute in the type definition lines I read.

3.15 I found no Atlas document that defines "owner" beyond the string attribute. The Hive code shows it mirrors the source system.

====================================================================
4. MARQUEZ (MarquezProject/marquez, main)
====================================================================

HOW METADATA ARRIVES: push only.

4.1 Marquez collects dataset, job and run metadata through its HTTP API using OpenLineage events. `POST /lineage` is the OpenLineage endpoint ("Record a single lineage event").
- Source: spec/openapi.yml, lines 575-588 (`recordLineage`).
- docs/docs/quickstart/index.mdx, line 85: "Run-level metadata is tracked via HTTP API calls to `/lineage` using [OpenLineage]".
- Marquez has no connector or crawler that pulls from sources. The deployment docs name a user-provided scheduler (for example Airflow) and "workflow using an OpenLineage integration to send lineage metadata to Marquez."
- Source for that: docs/docs/deployment/deployment.mdx, lines 30-36.

4.2 Other API calls create or change entities directly. Examples are PUT namespace, PUT source, PUT dataset, run start, complete, fail and abort, and tags.
- Source: spec/openapi.yml, paths at lines 16-424 (namespaces, sources, datasets, jobs, runs, tags).

MODELLING

4.3 The model is a normalised relational model of namespaces, sources, datasets, jobs and runs, with built-in versioning.
- Source: docs/docs/quickstart/index.mdx, lines 67-85. Quote: "built-in metadata versioning support."
- A run has a unique ID and records its code version, inputs and outputs, run arguments and run state transitions.
- A dataset version pointer is kept for each input and output dataset. Dataset versions are immutable.
- A job version points to a link to code, the latest run ID, and versioned input and output datasets.
- The tables themselves are in api/src/main/resources/marquez/db/migration/V1__initial_schema.sql: `namespaces`, `owners`, `namespace_ownerships`, `sources`, `datasets`, `jobs` and so on (lines 3-60). `sources` has `type`, `name` and `connection_url`.

STORAGE AND INDEXING

4.4 Primary storage is PostgreSQL only.
- Source: docs/docs/deployment/deployment.mdx, line 12.
- Quote: "relies only on PostgreSQL to store dataset, job, and run metadata".

4.5 Search is optional OpenSearch.
- Source: marquez.example.yml, lines 69-75 (a `search:` block with `enabled`, `host: marquez-opensearch`, port 9200). docker-compose.search.yml (lines 9-12) runs `opensearchproject/opensearch:2.5.0`.
- I did not verify that the default configuration leaves search off. Only that the example config enables it, so call it "optional" only after you check the config default.

4.6 The API server and web UI are Docker images. The Helm chart is maintained in the repository (docs/docs/deployment/deployment.mdx, lines 4-8, 30-36).

OWNERSHIP

4.7 Marquez records an owner only on the namespace. In the Java models, only `Namespace.java` and `NamespaceMeta.java` have an owner field: `@NonNull OwnerName ownerName;` (api/src/main/java/marquez/service/models/NamespaceMeta.java, line 16). Dataset, DatasetMeta, Job, JobMeta, Run and SourceMeta have none (I grepped for "owner" across api/src/main/java/marquez/service/models/ and got only the two namespace files).

4.8 The OpenAPI spec agrees. The namespace has `ownerName`: "The owner of the namespace." It is a string, and in the create schema it is required. No `ownerName` appears on datasets, jobs or sources.
- Source: spec/openapi.yml, lines 939-946 and 965-975 (`ownerName: me` in the example).

4.9 What a valid owner name is: any non-blank string. `OwnerName` checks only `checkNotBlank(value, "value must not be blank")`.
- Source: api/src/main/java/marquez/common/models/OwnerName.java, in the constructor.

4.10 Ownership has history. A namespace row keeps `current_owner_name VARCHAR(64)`. Table `owners` holds names. Table `namespace_ownerships` has `started_at`, `ended_at`, `namespace_uuid` and `owner_uuid`. When a namespace's owner changes, the old ownership is ended and a new one started.
- Source: V1__initial_schema.sql, lines 3-25. api/src/main/java/marquez/db/NamespaceDao.java, lines 40-56.
- Migration V63 (api/src/main/resources/marquez/db/migration/V63__alter_tables_add_on_cascade_delete.sql, lines 190-201) still alters the `namespace_ownerships` foreign keys, so the tables existed as of V63. I did not check that nothing later drops them.

4.11 When a namespace is created implicitly from an OpenLineage event, its owner is the constant "anonymous".
- Source: api/src/main/java/marquez/db/OpenLineageDao.java, line 82: `String DEFAULT_NAMESPACE_OWNER = "anonymous";` and its uses at lines 192, 224, 299, 842, 871 and 899.
- So a platform that fills itself from OpenLineage has an owner field filled with "anonymous". This is a Marquez behaviour, not an OpenLineage one.
- Also, Marquez has no owner for a dataset or a job. The only owner-like thing is the namespace's, so a requirement "track ownership" is met only for the namespace.

====================================================================
CROSS-PLATFORM SUMMARY FOR THE OWNERSHIP REQUIREMENT
====================================================================

- DataHub: the owner is a reference to a user or group entity (`corpuser` or `corpGroup`) with a separate ownership type (technical owner, business owner, data steward, none, or a custom type). It can also carry a source and attribution.
- OpenMetadata: `owners` is a list of references to a user or to a team whose type is Group. There is no ownership-type field in the schema I read.
- Atlas: `owner` is one optional free string on `Asset`. For Hive assets it is copied from Hive's own owner, and for databases it also comes with a user, role or group tag (`ownerType`).
- Marquez: only a namespace has an owner, a required non-blank string, defaulting to "anonymous" for OpenLineage-created namespaces. Datasets and jobs have none.

Things I did not do or could not confirm: I did not read docs.open-metadata.org, so nothing here comes from OpenMetadata's user documentation. I did not check Atlas storage backends other than HBase. I did not verify that Marquez's search is off by default, or that the ownership tables survive all later migrations. DataHub's docs/what/graph.md (Neo4j) conflicts with current configuration; cite application.yaml.
