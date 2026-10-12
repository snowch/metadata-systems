# VERDICTS ON THE CHAPTER 18 FINDINGS

7 upheld, 9 partly upheld, 3 rejected (19 findings: B1 to B3, S1 to S9, C1 to C7).

What I ran or read: `findings.md`, the as-built chapter, `notebook/chapter_18.py`, `docs/notes/chapter-18.md`, and `shop/delivery.py`. I also read Chapters 8, 9, 10, 13, 14, 16 and 17, `docs/style.md` rule 24, `docs/sources.md` (Part V and the run-cycle lines), `docs/plan.md` and the Chapter 18 pins in `tests/test_words.py`. In `/home/user/metadata-systems/notebook` I ran `shop.run_week(["returns"])`, `delivery.send` with `lose=`, `lose_ack=` and `at_least_once=`, `retried()`, `open_runs`, `ingest.edges(...).of(...)`, the `daily_sales` queries, and the raw `remove_return` events.

## BLOCKING

**B1. UPHELD.**
- Checked: the event time is 16:50:04, the first sending is at 16:50:05, the second at 16:50:35, and the receipt at 16:50:37. The receipt is 32 s after the first sending, not 30. The table's "event" column shows 16:50:04, so a learner can work out the sending times from the 1 s lag.
- The fix must state the 30 seconds as the wait between the two sendings, with the sending times or enough to derive them, so the sentence is true and checkable. The table needs no change.
- `tests/test_words.py` line 1160 pins the wrong sentence and must change with it.

**B2. UPHELD.**
- Checked: Chapter 9 (line 34) says "Now the analyst's script sends its own events, each night". Chapter 16 (line 95) says the script "sends events (Chapters 6 and 9)". Chapter 13 (line 309) says the export sends none.
- The "(Chapter 8)" citation is stale, because Chapter 8's line was true only before Chapter 9.
- In this week (`["returns"]`) there is no analyst copy run at all. The writers are the nightly jobs, `export`, `record_return` and `remove_return`.
- The fix must name only the program that sends nothing now, the export (Chapter 13), and drop the analyst's copy and the Chapter 8 pointer. The "not met" verdict still stands, because the export touches the data.
- `docs/notes/chapter-18.md`, Requirements items 3 and 5, repeats the stale claim and must be fixed too.
- The reflection question is generic and can stay.

**B3. PARTLY UPHELD.**
- Stands: "met with at least once, as long as each program sends its events at all" overclaims. Retrying needs a live program that still holds the event. A program that stops before it sends its terminal event, and a run that is still going, leave a run open under any delivery. The notes already say this ("a run lost before it sends anything leaves nothing to find") and the page dropped it. Reading 3 is the place for it.
- Does not stand: the Chapter 10 point (unrecorded reads such as the SQL function's) is another subject. This chapter is about lost events, and I would not add it.
- The fix must say, in a clause or sentence, what at least once does not cover: a program that stops before sending, and a run that has not ended. State it as scope, not as a slogan.

## SHOULD

**S1. PARTLY UPHELD.**
- Checked: Chapter 9 (lines 224-226, 318) shows `writes` in "6 runs, not 7" and the edge staying "because other runs had it". It also says the stored record is "the same stored record as a run still working". The prediction's answer is recallable.
- The fix is one clause tying the prediction to Chapter 9 and naming what is new: here the event is lost in the path and the line was not cut short at the source. Do not redesign the prediction. It is a fair belief to test, and the next question (lost or still running?) is new.
- Rejected part: the Wednesday 9 and Thursday 10 confusion. Different weeks and different runs, and the page already says the Thursday run writes Wednesday's row.

**S2. PARTLY UPHELD.**
- Stands: "Other evidence can tell them apart" is vague. The page also presents 369000 s against a usual 21 s without saying what it does and does not establish. It makes a lost event likely and proves nothing, and the closing question rightly asks how to tell them apart.
- Does not stand as an error: "the events cannot tell" is literally true. A START and nothing after it is identical in both cases. Keep the claim and scope it.
- The fix must say what the usual-time column suggests (likely lost, not proved), and name the other evidence. This merges with S3 and C5's personification point ("the collector's events cannot tell").

**S3. PARTLY UPHELD.**
- Checked: `daily_sales` gets exactly one row per run (rows=1 each night), and the Thursday 10 run writes the day-before row, so the attribution is sound. The result shows only `day` and `revenue_pence`, with no write time.
- Stands: "The run did its work. Only its `COMPLETE` is missing." is an inference stated as an observation. The row shows the write happened, not how the run ended (a run could write and then fail, or send a lost `FAIL`).
- The fix must say what the row shows (the write happened, one row per run) and what it does not (that the run ended). The summary's "The warehouse's row could tell them apart" needs the same scoping.

**S4. PARTLY UPHELD.**
- Checked: the `remove_return` START and COMPLETE both carry `shop_objectChange` naming `s3://shop-returns/r-203.json` with change `deleted`. Only inputs and outputs are empty in the START. `found_once.of("shop/remove_return")` is empty.
- `record_return` still has a `writes` edge to `returns` (5 runs), so the graph credits `returns` to `record_return` alone.
- Stands: "The dependency is real, and it cannot be shown" is a slogan, and it is too broad.
- Does not stand: "nothing the collector holds shows that `remove_return` writes `returns`" is literally true, because the facet names the object, not the table.
- The fix must scope the claim to the graph (no edge), say what the START does carry, and drop the slogan. One sentence on the consequence, that the graph now credits `returns` to `record_return` alone, is welcome but optional.

**S5. UPHELD.**
- Checked: the result of the `lose_ack` run (received twice, at 16:50:07 and 16:50:37) is stated in the paragraph straight after the instruction to make the change. The notes call this an experiment whose prompt "asks how many times", and the page has no such prompt. This is also the chapter's designed surprise.
- The fix must give the learner a prediction before the `lose_ack` change, in the chapter's free-text cell form. It should ask for a result, how many times the `COMPLETE` arrives with the acknowledgement lost. No option or prompt may carry the explanation.
- Keep the result paragraph after the run.
- Correct the notes, which say the learner changes `at_least_once` (the cell already sets it).

**S6. PARTLY UPHELD.**
- Stands:
  - "Instrumented" appears in no earlier chapter (grep) and is jargon. Use plain words.
  - The section lacks "Compare these with what you wrote.", which Chapters 13, 14, 15, 16 and 17 all have after their readings.
  - Readings 1 and 3 read as overlapping. The B3 fix separates them: reading 1 is arrival of what was sent, and reading 3 is a run having an end, which also needs a program that sends and a run that has finished.
- Rejected: adding new readings ("complete for a stretch of time", "for the question asked"). `docs/plan.md` fixes the candidate as the programs that send events versus every program that touches the data. A fourth and fifth reading is scope growth the chapter does not need.

**S7. UPHELD (small).**
- The sentence defining runs with a START and no end does not name them. Introduce "open run" there, once, before the cell lists "one open run". Later uses ("left one run open") then work.

**S8. REJECTED.**
- The sentence "The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them." is identical in Chapters 14 to 23. It is a convention every chapter keeps, not a Chapter 18 fault.
- A path figure is not needed. The timings are four numbers (1 s, 2 s, 30 s, and the acknowledgement), and a sentence of arithmetic (the B1 fix) carries them.
- The only change is in the notes: their "Serves: where the programs and the collector sit" is not what the standing map does. Make the notes describe the figure as the standing map.

**S9. UPHELD (trivial).**
- "A lost `COMPLETE` left every edge in the graph" needs its scope: the one lost from `build_daily_sales`, which had other runs.
- The same summary also carries the S3 and S2 overclaims about the warehouse row, so fix them together.

## COULD

**C1. UPHELD.**
- Checked: Chapter 9 counts "four jobs and the two functions", and the map caption separates jobs from functions. `remove_return` is a function.
- Change the heading "A job that ran once" and "the job has no other run to compare with" to "function". Leave the engine's `job` table column alone.

**C2. REJECTED.**
- The learner changes only `lose` to `lose_ack`, never the log spec, so the "job TYPE date" form need not be taught.
- 09:00 on Monday 14 is the moment the listing is made, and the prose already says "at 09:00 on Monday 14".

**C3. PARTLY UPHELD (optional).**
- Checked: `docs/sources.md` line 66-67 supports it: STREAMING and SERVICE jobs have "No expected terminal event under normal operation".
- One bullet in the model-versus-reality list would sharpen the point that an open run can be normal, and it sits well beside "How would you tell a slow run from a lost event?". Do not expand beyond one bullet, and cite the source.

**C4. REJECTED.**
- "Real producers' retries are usually capped or buffered" has no source in `docs/sources.md`, and adding it would be inventing behaviour. The timings are already introduced as "In the shop".

**C5. PARTLY UPHELD.**
- Stands:
  - "The collector's events cannot tell" personifies (fixed with S2).
  - "Its usual time is empty" should use the column's name, `usual seconds`, which is `None` in the engine.
  - The earlier "Chapter 19 takes up the event that arrives twice" duplicates the closing's forward reference to Chapter 19 (style rule 24). Drop the earlier one, because the closing section carries the required next-chapter naming.
- Rejected:
  - "The head of the shop's requirement" is the house pattern.
  - The two lists differ in shape because they serve different jobs. Chapter 17 does the same.

**C6. PARTLY UPHELD (cross-part).**
- Checked: the "Time and memory" text is identical in Chapters 15 to 23. `test_jupyterlite.py` pins measurements for Chapters 3 to 17 only, so "measured on a computer" is unsupported for Chapter 18.
- This is one decision for Chapters 18 to 23: measure and pin them, or reword the claim. Do not patch only Chapter 18.

**C7. UPHELD.**
- Checked: the notes describe options ("the same edges, an edge gone, no job") while the page uses a free-text cell, the same as Chapters 13 to 17. Update the notes' "Gives nothing away" and "action" lines to match the page, including any prediction added for S5.

## Summary of the page fixes that matter
B1 (wrong time and its pin), B2 (stale claim about programs), B3 (scope of at-least-once), the S2/S3/S4/S9 scoping of what the events and the row show, S5 (a prediction before `lose_ack`), S6 (plain word and "Compare these with what you wrote"), S7, C1 and C5. Notes fixes: S8, C7 and B2.
