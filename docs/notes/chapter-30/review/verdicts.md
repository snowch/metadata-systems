# VERDICTS ON THE CHAPTER 30 FINDINGS

Upheld 7, partly upheld 8, rejected 2 (17 findings).

What I ran and read:
- From `/home/user/metadata-systems/notebook` I ran `shop.integrations.airflow`, `dbt`, `spark`, `check_trino` and `jobs_by_format` on `run_week(["returns","source","failed"])`.
- I tried `$QUERY_ID`, `$SOURCE`, `$USER` and a blank source.
- I read the clones: `ol` (Spark `JobNameBuilder`, `InsertIntoHadoopFsRelationVisitor`, `JobNameSuffixProvider.trimPath`, dbt `local.py` and `processor.py`), `af` (provider `extractors/manager.py`, `plugins/adapter.py`) and `tr` (`OpenLineageListener`, `OpenLineageListenerConfig`).
- I did not clone Airflow core or Trino's `FormatInterpolator`, so Airflow's task-instance storage across versions was not re-checked.

Convention applied: in Parts VI and VII the answer cells print below the prediction cell, and the closing summary states rules applied. Chapter 29's "Before Chapter 30" and its requirement section do the same.

State of the working tree: HEAD (317701d) already changed `integrations.spark()` to use a path (`SPARK_PATH`) and re-pinned the test. `notebook/chapter_30.py` still prints and states the old name, and `docs/sources.md` still states the old rule.

**1. Spark job name. UPHELD.**
- I confirmed it in the clone. `InsertIntoHadoopFsRelationVisitor.jobNameSuffix` returns `trimPath(context, di.getName())`. `trimPath` joins the last two path elements with `_`. The dataset identifier comes from `PathUtils.fromPath` or `fromCatalogTable`, which is location-based.
- The `.` to `_` step in `JobNameBuilder` (line 59) only acts on that suffix.
- The fixture `pysparkHadoopFSEndEvent.json` gives `...warehouse_target` for output `/tmp/warehouse/target`.
- The engine now prints `...analytics_daily_sales`, so the remaining work is the page and the sources.
- Fix:
  - The page (the rules-table "named with its plan's top node and output table", the Spark paragraph, the printed-name sentence, "the table's dots become `_`", the closing summary) must say the name's last part comes from the path the files are written to.
  - It must give the shop's path as the shop's assumption and drop the dots claim.
  - `docs/sources.md` ("Read for Part VII", the Spark bullet) must record the `trimPath` rule and the path-based identifier.
  - Run the browser test, which types the reference into the chapter's cell.

**2. Analyst's-copy sentence. UPHELD.**
- The "so" does not follow.
- In the code, `queryTypeSupported` gates both `START` and `COMPLETE`, so a `SELECT` sends nothing and its input would be missing.
- The output side comes from `QueryIOMetadata.getOutput()`, which holds a Trino catalog, schema and table. A file a client saves is not one, so the output would be missing in any case.
- Fix: say that the copy would be made in Trino for this sentence, and name both missing parts (the read of `clean_orders` and the write of the file) with their separate causes.
- Chapter 9 already has the script send its own events, so the sentence must read as a supposition.

**3. Airflow "inputs from". UPHELD.**
- `extractors/manager.py` takes lineage from the operator's extractor, from hook lineage (`get_hook_lineage`) and from declared `inlets` and `outlets` (`extract_inlets_and_outlets`).
- `docs/sources.md` records none of this. The research note says it did not check it.
- Fix:
  - Record these three routes in `sources.md`.
  - Change the rules-table cell and Chapter 29's "from what each task reports" if it should match.
  - State that the shop's tasks reporting their inputs is an assumption, under "How this differs".
- The finding's COULD bullet on unrecorded timing and input claims for the other systems belongs with this fix. The facts are in the research note, so only `sources.md` needs them.

**4. Prediction already settled. PARTLY UPHELD.**
- Stands: the count of 7 under `$QUERY_ID` follows from the stated default, the table's "a query, by default" and "one query". It is a derivation, not a belief the learner could hold wrongly.
- The unsettled belief is the shared-source case. The page never says what one shared source does to the jobs and to whose runs they hold.
- Fix: move the commitment to the shared-source case, before any check runs. Keep it a written cell with no new figure. Keep the baseline check under it, as the convention allows.
- Does not stand: the claim that the merge "is never predicted" asks for a redesign. A changed question in the existing cell does the job.

**5. Printed outputs give the experiment away. PARTLY UPHELD.**
- Rejected part: the check line under the prediction cell. That is the convention, and it is now only the baseline.
- Stands: the `jobs_by_format` table. Before any change it prints `$SOURCE | 1`, `$USER | 1` and `$CLIENT_IP | 1`, which settles the merge the learner is about to try.
- Fix: place that table after the change instructions, so it reads the learner's final `source_of`, or cut it to what the prose uses (the 28). Do not show the other formats' counts before the change.
- Check that the prose "as the table below the check lists" follows the move.

**6. Starting check marked "no" without the target. PARTLY UPHELD.**
- Stands: the first mention of the aim, one job holding only `build_daily_sales`'s runs, is in the line after the changes. Before that the learner has no reason to move to `$SOURCE`.
- Fix: state the aim in a sentence before the cell. The shop's lineage wants one job for the program's 7 runs, and no other program's runs in it.
- Rejected part: the blank source. I ran it and `source_of["build_daily_sales"] = ""` does pass. The learner has to type it deliberately, and it is not worth an engine branch. Say so only if the cost is trivial.
- AGENTS.md rule 7 is about wrong-answer feedback and does not decide this.

**7. Hidden user and address. UPHELD.**
- Confirmed: the engine fixes `$USER` as `etl_service` and `$CLIENT_IP` as `10.0.0.5`.
- `$USER` gives 1 job holding the other three programs and cannot be changed through `source_of`.
- Fix: in the supposition ("from one client whose source is `shop-nightly`"), say the four jobs also share one user and one address.
- Add the user and address to the shop's assumptions in "How this differs".
- With that said, the `$USER` and `$CLIENT_IP` rows teach that a value the shop cannot vary cannot separate the programs.

**8. Format is a template. UPHELD.**
- `OpenLineageListenerConfig.isJobNameFormatValid` says a format "may consist of only letters, digits, underscores, commas, spaces, equal signs and predefined values". So the four values can be combined with fixed text.
- Fix: the page's "only from those four values" is wrong. Say the format can combine the values with fixed text, and that the cell takes one value.
- Record that validation message in `sources.md`. I could not read `FormatInterpolator` itself, so the record should say the message is the source.

**9. "What it calls a job and a run". UPHELD.**
- Dbt and Trino do not call a model or a query a job. Spark's own job is an action. Airflow's "run" is a Dag run.
- The table says what each integration makes a job and a run in OpenLineage.
- "Run" also collides with `dbt run`, and the dbt "run" in the table is a reading of the artifacts.
- Fix: in the objective, the opening sentence and the table headers, make clear the job and run are the integration's, in OpenLineage's terms. Keep each system's own term separate where the page uses it ("a job is one action" for Spark).

**10. Versions not named. PARTLY UPHELD.**
- Stands: the page says "the version read" but names no version.
- The engine docstring has Airflow 3.3.0 and provider 2.20.3, and Chapter 29 named 2.20.3.
- Fix: name the versions in the opening sentence, and the Spark, dbt and Trino sources where the table needs them.
- Rejected part: "say where earlier tries go". The 3.3.0 task-instance row is recorded as unique on Dag, task, run and map index. `task_instance_history` was read at 3.2.0 and not at 3.3.0, and `main` differs. The chapter's point needs only "one row, `try_number` 2". Do not state the history table.

**11. Jobs left out; "four kinds of job". PARTLY UPHELD.**
- Confirmed: the provider also sends Dag-level events (`job_type=_JOB_TYPE_DAG`, `dag_started`/`dag_success`/`dag_failed`). `dbt-ol` also sends a wrapper job `dbt-run-{project}` (`local.py` `job_name`).
- Fix:
  - In "How this differs", say jobs are left out as well as facets: the Dag's job, and dbt's job for the whole invocation.
  - Reading 1's "gives four kinds of job" should say so too.
- Rejected part: `.build.run`. It applies only to `dbt build`, and the page's dbt run is not one.

**12. dbt delay. PARTLY UPHELD.**
- The table prints 02:30:21 for all three, which is the last end time. The prose's "or later" is right about the real wrapper, but the table gives the earliest possible time.
- The 30 minutes comes from the shop's schedule (02:00, 02:05, 02:30) put into one invocation.
- Fix: say the first `START` is held back by the invocation's length, the shop's span here. Say the printed time is the earliest.
- Keep "late by design". The wrapper's own log line says events are sent at the end, per the research.

**13. Closing summary. PARTLY UPHELD.**
- Rejected: the framing. The "Before Chapter N" summary states rules applied, with the closing caveat. Chapters 28 and 29 do the same, and the page's next sentence qualifies it.
- Stands: "Trino named a job by its query" should be "by its query's id". The default is `$QUERY_ID`, and a query is not its name.
- If the Spark sentence changes under finding 1, it will say "path", not "table".

**14. "As in Chapter 22". UPHELD.**
- Chapter 22 has no jobs. It merges references to datasets, and its prose says that if it merges too much "the development table's runs show in production's lineage (Chapter 12)".
- The same issue affects reading 2's "as Chapter 22's aliases did". Aliases joined dataset references, not programs.
- Fix: qualify both as analogies to Chapter 22's dataset merging. Name the dataset-level case, and do not say runs or programs were merged there.

**15. Requirement section. REJECTED.**
- The last step is carried by the three items, in the same form as Chapters 20 and 22 to 29. Reading 1 says what it gives, 2 what it needs, 3 what it misses. The close is the standard "The requirement does not say which it means."
- Reading 3's "needs each system to name the same dataset the same way (Chapter 12)" states a need from Chapters 12 and 22, not a fact about these systems.
- The overstatement in reading 1 ("four kinds of job") is handled under finding 11.

**16. Read-only tables with no question. PARTLY UPHELD.**
- Stands for Airflow and dbt. CLAUDE.md puts a question in front of an instrument. The Airflow table has a discrepancy the learner can count (7 rows, 8 runs). The dbt table shows when events are sent against when the work happened.
- Fix: one sentence before each, saying what to compare. Do not add [WRITE] cells.
- Not for Spark, whose cell prints one name and whose rule the preceding prose states. The Spark change under finding 1 may carry its own question.

**17. "Dag run" column. REJECTED.**
- The column prints the night's date and the prose says "one for each night" and "Monday 14's task instance". The page never uses a logical date, so an Airflow-specific confusion is not reached here.
- The engine takes the date from the run's `START`, and renaming would touch the engine and its test for little gain.

**COULD items in the findings, for the fixer.**
- Worth taking with the above: the sourcing bullet (`sources.md` entries for when each system sends and where inputs come from, folded into finding 3); "makes each try's run id from its try number, among other values" (name the values, from `utils.py`: namespace, Dag, task, try number, map index); and the repeated sentences after the Airflow and Spark cells.
- The "in turn" wording and the mid-flow "The week has the returns desk..." line are cheap prose edits.
- The namespace notation and the platform-map caption are not worth the cost.
