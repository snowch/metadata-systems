(A reviewer on another model, reading as a learner who has done Chapters 1 to 21; returned as text and saved here.)

# REVIEW OF CHAPTER 22, "Identity across systems"

Numbers checked: I ran `shop.aliases.references()` and `shop.aliases.merge(rule)` for `last part`, `qualified` and `aliases` from `/home/user/metadata-systems/notebook`. They give 1 entity of 6 references, then 5 entities (2+1+1+1+1), then 3 entities (4+1+1). The page's counts, "Qualified names merged two references" and "merged four" all match, and `notebook/tests/test_engine.py` and `test_words.py` (`test_chapter_22`) pin them. I read `shop/aliases.py`, `chapters 2, 3, 4, 8 and 12`, `chapters 18 and 21` (requirement pattern), `docs/plan.md`, `docs/sources.md` and `docs/notes/chapter-22.md`. I did not run the notebook in a browser, so cell rendering, Run below and the phone layout are unchecked.

## BLOCKING

**B1. "Alias" and the merge equate a thing that builds or reads a table with the table itself.**
- Quotes:
  - "Another name a system uses for an asset, stated by that system, is an **alias**."
  - "The model `shop_models:daily_sales` builds `shop.analytics.daily_sales`. … `Daily sales` reads `daily_sales`."
  - "The `aliases` rule merges by what each system states it reads or builds"
- What the engine does: `CONFIGURED` maps both references to the table, so one entity holds "four references: the warehouse's, the events', the transformation tool's and the reporting tool's".
- Problem: "builds" and "reads" are lineage relations (job to asset, dataset to asset), not statements of identity. A model is a program that builds a table. A reporting dataset that reads a table is not shown to be that table.
- Contradiction inside the course: Chapter 12 pair 4 found that a view over `daily_sales` has "the same rows and environment, but is another object". Chapter 6 and Chapter 4 keep `job` and `dataset` as separate types. Chapter 22 never says why this dataset is a bare mirror, or why a model is a name for its output.
- Direction: either state that these two systems declare a name for the output, rather than a read or build relation, or show the difference between "is" and "reads". Say what the rule would do wrongly if a dataset filtered or aggregated the table. As written, the chapter teaches that a lineage statement is an alias.
- Related: the alias is trusted without question. Chapter 21 just taught that systems' claims conflict, and this chapter does not mention that a configuration can be stale or wrong.

**B2. The requirement exercise omits the last of the five steps: which readings the record meets.**
- Quotes:
  - "The `aliases` rule merges by what each system states it reads or builds, and it keeps the environments apart. A reading of "the same thing to the business" might merge the development table too. A reading of "the same rows" might merge Jo Marsh's file on the day it was exported."
  - "The requirement does not say which it means."
- Problem: CLAUDE.md "Question the requirement" step 5 requires the page to say whether the record meets the requirement as written and as meant. Chapter 18 does this ("met with at least once, not without it"). Chapter 12 does it ("The same name: met in part…"). Chapter 22 ends with "might merge" hypotheticals and no verdict on the four readings.
- Related: the four bullets are not parallel.
  - "across environments or not" is a scope, not a meaning of "same".
  - "the same thing to the business: someone's statement, or each system's own" already describes what the `aliases` rule does. The page then says that reading "might merge the development table too", which contradicts that.
- Related: three of the four bullets repeat Chapter 12's "four meanings" (name, rows, environment) almost word for word. That is the same argument made twice. Direction: choose a candidate that is new in this chapter, or make the new reading (a system's own statement) the centre.

**B3. "Six systems" is not true of the six references.**
- Quotes:
  - "Read the six references that six systems make to `daily_sales`" (objective)
  - "Six systems name `daily_sales`, or something named like it, in six ways."
  - the `references()` column `system`, which lists "events" and "development warehouse".
- Checks:
  - The events are not a system. They are the producers' messages, named by namespace and name.
  - Chapter 12 says the development database is "a second database of the warehouse", so it is not a second system. The shop has three systems, and the map above the table shows three.
- Problem: "system" means different things within one page, and the count contradicts the map. Direction: use "references from N places", or say which references share a system.

## SHOULD

**S1. The prediction asks for rule execution, not for a belief.**
- Quote: "Before you read on, write in the next cell which references this rule will merge."
- Problem: the rule is stated in full just above, including the exact edge cases ("in lower case, with spaces and hyphens read as underscores, and a file's extension left off"). Anyone can compute the answer by hand, and the notes call it "Predictable: yes".
- What the learner might believe instead is whether this rule is good, or what it would join that they would not want joined. The cell does not ask that.
- Related: the `qualified` and `aliases` steps have no prediction at all. The results are printed in the same cell as the instruction ("The result has five entities…", "The result has three entities. One of them holds four references…"), so the learner reads the outcome before running. That may be acceptable as "say the thing", but it leaves the chapter with a single, trivial commitment.
- Also: the page says the dev table and the CSV are copies "among them" after the result, which is the right order. The tell-then-run order for the other two rules is the weaker one.

**S2. The cost of merging too much or too little is asserted, and nothing shows it.**
- Quotes:
  - "Merging too much is as much a fault as merging too little: the development table's runs would show in production's lineage."
  - "Under that rule, all six become one entity."
- Problem:
  - Under-merging (5 entities under `qualified`) has no stated consequence at all, so "as much a fault" is not supported on the page.
  - Over-merging relies on Chapter 12's graph, which is not re-shown.
  - `merge()` never touches the ingested graph from Chapters 8, 9 and 12. The whole chapter is a table of groups of strings, so the learner never sees a lineage graph join or split.
- "As much a fault as" is also close to the forced-contrast aphorism the voice rules reject.
- Direction: the chapter's gap is the effect on lineage. Show it, or drop the claim.

**S3. The map at the top does not carry what the chapter needs.**
- Quote: "The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table `returns`."
- Problem:
  - The chapter is about `daily_sales`, a transformation tool, a reporting dataset, a development database and a CSV in `shop-scratch`.
  - The figure is `run_week(["returns"])`, with no `dev` change. It shows none of those, and it shows three systems against the "six systems" claim.
  - The caption is about return files, which are not used in this chapter.
  - CLAUDE.md says a diagram should carry what the passage makes the reader hold in mind, and this chapter's six references and their systems are exactly that.
- Direction: either drop it for this chapter, or make a figure that places the six references in their systems.

**S4. Claims about the development table and the CSV are not produced by the engine.**
- Quotes:
  - "Among them are the development table, which holds other rows in another environment, and Jo Marsh's CSV file, a copy made at one time."
  - "A reading of "the same rows" might merge Jo Marsh's file on the day it was exported."
- Checks:
  - `shop/week.py` has `s3://shop-scratch/clean_orders_copy.csv`, but no `daily_sales.csv`, and no table exists in the page's week (`run_week(["returns"])`).
  - The development table exists only under the `dev` change. It holds a sample of Sunday's orders there.
- Problem:
  - `shop.aliases` is six hard-coded strings. Nothing computes "other rows" or "a copy made at one time".
  - CLAUDE.md requires a number or fact the learner reads to be an engine output.
  - The "How this differs" list says the tool, its notation and the dataset are invented. It does not say that Jo's export and the file are invented too. Jo's CSV also sits in the same bucket as the analyst's `clean_orders_copy.csv` from Chapter 2, and nothing separates the two.
- Direction: compute it, or reduce the claim.

**S5. Under `qualified`, the page explains only two of the four unmerged references.**
- Quote: "The other four references each stay alone. The transformation tool's name and the reporting tool's name are not warehouse names."
- Problem:
  - Nothing says why the development table stays alone (a different database) or why the CSV does (an object storage key).
  - The learner is left to infer that the rule cannot read non-warehouse names.
  - The CSV's reason also conflicts with Chapter 12, where object storage keys are read by their own exact rules.

**S6. The six-reference list repeats the cell directly above it.**
- Quote: "These are the six references, with the system each came from:" followed by six bullets.
- Problem: the preceding cell already lists the six references and their systems ("The next cell lists the six references, and the system each came from."). The bullets repeat it with the same content, so the learner would not miss them.
- Direction: keep only what the table does not hold.
- Undefined or unexplained notation on the page:
  - the `dataset:` prefix in `dataset:Daily sales`
  - `shop_models` (is it the project?)
  - "a model in a project" (not explained)
  - the dataset is written both as `Daily sales` and `dataset:Daily sales`

**S7. The closing lacks what the experiments could not show, and the "differs from a real platform" note is thin.**
- Quotes:
  - "The shop's rules work on six references."
  - "The transformation tool, its notation and the reporting tool's dataset are invented for the course."
- Problems:
  - The summary says what happened. CLAUDE.md asks for what the experiments could not show as well.
  - The second note ("The shop's rules work on six references") is not a difference from a real platform. The note says nothing about what real platforms do. OpenLineage's naming rules and its `symlinks` facet (a standard's own alias mechanism) are in `docs/sources.md` and in Chapter 12's note, but Chapter 22 does not use them.
  - It also leaves unsaid that real resolution is not a fixed ordered rule list.
- Unsourced terms: `docs/sources.md` has no entry for "entity resolution" or "alias" as the course uses them. They are definitional claims, not OpenLineage terms.
- "Entity" now means a group of references. In Chapter 4 it was a thing the records describe.

**S8. The "Time and memory" warning's measurements are not recorded for this chapter.**
- Quotes: "the first time you open it on its own your browser downloads about 13 MB", "The page downloaded less than 1 MB when opened from Chapter 21's link … (measured on a computer)", "Running every cell took 9 to 12 seconds, and the page used about 400 MB of memory."
- Check: the text is identical to Chapter 12's. `tests/test_jupyterlite.py` pins these claims only for chapters 1 to 17. A grep of `docs/notes/notebook-prototype.md` finds nothing for chapters 18 to 23, and the page's own compute is tiny. In Python, `run_week` twice plus the merge took 0.14 s.
- Direction: measure Chapter 22, or reword.

**S9. The chapter's notes are incomplete.**
- `docs/notes/chapter-22.md` lists `references` as "**Role:** inspect" only. It lacks the two answers an instrument must give: the question it serves, and why the learner needs it then.
- There is no block for the `qualified` step or for the requirement.
- `last-part` says "Gives nothing away: options are groupings", but the page asks for free text.
- Its "Requirements" section lists the same readings as the page without saying which figure questions them.

## COULD

- "Read the six references that six systems make to `daily_sales`, or to a thing named like it." is vague ("a thing named like it"), and it makes the references personified.
- "Chapter 12 tested pairs of references inside the warehouse and object storage." Chapter 12 calls them "pairs of names". "Reference", "name" and "entity" are used interchangeably in this chapter, and "reference" is not defined.
- "The shop's metadata system takes references from more systems than those." Which system takes them, and from where, is not clear. Nothing in the chapter changes the learner's own system.
- "Another name a system uses for an asset, stated by that system, is an **alias**." The sentence is clumsy, and it does not give the sense in which the transformation tool's model name is an alias (see B1).
- The footer reflective question "Which of your systems name the same table differently?" is fine. "Where does each of your systems state what it reads or builds?" repeats the B1 conflation.
- "As Chapter 7 left them" repeats Chapter 12's identical sentence. Acceptable, but the learner has no way to tell why Chapter 22 needs the returns desk.
- The learner is told "Select the cell and press **Run below**" and edits `"last part"` in place. After Run all, the output shows only the first result, and the next two results exist only in prose until the learner edits. This follows the other Part V chapters, so I do not rate it above COULD.
- The list of references omits the reporting events' namespace (`reporting://shop-reporting`, Chapter 8 line 458), so the dashboard's dataset appears in only one form here.
