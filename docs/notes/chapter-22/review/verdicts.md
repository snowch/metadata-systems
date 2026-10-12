# VERDICTS ON THE CHAPTER 22 FINDINGS

Count: 4 upheld, 6 partly upheld, 3 rejected. The COULD list is one verdict and counts once.

What I ran or read:
- I ran `shop.aliases.references()` and `merge()` for `last part`, `qualified` and `aliases`. The results are 1 entity of 6 references; 5 entities (2, 1, 1, 1, 1); 3 entities (4, 1, 1). These match the page and the pins in `test_engine.py` and `test_words.py::test_chapter_22`.
- I read `notebook/shop/aliases.py`, `notebook/chapter_22.py`, `docs/notes/chapter-22.md` and the plan rows for Chapter 22.
- I read the neighbouring chapters: 12 (lines 21, 76, 135, 190, 262, 314, 335), 18 (lines 262 to 289), 20 (lines 201 to 223), 21 (lines 120 to 175) and 4 (line 200).

## BLOCKING

**B1. Alias equates a program or dataset with the table it builds or reads. UPHELD.**
- The engine itself calls `CONFIGURED` "what each system's own configuration says a reference stands for". The page turns that mapping into lineage relations: "builds", "reads", "states what it reads or builds".
- Chapter 12 line 262 says a view with the same rows and environment "is another object". Chapter 4 keeps the dashboard as a type of its own. The chapter never says why this model and this dataset count as the table.
- The fix must do three things:
  - State that the shop's two configurations declare these names to stand for the table, and label that the shop's choice. Do not describe the relation as a build or a read.
  - Say in a sentence that a dataset which filtered or aggregated the table would not be an alias, and that the rule would merge it wrongly.
  - Reword the closing question "Where does each of your systems state what it reads or builds?" to match.
- The point that a configuration can be stale or wrong (Chapter 21) stands, but costs one clause. Put it in the closing "could not show" sentence (see S7), not in a new section.
- No new figure or engine feature.

**B2. The requirement exercise stops at "might merge". PARTLY UPHELD.**
- Upheld: step 5 is missing. Chapters 18 (lines 281 to 289) and 20 (line 223) say which readings the record meets. Chapter 22 ends with the hypotheticals "might merge the development table" and "might merge Jo Marsh's file".
  - The fix must give a verdict per reading, using only what the engine computes.
  - Same name: met for warehouse names (the `qualified` rule). Not met for the other names alone.
  - Same thing to the business: met only as the two configurations declare it, which is the shop's choice.
  - Across environments: the development table is kept apart.
  - Same rows: the rule never compares contents, so it is not met and not tested.
  - The page already says the development table is kept apart, so the verdict on that reading is a checkable fact.
- Upheld, and it ties to the verdicts above: the bullets are not parallel. "Across environments or not" is a scope, not a meaning of "same". The business bullet ("each system's own") describes what the rule already does, then the next paragraph says that reading "might merge the development table too". The fix is to make each reading state what it needs and not to contradict the rule.
- Rejected: "repeats Chapter 12's four meanings, choose a new candidate". `docs/plan.md` line 216 records this chapter's candidate: "the same name, the same rows, or the same thing to the business; across environments or not". The overlap with Chapter 12 is a recorded decision. Chapter 12 also already cross-references the rows reading.

**B3. "Six systems" is not true of the six references. UPHELD.**
- Events are the producers' messages, not a system. Chapter 12 line 76 calls `shop_dev` "a second database of the warehouse". The map and caption above the table show three systems.
- Objective 1 and the closing say "six systems". Objective 1 also says "a thing named like it", which is vague.
- The fix is to count references, not systems, in the objective, the opening and the closing. Say in the table's lead-in what the first column names (where each reference came from).
- Do not rename the engine column. `test_engine.py` line 811 pins the `systems` string, so change the prose only.
- "Source" is on the doubled-word list, so avoid it.

## SHOULD

**S1. The prediction asks for rule execution. REJECTED.**
- The plan's central experiment for this chapter is "predict which references merge". The surprise is the development table and the copy merging, which a learner can reason to from the stated rule. Derivability is allowed, and "Predictable: yes" in the notes is honest.
- Stating the results of the `qualified` and `aliases` runs in the same cell as the instruction is the convention in Chapter 21 (lines 160 to 163) and Chapter 12.
- One optional nit: after "all six become one entity", Chapter 21 says "Compare this with what you wrote." Chapter 22's first result paragraph has no such line. That is a sentence at most, not a finding.

**S2. The cost of merging too much or too little is asserted. PARTLY UPHELD.**
- Upheld: "Merging too much is as much a fault as merging too little" is a forced contrast, and the under-merging half has no consequence on the page.
- The fix is to drop the symmetry. State each consequence in a sentence:
  - Over-merging: the development table's runs would show in production's lineage (Chapter 12 showed this).
  - Under-merging: the model, the dataset and the table stay separate entities, so what one records is not joined to what the others record.
- Rejected: a figure that shows a graph joining or splitting. `merge()` does not touch the ingested graph, and a sentence does the job. This is not worth new engine work.

**S3. The map does not carry the chapter. REJECTED.**
- CLAUDE.md says the map appears in every chapter. Chapters 12 and 21 carry the identical figure and caption.
- The three-versus-six conflict is a prose fault, fixed under B3.
- A figure placing the six references in their systems would add no mechanism, because the table already lists them.

**S4. Claims about the development table and the CSV are not computed. PARTLY UPHELD.**
- Rejected for the development table. "Other rows in another environment" was shown in Chapter 12.
- Rejected for the complaint that Jo's file sits in the same bucket as `clean_orders_copy.csv`. The names differ and nothing on the page confuses them.
- Upheld in two parts:
  - The sentence "might merge Jo Marsh's file on the day it was exported" asserts a rows comparison the engine never makes. `daily_sales.csv` exists in no week (`grep` of `shop/week.py` finds only `aliases.py` naming it). Remove or reword that sentence when B2 is fixed. Do not add an engine feature for it.
  - The "How this differs" bullet and the notes' Originality section list the tool, its notation and the dataset as invented. They should also say that Jo's export and the file are invented.

**S5. Under `qualified`, only two of the four unmerged references are explained. UPHELD (small).**
- The page says only that the two tools' names are not warehouse names. The development table (another database) and the CSV (an object key, not a warehouse name) get no reason.
- Add one clause each. The rule reads warehouse names only, as the cell's own sentence says, so this does not conflict with Chapter 12.

**S6. The six-reference bullets repeat the table above. UPHELD.**
- The cell directly above prints the same six references with the system column. The bullets add only two things the table lacks:
  - the events' reference is a namespace plus a name;
  - the development table is Chapter 12's.
- Delete the bullets and fold those two facts into the paragraph before the table.
- Partly upheld, as a consequence: `shop_models` (the project), the `dataset:` prefix and "a model in a project" are glossed nowhere. They need one clause in that paragraph, because the table is the only other place they appear.

**S7. The closing and the reality note. PARTLY UPHELD.**
- Upheld: CLAUDE.md asks for what the experiments showed and could not show, and the closing gives only the first. The fix is one sentence on what they could not show:
  - the rules decide from names and from what two configurations declare;
  - nothing compared contents;
  - nothing checked the configurations are right (this carries the B1 stale-configuration point).
- Upheld: "The shop's rules work on six references" is not a difference from a real platform.
  - Replace it with a concrete difference. Real resolution is not a fixed list of rules over six names.
  - The `symlinks` facet is sourced already (`docs/sources.md` line 164, and Chapter 12's reality note at line 335), so reusing it costs no new source. Do not repeat Chapter 12's sentence word for word.
- Rejected: the "entity" clash with Chapter 4. The plan fixes the term, and an entity as the thing that several references name is consistent with Chapter 4's "a thing the records describe".
- Optional: one line in `docs/sources.md` saying "alias" and "entity resolution" are the course's own terms, not OpenLineage's. Do this only if the sources file already keeps such a line for other course terms.

**S8. The "Time and memory" warning is not measured for Chapter 22. REJECTED.**
- The text ("9 to 12 seconds", "about 400 MB") is identical in Chapters 10 to 23, so it is a series convention, not a Chapter 22 fault.
- `test_jupyterlite.py` pins chapters 1 to 17 only. That is a gap for all of Part V and belongs to a separate task.

**S9. The notes are incomplete. PARTLY UPHELD.**
- Upheld:
  - The `references` block lacks the instrument's two answers (the question it serves, and why the learner needs it then). Chapter 21's `claims` block has a "Serves" line.
  - The same-dataset requirement exercise has no figure block, and the "Requirements" section does not name the figure that questions the requirement, which CLAUDE.md asks for.
  - There is no block for the `qualified` step. The `aliases` block already names the experiment it completes, which is correct.
- Rejected: "Gives nothing away: options are groupings, but the page is free text". Chapter 21's notes use the same wording for a free-text cell.
- This is a notes-only fix. It should follow the page changes above, so that the notes describe the final text.

## COULD list. PARTLY UPHELD.

- "Reference" is first used without a definition, and Chapter 12 used "names". Add one clause saying what a reference is. Upheld, small, and it can go in the same paragraph as the S6 fix.
- "A thing named like it" is vague. This is handled under B3.
- Rejected: the reporting events' namespace is missing from the list (it would add a seventh form for no purpose); the returns desk needing a reason (the map is the series' standard opening); the run-below display note (every Part V chapter works this way); "which system takes the references" (low cost, low value).
