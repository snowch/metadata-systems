# Revision brief P33: Chapter 33, Build the whole thing

Read `rev-common.md` first, then `common.md` (every rule there still holds). The first draft is
`docs/notes/part-8/drafts/P33.md`. Redraft these slots: A, B, MAP, CAPTION, FLOWS, D, F, G, H, I, L,
M, N, P, R, Z. Terms: none new.

The page's order changes at the start: B (the situation and the messages) now comes before MAP and
the figure, and MAP is followed by the figure and then the cell that lists the ferry's systems.

Say "after noon" for Thursday's 14:30 and 19:30 from the island, never "afternoon". Never use
"version" for anything but a batch's version.

## A

A list of six objectives. Keep the first five as in the first draft. The sixth: question three of
the ferry's requirements, and say which reading the platform meets.

## B

- Keep the heading `### The ferry's platform`.
- Keep the first draft's four paragraphs about the ferry, its gates and batches, its two functions
  and its two jobs, as they are.
- Keep the sentence introducing the messages, and the three messages, but the first message reads:
  "Thursday's sailings after noon from the island look nearly empty. The harbour master counted far
  more people on board."
- Do not end with a sentence about the next cell.

## MAP

- The figure below shows the ferry's four systems on Friday 25 at 09:00.
- The cell after it runs the ferry's three days and lists its systems, with what each records about
  its own work.

## CAPTION

One line, with no double quotation marks: the ferry's four systems on Friday 25 at 09:00; object
storage holds 36 batches and 3 reports. Say nothing about what the platform records.

## FLOWS

Three labels, one per line, each under 32 characters, in lower case, no full stop. Each says only
what the page has told the reader: between object storage and the functions, a change to a batch
starts a function; between the functions and the warehouse, the functions write to tables; between
the warehouse and the scheduler, the jobs run at set times.

## D

- Keep: "The log lists 3 runs of `load_scans` on that sailing's batches: gate 1's batch at 17:31:02 on Tuesday, gate 2's at 17:31:02, and gate 2's again at 07:05:02 on Wednesday, each with its version."
- Keep: "`build_loads` ran at 01:00 on Wednesday, Thursday and Friday."
- Keep: "No record links a run of `build_loads` to a batch or a version."
- The times might let you work out which version a run counted. That would be a reconstruction, as
  in Chapter 2, not a record. (Do not say which version.)
- Keep the heading `### What to record`.
- The ferry's data team has a requirement for lineage, in the box below.

## F

- Keep the first draft's readings list, but end its third item with: "The question about Tuesday's
  17:30 above needs this one." in place of "The question above needs this one."
- Keep the rest of the first draft's F as it is, up to and including "`shop.ferry.version_facet(version)` makes the `version` facet. Select the cell and press **Run below**."
- In the paragraph about `drop_scans`, say the batch is no longer listed in the bucket, in place of
  "the batch is gone".
- Then a new paragraph: the event the cell after the check prints holds the facet
  `ferry_batchChange`, with the change that started the function. OpenLineage has a dataset facet,
  `lifecycleStateChange`, whose values include `CREATE`, `OVERWRITE` and `DROP`; its documentation
  shows it on a run's output. Recording the change that started a function in a facet of its own is
  the ferry's choice.
- Keep: "The check below it tests every function run of the three days. As `inputs` stands, 1 of 3 tests passes. The cell after the check prints the event of the run that the delete of the test batch started."

## G

- Keep: "With the change, all 3 tests pass. The delete's event names the test batch with the version `e622b165c27a`, the version the engineer deleted."
- Keep the heading `### Capturing the ferry's lineage`.
- The next cell sends every event through the collector and builds the lineage graph, with the
  shop's reference collector and graph from Chapters 25 and 26. The jobs' events, for `build_loads`
  and `send_report`, are the ferry's own: you did not write them. The cell lists the graph's edges by
  job, with the batches counted rather than listed.

## H

- Keep: "With your change to `inputs`, `load_scans` read 37 batches in 38 runs."
- The 37 are the 36 batches in the bucket and the test batch, which is no longer listed. The 38th run
  is gate 2's second upload for Tuesday's 17:30.
- Keep: "`drop_scans` read 1 batch. `build_loads` read `boardings` and `sailings` and wrote `sailing_loads`. `send_report` read `sailing_loads` and wrote 3 report files."
- Keep the first draft's two sentences about `sailings` and the sentence "The graph now holds which
  run read which version of each batch, and when. The question about Tuesday's 17:30 comes back
  below."
- The heading `### Thursday after noon`.
- The first message is about Thursday's sailings after noon from the island. The next cell sets
  Thursday's rows of `sailing_loads` for the island beside the harbour master's own count of the
  people on board.

## I

- Keep the first draft's sentence about the three sailings' counts (31 and 31; 14 and 24; 10 and 17).
- Keep: "`sailing_loads` counts 10 and 7 fewer than the harbour master." and begin that sentence with
  "For the two sailings after noon,".
- Keep the last sentence (the prediction prompt) as in the first draft.

## L

- Keep the first draft's L as it is, but for "a batch arrived, its run finished, and its scans did
  not reach `boardings`" keep the same words.

## M

- Change `suspect` until it flags Thursday's two runs and no other, as the check below it asks.
- The next cell lists every batch from the island's gate 2, with its fields as its run recorded them.

## N

- Keep: "From 14:31:02 on Thursday, the island's gate 2 batches hold `scan_time` where the earlier ones hold `scanned_at`. `load_scans` read 10 scans and 7 scans from them and wrote 0 rows: it keeps only scans with a `scanned_at`."
- That is also why a rule that flags any run that wrote fewer rows than it read scans also flags
  Wednesday's 12:30 from the mainland, gate 1: that batch holds one aborted scan, which the gates
  write with no time, and `load_scans` leaves it out on purpose.
- Keep: "The fields show what changed and when. Nothing in the records shows why the gate's batches changed."
- Keep the heading `### Tuesday's 17:30`, and the rest of the first draft's N after it, as it is.

## P

- `boardings` no longer counts the test scans: it holds 17 for Wednesday's 19:30 from the island, the
  harbour master's count. `sailing_loads` and `loads-2026-09-23.csv` still do: each shows 22.
- Compare this with what you wrote.
- Keep: "The delete reached only what `drop_scans` changed. The row of `sailing_loads` was built before the delete, and the report is a copy that was emailed at 06:00."
- The graph also reached the reports for Tuesday's and Thursday's sailings, `loads-2026-09-22.csv`
  and `loads-2026-09-24.csv`. They have no row for that sailing and do not count the test scans.
  Following the edges job by job reaches every file `send_report` wrote, and cannot tell those two
  apart from Wednesday's.
- The ferry has a requirement for deleted batches, in the box below.

## R

- It could mean five things. Each item says what it needs (a list):
  - no rows made from the batch: `drop_scans` does this;
  - no figure that counted it: each figure built from it must be built again; the graph lists the
    datasets to look at;
  - no copy of such a figure: each copy must be found and replaced, the reports already emailed
    included; the graph lists the files, not the inboxes they were sent to;
  - no copy of the batch itself: object storage keeps every version, so the test batch's version
    `e622b165c27a` is still in the bucket behind the delete marker; each version must be removed;
  - no record that the batch ever existed: this would remove the events and edges that explain why
    Wednesday's 19:30 showed 22, and the version the delete removed.
- The last reading works against the second and the third: finding every figure the batch reached
  needs the lineage that the last reading would remove.
- The ferry's platform meets the first reading only. The requirement does not say which it means.

## Z

- Keep the heading `### The ferry's three days`, and the first draft's six paragraphs from "The
  ferry's platform recorded its triggers" to "The course ends here.", but say "Thursday's loss after
  noon" for "Thursday's loss".
- Three questions become four (a list, after the same short line):
  - keep the first draft's three questions;
  - the fourth: pick a requirement your platform is said to meet; which reading of it does the
    platform meet, and which does it not?
- Keep the heading `### How this differs from a real platform`, and the first draft's list, but its
  last item reads: naming the removed version as the input of a run that reads nothing, and
  recording the change that started a function in `ferry_batchChange` rather than in
  `lifecycleStateChange`, are the ferry's choices.
