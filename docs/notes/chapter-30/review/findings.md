# REVIEW OF CHAPTER 30, "Airflow, Spark, dbt and Trino"

**Checked:** I ran `shop.run_week(["returns","source","failed"])` with `integrations.airflow`, `dbt`, `spark`, `check_trino` and `jobs_by_format`, from `/home/user/metadata-systems/notebook`. The 7 task instances, the 8 OpenLineage runs (6×1 + 2), the 28 nightly queries and 28 jobs, 02:00:00 against 02:30:21, the Spark name, and the starting check (7 jobs, no) all match the page. `REFERENCE` gives 2 of 2. I also tried `$USER`, `$SOURCE` with partial fixes, an unknown format and an empty source. I checked the page's claims against the shallow clones left by the research (OpenLineage `60261f0`, Airflow provider, Trino `7a821d4`), `docs/sources.md` "Read for Part VII" and `docs/notes/part-7/research/chapter-30.md`. I read Chapters 7, 10, 12, 20, 22, 25 and 29 for the cross-references.

## BLOCKING

1. **The Spark job name is built wrongly for the command the page names.**
   - Page: "Spark's OpenLineage integration names the job from the application's name, the top node of the plan Spark ran, and the output table." Also "The plan's node is written in lower case with `_` between its words, and the table's dots become `_`." Also the printed `shop_nightly.execute_insert_into_hadoop_fs_relation_command.shop_analytics_daily_sales`.
   - Problem: for `InsertIntoHadoopFsRelationCommand` the suffix is not the table identifier with dots made `_`.
     - `InsertIntoHadoopFsRelationVisitor.jobNameSuffix` returns `trimPath(context, di.getName())`. That is the last two elements of the output's location path joined with `_`.
     - The project's own fixture `pysparkHadoopFSEndEvent.json` has output `/tmp/warehouse/target` and job `...execute_insert_into_hadoop_fs_relation_command.warehouse_target`.
     - The table-identifier route (`tableIdentifierToSuffix`) gives `database_table`, never a three-part `shop_analytics_daily_sales`.
   - The shop's name for `shop.analytics.daily_sales` therefore depends on where the table's files sit. The last bullet of "How this differs" ("Another kind of write has another top node") covers only the node.
   - The error is in `docs/sources.md` ("the output table's name with `.` made `_`") and `notebook/shop/integrations.py` (`spark()`) as well. Both record a looser reading than the code.
   - Direction: re-read the visitor, correct the suffix rule in the page, `sources.md` and the engine, and mark the table-to-name step as the shop's assumption.

2. **The analyst's-copy sentence gives the wrong cause.**
   - Page: "The analyst's copy is a `SELECT` whose result a client saves as a file. By default it sends nothing, so the edge to `clean_orders_copy.csv` would be missing."
   - Problem: the "so" is a non sequitur. Trino's output metadata describes writes to Trino tables, so a file saved by a client never appears as an output, even if `SELECT` were added to the query types. The default only removes the inputs; it does not explain the missing edge.
   - Chapter 10 also describes the copy as the analyst's script writing the result, and Chapter 9 has that script send its own events.
   - Direction: say which part of the edge is missing and why.

3. **The Airflow input claim is unsourced and incomplete.**
   - Page (rules table): "inputs from | what each task's operator reports".
   - `sources.md` records nothing on this. The research note says "I did not check how the Airflow OpenLineage provider consumes inlets and outlets." This breaks the Accuracy rule.
   - The provider's `extractors/manager.py` also takes inputs from hook lineage and from declared `inlets`/`outlets`. A task that reports none gives none.
   - Chapter 29 says the same ("the provider takes them from what each task reports"), so the shop's tasks having inputs at all is an assumption the page never states.
   - Direction: read and record the source, and say the assumption.

## SHOULD

4. **The prediction asks for something the page has already settled.**
   - Page: "write in the next cell how many jobs the 7 nightly queries of `build_daily_sales` make in Trino's events, with the default name format."
   - The rules table already says Trino's job is "a query, by default" and its run is "one query". The prose says "Its default is `$QUERY_ID`". The count is a derivation, not a belief the learner could hold wrongly.
   - The surprising result is the merge under `$SOURCE`, which is never predicted.
   - Direction: put the commitment where a belief can be wrong.

5. **The printed outputs give away the experiment.**
   - The check says "The 7 runs of `build_daily_sales` are 7 jobs in Trino's events." directly under the prediction cell.
   - The table under it lists `$SOURCE | 1`, `$USER | 1`, `$CLIENT_IP | 1` and `$QUERY_ID | 28`, which shows the merge and the 28 before the reader changes anything.
   - Direction: show less before the change.

6. **The starting check states a true fact and marks it "no", without the target.**
   - Line: "The 7 runs of `build_daily_sales` are 7 jobs in Trino's events. | no".
   - The reader is never told before the check that one job is wanted, or why. "Both tests pass: one job, holding..." comes only after the changes. This matches AGENTS.md rule 7.
   - The check also passes with a blank source (`source_of["build_daily_sales"] = ""`, a job named ""). Direction: state the target, and decide whether a blank source should pass.

7. **The Trino table's assumptions are hidden.**
   - Row `$USER | 1`: the engine fixes the user as `etl_service` and the address as `10.0.0.5`, and the page never says the four jobs share them.
   - A reader who sets `name_format = "$USER"` gets "also holds the runs of ..." and has no way to pass. The only lever named is `source_of`.
   - "How this differs" lists "the Trino client's sources and the query ids" but not the user or address.
   - Direction: state these and what the check shows for those formats.

8. **The format is a template, but the page treats it as a choice of one.**
   - Page: "The listener can name a job only from those four values, so a job's name depends on how each client is set up."
   - Trino's `FormatInterpolator` takes a template that can combine the placeholders and literal text. The engine rejects anything but one of four.
   - Direction: say the simplification, or say that the values can be combined.

9. **"What it calls a job and a run" is not true for the systems.**
   - Page: "what it calls a job and a run", then a table headed "its job" and "a run".
   - dbt and Trino do not call a model or a query a job. Spark's own job is an action, while the table's job is the OpenLineage name built from the plan and table. These are the integrations' jobs.
   - "job" has two meanings and "run" collides with `dbt run`. Direction: separate the system's term from the integration's.

10. **No versions are named and the Airflow model is version-dependent.**
    - Page: "in the version read" and "one row, `try_number` 2". No cell or sentence names a version.
    - The research (A5) says `main` keeps every try as its own row, while 3.3.0 keeps the latest live and earlier tries in `task_instance_history`.
    - Chapter 29 named the provider's version. Direction: name the versions read, and say where earlier tries go.

11. **Each integration sends jobs and events the page leaves out, and "four kinds of job" overstates.**
    - The Airflow provider also sends Dag-level events. Chapter 29 already showed the parent job `default/shop_nightly`.
    - `dbt-ol` also sends a job for the whole invocation, `dbt-run-{project}` (`local.py` `job_name`). A `dbt build` adds `.build.run` to model names.
    - Page: "gives four kinds of job, each with its own name" and "The systems also send facets the cells leave out."
    - This bears on the requirement's first reading. Direction: say jobs, not only facets, are left out.

12. **The dbt delay comes from the supposition, and "or later" contradicts the table.**
    - Page: "sent at least 30 minutes after it happened. These are late events ... they are late by design."
    - The 30 minutes comes from "Suppose the shop's three warehouse jobs ran as one dbt run". A real run does not idle between the 4-minute and 30-minute gaps of the shop's schedule.
    - The prose says "02:30:21 ... or later", but the table prints exactly 02:30:21 for all three.
    - Direction: say the delay equals the invocation's length and is the shop's.

13. **The closing summary says real systems acted.**
    - Page: "Airflow made a retried task two OpenLineage runs. Spark's job name held ... dbt sent each night's events after the run ... Trino named a job by its query".
    - Past-tense claims about real systems, contradicted by the next sentence ("The page could not show the four systems themselves"). "by its query" should be "by its query's id". Direction: phrase these as rules applied.

14. **Cross-reference: "too many runs merged, as in Chapter 22".**
    - Chapter 22 merged references to datasets by name. It did not merge runs or jobs. Direction: correct or qualify.

15. **The requirement section lacks its last step and rests on nothing shown.**
    - Reading 3: "it needs each system to name the same dataset the same way (Chapter 12)". No cell in this chapter shows any of the four systems' dataset names.
    - The section also never says which readings the integrations meet, as CLAUDE.md's five-step pattern ends. Direction: add that step, or cut the unevidenced claim.

16. **Three tables are read-only with no question in front of them.** The Airflow, Spark and dbt cells ("The next cell lists...", "prints...") are instruments with no question. Direction: give each a question to carry.

17. **The Dag run column is ambiguous.** The `Dag run | 2026-09-08` column could mean the logical date or the run date, and under Airflow 3 they can differ. Direction: say which.

## COULD

- "The name is `shop_nightly.execute_insert_into_hadoop_fs_relation_command.shop_analytics_daily_sales`." repeats the cell above it. So does "Monday 14's task instance failed on both tries: one row, `try_number` 2, state `failed`."
- The sentence "The four systems' jobs are four different things: ..." repeats the table's "its job" column.
- "in turn" in "ran in four systems in turn" could mean one after another, though the chapter treats them as four separate suppositions.
- "The week has the returns desk, the analyst's copy from Sunday 13, and Monday 14's failed night." sits mid-flow. The returns desk plays no part in the chapter.
- "makes each try's run id from its try number, among other values": name the values (namespace, Dag, task, map index, logical date).
- "8 runs" has no cell that shows it, though it is derivable.
- Namespace/name notation is mixed and unexplained in the "OpenLineage job" columns (`default/...`, `dbt/...`), and the Spark cell shows no namespace.
- The "inputs from" cell for dbt (the manifest's parents of the model) does not say that only model and source parents count.
- Sourcing: the rules-table claims on when events are sent (Airflow, Spark) and on where inputs come from (Spark, dbt, Trino) are true in the research clones. `sources.md` does not record them. Add them.
- The platform map caption, "The shop's three systems with the returns desk on Monday morning", has no link to this chapter's four systems.
