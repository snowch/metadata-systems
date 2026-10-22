# Copyright © 2026 Christopher Snow

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    width="medium",
    app_title="Build the whole thing",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 32](chapter_32.ipynb)

    # Chapter 33: Build the whole thing

    **Objectives**

    - Find what the ferry's platform records about its own work, and what it does not.
    - Instrument the ferry's functions so that each run names the batch, and the version, it read.
    - Diagnose a loss that no failed run shows.
    - Explain one sailing's figure from the versions its run counted.
    - Find what still counts a batch after it was deleted.
    - Question three of the ferry's requirements before building to them, and say which reading the platform meets.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The page runs Python in your browser, and the first time you open it on its own your browser downloads about 13 MB.

    <details><summary>Time and memory</summary>

    The page downloaded less than 1 MB when opened from Chapter 32's link, in a browser that had opened and run Chapter 32 (measured on a computer). Chapter 32's link opens this page in a new tab. Chapter 32 stays open in its own tab and keeps its own memory. On a phone, closing Chapter 32 leaves more memory for this page.

    Running every cell took 9 to 12 seconds, and the page used about 420 MB of memory. If a phone runs short of memory, the browser may reload the page, and a reload loses anything you have not saved.

    </details>
    """), kind="warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    **Running and saving the page**

    1. Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page.
    2. A cell does not run again when a cell it uses changes. After you change a cell, select it and press **Run below**: it runs that cell and every cell below it.
    3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your saved copy, which stays in this browser. When the chapter is updated, the page shows the new version instead. If you changed a cell, your copy is kept under the chapter's name with "(your copy)" added, and [the list of files in this browser](https://snowch.github.io/metadata-systems/jupyterlite/tree/) opens it.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The ferry's platform

    You have joined the data team of an island ferry. It crosses between the mainland and the island three times a day from each side: from the mainland at 07:30, 12:30 and 17:30, and from the island at 09:30, 14:30 and 19:30.

    Each harbour has two ticket gates. A minute after each departure, each gate uploads the sailing's scans to object storage as one batch, in the bucket `ferry-gates`. Each batch holds one scan per line, with the ticket, the fare and the time it was scanned, `scanned_at`.

    A change to a batch starts a function. `load_scans` starts when a batch is created or overwritten, and puts its scans into the warehouse table `boardings`. `drop_scans` starts when a batch is deleted, and removes its scans from `boardings`.

    At 01:00 each night, the job `build_loads` counts the day before's passengers for each sailing into the table `sailing_loads`. At 06:00, the job `send_report` writes those counts to a file in the bucket `ferry-reports`, and the harbour masters get the file by email.

    On Friday 25 at 09:00, the operations manager sends three messages:

    - "Thursday's sailings after noon from the island look nearly empty. The harbour master counted far more people on board."
    - "Tuesday's 17:30 from the mainland shows 35 passengers. `boardings` has 38."
    - "An engineer's test batch got into Wednesday's figures. It was deleted on Thursday morning."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The figure below shows the ferry's four systems on Friday 25 at 09:00. The cell after it runs the ferry's three days and lists its systems, with what each records about its own work.
    """)
    return


@app.cell(hide_code=True)
def _(figures, mo, shop):
    mo.Html(figures.figure(figures.ferry_platform(shop.ferry.run()), "The ferry's four systems on Friday 25 at 09:00; object storage holds 36 batches and 3 reports."))
    return


@app.cell
def _(shop):
    platform = shop.ferry.run()
    storage, functions = platform.storage, platform.functions
    warehouse, scheduler = platform.warehouse, platform.scheduler
    shop.ferry.platform()
    return functions, platform, scheduler, storage, warehouse


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which batches, and which versions of them, was the row of `sailing_loads` for Tuesday's 17:30 from the mainland built from?

    The next three cells show what the function platform and the scheduler record: the functions' triggers; the log of every function run on that sailing's batches; and the runs of `build_loads`.

    Look for a record that links a run of `build_loads` to the batches it counted.
    """)
    return


@app.cell
def _(functions):
    functions.triggers()
    return


@app.cell
def _(functions):
    functions.log("s3://ferry-gates/mainland/2026-09-22/1730")
    return


@app.cell
def _(scheduler):
    scheduler.runs("build_loads")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The log lists 3 runs of `load_scans` on that sailing's batches: gate 1's batch at 17:31:02 on Tuesday, gate 2's at 17:31:02, and gate 2's again at 07:05:02 on Wednesday, each with its version.

    `build_loads` ran at 01:00 on Wednesday, Thursday and Friday.

    No record links a run of `build_loads` to a batch or a version.

    The times might let you work out which version a run counted. That would be a reconstruction, as in Chapter 2, not a record.

    ## What to record

    The ferry's data team has a requirement for lineage, in the box below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The ferry's requirement: "Record the lineage of every boarding."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "record the lineage of every boarding" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of "record the lineage of every boarding"</summary>

    "Record the lineage of every boarding" could mean three things. Each item says what it needs:

    - per scan: each row of `boardings` needs the batch it came from. `boardings` keeps the batch's name, in its column `batch`, and not its version;
    - per batch: each run of a function needs to name the batch it read;
    - per version: each run needs to name the batch and the version it read, so that a figure can be traced to the versions it counted. The question about Tuesday's 17:30 above needs this one.

    The requirement does not say which it means. This page builds to the third. With the column `batch`, it answers the first two as well.

    </details>

    Each batch is one dataset, named by its key in `ferry-gates`. The version a run read goes on that run's input, in OpenLineage's `version` facet, whose field is `datasetVersion`, as the shop's returns desk did in Chapters 7 and 8. A batch's versions stay one dataset over time.

    The other choice, a dataset for each version, gives each version its own node in the graph; a reader then needs the key to find a batch's versions. Neither choice is wrong.

    ## Instrumenting the functions

    The ferry's function platform builds each function run's OpenLineage events. The inputs come from a piece of code you write, `inputs(change)`.

    `change` holds:

    - **Location:** the batch's bucket and key.
    - **What happened:** `"created"`, `"overwritten"` or `"deleted"`.
    - **New version:** the new version of the batch.
    - **Previous version:** the version before it, `previous`, where there was one.

    As it stands, `inputs` names the batch without its version for a create or an overwrite, and nothing for a delete. The shop's `remove_return`, in Chapters 7 and 8, named no input either.

    A run of `drop_scans` reads nothing: the batch is no longer listed in the bucket. Naming the version it removed as its input is the ferry's choice: it links the removal to the batch.

    Change `inputs` so that each run names the version it read, and a delete names the version it removed. `shop.ferry.version_facet(version)` makes the `version` facet. Select the cell and press **Run below**.

    The event the cell after the check prints, from the run that the delete of the test batch started, holds the facet `ferry_batchChange`, with the change that started the function. OpenLineage has a dataset facet, `lifecycleStateChange`, whose values include `CREATE`, `OVERWRITE` and `DROP`; its documentation shows it on a run's output. Recording the change that started a function in a facet of its own is the ferry's choice.

    The check below it tests every function run of the three days. As `inputs` stands, 1 of 3 tests passes.
    """)
    return


@app.cell
def _(shop):
    def inputs(change):
        batch = {"namespace": change["bucket"], "name": change["key"]}
        if change["change"] == "deleted":
            return []
        return [batch]
    return (inputs,)


@app.cell
def _(inputs, platform, shop):
    shop.ferry.check_inputs(platform, inputs)
    return


@app.cell
def _(inputs, platform, shop):
    print(shop.openlineage.show(shop.ferry.one_event(platform, inputs, "deleted")))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    With the change, all 3 tests pass. The delete's event names the test batch with the version `e622b165c27a`, the version the engineer deleted.

    </details>

    ## Capturing the ferry's lineage

    The next cell sends every event through the collector and builds the lineage graph, with the shop's reference collector and graph from Chapters 25 and 26. The jobs' events, for `build_loads` and `send_report`, are the ferry's own: you did not write them. The cell lists the graph's edges by job, with the batches counted rather than listed.
    """)
    return


@app.cell
def _(inputs, platform, shop):
    collected = shop.ferry.collect(shop.ferry.events(platform, inputs))
    graph33 = shop.ferry.graph(collected)
    shop.ferry.edges(graph33)
    return collected, graph33


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With your change to `inputs`, `load_scans` read 37 batches in 38 runs. The 37 are the 36 batches in the bucket and the test batch, which is no longer listed. The 38th run is gate 2's second upload for Tuesday's 17:30. `drop_scans` read 1 batch. `build_loads` read `boardings` and `sailings` and wrote `sailing_loads`. `send_report` read `sailing_loads` and wrote 3 report files.

    No job writes `sailings`. The timetable was typed in by hand, and nothing sends an event about it.

    The graph now holds which run read which version of each batch, and when. The question about Tuesday's 17:30 comes back below.

    ## Thursday after noon

    The first message is about Thursday's sailings after noon from the island. The next cell sets Thursday's rows of `sailing_loads` for the island beside the harbour master's own count of the people on board.
    """)
    return


@app.cell
def _(platform, shop):
    shop.ferry.compare_counts(platform, "2026-09-24", "island")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At the 09:30 sailing, `sailing_loads` has 31 and the harbour master counted 31 on board. At the 14:30 sailing, it has 14 and the harbour master counted 24. At the 19:30 sailing, it has 10 and the harbour master counted 17.

    For the two sailings after noon, `sailing_loads` counts 10 and 7 fewer than the harbour master.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide whether any run of a function or a job failed in the three days.
    """), kind="info")
    return


@app.cell
def _(collected, shop):
    shop.ferry.run_states(collected)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    Every run finished: 38 runs of `load_scans`, 1 of `drop_scans`, and 3 each of `build_loads` and `send_report`. None failed.

    Compare this with what you decided.

    </details>

    The ferry's next requirement, in the box below, is for a loss like this one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The ferry's requirement: "Alert us when a sailing's data is missing."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "a sailing's data is missing" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of the requirement</summary>

    It could mean four things:

    - no batch arrived from a gate: it needs the timetable and the list of gates. Both gates' batches arrived, so it does not catch it;
    - a batch arrived and its run failed: it needs each run's state. No run failed, so it does not;
    - a batch arrived, its run finished, and its scans did not reach `boardings`: it needs, for each run, the scans it read and the rows it wrote. It catches it;
    - a sailing carried fewer passengers than usual: it needs past loads, and a sailing that is quiet for another reason looks the same.

    The requirement does not say which it means. This page builds to the third.

    </details>

    The events of each run of `load_scans` hold its state (`state`), the scans it read (`scans_read`), the rows it wrote to `boardings` (`rows_written`), and the batch's fields (`fields`, from OpenLineage's `schema` facet).

    The next cell defines `suspect(run)`, which flags a run. As it stands, it flags a run that failed.

    Change it so that it flags a run whose scans did not reach `boardings`. Select the cell and press **Run below**.

    The check below it tests every run of `load_scans`. As `suspect` stands, 1 of 2 tests passes: it flags neither of Thursday's runs.
    """)
    return


@app.cell
def _():
    def suspect(run):
        return run["state"] == "FAIL"
    return (suspect,)


@app.cell
def _(collected, shop, suspect):
    shop.ferry.check_suspect(collected, suspect)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next cell lists every batch from the island's gate 2, with its fields as its run recorded them.
    """)
    return


@app.cell
def _(collected, shop):
    shop.ferry.fields(collected, "island", "gate-2")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From 14:31:02 on Thursday, the island's gate 2 batches hold `scan_time` where the earlier ones hold `scanned_at`. `load_scans` read 10 scans and 7 scans from them and wrote 0 rows: it keeps only scans with a `scanned_at`. That is also why a rule that flags any run that wrote fewer rows than it read scans also flags Wednesday's 12:30 from the mainland, gate 1: that batch holds one aborted scan, which the gates write with no time, and `load_scans` leaves it out on purpose.

    The fields show what changed and when. Nothing in the records shows why the gate's batches changed.

    ## Tuesday's 17:30

    The second message is about Tuesday's 17:30 from the mainland. `sailing_loads` shows 35 passengers for it, and `boardings` holds 38 rows. Gate 2 uploaded its batch for that sailing twice: 14 scans at 17:31 on Tuesday, and all 17 at 07:05 on Wednesday.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which of gate 2's two uploads the 35 counted.
    """), kind="info")
    return


@app.cell
def _(collected, platform, shop):
    shop.ferry.trace(platform, collected, "2026-09-22 mainland 17:30")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    Read the trace from the top. The row of `sailing_loads`, 35, was written by `build_loads` at 01:00 on Wednesday.

    That run counted gate 1's batch, 21 scans, and gate 2's first version, `15da88b56abc`, 14 scans.

    Gate 2's second version, `f0ff6ad37438`, with 17 scans, was loaded at 07:05:02 on Wednesday, after the run. `boardings` now holds 38.

    Compare this with what you decided.

    `build_loads` rebuilds only the day before, so no later run rebuilt Tuesday's rows. The row stays at 35 until somebody rebuilds it.

    The versions in the trace come from the inputs you wrote. Without them, the trace shows "not recorded" for each version.

    </details>

    ## The test batch

    The third message is about a test batch. At 23:40 on Wednesday, an engineer uploaded a test batch of 5 scans under Wednesday's 19:30 from the island, and `load_scans` loaded it. `build_loads` ran at 01:00 on Thursday, and `send_report` at 06:00 sent the file `loads-2026-09-23.csv`. At 08:30 the engineer deleted the batch, and `drop_scans` removed its rows from `boardings`.

    The next cell follows the graph downstream of the test batch and checks each dataset it reaches.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you read on, decide which of `boardings`, `sailing_loads` and `loads-2026-09-23.csv` still count the test scans.
    """), kind="info")
    return


@app.cell
def _(graph33, platform, shop):
    shop.ferry.made_from_test(platform, graph33)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>The printed result, explained</summary>

    `boardings` no longer counts the test scans: it holds 17 for Wednesday's 19:30 from the island, the harbour master's count. `sailing_loads` and `loads-2026-09-23.csv` still do: each shows 22.

    Compare this with what you decided.

    The delete reached only what `drop_scans` changed. The row of `sailing_loads` was built before the delete, and the report is a copy that was emailed at 06:00.

    The graph also reached the reports for Tuesday's and Thursday's sailings, `loads-2026-09-22.csv` and `loads-2026-09-24.csv`. They have no row for that sailing and do not count the test scans. Following the edges job by job reaches every file `send_report` wrote, and cannot tell those two apart from Wednesday's.

    </details>

    The ferry has a requirement for deleted batches, in the box below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    The ferry's requirement: "A deleted batch must leave no trace."
    """), kind="neutral")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    Before you open the readings below, decide what "leave no trace" means to you here.
    """), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <details><summary>Readings of the requirement</summary>

    It could mean five things. Each item says what it needs:

    - no rows made from the batch: `drop_scans` does this;
    - no figure that counted it: each figure built from it must be built again; the graph lists the datasets to look at;
    - no copy of such a figure: each copy must be found and replaced, the reports already emailed included; the graph lists the files, not the inboxes they were sent to;
    - no copy of the batch itself: object storage keeps every version, so the test batch's version `e622b165c27a` is still in the bucket behind the delete marker; each version must be removed;
    - no record that the batch ever existed: this would remove the events and edges that explain why Wednesday's 19:30 showed 22, and the version the delete removed.

    The last reading works against the second and the third: finding every figure the batch reached needs the lineage that the last reading would remove.

    The ferry's platform meets the first reading only. The requirement does not say which it means.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The ferry's three days

    The ferry's platform recorded its triggers, its function runs and its job runs, and nothing that linked a figure to the batches it counted. Your inputs added that link, version by version.

    Thursday's loss after noon failed no run. The runs' own counts showed it, and the batches' fields showed what changed.

    Tuesday's row counted gate 2's first version, and no later run rebuilt Tuesday.

    The delete removed the test batch's rows, and not the figure or the report built from them.

    The records could not show why the gate's batches changed, who read the emailed report, or what anybody did with it.

    The course ends here.

    Four questions:

    - On a platform you work on, which record links a figure to the version of the data it counted?
    - Which of your jobs rebuild only the latest day, and what happens to a correction that arrives later?
    - When data must be deleted, which copies of what was made from it does your platform know about?
    - Pick a requirement your platform is said to meet. Which reading of it does the platform meet, and which does it not?

    ### How this differs from a real platform

    - The ferry, its platform and its three days are invented. No real object store, function platform or scheduler is described: when a change starts a function, and what each system records, are the ferry's own.
    - Here each change to a batch starts its function once, in order. Chapters 19 and 20 showed what happens when a start is repeated or out of order.
    - The facets `version`, `schema`, `inputStatistics`, `outputStatistics` and `lifecycleStateChange` are OpenLineage's. `ferry_batchChange` is the ferry's own.
    - Naming the removed version as the input of a run that reads nothing, and recording the change that started a function in `ferry_batchChange` rather than in `lifecycleStateChange`, are the ferry's choices.

    [Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 32](chapter_32.ipynb)

    ---

    Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import shop
    from shop import figures
    return figures, mo, shop


if __name__ == "__main__":
    app.run()
