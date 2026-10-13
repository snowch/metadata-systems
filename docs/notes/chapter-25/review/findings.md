# REVIEW OF CHAPTER 25, "Build the event collector"

Numbers checked: I ran the stub, the REFERENCE pieces and about a dozen plausible wrong attempts through `shop.collector.check` and `run` (`PYTHONPATH=notebook python3`, week `run_week(["returns"])`). I also compared the `faults`, `arrivals` and `openlineage.problems` output with the page. These numbers hold: 5 faults; 2, 4 and 5 of 5 pass; 69 events with the content key; 68 once the key is fixed; 02:30:52 against 02:30:21; Friday `START` against `COMPLETE`; 4 of 6 and 69 events after a restart with a stub `start`; 6 of 6 after the fix. The restart falls between the two `remove_return` `COMPLETE` arrivals, at 16:50:07 and 16:50:37, and Chapter 18 already shows both. Part V's boilerplate, `docs/sources.md` and `tests/test_words.py` were read for the cross-references.

## BLOCKING

1. **A wrong cross-reference.** The page says "The collector normalises each event before it keeps it (Chapter 9's first stage)". Normalising is Chapter 9's second stage. The docstring of `shop/ingest.py` lists `parse` first and `normalise` second, and Chapter 9 has `## Parse` before `## Normalise`. Chapter 9's close says "A line cut short was refused at the first stage". Fix the reference.

2. **"The graph test passes anyway" is misleading, and the test line overclaims.** The page says: "The graph test passes anyway, because ingestion merges events into runs by run id (Chapter 19)."
   - With the stub content key, `objects(c.file).runs_of(job="shop/build_daily_sales", ...)` shows Thursday 10 ending at 02:30:52. That is the wrong end time Chapter 19 made a point of ("The run early on Thursday 10 still ends at 02:30:52"). So the graph from the file is wrong, not the same as the week with no faults.
   - The check compares only `edges(...).by_job` (run counts and the first and last time across the week). The wrong Thursday end time is hidden because the latest time is Sunday's.
   - The test line "The graph from the file is the graph of the week with no faults." passes with the stub, with `newer` returning `False`, and with strict `>`. It fails only for a key of run id alone.
   - The graph is built from `c.file`, so `newer` can never change it. The page never says what the per-run state in memory is for.
   - Direction: say accurately what the graph test can and cannot see. Do not give a reason that Chapter 19's own result contradicts. Say what the collector's run state is used for.

3. **The restart prediction is answered by the text above it.** The page says: "The collector holds two things in memory: the keys it has seen, and each run's state. Its file survives a restart. Its memory does not survive a restart.", then "The keys it remembers are what `start(stored)` gives", then "it gives an empty set", then "Before you read on, write ... whether the collector drops the `COMPLETE`".
   - Together these give the result. The prose says memory is lost, says the keys come only from `start`, and says `start` returns nothing.
   - The chapter's notes claim "Gives nothing away: the cell asks whether, not why", but the prose supplies the why.
   - This breaks the rule that nothing above a prediction hints at its answer, and it removes the surprise ("the key is not enough") that the design relies on.
   - Direction: either state the loss in prose and drop the prediction, or move the sentences about memory and the empty `start` to after the learner has committed. If you keep the prediction, give the reader something to reason from, such as what survives a restart.

4. **The model-versus-reality note drops a caveat the course already established.** The key is presented as "the event's run id and its event type, as Chapter 19's deduplication by run did", and the closing note says nothing against it.
   - Chapter 19's note says: "The shop's programs send one `START` and one `COMPLETE` for each run. The OpenLineage specification allows a run to send `RUNNING` and `OTHER` events as well, and several of them, so a key of run id and event type would drop real events there."
   - `docs/sources.md` supports this (the `eventType` entry, and "Chapter 19's note that a key of run id and event type would drop real events").
   - Every one of the week's 68 events is `START` or `COMPLETE` (Counter run). So Chapter 25's "How this differs" should carry the same caveat. The reader is now building the collector, not just running a dedupe.
   - The note also omits Chapter 20's "as long as the programs' clocks agree", which `newer` depends on.

## SHOULD

5. **Check lines and errors do not help a reader whose code is wrong.**
   - Returning `[event["run"]["runId"], event["eventType"]]` from `key` (the natural reading of "its run id and its event type") gives a raw `TypeError: unhashable type: 'list'`. A `start` returning `{e for e in stored}` gives `unhashable type: 'dict'`. A key reading a wrong field gives `KeyError`.
   - The page never says a key must be hashable (a tuple or text), and never names the fields (`event["run"]["runId"]`, `event["eventType"]`, `event["eventTime"]`). Both matter on a phone.
   - Wrong `newer` functions (`return False`, `None`, or reversed comparison) print "The run early on Thursday 10 ends at START, not 02:30:21." A run does not "end at START". That is nonsense for the commonest wrong attempt.
   - A key of run id alone prints "The run early on Friday 11 is `missing`, not `COMPLETE`."
   - Lines such as "The file holds 69 events, not 68: 1 more." do not point at `key`, `newer` or `start`. The reader must infer the mapping from the page's prose, which only covers the stub case.
   - Direction: catch the error and say which piece failed. Fix the wording for a run whose state is `START`. Make each failing line say which piece to look at without giving the answer.

6. **The key and newer pieces ask for no decision.**
   - The page says what to type before the reader has predicted or chosen anything: "Change `key` so that it gives the event's run id and its event type, as Chapter 19's deduplication by run did" and "gives whether the event's time is not earlier than the time of the event it would replace". The second is nearly the code.
   - The notes claim "the reader finds that the key decides which repeats are dropped". The page has already told them.
   - CLAUDE.md says the loop is predict, build, run. Only the restart has a prediction.
   - Direction: give the reader a choice or a prediction about the key or the comparison before the page names it. If the instruction stays, say so plainly and put the experiment elsewhere. The pointer for `newer` should be Chapter 20 (event time against arrival time), not Chapter 19.

7. **"State" is used without being defined.** "the event that holds the run's state", "each run's state", "rebuilds each run's state". The page never says a run's state is its latest event. It never says why the collector keeps one, given that ingestion derives state from the file. A reader writing `newer` has to guess what `current` is (the held event for that run).

8. **The held-up Wednesday `COMPLETE` is never used.** The fault table lists it ("held up", 2026-09-10T04:30:24Z arrival, event time 2026-09-09T02:30:21Z). No test, sentence or summary mentions it, and no stub or reference variant changes because of it. The reader is told the table shows "the 5 arrivals the faults touch" and then 3 of 5 get a test. Say why it does not matter to this collector, or give it a test. It was the dataset's-last-write fault in Chapter 20, which this collector does not keep.

9. **The closing section does not do what CLAUDE.md asks of a closing.**
   - It does not say "what its experiments ... could not show". Chapter 8's close does, and Chapter 20's wrap-up carries a limit.
   - "After a restart, a key it had seen was kept again until `start` rebuilt the keys from the file." The thing kept again was the event, not the key.
   - "A key of run id and event type kept each of the 68 events once" has the key keep the events. The collector does.
   - The three reflective questions ("What does your collector keep only in memory? What happens to it when the collector restarts? Which events does your collector refuse, and by which rule?") only restate what the page stated. They do not carry the idea to a new situation.

10. **The requirement section stops short.**
    - "the developer's event, had it carried a time, would have been kept" is a claim with no cell behind it. I confirmed it: `openlineage.problems` returns `[]` for the broken event with a time added. The page lets the reader neither try it nor see it.
    - "the developer's event" has not been introduced. Chapter 12 has a developer's `dev` runner, but no earlier chapter has a developer's event with no time. This chapter's table shows only `try_daily_sales`.
    - Item 5 of "Question the requirement" is not answered. The page says the collector "meets the first reading", but never says whether the collector, as built, meets the requirement as written.
    - The reader's own answer is never compared. The restart section says "Compare this with what you wrote." This one does not.
    - "The requirement does not say which it means." is a closing line that restates the bullets.
    - "which Chapter 8's check holds": that check holds a listed subset of the specification's rules (required fields, UUID, `eventType`, date-time, URIs, facet `_producer` and `_schemaURL`), not the full schema. Say "the rules Chapter 8's check holds".

11. **"start", "START" and "starts" collide.** The function `start(stored)`, the event type `START`, "When it starts", "restarts" and "A restart" all appear within a few lines. This is a word with two meanings on one page, under CLAUDE.md's "What no check can catch". Consider disambiguating in the prose (the function is introduced as `start` only in code font).

12. **The resource-use warning has no measurement behind it for this chapter.** "Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory", and "less than 1 MB when opened from Chapter 24's link". `test_jupyterlite.py` verifies the measurements only for chapters 1 to 23 (`range(18, 24)` is the last). Nothing pins Chapter 25's figures, and this chapter runs the collector three times. I read the test and did not find a measurement table past Chapter 23.

13. **The normalisation sentence arrives too late.** "comparing two times as text puts them in order" is what lets a phone-sized one-line `newer` work. It sits after both instructions, so a reader writing `newer` may reach for `datetime` first. The normaliser also truncates to whole seconds (`_utc` uses `%S`), so two events within one second tie. That belongs in the real-platform note with the clock caveat.

## COULD

14. Personification against AGENTS.md rule 4 and `common.md`: "an event arrives that `newer` says is newer" (also circular), "the keys it remembers", "the keys the collector remembered", and the objective "find what it forgets".

15. "You write two of these pieces" follows a list of four things the collector does. `key` is item 2 and `newer` item 4, and the third piece (`start`) is not in the list. Say which items the pieces implement, or number the pieces.

16. "The broken event" appears in the check lines and prose with a definite article before it is introduced. The table says only `try_daily_sales` and "no eventTime".

17. "The run early on Thursday 10" and its Friday twin appear in almost every test line. This is understandable but heavy.

18. The platform map plays no part in any question in this chapter (it is the standing opening, so this is only an observation).

19. The real-platform note could also say that the collector's set of keys grows without limit (Chapter 19: "with no time limit") and that a real collector would keep its keys in the store, so a restart would not lose them.

The first three BLOCKING items are the ones to fix before anything else. The rest of the chapter is accurate against the engine, and the code pieces are phone-sized (each 1 to 2 lines).
