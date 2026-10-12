Verdicts on the Chapter 14 findings (an independent sceptic, on another model; returned as text and saved here)

Checked against CLAUDE.md, the as-built chapter, the notes, `notebook/chapter_14.py`, `shop/quality.py`, `shop/week.py`, `shop/openlineage.py`, `tests/test_words.py`, Chapters 2, 6, 11, 12 and 13, `docs/plan.md`, `docs/sources.md` and `docs/notes/notebook-prototype.md`. The numbers match the page. The term gate forbids "assertion" in the objectives, and its anchor is the heading "## A rule tested on every run".

1. Cross-reference to Chapter 2. UPHELD. Chapter 2 never gives `customer_id IS NOT NULL`; Chapter 6 (line 378) does. Fix: "(Chapter 6)" in that sentence; the other two "(Chapter 2)" are right.
2. Second prediction has nothing to predict. PARTLY UPHELD. The pattern of result text after an edit is the course's (Chapters 11 and 12), not a fault; but the first table already shows the answer, so it is a read-off. Fix: delete only "Before you press **Run below**, decide which runs will fail."
3. The objective gives away the result. UPHELD (SHOULD). Fix: an action, without "assertion": test a condition on the table and on the file, run by run.
4. "Rule" names two things. PARTLY UPHELD. Keep "rule" for the job's filter, as earlier chapters use it; give the assertion "test" on first appearance; "A third test" becomes "Another test"; mirror a renamed heading in the term gate's anchor.
5. Definition of assertion. PARTLY UPHELD. Fix: "A stated expectation about data, with a record of whether it held in each run, is an **assertion**."
6. Measured claims. PARTLY UPHELD. The page's claims are measured (`notebook-prototype.md`, "Chapters 14 to 17"); the notes' "Measured" section must say so. Re-measure once published.
7. Heading "The counts in the shop's events". UPHELD. Retitle ("The counts as OpenLineage facets") and add that the shop's events do not carry them and the cell builds them.
8. Facet output not tied to the counts. PARTLY UPHELD. Add that 26 is 27 less the 1 repeat; say the facet has no field for `quantity 0 or less`; "rows with no customer id" for "rows where it is empty". Reject explaining `facets` against `inputFacets`.
9. Dashboard reading and its blank cell. PARTLY UPHELD. Drop "against its customer"; add "No run records this reading.", which also explains the blank. Reject recasting the reading.
10. Commit after the readings are supplied. PARTLY UPHELD. Move the "what do you take it to mean" prompt and cell to just after the requirement is quoted, before the developer's reading. Reject developing "what should happen to one".
11. "Rows read and rows written" has no question. PARTLY UPHELD. Open with the question (could a run's own two counts show it left rows out, whichever rule removed them?); keep "does not show which rule", the course's "what can the data not tell" beat.
12. "The count does not show whether they are the same 3 orders". UPHELD. Delete it: a repeat of what the page has said.
13. Closing omits the requirement exercise. PARTLY UPHELD. Add one sentence of the three verdicts and that the requirement does not choose. Reject adding the facets.
14. "Measurement" beside "observation". PARTLY UPHELD. "…are observations of the data a run read and wrote"; do not rename the code.
15. Instrument with no question; "`rows`: the rows."; "now also counts". REJECTED. The question is Chapter 13's closing gap, restated.
16. `quantity 0 or less` unused. REJECTED. It is the control for Chapter 2's rule that no row triggers.
17. The map. REJECTED. Every chapter opens with the map; a new figure would widen the chapter.
18. Wide tables. REJECTED. The constant columns echo the reader's edit; the phone smoke test passes.
19. "The head of the shop's requirement". REJECTED. The course's idiom since Chapter 1.
20. "Data quality" without a source. PARTLY UPHELD. Record a source actually read, or reword to what the sources support. Not blocking.
