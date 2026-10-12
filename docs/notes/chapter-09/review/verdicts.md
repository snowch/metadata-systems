VERDICTS ON CHAPTER 9

I checked every quote against the as-built page and `notebook/chapter_09.py`. I re-ran the engine for the numbers (`shop.run_week(["returns","source"])` through `ingest`). Every quote in the findings is exact. The counts the reviewer lists hold. I also confirmed:
- `objects()` on un-normalised events gives 13 datasets, not 12.
- `record_return` has a single code version, `2a625b5`, all week.
- `build_daily_sales` is `256e271` through Saturday 12 and `c715bde` from Sunday 13.
- `remove_return` has no read edge. lab.md says it "reads nothing; the object is gone".
- The edges by run per day total 12, 13, 12, 12, 11, 10 and 10, so "41 runs over 7 nights" is loose: 6 of the 41 are daytime function runs.

**1. BLOCKING. Contradiction with Chapter 8 about the analyst's script. UPHELD, BLOCKING fair.**
- Chapter 8 says "The analyst's copy sends no events", and its requirement section says "The export and the analyst's copy do not" send events. `docs/plan.md` says "The analyst's script sends events from Chapter 9".
- Chapter 9's "which has sent its own since Chapter 8" is false. A learner who did Chapter 8 will stop at it. It is a continuity error, not a preference.
- The fix is one clause, and the direction is compatible with the rules. Say that the script now sends its own events, without a "since".
- Beware the "now" in "and now from": it already says something changed, so one cut may be enough.

**2. BLOCKING. Requirement section order and missing verdict. UPHELD on the verdict, PARTLY on the order. BLOCKING is fair for the verdict, not for the order.**

*Verdict (upheld).*
- CLAUDE.md "Question the requirement" ends with "last, it shows which readings that record satisfies".
- The page ends "The requirement does not say which "current" it means." That says the requirement is ambiguous. It does not say which readings the shop's edges meet.
- Chapter 8 ends with "As written, the shop meets the requirement for…".
- The notes' Requirements item 5 claims a verdict the page does not carry. This is a binding structural element, and the notes' claim does not match the page.

*Order (partly).*
- The reviewer overstates "the platform's record before the readings". The record was already shown: the 80 and 17 counts, `found.of(...)` and the drawing.
- What is real is narrower. The learner commits to a meaning. Then `found.latest()` runs one reading as a query and prints it. Only then does the page list the three readings. CLAUDE.md puts the other readings before the figure that shows the platform's answer, so the order is off.
- The prose does say what the cell does ("lists, for each job, the edges its latest run had"). The page does not present the 13 edges as the graph's answer.
- The "Four are dropped" wording leans toward reading 2 and calls its result a loss. That sits badly with "no reasonable reading is marked wrong".
- Direction: list the readings first, then show `latest()` as reading 2's answer, then give the verdict. All of it is compatible with the rules. No need to add figures.

**3. Readings unequal and not all queryable. PARTLY. MINOR is right, "borderline blocking" is not.**

*What holds.*
- Bullets 1 and 2 say what they show ("all 17", "the 13 edges"). Only bullet 3 says what it needs.
- Readings 2 and 3 give the same edges for `build_daily_sales`. They differ only for `record_return`, where the code never changed, so reading 3 keeps all four file edges. The page says nothing of this. It is a real missed chance to separate the readings with an example.
- It folds into finding 2: state each need in the same form and say which readings the record answers.

*What overreaches.*
- "The stage keeps [the code version] from `sourceCodeLocation`" is true. `objs.runs_of` shows `sourceCodeLocation.version`. `found` simply does not carry it.
- So "a query can choose" overreaches only slightly. Reading 3 needs a join of runs to edges. Say that rather than call the claim false.
- The freshness meaning ("kept up to date") is a fair optional addition. Do not add it unless there is room. It is not a rule break.

**4. Dropped edges unverifiable; `r-203`. PARTLY, MINOR.**
- The 17-edge table is never shown, and the learner sees `build_daily_sales` reads the copy stranded in the 13th row.
- The learner can check `build_daily_sales` against the earlier `found.of(...)` cell, because it shows 3 edges. The learner cannot check the three `record_return` files.
- A `found.of("shop/record_return")` cell or the file names is cheaper than printing the 17-row table.
- The `r-203` point is accurate. The first sentence names three files and the bullet names two. The reason is that `r-203`'s row is gone, deleted by `remove_return`. One clause covers it.
- The missing `remove_return` read edge is the engine's deliberate fact ("it reads nothing"). Chapter 7 showed `remove_return` read 0 rows. Reject that part as a defect. At most a clause is needed.

**5. Edges prediction misaligned. PARTLY, MINOR.**

*What holds.*
- "Between jobs and datasets" fits only the 17 by-job edges. The 80 are run-to-dataset.
- One night's edges are 10 to 13, not 17, because 17 includes the returns files and the copy. So neither "as many as one night" nor "seven times" lines up cleanly. 80 against about 11 per night is roughly 7 to 8 times, so the "seven times" answer loosely fits the 80. The question's wording is what muddles it.
- "41 runs over 7 nights" is inaccurate, and it sits immediately before the prompt that offers "seven times". It nudges the prediction and should change.

*What overreaches.*
- "Never revisited" overcalls. "Each night's runs repeat the same reads and writes, so they add edges by run and not edges by job" does answer the expectation. Chapter 8's predictions also close the same way, with the result stated and no "compare with what you wrote".
- The three-places point for the parse prediction is mild.
- Direction: ask about the two counts (by run, by job) in the table's own terms, and fix "41 runs over 7 nights". A sentence returning to the expectation is optional.

**6. Normalising times unmotivated. PARTLY, MINOR.**
- The facts are right. No ordering changes this week, and skipping the stage gives 13 datasets.
- The only checkable consequence is for names. The reviewer's "let the learner skip the stage and see the one difference" would show names only, not times.
- A real reason for times needs a claim the data cannot show. `objects()` sorts by the time string. Events with `+00:00` and `Z` for the same instant sort differently from the same instant written with another offset. This week has only those two forms, so the page cannot show a consequence.
- Either add one honest clause for the reason, or accept time normalisation as a stated rule of the shop. It is not a rule break.
- The 26-row table is long but chosen, and the learner needs it for the 12 and 14 split. Shortening it is a preference. A skip-the-stage experiment is optional new content, not a fix.

**7. Unknown-facet section. PARTLY, MINOR.**

*Upheld.*
- "lists the runs of `record_return`: when each started, what it read, and the change and the version…" misdescribes a cell that shows only two columns. A learner may think the cell is broken until the next paragraph. "asks for" is the fix.

*Mostly a preference.*
- Telling the result before the edit ("shows whether its file was created or overwritten, and its version") contradicts the notes' "Gives nothing away: the prose says what to remove, not what appears". The notes and the page disagree.
- CLAUDE.md permits stating a conclusion ahead of an experiment, so this is a notes mismatch and an optional trim, not a rule break.
- Counting by facet instead of six UUID rows is a preference. The "All 6 are `shop_objectChange`" sentence uses the table. Reject that part.

**8. Words with two meanings. PARTLY, MINOR.**
- The "job" collision in "7 jobs (the four jobs, the two functions and the analyst's copy)" is real. It is inside one sentence, and it is on CLAUDE.md's list of words that mean two things.
- "version" bare in "the change and the version from the facet" is real and cheap to fix.
- "Saturday" has real ambiguity. The page says "reads the analyst's copy from Saturday's row on", "its last such run was on Saturday 12" and "the code since Saturday", but the first copy read is Sunday 13 and the code version changes between them. Make the dates agree.
- "Objects" the stage versus object storage: weak. The stage is named by its function and its output is explained ("jobs, runs and datasets"). Leave it, or rename only if cheap.
- "41 runs over 7 nights": see finding 5.
- Edge-name drift ("run edges | job edges" in the engine's table, "edges by run" in the prose) is real. Aligning the prose to the table is cheap.

**9. Personification and phrasing. PARTLY, MINOR.**
- "To the stage, the run looks as though it is still working" and "so to the graph that run wrote nothing" match CLAUDE.md's rejection of personifying systems. Say what the stored record shows: the state is `START`, with no end time and no output.
- "The stage then knows the facet" is weaker, since Chapter 8 itself uses "what a consumer knows". Reword it if the other two are fixed.
- The opening list ("parse, a stage that rewrites the events in one form, objects and edges") is uneven but explainable: it avoids using "normalise" before its definition. It is a preference. Plain glosses on all four would fix it.

**10. Tables nobody chose. UPHELD for the table, REJECTED for the map. MINOR.**
- `runs_of(state="START")` returns 10 columns, including `nominalTime`, `jobType.*` and `sourceCodeLocation.version`, and the prose uses four of them. This is "a table nobody chose, rendered because the component had it". The next cell already passes `columns=`, so the fix is the same call.
- The map: CLAUDE.md says it appears in every chapter. Its non-use after the introduction is not a rule break. Chapter 8 draws it the same way. Reject that part. Its caption matches the three live return files.

**11. Loose ends. REJECTED, with one trivial exception.**
- The Chapter 8 `START` question is a reflective question for the learner. Chapter 9 answers it by example (the run stays `START`) and states the rule in "How this differs": "a run's state from its latest event". At most a clause belongs in finding 9's rewrite.
- A bridge to Chapter 8's small consumer would be filler under CLAUDE.md's "silence is preferable". Reject.
- The reads 5 versus writes 6 asymmetry follows from Chapter 8's fact that the `START` names the input. The surrounding text says only the write edge is lost. Reject.
- "9 to 12 seconds" is the course-wide wording, deliberately spanning the local 8.3 to 9.0 measurement and the live 11.9 to 12.1 seconds. `test_jupyterlite.py` pins it. Reject.

**Act on first**
1. Finding 1 (false continuity claim, one clause).
2. Finding 2's missing verdict, then its reorder. Fold in finding 3's uniform "what each needs" and the `record_return` case that separates readings 2 and 3, and the "Four are dropped" lean.
3. Finding 10's START table, which is a one-line `columns=` change.
4. Finding 7's "lists" to "asks for", finding 5's "41 runs over 7 nights" and the question's wording, and finding 8's "job", "version" and "Saturday" cleanups.
5. Finding 9's personification and finding 4's `r-203` clause.
6. Finding 6 is optional. Findings 11 and the rest are not worth acting on.
