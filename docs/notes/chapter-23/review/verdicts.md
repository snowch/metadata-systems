# VERDICTS ON THE CHAPTER 23 FINDINGS

Upheld 6, partly upheld 10, rejected 5 (21 findings).

I read `CLAUDE.md`, the findings, the as-built chapter, `notebook/chapter_23.py`, `docs/notes/chapter-23.md`, `notebook/shop/scale.py`, and the neighbouring chapters (8, 9, 10, 18 to 22) and their notes. I ran `shop.scale.*` from `/home/user/metadata-systems/notebook`. All the reviewer's numbers reproduce, except the ~12,300 figure in finding 5 (see there).

## BLOCKING

**1. UPHELD (small fix).**
- Checked: `retain(events23, 3, "2026-09-14T09:00:00Z")` keeps 28 of 68 and leaves no run edge naming `r-201.json`. `retain(..., 90, "2026-12-07T09:00:00Z")` keeps 60 of 68, so `r-201`'s events are still kept at 90 days until about 14:20 on Monday 7 December. The page never says why 3 days.
- "Retention by age meets the first meaning. It also lost the lineage of `r-201`..." reports the 3-day run as if it were the 90-day requirement's result.
- The fix must state that 3 days is a stand-in for the same loss at 90 days, and say when `r-201`'s events would pass 90 days.
- A sentence does this. A second `retain` cell is not needed.

**2. PARTLY UPHELD.**
- Stands:
  - "each needs something different:" is followed by bullets that name mechanisms and never say what each needs. Chapter 22's equivalent bullets carry their needs inline. The third reading's need ("which assets are still in use") appears only in a later paragraph.
  - The readings should be phrased as the questions the head of the shop might be asking, each with what it needs. That is the five-part structure in `CLAUDE.md`.
  - The projection says "Every event is kept for 90 days" before the requirement box. The page should say the 90 is taken from the head of the shop's number, or give it first as the requirement.
- Does not stand:
  - The list-then-"does not say which it means" shape is the Part V convention (Chapter 22). Do not restructure it.
  - Do not add more readings. "From last use" is already the third reading. "Queryable or archived" is not worth a fourth.

**3. UPHELD.**
- `Rows` takes a `null` label (`platform.py` line 71, default "NULL"), and `first_over` does not set it, so "never" shows as NULL. The prose's "never passes it" is not tied to that cell.
- Smallest fix: pass a `null` label to `first_over`'s Rows saying the way does not pass within 10,000,000 assets, and keep the data values as they are. `tests/test_engine.py` line 831 reads the values.
- Apply the same label to `project` only if it has nulls (it does not).

## SHOULD

**4. PARTLY UPHELD.**
- Stands: the `first_over` table prints "index" and "partitions" labels one paragraph before they are introduced. The column is headed "question" but holds six ways.
- Does not stand: "scan" is an ordinary verb, not a defined term. The next paragraph introduces both terms immediately.
- Fix: plain labels or a header that says "way", or a one-line gloss. The same labels appear in `project`, so keep the two tables consistent.
- Do not introduce the terms before the prediction.

**5. PARTLY UPHELD.**
- Stands:
  - "the first number of assets at which it reads more than 1,000,000" is false as worded: it is the first listed size. `SIZES` are powers of ten, and the scan way passes 1,000,000 at about 12,600 assets (79.48 stored events per asset), not at 100,000.
  - The prediction asks for one question, but the answer is two questions, each in its read-everything way. Ask "which ways" and say the sizes are powers of ten.
- Does not stand: pointing out the near-misses (partitions at 883,117 against a limit the page already calls the shop's choice). The project table shows them, and saying so would explain the result.

**6. UPHELD.**
- Fan-out of 3 (`FANOUT`, 3^4 = 81 edges) is never stated on the page. "Followed 4 steps, it never passes it" cannot be checked.
- "The widest search follows 0.43 of the edges" at every size is an assumption, because `project` holds the share constant.
- The fix must state both, and add both to "How this differs from a real platform". The fan-out belongs among "the shop's own choices".

**7. UPHELD (small).**
- `latest run, index` is `ceil(log2(stored)) + 1`, per the docstring: about 30 steps down the index and one record. 31 is not 31 stored events.
- The page says the projection "counts the stored records that three questions read". Reword to "records read" and say what the 31 is. The unit change is minor.

**8. PARTLY UPHELD.**
- (a) Stands. "`r-201`'s row is still in `returns`" is asserted and no cell shows it. The row exists (`week23.warehouse.sql('SELECT * FROM returns')` returns r-201, r-202 and r-204). Chapter 9 line 391 says the same, so a pointer to Chapter 9 or one query cell would do. This is the chapter's surprise and should be seen, not only stated.
- (b) Stands. "In use" is undefined. `reach` shows `returns` follows 0 edges, so the recorded lineage does not show anything using it. The page should say what it means by "in use": the row is still in the table, and Chapter 10 shows a function reading it. It should not call the asset "in use" as if the data showed that.
- (c) Stands, lightly. Tidy "`r-201`", "`r-201.json`", "`r-201`'s row" and "the asset" into file, return, row.
- (d) Rejected. The deletion step is not a prediction, so its predictability costs nothing.
- (e) Partly stands. The compaction cell runs on all 68 events and deletes none. "That edge stays when the events are deleted" is the shop's rule, not a result. Say so; a combined retain-then-keep cell is not needed.

**9. PARTLY UPHELD.**
- Stands: the page presents "compaction" as a general term but defines it in the shop's own sense. It needs a note that the word means other things elsewhere, and a `docs/sources.md` entry.
- Does not stand: **index**, **partition** and **retention** are defined in their ordinary sense. They need no relabelling, though a sources line would be harmless.

**10. PARTLY UPHELD.**
- Stands:
  - Add a sentence to "How this differs" that the projection counts reads and not writes, including index upkeep.
  - Replace "held them off" in the closing and the summary, since it is figurative.
- Does not stand:
  - "Billions of events" and "ingestion rate" are in the plan. 794,805,210 and the "events a day" column cover the plan's intent. Do not extend the model.
  - Computing the retention saving (`project(retention_days=3)` gives 26,493,507) is optional. The 794,805,210 already assumes 90-day retention, and a 3-day saving would mislead, since 3 days is only a stand-in.

**11. PARTLY UPHELD.**
- Stands: "a search downstream" and "follows" should use Chapter 5's "traversal" and steps. The engine's own docstring says traversal.
- Partly stands: "run edges" and "job edges" against Chapter 9's "edges by run" and "edges by job". Aligning the prose is cheap. The `measure` column headers need a change only if the cost is low. Do not leave prose and table in different words.

**12. REJECTED.**
- Chapters 18 to 23 all use `run_week(["returns"])`, which gives 34 runs and 68 events. Chapter 18 states "68 events" without a note.
- Chapter 9 uses `["returns","source"]`, which gives 41 runs, 82 events, 81 and 17. The difference is the `source` change's analyst's-script runs, not "the development run" as the reviewer says.
- Every chapter picks its own variant of the week. This is a convention, and a note here would raise more questions than it answers.

**13. UPHELD.**
- "the parts of a metadata system that the shop's pages have used so far" is vague and points at the engine, which the page may not name.
- Name what Chapter 24 builds, from `docs/plan.md` line 163: the metadata store, as JSON documents, then tables, then an indexed store, then a graph.

**14. PARTLY UPHELD.**
- Stands: the `measured` block has only a Role, and `retention` has no objective or twelve-question block. Both should be completed. If `retention` has no prediction, honestly mark it as a demonstration or completion.
- Does not stand: listing the opening map in the notes. Chapter 22's notes also omit it, and `reference` figures are not required there.
- Chapters 20 to 22 have the same terse inspect and completing blocks. Fix them together as a Part V sweep.

## COULD

**15. REJECTED.** The 1492 bytes is printed in the table. Projecting storage size would need a new pinned engine column and is not worth it. Trimming the sentence is optional.

**16. REJECTED.** All 11 rows are needed to support "the widest share". The rows are a chosen table.

**17. REJECTED.** Learner-facing numbers must be ones the engine produced, per `CLAUDE.md`. Rounding 794,805,210 in prose would break that pin.

**18. UPHELD.**
- Fix "kept that `r-201.json` was read", "keeps that `r-201.json` was read" and "The shop's metadata system holds one week of one small shop".
- "Each asset gets the week's events per day" is genuinely unclear. It means the week's rate of about 0.9 events per asset per day.

**19. PARTLY UPHELD.**
- The test `tests/test_jupyterlite.py` pins the "9 to 12 seconds / about 400 MB / less than 1 MB" callout for Chapters 1 to 17 only. Chapters 18 to 23 carry the same wording, copied and not measured.
- Chapter 23's Python work is tiny (about 0.2 s), so the numbers are probably still true. This is a Part V-wide mechanical-review item for the browser smoke run, not a Chapter 23 edit.

**20. REJECTED.** "Ninety days" does not quote the requirement. It matches Chapter 22's "The same dataset" and the plan's rule applies to headings that quote the sentence above the box.

**21. PARTLY UPHELD.**
- Stands: "held them off" (see 10).
- Does not stand: the summary restating results is the Part V convention (Chapter 22). Adding "could not show" here would need a sentence on the three open readings, and the requirement paragraph already says so.
