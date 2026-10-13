# VERDICTS ON THE CHAPTER 25 FINDINGS

8 upheld, 9 partly upheld, 2 rejected (19 findings).

I read `CLAUDE.md`, `AGENTS.md`, `chapter_25.py`, `shop/collector.py`, the as-built page, the chapter's notes and the Part VI design. I also read Chapters 9, 19, 20, 24 and 26, `docs/plan.md`, `docs/sources.md`, `tests/test_words.py` and `tests/test_jupyterlite.py`. I ran the collector from `/home/user/metadata-systems/notebook`. The reviewer's numbers hold: 2, 4 and 5 of 5; 4 of 6 and 69 events after a restart with the stub `start`; 6 of 6 after the fix.

## BLOCKING

**1. Chapter 9's "first stage". UPHELD.**
- The docstring of `shop/ingest.py` lists `parse` first and `normalise` second. Chapter 9 has `## Parse` before `## Normalise`. Its close says "A line cut short was refused at the first stage".
- Fix: name the second stage, or drop the ordinal.

**2. "The graph test passes anyway". UPHELD.**
- I ran the stub key with `newer` always true, then `objects(c.file).runs_of(job="shop/build_daily_sales")`. Thursday 10 ends at 02:30:52, the wrong end time Chapter 19 made a point of.
- The check compares only `edges(...).by_job`: run counts and the first and last time across the week. That hides Thursday's end, because the latest time is Sunday's.
- The graph is built from `c.file`, so `newer` can never change it.
- The page's reason (runs merge by run id) explains why the run counts stay right, not why the graph is right. Presented as the whole reason, it contradicts Chapter 19.
- The fix must do two things:
  - Make the sentence say what the graph test compares (edges by job: run counts, first and last time) and that it cannot see a wrong end time.
  - Make the test line say what it compares, for example edges by job, instead of "the graph of the week with no faults".
- Reject a stronger graph test. It is an engine feature, and a sentence does the job.
- The reviewer's point about the collector's per-run state goes with item 7.

**3. The restart prediction is answered above it. UPHELD.**
- The text before the prediction says "Its memory does not survive a restart", that the keys come only from `start(stored)`, and that `start` gives an empty set. That is the answer to a question about whether the repeat is dropped.
- The notes' "Gives nothing away" is wrong as written.
- The fix must:
  - Keep above the prediction what a reader needs to reason from: the file survives, and on starting the collector reads its file and rebuilds each run's state.
  - Move the statements that memory is lost and that the stub gives an empty set to after the learner has committed.
  - Keep the prediction.
- The result text then says what was lost.
- Correct the notes' "Gives nothing away" line to match.

**4. The real-platform note drops Chapter 19's caveat. UPHELD.**
- Chapter 19's note says: "The shop's programs send one `START` and one `COMPLETE` for each run. The OpenLineage specification allows a run to send `RUNNING` and `OTHER` events as well, and several of them, so a key of run id and event type would drop real events there." `docs/sources.md` supports it (the `eventType` entry).
- The reader now builds that key into a collector, so the chapter should carry the caveat.
- Add a bullet with Chapter 19's caveat, which is already sourced.
- Add Chapter 20's "as long as the programs' clocks agree", which `newer` depends on.
- Do not add claims about real collectors that `docs/sources.md` lacks.

## SHOULD

**5. Check lines and errors. PARTLY UPHELD.**
- I ran these:
  - A list key gives `TypeError: unhashable type: 'list'`.
  - `start` returning `{e for e in stored}` gives `unhashable type: 'dict'`.
  - A `newer` that is always false prints "The run early on Thursday 10 ends at START, not 02:30:21."
- Upheld:
  - The "ends at START" wording is wrong whenever the run's state is not `COMPLETE`. Fix the message for that case.
  - Add one sentence naming the fields (`run` then `runId`, `eventType`, `eventTime`) and saying a key must be hashable, such as a tuple or text. These are interface names, not the answer.
- Rejected:
  - Catching exceptions in `check`. No Part VI check does, and it would be a new engine feature where a sentence works.
  - Pointing each failing line at `key`, `newer` or `start`. That edges toward giving the answer, and the prose after the stub run already maps failures to pieces.
  - The `missing` wording for a key of run id alone is acceptable.

**6. Key and newer ask for no decision. PARTLY UPHELD.**
- Rejected:
  - Adding predictions. "Change X so that it gives..." is Part VI's convention (Chapters 24, 26 and 27). This chapter already has a prediction at the restart and a free-text one at the requirement.
  - The design lets the page name what each piece compares.
- Upheld:
  - The `newer` instruction has no pointer. Add one to Chapter 20 (event time against arrival time). Chapter 19 belongs to `key` only.
  - The notes' objective ("the reader finds that the key decides...") overstates what the page leaves open. Reword the objective, or the "Gives nothing away" line, to match.

**7. "State" is undefined. PARTLY UPHELD.**
- Add one sentence that a run's state is its latest event, as in Chapter 9 ("each run's state taken from its latest event").
- Add one sentence that the collector keeps it so the tests can ask what state a run is in without re-reading the file. Today it is used only by the Thursday and Friday tests.
- Say plainly that `current` is the event the collector now holds for that run.
- Reject any redesign of why the collector keeps state at all.

**8. The held-up Wednesday `COMPLETE`. UPHELD (a sentence, not a test).**
- The table promises "the 5 arrivals the faults touch", and one of them has no test.
- Say that it needs no piece: it is the first `COMPLETE` of its run, and the collector keeps it whenever it arrives. Say that Chapter 26 uses it.

**9. The closing. PARTLY UPHELD.**
- Upheld:
  - Add one sentence on what the experiments could not show. Chapter 24 has one, and `CLAUDE.md` asks for it.
  - "a key it had seen was kept again" is imprecise. The event was kept again.
  - "A key ... kept each of the 68 events" gives the key the collector's action. Fix both.
- Rejected:
  - The reflective questions. They follow the Part VI pattern in Chapters 24 and 26 and ask about the reader's own collector.

**10. The requirement section. PARTLY UPHELD.**
- Checked: `openlineage.problems` on the broken event returns `[('eventTime', 'missing')]`. With a time added it returns `[]`. So the claim "would have been kept" is true.
- Nothing pins that claim in `tests/`. The notes say "tested", which is wrong today.
- Upheld:
  - Add a test for it, or drop "tested" from the notes.
  - Name the referent ("the developer's event" is the `try_daily_sales` row, in a producer and namespace the shop does not list). Chapter 12 introduced a developer, but not this event.
  - Say "the rules Chapter 8's check holds". The check holds a listed subset of the specification's rules.
- Rejected:
  - A new cell.
  - The closing line "The requirement does not say which it means." Chapter 26 ends the same way, so it is the convention.
  - "Compare with what you wrote." Chapter 26 does not add one either.
- Item 5 of "Question the requirement" is already answered: the collector meets the first reading, keeps no list for the second, and does not refuse for the third.

**11. `start`, `START` and "starts". PARTLY UPHELD.**
- Reword the prose verb ("When it starts, it reads its file" becomes something like "After a restart, the collector reads its file").
- Keep the function name `start`. It is in code font, and renaming touches the stubs, references, tests and smoke test.

**12. The resource warning. PARTLY UPHELD.**
- The finding is right about the gap. `tests/test_jupyterlite.py` pins the warning only for chapters 1 to 23 (`range(18, 24)`), and `notebook-prototype.md` has no table past 23.
- It is not specific to Chapter 25. Chapters 24 to 28 all carry the same unpinned text ("9 to 12 seconds", about 400 MB, "less than 1 MB").
- Handle it once for Part VI: measure, extend the test and the table. Make no Chapter 25 change.
- "This chapter runs the collector three times" is irrelevant. Three checks take 0.07 s natively.

**13. The normalisation sentence arrives too late. PARTLY UPHELD.**
- Move the "comparing two times as text puts them in order" sentence above the `newer` instruction, and correct its stage reference (item 1).
- Reject the whole-second tie note. It does not affect the shop's events, which are 21 s apart at the closest, and it is not worth a bullet.

## COULD

**14. Personification. UPHELD (cheap wording fixes).**
- "an event arrives that `newer` says is newer" is circular. Say "when `newer` gives `True`".
- "the keys it remembers" and "the keys the collector remembered" break AGENTS.md rule 4. Say "the keys it has seen".
- The objective "find what it forgets" becomes "find what a restart loses".

**15. "You write two of these pieces". UPHELD (minor).**
- Say which items the pieces implement (items 2 and 4), or say the third piece, `start`, comes later.

**16. "The broken event" before it is introduced. UPHELD.**
- Introduce it in the faults paragraph, as the developer's laptop event with no `eventTime`, with the `try_daily_sales` row.
- Check line text lives in `collector.MESSAGES` and `test_words.py` may pin it. Change them together.

**17. "The run early on Thursday 10" in nearly every line. REJECTED.**
- It is heavy but precise. It names the one run that tells the reader which test failed, and the chapter has nothing shorter that stays unambiguous.

**18. The platform map plays no part. REJECTED.**
- It is an observation, not a fault. The map is the standing opening in every chapter.

**19. Unbounded key set; keys kept in the store. PARTLY UPHELD.**
- Fold into the item 4 bullet, only as far as Chapter 19 already says: the shop's deduplication keeps every key, "with no time limit".
- Reject any claim about how real collectors keep keys. `docs/sources.md` has no source for it.
