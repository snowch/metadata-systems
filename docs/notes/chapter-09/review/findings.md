REVIEW OF CHAPTER 9

I read the as-built text, `notebook/chapter_09.py`, `docs/notes/chapter-09.md` and `shop/ingest.py`, and re-ran the week to check every number. All the stated counts hold:
- 82 lines, 1 refused, 81 events passed.
- 26 normalise changes, split 12 and 14.
- 7 jobs, 41 runs, 12 datasets, 6 unknown facets.
- 80 edges by run and 17 by job; `build_daily_sales` has 5, 6 and 2 runs on its three edges.
- 13 of the 17 edges by job remain in the latest-run view.
- With the `# ` removed, the unknown list is empty and the change and version columns appear.

The findings are about continuity, order, teaching and wording. Most serious first.

---

**1. BLOCKING. Chapter 9 contradicts Chapter 8 about the analyst's script.**
- Where: first section, "The events come from the jobs, from the functions, and now from the analyst's script, which has sent its own since Chapter 8."
- Chapter 8 says: "The analyst's copy sends no events. The analyst writes the two events of Friday 11's copy by hand." The learner sent one pair of hand-written events to a consumer, for one night.
- Chapter 9's week has the script sending events on all 7 nights (14 events). `docs/plan.md` says the script sends events "from Chapter 9", not Chapter 8.
- A learner who finished Chapter 8 will stop at this sentence.
- Direction: say what changed between the chapters, in the learner's terms: the analyst now has the script send its events. Do not claim it sent them in Chapter 8.

**2. BLOCKING. The requirement section shows the platform's record before the readings, and never says which readings it meets.**
- Where: section `"The graph must show the current lineage."`
- The order breaks CLAUDE.md's five steps.
  - The learner writes what "current" means to them.
  - The page then states "The cell after it lists, for each job, the edges its latest run had", and `found.latest()` prints the 13 edges. This is one reading presented as the graph's answer.
  - Only afterwards does the page list "three things" "Current" could mean.
- CLAUDE.md says the other readings come first, each beside what it needs, then the record, then which readings the record satisfies.
- The section has no step-5 verdict. It ends: "The requirement does not say which "current" it means." That says the requirement is ambiguous. It does not say which readings the shop's edges meet. Chapter 8's section ends with "As written, the shop meets the requirement for…", and `docs/notes/chapter-09.md`, "Requirements" item 5, claims such a verdict.
- Direction: list the readings with what each needs, then show the record. Show more than the latest-run view, or at least say that this view is one reading's answer. End by saying which readings the edges satisfy and which they cannot.

**3. MINOR (borderline blocking). The three readings are not equally concrete or queryable.**
- Where: the three bullets after "'Current' could mean three things, each needing something different".
- Bullets 1 and 2 state what they would show ("all 17", "the 13 edges"), not what each needs.
- Only bullet 3 names a need: "the code version of each run".
- `found` (the edges by job) has no code version, and its by-run rows carry only the run id. So the closing claim "The edges by job keep the first and last time, so a query can choose" holds for readings 1 and 2 and not for reading 3. The notes' "each reading can be queried" overreaches.
- Readings 2 and 3 are never separated by a case from the shop. For `build_daily_sales` they give the same edges. For `record_return` the code never changed in the week, so reading 3 would keep every file edge and reading 2 would not. The page does not say so.
- Reading 1, "as of the last event received", is really "all edges, no filtering". It does not cover the other natural meaning given the opening ("kept up to date"): the graph has ingested everything received so far. The cut line is exactly a case where it has not.
- Direction: state each reading's need in the same form, and say which readings the current edges can and cannot answer. Consider using `record_return` to separate readings 2 and 3, and adding the freshness meaning or saying why it is left out.

**4. MINOR. Four dropped edges cannot be checked, and the `record_return` bullet drops a file without saying why.**
- Where: "Four are dropped: `build_daily_sales` reads `clean_orders`…" and "For `record_return` it also drops `r-201.json` and `r-202.json`, whose rows are still in the table `returns`".
- The 17-edge table is never shown, so the learner cannot see what was dropped. The 13 rows are in job order with `build_daily_sales reads copy` stranded in the last row.
- The first sentence names three `record_return` files; the bullet names two. `r-203.json` is left out silently. The reason is that `remove_return` deleted it and its row is gone. I checked: `returns` holds r-201, r-202 and r-204.
- `remove_return` has no edge to `r-203.json` in this graph (its reads are empty). That is a visible gap in a chapter about what the events record, and the page never mentions it.
- Direction: show or list the dropped rows, and account for `r-203` in one clause.

**5. MINOR. The edges prediction does not line up with the numbers it is checked against.**
- Where: "how many edges between jobs and datasets you expect, and why: about as many as one night's reads and writes, or about seven times as many."
- The stage makes two kinds of edge. By-run edges run between runs and datasets, not between jobs and datasets, so the question fits only one of the two counts shown. The labels also drift: "run edges | job edges" in the table, "edges by run" in the prose.
- The ratio of the two counts shown is not seven (80 against 17). One night's edges are not 17 either, since 17 includes the returns files and the copy.
- Neither written expectation is revisited afterwards. No sentence returns the learner to what they wrote. The notes' "either answer was half right" never reaches the page.
- Same pattern for the parse prediction: the answer arrives in three places (the START run, then "6 runs, not 7", then the summary) with no point that says "compare with what you wrote".
- Direction: align the question with the two counts, and add one sentence after the counts that returns the learner to their expectation and says what it was right and wrong about.

**6. MINOR. Normalising times is never motivated or shown.**
- Where: "Producers write the same thing in different ways. The functions' producer writes times with `+00:00`; … Both mean UTC." The definition is "rewrite such things in one form, so that the same thing is written the same way."
- Only names have a consequence the learner can see ("would not join `clean_orders`, as in Chapter 8"), and even that is asserted, not shown.
- For times the page gives no reason. The cost is real: `objects()` sorts events by the `eventTime` string, and a run's state depends on that order. In this week's data nothing changes.
- When I ran `objects` on the un-normalised events I got 13 datasets, not 12. The change is small and checkable.
- Direction: give times a reason, and let the learner skip the stage and see the one difference it makes. The 26-row table also holds 24 near-identical rows. The sentence below it carries the pattern, so the table could be shorter or grouped.

**7. MINOR. The unknown-facet section misdescribes its first cell and tells the result before the learner acts.**
- Where: "The cell after it lists the runs of `record_return`: when each started, what it read, and the change and the version from the facet `shop_objectChange`."
- The cell asks for those columns and silently gets none. The output shows only started and reads. The sentence reads as if the change and version are listed, so a learner may think the cell is broken. Use "asks for".
- The paragraph then gives the cause ("the stage did not read the facet"), then the edit, then the result ("The list of facets it does not know is empty, and each run … shows whether its file was created or overwritten").
- The notes say "Gives nothing away: the prose says what to remove, not what appears". The page does say what appears.
- The 6-row `objs.unknown` table repeats full run UUIDs for one facet name.
- Direction: reword the description. Let the learner see the effect before reading it. Consider counting by facet instead of listing six UUID rows.

**8. MINOR. Words that carry two meanings.**
- "7 jobs (the four jobs, the two functions and the analyst's copy)": "job" in one sentence means the stage's job object and, a few words later, the nightly programs only.
- "Objects" as a stage and heading (jobs, runs, datasets) sits beside "object storage" and `shop_objectChange.object` (a stored file). The stage name is never explained.
- "version" appears as the code version, the dataset version and the file version, with "the change and the version from the facet" left bare.
- "Saturday" is the data row from which the code changed ("as the code since Saturday does"), the last run reading `clean_orders` (Saturday 12), and the first run reading the copy (Sunday 13, new code version). Make the dates match.
- "41 runs over 7 nights" includes 6 daytime function runs.
- Edge names vary: "run edges", "edges by run", "edges between jobs and datasets".

**9. MINOR. Personification and unnatural phrasing.**
- "To the stage, the run looks as though it is still working."
- "so to the graph that run wrote nothing"
- "The stage then knows the facet."
- Say what the stored record shows instead: the run has no end time and no outputs.
- The opening list "four stages: parse, a stage that rewrites the events in one form, objects and edges" mixes shapes and hides the name "normalise". The heading names the stage later.

**10. MINOR. Tables nobody chose.**
- `objs.runs_of(state="START")` returns one row with 10 columns, including `nominalTime`, `jobType.*` and `sourceCodeLocation.version`. The prose needs state, started, ended and reads. A phone shows this row mostly off-screen.
- The platform map above the cells is never used or referred to after its introduction. It shows `["returns"]` only, without the copy or the `source` change, while the chapter states 12 datasets. Chapter 8 has the same figure, but there the cells used it.

**11. MINOR. Loose ends.**
- Chapter 8 ends by asking "What should a consumer do with a `START` whose run never sends another event?" The Chapter 9 run keeps the state `START` with no statement of what the shop's stage does or should do with it.
- Chapter 9 never says how its ingestion relates to Chapter 8's small consumer (one row per run, a lineage query), which already did part of the same job.
- `build_daily_sales` shows reads 5 + 2 = 7 but writes 6. The reads include Wednesday because the `START` names the input (Chapter 8's own fact). The page never says so, so the asymmetry may puzzle a learner.
- The page's "9 to 12 seconds" for Run all does not match the notes' measured 8.3 to 9.0 seconds. The memory figure of about 410 MB matches.

No em dashes or "lab/engine" wording found in the chapter source. Numbers not listed above held.
