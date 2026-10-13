# REVIEW OF CHAPTER 26, "Build the lineage graph"

**Numbers checked.** I ran these from `/home/user/metadata-systems/notebook`:
- `shop.run_week(["returns","source"])` and `shop.lineage_graph.stored` (82 events).
- `lineage_graph.check` with `STUBS["add"]` (2 of 3 pass, Thursday fails) and with `REFERENCE["add"]` (3 of 3).
- `build`, `table` and `now`, which reproduce every table in the as-built file.
- `shop.collector.arrivals`, for the Wednesday and Thursday arrival times.
- Chapter 25's week (`["returns"]`), which stores 68 events.
- Chapter 9's `ingest.edges`.
- A variant `add` that only fixes `last`, and one that adds an extra field to an edge.

I also read `chapter_09.py`, `chapter_20.py`, `docs/notes/chapter-25/review/chapter_25-as-built.md`, `docs/notes/chapter-26.md` and `docs/notes/part-6/design.md`. The chapter makes no OpenLineage or real-system claim that needs a `docs/sources.md` entry. Its numbers are correct against the engine, except where flagged below.

## BLOCKING

1. **The check's output gives away the prediction, in view while the learner writes it.**
   - The prediction cell is followed immediately by `shop.lineage_graph.check(week26, add)`. The page's step 1 tells the learner to press **Run all**, so the check has already printed: "At 09:00 on Thursday 10, `build_daily_sales` last wrote `daily_sales` at 2026-09-09T02:30:21Z, not 2026-09-10T02:30:21Z."
   - That line is the answer to "when will the graph show that `build_daily_sales` last wrote `daily_sales`", and it sits directly under the cell where the learner writes it. CLAUDE.md names this fault: "a figure ... just below a prediction, which is in view while the learner is still choosing".
   - The text above the cell also leads to the answer: "sets the edge's last time to the time of each event as it arrives" and "It arrived at 04:30:24 on Thursday 10, after Thursday 10's `COMPLETE`". The Objectives line "Find what a late event does to an edge's last time" does the same.
   - Chapter 20 already showed this result. Its closing says taking the last event to arrive as the latest "made `daily_sales` a day behind on Thursday morning". So the learner traces code rather than predicting from a belief.
   - Direction: separate the prediction from the printed check, so the check is not on screen while the learner writes. Ask for something the paragraph above does not already spell out.
   - Chapter 25 uses the same layout, so this is a Part VI decision to review.

2. **"The third fails" does not match the table.**
   - The check prints the Thursday test second. The reload test is third and passes.
   - The prose after the check describes the whole-file test, then the reload test, then says "The third fails: at 09:00 on Thursday 10 ...".
   - A reader who looks for the third row finds "yes".
   - Direction: describe the tests in the printed order, or name the failing test instead of numbering it.

3. **"The file is the one Chapter 25 built" conflicts with the count.**
   - Chapter 25's file holds 68 events. I ran `stored(run_week(["returns"]))` and got 68.
   - This chapter says "The next cell reads the file: 82 events." The extra 14 are `copy_clean_orders`, which only the `source` week adds. The page never says why the number changed.
   - Direction: say that this file adds the analyst's copy job, and why.

4. **The check claims "Chapter 9's edges, each with the same number of runs", but Chapter 9 printed different numbers.**
   - The test line reads "Built from the whole file, the graph has Chapter 9's edges, each with the same number of runs."
   - Chapter 9's page says `build_daily_sales` "writes `daily_sales` in 6 runs, not 7", because Wednesday's `COMPLETE` line was cut short. This chapter's table shows 7.
   - Chapter 9's `ingest.edges` times an edge by the run's end (`r["ended"] or r["started"]`). Chapter 9 gives the first read of `clean_orders` as `2026-09-08T02:30:21Z`. This chapter's table gives `2026-09-08T02:30:00Z`, the `START` event's time.
   - The test compares Chapter 9's engine function run over this clean file, not what Chapter 9's page showed. A reader who remembers Chapter 9 sees two contradictions and is told they match.
   - Direction: say that the match is on edges and run counts, over a file with no cut line. Say that the graph's times are event times, not run-end times.

## SHOULD

5. **The "now" exercise repeats Chapter 9's "current" exercise without saying so.**
   - Chapter 9 has "The graph must show the current lineage." It gives three readings: last event received, latest run (13 of the 17 edges), code change. This chapter's three readings are "every edge ever seen" (Chapter 9's first), "the edges of each program's latest run" (Chapter 9's second), and a 2-day window.
   - The page never mentions Chapter 9. The learner has already asked this question and answered it for the same edges.
   - The chapter's surprise is thin overall. The late-event result is Chapter 20's, and the fix repeats Chapter 25's `newer`.
   - Direction: tie this requirement to Chapter 9, or pick a reading that is new.

6. **The "now" table does not separate the readings, and the claims around it overreach.**
   - Quote: "Each needs something different." The table shows "in the latest run" and "in the last 2 days" giving identical answers on all three rows. Only "ever" differs. I ran `now` on `build_daily_sales`.
   - The `ever` column is constant (`"yes"` hard-coded), so it carries nothing.
   - The bullets state mechanisms ("with each edge's last time and a window"), not the questions someone might be asking when they write "now". CLAUDE.md's "Question the requirement" asks for the questions behind the word.
   - "a window" is undefined. The 2 days is explained only at the bottom, under the model-versus-reality note.
   - "A graph with no times on its edges can answer only 'ever'" is overstated. Each edge keeps its set of run ids, and a join to run records could give the latest run. Chapter 9 itself said the third reading needs "a query would have to join the runs".
   - "The graph keeps ... each program's latest run" (the first bullet) is not true of this graph. `now` infers "in the latest run" by matching an edge's last time to the job's newest last time. That works only because every run names all its edges at the same terminal time.
   - Direction: use a job where the readings differ (`record_return` would). State the question each reading answers. Soften the "only 'ever'" claim.

7. **Save and load are in the Objectives but the learner does nothing with them.**
   - Quote: "Save the graph and load it again after a restart."
   - The learner writes only `add`. The page gives no reason for saving, and no first-principles problem (the graph is lost with the process).
   - "the restart" first appears in the check output ("Saved and loaded again after the restart") before anything in the chapter introduces it. A later sentence says "the collector's restart" and never gives the time.
   - The page does not say what the saved lines hold. I tried an `add` that keeps an extra field per edge. `check` then crashed with a Python `KeyError: 'n'` traceback, because the reload drops fields other than runs, first and last. A learner who adds a count gets a traceback, not a test line.
   - With a standard `add`, the reload test cannot fail, so it teaches nothing.
   - Direction: say what the saved lines hold, or drop the objective. Make the reload test report a lost field.

8. **The "first" half of the fix has no test.**
   - The page says "Change `add` so that an edge's first time is the earlier of ... and its last time is the later of ...".
   - I ran an `add` that fixes only `last`. It passes 3 of 3, and its graph equals the reference graph, because no late event creates an edge.
   - Direction: add a case where the first time matters, or say that the shop's week never exercises it.

9. **Event time and arrival time are never separated here.**
   - Quote: "the first and last time an event named it" and "Wednesday's `COMPLETE` arrived last, so it set the edge's last time".
   - The graph's times are the producer's event times. Arrival time is the collector's. Chapter 20 stated this distinction in one sentence. Here it is implicit, and "time" means both within a few lines.

10. **An instrument with no question in front of it.**
    - The `build_daily_sales` edges table is introduced with "The next cell builds the graph from the whole file and lists the edges of `build_daily_sales`." No question comes first.
    - The notes give "what changed on Sunday?" as the question. The page never asks it.
    - The `now` table has no learner action beyond Run all, yet the notes class it an "experiment".

11. **Words with two meanings or two names for one thing.**
    - "program" and "job" are used for the same thing: "Each edge ... is one program reading or writing one dataset", "each program's latest run", against the `job` column and "the four jobs".
    - Chapter 9 uses "program" for any sender, and the plan decided "jobs, not programs" for Chapters 1 and 2.
    - In the `now` table, `edge` is a column holding `reads` or `writes`, while the prose says an edge is "one program reading or writing one dataset". Chapter 9 uses the same column name, so this is lower severity.
    - "file" means the collector's file, the saved edge file, and the shop's files.

12. **The closing is thin.**
    - The "Before Chapter 27" summary does not say what the experiments could not show. For example, the graph cannot say whether an edge is gone or only idle.
    - "How this differs from a real platform" has two bullets. "It is never too big to keep in memory" is odd and overstated.
    - Neither bullet says that the OpenLineage specification is silent on how a consumer orders late events. Chapters 20 and 25 say that.

13. **Phone size.**
    - The `add` cell has a line of about 110 characters: `edge = edges.setdefault(key, {"runs": set(), "first": event["eventTime"], "last": event["eventTime"]})`. It will scroll sideways on a phone.
    - The instruction to change `add` is clear and does not give the code.

14. **The callout says "(measured on a computer)" for this page.**
    - The same numbers (9 to 12 seconds, 400 MB) are repeated in Chapters 24 to 28.
    - `notebook/tests/test_jupyterlite.py` pins measurements only for Chapters 3 to 23. I found none for Chapter 26.

## COULD

- "make Thursday's write look a day old" (closing summary) is loose. At 09:00 on Thursday the wrong time was Wednesday 02:30:21, so the write looked about 30 hours old, not a day.
- "the graph goes on from where it was" personifies the graph. Say what the reload restores.
- The map caption says "Monday morning" and the figure shows no relation after the learner has built a lineage graph. CLAUDE.md says the map gains a relation once something the learner built records it.
- The closing question "Which of your edges have not been seen for a week?" has no answer in the shop's week. The oldest last time is `r-201.json` at 14:20 on Monday 8, about 5.8 days before Monday 14 at 09:00.
- The `now` function has a `days` parameter, but the cell does not expose it. Letting the learner change the window would turn the table into an experiment.
- "Each needs something different." uses a vague "something". Name what each reading needs.
- A failing whole-file test says "differs from Chapter 9's in {n} edges or run counts" and does not say which edges. Naming them would help a learner whose code is wrong.
