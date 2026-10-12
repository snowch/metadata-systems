# Review of Chapter 12, "Identity"

Reviewed as a reader of Chapters 1 to 11 only. Findings are ordered most serious first.

## BLOCKING

**1. BLOCKING. The requirement section says ingestion "joined pair 3", and that is false for pair 3 as listed.**
- Where: "That is the first reading. It compares names exactly, so it would keep pair 1 apart, which the warehouse reads as one table. Its rule for names joined pair 3, which no reading joins."
- Pair 3 is `shop.analytics.daily_sales` and `shop_dev.analytics.daily_sales`. Both are qualified.
  - `ingest.normalise` only touches names with exactly one dot (`d["name"].count(".") == 1`, ingest.py line 129).
  - I ran a dev COMPLETE event with its output named `shop_dev.analytics.daily_sales`. The name came through unchanged, so the two keys stay apart.
- What actually joined was the dev runner's unqualified `analytics.daily_sales`, which ingestion qualified with the wrong default. That is the same mechanism as pair 2 (a default filling in what a name leaves out).
  - The sentence blames "its rule for names" for a pair whose names the rule would never join.
- "That is the first reading" also contradicts the next sentence. The first reading includes pair 1 (the page lists it), and ingestion keeps pair 1 apart.
- Direction: say which step of ingestion failed (qualifying with a default) and which of the learner's pairs it resembles (pair 2, with the wrong default). Say how ingestion differs from the first reading. This is the chapter's central payoff, so it must be exact.

## SHOULD

**2. SHOULD. The requirement section does not complete steps 4 and 5 of CLAUDE.md's five steps.**
- Step 4 asks what the platform records, by which meaning. Step 5 asks which readings that record satisfies.
- The page gives a verdict only for the first reading, and a muddled one (finding 1). For the second, third and fourth readings it never says what the shop's graph or records hold.
  - The graph holds no row comparison.
  - It holds no record of an asset's environment.
  - It holds no table versions, apart from the "no versions" remark.
- Chapters 9 and 11 gave "met / not met" for each reading. This one does not.
- Direction: for each of the four readings, state what the shop's records hold and whether they meet it. Then keep "The requirement does not say which 'same' it means."

**3. SHOULD. The requirement exercise reveals the readings before the learner commits.**
- The five column headings of the `compare` table are "same text, same object, same rows, same environment, same version".
  - These are the four readings, shown before "Before you read on, write … what 'the same table' means to you."
  - The later list ("could mean four things") adds nothing the learner has not seen.
- CLAUDE.md wants commit first, then the other readings, then the record.
- Direction: either move the requirement question before the tests, or drop the "five tests" framing from the earlier cell. The tests could present the pairs without naming the readings.

**4. SHOULD. "Same environment" is a lookup the page never discloses, and the shop records no environment.**
- In `identity.py`, `ENVIRONMENTS = {"shop": "production", "shop_dev": "development"}` is hard-coded. Every object-storage key, `Orders.jsonl` included, is assigned "production".
- The page presents the column as a test of the stores. It says only "tests each pair five ways", and the reading 3 text says "It needs to know which environment holds each asset".
- No store or record in the shop says which environment holds an asset.
- Direction: say where each test's answer comes from. State that the shop records no environment for an asset, so that reading is unmet by what the graph holds. Item 2 needs the same statement.

**5. SHOULD. Several pair descriptions give their answers away above the prediction.**
- Pair 5: "which the supplier wrote on Friday 11 to test a new export". This says a separate file exists, so "no" is the only sensible answer.
  - Pair 5 therefore teaches nothing about case rules by prediction.
- Pair 3: "the developer's table".
- Pair 4: "a name for a query, which holds no rows of its own". A view is a different object, and the description says so.
- Direction: describe where each name comes from, not what it is. Or accept that the pairs mostly test the "cannot tell yet" option, and say so.

**6. SHOULD. The six-pair prediction gets no feedback.**
- The page defines identity as "What makes two names refer to the same asset" before the pairs, then asks "same asset?" without saying what "same" means.
- The notes say "cannot tell yet" is the right answer for several pairs, and that the requirement section says so. The page does not.
- After the tests, the bullets only restate the table ("Pair 4: the same rows and environment, but not the same object"). They never say what that means for the learner's answer.
- Direction: after the tests, say for pairs 4 and 6 (and the others) that the answer depends on which test is meant, and name the evidence. Do not mark an answer wrong without that.

**7. SHOULD. The first prediction rests on a rule the page does not restate.**
- Above it: "It names the tables `analytics.clean_orders` and `analytics.daily_sales`, without the database." Chapter 9's rule is stated only after the prediction ("Chapter 9's rule for names gave …").
- The notes say "Chapter 9's rule for names, stated there and here". "Here" is below the prediction.
- Chapter 9 flagged this exact failure: "where two databases hold tables of the same name, it would join tables that are not the same". The notes' "a rule … fail on a case it did not foresee" is therefore wrong.
- Direction: put a one-line reminder of the rule, as a fact and not the answer, above the prediction. Fix the notes.

**8. SHOULD. The third experiment has no question and teaches less than the notes claim.**
- The notes give the driving question "does a database for each producer keep the two tables apart?" The page asks nothing. It says "Delete the `# `…", and the result follows in the next cell.
- The notes also claim the learner learns the fix can be made "at the source, with qualified names". The page only asserts "A runner that sends qualified names needs no rule", and nothing in the cell tests it.
- Direction: add a prediction before the edit, for example what the dev run's reads and writes will name afterwards. Or let the learner test the qualified-name claim.

**9. SHOULD. The claim "it has to list each producer" is wrong.**
- Where: "The rule now lives in ingestion, and it has to list each producer."
- `databases.get(e.get('producer'), 'shop')` gives `shop` to any unlisted producer. I checked that an empty dict reproduces the original changes exactly, and the page itself says the empty list "gives the same answer as before".
- Only producers whose names are not production's need a line.
- "now lives" is also vague, since Chapter 9's rule already lived in ingestion.
- Direction: say what the per-producer table adds.
- Unmentioned limit: a producer is code, not an environment. The same runner code running in both environments would defeat this rule. This is a limit of the abstraction (CLAUDE.md first-principles step 6) and the model-versus-reality note could carry it.

**10. SHOULD. The page says the dev tables are "copies", and they are not.**
- Where: "runs it on copies of `clean_orders` and `daily_sales` in a second database of the warehouse, `shop_dev`, which holds Sunday's orders."
- `create_database` makes empty tables with the same columns. The run loads a 5-row Sunday sample.
  - `shop_dev.daily_sales` ends with 1 row, against 7 in production.
- The environment definition, "A separate copy of the platform's data and programs, kept for one purpose", overclaims. Development here is two tables and a laptop runner. Real development environments often hold synthetic data and not copies, so the definition fails CLAUDE.md's "must hold for every case".
- Direction: say what the dev database actually holds. Loosen the definition of environment.

**11. SHOULD. "Schema" has two meanings across Chapters 11 and 12.**
- Pair 2 text: "the database `shop` and the schema `analytics`". Chapter 11 used "schema" throughout for a dataset's columns ("schema evolution", "versions of the schema").
- The notes admit the collision but only the brief handled it. The page does not say the term here means a group of tables.
- Direction: avoid the word, or define it where it first appears.

**12. SHOULD. The map does not show what the chapter adds.**
- The opening map is `run_week(["returns"])`, "as Chapter 7 left them". It has no `shop_dev`, no `sales_by_day` and no `Orders.jsonl`.
- The notes claim it serves "the warehouse now holds two databases". The page does not show that.
- Pairs 3 to 5 refer to things that are not on it.
- Direction: either show the second database and the other additions, or correct the notes and move the map's job elsewhere.

## COULD

**13. COULD. The `compare` and `references` tables repeat each other.**
- `references` shows what each name names. The `same object` column of `compare` derives from the same `resolve` call, so it shows the same thing.
- The learner reads the same fact twice.
- Direction: merge the two or give the second a different job.

**14. COULD. Some `compare` columns carry nothing, and `same rows` is not defined.**
- `same text` is "no" in all six rows, by construction.
- `same version` is blank for four rows. For pair 5 it reads "no" for two unrelated objects, which is meaningless.
- "Rows" for a JSON file is the hash of its text.
- Direction: explain the baseline, drop or explain the empty columns, and define "same rows" for a file.

**15. COULD. The commentary after `references` is incomplete and out of order.**
- It comments on pairs 1, 5, 2, then defines "qualified name". Pairs 3, 4 and 6 get nothing until later.
- Direction: put the commentary in order, or put it all after the tests.

**16. COULD. The bullets after `compare` are padding.**
- They restate the table. "Pair 3: none of these." is a vague reference to the previous bullet's list.
- Direction: replace them with the inference (see item 6), or cut them.

**17. COULD. The "Before Chapter 13" closing is detached from the chapter.**
- "Nothing here shows whether the dashboard is up to date, or by which clock." is true of nearly everything, and "which clock" hints at Chapter 13's answer.
- Direction: say what this chapter's experiments could not show about identity, for example that the shop records no environment and no table versions. Then bridge.

**18. COULD. "Identity" is defined before the learner needs it, and the definition prejudges the answer.**
- "What makes two names refer to the same asset is the asset's identity." The chapter's point is that there are several "same"s.
- Direction: introduce the term after the tests.

**19. COULD. Terms and notation appear unexplained.**
- `…r-202.json@dce9388ac585` (the `@version` notation) is never explained.
- The table header "reference" and the column "names" mix noun and verb ("Pair 5 names two objects").
- "Runner" appears next to "script" without introduction.
- `dev` (the namespace) differs from "development" (the environment).

**20. COULD. The "invented" list in "How this differs from a real platform" is incomplete.**
- It lists "The developer, the view and the supplier's test file". It omits the query Jo Marsh typed in capitals, which no earlier chapter shows.
- Chapter 11's Jo query used lowercase `clean_orders` and is "in no record".

**21. COULD. The symlinks sentence drifts from the recorded source.**
- Page: "such as a file's location and the table name a catalogue gives it". sources.md records "such as a physical location and a logical table name".
- "A catalogue gives" is not in the source.
- The OpenLineage naming and Iceberg snapshot sentences match sources.md.

**22. COULD. The plan promises more than the chapter builds.**
- The plan row for Chapter 12 says "the identity laboratory: rules over namespace, name, environment and version". The learner builds no rules; they uncomment one line.

**23. COULD. The first "Pair 2" commentary and the third "Chapter 9's rule gives `shop`…" repeat.**
- Chapter 9's rule is restated in "A run in development", after the first output, and again at the start of "A database for each producer".

## What I checked

- **Documents read:** all the files you listed, and Chapter 11 and Chapter 9 as built. I skimmed Chapter 8 for how namespace, name and producer were introduced.
- **Engine reads:** `identity.py`, `ingest.py`, the `dev_events` part of `openlineage.py`, and the `dev`, `view` and `development_run` parts of `week.py`.
- **Output reproduced:** I ran `run_week(["returns","dev","view"])` and reproduced all four tables exactly.
  - The edges: 7 runs, last write `2026-09-14T02:30:21Z`, and the dev run, 1 run at `2026-09-14T10:20:04Z`.
  - The edges after the fix: the dev run writes `shop_dev.analytics.daily_sales`.
  - The `references` table.
  - The `compare` table.
  - All the pair-by-pair statements, the bullets after `compare` and the reading lists, which agree with the table.
- **Dates and objects:**
  - Wed 9, Thu 10 and Fri 11 match the object versions (r-202 versions at 09-09 and 09-10, `Orders.jsonl` at 09-11).
  - The two r-202 versions, `daily_sales` in the dashboard code, and the view `sales_by_day` over `daily_sales` (same two columns, hence "same rows") all check out.
- **Not found:** no em dashes, no "lab" or engine named on the page, no number the engine did not produce.
- **Not verifiable:** the warning-box figures (13 MB, "9 to 12 seconds", "about 410 MB") for this chapter specifically.
  - They are copied from the Chapter 9 and Chapter 11 pages.
  - `docs/notes/notebook-prototype.md` records measurements only for Chapters 3, 4, 8 and 9.
  - I found no Chapter 12 measurement and did not run a browser.
- **Sources:** the OpenLineage naming, symlinks and Iceberg snapshot claims were checked only against `docs/sources.md`. I did not re-fetch the upstream documents.
- **Style:** I read the page against `docs/style.md` and the prose-review prompt. The "Before you read on, write in the next cell" and "The next cell …" signposting is the course's pattern in other chapters, so I did not list it.
