(A reviewer on another model, reading as a learner who has done Chapters 1 to 17; returned as text and saved here.)

# REVIEW OF CHAPTER 18, "Missing events"

Numbers checked: I ran every cell's call from `/home/user/metadata-systems/notebook` (`shop.run_week(["returns"])`, `delivery.send` with each `lose=`, `lose_ack=` and `at_least_once=`, `ingest.edges(...).of(...)`, `delivery.open_runs`, the `daily_sales` query). I printed the raw events of `remove_return`, `record_return` and `build_daily_sales`, and read `shop/delivery.py`, `shop/week.py` and `tests/test_words.py` (lines about 1145-1165).

The following all match the engine: 68 sent, 68 received, 0 lost; `writes` 6 runs and `reads` 7; open run `build_daily_sales` 2026-09-10T02:30:00Z, 369000 s, usual 21 s; 15375 pence for 9 September; `remove_return` with no edge and its open run 16:50:02 with an empty usual time; sent twice and received once at 16:50:37; with `lose_ack`, received at 16:50:07 and 16:50:37. The weekdays are right (10 Sept is Thursday, 12 is Saturday, 14 is Monday), and 369000 s is more than four days. One stated number is wrong (finding B1).

I also read the as-built chapter, the chapter's notes, `chapter_08.py`, `chapter_09.py`, `chapter_10.py`, `chapter_16.py`, `chapter_17.py`, and the Part V parts of `docs/sources.md`.

## BLOCKING

**B1. A stated time is wrong.**
- Quote: "The receipt was at 16:50:37 on Saturday 12, 30 seconds after the first sending."
- Engine: the event time is 16:50:04 and the first sending is at 16:50:05. The second sending is at 16:50:35, 30 s later, and the receipt is at 16:50:37. So the receipt is 32 s after the first sending. It is 30 s after the receipt the first sending would have had (16:50:07).
- The page's table shows only the arrival times, so the learner cannot check the sentence.
- `tests/test_words.py` pins this sentence as text only (the receipt time is asserted separately), so the test does not catch it.
- Direction: say 30 seconds is the wait before the second sending, or state the sending time. Better still, make the table show the sent times so the claim is checkable.

**B2. "The export and the analyst's copy send no events" contradicts later chapters.**
- Quote: "Every program: not met. The export and the analyst's copy send no events (Chapter 8)."
- Chapter 9 says "Now the analyst's script sends its own events, each night." Chapter 16 says the script "sends events (Chapters 6 and 9)". Only the export still sends nothing (Chapter 13 confirms).
- A reader at Chapter 18 has seen the analyst's script send events for nine chapters. The sentence is also not true of this week, which has no `source` change and shows no analyst's copy.
- Direction: restate which programs send nothing now. The reflection question "Which of your platform's programs send no events at all?" depends on the same fact.

**B3. The third reading's verdict overclaims.**
- Quote: "Every run's end: met with at least once, as long as each program sends its events at all."
- At least once only helps a program that is still alive to resend. A program that dies before it sends its terminal event leaves a run open however the path behaves. The chapter's own notes say so ("a run lost before it sends anything leaves nothing to find"), but the page dropped it.
- A run still going also has no end.
- Reading 3 is "end and edges are known", but the verdict addresses only the end. Chapter 10 records reads that no event carries, for example the SQL function's read of `returns`.
- Direction: say what at least once does not cover, since this is the exercise's conclusion.

## SHOULD

**S1. The first prediction repeats Chapter 9, and the page never says so.**
- Quote: "Before you read on, write in the next cell what the graph will show for `build_daily_sales` when that `COMPLETE` never arrives".
- Chapter 9 (line 318) already showed "It writes `daily_sales` in 6 runs, not 7 … Its `START` named its input, so its read is counted." Chapter 9 (lines 224-226) already said the stored record "is the same stored record as a run still working". Chapter 8 (line 190) said the same.
- Here the cause is a lost event rather than a cut-short line, and the run is Thursday 10 rather than Wednesday 9. The page does not connect the two.
- A learner who remembers Chapter 9 recalls the answer rather than predicting it. One who does not has the pieces on the page: the 7 and 7, and "A run reports its outputs in its `COMPLETE`".
- Direction: point to Chapter 9 and say what is new (a lost event against a refused line), or build the prediction on the new part.
- Related: Chapter 9 used Wednesday 9 and this chapter uses Thursday 10, and the Wednesday-9 row is queried here. This invites confusion.

**S2. "Cannot tell" is stronger than the evidence.**
- Quote: "The collector's events cannot tell a lost `COMPLETE` from a run that is still running."
- Just above, the page shows 369000 s open against a usual 21 s, and the closing question asks "How would you tell a slow run from a lost event?". The events do give strong evidence, though not proof. The same applies to the objective "Find the runs that started and never ended", since the page can only show runs with no end received.
- Direction: say what the usual-time column does and does not establish.
- "Other evidence can tell them apart" is also vague. Name the evidence.

**S3. The warehouse row is presented as proof.**
- Quote: "The row is there: 15375 pence for Wednesday 9. The run did its work. Only its `COMPLETE` is missing."
- A row shows a write happened. It does not show how the run ended: a run could write and then fail, or send a FAIL that is lost. This is the observation-against-inference distinction the course asks for.
- The engine appends one day per run, so the row is attributable to Thursday's run. The page never says the table is append-only, so the attribution is not in front of the learner.
- Direction: state the append fact, and say what the row shows and what it does not.

**S4. "Nothing the collector holds shows…" is too broad, and "Its START names no dataset" is only half true.**
- Quote: "With its one `COMPLETE` lost, nothing the collector holds shows that `remove_return` writes `returns`. The dependency is real, and it cannot be shown."
- Both the `START` and the `COMPLETE` of `remove_return` carry the `shop_objectChange` facet naming `s3://shop-returns/r-203.json` with change `deleted`. Only `inputs` and `outputs` are empty in the START.
- What is missing is the job-level `writes` edge in the graph, not every trace.
- `returns` also still has an upstream edge from `record_return`. The graph now credits `returns` to `record_return` alone, which is the more telling consequence and goes unmentioned.
- "The dependency is real, and it cannot be shown" is a slogan-shaped line (AGENTS rules 1 and 3).
- Direction: scope the claim to the graph, and say what the START does carry.

**S5. The at-least-once result is told before it is run, with no prediction.**
- Quote: "Now change `lose=` to `lose_ack=` in the cell, select it, and press **Run below**. The `COMPLETE` then arrives, and its acknowledgement is lost."
- The next paragraph states the result, so a learner who reads on never needs to run it.
- The notes say the figure's prompt "asks how many times" and that the learner changes "`at_least_once` and `lose_ack`". The page has no such prompt, and the cell already sets `at_least_once`.
- Direction: either ask for the count of receipts before the run, or keep the prose and drop the experiment framing in the notes.

**S6. The three readings are not three different needs.**
- Quote: "Every event a program sends arrives. It needs delivery at least once, or no loss." and "Every run's end and edges are known. It needs a `COMPLETE`, `ABORT` or `FAIL` for each run."
- With programs that send, readings 1 and 3 need the same thing: the terminal event arrives. The verdict for reading 3 even repeats the condition from reading 2 ("as long as each program sends its events at all").
- Meanings the chapter has evidence for are missing: complete for a stretch of time (a run in progress is not complete yet), and complete for the question asked (an asset or column).
- Reading 3 joins two things, the end and the edges.
- "Instrumented" is new jargon and appears in no earlier chapter.
- Direction: make the readings distinct, and keep them in one shape.
- The Chapter 17 pattern ends its readings with "Compare these with what you wrote". This chapter has no equivalent after its readings.

**S7. "Open run" is used without being defined.**
- Quote: "The cell lists one open run: `build_daily_sales`".
- The earlier sentence describes a START with no end but never gives the thing a name. "Open" appears again in the closing summary ("left one run open") and in `open_runs`.
- Direction: name it where the cell first lists them.

**S8. The platform map does not carry what the notes say it carries.**
- Quote: "The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them."
- The notes give its job as "where the programs and the collector sit". The figure is the Chapter 15-17 map, with no collector and no path.
- The new model (send +1 s, receive +2 s, wait 30 s, acknowledgement) is carried in prose. CLAUDE.md says a figure should carry what prose would make the learner hold in mind.
- Direction: add a path figure, or fix the notes. The sentence is also scaffolding the learner would not miss.

**S9. The closing summary overstates.**
- Quote: "A lost `COMPLETE` left every edge in the graph, because other runs carried them."
- The next sentences say a job that ran once left no edge. The first sentence needs its scope: for a job with other runs.

## COULD

**C1. A function is called a "job".**
- Quote: "## A job that ran once", and "because the job has no other run to compare with".
- `remove_return` is a function (`jobType: FUNCTION`). The map caption separates "jobs nightly; functions at any hour", and Chapter 9 counts "four jobs and the two functions".

**C2. Two details in the setup are unexplained.**
- The log spec in `lose=["build_daily_sales COMPLETE 2026-09-10"]` has a date, while `lose=["remove_return COMPLETE"]` has none. One sentence on the "job TYPE date" form lets the learner lose other events.
- Why 09:00 on Monday 14?

**C3. "Open run" has a real-world case the page does not mention.** A STREAMING or SERVICE job has "no expected terminal event under normal operation" (`docs/sources.md`, line 67). That would sharpen the model-versus-reality list.

**C4. The model-versus-reality list is thin.**
- It does not say that a real producer's retries are usually capped or buffered.
- It does not say that the 30 s wait and 1 s/2 s lags are the shop's choices. The first bullet only says "invented".

**C5. Wording.**
- "The collector's events cannot tell" and "the available events" read as personification.
- "Its usual time is empty" refers to the column "usual seconds".
- "The head of the shop's requirement" is the house pattern from Chapters 8 and 17 but still reads oddly.
- The forward reference to Chapter 19 appears three times (the at-least-once paragraph, the summary, and the following lead-in), against `docs/style.md` rule 24.
- The two lists in the readings section differ in shape (rule 8).

**C6. The "Time and memory" callout is a copy.**
- It says "Running every cell took 9 to 12 seconds … about 400 MB … (measured on a computer)", identical to Chapters 16 and 17.
- `tests/test_jupyterlite.py` pins measurement rows for Chapters 3 to 17 only, so Chapter 18's figures are not measured. Confirm or measure.

**C7. The notes' "Gives nothing away" answers describe options that do not exist.** The notes talk of options "the same edges, an edge gone, no job" but the page uses a free-text cell. Review fails a block whose answers do not match the page, so update the notes' text.

Reviewed: the as-built chapter (prose, prediction prompts, code cells, labels, requirement section, closing questions and model-versus-reality note), its notes, and the engine outputs above. Not inspected: the rendered notebook in a browser, and the pinned `docs/sources.md` source text beyond the lines cited.
