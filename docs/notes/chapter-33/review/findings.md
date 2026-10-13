# REVIEW OF CHAPTER 33, "Build the whole thing"

Numbers checked: I ran `shop.ferry.run()` from `/home/user/metadata-systems/notebook` and compared the printed tables with the as-built file. That covered `functions.log`, `compare_counts`, `check_inputs`, `edges`, `trace`, `made_from_test`, `f.report`, `storage.versions`, `storage.version_text` and `downstream`.
- I also ran `REFERENCE` for `inputs` and `suspect`.
- I ran 5 wrong `inputs` and 8 wrong `suspect` attempts through the checks.
- I ran the starter code through `collect`, `trace`, `fields` and `edges`.
- All page numbers match: 31/31, 14/24, 10/17; 35, 38, 21, 14 and 17; 37 batches in 38 runs; 36 batches and 3 reports in storage; 22 in the report.
- OpenLineage claims were checked against `docs/sources.md` ("Read for Part VIII" and the custom-facet rule at lines 119-122).
- I did not check the "13 MB / 410 MB / 9 to 12 seconds" callout.

## BLOCKING

**B1. The figure's caption and labels give away section 1's finding before the reader looks.**
- Quote (caption): "the platform records which change to a batch starts which function, and not what a function or a job writes."
- Quote (labels in `FERRY_FLOWS`): "what they write is not recorded" and "reads and writes not recorded".
- Section 1 then asks "Look for a record that links a run of `build_loads` to the batches it counted" and answers "No record links a run of `build_loads` to a batch or a version."
- CLAUDE.md says no caption or label may give away an exercise's answer. It also says the standing map shows absence by drawing no arrow, not by announcing it.
- Direction: keep the figure to what exists (the systems, their parts, the counts, and perhaps "a change starts a function"). Let the instrument cells carry the absence.
- The notes call this "the standing map's rule", but the labels go further than an absent arrow.

**B2. Section 1 pre-answers the Tuesday prediction.**
- Quote (section 1): "From the times you can work out that Wednesday's 01:00 run counted gate 2's first version. That is a reconstruction, as in Chapter 2, not a record."
- Much later the page asks, as a prediction: "write in the next cell which of gate 2's two uploads the 35 counted."
- The page asks the question twice, as "Which batches, and which versions of them…" in section 1 and as the prediction. It answers it once in section 1, before the prediction exists, and again in the trace paragraph.
- That is more than the convention that answers print below the prediction.
- Direction: say in section 1 only that the times might allow an inference. Or drop the sentence and let the prediction carry it. Or make the later prediction ask something the earlier text did not settle, such as whether the instrumented record agrees with the reconstruction.

**B3. The "test batch" cell hides what the graph returns, and the prose then overstates the graph.**
- Quotes:
  - "The next cell follows the graph downstream of the test batch and checks each dataset it reaches."
  - "The graph reached all three because each run that read the test batch, or something made from it, named what it read."
  - "the graph lists them" and "the graph lists the files, not the inboxes they were sent to".
- I ran `ferry.downstream(graph, test batch)`. It returns 5 datasets: `loads-2026-09-22.csv`, `loads-2026-09-23.csv`, `loads-2026-09-24.csv`, `boardings` and `sailing_loads`.
- `made_from_test` silently drops the Tuesday and Thursday reports. They have no line for that sailing, so the code does `continue`.
- The reader sees 3 rows and is told "the graph reached all three". The real finding is that the dataset-level graph reaches more than it counts. Chapter 16 taught that the graph over-approximates or is incomplete.
- Direction: show the reached datasets that do not count the test scans, as "no" rows or as a stated count. Say that the graph holds no times or versions that would separate Wednesday's report from Tuesday's and Thursday's. Then "the graph lists them" and "reached all three" can be made accurate.

**B4. The page's own storage description contradicts "the batch is gone", and the "no trace" readings leave out the stored bytes.**
- Quotes:
  - "A run of `drop_scans` reads nothing: the batch is gone."
  - Reading 4: "no record that the batch ever existed: this would remove the events and edges that explain why Wednesday's 19:30 showed 22, and the version the delete removed."
- The platform table says object storage records "every version, with a marker where one was deleted".
- I checked: after the delete, `storage.exists(uri)` is False. But `storage.versions(uri)` still lists `e622b165c27a`, and `storage.version_text(uri, 'e622b165c27a')` returns the five test scans.
- So the deleted batch's content survives in the bucket, in the ferry's own storage. None of the four readings names it. A reader who has just been told storage keeps every version will write exactly this reading.
- Direction: add the reading (no copy of the content left in storage) and say which readings the ferry's platform meets. Chapter 32 ends its requirement with "This record meets none of the three." Chapter 33's third requirement never says what the platform meets.

## SHOULD

**S1. The `suspect` instruction contradicts its own test, and the explanation arrives too late and too early.**
- Quote: "Change it so that it flags a run whose scans did not reach `boardings`."
- Read literally, that rule flags Wednesday's aborted-scan batch, because that scan did not reach `boardings`. I ran `rows_written < scans_read`: test 2 fails with "Also flagged: Wednesday's 12:30 from the mainland, gate 1."
- The distinguishing criterion is explained only after the check, as "A rule that flags a run that wrote fewer rows than it read scans also flags Wednesday's 12:30…".
- That paragraph also says "`load_scans` leaves such a scan out on purpose" before the `fields` cell. It hands over the mechanism of the loss (batches without `scanned_at`) ahead of the evidence that shows it.
- The check line "0 of Thursday's 2 runs on the island's gate 2 after noon are flagged." tells the reader where the loss is. The "where" step of the investigation is told, not found.
- "Change `suspect` until both tests pass." repeats the instruction given above the check.
- Direction: state the target in terms that separate lost from filtered. Move the aborted-scan fact to after the reader has tried. Consider wording check line 1 so it does not name the gate.

**S2. `check_inputs` messages do not tell a reader with wrong code where to look.**
- Wrong `previous` for an overwrite gives "1 of 38 runs … do not name the version of the batch they read." That reader did name a version, the wrong one.
- Putting `version` at the top level of the input gives "38 of 38 runs … do not name the version…" and, for the delete, "names the batch, with its version not recorded". That is awkward English, and neither line says the version belongs in the input's `facets`.
- Naming the dataset `key@version` gives "names nothing" for the delete, although it names a different dataset.
- The page never shows the shape of an input with a facet. It says only "in OpenLineage's `version` facet, whose field is `datasetVersion`" and "`shop.ferry.version_facet(version)` makes the `version` facet".
- Direction: separate "no version", "wrong version" and "version in the wrong place" in the messages. Say where the facet goes, or point to the Chapter 8 example.
- Positive: the delete-with-`version` attempt gives a good line ("the version `3bebca4eb852`; the version it removed is `e622b165c27a`"). The KeyError message is clear.

**S3. Numbers and claims stated with no cell that shows them.**
- Quote: "the report shows 22 passengers on Wednesday's 19:30 from the island, and the harbour master counted 17." No cell prints 22 or 17. The `made_from_test` cell prints only yes/no.
- The 17 is also Thursday's 19:30 harbour count in the earlier table, a coincidence that invites confusion. I checked: Wednesday gives 9+8, Thursday 10+7.
- "a test batch of 5 scans" is never shown.
- Quote: "`boardings` keeps the batch's name, in its column `batch`, and not its version". No cell shows `boardings`' columns.
- The aborted scan batch is described but never displayed once the reader's `suspect` passes.
- "Both gates' batches arrived" has no cell behind it.
- Direction: add the report line and the harbour count to the made-from cell, or pick a different count. Show `boardings`' columns somewhere.

**S4. 36 batches in the figure and 37 in the edges are never reconciled.**
- The figure caption says "object storage holds 36 batches". The edges table and the prose say "`load_scans` read 37 batches in 38 runs."
- The 37th is the deleted test batch, and the 38th run is Tuesday's overwrite. Neither is explained at that point, and a reader will count.
- Direction: one clause saying which batch is no longer listed and which was loaded twice.

**S5. A word with two meanings on one page, and a thing named before it is explained.**
- "version" has two meanings. Quote: "with the shop's versions of the pieces you wrote in Chapters 25 and 26". The page's other "version" is a batch's version. Use "the shop's reference collector and graph" or similar.
- `ferry_batchChange` appears in the printed event ("ferry_batchChange": … "change": "deleted") before the paragraph that explains it, which comes after the cell.
- "run" is used as a verb for the simulation ("The next cell runs the ferry's three days") and as the noun for a function run. This is minor.

**S6. The opening names the platform before the page introduces it, and the figure duplicates the next table.**
- The Objectives and the figure ("the ferry's four systems", `load_scans`, `sailing_loads`) come before "You have joined the data team of an island ferry."
- The `shop.ferry.platform()` table then restates the same four systems.
- Direction: put the situation first, as Chapter 2's standing example does. Make the figure carry something the table does not.

**S7. Who produces the jobs' events is never said.**
- Quote: "The ferry's function platform builds each function run's OpenLineage events. The inputs come from a piece of code you write, `inputs(change)`."
- `build_loads` and `send_report` also appear in the graph with reads and writes, and the closing lists "No job writes `sailings`… nothing sends an event about it." The page never says the jobs' events are given, or that the reader is not instrumenting them.

**S8. The `lifecycleStateChange` claim is a design argument presented as a fact about OpenLineage.**
- Quote: "It describes a change a run makes to a dataset. The gates and the engineer changed the batches, not the functions, so the ferry records the change that started a function in a facet of its own".
- `docs/sources.md` supports only that it records "the lifecycle states of the Dataset", with the documentation page showing it on an output. It does not say the specification confines it to changes a run makes.
- Label it as the ferry's reasoning, and add it to the model-versus-reality bullet about the ferry's choices. That bullet currently covers only the removed-version choice.

**S9. The requirement habit is not closed.**
- Objective 6 says "Question three of the ferry's requirements before building to them." The third requirement ("A deleted batch must leave no trace.") has nothing built to it and no statement of what the platform meets (see B4).
- The close and the "Three questions" do not return to questioning a requirement, which is the habit the course says it teaches beyond metadata.
- Direction: one closing question about it.

## COULD

- "Thursday afternoon's sailings" includes the 19:30 sailing.
- Message 3 ("An engineer's test batch got into Wednesday's figures. It was deleted on Thursday morning.") nearly answers the later prediction before it is asked.
- "The ferry's data team has a requirement for this" has a vague "this". "The question above needs this one" is ambiguous, because two questions sit above it.
- "Your inputs added that link, version by version." personifies slightly.
- The last summary sentence ("who read the emailed report, or what anybody did with it") claims limits the chapter never demonstrates.
- "The gates write no `scanned_at` when a scan is aborted" is not what the data holds. The engine writes `"scanned_at": null`, so the key is present with no value. Say "no time".
- The model-versus-reality list does not say that keeping every version and a delete marker is a storage setting, not a given.
- Read before the reader's change, these hold only afterwards: "`drop_scans` read 1 batch" (the starter's edges show no read row) and "gate 2's first version, `15da88b56abc`" (the starter's trace says "not recorded"). Both are prefaced, "With your change to `inputs`" and the "Without them…" sentence, so this is acceptable.

## Answers to the brief's questions

- **What to change:** `inputs` is clear. `suspect` is not (S1).
- **Check lines for wrong code:** weak for `inputs` (S2) and good for `suspect` (the "Also flagged" and KeyError lines).
- **Predictions:** all three are beliefs the reader can hold. The Tuesday one is pre-answered (B2). "Did any run fail" is only mildly shadowed by the "finished"/"succeeded" columns already printed.
- **Requirements:** the first and second are questioned before the build. The third is questioned after the evidence and with no build (B4, S9).
- **OpenLineage claims:** `version`/`datasetVersion`, the `schema` and statistics facets, the `lifecycleStateChange` values and the custom-facet prefix rule are all supported by `docs/sources.md`. The one exception is the unsupported edge of the `lifecycleStateChange` sentence (S8).
- **Scope for a final chapter:** the reader writes two small functions. Model, capture, ingest and schemas are given or only read. That is lighter than "almost everything at once", and acceptable, but the plan's "model it" is the page's choice, not the reader's.
