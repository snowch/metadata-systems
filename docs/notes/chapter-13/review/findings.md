REVIEW OF CHAPTER 13, "Runtime metadata" (read as a learner who has done Chapters 1 to 12)

Every number the page states is correct. I re-ran the failed, renamed, clock and returns weeks and every figure matches. The faults are in claims about what the table holds, in the two experiments, and in the requirement section.

## BLOCKING

**1. "Every time then comes from the runs' events" is false for one of the four times.**
- Where: "Change `by="stores"` to `by="runs"`, select the cell and press **Run below**. Every time then comes from the runs' events, which the shop's programs stamp by one clock."
- Problem: with `by="runs"`, the first step (`orders.jsonl`, 01:00:41) is not read from an event.
  - `observe.last_run` takes `orders.jsonl`'s time from the export's execution record.
  - Chapter 7 says "The export and the analyst's copy send no events: their code is not in the shop's repository."
  - I checked `shop.events(week)`: no event has `orders.jsonl` in `writes`, and the jobs are only the four programs.
  - So the one step the clock experiment leaves unchanged is the only one whose time no event could supply. The learner's own Chapter 7 events cannot reproduce this table.
  - The lineage in `chain` is also a hard-coded constant (`CHAIN`), not a traversal of the graph the learner built in Chapters 6 to 9. "Along the lineage that feeds the dashboard" suggests otherwise.
- Direction: make the claim true. Either say the first time comes from somewhere else, or drop the "every". Better, let the chain read from the learner's graph and events, and say what a run-based check cannot see (a file written by code outside the repository).

**2. The definition of `bytes` is contradicted by the page's own tables.**
- Where: "the size in bytes of what it wrote", and the renamed table: `run-022 … rows written 0 … bytes 960` and `run-023 … 0 … 750`.
- Problem: `bytes` is the catalogue's estimated size of the whole table after the write.
  - In `platform.py` it is `estimated_bytes`: 512 + 64 per column, plus the values.
  - A run that wrote 0 rows therefore "wrote" 960 bytes.
  - `build_daily_sales` writes one row a night, yet its bytes climb 662, 684, 706, 728, 750, 772, because it appends and the figure is the table's total.
  - `refresh_dashboard` has none.
  - A careful reader will stumble on "0 rows, 960 bytes".
  - OpenLineage's `outputStatistics.size` (`docs/sources.md`) really is "the size in bytes written to the dataset", so the model-versus-reality note implies the shop's column is that. It is not.
- Direction: state what the column is (the table's size after the run, a catalogue estimate). Or change the engine to record bytes written. Or drop the column, since nothing in the chapter uses it. `seconds` is also never used: every night is identical and none is slow.

**3. The Two clocks experiment gives the cause and the result before the learner acts, so it teaches less than the notes claim.**
- Where: "In the week with the `clock` change, the reporting tool's clock runs 40 minutes slow." Then "…the dashboard was refreshed before its input, though it ran after it". Then "By them the refresh finished at 03:00:09, after `daily_sales` was written."
- Problem:
  - This breaks the rule "the effect before its cause", and the rule that no text gives away what an experiment shows.
  - The cause is announced first, and the outcome of the one-word edit is printed in the paragraph above the cell.
  - The learner changes `"stores"` to `"runs"` and confirms a sentence they have already read.
  - There is no discrepancy to investigate, no competing hypothesis, and no independent evidence.
  - Independent evidence exists but is unused. In the clock week the dashboard shows Sunday 13, a value that did not exist before 02:30:21, so a 02:20:09 refresh is impossible.
  - Nothing on the page says what the experiment proved.
  - The notes' consequence ("a freshness check is only as right as the clocks it compares") appears nowhere in the prose.
  - The only wrap-up is the cryptic "Two clocks reversed the order of two writes until every time came from the runs' events."
  - The page implies the runs' events are the cure. Yet the closing note says "Every machine on a real platform keeps its own clock too", which undercuts "one clock", and the page never says so.
- Direction: show the reversal first with no cause given. Ask what could explain a refresh recorded before its input, offering hypotheses and the evidence that would separate them: the latest day shown, the run's finish time. Only then name the skew. After the edit, say what it proved and what it did not: the runs' times are the shop's programs' own claim, trustworthy only if they share a clock.

## SHOULD

**4. The source of the "observations" is never named, and the notes say it is not the learner's events.**
- Where: "A fact recorded about a run while it ran is an **observation**…", and "The shop's events send the row count only."
- Problem: a reader who built events in Chapter 7 and OpenLineage events in Chapter 8 asks who records `bytes` and `error`.
  - The notes (Known gaps) admit the events carry neither, so the table is not built from the learner's events.
  - The note also misstates the events. They carry rows read and rows written (`inputStatistics`, `outputStatistics.rowCount`), status, and a FAIL event.
  - It should say which facets are missing: size, and the error message.
- Direction: say where each column comes from, and which the shop's events carry and which they do not.

**5. The objective "Find a night that wrote nothing" is handed over.**
- Where: `shop.observe.observations(week13r, rows_written=0)`, preceded by "The next cell lists the runs that wrote no rows."
- Problem: the code does the finding.
  - The learner never sees the week's full table under the change.
  - They are never asked how they would notice that 0 rows is wrong. 0 is only abnormal against history: 39 and 44 rows on earlier nights, or 43 rows read.
  - The heading and objective say "a night", but there are two nights and four runs.
  - The page does not say why the rows are 0, only "Chapter 11's `renamed` change".
- Direction: ask first, for example which readings the dashboard will meet under this change, and let the learner look for the runs themselves. Say what makes 0 a signal (compare with earlier nights and with rows read). Use "nights" in the heading and objective.

**6. Overstatement.**
- Where: "The status and the times say the dashboard is up to date. The rows written and the latest day say it is not."
- Problem: a row count of 0 does not say the dashboard is out of date. It is a signal only by comparison. The sentence also personifies data, which the course rule prohibits.
- Direction: state what the learner can conclude from the figures and which comparison supplies it.

**7. Blank is not 0, and the page glosses over it.**
- Where: "It wrote no rows." (about `run-027`). In the table the failed run has blank `rows read`, `rows written` and `bytes`.
- Problem: the table records no number for the failed run, while the next section filters on a recorded 0. The claim "wrote no rows" comes from outside the table. "Unknown" versus "zero" is exactly the distinction runtime metadata needs, and it is not made.
- Direction: name the difference, and say why the failed run is absent from the `rows_written=0` list.

**8. The requirement section does not follow CLAUDE.md's five steps.**
- No commit first: there is no "what does 'fresh' mean to you?" cell, unlike Chapters 11 and 12. The opening question uses "not up to date", and the page never returns to it.
- Step 4 (what the platform records) is not separate from step 5. The bullets say what each reading needs, then one cell tests them.
- The section ends with "The requirement does not say which it means." before the two later sections (wrote nothing, two clocks) test the same readings. The strongest result, a dashboard that meets two of three readings and is a day behind, is never brought back to the requirement.
- Reading 1 is met in every week the chapter shows. This is never said, though it is the point: the "last refreshed" figure most platforms show cannot catch any of these faults.
- The page never closes the loop on the opening prediction. Nothing compares the learner's answer with the tables. Chapter 11 does ("Compare these with what you wrote"). The freshness bullets never say which of the four assets are not up to date.
- Direction: add the commit, separate "what is recorded" from "is it met", return to the requirement after the three cases, and compare with the learner's first answer.

**9. The opening gives most of the prediction away, and the instruments have no question in front of them.**
- Where: "`build_daily_sales` fails and writes nothing. `refresh_dashboard` runs after it, as every night, and redraws the dashboard from `daily_sales`."
- Problem: that bullet tells the learner what `daily_sales` and the dashboard hold.
  - The question that remains open is "how would you tell?", and nothing returns to it.
  - The cells in "What each run recorded", "How recent each asset is", the renamed readings and "A table written at any hour" are each introduced with only "The next cell lists…".
  - No question or evidence to look for precedes them. The "any hour" section never asks whether `returns` is up to date.
  - The only learner action in the chapter is a one-word edit whose result is pre-announced. In effect it is a tour of outputs.
  - Nothing is built by the learner, although the plan lists "observations from execution" as what they build.
- Direction: put a question before each instrument. Predict-then-run candidates: the readings under `renamed`; whether `returns` is up to date; which clock to trust. Let the learner choose what to record or what rule to apply.

**10. Tables are restated row for row.**
- Where: the freshness bullets ("`orders.jsonl`: last written 8.0 hours before; latest day Sunday 13." and so on). Also "Refreshed lately: met. Built from the latest data: not met. Showing the latest day: not met." and "4 runs: …".
- Problem: each repeats the table above it, which is filler under the course's rules.
- Direction: keep only the inference the table does not show.

**11. No figure carries time.**
- Where: the chapter asks the learner to hold about ten timestamps across four assets and three stores.
- Problem: the only figure is the stock platform map. Its caption describes the week with the returns desk, while the chapter's first sections run a week without it, so the freshness table omits `returns`.
- Direction: add a reference figure of each asset's last write on a time axis, perhaps beside a plain-week baseline. The plain week is never shown, so "a day behind" has no visible expectation.

**12. The returns section's prose order does not match the output, and it names a rule nobody stated.**
- Where: "lists how recent each asset is in the week with the returns desk, then the time of the last change to the bucket". The cell prints the bucket change first.
- Where also: "A rule for the nightly tables, written within a day, says it is not up to date."
- Problem: "A rule for the nightly tables" was never stated as a rule; the threshold appears only inside the readings table and the closing note. The `returns` "latest day" (2026-09-11) is shown and never explained.
- Direction: state the rule where it is used and explain or hide that column.

**13. The "Measured" claims for this chapter have no measurement behind them.**
- Where: "Running every cell took 9 to 12 seconds, and the page used about 410 MB", and "less than 1 MB when opened from Chapter 12's link … (measured on a computer)".
- Problem: the notes point to `docs/notes/notebook-prototype.md`, "Chapters 10 to 13". That section does not exist. The file stops at "Chapters 7, 8 and 9". The numbers look copied from Chapters 11 and 12.
- Direction: measure Chapter 13, or remove the claim.

**14. `docs/sources.md` has no Chapter 13 entry.**
- The page says "OpenLineage defines a run facet, `errorMessage`". Sources records `ErrorMessageRunFacet` only as "read and not used", and never the key name.
- The page says "the `outputStatistics` facet holds a row count and a size in bytes". It omits that this is an output dataset facet and that `fileCount` exists.
- Direction: record the sources and sharpen both sentences.

## COULD

- **Terms.** "fresh", "freshness", "up to date", "how recent", "refreshed lately" and "stale" (in the notes) overlap. "Freshness" is defined as two measures, but the second reading (lineage order) is a third kind of thing that is not a measure of recency. "Up to date" is used before it is defined and never defined.
- **Wording.** "(`freshness`) How recent an asset's data is, by some measure, is its **freshness**" has a vague "by some measure". "By the time it was last written, the dashboard is the most recent of the four" mixes tenses and is awkward. "A day behind" has no stated referent.
- **"store".** "Store" (as in "the asset's store", "their stores", `by="stores"`) is used for object storage, the warehouse and the reporting tool, and is easily confused with "storage".
- **"change".** It means both the shop's `clock` and `renamed` settings and the learner's edit ("Change `by=…`").
- **"program" and "job".** The column header "program" differs from the Chapter 7 event field `job` and the Chapter 9 and 12 graph column `job`. The plan's "jobs, not programs" decision applies.
- **Model-versus-reality note.**
  - "fixed in the course's code" slips toward naming the machinery. Chapters 11 and 12 say the scenario is "invented for the course".
  - A 40-minute skew is unrealistic where clocks are synchronised. A timezone error or a store stamping its own receipt time is more typical.
- **"Next, Part IV starts."** Curriculum narration; cut or fold into the next-chapter sentence.
- **Dead hidden cell.** The hidden cell `week = shop.run_week()` is unused here (harmless; five other weeks are also built).
- **Summary conflation.** "one run failed with an error, and four succeeded and wrote no rows" joins two different weeks (failed and renamed) into one sentence.

## What I checked

- I read `CLAUDE.md`, `docs/style.md`, the review prompt, the as-built chapter, `notebook/chapter_13.py`, the chapter notes and brief SA, and the as-built Chapters 11 and 12.
- I read the relevant parts of `chapter_02.py` and `chapter_07.py`, and `observe.py`, `week.py`, `runs.py` and `platform.py`.
- I ran Python for the failed, renamed, clock and returns weeks and verified every printed figure:
  - 28 runs, and `run-027` failed with "database is locked" after 21 seconds;
  - the freshness hours (8.0, 6.9, 30.5, 6.0, and 40.2 for `returns`);
  - the latest days;
  - the readings in each week and the chain by stores and by runs;
  - the 02:20:09 refresh time against 02:30:21;
  - the bucket's last change at 16:50:00 on Saturday 12 (the `r-203` delete) and the table write 4 seconds later;
  - the four zero-row runs in the renamed week.
- I confirmed that `orders.jsonl` has no event, that `bytes` is a whole-table estimate (e.g. 960 for an empty table), and that `ARRIVAL` is 09:00.
- I checked the OpenLineage claims against `docs/sources.md`, and that the notes' "Chapters 10 to 13" measurement section does not exist.
- I did not run a browser or the mechanical half of the review. I did not read Haiku's drafts under `docs/notes/chapter-13/drafts`. I did not test the term gate or the prose check.
