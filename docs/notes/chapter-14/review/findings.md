REVIEW OF CHAPTER 14, "Data quality as metadata" (read as a learner who has done Chapters 1 to 13)

(The reviewer returned this as text: its Write was refused. Saved as returned, its formatting kept.)

The numbers are right. The reviewer ran `shop.run_week()` and printed `quality.measurements`, `check` (both datasets), `reconcile`, `readings` and `left_out`: 7 runs; 6 rows on Tuesday 8 to 48 on Monday 14; `order_id twice` 1 from Thursday 10; `no customer_id` 3 from Friday 11; 4 failed runs on the file, 0 on the table; left out 0, 0, 0, 3, 3, 3, 3; Friday 11, 27 read and 23 written; Thursday 3 orders, 15400 pence; the facet's 27, 3 and 26.

## BLOCKING

### 1. A cross-reference points at the wrong chapter
**Where:** "`build_clean_orders` drops every order with no customer id before it writes the table. Its rule is `customer_id IS NOT NULL` (Chapter 2)."
**Problem:** Chapter 2 does not give the rule; it says "nothing on the platform records the rule that left them out". The first chapter that states `WHERE customer_id IS NOT NULL` is Chapter 6 (`chapter_06.py` line 378), checked with grep.
**Direction:** Point to Chapter 6, where the learner read the code.

### 2. The answer to the second prediction is in view, twice, before the learner commits
**Where:** "Change `dataset = "clean_orders"` to `dataset = "orders.jsonl"`. Before you press **Run below**, decide which runs will fail." The next cell: "On `orders.jsonl`, 4 runs fail: Friday 11, Saturday 12, Sunday 13 and Monday 14, each with a count of 3."
**Problem:** The answer is in the very next cell, and the earlier table already shows it (`no customer_id` 0, 0, 0, 3, 3, 3, 3 against a threshold of 0). Nothing to predict.
**Direction:** Drop the second "decide which runs will fail" and let the change be a plain act, or make the prediction worth making; word the result as conditional on having run it.

### 3. The objectives give away the first prediction's result
**Where:** "Test a rule against every run, and find why it passed on every night."
**Problem:** Read before the first prediction, it states the experiment's main surprise.
**Direction:** State what the learner does, without the outcome.

## SHOULD

### 4. "Rule" names two different things
**Where:** "writes it as a rule tested on every run", "A rule that a measurement must meet … is an **assertion**", "Its rule is `customer_id IS NOT NULL`", "While the rule stays, this assertion cannot fail", "because the rule had removed the orders".
**Problem:** "Rule" is the assertion in the first two and the job's filter in the rest. "A third test" counts tests nobody numbered.
**Direction:** "Assertion" for the check only; give the filter its own name; stop numbering tests.

### 5. The definition of assertion is awkward and narrow
**Where:** "A rule that a measurement must meet on every run, with whether it held recorded, is an **assertion**."
**Problem:** Hard to parse; requires a single measurement and "every run", which the reconcile assertion and the OpenLineage `not_null` example do not fit.
**Direction:** A stated expectation about data, and a record of whether it held; say the shop tests its assertions on every run.

### 6. The measured claims are not measured for this chapter
**Where:** "The page downloaded less than 1 MB when opened from Chapter 13's link…" and "Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory."
**Problem:** The notes say "To be done after the build."
**Direction:** Measure and record.

### 7. "The counts in the shop's events" says something the shop does not do
**Where:** The heading, and "as the shop's producer would send it with both facets."
**Problem:** The shop's events carry no quality facets; `quality.facets` builds them for this cell. The heading reads as if they travel in the events.
**Direction:** Retitle for what it is, and say in a clause that the shop's events do not carry them.

### 8. The facet output is not tied to the counts just read
**Where:** "`rowCount` is 27. … For `order_id`, `distinctCount` is 26." and "Both facets go with the dataset the run read."
**Problem:** 26 is 27 less the 1 repeat, unsaid; `quantity 0 or less` has no counterpart, unsaid; one facet is under `facets`, the other under `inputFacets`; "empty" is a fourth name for one condition.
**Direction:** Map each count to the facets and say which has no field; explain the placement in one sentence or drop the sentence; one word for the condition.

### 9. The "on the dashboard" reading is not a reading of the requirement, and no run records what tests it
**Where:** "On the dashboard: every completed order the shop took is counted in a day's revenue, against its customer." and the table row with "runs failed" blank.
**Problem:** "No order without a customer" on the dashboard would be met by a dashboard that leaves such orders out; the tested statement is completeness, a different requirement. The verdict is computed over the file, which no run records. The blank is unexplained, a chapter after "Empty is not 0".
**Direction:** State the third reading as a reading of the requirement, say what it needs and that no run records it, and why the cell is blank.

### 10. The learner commits to a meaning after the page has supplied two readings
**Where:** "Before you read on, write in the next cell what you take the requirement to mean…"
**Problem:** CLAUDE.md says the learner commits first; by now the page has given the developer's reading and run it on the file. "What should happen to one" is never developed.
**Direction:** Ask for the meaning before the developer's assertion, or say what stays open; give "what should happen" its needs or drop it.

### 11. "Rows read and rows written" has no question, and says what the learner already knows
**Where:** "A third test sets what each run read against what it wrote." and "It does not show which rule left them out, or whether it should have."
**Problem:** The notes' question is never asked on the page. What the test newly offers, catching removed rows whatever removed them, is not said.
**Direction:** Put the question first; say what the test can and cannot see.

### 12. "The count does not show whether they are the same 3 orders" contradicts the page
**Where:** "Each of the four runs counts 3. The count does not show whether they are the same 3 orders."
**Problem:** The page already says they are Thursday's three and stay in every later file.
**Direction:** Say plainly what the counts cannot tell, or remove the sentence.

### 13. The closing leaves out the requirement exercise and the facets
**Where:** "## Before Chapter 15".
**Problem:** Omits the three readings and their verdicts, and that the requirement did not say which it meant.
**Direction:** Add one sentence.

### 14. "Measurement" arrives beside Chapter 13's "observation"
**Where:** "Counts like these, recorded by each run, are measurements of it."
**Problem:** These counts are observations as Chapter 13 defined them; the relation is not stated.
**Direction:** Say a measurement is an observation, or what separates them.

## COULD

15. The first section is an instrument with no question in front of it; "`rows`: the rows." says nothing; `order_id twice` counts an order three times as 2; "now also counts" implies a change nobody made.
16. `quantity 0 or less` is introduced and never used.
17. The map shows the returns desk, which the chapter does not use; the chapter's real picture (file, filter, table, where each count is taken) is not drawn.
18. Tables are wide for a phone: constant columns (`dataset`, `at most`) and 150-character `_schemaURL` lines.
19. "The head of the shop's requirement" can be read as the head of a requirement.
20. "Data quality" is defined without a source in `docs/sources.md`.
