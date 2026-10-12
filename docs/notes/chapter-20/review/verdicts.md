# VERDICTS ON THE CHAPTER 20 FINDINGS

4 upheld, 7 partly upheld, 2 rejected (13 findings).

What I ran or read: `findings.md`, the as-built page, `notebook/chapter_20.py`, `docs/notes/chapter-20.md`, `docs/plan.md` (rows 20 and 213-214), the `sources.md` OpenLineage entries, Chapters 8, 9, 13, 18 and 19 as built, and `shop/delivery.py`, `shop/ingest.py` and `shop/observe.py`. From `/home/user/metadata-systems/notebook` I re-ran the three experiments with both orders, `Delivery.received()` for each, `open_runs`, and `runs_of(state="START")`. Every number the reviewer checked is right.

## BLOCKING

**1. Slow-clock claim: UPHELD.**
- I ran `delivery.week_events(run_week(["returns","clock"]))` against the same call for `["returns"]`. The `refresh_dashboard` events are identical (START 03:00:00, COMPLETE 03:00:09 on Monday 14), so no event time in the shop is early because of the `clock` change.
- Chapter 13 says the slow clock changed what the reporting store records, and that `by="runs"` uses the one clock the runs' events carry. The page and the notes' Requirements section both present a Chapter 13 event-time fault that does not exist.
- The fix is a sentence, not a new figure. Say that each program sets its own event times, so a program whose clock runs slow sends early event times and its events then sort wrongly beside other programs' events. Say this as what can happen, in the conditional form Chapter 13 uses ("two of them can disagree in the same way"). Remove "as the reporting tool's did in Chapter 13" from the page, and "Chapter 13's slow clock" from the notes.
- I reject the reviewer's other option, building a skewed-event-time case in the engine. The chapter's three experiments do not need it. `restamp` already exists, but it models a retry, not a skewed clock.

**2. Requirement section: PARTLY UPHELD.** It stands as a real fault, though I would not call it blocking.
- What stands:
  - The section never says what each reading needs from the platform, whether the shop records it, or which readings that record satisfies. CLAUDE.md's "Question the requirement" steps 3 to 5 and Chapter 19's section both do this.
  - "By when it happened, the shop's ingestion meets that meaning. By when it arrived, the run … shows `START`, and `daily_sales` is a day old" reads as a pass and a defect. It should be neutral.
  - The fix must say the following:
    - The event-time reading needs `eventTime` on every event, which is the producer's clock. The shop's ingestion uses it by default.
    - The arrival reading needs only the order the collector received events in, which the shop also keeps. It answers "which message did the collector hear last?".
    - Both can be computed from what the shop records. Neither is marked wrong. The requirement does not say which question is asked.
  - Change "could mean two things" to "at least two", or state the third reading.
- What does not stand:
  - The third reading (latest by lifecycle position) is not required. `docs/plan.md` row 214 records two readings as the decision.
  - `docs/sources.md` (around line 35) records that the run-cycle page and `OpenLineage.json` disagree: the page says a terminal event ends the run, while the JSON allows `OTHER` after completion. The third reading therefore rests on a disputed claim.
  - The third reading orders events only within one run. It would not touch `daily_sales`' last write or the delete-before-create case. If it is added, add one bullet saying exactly that, with the disagreement noted. Otherwise leave it out.

## SHOULD

**3. Arrival times stated, never shown: PARTLY UPHELD.**
- The first section introduces "arrival time" as a new term, and no cell shows one. `Delivery.received()` has an `arrived` column and the chapter never calls it. This stands for the first experiment.
- Add one cell after the learner commits that lists the rows concerned, filtered to the `build_daily_sales` COMPLETEs around Wednesday 9 and Thursday 10. Then the prose sentence "It arrives at 04:30:24…" can go, or follow the cell.
- A cell for each of the other two experiments is not needed. The term is shown once, and the `runs_of` cell and the object table already carry their cases.
- `test_chapter_20` pins these sentences with `says`, so a rewrite means updating the test.

**4. First prediction answered by the paragraph above: PARTLY UPHELD.**
- The paragraph before the prediction gives the arrival order outright ("arrives at 04:30:24 on Thursday 10, after the COMPLETE … which arrived at 02:30:24"). The by-arrival half is a read-off, not a prediction.
- The fix is to state only the hold-up (26 hours) before the prediction. From the 26 hours the learner can work out the arrival order (Wednesday 02:30:24 plus 26 hours is 04:30:24 on Thursday, after Thursday's COMPLETE). The arrival times then appear in the cell from finding 3.
- Say what "last written" means for a dataset before asking for it (see finding 5).
- The "no route for 'I can't tell yet'" point does not stand. The prediction is a free-text cell, and the notes already say "Not knowing: fair".

**5. Chapter 9 cross-reference: UPHELD.**
- Chapter 9 says only "A run's state is the type of its latest event, by time." No earlier chapter mentions a dataset's last write, and `.written` first appears in this chapter's first code cell.
- Cite Chapter 9 for run state only. State here that `written` keeps, for each dataset, the run that last wrote it, in the same order.
- Chapter 8's consumer "takes a run's state from the last event it received", which is the arrival reading. The page could say in one clause that Chapter 9 changed the order.

**6. First output is a table nobody chose: UPHELD.**
- `.written` prints five datasets with `job`, `run ended` and `rows`. Only the `daily_sales` row matters, and the other four are identical in both orders.
- `rows` is 1 for `daily_sales`, which a learner could read as the table's size, and nothing explains it.
- Show only the row the question is about and the columns it needs (the dataset and when it was last written). Keep the cell simple, because the learner edits `order=`.

**7. Learner never holds an event up: PARTLY UPHELD.**
- What stands:
  - Objective 2 says "Hold an event up", but the learner only flips `order=`.
  - A cheap fix is to invite one edit of the delay and say what to look for. For example, a delay under about a day leaves the Wednesday COMPLETE arriving before Thursday's, so arrival order equals event order. The lesson is that a delay matters only when it passes the next event of the same kind. The other fix is to reword the objective.
  - The notes lack the twelve-question blocks for `start-after-complete` and `delete-before-create`, and have no block for the opening map. `docs/notes/chapter-20.md` needs them. CLAUDE.md says review fails such a figure.
- What does not stand:
  - A new skewed-clock figure. After finding 1 is fixed, one sentence carries the caveat.
  - "The surprising result is thin". A one-day-late event making a table look a day stale, and a return that exists though it was withdrawn, are the chapter's surprises.

**8. "Seems to have started again": PARTLY UPHELD.**
- What stands:
  - The `runs_of` table shows `started` 02:30:00 unchanged, `ended` 02:30:21 and state `START`. That is a run with an end time whose state is `START`, not a second start.
  - The page should describe that contradiction.
  - It should also name the consequence for a view the learner already has. Chapter 9's `runs_of(state="START")`, the "runs whose latest event is a START" cell, lists exactly this run. I ran it and it does.
- What is wrong in the finding: it says Chapter 18's open-runs check would treat the run as running. `delivery.open_runs` keys on terminal events (`TERMINAL`), not on state. I ran it with this delay, both at the end of the week and at 02:30:30 on Wednesday 9, and it returns no rows. Do not name Chapter 18 as affected.

**9. OpenLineage statement too broad: UPHELD.**
- The page says the specification "says nothing about events that arrive late or out of order". Chapters 8, 18 and 19 say it does not say what a consumer does with such an event. `sources.md` (around line 71) records a text search that found nothing on consumer handling, and also records the run-cycle statement that a terminal event ends a run's events.
- Match the Chapter 18 and 19 wording. Optionally add that the specification does say a terminal event means no other events for that run follow.

## COULD

**10. "State" in three senses: PARTLY UPHELD.**
- Two spots stand. "Older state replaced newer" is abstract (the thing replaced is a dataset's last write). Objective 3, "Find a run and a return whose state depends on…", is hard to read and uses "state" for a return's existence.
- Use "run state", "last write" and "exists" in those places.
- Leave "Show the latest state of each run" alone. It is the requirement's own wording.

**11. Third table's unmentioned rows and different week: REJECTED.**
- The cell shows `["returns","withdrawn"]` in its own code, and the prose before it introduces `r-206` and its withdrawal. The page directs the learner to `r-206.json`'s row.
- I ran both orders. `r-201` to `r-204` are identical in both, so the other rows do not mislead.
- The opening map's different week is the standing figure's job, and its caption is accurate.

**12. Opening map serves no question: REJECTED.**
- The map is the standing reference that CLAUDE.md puts in every chapter.
- A time diagram is a new figure for a problem that finding 3's cell removes. After finding 4's change the prose no longer holds a stack of times.
- The map still needs a notes block, which finding 7 covers.

**13. Small wording points: PARTLY UPHELD.**
- Stands:
  - "Taking them in the order they arrived is the other way" is awkward.
  - "By when it happened, the shop's ingestion meets that meaning" is clumsy. Finding 2's rewrite covers it.
  - "Chapter 13's freshness, read from this" has a vague "this". Name the collector's last write instead.
- Does not stand: the claim itself is sound.
  - The 24 hours is exact. At 09:00 Thursday the write is 6.5 hours old by event time and 30.5 hours old by arrival.
  - Chapter 13's `by="runs"` takes its times from the runs' events, so the freshness reading is legitimate.
  - A new cell for it is not needed.
- Objective 3 is covered by finding 10.

## Order of work

Fix in this order:
1. Finding 1 (page and notes).
2. Findings 5, 6, 3 and 4 together (one set of cell and prose edits to the first section).
3. Finding 2, with findings 8, 9, 10 and 13 as wording edits.
4. Finding 7 (objective or delay edit, and the notes blocks).
5. Update `test_chapter_20` for any rewritten sentence.
