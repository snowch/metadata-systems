Verdicts on the Chapter 13 findings. Checked against the page, `notebook/shop/observe.py`, `runs.py`, `platform.py`, `chapter_07.py`, `docs/sources.md` and the plan. Python runs were done from `/home/user/metadata-systems/notebook`.

**1. "Every time then comes from the runs' events" is false for one time. PARTLY UPHELD.**
- Evidence:
  - `observe.last_run` reads `week.executions` (execution records), not events.
  - The export is not a shop program. `chapter_07.py` says "The export and the analyst's copy send no events".
  - So `orders.jsonl`'s 01:00:41 under `by="runs"` is no event's time. I confirmed `last_run(week, 'orders.jsonl')` returns 2026-09-14T01:00:41Z, and `run_week(["clock"])` with `by='runs'` gives yes/yes/yes.
  - The page's "every" is wrong and "stamp by one clock" is loose.
- Reject the "read the chain from the learner's graph" part. `CHAIN` is the lineage of the jobs' code, labelled as such. Traversing the learner's graph would widen the chapter for no learning gain.
- Fix: reword to say the times come from the runs' own records (not the stores), and that the export's time is the platform's record of its run; no "every", no "events".

**2. `bytes` is contradicted by the tables. UPHELD.**
- Evidence: `platform.estimated_bytes` is 512 + 64 per column plus values, so it is the table's size after the write. The renamed week's 0-row runs show 960 and 750, and `build_daily_sales` climbs 662, 684 and so on.
- "The size in bytes of what it wrote" is therefore false.
- Fix: define it as "the table's size after the run, a catalogue estimate", and make the model-versus-reality note say it differs from OpenLineage's bytes written.
- Reject the aside that `seconds` is unused. Duration is in the plan row, and a run table without it would be odd.

**3. Two clocks gives away cause and result. UPHELD, with a scaled-down fix.**
- The text before the cell states the cause ("clock runs 40 minutes slow"). The paragraph with the edit instruction already states the result ("By them the refresh finished at 03:00:09").
- The notes class the figure an experiment with "Gives nothing away: the prose names the change", which is not true.
- Nothing on the page says what the experiment proved, and "one clock" is never qualified against the closing note's "Every machine on a real platform keeps its own clock too".
- Independent evidence exists and is unused. I ran the clock week: the dashboard's latest day is 2026-09-13 and the readings say "latest day shown 2026-09-13" met, yet its refresh is stamped 02:20:09. The 2026-09-13 value in the dashboard needed `daily_sales`, written 02:30:21.
- Fix:
  - Show the reversal first and ask which explanation fits, with the dashboard's latest day as evidence.
  - Only then name the slow clock and the edit.
  - After the edit, state the result and its limit: the runs' times are the programs' own, trustworthy only if they share a clock.
- Reject the full hypotheses-and-evidence scaffold as over-building; one question plus the limit is enough.

**4. The source of the observations is never named. UPHELD.**
- The events carry `status`, `time`, `rows_read` and `rows_written` (`shop.event_fields()`), but no size and no error.
- The notes' "The shop's events send the row count only" is wrong, since events send both row counts and the status.
- Fix: say once where the table's columns come from, and correct the note to "events carry times, status and the row counts; not size or error".

**5. "Find a night that wrote nothing" is handed over. PARTLY UPHELD.**
- Upheld: the objective says "a night" and the heading says "A night", but the list holds four runs on two nights. 0 is a signal only against earlier nights and the rows read, and the page does not say that.
- Fix: put a question first, for example whether the dashboard looks right under this change, then say what makes 0 abnormal. Use "nights" in the heading and objective.
- Reject:
  - Showing the whole renamed week. 28 rows adds noise.
  - "The page does not say why the rows are 0". It points at Chapter 11's `renamed`, which the learner just ran.

**6. Overstatement. UPHELD.**
- "The rows written and the latest day say it is not" overstates the 0 rows, which only a comparison makes abnormal.
- "Say" also personifies the figures.
- Fix: state what each figure shows (latest day Friday 11 against the day before, 0 rows written against earlier nights' counts) and conclude from those.

**7. Blank is not 0. PARTLY UPHELD (minor).**
- The failed week and the `rows_written=0` filter are never shown together, so "why the failed run is absent from the list" is moot.
- But "It wrote no rows" about `run-027` is stated with blank cells in the table. `observations` sets `rows written` to None unless succeeded.
- Fix: one sentence saying a failed run records no counts, so the table shows blanks, which are not zeros.

**8. The requirement section does not follow the five steps. PARTLY UPHELD.**
- Upheld:
  - The opening prediction is never compared with the result, and the freshness section never says which assets are or are not up to date. Chapter 11 does compare ("Compare these with what you wrote").
  - The requirement is not revisited after the two later cases.
  - Reading 1 is met in every week shown. I confirmed that in the failed, renamed and clock weeks.
- Rejected:
  - A separate "what does fresh mean to you?" commit cell. The opening prediction is the commit, and a second one is redundant.
  - Splitting steps 4 and 5. The bullets and one cell are adequate.
- Fix: after the three cases, compare with the learner's first answer and say that "refreshed lately" passed in every case, and that the requirement does not choose a reading.

**9. The opening gives away the prediction, and the instruments have no question. PARTLY UPHELD.**
- The setup is Chapter 2's known failed night, so it gives away little. Reject that half.
- Upheld in part: "The next cell lists…" for the renamed readings and for the any-hour cell is asked no question. Fix: put a one-line question before each, such as whether the dashboard is fresh under the rename, and whether `returns` is up to date and by which measure.
- Reject "nothing is built by the learner". The plan row "observations from execution" is what the engine builds for this chapter, and Chapters 10 to 12 follow the same inspect-heavy shape.

**10. Tables are restated. UPHELD.**
- The freshness bullets repeat the table with weekdays. "Refreshed lately: met. Built from the latest data: not met. Showing the latest day: not met." repeats the readings table. "4 runs: …" mostly repeats the list.
- Fix: delete the bullets and the recap lines, keeping only the inference the table does not show. The weekday mapping can be kept if needed. The facts tests need updating with it.

**11. No figure carries time. REJECTED.**
- Each comparison is within one table, and `hours before` already carries recency.
- A new time-axis figure needs engine work for little learning gain.
- The map caption ("as Chapter 7 left them") is the standing opening, and `returns` is introduced in its own section.

**12. The returns prose order and an unstated rule. UPHELD.**
- The prose says the cell lists the freshness "then the time of the last change to the bucket". The cell prints the bucket change first.
- "A rule for the nightly tables, written within a day" refers to a rule not stated at that point. The only nearby "within a day" is the readings table.
- The `returns` latest day (2026-09-11) is unexplained.
- Fix: correct the order. Name the rule as the "written within a day" test used for "refreshed lately". Add one clause on what the latest-day value is, or drop that column for `returns`.

**13. Measured claims have no measurement. UPHELD (being fixed).**

**14. `docs/sources.md` has no Chapter 13 entry. PARTLY UPHELD.**
- Line 169 records `ErrorMessageRunFacet` (`message`, `programmingLanguage`) and line 171 records `OutputStatisticsOutputDatasetFacet` (`rowCount`, `size`, `fileCount`). So the "output dataset facet" and `fileCount` point is already covered; reject that sub-point.
- The key name `errorMessage` that the page uses is nowhere in `sources.md` (grep finds nothing). There is also no Chapter 13 heading, which CLAUDE.md requires for any claim about a standard.
- Fix: add a Chapter 13 entry for both facets (key `errorMessage`, run facet versus output dataset facet), and say the shop's `error` is the shop's own field.

**COULD items.**
- Upheld, cheap: "by some measure" is vague. "A day behind" needs its referent (it is defined by the readings table). The summary joins two weeks in one sentence. "Next, Part IV starts." is curriculum narration.
- Rejected:
  - "Up to date" undefined. Leaving it open is the requirement exercise.
  - The `program` column header. "Program" is the plan's word for the shop's side.
  - "Store" and "change" word overlap. The wording is close enough and the cost of a fix is high.
  - The model-versus-reality note, except that "fixed in the course's code" should become "invented for the course", as in Chapters 11 and 12.
  - The unused hidden cell.
