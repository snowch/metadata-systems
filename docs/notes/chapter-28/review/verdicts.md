# VERDICTS ON THE CHAPTER 28 FINDINGS

3 upheld, 9 partly upheld, 3 rejected (15 findings).

What I ran or read: `CLAUDE.md`, `sceptic-brief.md`, `notebook/chapter_28.py`, `notebook/shop/interface.py`, `docs/notes/chapter-28.md`, `docs/notes/part-6/design.md`, the as-built chapter, the matching lines of Chapters 24 to 27, `docs/sources.md` and `tests/test_words.py`. I ran `shop.interface` from `notebook/` (`runs()`, `writers`, `check` with several functions, `page` with `freshness`, `observe.freshness`, `query.owners`).

I did not drive a browser. The factual claims in findings 1 to 8 hold; where a finding's premise fails, the verdict says so.

## BLOCKING

**1. "The page's own claim about what it shows is false." PARTLY UPHELD (a prose fix, not blocking).**
- Stands: "so whoever reads it can tell what it does not show" overstates. I confirmed that the `left_out` line is computed from `SECTIONS` minus the chosen names, so it names unchosen sections only. `runs` drops `writes`, and `owner` drops empty values (`if v`).
- Does not stand: "Every section is on this page." is accurate. It is a statement about sections, and the first reading of "everything" is met by definition. That is the exercise's own point, so do not change the engine message.
- I could not confirm "earlier descriptions and owners". `store.DESCRIBED` holds one record per asset.
- Fix: say exactly what the line tells the reader (which of the seven names are not drawn) and what it cannot (what a drawn section omits, such as earlier values or why a run failed). Do not present it as meeting the requirement.

**2. "The fix is complete but has an unstated hole." PARTLY UPHELD.**
- Stands: `writers()` reads the graph's `writes` edges, and the failed run has `writes == []`. I confirmed this in the runs listing. A job whose runs all failed would give `writers() == []`, and the "complete" history would be empty. `docs/sources.md` says only that an event type is `FAIL` and is silent on whether `FAIL` events carry outputs. So "wrote nothing" is the shop's event choice, which Chapter 8 already states as a shop fact ("It has no output"). Neither the chapter nor its real-platform note frames it as the shop's choice.
- The closing summary says what the experiments showed and never what they could not, which CLAUDE.md requires.
- Does not stand: the BLOCKING severity. The chapter's lesson (build a view from the record that holds what it shows) is sound, and the reference does improve on the stub.
- Fix: one clause in "Before Chapter 29" saying the history is complete only for programs whose other runs name the asset. Put the failed-run-outputs point in the real-platform note (see 10).

## SHOULD

**3. "The requirement exercise stops before its last step." PARTLY UPHELD.**
- Stands: Chapter 27 ends with which reading the record satisfies and which question needs what. Chapter 28 ends with a flat "does not say which it means", and only the second reading says what it needs.
- Does not stand: tying the learner's free-text answer back. The cell is not recorded and is not tied back in any chapter, so that is a convention.
- Fix: a few sentences, no new cell or engine feature. Each reading says what it needs. The first is met by listing all seven names and shows nothing more. The third is met by no section list, because `runs` holds the week's 7 runs only. Say that the page meets a reading only by the sections chosen.

**4. "The sections step is an instrument with no question in front of it." PARTLY UPHELD.**
- Stands: the cell has no asker and no consequence beyond the left-out line. Adding all seven is the free answer, and the notes call this an experiment, which overstates it.
- Fix: put one concrete question or asker in front of the sections cell. It must not give away the readings or Monday's failure. Alternatively, reclassify the cell in the notes as an instrument serving the requirement exercise. No engine change.

**5. "`check` never uses its sections test; a typo is dropped silently." UPHELD.**
- Confirmed in code: `Page.__init__` filters with `[s for s in sections if s in SECTIONS]`. A mistyped name then appears in "Not on this page: ..." beside the real omissions. The notebook calls `check(run_history)` without `sections`, so `sections_no` is never reachable by a learner.
- Fix: the page must name any chosen section it does not recognise, so a typo is not read as an omission. Then use the `check` sections parameter in the notebook or delete it as dead code. Pin the result in `test_engine.py`.

**6. "The `run_history` check is weaker than the page says." UPHELD.**
- I ran it. A function returning only the FAIL run passes ("holds 1 runs, Monday's `FAIL` among them."). One returning the writer's runs twice passes ("holds 14 runs ..."). The "1 runs" grammar is wrong too.
- Fix: the check must require each of the writer's runs exactly once, from the same source the reference uses, and say which are missing or repeated. Pluralise correctly. Pin the check with the stub, the reference, FAIL-only and duplicated functions. The prose figures 6 and 7 stay and now follow from the check.

**7. "A date and a phrase are stated with no cell that shows them." PARTLY UPHELD.**
- Stands: the default `sections` has no `freshness`, and `daily_sales`'s latest day (2026-09-12) is pinned nowhere in the Chapter 28 test. The date is correct: I ran `observe.freshness` and got 2026-09-12 (a Saturday, 14 September being Monday), and Chapter 27 line 153 states the same. Pin it for Chapter 28.
- Does not stand: "gives away the chapter's finding." Monday's failed run is named in the opening and in the prediction, and the readings come after the learner has seen the 6 and the 7. Chapter 27 already established the latest-day fact. A less revealing example is not needed.

**8. "Near-identical names for different things; a repeated fact." PARTLY UPHELD (low priority).**
- Stands: I confirmed `description` holds `means` and `responsible | j.marsh`, and `owner` holds a `meaning` column with `account`, `responsible` and `team`. A page that chooses both shows `j.marsh` twice.
- Does not stand: renaming. `means` is Chapter 4's stored field, and `meaning` is the key the learner's Chapter 27 `owner()` returns. Both are inherited.
- Fix: at most one sentence saying that the description is Chapter 4's record, which names the person responsible, and that `owner` sets that person beside the other two owners. Alternatively leave it, since the repeat is faithful to the store.

**9. "The 'Part VI built these' claim is inconsistent." PARTLY UPHELD.**
- Stands: `columns` (warehouse) and `freshness` (Chapter 13's measure) are not Part VI pieces, yet the sentence says "from what the earlier chapters of Part VI built". "The owners' sources" and "in the shop's own versions" are vague. The design note promised one plain sentence saying the earlier pieces arrive as the engine's reference, and the learner writes only `run_history` and a list.
- Fix: reword the sentence so each section names its source accurately. Say once that Chapters 24 to 27's pieces arrive as the shop's, not the learner's code. Align the objective ("from the store ... that Chapters 24 to 27 built") with that.
- Does not stand: the missing row-count and "Thursday's run" tests. The design note is a pre-engine working note, and the chapter and notes consistently describe a smaller page. Update the design note rather than add a row-count column.

**10. "How this differs from a real platform is a single trivial bullet." UPHELD.**
- Confirmed: one bullet, which is thin beside Chapters 25 to 27, which have two or more each.
- Fix: add a bullet that "wrote nothing" for a failed run is the shop's event choice, which the specification as recorded in `docs/sources.md` does not settle (see 2). Add a bullet that the shop's page is drawn from a file read whole, whereas a real page reads a live store (Chapter 23's projection). Say nothing about access control or history unless a source supports it.

## COULD

**11. "The prediction is guessable and the page does not justify it." REJECTED.**
- The learner can reason from Chapter 8 ("It has no output") and Chapter 13 ("fails and writes nothing") plus the stub's visible filter. That is the belief the prediction rules want a learner to be able to hold.
- A free-text cell already allows "I can't tell". No Part VI chapter records or compares the cell, so that is the convention.
- The build instruction names the method, not the result, and it is an instruction to build, not an option.

**12. "Filler or tautology." PARTLY UPHELD.**
- Stands: "Monday's run failed and wrote nothing, so the datasets it wrote are none." The second clause repeats the first. Cut it.
- Rejected: "Compare this with what you wrote." appears verbatim in Chapters 18, 19, 21, 22 and 24 to 26. "The head of the shop's requirement" is the standing frame of Chapters 13 and 24 to 27. "The requirement does not say which it means." is the Chapter 26 and 27 closer. The suggestion to say which questions each reading answers is handled in 3.

**13. "Terms." PARTLY UPHELD (one item).**
- Stands: "every claim" in the third reading ties to nothing the page can show. Use words the page can show, or drop it.
- Rejected: "program" against `job` is defensible, as the finding concedes, and Chapter 24 sets the usage. "datasets it wrote" against "asset" is minor. "Hours before" is Chapter 13's and 27's column, whose referent those chapters give.

**14. "The platform map has no job in this chapter." REJECTED.**
- The identical `figures.pipeline(run_week(["returns"]), ...)` call and caption appear in Chapters 24 to 27, and CLAUDE.md makes the map standard in every chapter. "Monday morning" in the caption and "Monday's run" are the same Monday, 14 September.

**15. "The warning callout's numbers are unverified." REJECTED.**
- The text is identical in Chapters 24 to 28. `tests/test_jupyterlite.py` pins the "13 MB" and "about 400 MB" figures to measured values, so they are not unpinned.

## Order of work
1. Engine: finding 6 (the check) and finding 5 (the page names unrecognised sections), with tests.
2. Facts to Haiku: findings 1, 2, 3, 9, 10 and 13's "every claim", then the tautology in 12. Findings 4 and 8 are optional sentences.
3. Pin the `daily_sales` latest day in `test_words.py` (7), and correct the notes: the sections cell's role (4) and the design-note drift (9).
