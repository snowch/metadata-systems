# Source research for Chapter 32 (to be checked before use)

SOURCES FOR CHAPTER 32

How these were gathered: raw files from each project's own repository, fetched with curl on 2026-10-13, plus `git ls-remote` for the commit at each branch tip. Raw files came from the default-branch tip, and the ls-remote shas were taken minutes after, so they could differ by a commit. The OpenLineage sha is exact (shallow clone). The GitHub API was blocked ("not enabled for this session"), so I did not use it, and I could not list MLflow's directory tree. Nothing was written to the project. Short quotations are marked.

Branch tips seen:
- mlflow/mlflow `master`: 9d651c2f19738560f38652b3e6a5f0d51ae92711
- iterative/dvc `main`: 56e59829512ff134aa269099a2099587b810b4dd
- iterative/dvc.org `main`: 21fabba8d66bf81e3cfcbcb9e061d4a5363399ad
- OpenLineage/OpenLineage: 60261f0b57fb1370c2c6c3cadc9f1721b6c3c3b5 (commit date 2026-10-12)
- langchain-ai/langchain `master`: f2bf626ccee0a0e88d560706d4fdad35e43116e5
- run-llama/llama_index `main`: 5b7b6e323e1da3edd787a2104a89257c14f026d0

------------------------------------------------------------
1. MLFLOW (mlflow/mlflow, branch master)

1.1 A run holds four things: info, data, inputs and outputs.
- Source: `mlflow/entities/run.py`, class `Run`, lines 19-31 and 33-60.
- Its docstring says the data includes "metrics, parameters, and tags" (the docstring of `Run.data`, line 45).
- `Run.inputs` is a `RunInputs`; the docstring says "including dataset inputs".

1.2 `RunData` has exactly three collections: metrics, params and tags.
- Source: `mlflow/entities/run_data.py`, lines 14-57.
- Params are string key to string value. Metrics are key to float. Tags are key to string.
- The metrics property returns, per key, the value with the latest timestamp (lines 41-47).

1.3 `RunInfo` carries run_id, experiment_id, user_id, status, start_time, end_time and artifact_uri.
- Source: `mlflow/entities/run_info.py`, property definitions at lines 89, 94, 107, 112, 120, 125 and 130.
- Artifacts are files logged with `mlflow.log_artifact`, written under the run's artifact location. See `mlflow/tracking/fluent.py`, `def log_artifact` at line 1637; its docstring says "Log a local file or directory as an artifact of the currently active run."
- An artifact is a file stored beside the run. It is not a field of the `Run` entity (`run.py` has no artifacts attribute).

1.4 Some tags MLflow reserves by key name:
- Source: `mlflow/utils/mlflow_tags.py`, lines 11-23.
- `mlflow.runName`, `mlflow.parentRunId`, `mlflow.user`, `mlflow.source.name` and `mlflow.source.git.commit`.
- So the code commit is a convention carried in a tag, not a dedicated field.

1.5 The dataset entity has six fields: name, digest, source_type, source, schema, profile.
- Source: `mlflow/entities/dataset.py`, constructor lines 10-18; `to_dictionary` lines 84-92.
- `schema` and `profile` are optional (`str | None`) and are strings in the entity.

1.6 The user-facing `Dataset` class describes itself as a name, a digest, a schema and a profile, plus source information.
- Source: `mlflow/data/dataset.py`, class docstring lines 10-15.
- Quotation (line 11-12): "including the name, digest (hash), schema, and profile of the dataset".
- The source is described as the place the data was derived from, "e.g. the S3 bucket or managed Delta table".
- `digest` is documented as "A unique hash or fingerprint of the dataset" (lines 80-85).
- The name defaults to the literal string "dataset" when none is given (lines 70-78).
- `profile` and `schema` are abstract and described as optional (lines 97-111).

1.7 The source is a pointer, not a copy of the data.
- Source: `mlflow/data/dataset_source.py`, lines 6-33.
- `DatasetSource` represents "cloud storage location, delta table name / version, etc." Its `load()` method "downloads source CSV files from S3 ... loads a source Delta Table" (paraphrased from lines 25-28).
- So `load()` fetches whatever the source points at now. The source record does not itself freeze the content.
- Inference, not a documented guarantee: the entity holds the source as a string (`source: str`) next to the digest. The digest is the only content check.

1.8 What the pandas dataset records as profile and schema.
- Source: `mlflow/data/pandas_dataset.py`.
- Profile (lines 115-122) is only `{"num_rows": ..., "num_elements": ...}`.
- Schema (lines 125-133) is inferred from the DataFrame via `_infer_schema`, and is `None` if inference fails.
- Digest is computed by `compute_pandas_digest(self._df)` (lines 65-71).

1.9 How `digest` is computed for a pandas DataFrame.
- Source: `mlflow/data/digest_utils.py`, `compute_pandas_digest` lines 12-43; `get_normalized_md5_digest` lines 87-107; constant `MAX_ROWS = 10000` at line 9.
- Only the first 10,000 rows are hashed (line 25, `df.head(MAX_ROWS)`).
- Only columns whose values are all `str`, plus numeric columns, are kept. Other column types are dropped (comment at line 27; lines 28-35).
- It hashes the row hashes from `pd.util.hash_pandas_object`, then the full row count `np.int64(len(df))`, then each column name (lines 37-43).
- The result is an md5, with `usedforsecurity=False` (line 103), truncated to 8 hex characters (line 107).
- Quotation (docstring line 94): "An 8-character, truncated md5 digest."
- Consequences to teach, each following from the code above:
  - A change after row 10,000 that keeps the row count the same does not change the digest.
  - A change in a dropped column type (for example a datetime or list column) does not change it.
  - The digest is of the data as loaded in memory, not of the query or the file.
- The numpy digest (lines 46-84) uses the same first-10,000-elements rule and adds array shapes.
- The base class `Dataset._compute_digest` docstring (`mlflow/data/dataset.py` lines 28-36) recommends a digest of at most 10 characters, ideally 8. A caller may pass their own digest to the constructor (line 25: `digest or self._compute_digest()`).

1.10 Linking a dataset to a run, with a context.
- Source: `mlflow/tracking/fluent.py`, `def log_input`, lines 1456-1491.
- The `context` argument is documented: "Context in which the dataset is used. For example: "training", "testing". This will be set as an input tag with key `mlflow.data.context`."
- The example in the docstring uses `context="training"`.
- The context is a free string. The code gives "training" and "testing" only as examples (the docstring's wording is "For example").
- The tag key constant is `MLFLOW_DATASET_CONTEXT = "mlflow.data.context"`, in `mlflow/utils/mlflow_tags.py` line 88, under the comment "For MLflow Dataset tracking".

1.11 The run-to-dataset link carries tags, and the context is one of them.
- Source: `mlflow/entities/dataset_input.py`, lines 9-30.
- `DatasetInput` is a `Dataset` plus a list of `InputTag`s (key and value strings; `mlflow/entities/input_tag.py`).
- `RunInputs` holds `dataset_inputs` and `model_inputs` (`mlflow/entities/run_inputs.py`, lines 12-33).
- So one run can have several datasets, each with its own context.
- Model inputs are also recorded separately from dataset inputs (`LoggedModelInput`).

1.12 Evaluation can log the dataset, and the context is set only conditionally.
- Source: `mlflow/models/evaluation/base.py`, around lines 1760-1780 of the file as fetched.
- `context` is taken from a built-in evaluator's `metric_prefix` config, if there is one; otherwise `context = None`.
- Then `tags = [InputTag(key=MLFLOW_DATASET_CONTEXT, value=context)] if context else []`.
- So an evaluation dataset may be logged with no context tag at all.
- That call also passes `models=[LoggedModelInput(model_id)]` when a model id exists, so an evaluation run can record both the dataset and the model it scored.

1.13 A registered model version records a run id and a source string.
- Source: `mlflow/entities/model_registry/model_version.py`, constructor lines 20-43; properties:
  - `source`, lines 118-121: "String. Source path for the model."
  - `run_id`, lines 123-126: "String. MLflow run ID that generated this model."
  - `run_link`, lines 128-131: "MLflow run link referring to the exact run that generated this model version."
- It also has user_id, status, tags, aliases, `model_id`, and optional `params` and `metrics` lists (lines 38-40).
- `run_id` and `source` are both optional (`str | None`).
- `current_stage` is a field (line 110), and the entity also has `aliases`.

1.14 How `run_id` and `source` get filled when a run's model is registered.
- Source: `mlflow/tracking/_model_registry/fluent.py`, `_register_model`, lines 166-260.
- If the model URI is `runs:/<run_id>/<path>`, `run_id` is parsed from it (line 196).
- If the run has an MLmodel file at that path, `source` becomes the run's underlying artifact URI (line 201: `source = RunsArtifactRepository.get_underlying_uri(model_uri)`).
- Otherwise it looks for a logged model and sets `source = f"models:/{model_id}"`.
- If the URI is not a `runs:/` URI (for example `s3://...`), `run_id` stays `None` and `source` is the URI as given (lines 190-192).
- The client's `create_model_version` docstring (`mlflow/tracking/client.py`, from line 4664) says `source` is "indicating the location of the model artifacts" and `run_id` is the "Run ID from MLflow tracking server that generated the model."
- Consequence: the registry's link to training data is indirect. A version points to a run (when it has one), the run points to dataset inputs, and the dataset entity holds a name, a digest and a source pointer.

1.15 Limits, as far as I could check:
- I found no field anywhere in these files that records the query that selected the data, or features computed from it. The `Dataset` entity has only the six fields in 1.5.
- I did not fetch MLflow's prose documentation. The path `docs/docs/ml/dataset/index.mdx` returned 404, so everything above is from code and docstrings. MLflow's directory tree was not listed.

------------------------------------------------------------
2. OPENLINEAGE (OpenLineage/OpenLineage, shallow sparse clone at 60261f0b..., dirs `spec`, `proposals`, `integration`)

2.1 No ML facet exists in `spec/facets/`.
- I listed all 39 files there. They are:
  - Dataset facets: BaseSubset, Catalog, ColumnLineage, DataQualityAssertions, DataQualityMetrics, DataQualityMetricsInput, DatasetType, DatasetVersion, Datasource, Documentation, Hierarchy, InputStatistics, LifecycleStateChange, OutputStatistics, Ownership, Schema, Storage, Symlinks, Tags.
  - Job facets: DocumentationJob, JobType, OwnershipJob, SQLJob, SourceCode, SourceCodeLocation, TagsJob.
  - Run facets: EnvironmentVariables, ErrorMessage, ExecutionParameters, ExternalQuery, ExtractionError, JobDependencies, NominalTime, ParentRun, ProcessingEngine, TagsRun, Test.
  - Also LineageFacet.
- A case-insensitive search across `spec`, for `ml`, `training`, `embedding`, `mlflow`, `machine learning` and `"model"`, returned no matches. The `proposals` directory contains no mention of mlflow, machine learning or embedding. The `integration` directory has no mlflow or machine learning integration (subfolders: common, dbt, flink, hive, spark and similar). The `integration` search was recursive but not exhaustive of every non-text file.
- `spec/registry/core/registry.json` has no ML entry either (37 lines; no `ml` token).
- The only "model" hit is a job-type string (2.3 below). It is dbt's use of the word, not ML.

2.2 Closest existing facets, usable by analogy only (the spec does not describe them as ML):
- `ExecutionParametersRunFacet.json` (parameters passed to a job at runtime). The description at line 41 reads "The parameters passed to the Job at runtime".
- `DatasetVersionDatasetFacet.json`: one property `datasetVersion`, type string, description "The version of the dataset." The file's `$id` is `.../facets/1-0-1/DatasetVersionDatasetFacet.json`. The facet defines no meaning for the version string.
- `SourceCodeLocationJobFacet.json`, `SQLJobFacet.json`, `SchemaDatasetFacet.json`, `ColumnLineageDatasetFacet.json`.
- `ParentRunFacet.json`: link a run to a parent run.
- Custom facets are allowed by the base spec, so an ML facet could be written as a custom one. I did not verify that sentence against `OpenLineage.md` in this pass; check it before citing.

2.3 `JobTypeJobFacet.json` (line 24) lists "MODEL" among example job types.
- Quotation: "Run type, for example: QUERY|COMMAND|DAG|TASK|JOB|MODEL. This is an integration-specific field."
- The only implementation that sets it is the dbt integration. `integration/common/src/openlineage/common/provider/dbt/processor.py` line 351 sets `jobType = "MODEL"`, and `.../dbt/utils.py` line 236 returns "MODEL".
- The spec does not say it means a machine-learning model. Do not cite it as ML support.

2.4 W3C PROV: I did not fetch the PROV specification in this pass, so I make no claim about its view of ML.

------------------------------------------------------------
3. CONTENT HASHES IN DVC (iterative/dvc and iterative/dvc.org, branch main)

3.1 A `.dvc` file is a placeholder holding, per output, a hash and a path.
- Source: `iterative/dvc.org`, `content/docs/user-guide/project-structure/dvc-files.md`, lines 8-20.
- Quotation (line 11): "They contain the information needed to track the target data over time."
- Example (lines 15-17): `outs:` then `- md5: a304afb96060aad90176268345e10355` and `path: data.xml`.

3.2 Output entry fields, from the same page (table at lines 45-54):
- `path`: required, relative to `wdir`.
- `hash`: the algorithm; the page says "only `md5` is currently supported" (line 50).
- `md5`, `etag` or `checksum`: the hash value. MD5 is used for the local file system and SSH. ETag is used for HTTP, S3 or Azure external outputs. A special checksum is used for HDFS (line 51).
- `size`: of the file or the directory (sum of all files).
- `nfiles`: for a directory, the number of files, recursive (line 54).

3.3 Dependency entries in a `.dvc`/`dvc.yaml` file have the same fields (table at lines 71-75).
- The hash value on a dependency appears "Only in external dependencies created with `dvc import-url`" (line 73).
- Import dependencies add `rev` and `rev_lock` (the Git commit hash of the source repo at import or update time; lines 84-85).

3.4 `dvc.lock` records, per stage, the command and the resolved dependencies, params and outputs, each with a content hash.
- Source: `content/docs/user-guide/project-structure/dvcyaml-files.md`, section "dvc.lock file" at lines 821-880.
- Purpose (lines 824-831): detect when stage definitions or dependencies changed; "Tracking of intermediate and final outputs of a pipeline".
- The example (lines 841-863) has `cmd`, then `deps:` with `path: data/clean` and `md5: ...`, then `params: params.yaml: levels.no: 5`, then `outs:` with `path`, `md5` and `size` per output.
- Lines 873-875: dependency entries and "all forms of output entries ... are also listed (per stage) in `dvc.lock`, including a content hash field (`md5`, `etag`, or `checksum`)."
- Full parameter dependencies are listed with both key and value (lines 877-878).
- Templated `dvc.yaml` values are written out in `dvc.lock` (lines 878-879).

3.5 The code that writes `dvc.lock` entries.
- Source: `dvc/stage/serialize.py`, `to_single_stage_lockfile` (line 143).
- Inner `_dumpd` (lines 155-176): for each dep and out it writes `path`. It writes `hash: md5` when the hash name is not in the legacy set (line 161). It adds the hash value via `_serialize_hi_to_dict` and then the file meta (size, nfiles), and the stage dict gets `deps`, `params`, `outs` (lines 186-190).
- Directory outputs can list their files with hashes when `with_files` is set (lines 163-170).
- Output keys defined in `dvc/output.py`: `PARAM_PATH = "path"`, `PARAM_FILES = "files"`, `PARAM_HASH = "hash"` (lines 284-302).
- `Output.dumpd` (`dvc/output.py` from line 822) writes the same fields (hash value, size/nfiles, `hash: md5`, `path`).
- Pipeline definition side: `to_pipeline_file` (line 114) writes `cmd`, `wdir`, `deps`, `params`, `outs`, `metrics`, `plots`, `frozen`, `always_changed` and `meta` into `dvc.yaml`. There deps and outs are paths only.

3.6 What the hash covers, and where it is stored.
- Source: `content/docs/user-guide/project-structure/internal-files.md`, lines 86-98.
- The hash is of file contents only: "file hashes are calculated from file contents only" (the sentence is a paraphrase-safe reading of lines 96-98). Two files with different names but the same contents share one cache entry.
- The cache is content-addressable. A file with hash `ec1d29...` is stored at `.dvc/cache/files/md5/ec/1d2935f811b77cc49b031b999cbf17`.
- A directory is stored as a `.dir` object. Lines 130-135 show it is a JSON array of `{"md5": ..., "relpath": ...}` entries, so the directory hash is a hash of that listing of file hashes.
- The default algorithm is md5: `DEFAULT_ALGORITHM = "md5"` in `iterative/dvc-data`, `src/dvc_data/hashfile/hash.py` line 34 (raw fetch).
- Run cache: pipeline runs are cached under `.dvc/cache/runs`. The internal-files page (line 163) says those files are backups of the `dvc.lock` that resulted from the run. The page lists the run cache at lines 47 and 156-163.

3.7 Content hash versus MLflow digest, for the chapter:
- DVC hashes the whole file, with no truncation. The MLflow digest hashes at most 10,000 rows of selected column types, and keeps 8 hex characters.
- Neither records the query that chose the rows. DVC's `dvc.lock` does record the command (`cmd`) and the params values of the stage that produced an output.

------------------------------------------------------------
4. MODEL CARDS (arXiv 1810.03993, fetched OK)

- Mitchell, Wu, Zaldivar, Barnes, Vasserman, Hutchinson, Spitzer, Raji, Gebru. "Model Cards for Model Reporting". arXiv:1810.03993. Submitted 5 Oct 2018 (v1); last revised 14 Jan 2019 (v2). Published at FAT* '19, 29-31 January 2019, Atlanta (DOI 10.1145/3287560.3287596).
- I read the PDF text (`https://arxiv.org/pdf/1810.03993`) and the abstract page (`https://arxiv.org/abs/1810.03993`).

4.1 Section names in Figure 1 and Section 4, in order (sections 4.1 to 4.9):
1. Model Details (4.1)
2. Intended Use (4.2)
3. Factors (4.3)
4. Metrics (4.4)
5. Evaluation Data (4.5)
6. Training Data (4.6)
7. Quantitative Analyses (4.7)
8. Ethical Considerations (4.8)
9. Caveats and Recommendations (4.9)

4.2 Training Data, in the paper: the card's Figure 1 says "May not be possible to provide in practice." and "When possible, this section should mirror Evaluation Data."
- Section 4.6 says the data may be "proprietary, or require a non-disclosure agreement", and in that case advocates "basic details about the distributions over groups in the data".
- This matters for the requirement "Record the training data of the model": the paper itself treats training data as something a card might only describe by distribution.

4.3 Evaluation Data's prompts are Datasets, Motivation and Preprocessing (Figure 1 and Section 4.5).
- Section 4.5 says referenced datasets should "point to any set of documents that provide visibility into the source and composition of the dataset" (paraphrase of the text I read; check the wording against the PDF before quoting).
- Model Details lists "Information about training algorithms, parameters, fairness constraints or other applied approaches, and features", plus model version, date, type, license and a contact.

------------------------------------------------------------
5. RETRIEVAL AND EMBEDDINGS

5.1 LangChain (langchain-ai/langchain, `master`)
- `libs/core/langchain_core/documents/base.py`, `BaseMedia` (lines 34-56) has an optional `id` and `metadata: dict[Any, Any]`, "Arbitrary metadata associated with the content" (line 56). The `id` comment says it is optional "at the moment" and should ideally be unique across the document collection (lines 45-53).
- `Document` (line 288) adds `page_content: str` (line 306). Its docstring example (line 301) sets `metadata={"source": "https://example.com"}`; the `source` key there is a convention, not a schema field.
- `libs/core/langchain_core/vectorstores/base.py`: `add_documents(documents, **kwargs) -> list[str]` (line 234) takes the documents' `page_content` and `metadata` (lines 256-258). The `embeddings` property (line 100) returns the "query embedding object if available", and the default returns `None` after a debug log that it "has not been implemented" (lines 99-107).
- `libs/core/langchain_core/embeddings/embeddings.py`: `Embeddings` is an abstract interface that maps text to a vector. I found no field for a model name or version there.
- So the base interface defines no record of which source documents or which embedding model produced the index, other than whatever the user puts in `metadata`.

5.2 LlamaIndex (run-llama/llama_index, `main`; paths under `llama-index-core/llama_index/core/`)
- `schema.py`, `BaseNode` (from about line 270): `id_` (default a new UUID4), `embedding: Optional[List[float]]` (line 278), `metadata: Dict[str, Any]`, described as "A flat dictionary of metadata fields" (line 291), and `relationships` (lines 302-307), described as "A mapping of relationships to other node information."
- `NodeRelationship.SOURCE` is the relationship that marks a node's source document (lines 207-220). `ref_doc_id` is derived from the SOURCE relationship, and is marked deprecated (lines 450-456).
- So a node can point to its parent document inside the index, if the document id is itself meaningful.
- `data_structs/data_structs.py`: `IndexStruct` has `index_id` (a new UUID4 by default) and an optional `summary` (lines 22-26). `IndexDict` (line 179) holds `nodes_dict` (vector store id to node doc_id) and marks `doc_id_dict` and `embeddings_dict` as "deprecated, not used" in comments.
- `indices/vector_store/base.py`: `VectorStoreIndex.__init__` takes `embed_model` and falls back to `Settings.embed_model` (lines 56, 70-71), and passes it to the embedding step (line 139). The embed model is held on the index object, not in the `IndexStruct` fields. I found no `embed_model` or `embedding_model` field in `data_structs.py` or `storage/storage_context.py`.
- `storage/storage_context.py`: `StorageContext.persist` (line 151) writes the docstore, index store, vector store, image store, graph store and property-graph store to files. The embedding model's identity is not among its parameters.
- Conclusion for LlamaIndex: the persisted index keeps nodes, their embeddings and relationships. The model that produced the embeddings is a runtime setting, not a stored field in the files I read.

5.3 MLflow with indexes and embeddings
- `mlflow/data/__init__.py` imports registered dataset sources and defines a `get_source` function. I saw no dataset type for a vector index or for embeddings there. I could not list the `mlflow/data` directory, so other dataset types may exist.
- A text search in `mlflow/llama_index/__init__.py` for `persist`, `embed_model` and `Settings` returned nothing, so I have no fact about how MLflow stores a LlamaIndex index. I did not read the flavor's other files.
- The pandas dataset's profile (1.8) holds only row and element counts.

5.4 What none of the sources above record:
- No project I read has a standard field for "the documents this vector index was built from" or "the embedding model that produced these vectors". Each leaves it to free-form `metadata` dicts, user conventions or runtime settings.
- I did not fetch vector database documentation (Chroma, pgvector, Pinecone, etc.), so I make no claim about them.

------------------------------------------------------------
SUMMARY OF GAPS
- MLflow prose docs and the W3C PROV specification were not fetched.
- OpenLineage: the statement that custom facets are allowed was not checked against `spec/OpenLineage.md` in this pass.
- The MLflow directory tree could not be listed (GitHub API blocked), so "no dataset type for vector indexes" is not proven.
- Nothing found records the selecting query or the derived features in any of MLflow, DVC or OpenLineage. DVC's `dvc.lock` is the only one that records the command and the params values of the producing stage.


## Correction, 13 October 2026

OpenLineage's facets (`spec/facets/`, commit `60261f0`) have no facet for training or evaluation, but
`DatasetTypeDatasetFacet` lists `MODEL` among a dataset's types, so a trained model can be named as a
dataset of that type. The note above that OpenLineage has nothing for ML is narrowed to that.
