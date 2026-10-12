Verdicts on the 23 findings on Chapter 12. I read the page, notes and engine and ran the engine where a claim was checkable. Findings 1 to 12 are the SHOULD and BLOCKING ones; the rest are COULD.

**1. BLOCKING, "joined pair 3". PARTLY UPHELD.**
- Real defect: the sentence is false as written. Pair 3 is two qualified names, and `normalise` only qualifies names with exactly one dot (`d["name"].count(".") == 1`).
  - I confirmed the dev events name `analytics.clean_orders` and `analytics.daily_sales` with no database.
  - The normalise changes at lines 69 and 70 show those two names becoming `shop.analytics.…`.
  - So what joined was the dev runner's unqualified name, qualified with the wrong default. That is pair 2's mechanism with the wrong default.
- Rejected part: "That is the first reading" does not contradict "keeps pair 1 apart". Ingestion implements reading 1 only partly: it qualifies but compares exactly. That is a fair imperfection, not an inconsistency.
- Fix: say that ingestion qualified the dev runner's unqualified names with production's database, the pair-2 mechanism with the wrong default. Say that it compares qualified names exactly, so it would keep pair 1 apart. Make the same correction in notes item 5.

**2. Steps 4 and 5 incomplete. UPHELD.**
- The page gives a verdict for reading 1 only. Chapters 9 and 11 give one verdict per reading ("met", "not met").
- Fix: state, for each of the four readings, what the shop's records hold (no row comparison, no environment, no table versions) and whether they meet it. Keep "The requirement does not say which 'same' it means."

**3. Readings shown before the commit. PARTLY UPHELD.**
- The `compare` headings ("same text, same object, same rows, same environment, same version") are the four readings. They sit before "write … what 'the same table' means to you", so the commit is primed.
- The five tests are the experiment's instrument, though, and the contamination is mild.
- Fix: put the "what does 'the same table' mean to you" cell before the `compare` cell, or stop calling the columns "five ways" in the prose before it. Do not restructure further.

**4. "Same environment" is an undisclosed lookup. UPHELD.**
- `ENVIRONMENTS = {"shop": "production", "shop_dev": "development"}` is hard-coded, and `resolve` returns `"production"` for every s3 key.
- The column therefore shows "yes" for pair 5 from a constant, and the page presents it as a store test.
- Fix: say the environment answers come from the database names the shop uses (`shop` is production, `shop_dev` is development, and object storage has one environment). State that the graph records no environment for an asset, and feed that into finding 2.

**5. Pair descriptions give answers away. PARTLY UPHELD.**
- Pair 4's "a name for a query, which holds no rows of its own" states what the object is, and so settles it. Pair 3's "the developer's table" does the same.
- Pair 5's provenance ("wrote on Friday 11 to test a new export") is needed to make the pair meaningful, so keep it.
- Fix: describe pairs 3 and 4 by where the name comes from ("a view Jo Marsh made over `daily_sales`"). Drop "holds no rows of its own".

**6. No feedback on the six-pair prediction. PARTLY UPHELD.**
- The requirement section's per-reading pair lists do the work two cells later. But no text says that the answer depends on which test is meant, or that "cannot tell yet" was fair for pairs 4 and 6.
- Fix: after `compare`, add a short passage saying that "same asset?" depends on the test used, with pairs 4 and 6 as the examples. Merge this with finding 16.

**7. First prediction rests on an unrestated rule. UPHELD.**
- Chapter 9 line 147 already foresaw this exact failure: "where two databases hold tables of the same name, it would join tables that are not the same."
- So the notes' "fail on a case it did not foresee" is wrong.
- The page states the rule only after the prediction.
- Fix: put one factual line above the prediction ("the stage adds `shop` to a warehouse name that leaves out its database"). Do not give the result. Correct the notes' Consequence line.

**8. Third experiment has no question. PARTLY UPHELD.**
- The notes' driving question and "learns the fix can be made at the source" are not on the page.
- "A runner that sends qualified names needs no rule" is true (the rule only touches one-dot names) but untested on the page.
- Fix: add a one-line question before the edit (what will `dev/build_daily_sales` write after the change?), or at least state the claim as a fact. Trim the notes' objective to what the page does. Do not build a new experiment.

**9. "It has to list each producer". UPHELD.**
- `databases.get(e.get('producer'), 'shop')` defaults any unlisted producer to `shop`, and the page says the empty list "gives the same answer as before".
- "now lives" is also vague, since the rule already lived in ingestion.
- Fix: say only producers whose names mean another database need a line. Add one sentence on the limit: a producer is code, not an environment, so the same runner run in both environments defeats the rule. That limit fits the model-versus-reality note.

**10. "Copies". PARTLY UPHELD.**
- `create_database` makes empty tables with the same columns. The run loads a 5-row Sunday sample: `shop_dev.clean_orders` has 5 rows against 44, and `shop_dev.daily_sales` has 1 row against 7.
- The page's "which holds Sunday's orders" is accurate. "Copies" and "A separate copy of the platform's data and programs" overclaim, and real development environments often hold synthetic data.
- Fix: say "tables of the same names and columns", and define an environment as "a separate set of the platform's data and programs, kept for one purpose".

**11. "Schema" collision. UPHELD, low priority.**
- Pair 2 says "the schema `analytics`". Chapter 11 used "schema" for a dataset's columns, and Chapter 8 used it as the group of tables.
- Fix: avoid the word ("the group `analytics`"), or define it there.

**12. Map does not show what the chapter adds. PARTLY UPHELD.**
- `figures.py` has no notion of `shop_dev`, so showing the second database would be engine work outside this chapter.
- The caption's "Monday morning, as Chapter 7 left them" is honest, and the map precedes the dev run.
- Fix: correct the notes' "Serves" line ("the warehouse now holds two databases"). Do not extend the figure.

**13. `compare` and `references` repeat. REJECTED.**
- `references` shows which object each name resolves to (case, defaults). `compare` gives only yes/no per test. They do different jobs.

**14. Empty or meaningless columns, "same rows" undefined. PARTLY UPHELD.**
- "Same text" all "no" is a legitimate baseline: it shows that text fails as a test. Blank version cells are explained by the page's last sentence.
- "Same rows" for an object (a hash of its text) is undefined.
- Fix: one sentence defining "same rows" (a table's rows, or an object's contents).

**15. Commentary after `references` out of order. REJECTED.**
- It is grouped by mechanism (case, then defaults, then the term). The remaining pairs are covered after `compare`. This is stylistic, with little benefit.

**16. Bullets after `compare` are padding. UPHELD.**
- They restate the table, and "Pair 3: none of these." is a vague reference.
- Fix: replace them with the inference passage from finding 6.

**17. Closing detached. UPHELD.**
- Chapter 11's closing says what its experiments could not show about its own topic. This one's "Nothing here shows whether the dashboard is up to date, or by which clock" is Chapter 13's subject, and "which clock" hints at Chapter 13's answer.
- Fix: say what identity's experiments could not show: the shop records no environment and no table versions, and the stage compares no rows. Then bridge to Chapter 13.

**18. "Identity" defined too early. REJECTED.**
- The pairs question raises the term, and the chapter title carries it. The definition leaves the several "sames" open.

**19. Unexplained notation. PARTLY UPHELD.**
- The `@version` notation in pair 6 is never explained.
- Fix: one sentence ("`@` followed by a version names one version of the object").
- The runner/script, noun/verb "names" and `dev`/development points are rejected as trivial.

**20. "Invented" list omits the capitals query. UPHELD, small.**
- Pair 1's query typed in capitals is invented and appears in no record.
- Fix: add it to the list.

**21. Symlinks sentence drifts from the source. UPHELD, small.**
- sources.md says "a physical location and a logical table name". "A catalogue gives" is not in it.
- Fix: use the source's words.

**22. Plan promises more than the chapter builds. PARTLY UPHELD.**
- The plan row says "the identity laboratory: rules over namespace, name, environment and version". The learner changes one rule.
- Do not widen the chapter. At most, reword the plan row to match the build (a database per producer in ingestion).

**23. Chapter 9's rule restated. REJECTED as a separate finding.**
- The sentence after the first output explains the result, and the one in "A database for each producer" sets up the fix. With finding 7's reminder added, check that the three do not read as repeats, and trim the weakest.
