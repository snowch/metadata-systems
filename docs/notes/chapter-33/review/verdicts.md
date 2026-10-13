# VERDICTS ON THE CHAPTER 33 FINDINGS

7 upheld, 5 partly upheld, 1 rejected (13 findings: B1 to B4, S1 to S9). The COULD items are dealt with at the end and are not counted.

I read the brief, CLAUDE.md, AGENTS.md, `notebook/chapter_33.py`, the as-built file, the notes, `docs/notes/part-8/design.md`, `notebook/shop/ferry.py`, `notebook/shop/figures.py`, `docs/sources.md` and the neighbouring chapters (2, 16, 28, 32). I ran the engine from `/home/user/metadata-systems/notebook`. I wrote no file.

Warning: `shop/ferry.py` changed at 07:14 while I worked, and the as-built file predates it. The check messages for `inputs` are now different (see S2). Anything that pins or prints the old message needs a re-check.

## BLOCKING

**B1. UPHELD.**
- I read `FERRY_FLOWS` and the caption in `figures.py` and `chapter_33.py` line 69.
- The caption says the platform records "not what a function or a job writes". Two flow labels say "what they write is not recorded" and "reads and writes not recorded".
- Section 1 then asks the learner to "look for a record that links a run of `build_loads`" to its batches. Its answer is "No record links…". The figure states that answer before the learner has looked.
- This breaks CLAUDE.md's rule that no caption or label gives away an exercise's answer, and its "no arrow, not an announcement" standing example.
- Chapter 2's flow label is "unseen jobs move data each night", and its caption is plain: "three systems and what each holds". Neither states what is recorded.
- The notes call the labels "the standing map's rule". They go further than that rule.
- The fix must keep the caption and flow labels to what exists: the systems, their parts, the counts, and perhaps "a change starts a function".
- The instrument cells should carry the absence.
- Fix the notes line (`chapter-33.md` line 43) too. It describes the old labels.
- The labels are Haiku-drafted, so the replacements go through the fact-brief process.

**B2. UPHELD.**
- Section 1 says "From the times you can work out that Wednesday's 01:00 run counted gate 2's first version." That answers the Tuesday prediction ("which of gate 2's two uploads the 35 counted") before it exists.
- It also makes the notes' "Predictable: yes, from the times" empty.
- The fix must keep Chapter 2's point, that a reconstruction from times is not a record. It must stop saying which version was counted.
- Say only that the times might support an inference. Let the later prediction and the trace settle it.

**B3. PARTLY UPHELD.**
- I ran `ferry.downstream(graph, test batch)`. It returns 5 datasets: the three reports (`loads-2026-09-22.csv`, `-23`, `-24`), `boardings` and `sailing_loads`.
- `made_from_test` silently skips the Tuesday and Thursday reports with `continue`, because they have no line for that sailing. The page says the cell "checks each dataset it reaches" but shows 3 rows.
- "The graph lists them" and "the graph lists the files" therefore overclaim, and the learner never learns the graph reaches more than it counts. That stands.
- Chapter 16 already taught that dataset lineage lists datasets that did not change, so the one-sentence fix fits.
- Part of the finding does not stand. The reviewer says the graph holds no times or versions. In fact the graph edges carry run sets and `first`/`last` times (checked on a graph key). The page itself says "which run read which version… and when".
- The real cause is that `downstream` follows jobs, not runs.
- The fix must state that the graph also reaches the other two reports, which have no line for that sailing and do not count the test scans. It must also say that following edges by job cannot separate them.
- Printing the extra rows is optional. The prediction names three datasets, and a "no line" value would break the yes/no column. A sentence is enough.
- With that sentence, "reached all three" and "the graph lists them" become accurate.

**B4. UPHELD.**
- I confirmed it. After the delete, `storage.exists(uri)` is False.
- But `storage.versions(uri)` still lists `e622b165c27a`, then the delete marker `3bebca4eb852`.
- `version_text(uri, 'e622b165c27a')` returns the five TEST scans.
- The page's own platform table says storage keeps "every version, with a marker where one was deleted".
- "The batch is gone" and the four readings never mention that the content survives in the bucket. A learner who has just read the table will write exactly that reading.
- The fix is a fifth reading: no copy of the batch's content left in storage, which needs each version removed. "Four things" becomes five.
- "The batch is gone" needs a small qualification, for example "not listed".
- The requirement should then say which readings the ferry's platform meets. `drop_scans` meets only the first; the others are not met.
- That is Question the requirement's step 5. Chapter 32 ("meets none of the three") and Chapter 28 both do it. This is the same fix as S9.

## SHOULD

**S1. PARTLY UPHELD.**
- Confirmed by running:
  - `rows_written < scans_read` gives test 2 "Also flagged: Wednesday's 12:30 from the mainland, gate 1".
  - That batch read 13 scans and wrote 12.
  - `scans_read > 0 and rows_written == 0` passes both tests.
- Standing part: the paragraph after the check pre-announces the trap. It names the aborted scan and says `load_scans` "leaves such a scan out on purpose". The notes' intended evidence is "then Wednesday's aborted scan flagged too".
- That paragraph also hands over the filter mechanism before the `fields` cell, and the `fields` cell says it again.
- "Change `suspect` until both tests pass" repeats the instruction above it.
- The fix must let the check output carry the discovery. Move the aborted-scan explanation to after the learner has had the check, in practice next to the `fields` paragraph, and drop the repeated instruction.
- Rejected part: rewording check line 1. A test must name its target, and it is only a check line. The "where" step is carried by `compare_counts` (the sailings) and the `fields` cell.
- Optional: "whose scans did not reach `boardings`" is ambiguous (any scan or all). The check settles it, which fits the course.
- Tied to this paragraph: "the gates write no `scanned_at`" is wrong. The engine writes `"scanned_at": null`. Say "no time".

**S2. REJECTED, as already handled.**
- The messages the reviewer criticises are gone from the current `ferry.py`. It now has `versions_batch`, `versions_none` and `versions_wrong`.
- I ran four wrong attempts through the current code:
  - A (no facet) and B (`version` at the top level) both give "…name no version of the batch they read: a version goes in the batch's `facets`, as `"version": shop.ferry.version_facet(...)`".
  - C (name is `key@version`) gives "name no input with the batch's bucket and key".
  - D (wrong `previous` on an overwrite) gives "1 of 38 runs… name a version, but not the one they read, `change["version"]`".
- The facet placement is shown, and "no version", "wrong version" and "wrong batch" are separate.
- Remaining nit, not worth acting on: for a delete in case C the line says "names nothing".
- The as-built text and any test that pins the old message are stale. Re-run the tests and rebuild the as-built file.

**S3. PARTLY UPHELD.**
- Verified: the report line for Wednesday's `island 19:30` is 22, and the harbour master's count is 17. Wednesday's 17 comes from 9 + 8.
- Thursday's 19:30 count is also 17, so the coincidence is real.
- Standing part: the table's "yes" for `sailing_loads` and the report is an inference from 22 against 17, and no cell shows either number. The learner has to trust it, and that is the independent evidence.
- The fix must put the figure and the harbour count beside each dataset's yes/no, or in the cell.
- Not worth acting on:
  - The test batch of 5 scans, `boardings`' `batch` column and "both gates' batches arrived" are scenario facts, pinned by tests, like the rest of the setup prose.
  - The aborted batch is dealt with in S1.

**S4. UPHELD.**
- I checked: the figure's "36 batches" is `len(storage.ls)`, after the test batch was deleted. The graph's 37 is those 36 plus the test batch.
- 38 runs is 37 batches plus gate 2's second upload of Tuesday's 17:30.
- The page never reconciles them, and a reader who multiplies 3 days × 6 sailings × 2 gates will count 36.
- One clause after the edges table is enough. The log in section 1 already shows the double upload, so naming it there gives nothing away.

**S5. PARTLY UPHELD.**
- Upheld: "the shop's versions of the pieces you wrote in Chapters 25 and 26" uses *version* for something else. CLAUDE.md lists *version* among the two-meaning words. Chapters 25 and 26 are the collector and the graph, so name them.
- Upheld: the printed event shows `ferry_batchChange` before the paragraph that explains it. Move the `lifecycleStateChange` and `ferry_batchChange` paragraph above the event cell, or add a clause before it.
- Rejected: "run" as verb and noun is used throughout the course and is unambiguous here.

**S6. PARTLY UPHELD.**
- Upheld: the figure and "The figure below shows the ferry's four systems" come before "You have joined the data team…".
- It shows `load_scans` and `sailing_loads` before any of them is introduced. Chapter 2's opening, the standing example, puts a short situation first and the map after.
- The fix is to put the short situation first and the figure after it.
- Rejected: the duplication complaint. The figure is the architecture reference, and the table is the instrument whose "records" column carries the question. Dropping either costs more than the overlap.

**S7. UPHELD (small).**
- `design.md` says "The jobs' events are the ferry's own and are given". The page never says so.
- The page says only that the function platform builds the function events.
- The edges table then shows `build_loads` and `send_report` reading and writing, which the reader never instrumented.
- One clause where the events are first collected is enough: the jobs' events are sent by the ferry and are not the reader's code.

**S8. UPHELD.**
- `docs/sources.md` lines 671 to 677 support only that `lifecycleStateChange` captures "the lifecycle states of the Dataset", shown on an output. "It describes a change a run makes to a dataset" is not in the source.
- The sources file itself says "The chapter says…", so this is the course's gloss, not the specification's.
- The fix must keep the specification claim to what the source supports.
- The ferry's reasoning for using its own facet becomes labelled as the ferry's choice. Add it to the model-versus-reality bullet beside the removed-version choice, and fix the sources entry.

**S9. UPHELD.**
- Objective 6 says "before building to them". Nothing is built to the third requirement, and the page never says what the platform meets (see B4).
- The fix must do two things:
  - Close the third requirement with what the ferry's platform meets.
  - Add one closing question that carries the habit to the reader's own work, for example about which reading of a requirement their platform meets.
- Also adjust the objective's wording to match what the page does.

## COULD

- Accept (trivial wording): "afternoon sailings" includes the 19:30, which is evening, so say "after noon". "The question above needs this one" is ambiguous, so name the Tuesday 17:30 question.
- Accept: "no `scanned_at`" becomes "no time" (see S1).
- Reject:
  - Message 3 nearly answering the prediction. It only states the premise, the effect of the test batch.
  - "Your inputs added that link" as personification, a very mild case.
  - The closing limits sentence ("who read the emailed report…"), which is true by construction.
  - A model-versus-reality line about storage versioning being a setting. The first bullet already says what each system records is the ferry's own.
  - Items 7 and 8 under COULD, which the reviewer already accepted.
