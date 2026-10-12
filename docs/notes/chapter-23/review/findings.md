(A reviewer on another model, reading as a learner who has done Chapters 1 to 22; returned as text and saved here.)

# REVIEW OF CHAPTER 23, "Metadata at scale"

Numbers checked: I ran every engine call the cells make from `/home/user/metadata-systems/notebook`: `scale.measure`, `reach`, `first_over`, `project`, `retain`, `compact`, `lineage_of`, and `project(..., retention_days=3)`. Every number the page states reproduces: 11/6/34/68/67/14/7/1492, 6 of 14 = 0.43, 4 = 0.29, 100,000 / 10,000,000 / never, 31 records, 794,805,210, 68 events with 28 kept, and the `r-201.json` job edge at 14:20:05. I also compared the chapter with Chapter 9 and Chapters 18 to 22, the notes, `docs/plan.md` and `docs/sources.md`. No file was written.

Sources: the chapter makes no claim about a standard or a named product. Its terms are general, though, and `docs/sources.md` has no entry for index, partition, retention or compaction (see SHOULD 9).

## BLOCKING

**1. The retention experiment is run at 3 days, then used as evidence against a 90-day rule.**
- Page: "Retention by age meets the first meaning. It also lost the lineage of `r-201` while its row was still in use."
- The only deletion the learner runs keeps 3 days, "measured at 09:00 on Monday 14". At 90 days, `r-201` (recorded Tuesday 8) would still be fully kept on Monday 14. So retention by age under the shop's requirement did not lose it. The week's 7 days cannot show a 90-day loss.
- The sentence reads as an observed result of the requirement being questioned. It is an inference about a later date.
- Direction: say plainly that 3 days is a stand-in for the same loss at 90 days, and when `r-201` would reach it. Or run `retain` with 90 days at a date 90 days after Tuesday 8, which the engine can do. Also say why 3 days was chosen.

**2. The requirement exercise does not follow the "Question the requirement" structure.**
- Page: "The requirement could mean three things, and each needs something different:" The list that follows names mechanisms ("retention of events by age", "compaction before retention", "retention by use, not by age"), not the questions the requirement might ask.
- Nothing says what each reading needs. For example, the page never says that the third reading needs a record of which assets are in use.
- The projection also adopts the first reading before the requirement appears: "Every event is kept for 90 days." The requirement box then arrives as if that choice were still open.
- The closing "The requirement does not say which it means" is the whole of step 5.
- Direction: state the readings as questions the head of the shop might be asking, put what each needs beside it, then say which the shop's record meets. Give the 90 days its first appearance as the requirement, not as a projection parameter.
- Other readings are not offered: whether "keep" means queryable or archived, and whether the 90 days run from the event or from the last use of the asset.

## SHOULD

**3. The "never passes" cells show NULL.**
- I rendered `first_over`. "latest run, index" and "downstream, 4 steps" appear as italic NULL.
- The prose says "never passes it" but nothing tells the learner that NULL means never, within 10,000,000 assets.
- Direction: change what the cell prints, or say what it means at that cell.

**4. The first-over table shows structure names before the page defines them.**
- The rows read "latest run, index", "one day, partitions" and "latest run, scan", and "scan" is never defined.
- The table sits directly under the prediction and above the paragraph that introduces **index** and **partition**.
- Direction: make the labels plain ("read every event" or "read the sorted events") until the terms are introduced. Also check how the table's "question" column relates to the prediction's "question". Six rows are "ways", not three questions.

**5. The prediction is ill-posed and its answer depends on the size grid.**
- Page: "write in the next cell which question passes that limit first." The page defines three questions, each in two ways. The answer is two questions tied, in their read-everything way.
- "the projection gives the first number of assets at which it reads more than 1,000,000 records" is not literally true. It gives the first of the listed sizes (10, 100, ... powers of ten). I checked `project`: the read-everything cost is 794,790 at 10,000 assets and passes 1,000,000 at roughly 12,300 assets. "100,000" is an artefact of the grid.
- Likewise partitions read 883,117 at 1,000,000 assets, and "only at 10,000,000" sits just over a budget the page calls "the shop's own choice".
- Direction: ask which ways pass first, say the sizes are powers of ten, and note how close the neighbouring values sit to the limit.
- The prediction is a free-text cell like Chapters 18 to 22, so I raise no option-wording issue.

**6. The traversal result depends on two assumptions the page does not state.**
- Page: "The widest search follows 0.43 of the edges" at every size. This holds the whole platform to the shop's share, so one search follows 5,472,727 edges at 10,000,000 assets.
- "Followed 4 steps, it never passes it" rests on `FANOUT = 3` in `scale.py` (3^4 = 81 edges). The page and the differences list mention only "the 4 steps" as a choice.
- Direction: state the fan-out of 3. Say that constant share is an assumption, and add it to "How this differs from a real platform".

**7. "31 records" is not the quantity the model counts.**
- Page: "the latest run reads 31 records at 10,000,000 assets." The engine computes `ceil(log2(794805210)) + 1 = 31`. That is about 30 comparisons walking an index and one record.
- The page also says the projection "counts the stored records that three questions read". 30 of the 31 are not stored events.
- Direction: say what the 31 counts, or change the unit.

**8. The retention section asserts more than it shows.**
- (a) Page: "`r-201`'s row is still in `returns`. The asset is in use; its lineage is not kept." No cell shows the row. The test checks it, but the learner cannot. I confirmed Chapter 9 says the row remains.
- (b) "In use" is undefined. `reach` shows nothing downstream of `returns` in the job edges. Chapter 10 says `daily_sales` values depend on `returns` through a function that the job edges do not record. So "in use" is not what the data shows, and the third reading depends on it.
- (c) `r-201`, `r-201.json`, "`r-201`'s row" and "the asset" are used interchangeably. Asset (file or table), row and return id are different things.
- (d) The deletion step in the experiment is trivially predictable: events older than 3 days are gone. The surprise is (a), which is not shown.
- (e) "That edge stays when the events are deleted" is stated, but the compaction cell runs on all 68 events and deletes nothing.
- Direction: show the row. Show deletion and the surviving compacted edge in one flow, for example retain, then compact the removed events and keep the result. Define "in use".

**9. "Compaction" is used as a general term but is the shop's own sense.**
- Page: "Folding each run's edges into one edge per job, before the events are deleted, is **compaction**."
- In real stores the word has other meanings (key-compaction in logs, merging files in storage engines), and Part VII compares such systems. The same check applies to **retention**, **index** and **partition**, which have no entry in `docs/sources.md`.
- Direction: label the sense as the shop's, add a source note, and say that rolling up is the closest general idea. A fold to job edges is lossy in ways the log-compaction meaning is not.

**10. The cost of the fixes is half-stated.**
- Index and partitions "held them off" is figurative and omits their cost. Writes pay for an index. Partitioning by day makes "latest run of one job" a different problem.
- "How this differs" says time, memory and read cost are not counted, but not write cost. The plan lists "ingestion rate" and "billions of events" for this chapter, and the chapter has neither: its largest figure is 794,805,210.
- Retention is introduced with the 794,805,210 figure, but the savings are never computed. `project` takes `retention_days`, and `project(week, retention_days=3)` gives 26,493,507 stored events at 10,000,000 assets. The chapter does not use it. Without it the learner sees the cost of deleting and not the saving.

**11. Terms drift from earlier chapters.**
- "a search downstream", "follows" and "followed to the end" are used where Chapter 5 introduced **traversal** and "steps".
- "run edges" and "job edges" differ from Chapter 9's "edges by run" and "edges by job".
- Direction: use the established words.

**12. The week's counts differ from Chapter 9's with no explanation.**
- Chapter 9 says "The week has 41 runs", "80 edges by run and 17 edges by job".
- Chapter 23 says "34 runs, 68 events, 67 run edges and 14 job edges". I ran `run_week(['returns'])` and it gives 68 events, 67 and 14. The difference is the analyst's script and the development run, which Chapter 9's week includes.
- A learner who remembers Chapter 9's figures sees two different counts for "the week" and no reason.
- Direction: say which runs this week leaves out.

**13. The closing contains a vague line.**
- Page: "Chapter 24 starts Part VI, where you build the parts of a metadata system that the shop's pages have used so far." "The shop's pages" is vague, and its only possible referent (the engine) is something the page must not name.
- Direction: say what Chapter 24 builds. The plan says it is the metadata store, with an indexed store among its steps.

**14. The notes are incomplete.**
- In `docs/notes/chapter-23.md`, `measured` has only a Role. As an inspect figure it needs the two answers (question served, why needed then). `retention` has no objective or twelve-question block.
- The opening platform map appears in the chapter but not in the notes' figure list.
- Direction: complete the blocks, and name the experiment the map and `measured` belong to.

## COULD

- **15. "An event takes 1492 bytes on average" is measured and never used.** Projecting it to 10,000,000 assets would give a size, and the number would earn its place. Otherwise cut it from the summary sentence.
- **16. The `reach` cell prints 11 rows, and the page discusses 2.** The rest are the zero or 2 edge starts. Consider showing only the top rows.
- **17. 794,805,210 appears three times:** the table, "Keeping less", and the closing. It is also false precision for a 7-day, 11-asset model. Round it in prose, or note that the digits are projected.
- **18. Phrasing.**
  - "Folding each run's edges into job edges first kept that `r-201.json` was read."
  - "That job edge keeps that `r-201.json` was read, and when."
  - Both use "kept that", which is awkward.
  - "The shop's metadata system holds one week of one small shop." is clumsy.
  - "Each asset gets the week's events per day." is unclear.
- **19. The "Time and memory" callout repeats Chapters 21 and 22 word for word** ("9 to 12 seconds", "about 400 MB", "less than 1 MB"). I cannot tell whether it was measured for this chapter. Please confirm.
- **20. The heading "Ninety days" carries the requirement's number.** Check it against the plan's decision to name the section's subject instead.
- **21. The closing summary mostly restates, and does not say what the experiments could not show.** It also uses "held them off" (figurative).
