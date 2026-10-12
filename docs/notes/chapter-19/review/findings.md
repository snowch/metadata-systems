(A reviewer on another model, reading as a learner who has done Chapters 1 to 18; returned as text and saved here.)

# REVIEW OF CHAPTER 19, "Duplicate events"

Checked by running Python from `/home/user/metadata-systems/notebook` with `PYTHONPATH=.`. I ran every code cell's expression (`shop.delivery.send` with `lose_ack`, `at_least_once` and `restamp`; `ingest.dedupe`; `repeated_work`; `run_week(["returns","twice"])`). I also ran the checks the page does not show: the job graphs, `dedupe` on the exact-repeat delivery, and `runs_of` after `dedupe(..., "run")`. I read `shop/ingest.py`, `shop/delivery.py` and `shop/week.py`, Chapters 7, 8, 9 and 18, `docs/sources.md`, `docs/plan.md` and the Chapter 19 tests (`test_engine.py`, `test_words.py`). I did not open the built site in a browser.

Every number the prose states reproduces:
- 68 sent, 69 received, and the job graph is unchanged (`True`).
- Run ends 02:30:52 against 02:30:21, with 21-second runs.
- `dedupe(retimed, "content")` drops 0; `dedupe(retimed, "run")` drops 1 (02:30:52, keeping 02:30:21).
- `returns` is the same in both weeks.
- `repeated_work` lists one row: `r-202.json`, `overwritten`, 2 runs.
- `dedupe(events_t, "run")` drops 0.
- `record_return` writes `returns` in 6 runs against 5. The two starts are 25 seconds apart (09:30:02 and 09:30:27).
- The figure caption's "three return files" and "Monday morning" match Chapter 18's.

The tests pin all of these. The problems are in what the page shows the learner, and in some wording.

## BLOCKING

**B1. The second prediction is never answered by evidence the learner sees.**
- Quote: "In the lineage, `record_return` now writes `returns` in 6 runs, not 5."
- The prediction asks "What changes in the lineage?". The only evidence is `repeated_work`, which lists a version and "runs: 2".
- No cell builds the graph for the `twice` week or shows `record_return`'s run counts. The 6 and the 5 come from nowhere on the page (checked: `edges.of("shop/record_return")` gives 5 and 6, but the chapter never prints it).
- The learner can only take the lineage claim on trust, and so cannot compare it with their prediction. This breaks "the figure then answers" and "a number with no cell that shows it".
- Direction: add a cell, as Chapter 18 does with `found.of(...)`, that shows `record_return`'s edges for the week with the notice once and the week with it twice.
- The same graph also shows the `r-202.json` read edge going from 2 runs to 3. The page does not mention this.

## SHOULD

**S1. The first prediction asks "how", but the cell shows only a boolean.**
- Quote: "Will the lineage change, and how?" The output is `69, True`.
- The lineage is never displayed. A learner who wrote "run counts go up" or "a second edge appears" cannot check either claim.
- Direction: show the edges for `build_daily_sales` once and twice, or the counts, beside the comparison.

**S2. Claims in the requirement section that no cell shows.**
- Quote: "the same event: no edge changes, and deduplication by content drops it".
  - Content deduplication is run only on the restamped copy, where it drops 0. The exact-repeat case is never deduplicated on the page (checked: it drops 1).
- Quote: "It is not idempotent for a run's end time, unless repeats are dropped by run first."
  - No cell re-ingests after `dedupe(..., "run")`. Checked: the end time becomes 02:30:21 again, so the claim is true, but the learner is not shown it.
- Direction: let the existing cells show these, or soften the claims.

**S3. "Ingestion keyed by run id" and "dropped by run" read as the same thing but behave differently.**
- Quote: "Ingestion keys each run by its id (Chapter 9), and adds an edge to a run only once." Later: "Ingestion keyed by run id is idempotent for the graph's edges. It is not idempotent for a run's end time, unless repeats are dropped by run first."
- The page never says why ingestion keyed by run id still moves the end time. `objects()` merges events into a run record and takes the end from the latest event time. `dedupe` discards the later event and keeps the first received.
- "Ingestion took the end time from the later copy" is also ambiguous. It means later by event time, not by arrival. Chapter 20's subject is exactly that distinction.
- Direction: name the two rules and which one each step uses.
- Cross-reference: Chapter 9 says only "A run's state is the type of its latest event, by time." It never says runs are keyed by id or that an edge is added once, so "(Chapter 9)" supports less than it implies.

**S4. "Idempotent" is applied to inputs that are not the same.**
- Quote: "An operation is **idempotent** when doing it twice leaves the same result as doing it once... It is not idempotent for a run's end time".
- The retimed copy is a different message, not the same operation done twice. The definition needs to say the repeated operation is "ingest this run's COMPLETE", or the claim needs to be reworded. `docs/sources.md` records `eventTime` as "the time the event occurred at", so the restamped copy states a wrong time. That fact explains the result better than idempotence does.

**S5. "(run id, event type)" is offered as the key for "the same run reported twice" without a caveat.**
- Quote: "By run, a repeat is a second event with the same run id and the same type." and "the same run reported twice, with a new time: the run id and the event type".
- Chapter 8 (line 391) and `sources.md` say RUNNING and OTHER events are optional and may occur several times in a run. Deduplicating by (run, type) would drop legitimate later ones.
- The shop sends only one START and one terminal event per run, so the key works here. The "How this differs from a real platform" list should say so.

**S6. The final section contradicts itself on event keys.**
- Quote: "the same work done twice: two runs in the lineage, and no event key drops either." Earlier: "Only a key made from the object and its version finds the two runs."
- The object, version and change come from the events' own facet (`shop_objectChange`), so that is an event key in the ordinary sense.
- The page also says "the object and the version a run read" in the readings list, but earlier says "the version the correction wrote". `repeated_work`'s key is (object, version, change), not just object and version.
- Direction: say which keys are identity keys and which are work keys, and use one description of the version.
- "uses the object facet that each function's events carry" should name `shop_objectChange` (introduced in Chapters 8 and 9).

**S7. The requirement is questioned after its readings have been shown.**
- Quote: "Before you read on, write in the next cell what counts as a duplicate here."
- The three preceding sections are the three readings. The learner's commitment is therefore a recap, not the "commit first, as they would at work" that CLAUDE.md asks for.
- Direction: put the commitment before the first experiment, or keep the requirement as a lens and say so in the notes.
- The section also stops at "The requirement does not say which of these it means." Compare Chapter 2 and Chapter 18, which state which readings the record meets as written and as meant.
- The shop's ingestion has no deduplication stage. `dedupe` is a function the learner calls. "Here is what the shop's ingestion does ... deduplication by content drops it" blurs that.

## COULD

- **C1.** "In Chapter 18, delivery was at least once." Chapter 18 sent once only until its "Sending again" section, and used `at_least_once` only there. Say "In Chapter 18, the last cells sent at least once".
- **C2.** "Some programs build an event again when they send it again, with the time of the new sending." This is an unsourced claim about real programs. Label it as the shop's fault or a hypothesis, or add it to the model-versus-reality list. The same list has no note on whether real object-store notices repeat. Neither claim is sourced.
- **C3.** "Then, for each of the three, here is what the shop's ingestion does:" and "Compare this with what you wrote." are signposting filler. The second and third predictions get no compare prompt at all.
- **C4.** The text before the second prediction gives much of the answer: "So `record_return` starts twice" and "Each run deletes the return's row from `returns` and writes it again." These are needed for fairness, but nothing is left to predict except the two outcomes.
- **C5.** "They are the same work done twice" and "added an extra run" treat the second run as a defect. Both runs really happened. `repeated_work` cannot tell a repeated notice from a deliberate re-run of the same version, so the page should say the lineage is accurate and the question is how to count.
- **C6.** "byte for byte" is looser than the code. `dedupe` compares `json.dumps(sort_keys=True)`, which ignores key order.
- **C7.** `docs/plan.md` row 19's candidate readings ("the same content at another time") differ from the chapter's three readings. The chapter notes match the chapter, so update the plan.
- **C8.** "Ingestion keeps every event it has ever received" in the real-platform notes is true of `dedupe` only because it takes a list. Say it is a window-free simplification.
