# Sceptic's verdicts (12 October 2026)

Verdicts on the 22 findings for Chapter 3. I checked quotes against the as-built and after-edit pages, Chapter 2 (round-17), `notebook/shop/records.py`, `week.py` and `platform.py`, and ran the engine for finding 4.

1. UPHELD. The steps box says "Run all" first, and the prediction cells say "Before you run the cells below". After Run all or Run below, every output already sits under each prediction. Chapter 2 does not use "before you run", so the wording is new to Chapter 3 and false of the page as met.

2. PARTLY. The message says Jo "decides what counts as revenue" and "built the dashboard". It does not say who is responsible for the table `daily_sales`. The head also hands only the two cleaned tables to the learner, so who looks after `daily_sales` is unstated. Chapter 2 had just said the owner question needs "a person or a team". The page turns this into `responsible: Jo Marsh` and says the record "answers" the fourth question without comment, so that part holds. The point that the lookup "returns what you typed" is weak. That is true of any written record and is not an overstatement in itself.

3. PARTLY. These parts hold:
   - The heading and the closing question ("when a table's meaning changed") mislabel what changed. Jo's meaning is the same, and the table has moved away from it.
   - The page runs two detectors, `records.check` (columns) and the value comparison against Jo's meaning, then speaks as if "the check" were one.
   - "which version of the job's code wrote each row" differs from Chapter 2's "which version of the job's code ran each night" and the plan's "code version" per run.

   The "would have shown the edit" overreach is weak. The value comparison shows an effect, not that the job's code changed, and the page's claim is defensible as worded.

4. PARTLY. The reviewer's evidence is wrong. `daily_sales` is written with `append=True`, so its row count grows by one each night (1 to 7), and it does not have 7 rows every night. Chapter 2's "still has 7 rows" compares the final state of the edited and unedited weeks. The page's claim is still false for `clean_customers`. That table is replaced with the same 9 rows each night: row count 9 and bytes 1463 stay constant, and only the last-altered time moves. So the claim "change with every write" is overbroad. It holds for `daily_sales` and `clean_orders`, which grow. Size does follow the rows, as the reviewer says.

5. UPHELD. The page says row count, size and last-altered "record what happened to the table". Chapter 2 says the platform "records the current state of each asset and none of its history" and "The systems do not keep ... what happened to it". Row count and size are current state, not events. The creator is sorted as "what happened" and the owner as "what it is", with no criterion given.

6. UPHELD. All three quotes are in the as-built page and the screen contradicts them:
   - The "names Jo Marsh" sentence sits above "........".
   - "the check reports nothing" sits under a two-problem output.
   - "the 12 columns" sits above a 14-row table.

   This follows from the pre-edit Run all state and is partly cured by fixing finding 1.

7. PARTLY. Chapter 2's wording is "about an asset or about the platform". Chapter 3 says "an asset, or the work done on the platform", so the second wording is real. `updated_by` is arguably a fact about an edit, and the page asserts "business data" without spelling out the criterion. The page does imply it ("a fact about each product"), and a product is not one of the platform's assets, so "blocking" is too strong.

8. UPHELD. "Record" means a set of lines ("A record is a set of lines"), a kind of information ("Records of the first kind"), a verb ("The warehouse records"), a single item ("An operational record"), and the check's plural "The records do not describe". "Jo Marsh's meaning" and "Jo Marsh's description" both appear for one thing.

9. UPHELD. The example `daily_sales revenue_pence unit: pence` is the fifth line of the cell with the dots filled in.

10. PARTLY. The result follows from what the learner wrote: all five lines are about `daily_sales`, so "No rows." cannot fail. "The last cell" is misleading, because many cells follow. The reviewer's "eight sections follow" is a miscount. The cell is the last of its own section.

11. PARTLY. The decision is announced in the paragraph before the cell ("keeps each completed order once, even an order the export wrote twice"), then discussed. So the ordering and repetition point holds. "Overstates the ambiguity" is arguable pedantry. Whether duplicate lines count is a real ambiguity in "every completed order".

12. UPHELD (minor). Chapter 2 showed raw totals differing on Tuesday, Wednesday, Thursday and Saturday. Here Jo's meaning agrees on all of them except Thursday, and the page does not say why (cancelled and duplicate orders are excluded). The data-only description agrees with the data by construction, and the page does not say so.

13. UPHELD. The prompt asks whether one line meets "Every column must have a description", which one line cannot do. The `means` value already says "in pence", and "needs a `unit` line" comes from the notation. "Under the other readings" has no listed first reading, and "met as written" is the check's rule.

14. UPHELD. The same sentence is repeated 14 or 12 times. The check can tell "no means line" from "dots" (see `written()` in `records.py`), but the message hedges with "or". "Still only dots" is false for a table the learner wrote nothing about.

15. UPHELD. The record string starts with a newline, so its first line is numbered 2, while `by_name` starts at 1 (its `daily_sales` lines are 13 and 14). The `line` numbers are never explained.

16. UPHELD (minor). The `no_column` and `no_asset` paths are never triggered in the chapter. The `responsible` and `unit` fields are never checked either.

17. UPHELD. "Next, you write what you have learnt ... then ask Chapter 2's four questions again" is roadmap narration. Chapter 2 has no step where the learner asks the head who decides what `daily_sales` should count. A grep for "asked" and "decides" in Chapter 2 finds nothing, and the only head's message there is "Thursday's revenue looks wrong."

18. UPHELD. No question precedes the `updated_by` count. The next sentence restates the output ("The cell counts `k.adeyemi` 3, `r.novak` 2 and `s.lund` 3"), and 3+2+3 = 8 is correct.

19. PARTLY. The warehouse, storage and dashboard paragraphs largely restate Chapter 2's "What the platform holds". "A key ... says what the file is" overstates what a name and location tell you. "No action" overstates, because the section does contain the `information_schema` cell.

20. PARTLY (weak). Chapter 3 never shows the namespace sense of `schema`. That sense appears in Chapter 2's `table_schema | analytics` output. Chapter 2 also already introduced `information_schema`. The collision is real but cross-chapter and minor.

21. PARTLY.
   - The second question (a description versus the column's name) can be read as hypothetical, so "presupposes it can" is arguable.
   - The third question is partly answered in the chapter (Chapter 7 operational records).
   - None of the three leads towards Chapter 4, which holds.
   - The identity point is fair: the head's message and `j.marsh` strongly imply the same person, and no record states it.

22. PARTLY. The two objectives are awkward, and the second mixes the requirement test with the change test. The summary omits the requirement result, which was an experiment. It also omits the descriptive/operational sort, but that is exposition and not an experiment result, so that omission is weak.

Summary: No finding is wholly rejected, but several are overstated. Finding 4's evidence is factually wrong. `daily_sales` is appended nightly and grows from 1 to 7 rows, but the page's claim still fails for `clean_customers`. Findings 2, 3 and 7 rest on real problems but overreach in places: the lookup "returns what you typed" point, "would have shown the edit", and "blocking" for 7. The strongest findings are 1, 5, 6, 8, 13, 15 and 17, which are borne out by the page, Chapter 2 or the engine. 9, 12, 14, 16 and 18 are valid minor points. 10, 11, 19, 20, 21 and 22 are partly valid and need trimming before they are acted on.
