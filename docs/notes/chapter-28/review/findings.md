REVIEW OF CHAPTER 28, "Build the metadata interface"

Checked: I ran `shop.interface` from `/home/user/metadata-systems/notebook` (`writers("daily_sales")`, `runs()`, `check` with the stub and with `REFERENCE`, `page` with several section lists). I confirmed these numbers and dates:
- `writers("daily_sales")` returns `['shop/build_daily_sales']`, and the file holds 41 runs.
- The stub finds 6 runs and the reference finds 7, with the FAIL run on 2026-09-14 (a Monday) among them.
- `daily_sales` has latest day 2026-09-12, a Saturday, last written 2026-09-13T02:30:21Z.

I read the chapter as built and `notebook/chapter_28.py`, `notebook/shop/interface.py`, the chapter notes, `docs/notes/part-6/design.md` and the matching passages of Chapters 13, 24 and 27. I did not drive a browser, so I did not check phone rendering. From the code, the cells are small (two lines for `run_history`, one for `sections`) and the tables sit in `.ms-scroll` wrappers.

## BLOCKING

1. **The page's own claim about what it shows is false.**
   - Quote: "The page draws the sections you chose and names the ones it leaves out, so whoever reads it can tell what it does not show."
   - With all seven sections chosen, the page prints "Every section is on this page." That is the first reading of "everything", and it is met trivially.
   - The page still omits the asset's earlier descriptions and owners, any claims, why the run failed, and row counts. The `owner` section drops empty values and `runs` drops the `writes` column.
   - The "left out" line names unchosen section names, not what the asset has that no section shows.
   - Direction: say exactly what the line does and does not tell a reader. Do not present it as meeting the requirement. Reconsider the "Every section is on this page." wording, which implies completeness.

2. **The fix is presented as complete, but it has a hole the chapter does not state.**
   - Quote: "Built from the programs that write the asset, the run history held all 7 runs."
   - `writers(asset)` comes from the lineage graph, and the graph's writes edges come from events that name outputs. The failed run's event carries none (`writes == []`).
   - A job whose runs have all failed, or whose graph edge is missing for another reason, would still be missing from this "complete" history. The chapter never says so.
   - The closing summary says what the experiments showed but not what they could not show, which CLAUDE.md requires.
   - Related: "Monday's run failed and wrote nothing" is a choice of the shop's events. `docs/sources.md` does not say whether OpenLineage `FAIL` events carry outputs, so the claim needs framing as the shop's choice. The "How this differs from a real platform" note should carry it.

## SHOULD

3. **The requirement exercise stops before its last step.** CLAUDE.md's "Question the requirement" ends with "which readings the record satisfies".
   - Quote: "The requirement does not say which it means."
   - Of the three readings, only the second says what it needs ("Who to ask ... needs `owner`").
   - Nothing connects the learner's free-text answer, or the sections they chose, back to the readings, and nothing shows whether the page meets each reading.
   - Direction: add a result that sets the readings against what the page can show, and ties back to the chosen sections.

4. **The sections step is an instrument with no question in front of it.**
   - Quote: "Add the sections you would want on the page, from the seven names."
   - No person is asking anything, no choice costs anything, and no check or consequence follows (the objective says "see what the page leaves out"). Adding all seven is always the easy answer, and the page then says "Every section is on this page."
   - Direction: put a concrete asking-person or question first, or tie the choice to the requirement's readings.

5. **`check` never uses its sections test, and a typo in `sections` is dropped without a word.**
   - `shop.interface.check(run_history)` is called without `sections`, so "The page cannot draw `upstreams`: choose from ..." never appears.
   - `Page.__init__` filters unknown names silently. I ran `page(..., ["description","upstreams","Runs"], ...)`: it drew only `description` and listed everything else as "Not on this page". A learner who mistypes `upstream` or `freshness` gets no hint.
   - Direction: either call `check` with the sections, or have `page` say which names it did not recognise.

6. **The `run_history` check is weaker than the page says.**
   - Quote: "The check finds 7 runs, the `FAIL` among them."
   - A function returning only the FAIL run passes ("holds 1 runs, Monday's `FAIL` among them."). One returning the right runs twice also passes ("holds 14 runs ...").
   - The message reads "1 runs", and the check never asserts the 6 or 7 the prose names.
   - Direction: check that the history holds each of the writer's runs once, and say which are missing or repeated.

7. **A date and a phrase are stated with no cell that shows them.**
   - Quote: "why its latest day is Saturday 12 needs `runs` and `freshness`".
   - The default page has no `freshness` section, and the chapter prints no latest day. "Saturday 12" appears only if the learner adds `freshness`, and then as `2026-09-12`.
   - The date is also unpinned in `test_words.py` for Chapter 28 (the pinned one is `sales_dashboard` in Chapter 27).
   - The example gives away the chapter's finding (Monday's failed run) before the learner has looked at it.
   - Direction: show the evidence first or pin the date. Consider a less revealing example.

8. **One page uses near-identical names for different things and repeats a fact.**
   - The `description` rows have a `means` field. The `owner` rows have a `meaning` column whose values are `account`, `responsible` and `team`.
   - The `description` section also holds `responsible | j.marsh`, which `owner` repeats. Choosing both shows the same fact twice and blurs what a "section" is.
   - Direction: separate the two sections' content, or say why `responsible` appears in both.

9. **The "Part VI built these" claim is inconsistent.**
   - Quote: "Each section is drawn from what the earlier chapters of Part VI built, in the shop's own versions: ... `columns` from the warehouse, and `freshness` from Chapter 13's measure."
   - Two sections are not from Part VI.
   - Quote (objective): "Build a page for one asset from the store, the collector's file, the lineage graph and the queries that Chapters 24 to 27 built."
   - The reader writes only `run_history` and a list.
   - Also "the owners' sources" and "in the shop's own versions" are vague. The design note promised one sentence saying the earlier pieces arrive as the engine's reference; here it is unclear whether the learner's own earlier code is used.
   - The design note's tests ("rows come from the store", "Thursday's run and its row count") are absent. The page has no row count or quality observations.

10. **The "How this differs from a real platform" section is a single trivial bullet.**
    - Quote: "The shop's page is drawn in these cells from the shop's own code, for one asset at a time."
    - It misses the points above: failed-run outputs, and a real page reading a live store, with access control and history, rather than a file of events.

## COULD

11. **The prediction is guessable and the page does not justify it.**
    - Quote: "Before you read on, write in the next cell whether that run history for `daily_sales` will include Monday's run."
    - The preceding text names "Monday's failed run" and the stub as "keeps the runs whose written datasets include the asset". A learner can reason to the answer. Chapter 13 supports "writes nothing", but this page does not recall it.
    - It is free text, so no "I can't tell yet" option is offered. The follow-up "Compare this with what you wrote." has nothing recorded to compare with.
    - The fix instruction also nearly spells out the code ("keeps the runs of the programs that write the asset, from `shop.interface.writers(asset)`").

12. **Filler or tautology.**
    - Quote: "Monday's run failed and wrote nothing, so the datasets it wrote are none." The clause after the comma repeats the first.
    - Quote: "Compare this with what you wrote." is a direction with nothing to act on.
    - Quote: "The head of the shop's requirement" is a phrase repeated across Chapters 13 and 24 to 27, with no meaning here.
    - Quote: "The requirement does not say which it means." is a flat closer. Say which questions each reading would answer.

13. **Terms.**
    - "program" and "job" are used for the same thing, with the table column `job` and the text "programs that write". Chapter 24 uses "program" to include the returns desk's functions, so the choice is defensible, but one word per page is cleaner.
    - "datasets it wrote" (`writes`) versus "asset" is the same kind of drift.
    - The freshness column "hours before" has no stated referent ("hours before" what?).
    - "every claim" in the third reading is not tied to anything the page can show.

14. **The platform map has no job in this chapter.**
    - The caption is the Monday-morning `run_week(["returns"])` figure shared by Chapters 7 and 20 to 27. It does not match the page's week (`returns`, `source`, `failed`), and it says nothing about the failed run.
    - Caption: "...on Monday morning: object storage holds three return files...". "Monday" here and "Monday's run" in the next section mean different things.
    - Direction: either keep it as a standing figure or drop it here.

15. **The warning callout's numbers** (13 MB, under 1 MB, 9 to 12 seconds, about 400 MB) are measured browser figures that no engine test pins. They are fine if they are measurements, but I could not verify them.
