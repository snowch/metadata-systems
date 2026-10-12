VERDICTS ON CHAPTER 11 FINDINGS

I ran the engine from /home/user/metadata-systems/notebook and read chapter_11.py, schemas.py, week.py, the notes, the plan, and Chapters 6, 10 and 12.

BLOCKING

B1. retyped breaks Jo's query because of the "C" prefix, not the type. UPHELD.
- I patched `week.supplier_changes` so `retyped` writes `str(id)` ("101") with no prefix. Result: `typeof(customer_id)` gives `integer` ×44, `JO_QUERY` returns 7 rows, and `diff` still shows `customer_id` integer to string.
- So the SQLite warehouse's INTEGER affinity coerces numeric-looking text. It keeps text only for values like `C101`.
- The page says "The new type broke Jo Marsh's query only" and "All 44 values are `text`... The warehouse keeps the text". Both attribute to the type what the value format does. The page does show `C101` and says "`C101` never equals `101`", so the mechanism is half-right. The headline claim and the diff label ("retyped") are not.
- The plan decision says "The shop's warehouse keeps a text value in a column declared INTEGER", which is only true for non-numeric text. The same assumption sits in docs/lab.md and the notes.
- Fix: say the supplier changed the identifier's format (and with it the type). Replace "the new type broke" with "the new ids broke". At the `typeof` cell, label the keep-the-text behaviour as the shop's own and say numeric-looking text would be converted. Do not rebuild the engine, because the surprise (one reader broken, another not) survives. Update the plan, lab and notes sentences.

B2. Requirement section. PARTLY UPHELD.
- (a) UPHELD. "each reading gives one verdict" is followed by a bullet with two outcomes (met for the rename, over-warns for the retype).
- (b) UPHELD. The page says "the dashboard: met". The notes (step 5) say "for programs and the dashboard... over-warns for the new type". By the page's own `customer_id` argument, `daily_sales` and the dashboard did not change under `retyped`. The page dropped the notes' qualification for the dashboard.
- (c) UPHELD, small. "Met" is undefined. One clause fixes it: "a warning could be raised from the shop's records".
- (d) REJECTED. Chapter 10's requirement section is also prose over earlier figures. The plan says only "the figure answers only what the platform does". A new cell per change would widen the chapter without need.
- (e) PARTLY UPHELD. The `whom_to_warn` cell comes after the counts and after "Jo Marsh's query is in no record", so the answer is already given. The reviewer's fix (commit before the counts) clashes with the term ration, because "breaking change" is introduced in "What each reader gets". Fix: keep the position, but change the cell to ask something the table has not answered, such as what the shop would have to record to warn each kind of reader.
- (f) REJECTED. Free-text strings are ungraded in every chapter, and "the requirement does not say for whom" is already the offered outcome.
- Fix for the upheld parts: state the verdicts per reading and per change, with the dashboard over-warning for `retyped`, and define "met" in one clause.

B3. "Breaking change" is defined too broadly. PARTLY UPHELD.
- UPHELD: "A change to a dataset after which a program or a person that reads it fails or gets a different answer" also covers every nightly load of new orders. CLAUDE.md says a definition must hold for every case. Fix: restrict it to a change to a dataset's structure or format, and say the definition is by effect on a reader.
- REJECTED: adding the registry and table-format compatibility sense. It is not in docs/sources.md, needs new sourcing, and widens the chapter. The plan's candidate is "breaking for which reader". The page's use ("broke all three readers") is consistent with its own effect-based definition.

SHOULD

S1. "Plans" versus data already containing the change. UPHELD, minor.
- The page says "The supplier plans one of three changes... from the export before Saturday's row", then reports "Version 2 was written twice, on Sunday 13 and Monday 14". This is a tense clash. Chapters 6 and 10 use "in the week with the X change".
- Reject the sub-point that retrospective counts differ from the "warn before" evidence. That is the exercise's point.
- Fix: say the three are alternative weeks, and that the changed export first appears on Sunday 13, the night that writes Saturday's row.

S2. Lineage claim and weak experiment. PARTLY UPHELD.
- UPHELD: before the run, the page says "The same program reads `customer_id`, in the same three ways". That gives the cell's result away (I confirmed it is true). Fix: ask what the learner expects (does the same program read it, and does that mean `daily_sales` breaks?) before stating anything.
- UPHELD, small: "and through it `daily_sales`" is not shown by the cell. It follows from Chapter 10's rows dependence, so cite Chapter 10 instead of implying the cell shows it.
- REJECTED (b): that `value: copied` versus `rows` tells whether a retype breaks a reader. A filter on a string column may or may not survive a retype, so the reviewer's rule is not general. The page's claim is defensible.
- REJECTED (d): running `qty`. It gives the `no_readers` message, but it widens the chapter.

S3. Storage keeps every past version of the file. UPHELD.
- I confirmed `storage.versions` returns 7 versions of `orders.jsonl`. "Object storage and the catalogue do not keep a dataset's past schemas" omits that old files survive. Chapter 7 uses `object_version`.
- Fix: say storage keeps old files but nothing reads their fields into a record. Qualify "version" as "schema version" at first use and in the `diffs` column header.

S4. Threads from Chapters 2, 3, 6 and 10. PARTLY UPHELD.
- UPHELD, one sentence: Chapters 2, 3 and 6 asked what renaming `customer_id` affects. The `customer_id` readers cell is the answer, so say so.
- REJECTED: closing the `SELECT *` loop. `clean_orders` stays at 1 version under every change, so a `SELECT *` copy would receive the same columns. Nothing happens without new engine work.
- REJECTED: "supplier" as a new actor (the model-versus-reality note says it is invented), and Chapter 16's duplicate (out of scope).

S5. Run record and empty table. PARTLY UPHELD.
- UPHELD: "`clean_orders` has no rows after the last two nights" reads as if only two nights are missing. I confirmed the table is empty (0 rows), because the file is rewritten each night. Fix: say the table is empty, and why.
- REJECTED: adding "rows 0, rows_read 43/48". That I confirmed, but the plan assigns "a run that succeeded and wrote no rows" to Chapter 13.

S6. Instruments without a question. PARTLY UPHELD.
- REJECTED: the map. It is the standing opening in Chapters 7 to 10. The notes' "serves" line is odd, but that is a notes issue only.
- REJECTED: questions before the `versions`, `diff` and `diffs` cells. Those are plain steps, and questions there would be filler.
- UPHELD, optional: the `typeof` cell could take a question first. Do it together with the B1 rewrite.

S7. The objective overclaims. PARTLY UPHELD.
- UPHELD: "Record a dataset's schema each time it is written" is something the engine does, not the learner. Chapters 8 to 13 use "Find", "See" and "Read". Fix: reword to "Read the shop's record of a dataset's schema at each write, and compare two versions".
- REJECTED: the "head of the shop's requirement" wording. Chapter 12 uses it, and the notes record it as a deliberate edit.
- REJECTED: "who is 'us'". It follows the Chapter 10 pattern.

S8. "Reader" used loosely. REJECTED, mostly.
- It is a wording nit. If touched, rename the table's first column header to "what is counted".
- Do not drop the dashboard row: the plan names it as a reader, and the pinned tests hold it.
- "Fields" versus "columns" for JSONL follows Chapter 10.

S9. Jo's query is not predicted, and appears from nowhere. REJECTED.
- The plan's prediction is "which changes break `daily_sales`". The surprise at Jo's query is the plan's intended one ("a type change that breaks one reader and not another"). The prediction cell concerns `daily_sales` only, so nothing hidden is being guessed.
- Jo Marsh is established in Chapters 3 to 5 as the finance owner of the dashboard. The prose introduces the query before the counts ("Jo Marsh's own query, which runs in a spreadsheet").

S10. The closing sentence is unsupported. UPHELD, low.
- "It could not show when two names refer to the same table" is about tables, which this chapter never touched.
- Fix: tie it to what the learner met (`quantity` and `qty` as two names compared as text), or cut it.

S11. Measurement claims. UPHELD, being fixed, but the reviewer's evidence is wrong.
- docs/notes/notebook-prototype.md does have "## Chapters 10 to 13" (line 318). It has a Chapter 11 column: 15 files, 0.32 MB; Run all 7.8 to 8.9 s; peak 395 to 402 MB alone and 621 MB with Chapter 10 open.
- The warning's "9 to 12 seconds, about 410 MB" is the section's rounded envelope, which it states in its last paragraph.
- Re-measure as planned, but the "section is missing" assertion should be dropped.

COULD

- C1. UPHELD, trivial accuracy fix. Per docs/sources.md, the `SchemaDatasetFacet` `type` is optional. Write "a name and, optionally, a type".
- C2. Covered by B1 (move the shop-choice label to the `typeof` cell). The `added` and `SELECT *` point is REJECTED (see S4).
- C3. UPHELD. The sentences restating the tables and the repeated "in no record" can go.
- C4. UPHELD, a good catch. "Only the supplier's notice says so" has no antecedent, because no notice appears on the page. Say what the records do not hold, or "only the supplier could say".
- C5. REJECTED. It is not needed.
- C6. REJECTED. The sentence is true of the shop's records.
