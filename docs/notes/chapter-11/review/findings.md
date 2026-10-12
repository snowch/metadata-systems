REVIEW OF CHAPTER 11, "Schema evolution"

Overall: the engine numbers on the page all reproduce. The problems are in what the chapter infers from them, in the requirement section, and in continuity with Chapters 2, 6 and 10.

---

## BLOCKING

**B1. The `retyped` change breaks Jo Marsh's query because of the "C" prefix, not because of the type. The page attributes it to the type.**
Quotes:
- "`retyped`: each customer id written as text, `C101` where it was `101`."
- "The new type broke Jo Marsh's query only."
- "All 44 values are `text`, in a column the catalogue declares `INTEGER`. The warehouse keeps the text."

I patched `supplier_changes` so that `retyped` wrote `"101"` (text, no prefix) and ran the week. Results:
- `typeof(customer_id)` gives `integer`, 44 rows.
- `JO_QUERY` returns 7 rows.
- The file's schema still shows `customer_id` going from `integer` to `string`.

The shop's SQLite warehouse coerces numeric-looking text under INTEGER affinity. It keeps text only when it cannot convert it, as with `C101`. So the chapter's headline surprise is a change of key values, a different identifier format. The type change contributes nothing. A competent engineer will ask "what if it were just '101'?" The page cannot answer that, and the answer would undercut "a type change that breaks one reader and not another".
Direction:
- Either make the change a pure type change and see what the engine does, or describe it honestly as a change of identifier format that also changes the type.
- Rewrite "the new type broke…" and the diff's "retyped" label accordingly.
- Label the lenient-affinity behaviour as the shop's own where the learner first meets it (the `typeof` cell), not only in the closing note.

**B2. The requirement section contradicts itself, computes none of its verdicts, and mixes steps 4 and 5 of CLAUDE.md's five steps.**
Quotes:
- "Checked against the shop's records, each reading gives one verdict:"
- "a program that reads it: met for the new name… For the new type, the warning reaches `build_clean_orders`, which did not break;"
- "the dashboard: met, by following lineage from `build_clean_orders` to the dashboard;"

Problems:
- (a) "each reading gives one verdict" is followed by a first bullet with two outcomes: met for the rename, over-warns for the retype.
- (b) The dashboard is "met" with no qualification. By the page's own sentence in "Who reads the column", a `customer_id` warning reaches `daily_sales` and the dashboard, which did not change. So the dashboard over-warns for `retyped` too.
- (c) "Met" is never defined. It could mean a warning could be raised, a warning that is correct, or a warning raised and received.
- (d) No cell produces a warning list. `diff` and `readers` exist, but nothing combines them, or follows lineage to the dashboard, for each of the three changes. The verdicts "met" and "not met" are asserted in prose, not computed. CLAUDE.md says a figure shows what the engine computes. The learner cannot compare "who would be warned" with "who broke".
- (e) The learner commits to "whom would you warn" only after the full table of who broke. The answer is already in "What each reader gets", so the commitment is nearly trivial. CLAUDE.md wants the commitment before the other readings and before the platform's record.
- (f) There is no "I can't tell yet" outcome. The prediction is a free-text string that nothing checks.

Direction:
- Add one computed cell: for each change, the readers the shop's records would warn, set beside the readers that broke.
- Move the commitment before the counts, or make it concern the warning itself.
- Give verdicts per reading and per change, with "met" defined.

**B3. "Breaking change" is defined too broadly, and the page's own use of it is relative to a reader, not to the change.**
Quote: "A change to a dataset after which a program or a person that reads it fails or gets a different answer is a **breaking change**."

Every nightly load of new orders is a change to a dataset after which a reader gets a different answer. The definition needs a restriction to structure or format, which is what this chapter is about. CLAUDE.md says a definition must hold for every case the course will meet.

The page also uses "breaking" two ways:
- by effect on a reader, which depends on the reader, so "the new type broke… only" is a verdict about readers, not about the change;
- by compatibility rule, which is how schema registries and table formats use the word. A rename or a retype is breaking by that rule whether or not anyone reads the column. The chapter never mentions this sense, which is the most obvious second meaning of "breaking".

Direction: restrict the definition to schema or format changes, and say it is defined by effect on readers. The compatibility sense is the missing second reading of "breaking" for the requirement exercise, in addition to "breaking for whom".

---

## SHOULD

**S1. The supplier's change is described as a plan, but the data already contains it, and the framing is counterfactual.**
Quotes: "The supplier plans one of three changes… It asks whether the shop can take the change." Then: "the week with the `renamed` change", and "Version 2 was written twice, on Sunday 13 and Monday 14."

The learner starts on Monday 14 (Chapter 1). A plan cannot already have been written on Sunday and Monday. The three changes are alternative weeks, as in Chapters 2 to 6, but the page does not say so, and no sentence of the setup ties it to the requirement "Warn us…", which is about warning before a change.
Related: "the export before Saturday's row" has to be mapped by the reader to Sunday 13.
Direction: say the three are alternative weeks, or make the tense honest. Say whether the warning is meant before the change, which makes the retrospective counts a different evidence from the one the requirement needs.

**S2. The claim that column lineage cannot say whether a change breaks a program is overstated, and the experiment does not produce its evidence.**
Quotes:
- "From column lineage, a change to `customer_id` reaches `build_clean_orders`, and through it `daily_sales`. But `daily_sales` did not change. Column lineage says which programs read a column, not whether a change breaks them."
- Jo's query is "in no record".

Problems:
- (a) The `readers` cell shows only `build_clean_orders`. The step "and through it `daily_sales`" comes from Chapter 10's upstream table, which is not run here.
- (b) The lineage record already carries information that does distinguish the cases. For `customer_id` it is `value: copied` plus `rows`. Chapter 10 showed `customer_id` reaches `revenue_pence` only through `rows`, never `value`. A retype lands downstream only through copied columns, not through filter-only dependence. So lineage says more than "which programs read it", and the "over-warns" conclusion hides that.
- (c) A change of column in one string, with an output that looks the same, is a weak experiment. The prose states the lesson. The notes' driving question ("which programs would a warning about each column reach?") is never put to the learner.
- (d) The more telling run is not suggested: `column = "qty"`. I ran it, and it returns the `no_readers` message ("No program whose code the shop has reads this column."). That shows a rename's new name is read by nobody while the old name's readers break. The `MESSAGES["no_readers"]` string is otherwise never used on the page.

Direction:
- Ask the learner to predict the readers of each column before the run.
- Run `qty` as well as `customer_id`.
- Use `value` versus `rows` to say what lineage can and cannot tell.

**S3. "Object storage and the catalogue do not keep a dataset's past schemas" omits that storage keeps every past version of `orders.jsonl`.**
I checked: `week.storage.versions("s3://shop-raw/orders.jsonl")` returns 7 versions, and the `put` code states that storage keeps every version. The old file with `quantity` is still there, so the past schema is recoverable by reading it. What is missing is a record, not the information.
A data engineer will notice, especially after Chapter 7's `object_version`. The page also says "version" for a schema version (2 of them) while storage holds 7 object versions of the same file. That is the same word with two meanings, and the `diffs` column "versions of clean_orders" is not qualified.
Direction: say storage keeps old files but nothing reads them into a schema record. Qualify "version" as "schema version" at its first use and in the column header.

**S4. The chapter drops the thread Chapter 10 left, and does not connect to the head's rename questions in Chapters 2, 3 and 6.**
- Chapter 10 ends: "`SELECT *` copies whatever columns its source has when it runs… Chapter 11 changes a dataset's columns." Chapter 11 never returns to `SELECT *` or the analyst's copy. The `added` change is the natural place: what a `SELECT *` reader receives.
- Chapters 2, 3 and 6 ask "If the checkout renames a column in `orders.jsonl`, what stops working?" and "Next week we rename `customer_id` … to `customer_ref`". Chapter 6's traversal gave "the most the rename could affect". Chapter 11 uses `quantity`→`qty` with no reference to those. The learner never learns what the earlier `customer_id` rename would have done, or why this chapter chose `quantity`.
- "The checkout's supplier" is a new actor. Earlier chapters say "the checkout" renames. Chapter 10 says "the export… is not in the repository".
- Chapter 16's candidate requirement ("Tell us what breaks if `customer_id` is renamed… what keeps running and gives a wrong answer") duplicates this chapter's rename result.

Direction: close the Chapter 6 question explicitly, and use `added` to close the `SELECT *` loose end.

**S5. The best "no error" evidence is available but unused. The `renamed` result is described as silent, but the run record says otherwise.**
In the `renamed` week, the executions for `build_clean_orders` on Sep 13 and 14 show `status succeeded, rows 0, rows_read 43/48`. Chapters 4 to 7 gave the learner run records with row counts. The page says "though the program succeeded each time" but never mentions that the recorded row count was 0. So the reflective question "Would a change that empties a table without an error be caught on your platform?" is already half answered by the shop's records, and the page ignores it. It is also a missed link to Chapter 13 (a run that succeeded and wrote no rows).
Related imprecision: "`clean_orders` has no rows after the last two nights". The whole table is empty, because the file is rewritten each night with every order, so the history under the new name also yields nothing. That is why Jo's query returns 0 for `renamed`. The sentence reads as if only two nights are missing. State that the table is empty, and why.

**S6. Several instruments have no question in front of them, and the typeof cell is a missed prediction.**
- The cells for versions, diff, diffs and typeof are introduced by "The next cell…", not by a question. Their results are then restated in prose.
- The `typeof` cell holds the chapter's best surprise: a warehouse accepts text into an INTEGER column with no error. It is handed over with no prediction, although CLAUDE.md prefers an experiment to an instrument.
- The map figure is introduced with no question and serves nothing in this chapter. The notes say it serves "the assets the supplier's file feeds", but the map has no arrows (per the course rule), and its caption is about the returns desk.

**S7. The objective "Record a dataset's schema each time it is written" overclaims.**
The learner records nothing. The engine does; the learner reads outputs, writes two ungraded strings and edits one string. The plan says "The learner builds: schema versions…". Either give the learner a small building step (for example, decide what a schema version is and when two consecutive writes make one), or change the objective. "Question the head of the shop's requirement" also uses "the head of the shop's", which can be read as the head of the shop's requirement or the head of a requirement. The requirement itself is never introduced: who states it, and who "us" is, are not said.

**S8. The word "reader" has three meanings, and the table headings do not match the requirement bullets.**
The comparison table's column "reader" has the entries "rows of `daily_sales`", "days on the dashboard" and "rows of Jo Marsh's query". Those are results, not readers. The `daily_sales` table is a dataset, not a reader; the reader is `build_daily_sales`. The "days on the dashboard" row repeats the `daily_sales` row in every column, because the dashboard reads `daily_sales`; it adds no information. The requirement bullets then use "a program that reads the dataset", "the dashboard" and "somebody's own query" as the three kinds. Align these. Also:
- "writes" means a write count in the versions table and a target dataset in the readers table.
- "fields" and "columns" are mixed for a JSONL file.
- "program" and "job" are mixed (Chapter 10 also uses "program").

**S9. "Retyped" disappoints the prediction: Jo's query is not predicted.**
The prediction covers only `daily_sales`. Jo's query, which is the chapter's surprise, appears after the prediction as one more row, so "Compare these with what you wrote" can compare only one of the three rows. Jo's query is also introduced out of nowhere: the Chapter 3 to 5 Jo Marsh in finance has never had a spreadsheet or query. The learner cannot reason to it, which is the "hidden fact about the shop" CLAUDE.md warns against. Consider introducing who reads the warehouse before the prediction, or asking "who else reads clean_orders?" with "I can't tell yet" as an outcome.

**S10. The closing sentence is not supported by the chapter.**
Quote: "It could not show when two names refer to the same table, or to two different ones." The chapter never attempted tables. The nearest content is the column rename, where `quantity` and `qty` might be one column. Tie the lead-in to what the learner actually met, or cut it.

**S11. Unmeasured performance claims in the warning box.**
Quotes: "The page downloaded less than 1 MB… (measured on a computer)" and "Running every cell took 9 to 12 seconds, and the page used about 410 MB". `docs/notes/chapter-11.md` says "See `docs/notes/notebook-prototype.md`, 'Chapters 10 to 13'". That file has no such section (headings stop at "Chapters 7, 8 and 9"). The claims are copied from Chapter 10 and are not measured for this chapter. Measure, or word them as the course's earlier measurements.

---

## COULD

**C1. The OpenLineage note is imprecise.** "which lists its fields with a name and a type": per `docs/sources.md` (`SchemaDatasetFacet` 1-2-0), `name` is required and `type` is optional. The note also says nothing about how this relates to the shop's version history (the facet is a snapshot per event, with no version notion).

**C2. The "how this differs" note's first point is too late and too mild.** "The shop's warehouse keeps a text value in a column declared `INTEGER`. A warehouse that enforces declared types would refuse the value, and the program would fail instead." This undercuts the `retyped` conclusion for most real warehouses. It belongs where the `typeof` cell appears, as a labelled shop choice. The `added` case is not discussed either: a reader that infers columns (`SELECT *`) would receive the new field.

**C3. Restated tables and repeated arguments.**
- Sentences that repeat the table above them: "`added`: 7, 7 and 7, as in the plain week. `renamed`: 5, 5 and 0. `retyped`: 7, 7 and 0."; "`added`: `coupon_code` added, its values `string`. `retyped`: `customer_id` from `integer` to `string`."; "The comparison lists `quantity` as removed and `qty` as added."; "2 versions."
- "Jo Marsh's query… is in no record" is said three times: end of "Who reads the column", the requirement verdicts, and "Before Chapter 12".
- "The new name broke all three readers…" is repeated in the closing summary.
Cut what loses nothing.

**C4. Mild personification and unreferenced noun.**
- "Nothing in the records says `qty` is `quantity` under a new name. Only the supplier's notice says so." There is no notice on the page, so "the supplier's notice" has no antecedent. Say what the records do not hold.
- "Column lineage says…", "The warehouse keeps the text."

**C5. The `retyped` null case.** Null ids stay null, which is why Thursday's filter still passes. This is not stated, but it is not needed.

**C6. The sentence "Only the supplier's notice says so"** could be reconsidered: position, type and a removal/addition pair would also let a heuristic guess a rename. The page asserts that nothing in the shop's records can say so, which is true of the shop's records but not of what a system could infer.

---

## What I checked

All of the following reproduce, run from `/home/user/metadata-systems/notebook`:
- `versions(week11, "orders.jsonl")`: 2 versions, 5 and 2 writes, the timestamps.
- `diff`, `diffs()` (including `clean_orders` at 1 version under all three changes).
- The `typeof` cell: 44 text values.
- `compare_all()`: 7/7/7, 5/5/0, 7/7/0.
- `readers` for `quantity` and `customer_id` (same program, same three ways), and `qty` (no readers).
- `build_clean_orders` rows 0 on the last two nights under `renamed`, and `clean_orders` empty.
- `daily_sales` lacking Saturday and Sunday (5 rows, Sep 7 to 11).
- Storage versions of `orders.jsonl` (7).
- My pure-type experiment for B1.

I also checked: `shop/schemas.py`, `shop/week.py` and `platform.file_schema`; `docs/sources.md` for the Iceberg and `SchemaDatasetFacet` claims (supported, with the `type` caveat); Chapter 10's as-built text and the references to Chapters 2, 3, 6, 10 and 13; `docs/plan.md` for the chapter's row and the candidate requirement; `docs/style.md` and the review prompt. I did not verify the browser measurements or run the notebook in a browser, and I did not read the tests.
