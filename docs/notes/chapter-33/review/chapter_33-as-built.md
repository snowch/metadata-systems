[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 32](chapter_32.ipynb)

# Chapter 33: Build the whole thing

**Objectives**

- Find what the ferry's platform records about its own work, and what it does not.
- Instrument the ferry's functions so that each run names the batch, and the version, it read.
- Diagnose a loss that no failed run shows.
- Explain one sailing's figure from the versions its run counted.
- Find what still counts a batch after it was deleted.
- Question three of the ferry's requirements before building to them.

The figure below shows the ferry's four systems on Friday 25 at 09:00.

## The ferry's platform

You have joined the data team of an island ferry. It crosses between the mainland and the island three times a day from each side: from the mainland at 07:30, 12:30 and 17:30, and from the island at 09:30, 14:30 and 19:30.

Each harbour has two ticket gates. A minute after each departure, each gate uploads the sailing's scans to object storage as one batch, in the bucket `ferry-gates`. Each batch holds one scan per line, with the ticket, the fare and the time it was scanned, `scanned_at`.

A change to a batch starts a function. `load_scans` starts when a batch is created or overwritten, and puts its scans into the warehouse table `boardings`. `drop_scans` starts when a batch is deleted, and removes its scans from `boardings`.

At 01:00 each night, the job `build_loads` counts the day before's passengers for each sailing into the table `sailing_loads`. At 06:00, the job `send_report` writes those counts to a file in the bucket `ferry-reports`, and the harbour masters get the file by email.

On Friday 25 at 09:00, the operations manager sends three messages:

- "Thursday afternoon's sailings from the island look nearly empty. The harbour master counted far more people on board."
- "Tuesday's 17:30 from the mainland shows 35 passengers. `boardings` has 38."
- "An engineer's test batch got into Wednesday's figures. It was deleted on Thursday morning."

The next cell runs the ferry's three days and lists its systems, with what each records about its own work.

    >>> platform = shop.ferry.run()
    >>> storage, functions = platform.storage, platform.functions
    >>> warehouse, scheduler = platform.warehouse, platform.scheduler
    >>> shop.ferry.platform()
      | system | part | records
      | object storage | `s3://ferry-gates`, `s3://ferry-reports` | each object's key, size, time, and every version, with a marker where one was deleted
      | functions | `load_scans`, `drop_scans` | each trigger, and each invocation: when, which object and version, and that it finished
      | warehouse | `sailings`, `boardings`, `sailing_loads` | each table's columns, rows and last change
      | scheduler | `build_loads` at 01:00, `send_report` at 06:00 | each run's start, end and status

Which batches, and which versions of them, was the row of `sailing_loads` for Tuesday's 17:30 from the mainland built from?

The next three cells show what the function platform and the scheduler record: the functions' triggers; the log of every function run on that sailing's batches; and the runs of `build_loads`.

Look for a record that links a run of `build_loads` to the batches it counted.

    >>> functions.triggers()
      | function | starts when
      | load_scans | an object in `s3://ferry-gates` is created or overwritten
      | drop_scans | an object in `s3://ferry-gates` is deleted

    >>> functions.log("s3://ferry-gates/mainland/2026-09-22/1730")
      | started | function | object | version | status
      | 2026-09-22T17:31:02Z | load_scans | s3://ferry-gates/mainland/2026-09-22/1730/gate-1.jsonl | 4a6121574c55 | finished
      | 2026-09-22T17:31:02Z | load_scans | s3://ferry-gates/mainland/2026-09-22/1730/gate-2.jsonl | 15da88b56abc | finished
      | 2026-09-23T07:05:02Z | load_scans | s3://ferry-gates/mainland/2026-09-22/1730/gate-2.jsonl | f0ff6ad37438 | finished

    >>> scheduler.runs("build_loads")
      | job | started | finished | status
      | build_loads | 2026-09-23T01:00:00Z | 2026-09-23T01:00:04Z | succeeded
      | build_loads | 2026-09-24T01:00:00Z | 2026-09-24T01:00:04Z | succeeded
      | build_loads | 2026-09-25T01:00:00Z | 2026-09-25T01:00:04Z | succeeded

The log lists 3 runs of `load_scans` on that sailing's batches: gate 1's batch at 17:31:02 on Tuesday, gate 2's at 17:31:02, and gate 2's again at 07:05:02 on Wednesday, each with its version.

`build_loads` ran at 01:00 on Wednesday, Thursday and Friday.

No record links a run of `build_loads` to a batch or a version.

From the times you can work out that Wednesday's 01:00 run counted gate 2's first version. That is a reconstruction, as in Chapter 2, not a record.

## What to record

The ferry's data team has a requirement for this, in the box below.

[BOX] The ferry's requirement: "Record the lineage of every boarding."

Before you read on, write in the next cell what "record the lineage of every boarding" means to you here.

    [WRITE] What does "record the lineage of every boarding" mean here?
    [WRITE] ........

"Record the lineage of every boarding" could mean three things. Each item says what it needs:

- per scan: each row of `boardings` needs the batch it came from. `boardings` keeps the batch's name, in its column `batch`, and not its version;
- per batch: each run of a function needs to name the batch it read;
- per version: each run needs to name the batch and the version it read, so that a figure can be traced to the versions it counted. The question above needs this one.

The requirement does not say which it means. This page builds to the third. With the column `batch`, it answers the first two as well.

Each batch is one dataset, named by its key in `ferry-gates`. The version a run read goes on that run's input, in OpenLineage's `version` facet, whose field is `datasetVersion`, as the shop's returns desk did in Chapters 7 and 8. A batch's versions stay one dataset over time.

The other choice, a dataset for each version, gives each version its own node in the graph; a reader then needs the key to find a batch's versions. Neither choice is wrong.

## Instrumenting the functions

The ferry's function platform builds each function run's OpenLineage events. The inputs come from a piece of code you write, `inputs(change)`.

`change` holds the batch's bucket and key, what happened (`"created"`, `"overwritten"` or `"deleted"`), the new version, and the version before it, `previous`, where there was one.

As it stands, `inputs` names the batch without its version for a create or an overwrite, and nothing for a delete. The shop's `remove_return`, in Chapters 7 and 8, named no input either.

A run of `drop_scans` reads nothing: the batch is gone. Naming the version it removed as its input is the ferry's choice: it links the removal to the batch.

Change `inputs` so that each run names the version it read, and a delete names the version it removed. `shop.ferry.version_facet(version)` makes the `version` facet. Select the cell and press **Run below**.

The check below it tests every function run of the three days. As `inputs` stands, 1 of 3 tests passes. The cell after the check prints the event of the run that the delete of the test batch started.

    >>> def inputs(change):
    >>>     batch = {"namespace": change["bucket"], "name": change["key"]}
    >>>     if change["change"] == "deleted":
    >>>         return []
    >>>     return [batch]

    >>> shop.ferry.check_inputs(platform, inputs)
      | test | passes
      | Every event passes Chapter 8's check. | yes
      | 38 of 38 runs started by a create or an overwrite do not name the version of the batch they read. | no
      | The run started by the delete of the test batch names nothing; the version it removed is `e622b165c27a`. | no

    >>> print(shop.openlineage.show(shop.ferry.one_event(platform, inputs, "deleted")))
      {
        "eventType": "COMPLETE",
        "eventTime": "2026-09-24T08:30:03Z",
        "run": {
          "runId": "01a0d289-3310-7ef5-92d8-2819382a8772",
          "facets": {
            "ferry_batchChange": {
              "_producer": "https://example.org/ferry/functions/runtime/v1",
              "_schemaURL": "https://example.org/ferry/facets/1-0-0/FerryBatchChangeRunFacet.json#/$defs/FerryBatchChangeRunFacet",
              "change": "deleted"
            }
          }
        },
        "job": {
          "namespace": "ferry",
          "name": "drop_scans"
        },
        "inputs": [],
        "outputs": [
          {
            "namespace": "warehouse://ferry-warehouse",
            "name": "ferry.boardings"
          }
        ],
        "producer": "https://example.org/ferry/functions/runtime/v1",
        "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"
      }

With the change, all 3 tests pass. The delete's event names the test batch with the version `e622b165c27a`, the version the engineer deleted.

OpenLineage has a facet for a change to a dataset, `lifecycleStateChange`, with values such as `CREATE`, `OVERWRITE` and `DROP`. It describes a change a run makes to a dataset. The gates and the engineer changed the batches, not the functions, so the ferry records the change that started a function in a facet of its own, `ferry_batchChange`.

## Capturing the ferry's lineage

The next cell sends every event through the collector and builds the lineage graph, with the shop's versions of the pieces you wrote in Chapters 25 and 26. It lists the graph's edges by job, with the batches counted rather than listed.

    >>> collected = shop.ferry.collect(shop.ferry.events(platform, inputs))
    >>> graph33 = shop.ferry.graph(collected)
    >>> shop.ferry.edges(graph33)
      | job | edge | dataset | runs
      | build_loads | reads | boardings | 3
      | build_loads | reads | sailings | 3
      | build_loads | writes | sailing_loads | 3
      | drop_scans | writes | boardings | 1
      | load_scans | reads | s3://ferry-gates/... (37 batches) | 38
      | load_scans | writes | boardings | 38
      | send_report | reads | sailing_loads | 3
      | send_report | writes | loads-2026-09-22.csv | 1
      | send_report | writes | loads-2026-09-23.csv | 1
      | send_report | writes | loads-2026-09-24.csv | 1

With your change to `inputs`, `load_scans` read 37 batches in 38 runs. `drop_scans` read 1 batch. `build_loads` read `boardings` and `sailings` and wrote `sailing_loads`. `send_report` read `sailing_loads` and wrote 3 report files.

No job writes `sailings`. The timetable was typed in by hand, and nothing sends an event about it.

The graph now holds which run read which version of each batch, and when. The question about Tuesday's 17:30 comes back below.

## Thursday afternoon

The first message is about Thursday afternoon's sailings from the island. The next cell sets Thursday's rows of `sailing_loads` for the island beside the harbour master's own count of the people on board.

    >>> shop.ferry.compare_counts(platform, "2026-09-24", "island")
      | sailing | sailing_loads | counted on board
      | 2026-09-24 island 09:30 | 31 | 31
      | 2026-09-24 island 14:30 | 14 | 24
      | 2026-09-24 island 19:30 | 10 | 17

At the 09:30 sailing, `sailing_loads` has 31 and the harbour master counted 31 on board. At the 14:30 sailing, it has 14 and the harbour master counted 24. At the 19:30 sailing, it has 10 and the harbour master counted 17.

For the two afternoon sailings, `sailing_loads` counts 10 and 7 fewer than the harbour master.

Before you read on, write in the next cell whether any run of a function or a job failed in the three days.

    [WRITE] Did any run of a function or a job fail in the three days?
    [WRITE] ........

    >>> shop.ferry.run_states(collected)
      | job | runs | COMPLETE | FAIL
      | build_loads | 3 | 3 | 0
      | drop_scans | 1 | 1 | 0
      | load_scans | 38 | 38 | 0
      | send_report | 3 | 3 | 0

Every run finished: 38 runs of `load_scans`, 1 of `drop_scans`, and 3 each of `build_loads` and `send_report`. None failed.

Compare this with what you wrote.

The ferry's next requirement, in the box below, is for a loss like this one.

[BOX] The ferry's requirement: "Alert us when a sailing's data is missing."

Before you read on, write in the next cell what "a sailing's data is missing" means to you here.

    [WRITE] What does "alert us when a sailing's data is missing" mean here?
    [WRITE] ........

It could mean four things:

- no batch arrived from a gate: it needs the timetable and the list of gates. Both gates' batches arrived, so it does not catch it;
- a batch arrived and its run failed: it needs each run's state. No run failed, so it does not;
- a batch arrived, its run finished, and its scans did not reach `boardings`: it needs, for each run, the scans it read and the rows it wrote. It catches it;
- a sailing carried fewer passengers than usual: it needs past loads, and a sailing that is quiet for another reason looks the same.

The requirement does not say which it means. This page builds to the third.

The events of each run of `load_scans` hold its state (`state`), the scans it read (`scans_read`), the rows it wrote to `boardings` (`rows_written`), and the batch's fields (`fields`, from OpenLineage's `schema` facet).

The next cell defines `suspect(run)`, which flags a run. As it stands, it flags a run that failed.

Change it so that it flags a run whose scans did not reach `boardings`. Select the cell and press **Run below**.

The check below it tests every run of `load_scans`. As `suspect` stands, 1 of 2 tests passes: it flags neither of Thursday's runs.

    >>> def suspect(run):
    >>>     return run["state"] == "FAIL"

    >>> shop.ferry.check_suspect(collected, suspect)
      | test | passes
      | 0 of Thursday's 2 runs on the island's gate 2 after noon are flagged. | no
      | No other run is flagged. | yes

A rule that flags a run that wrote fewer rows than it read scans also flags Wednesday's 12:30 from the mainland, gate 1. That batch holds one aborted scan with no `scanned_at`. The gates write no `scanned_at` when a scan is aborted, and `load_scans` leaves such a scan out on purpose.

Change `suspect` until both tests pass.

The next cell lists every batch from the island's gate 2, with its fields as its run recorded them.

    >>> shop.ferry.fields(collected, "island", "gate-2")
      | started | batch | fields | scans read | rows written
      | 2026-09-22T09:31:02Z | island/2026-09-22/0930/gate-2.jsonl | fare, scanned_at, ticket | 13 | 13
      | 2026-09-22T14:31:02Z | island/2026-09-22/1430/gate-2.jsonl | fare, scanned_at, ticket | 10 | 10
      | 2026-09-22T19:31:02Z | island/2026-09-22/1930/gate-2.jsonl | fare, scanned_at, ticket | 7 | 7
      | 2026-09-23T09:31:02Z | island/2026-09-23/0930/gate-2.jsonl | fare, scanned_at, ticket | 14 | 14
      | 2026-09-23T14:31:02Z | island/2026-09-23/1430/gate-2.jsonl | fare, scanned_at, ticket | 11 | 11
      | 2026-09-23T19:31:02Z | island/2026-09-23/1930/gate-2.jsonl | fare, scanned_at, ticket | 8 | 8
      | 2026-09-24T09:31:02Z | island/2026-09-24/0930/gate-2.jsonl | fare, scanned_at, ticket | 13 | 13
      | 2026-09-24T14:31:02Z | island/2026-09-24/1430/gate-2.jsonl | fare, scan_time, ticket | 10 | 0
      | 2026-09-24T19:31:02Z | island/2026-09-24/1930/gate-2.jsonl | fare, scan_time, ticket | 7 | 0

From 14:31:02 on Thursday, the island's gate 2 batches hold `scan_time` where the earlier ones hold `scanned_at`. `load_scans` read 10 scans and 7 scans from them and wrote 0 rows: it keeps only scans with a `scanned_at`.

The fields show what changed and when. Nothing in the records shows why the gate's batches changed.

## Tuesday's 17:30

The second message is about Tuesday's 17:30 from the mainland. `sailing_loads` shows 35 passengers for it, and `boardings` holds 38 rows. Gate 2 uploaded its batch for that sailing twice: 14 scans at 17:31 on Tuesday, and all 17 at 07:05 on Wednesday.

Before you read on, write in the next cell which of gate 2's two uploads the 35 counted.

    [WRITE] Which of gate 2's two uploads did the 35 count?
    [WRITE] ........

    >>> shop.ferry.trace(platform, collected, "2026-09-22 mainland 17:30")
      | step | made by | batch | version | passengers
      | the row of `sailing_loads` | `build_loads`, 2026-09-23T01:00:00Z |  |  | 35
      | a batch, as that run read it | `load_scans`, 2026-09-22T17:31:02Z | gate-1.jsonl | not recorded | 21
      | a batch, as that run read it | `load_scans`, 2026-09-22T17:31:02Z | gate-2.jsonl | not recorded | 14
      | a later version of a batch | `load_scans`, 2026-09-23T07:05:02Z | gate-2.jsonl | not recorded | 17
      | `boardings` now |  |  |  | 38

Read the trace from the top. The row of `sailing_loads`, 35, was written by `build_loads` at 01:00 on Wednesday.

That run counted gate 1's batch, 21 scans, and gate 2's first version, `15da88b56abc`, 14 scans.

Gate 2's second version, `f0ff6ad37438`, with 17 scans, was loaded at 07:05:02 on Wednesday, after the run. `boardings` now holds 38.

Compare this with what you wrote.

`build_loads` rebuilds only the day before, so no later run rebuilt Tuesday's rows. The row stays at 35 until somebody rebuilds it.

The versions in the trace come from the inputs you wrote. Without them, the trace shows "not recorded" for each version.

## The test batch

The third message is about a test batch. At 23:40 on Wednesday, an engineer uploaded a test batch of 5 scans under Wednesday's 19:30 from the island, and `load_scans` loaded it. `build_loads` ran at 01:00 on Thursday, and `send_report` at 06:00 sent the file `loads-2026-09-23.csv`. At 08:30 the engineer deleted the batch, and `drop_scans` removed its rows from `boardings`.

The next cell follows the graph downstream of the test batch and checks each dataset it reaches.

Before you read on, write in the next cell which of `boardings`, `sailing_loads` and `loads-2026-09-23.csv` still count the test scans.

    [WRITE] Which of boardings, sailing_loads and loads-2026-09-23.csv still count the test scans?
    [WRITE] ........

    >>> shop.ferry.made_from_test(platform, graph33)
      | dataset | still counts the test scans
      | boardings | no
      | sailing_loads | yes
      | loads-2026-09-23.csv | yes

`boardings` no longer counts them. `sailing_loads` and `loads-2026-09-23.csv` still do: the report shows 22 passengers on Wednesday's 19:30 from the island, and the harbour master counted 17.

Compare this with what you wrote.

The delete reached only what `drop_scans` changed. The row of `sailing_loads` was built before the delete, and the report is a copy that was emailed at 06:00.

The graph reached all three because each run that read the test batch, or something made from it, named what it read.

The ferry has a requirement for deleted batches, in the box below.

[BOX] The ferry's requirement: "A deleted batch must leave no trace."

Before you read on, write in the next cell what "leave no trace" means to you here.

    [WRITE] What does "a deleted batch must leave no trace" mean here?
    [WRITE] ........

It could mean four things. Each item says what it needs:

- no rows made from the batch: `drop_scans` does this;
- no figure that counted it: each figure built from it must be built again; the graph lists them;
- no copy of such a figure: each copy must be found and replaced, the reports already emailed included; the graph lists the files, not the inboxes they were sent to;
- no record that the batch ever existed: this would remove the events and edges that explain why Wednesday's 19:30 showed 22, and the version the delete removed.

The last reading works against the second and the third: finding every figure the batch reached needs the lineage that the last reading would remove.

The requirement does not say which it means.

## The ferry's three days

The ferry's platform recorded its triggers, its function runs and its job runs, and nothing that linked a figure to the batches it counted. Your inputs added that link, version by version.

Thursday's loss failed no run. The runs' own counts showed it, and the batches' fields showed what changed.

Tuesday's row counted gate 2's first version, and no later run rebuilt Tuesday.

The delete removed the test batch's rows, and not the figure or the report built from them.

The records could not show why the gate's batches changed, who read the emailed report, or what anybody did with it.

The course ends here.

Three questions:

- On a platform you work on, which record links a figure to the version of the data it counted?
- Which of your jobs rebuild only the latest day, and what happens to a correction that arrives later?
- When data must be deleted, which copies of what was made from it does your platform know about?

### How this differs from a real platform

- The ferry, its platform and its three days are invented. No real object store, function platform or scheduler is described: when a change starts a function, and what each system records, are the ferry's own.
- Here each change to a batch starts its function once, in order. Chapters 19 and 20 showed what happens when a start is repeated or out of order.
- The facets `version`, `schema`, `inputStatistics`, `outputStatistics` and `lifecycleStateChange` are OpenLineage's. `ferry_batchChange` is the ferry's own.
- Naming the removed version as the input of a run that reads nothing is the ferry's choice.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 32](chapter_32.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

