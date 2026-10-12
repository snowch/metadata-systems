REVIEW OF CHAPTER 15, "Provenance" (read as a learner who has done Chapters 1 to 14)

(The reviewer returned this as text: its Write was refused. Saved as returned, its formatting kept.)

Every number the page states is right: 5150 at all four steps; lines 21, 23, 25, 27 and 22, 24, 26; 15400 for 7021, 7023, 7025; runs 014, 015, 028 and 031, 033, 034, 035; 02:30 and 08:40; 9775, 1425, 2850, 8350, 6925. The PROV bullets match `docs/sources.md`.

## BLOCKING

### 1. Step 3 of Thursday's trace attributes the rows of `clean_orders` to a run that no longer holds them
**Where:** "3. The rows of `clean_orders` for orders 7020, 7022, 7024 and 7026, written by `run-014`, `build_clean_orders`, early on Friday 11." and "`clean_orders` is read as it is now: the warehouse keeps no earlier state of a table."
**Problem:** `build_clean_orders` replaces the table every night; the rows now were written by `run-026`. The trace reads the current table and labels it with the run whose output `daily_sales` read. The agreement shows the rows have not changed since Friday, not what `run-014` wrote. On Sunday the same step names `run-033`, which happens to be the latest.
**Direction:** State what is known: `daily_sales` read the table after `run-014` wrote it; the page reads it as it is now; the rows agree, which is evidence they have not changed. One rule for both days.

## SHOULD

### 2. "The next week has the change `corrected`" is not next week
**Problem:** It is the same week run again; run numbers differ between runs of the week (`run-028` is a refresh in one and a `build_clean_orders` run in the other), unsaid.
**Direction:** Say it is the same week run again with the change; say once that run numbers belong to each run of the week.

### 3. The platform map shows a week the chapter does not use
**Problem:** The map is drawn from `run_week(["returns"])`; Thursday's trace runs in the plain week (no `returns` table); Sunday's in `corrected`, where storage holds four return files including `r-205`, which the map does not show.
**Direction:** Draw the map from the week each section uses, or do not caption a count the chapter's own week contradicts.

### 4. The Sunday result is presented as proof of what `run-034` read, but it is a rebuild
**Where:** "At 02:30:00, `returns` held `r-205` with 2 rolls, from the first version, read by `run-031`" and "`run-034` used what the first version held."
**Problem:** The shop records no state of `returns` at 02:30; `returns_as_of` rebuilds it. Reproducing 6925 is evidence, not proof.
**Direction:** Say it is a rebuilt state that reproduces the total; name what supports it and what is inference.

### 5. The chapter never says what the Sunday result means for the total
**Problem:** The dashboard still shows £69.25; the returns now recorded imply 8350 pence. Which number should a reader believe is never said.
**Direction:** Say what each total is a total of, and which the dashboard shows.

### 6. The objective and the Thursday prediction give away what the predictions ask
**Where:** "Find why Sunday's total no longer adds up from the shop's tables." and "Thursday's total is low because three orders were left out (Chapter 2)." before "decide whether the steps will then list orders 7021, 7023 and 7025."
**Problem:** The objective states the Sunday discrepancy; the Thursday question names the orders and the answer is plainly yes.
**Direction:** Objective as a question; ask for a belief the cell can contradict.

### 7. Step 4 chooses a file version by time, but the requirement section counts it as recorded
**Problem:** `build_clean_orders` records no version; the version is inferred from times. Kept, not recorded.
**Direction:** Separate "kept by object storage" from "recorded by the run".

### 8. The requirement section's verdicts are partly unsupported, and its conclusion is a fifth, unlisted need
**Problem:** "The program … from lineage" is called met though no lineage query appears; the list of four is followed by a need none covers; "these" has no noun; "does not say which" stops there.
**Direction:** Tie each verdict to the chapter; state what was left out as a reading with its need.

### 9. The definition of provenance already contains the four readings the exercise separates
**Problem:** It joins the four readings, omits people and bodies responsible (agents), and "the record" is also the page's word for the trace, which is computed, not kept.
**Direction:** Define it plainly as where data came from and how it was made; leave the readings to the requirement; say whether the shop keeps a provenance record or computes it.

### 10. Absolutes about object storage and the warehouse are the shop's choices stated as facts
**Direction:** "The shop's object storage", "the shop's warehouse"; say what real platforms keep, with a source.

### 11. The same points are made two and three times
**Problem:** The numbered list repeats the table; the version's time twice; "keeps no earlier state" three times; "what was used / what was not" three times; the `dropped=False` cell reprints the table.
**Direction:** Keep what the table does not carry; say each point once.

### 12. The "Time and memory" callout states measurements the notes say were not made
**Direction:** Measure and record.

## COULD

13. "No one of them is its source": "source" has another meaning in the course; an aphorism; the learner never changes an order.
14. Words with two meanings: "function" (SQL and the desk's), "record" (noun and verb), "rows" (table rows, file lines, a dashboard value).
15. The Sunday prediction is nearly answered by its setup; "and why" asks the learner to restate it.
16. Trace output on a phone: the `dropped` row packs three reasons in one cell; "09-11 01:00" reads as 9 November; two Sunday rows are step 3, unexplained; "made by: record_return" has no run id.
17. The version listing carries columns the question does not need (`deleted`, `order`, the identifiers).
18. The closing claims a limit no cell tested ("what was made from a return after it changed, or what a change to a column would affect").
19. Small points: "01:00" against 01:00:41; "drawn by" for a refresh; "the head of the shop's requirement"; the reality note's first bullet; "fixed aspects" unquoted; the first prediction is never compared; Chapter 14's count of 3 left out is independent evidence for the dropped rows.
