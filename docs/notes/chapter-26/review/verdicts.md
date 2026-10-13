# VERDICTS ON THE CHAPTER 26 FINDINGS

5 upheld, 6 partly upheld, 3 rejected (14 findings; the COULD items are at the end).

What I ran or read: `shop.run_week(["returns","source"])`, `lineage_graph.stored`, `check` with the stub, the reference, an `add` that fixes only `last`, and an `add` with an extra `n` field. I also ran `now`, Chapter 9's `ingest.edges` over this file (17 edges by job), and `stored(run_week(["returns"]))` (68 events). I read `chapter_09.py`, `chapter_20.py`, `chapter_25.py`, `chapter_26.py`, `shop/lineage_graph.py`, `docs/authoring.md`, `docs/plan.md`, `notebook/tests/test_jupyterlite.py` and the notes.

## BLOCKING

**1. The check's output gives away the prediction. REJECTED.**
- The layout is the Part VI convention and the one `docs/authoring.md` prescribes: "Put the question before the cell that answers it, and say in the prose to write the expectation down before running on." The page does that ("Before you read on, write in the next cell...").
- Chapters 24 and 25 use the same layout, so changing it here would break the part.
- The prose before the cell gives the facts a learner needs to predict from Chapter 20's belief: the late arrival time, and the rule `add` applies. The notes record "Predictable: yes, from Chapter 20" as the design.
- The objective names the topic, not the answer.
- If the part ever moves the check behind a control, that is a Part VI decision for all of Chapters 24 to 28. It is not a Chapter 26 fix.

**2. "The third fails" does not match the printed order. UPHELD.**
- I confirmed the printed order is whole file, Thursday, reload.
- The prose after the check describes whole file, then reload, then "The third fails", which is the reload row and it passes.
- Fix: describe the tests in the printed order, or name the failing test instead of numbering it.

**3. "The file is the one Chapter 25 built" conflicts with 82 versus 68. UPHELD.**
- I ran both weeks: 68 events with `["returns"]` and 82 with `["returns","source"]`. The extra 14 are `copy_clean_orders`, 7 nights of 2 events each.
- Fix: one sentence saying this file is Chapter 25's collector run over the week that adds the analyst's copy job, so it holds more events.

**4. "Chapter 9's edges, each with the same number of runs" versus what Chapter 9 printed. UPHELD.**
- Chapter 9's page says `daily_sales` is written in "6 runs, not 7" (cut-short line) and gives the first read of `clean_orders` as `02:30:21`.
- This chapter's table shows 7 runs and `02:30:00`.
- I ran `edges` over the stored file. It gives 7 writes, because this file has no cut line. The test compares only job, edge, dataset and run count. The learner will see two apparent contradictions with a chapter they remember.
- Fix: state that the match is with Chapter 9's method over this file, which has no cut line. Also state that this graph's times are event times (`eventTime`, `START` included), not run-end times. Fix 9 covers the second part.

## SHOULD

**5. The "now" exercise repeats Chapter 9's "current" exercise. PARTLY UPHELD.**
- Stands: Chapter 9 asked "The graph must show the current lineage" with readings that include the latest run, and the page never mentions it.
- Does not stand: replacing the requirement. The part design assigns this requirement, and the 2-day window is a new reading that only a time-stamped graph can give. "The surprise is thin" is a design opinion, not something to act on here.
- Fix: one sentence tying it to Chapter 9 ("Chapter 9 asked this of the edges by job; this graph keeps times, which adds a window"). No new exercise.

**6. The "now" table does not separate the readings, and the claims overreach. PARTLY UPHELD.**
- Confirmed by running `now`: "in the latest run" and "in the last 2 days" agree on all three rows, and `ever` is constant. `ever` as a constant comparison column is fine and should stay.
- The overreach stands: "A graph with no times on its edges can answer only 'ever'". Chapter 9 itself says the code-change reading needs a join to runs, so a bare edge graph plus run records can do more. Soften it to what the graph itself holds.
- "Each needs something different" is vague. Name what each reading needs.
- The table does not make the case that the readings differ. For `record_return` at Monday 14 09:00, the latest run (Friday 11 13:15) differs from the 2-day window (since Saturday 12 09:00). Direction: show a job where those two readings disagree. That means giving `now` a `job` parameter, which is a small engine change with a pinned test, or saying plainly that they coincide for this job and why.
- Rejected: recasting the bullets as questions. They follow Chapter 9's reading-plus-need form, which the course's own requirements pattern uses.
- Rejected: "a window" being undefined. The bullet says "last 2 days".

**7. Save and load are an objective but the learner does nothing with them. PARTLY UPHELD.**
- Confirmed: with an extra field per edge, `check` crashes with `KeyError: 'n'`, because `save` and `load` keep only runs, first and last.
- Confirmed: with any sensible `add`, the reload test cannot fail, so it teaches nothing.
- Fix on the page:
  - Say before the check that the graph is saved as one line per edge (runs, first, last) and loaded after Chapter 25's restart, the Saturday 12 one at 16:50:20.
  - Say why: the graph lives in the process and the collector's memory does not survive.
  - Reword the objective to what the learner actually does with save and load, for example that the graph survives a restart.
- Not needed: the traceback hardening, since the page never invites an extra field. If it is cheap, keep it out of scope.

**8. The "first" half of the fix has no test. UPHELD.**
- I ran an `add` that fixes only `last`. It passes 3 of 3, and its graph equals the reference's, because no late event creates an edge in the shop's week.
- Fix: a sentence saying the shop's week never exercises `first`, and why it is still the right rule. Adding an engine case is not worth it.

**9. Event time and arrival time are never separated. UPHELD.**
- "The time of each event as it arrives" and "Wednesday's `COMPLETE` arrived last, so it set the edge's last time" mix the two.
- Fix: one sentence. The graph's times are the producers' event times; arrival order only fixes the order of updates. Chapter 20 introduced the distinction.

**10. Instrument with no question in front of it. PARTLY UPHELD.**
- Stands: the `build_daily_sales` edges table has no question before it. Name the question briefly, for example what the graph says about the Sunday change (Chapter 9 and this chapter's own prose already tell the learner there was one).
- Rejected: the "now" table being an experiment without a learner action. The free-text cell before it is the action, and the notes say it completes the requirement. If wanted, classify it in the notes as the answer to the written reading.

**11. "program" versus "job", `edge` column, "file". REJECTED.**
- "Program" is the course's word for any sender: Chapters 9 and 24 use it, and `remove_return` and `record_return` are functions, not jobs. The `job` column name is the engine's, as in Chapter 9.
- "The four jobs" is not on this page (I grepped `chapter_26.py`).
- The `edge` column holds reads or writes, as in Chapter 9.
- "The file" means the collector's file throughout the page. The saved lines are called "lines".

**12. The closing is thin. PARTLY UPHELD.**
- Stands:
  - The summary says what worked but not what the experiments could not show. One line fixes that. Something like: an edge that stops appearing cannot be told apart from one that is idle.
  - "It is never too big to keep in memory" is an odd, overstated reality note. Say what differs on a real platform and that ordering by event time is the shop's choice.
- Rejected: a spec-silence bullet. The chapter makes no OpenLineage claim, and Chapters 20 and 25 already state that the specification is silent on late events and repeats.

**13. Phone width, the roughly 110-character line in `add`. REJECTED.**
- Code cells scroll inside the cell. The smoke test checks only the page's horizontal scroll.
- Other chapters have longer lines in code cells (Chapter 2's SQL).
- The stub text is pinned to the engine's `STUBS`, so wrapping it would change tests for no gain.

**14. "(measured on a computer)" is unbacked for this page. PARTLY UPHELD.**
- Confirmed: `test_jupyterlite.py` pins 9 to 12 seconds and 400 MB only for Chapters 3 to 23 (`range(18, 24)`). Chapters 24 to 28 carry the same copied callout.
- It is a Part VI-wide fault, not a Chapter 26 one. Fix: measure Chapters 24 to 28 and extend the pinned range, or reword all five at once. Do not edit this chapter alone.

## COULD items

- **"A day old" in the closing summary:** accept as a small wording fix. The wrong time was Wednesday 02:30:21, a day older than the right one, though about 30 hours old at 09:00 Thursday.
- **"Goes on from where it was":** fold into fix 7, and say what the reload restores.
- **Map caption and no relation:** rejected. Chapters 9 and 24 to 28 keep this standing map unchanged.
- **"Not seen for a week" has no answer in the week:** rejected. It is a reflective question about the learner's own platform (the oldest last time here is about 5.8 days before Monday 14 09:00).
- **Exposing `days`:** rejected, extra cost for little.
- **"Something different" is vague:** covered by 6.
- **Naming the differing edges in the failing whole-file message:** rejected. Only a badly broken `add` triggers it, and the engine change is not worth it.
