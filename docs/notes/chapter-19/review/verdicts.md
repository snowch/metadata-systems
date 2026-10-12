# VERDICTS ON THE CHAPTER 19 FINDINGS

Upheld 5, partly upheld 8, rejected 3 (16 findings).

How I checked: I read CLAUDE.md, `docs/notes/chapter-19.md`, `docs/plan.md` row 19, the built chapter and `notebook/chapter_19.py`. I also read Chapters 9, 18 and 20, `docs/sources.md`, `shop/ingest.py`, `shop/delivery.py` and the Chapter 19 tests. I ran the engine from `/home/user/metadata-systems/notebook`. The numbers the reviewer gives all reproduce:
- 68 sent, 69 received.
- `dedupe` of the exact repeat by content drops 1.
- `dedupe` of the retimed copy by content drops 0, and by run drops 1 (02:30:52, keeping 02:30:21).
- After `dedupe(..., "run")`, the run's end is 02:30:21 again.
- `record_return` writes `returns` in 5 runs in the once-week and 6 in the twice-week. The `r-202.json` read edge goes from 2 to 3.
- `repeated_work` lists one row, with 2 runs.
- The shop sends only START and COMPLETE, and each (run id, type) pair occurs once.

## BLOCKING

**B1. UPHELD.** The second prediction asks "What changes in the lineage?". The 5 and the 6 appear nowhere on the page. The only evidence shown is `repeated_work`, which lists "runs: 2" for a version.
- The sentence "In the lineage, `record_return` now writes `returns` in 6 runs, not 5." is the answer, and the learner can only take it on trust. `test_words.py` pins the sentence, but no cell produces it.
- The fix must let the learner see the run counts, as Chapter 18 does with `found.of(...)` and Chapter 9 does with `edges.of`. One cell should show `record_return`'s job edges for the once-week and the twice-week.
- Both weeks must be built the same way, both through `week_events`. The earlier `graph` lambda is not returned from its cell, so a later cell cannot reuse it.
- The `r-202.json` read edge also moves from 2 to 3. It will appear in the table, and one clause can say so.
- Keep the prose number, now backed by the cell.

## SHOULD

**S1. PARTLY UPHELD.**
- What stands: the prompt says "and how", but the cell shows `69, True`, so a learner who predicted a different how cannot check it against anything.
- What does not stand: `True` is not weak evidence. `graph()` is `edges(...).by_job`, and those rows hold the run counts and the first and last times, so equality covers all of them.
- The fix is cheap and shares its cell with B1's helper. Either show `build_daily_sales`'s two edges for the twice delivery (7 and 7 runs, the figures Chapter 18 already printed), or say in one sentence what the equality covers. Alternatively, drop "and how" and ask what the learner expects the run counts to do.

**S2. PARTLY UPHELD.**
- Rejected part: "deduplication by content drops [the exact repeat]". It follows from the definition on the page, "the same as one received before", and the unit test pins it (1 dropped). No new cell is needed.
- Upheld part: "the run's end time moves, unless repeats are dropped by run" is never shown to return to 02:30:21 after the drop. The page shows the dropped event and the kept time but never re-ingests.
- The fix is one short cell, or one line in the existing cell, that lists the run's `started` and `ended` from `dedupe(retimed.events, "run")`. It also backs the "idempotent" paragraph.

**S3. PARTLY UPHELD.**
- What stands: the page says ingestion "keys each run by its id (Chapter 9)", but Chapter 9 says only "A run's state is the type of its latest event, by time". The cross-reference supports less than it implies. The page also never says why run-keyed ingestion still moves the end time.
- The engine settles it. `objects` merges events by `runId` and, going through them in event-time order, takes the end from the latest event time. `dedupe(..., "run")` keeps the first received and drops the rest. One sentence naming these two rules, and which step uses which, fixes it. Drop or correct the "(Chapter 9)" attribution.
- Rejected part: "later copy" is ambiguous between event time and arrival. Here both orders agree (the copy is later by both), so the sentence is true as written. Separating them is Chapter 20's subject, and doing it here would pre-empt that chapter.

**S4. PARTLY UPHELD.** "Doing it twice" is loose when the second input differs.
- Which operation is repeated is not stated. A restamped copy is a different message, because the sender rebuilt it with the time of sending. `docs/sources.md` (line 202) records `eventTime` as "the time the event occurred at", so the copy states a wrong time.
- The fix is one clause on the page saying the repeat is a different message because its time differs, or saying the operation is "ingesting what the collector received". The definition of idempotent stays.

**S5. UPHELD.**
- The specification (`docs/sources.md`; Chapter 8 line 391) says RUNNING and OTHER are optional and a run may have several of them.
- (Run id, type) would drop legitimate events on a real platform. It works in the shop only because each run has one START and one terminal event (verified: max count 1).
- Add one bullet to "How this differs from a real platform". No other change.

**S6. UPHELD, narrowly.**
- "No event key drops either" sits against "Only a key made from the object and its version finds the two runs". The object, version and change come from the event's own facet (`shop_objectChange`), so "event key" is undefined and reads as a contradiction.
- The fix must say what was actually tested: deduplication by content and by run drop neither run. Name the facet `shop_objectChange` (Chapter 9 introduced it).
- Use one description of the version. `repeated_work` keys on object, version and change.
- Do not add the reviewer's "identity key / work key" framework. It is extra apparatus for this chapter.

**S7. PARTLY UPHELD.**
- Rejected part, the placement of the commitment. Chapters 18 and 20 put the requirement section after the experiments and use the same "head of the shop's requirement" box and "write what X means to you" cell. It is the Part V convention, so moving it here would be a restructure of one chapter against its neighbours. The reviewer's own contrast with Chapter 18 does not hold for placement.
- Upheld part, the ending. Chapter 18 states for each reading whether the shop's records meet it. Chapter 19 lists what happens and stops. It should say, for each reading, whether "Ingestion must ignore duplicates" is met in the shop, and the same-event case should read as met for edges only.
- Also upheld: "here is what the shop's ingestion does ... deduplication by content drops it" blurs two things. `ingest.dedupe` is a function the learner calls, not a stage of the shop's ingestion (`objects` and `edges` never call it). Separate "ingestion does" from "deduplication, where applied, does".
- Chapter 18 also keeps the final line "The requirement does not say which of these it means."

## COULD

**C1. UPHELD.** Chapter 18 sent once only until its "Sending again" section. "In Chapter 18, delivery was at least once" is too general. Say the last cells of Chapter 18 sent at least once.

**C2. PARTLY UPHELD.**
- Upheld: "Some programs build an event again when they send it again" is a claim about real programs with no source. It is the engine's `restamp` fault. Reword it as the shop's program, or as something a program can do.
- Rejected: the real object-store notice claim. The page does not say real stores deliver notices twice, and the existing bullet "The shop's faults are invented for the course" already covers it. Adding a sourced claim would cost a new `sources.md` entry for nothing.

**C3. REJECTED.** "Compare this with what you wrote." is the convention in Chapters 18, 21 and 23, so it is not a Chapter 19 fault. The second and third predictions get no such prompt, and that is fine. The only weak phrase is "Then, for each of the three, here is what…". Drop "Then, for each of the three," as part of S7's rewrite, but the finding as filed is not worth a separate change.

**C4. REJECTED.** "So `record_return` starts twice" and "Each run deletes the return's row … and writes it again" are the premise, and the learner cannot predict anything without them. They do not state either outcome.

**C5. REJECTED.** The page does not call the second run a defect. It says "the same work done twice", and `repeated_work` is described as finding runs "started more than once for the same change to the same version", which is what the code does. The page already ends on "Where would you look to tell a retried event from a second run?". At most, optionally change "added an extra run" to "a second run".

**C6. PARTLY UPHELD.**
- Upheld: line 136, which describes the `dedupe` rule as "byte for byte". `dedupe` compares `json.dumps(sort_keys=True)`, so key order is ignored. Say "with the same content".
- Rejected: line 78 ("the two copies are the same, byte for byte"). The copies are a retransmission of the same line, so that sentence is accurate.

**C7. UPHELD.** `docs/plan.md` row 213 lists "the same event twice; the same run reported twice; the same content at another time". The chapter and its notes use "the same event twice; the same run reported twice, with a new time; the same work done twice". Update the plan row. It is a docs-only change, and no test depends on it.

**C8. PARTLY UPHELD.**
- "Keeps every event it has ever received" is true of the collector (`event_lines`), and `dedupe` is given the whole list.
- Reword the bullet to say the comparison has no time limit, as a simplification of the shop.
- Do not add a claim about how real platforms bound the window. There is no source in `docs/sources.md`.
