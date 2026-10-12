Verdicts on the Chapter 15 findings (an independent sceptic, on another model; returned as text and saved here)

Checked against `notebook/chapter_15.py`, `notebook/shop/provenance.py` (the plain, `returns` and `corrected` weeks run), `docs/sources.md`, `docs/lab.md`, `docs/notes/notebook-prototype.md`, the notes, and Chapters 10, 13, 14, 16 and 17. Confirmed: `run-014` wrote 23 rows, `run-026` 44, and the table now is `run-026`'s; `run-014` and `run-034` record no version, and `run-034` records its reads as `clean_orders` only; `record_return`'s runs record the version they read. The engine was being changed while the sceptic worked (step 3 labelled "as it is now" with the latest run, full timestamps, left-out rows one per line).

1. Step 3 attributes the table's rows to `run-014`. UPHELD (SHOULD). Keep the engine change; say `run-015` read the table after `run-014` wrote it, and the table now was last written by `run-026`; the same rule for Sunday.
2. "The next week". REJECTED. The course's idiom; no run number is cited across weeks.
3. The map. REJECTED. The standing opener; its caption is true of the week it draws.
4. The Sunday result as proof of what `run-034` read. UPHELD. "The rebuilt `returns` held…"; the shop does not record that `run-034` read `returns`, and the rebuilt state reproducing 6925 is the evidence.
5. What the Sunday result means for the total. REJECTED. The page says what 6925 is; which number to believe is left open, and answering would widen the chapter.
6. The objective and the Thursday prediction give away answers. PARTLY UPHELD. Objective: "Check whether Sunday's total adds up from the shop's tables, and find what it adds up from." Ask instead what reason the steps will give for each of the three orders.
7. The file's version is chosen by time, not recorded. UPHELD. Say it was kept by object storage and chosen by the time `run-014` started, and `run-014` did not record it.
8. The requirement's verdicts. PARTLY UPHELD. Delete "A record of what was used does not show what was left out…", or make it "None of the four readings asks for the rows each run read and left out." Do not add a fifth reading.
9. The definition of provenance. PARTLY UPHELD. Define it plainly (information about where a piece of data came from and how it was made); say separately what the shop's trace is built from, computed from the run records.
10. Absolutes about storage. PARTLY UPHELD. "The shop's object storage", "the shop's warehouse". Reject a sourced survey of real platforms.
11. Repeats. PARTLY UPHELD. Cut the requirement-section sentence of 8 and the duplicate "current when `run-014` started" paragraph; the list adds the times, and the `dropped=False` cell is the experiment's control.
12. The measurements. REJECTED for the page (measured, and pinned by `test_jupyterlite.py`); fill the notes.
13. "No one of them is its source". PARTLY UPHELD. "The total is made from four orders together; none of them alone is where it came from."
14. Two meanings. PARTLY UPHELD. "The SQL function `returned_quantity`". Reject the rest.
15. The Sunday prediction's setup. REJECTED. The learner still has to work out the times.
16. The trace's output. PARTLY UPHELD. The full timestamp and one row per left-out line fix it; the prose's "01:00" must follow the version's 01:00:41.
17. The version listing's columns. REJECTED.
18. The closing's limit. REJECTED; optionally say the trace starts from a total and cannot start from a return or a column.
19. Small points. Mostly REJECTED; mark "with some fixed aspects" as PROV-DM's words.
