VERDICTS ON CHAPTER 7

Method: I checked every quote against chapter_07.py and the as-built page. I checked the claims against the engine by running `shop` (`readings`, `events`, `runs`, `lineage`, the `source` and `failed` changes), `shop/week.py`, `shop/runs.py`, `shop/figures.py`, Chapters 2 to 6, the chapter notes and CLAUDE.md. All quotes are exact. The reviewer's numbers are right, with two small slips noted below. The findings overcall severity: nothing here is a wrong fact. Two or three are real defects in what the experiments show, and the rest are cheap fixes or preferences.

**1. "Answer to Jo" stated as if events showed it. PARTLY. Real, but MAJOR, not BLOCKING.**
- Quotes are exact.
- The events do carry only counts. The causes ("second copy of order 7015", "Thursday's three orders with no customer id") come from Chapters 2 and 3. Chapter 3 already says "Thursday's three orders with no customer id (7021, 7023 and 7025...)". The Friday 11 step is therefore a confirmation of what the learner knows, not a discovery. I verified the series 0, 0, 1, 4, 4, 4, 4 and the dates.
- The page does attribute the 1 to "Chapter 2's rules", so it is not hiding its source for that row. It never says the events cannot name the orders.
- That breaks CLAUDE.md "After a result, ask what it proved ... and what the data could not tell". It does not break a hard rule, and the numbers are right.
- The overstatement point is weak. "Nothing on the platform keeps what an earlier night did" is about what the job did each night, which is a record of work. Recomputing from raw orders is not a record. Only a clause is needed, not a rewrite.
- Direction: compatible. Add one or two sentences: the events give counts per run and the step on Friday 11, and the orders and the rule come from Chapters 2 and 3. Do not reword the "nothing keeps" sentence beyond a clause.

**2. Wednesday prediction nearly answered. PARTLY. Real hint, MAJOR/minor, not BLOCKING.**
- The quote is exact. The clause "because each job runs once a night" hands over the cadence, which is the reason the prediction asks for.
- Any engineer who knows GROUP BY answers "1" anyway, and the notes admit "Predictable: yes". The deeper weakness is that the prediction is nearly trivial, not that one clause leaks it.
- The "no text gives away an exercise's answer" rule (CLAUDE.md "A figure shows only what the learner has been told", plus the prediction rules) supports removing the clause or moving it after the result. That is a one-sentence fix.
- Direction: compatible. Moving the clause after the result is right. Asking what the single row will stand for (how many runs) is better than "how many rows, and why", and it also fits "effect before cause".

**3. "Without reads" conclusion. UPHELD in substance. The label "self-contradictory" is overcalled. BLOCKING is defensible, and this is the most important finding.**
- The quote is exact.
- It is elliptical, not contradictory. It says absence of `reads` is indistinguishable from a run that read nothing, and `remove_return` is the example.
- The flaw is real. The `with_run` table that shows `remove_return` has no `reads` column, only `rows_read` 0. The learner has never seen its `reads`. In the engine it is `''` on the start event, not `None`, which is immaterial because both print blank. `record_return`'s `reads` is a file path.
- The lineage cell uses `week`, which has no functions. Deleting `"reads"` therefore shows only that no `reads` field means no edges, which is true by construction and which Chapter 6 already teaches. The experiment never shows the indistinguishability the closing sentence claims.
- The prediction is answerable from Chapter 6 alone. That fails CLAUDE.md "A prediction is built around what the learner should learn".
- "really" is also an intensifier (style rule 19).
- Direction: compatible. I would go further than the reviewer. Build the lineage from the returns week, so `remove_return` appears as a node with a `writes` edge and no `reads` edge. That is the same picture the learner gets when `reads` is deleted. This is engine-computed and fits the rules. At minimum, show `remove_return`'s `reads` before the claim, or drop the example.

**4. Sunday 13 against Chapter 6's "from Saturday". UPHELD. MAJOR. BLOCKING is generous but not unfair, and it is a one-sentence fix.**
- Both quotes are exact. Chapter 6: "from Saturday, `build_daily_sales` is changed to read the copy". Chapter 7: "The runs on Sunday 13 and Monday 14 read ..."
- `week.py` uses `day >= "2026-09-12"` (Saturday's row). The 02:30 run on Sunday 13 writes it.
- Chapter 7's own table is correct. Chapter 7 itself asks "on which nights", and a reader will see "Saturday" then "Sunday" with no bridge, on exactly the question this section answers.
- Direction: compatible. Add one sentence that the run at 02:30 on Sunday 13 writes Saturday's row. Chapter 6 could also say "from Saturday's row on", as `week.py` does.

**5. Returns-desk figure. REJECTED, apart from a minor flow label.**
- The caption does date the figure: "on Monday morning". Earlier chapters set the story on Monday 14, and the figure shows exactly that state (r-201, r-202, r-204, which is 3 files; I checked the rendering).
- The figure draws no relation, so "a figure shows only what is told" is not broken.
- The claim that it reveals the deletion early is weak. The page has already said deletion starts `remove_return`, and r-203 is not yet named when the figure appears.
- The label "jobs nightly; functions at any hour" does sit on both arrows, which is imprecise. That is cosmetic.

**6. Requirement section. PARTLY. MINOR, with two real points.**
- Real: the bullets repeat the table's reading and needs columns. That is the same argument made twice, an easy cut.
- Real: "any design meets 'Record every run.' if each run sends events" sits uneasily beside the chapter's own finding that without `run` runs merge. I confirmed `readings(['job','type'])` gives "no" on all four rows. The sentence is the intended "meets as written" pattern (the Chapter 2 owner example), but it needs one qualifying clause about `run`.
- Fair but small: no `status` value is ever shown. The `failed` change exists in the engine, but this chapter's week has no failed run, and the Chapter 6 closing promised "whether it succeeded". A crashed program sends no `status` at all; reflective question 2 gestures at this.
- Staging is mostly compliant. The learner commits first (`meaning`, `yours`) and the table then shows readings, needs and met. The four readings are not named before the commit. The "platform's record" step is the learner's own design, so collapsing steps is defensible.
- Questioning what `time` and `status` mean, and the missing `job` in the needs lists, are preferences, not rule breaks.

**7. Objective overstates. REJECTED, apart from a tiny point.**
- The learner does choose fields in `yours`, and may edit `design`. "Design the messages a program sends" is fair.
- Reflective question 2, "In your design, which events exist...", mismatches slightly, because the design lists fields and the events are always start and finish. This is trivial.

**8. Engine rows. PARTLY. MINOR.**
- Real: the merged Wednesday row shows `rows_read` 1 and `rows_written` 1. `runs()` lists distinct values only, so two runs that each read 1 show as 1. This hides a count in the very row that demonstrates merging. A clause or an engine choice would fix it.
- Tiny: `remove_return` has `rows_written` 1 for a removal, against the field's definition "how many rows the program wrote". One clause covers it.

**9. Numbers and wording. PARTLY.**
- UPHELD, and a real rule hit: "five and a half hours" is a number in words that the engine did not produce. 10:05:02 to 15:40:05 is 5 h 35 m. This breaks CLAUDE.md "a number spelled as a word that the engine did not produce" and style rule 12. Use the two times alone, or a computed span.
- UPHELD, small: "which programs the shop did not write can read" has an ambiguous "which". Use "that".
- Preference only: "seems to be made from nothing" is concrete and mirrors Chapter 6's "seems to affect". "The runs recorded" is mild agency. The closing "Nothing here shows..." is a meta-sentence, but it names the limit and leads into Chapter 8.
- The fragment "The three systems, in the order data moves through them each night." is identical to Chapter 6's line, so it is a course convention. Changing it is a course-wide decision. REJECTED here.

**10. Terms and tables. PARTLY, item by item.**
- UPHELD: the "What each run read" table is 13 columns wide. Three are empty for `build_daily_sales` (`object`, `object_change`, `object_version`). The reviewer said "five", which is wrong. This is "a table nobody chose for this question". Pass a narrower design.
- UPHELD, and important: the `lineage` cell uses `week`, not `changed`. I ran `changed`: the upstream graph has 7 nodes and includes `s3://shop-scratch/clean_orders_copy.csv` as a dead end with no writer. The page does not say it uses the original week. That is an unexplained choice, and it also hides a richer, engine-computed result. It could be fixed by saying so or by switching.
- UPHELD, small: `object`, `object_version` and `object_change` appear in the fields table before any function exists, and no earlier chapter mentions object versions. The "How this differs" note should say real buckets give a version identifier only with versioning enabled. This is plausible but not in `docs/sources.md`, so check the source first.
- UPHELD, small: `time` cannot tell runs apart "because start and finish differ" is weak. Pairing each start with the next finish works for the non-overlapping Wednesday runs. One clause saying it fails for overlapping runs or a missing finish would fix it.
- PARTLY: the field `job` holds the function names (`record_return`), and "program" is used before "function" is defined. One clause suffices. "The next cell runs the week ... and lists the runs" mixes the verb and the noun in one sentence, but it follows Chapter 6's precedent.
- REJECTED: the undefined `started` and `finished` columns are self-explanatory.

**Act on first, in order:**
1. #3 (and #10's `lineage` using `week`): rebuild the experiment so it shows the empty-versus-absent case, probably from the returns or changed week.
2. #4: one sentence tying Sunday 13 to Saturday's row.
3. #1: say what the events cannot name.
4. #2: move the "because each job runs once a night" clause after the result.
5. #9: the "five and a half hours" number, plus the ambiguous "which".
6. #6, #8 and the remaining #10 clauses: low-cost sentence edits. Skip #5 and #7.
