(A reviewer on another model, reading as a learner who has done Chapters 1 to 19; returned as text and saved here.)

REVIEW OF CHAPTER 20, "Out-of-order events"

Numbers checked: I ran `shop.delivery.send`, `shop.ingest.objects(..., order=...)` and `shop.delivery.object_states` from `/home/user/metadata-systems/notebook` for all three experiments, with both orders. I also ran `week_events` on the `clock` week, and compared `test_chapter_20` in `tests/test_words.py` and `shop/delivery.py` with the page. Every time the page states matches the engine: 04:30:24 and 02:30:24 on Thursday 10, 02:31:03, 09:15 on Monday 14, 08:50:02, and the `daily_sales` last-write times by event time and by arrival. The runs table shows `START` with an end of 02:30:21 for Wednesday 9 by arrival and `COMPLETE` by event time. `r-206.json` is `created` and existing by arrival, `deleted` and not existing by event time. Two things are wrong or unsupported: the slow-clock claim and the Chapter 9 cross-reference, both below. I also read Chapters 8, 9, 13, 16, 18 and 19, `docs/sources.md`, the chapter's notes and the as-built file.

## BLOCKING

1. **The slow-clock claim contradicts Chapter 13 and the engine.**
   - Page: "A program whose clock runs slow, as the reporting tool's did in Chapter 13, sets event times that are early. Its events then sort in the wrong order beside other programs' events."
   - Chapter 13's slow clock (the `clock` change) affected the time the reporting tool's store recorded for the dashboard's last refresh. Chapter 13 itself says `by="runs"` uses "the one clock the shop's platform keeps for its runs", and that the export "sends no events".
   - I ran `delivery.week_events(shop.run_week(["returns","clock"]))`. `refresh_dashboard` on Monday 14 still has START 03:00:00 and COMPLETE 03:00:09, the same as without the change. No shop event carries an early time because of that clock.
   - The page presents a hypothetical as an event the learner saw. The notes' Requirements section repeats the same mapping ("Chapter 13's slow clock").
   - Direction: either say Chapter 13's two clocks were store clocks and that event times could be skewed the same way, or build a skewed-event-time case in the engine (for example `restamp` or a per-program offset) and let the learner run it.

2. **The requirement section marks the arrival reading wrong, lists only two readings, and leaves out the one the specification supports.**
   - Page: "By when it happened, the shop's ingestion meets that meaning. By when it arrived, the run early on Wednesday 9 shows `START`, and `daily_sales` is a day old."
   - This pairs the shop's behaviour with a reading it does not implement and presents the result as a defect. It marks the arrival reading wrong. CLAUDE.md ("Question the requirement") forbids that. "Which message did the collector hear last?" is a legitimate monitoring question.
   - "Latest could mean two things" is also an overstatement. `docs/sources.md` records OpenLineage's run-cycle page: `COMPLETE`, `ABORT` and `FAIL` are terminal, and "Sending any of terminal events means no other events related to this run will be emitted". That supports a third reading, latest by position in the run's lifecycle. It would give a different answer for the `START`-after-`COMPLETE` run, and it does not depend on clocks.
   - The chapter never says what each reading needs from the platform, or whether the shop records it. Chapter 19's duplicates section does this for each reading.
   - Direction: treat each reading as reasonable, say what each needs, say what the shop records, and say which readings that record satisfies. Do not frame consequences as only the arrival reading's failures.

## SHOULD

3. **The arrival times are stated but no cell shows them.**
   - Page: "It arrives at 04:30:24 on Thursday 10, after the `COMPLETE` of the run early on Thursday 10, which arrived at 02:30:24." The same applies to "It arrives at 02:31:03, after its own `COMPLETE`, which arrived at 02:30:24." and "They arrive at 09:15 on Monday 14".
   - "Arrival time" is the chapter's new term, yet the learner never sees one displayed. `Delivery.received()` already lists arrival time beside event time, and the chapter never calls it.
   - Direction: show those rows for the build runs concerned, so the learner can set event time against arrival time before the experiments rely on it.

4. **The first prediction is answered by the paragraph above it.**
   - Page: "Before you read on, write in the next cell when `daily_sales` was last written, as the collector's events show it at 09:00 on Thursday 10: by event time, and by arrival."
   - The preceding paragraph states that the Wednesday `COMPLETE` arrives after Thursday's. The by-arrival half is read off that paragraph, not predicted. The page never states the event times either, so the learner has to recall that every night's build ends at 02:30:21.
   - "Last written ... by arrival" is also ambiguous, since "last" and "by arrival" are not yet defined for a dataset's last write.
   - There is no "I can't tell yet" route, though the notes say "Not knowing: fair."
   - Direction: put the question before the page says which event is held up, or ask what the learner expects the collector to hold, then show it.

5. **The cross-reference for dataset last writes is wrong.**
   - Page: "Ingestion so far took a run's state and each dataset's last write from the events in the order of their event times (Chapter 9)."
   - Chapter 9 states only "A run's state is the type of its latest event, by time." Chapter 9 never mentions a dataset's last write. `.written` appears in no earlier chapter and is first used in this chapter's first code cell.
   - Chapter 8's consumer "takes a run's state from the last event it received", which is the arrival reading. The page does not say that Chapter 9 changed this.
   - Direction: say that `written` keeps, for each dataset, the run that last wrote it, and state that order rule here. Do not attribute it to Chapter 9.

6. **The first output is a table nobody chose.**
   - `…written` prints five datasets with full URIs, `job`, `run ended` and a `rows` column. The learner needs one row.
   - `rows` is 1 for `daily_sales`, which could be misread as the table's size. The page does not explain it.
   - Direction: show only the asset the question is about, and the columns it needs.

7. **The learner never holds an event up, and the delays are never varied.**
   - Objective: "Hold an event up, and find what taking the last one to arrive as the latest shows." In all three cells the page fixes the delay (26 hours, 60 seconds, 12 hours). The learner's only action is flipping `"event"` and `"arrival"` in two cells.
   - The second experiment (`START` after `COMPLETE`) has no flip. "By event time, its state is `COMPLETE`." is simply told.
   - The chapter's surprising result is thin as a consequence: every case ends with event time right.
   - Direction: let the learner choose or change a delay, and what it has to pass for the order to change. Also show a case where event time is the unreliable ordering, so that "as long as the programs' clocks agree" is tested. At the moment that caveat rests only on the unsupported claim in finding 1.
   - The notes' blocks for `start-after-complete` and `delete-before-create` give only Role and Evidence. The twelve questions are missing, and the opening map has no block. CLAUDE.md says review fails such a figure.

8. **"Seems to have started again" is not what the table shows.**
   - Page: "Read by arrival, the `START` came last, so the run seems to have started again after it ended."
   - The `started` time is unchanged (02:30:00). The table shows a run with an end time and the state `START`.
   - The practical consequence is missing. Chapter 9's "runs whose latest event is a `START`" and Chapter 18's open-runs check would treat the run as still running.
   - Direction: describe the contradiction the table holds, and name the consequence for the views the learner already has.

9. **The OpenLineage statement is broader than the sources.**
   - Page: "The OpenLineage specification says nothing about events that arrive late or out of order (Chapter 8)."
   - Chapter 8 and `docs/sources.md` say narrowly that the specification does not say what a consumer does with a missing, repeated or late event. `docs/sources.md` records the run-cycle terminal-state statement (see finding 2).
   - Direction: match Chapter 18 and 19's wording, and name what the specification does say about terminal events.

## COULD

10. **One word, "state", carries three meanings.**
    - A run's state (`START`, `COMPLETE`).
    - A dataset's last write: "older state replaced newer".
    - A return's existence: "a run and a return whose state depends on…" and "The latest state".
    - "Older state replaced newer" is also abstract.
    - Direction: say run state, last write and existence.

11. **The third experiment's table has an unmentioned row.**
    - `r-203.json` also shows `deleted`, and `r-202.json` shows `overwritten`.
    - The page does not say these are unaffected.
    - The page does not say that this cell uses a different week (`["returns","withdrawn"]`) from the opening map's (`["returns"]`). The map caption says the desk holds three files and does not show `r-206`.

12. **The opening map serves no question in this chapter.**
    - It is the standing figure, and the prose then carries 02:30:21 Wednesday, 04:30:24 Thursday, 02:30:24 Thursday and 09:00.
    - Under CLAUDE.md's "diagram carries what prose would make the learner hold in mind", a time diagram would carry these.

13. **Small wording points.**
    - "Chapter 13's freshness, read from this, would find `daily_sales` a day behind on Thursday morning." This is a number-like claim with no cell, and "from this" is vague. At 09:00 the write is 30.5 hours old against 6.5.
    - "Taking them in the order they arrived is the other way." is awkward.
    - Objective 3, "Find a run and a return whose state depends on…", is hard to read.
    - "By when it happened, the shop's ingestion meets that meaning." is clumsy.

Reviewed: the as-built chapter, `chapter_20.py`, the notes, the OpenLineage entries in `docs/sources.md`, and the engine paths above. I checked no em dashes, no "lab" or "simulator", no term-gate problem ("event time" and "arrival time" are the plan's terms for this chapter), and the closing names Chapter 21 correctly. The "Originality" and "Requirements" sections exist in the notes. I did not run the browser checks (dark theme, phone width, Run all).
